#!/usr/bin/env python3
import argparse
import copy
import datetime as dt
import hashlib
import hmac
import json
import os
import re
import secrets
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


HOME_DIR = Path.home()
OPENCLAW_HOME = Path(os.environ.get("OPENCLAW_HOME", str(HOME_DIR / ".openclaw"))).expanduser()
CONFIG_PATH = Path(
    os.environ.get("OCGUARD_CONFIG_PATH", str(OPENCLAW_HOME / "openclaw.json"))
).expanduser()
BACKUP_DIR = Path(
    os.environ.get("OCGUARD_BACKUP_DIR", str(OPENCLAW_HOME / "config-backups"))
).expanduser()
LOG_PATH = Path("/tmp/openclaw-config-guard.log")
ERROR_PATH = Path("/tmp/openclaw-config-guard-last-error.log")
LAST_PROPOSAL_PATH = Path("/tmp/oc-guard-last-proposal.json")
LAST_PLAN_PATH = Path("/tmp/oc-guard-last-plan.json")
OPENCODE_DEBUG_PATH = Path("/tmp/oc-guard-last-opencode-output.txt")
OPENCLAW_BIN = Path(
    os.environ.get("OCGUARD_OPENCLAW_BIN")
    or shutil.which("openclaw")
    or str(HOME_DIR / ".npm-global/bin/openclaw")
)
OPENCODE_BIN = Path(
    os.environ.get("OCGUARD_OPENCODE_BIN")
    or shutil.which("opencode")
    or str(HOME_DIR / ".npm-global/bin/opencode")
)
RECEIPT_SECRET_FILE = Path(
    os.environ.get("OCGUARD_RECEIPT_SECRET_FILE", str(OPENCLAW_HOME / ".ocguard_receipt_secret"))
).expanduser()


SECRET_RE = re.compile(r"(secret|token|apikey|api_key|password)", re.IGNORECASE)
ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")
ALLOWED_PATH_PREFIXES = (
    "/channels",
    "/bindings",
    "/agents",
    "/models",
    "/messages",
    "/commands",
    "/gateway",
    "/plugins",
    "/tools",
)
SUPPORTED_CHANNEL_IDS = {"feishu", "telegram", "discord"}
NON_EXEC_MARKER = "【模型说明-未执行】"
ALLOWED_TOOLS_EXEC_ASK = {"off", "on-miss", "always"}


def log(msg: str) -> None:
    line = f"[{dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}"
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


class GuardError(Exception):
    def __init__(self, message: str, status: str = "失败", code: int = 1):
        super().__init__(message)
        self.message = message
        self.status = status
        self.code = code


class GuardArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        raise GuardError(f"参数错误：{message}", status="阻断", code=2)


def fail(msg: str, code: int = 1, status: str = "失败") -> None:
    ERROR_PATH.write_text(msg + "\n", encoding="utf-8")
    log(f"ERROR: {msg}")
    raise GuardError(msg, status=status, code=code)


def run(cmd, timeout=60, check=True, env=None):
    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, check=check, env=env)


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def dump_json(path: Path, data) -> None:
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def mask_value(path: str, value):
    if SECRET_RE.search(path):
        s = str(value)
        if len(s) <= 8:
            return "****"
        return s[:4] + "****" + s[-4:]
    return value


def get_receipt_secret() -> str:
    env_secret = os.environ.get("OCGUARD_RECEIPT_SECRET", "").strip()
    if env_secret:
        return env_secret
    RECEIPT_SECRET_FILE.parent.mkdir(parents=True, exist_ok=True)
    if RECEIPT_SECRET_FILE.exists():
        return RECEIPT_SECRET_FILE.read_text(encoding="utf-8").strip()
    secret = secrets.token_hex(32)
    RECEIPT_SECRET_FILE.write_text(secret + "\n", encoding="utf-8")
    os.chmod(RECEIPT_SECRET_FILE, 0o600)
    return secret


def build_request_id() -> str:
    return f"{dt.datetime.now().strftime('%Y%m%d-%H%M%S')}-{secrets.token_hex(2).upper()}"


def build_signature(request_id: str, operation: str, status: str, content: str) -> str:
    digest = hashlib.sha256(content.encode("utf-8")).hexdigest()
    payload = f"{request_id}|{operation}|{status}|{digest}"
    sig = hmac.new(get_receipt_secret().encode("utf-8"), payload.encode("utf-8"), hashlib.sha256).hexdigest()
    return sig[:12].upper()


def emit_receipt(operation: str, request_id: str, status: str, content: str) -> None:
    body = content.strip() if content and content.strip() else "无"
    sig = build_signature(request_id, operation, status, body)
    status_map = {"成功": "Success", "失败": "Failed", "阻断": "Blocked"}
    status_bi = f"{status} / {status_map.get(status, status)}"
    print("【执行回执 | Execution Receipt】")
    print("执行来源 | Executor: OC_GUARD")
    print(f"操作类型 | Operation: {operation}")
    print(f"请求编号 | Request ID: {request_id}")
    print(f"执行状态 | Status: {status_bi}")
    print(f"验签码 | Signature: {sig}")
    print("【本次内容 | Details】")
    print(body)


def decorate_non_executed(status: str, message: str) -> str:
    msg = (message or "").strip() or "无"
    if status == "阻断" and NON_EXEC_MARKER not in msg:
        return f"{NON_EXEC_MARKER}\n{msg}"
    return msg


def extract_json_object(text: str):
    cleaned = ANSI_RE.sub("", text).strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```[a-zA-Z0-9_-]*\n", "", cleaned)
        cleaned = re.sub(r"\n```$", "", cleaned)

    first = cleaned.find("{")
    if first == -1:
        return None

    depth = 0
    in_str = False
    escape = False
    start = None
    for i, ch in enumerate(cleaned[first:], start=first):
        if in_str:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == '"':
                in_str = False
            continue

        if ch == '"':
            in_str = True
            continue
        if ch == "{":
            if start is None:
                start = i
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0 and start is not None:
                return cleaned[start : i + 1]
    return None


def parse_ptr(path: str):
    if not path.startswith("/"):
        raise ValueError(f"Invalid path: {path}")
    return [p for p in path.split("/") if p]


def get_or_create_by_key(list_obj, key_name, key_value):
    for item in list_obj:
        if isinstance(item, dict) and item.get(key_name) == key_value:
            return item
    item = {key_name: key_value}
    list_obj.append(item)
    return item


def set_pointer(root, parts, value):
    cur = root
    for i, part in enumerate(parts):
        last = i == len(parts) - 1
        if part.isdigit():
            idx = int(part)
            if not isinstance(cur, list):
                raise ValueError(f"Segment {part} expects list")
            if idx < 0 or idx >= len(cur):
                raise ValueError(f"Index out of range: {idx}")
            if last:
                cur[idx] = value
                return
            cur = cur[idx]
            continue
        if not isinstance(cur, dict):
            raise ValueError(f"Segment {part} expects object")
        if last:
            cur[part] = value
            return
        if part not in cur or not isinstance(cur[part], (dict, list)):
            cur[part] = {}
        cur = cur[part]


def delete_pointer(root, parts):
    cur = root
    for i, part in enumerate(parts):
        last = i == len(parts) - 1
        if part.isdigit():
            idx = int(part)
            if not isinstance(cur, list) or idx < 0 or idx >= len(cur):
                raise ValueError(f"Invalid list path at segment {part}")
            if last:
                cur.pop(idx)
                return
            cur = cur[idx]
            continue
        if not isinstance(cur, dict) or part not in cur:
            raise ValueError(f"Path does not exist at segment {part}")
        if last:
            del cur[part]
            return
        cur = cur[part]


def set_path(cfg, path, value):
    parts = parse_ptr(path)
    if len(parts) >= 3 and parts[0] == "bindings" and parts[1] == "by-agent":
        bindings = cfg.setdefault("bindings", [])
        if not isinstance(bindings, list):
            raise ValueError("bindings must be a list")
        target = get_or_create_by_key(bindings, "agentId", parts[2])
        set_pointer(target, parts[3:], value)
        return
    if len(parts) >= 3 and parts[0] == "agents" and parts[1] == "by-id":
        agents = cfg.setdefault("agents", {}).setdefault("list", [])
        if not isinstance(agents, list):
            raise ValueError("agents.list must be a list")
        target = get_or_create_by_key(agents, "id", parts[2])
        set_pointer(target, parts[3:], value)
        return
    set_pointer(cfg, parts, value)


def delete_path(cfg, path):
    parts = parse_ptr(path)
    if len(parts) >= 3 and parts[0] == "bindings" and parts[1] == "by-agent":
        bindings = cfg.get("bindings", [])
        if not isinstance(bindings, list):
            raise ValueError("bindings must be a list")
        aid = parts[2]
        for i, item in enumerate(bindings):
            if isinstance(item, dict) and item.get("agentId") == aid:
                if len(parts) == 3:
                    bindings.pop(i)
                    return
                delete_pointer(item, parts[3:])
                return
        raise ValueError(f"No binding found for agentId: {aid}")
    if len(parts) >= 3 and parts[0] == "agents" and parts[1] == "by-id":
        agents = cfg.get("agents", {}).get("list", [])
        if not isinstance(agents, list):
            raise ValueError("agents.list must be a list")
        aid = parts[2]
        for i, item in enumerate(agents):
            if isinstance(item, dict) and item.get("id") == aid:
                if len(parts) == 3:
                    agents.pop(i)
                    return
                delete_pointer(item, parts[3:])
                return
        raise ValueError(f"No agent found for id: {aid}")
    delete_pointer(cfg, parts)


def check_provider_models(cfg):
    providers = cfg.get("models", {}).get("providers", {})
    provider_models = {}
    for pname, pobj in providers.items():
        models = pobj.get("models", []) if isinstance(pobj, dict) else []
        ids = {m.get("id") for m in models if isinstance(m, dict) and isinstance(m.get("id"), str)}
        provider_models[pname] = ids

    def check_ref(label, ref):
        if not isinstance(ref, str) or "/" not in ref:
            raise ValueError(f"{label} model primary must be provider/model")
        provider, model_id = ref.split("/", 1)
        if provider not in provider_models:
            raise ValueError(f"{label} references unknown provider: {provider}")
        if model_id not in provider_models[provider]:
            raise ValueError(f"{label} references unknown model: {ref}")

    defaults_primary = cfg.get("agents", {}).get("defaults", {}).get("model", {}).get("primary")
    if defaults_primary is not None:
        check_ref("agents.defaults", defaults_primary)

    for agent in cfg.get("agents", {}).get("list", []):
        if not isinstance(agent, dict):
            continue
        primary = agent.get("model", {}).get("primary")
        if primary is not None:
            check_ref(f"agent:{agent.get('id', 'unknown')}", primary)


def check_channels_and_bindings(cfg):
    channels = cfg.get("channels", {})
    if not isinstance(channels, dict):
        raise ValueError("channels must be object")
    channel_ids = set(channels.keys())
    unknown_channels = sorted(channel_ids - SUPPORTED_CHANNEL_IDS)
    if unknown_channels:
        raise ValueError(f"unsupported channel ids: {', '.join(unknown_channels)}")

    agents = cfg.get("agents", {}).get("list", [])
    agent_ids = {a.get("id") for a in agents if isinstance(a, dict) and isinstance(a.get("id"), str)}

    bindings = cfg.get("bindings", [])
    if not isinstance(bindings, list):
        raise ValueError("bindings must be array")

    seen_scopes = set()
    for i, b in enumerate(bindings):
        if not isinstance(b, dict):
            raise ValueError(f"bindings[{i}] must be object")
        aid = b.get("agentId")
        if not isinstance(aid, str) or aid not in agent_ids:
            raise ValueError(f"bindings[{i}].agentId is missing or unknown: {aid}")
        match = b.get("match", {})
        if not isinstance(match, dict):
            raise ValueError(f"bindings[{i}].match must be object")
        channel = match.get("channel")
        if not isinstance(channel, str) or channel not in channel_ids:
            raise ValueError(f"bindings[{i}].match.channel unknown: {channel}")

        account_id = match.get("accountId")
        channel_cfg = channels.get(channel, {})
        if account_id is not None:
            accounts = channel_cfg.get("accounts") if isinstance(channel_cfg, dict) else None
            if isinstance(accounts, dict) and account_id not in accounts:
                raise ValueError(
                    f"bindings[{i}] accountId '{account_id}' not found in channels.{channel}.accounts"
                )

        peer = match.get("peer", {}) if isinstance(match.get("peer", {}), dict) else {}
        scope_key = (
            channel,
            account_id,
            peer.get("kind"),
            peer.get("id"),
        )
        if scope_key in seen_scopes:
            raise ValueError(f"bindings has scope conflict: {scope_key}")
        seen_scopes.add(scope_key)


def plugin_feishu(cfg):
    fei = cfg.get("channels", {}).get("feishu")
    if fei is None:
        return
    if not isinstance(fei, dict):
        raise ValueError("channels.feishu must be object")
    accounts = fei.get("accounts")
    if not isinstance(accounts, dict) or not accounts:
        raise ValueError("channels.feishu.accounts must be non-empty object")
    for aid, acfg in accounts.items():
        if not isinstance(acfg, dict):
            raise ValueError(f"channels.feishu.accounts.{aid} must be object")
        for req in ("appId", "appSecret"):
            val = acfg.get(req)
            if not isinstance(val, str) or not val.strip():
                raise ValueError(f"channels.feishu.accounts.{aid}.{req} is required")


def plugin_telegram(cfg):
    tg = cfg.get("channels", {}).get("telegram")
    if tg is None:
        return
    if not isinstance(tg, dict):
        raise ValueError("channels.telegram must be object")
    accounts = tg.get("accounts")
    if isinstance(accounts, dict):
        for aid, acfg in accounts.items():
            if not isinstance(acfg, dict):
                raise ValueError(f"channels.telegram.accounts.{aid} must be object")
            if not any(isinstance(acfg.get(k), str) and acfg.get(k).strip() for k in ("botToken", "token")):
                raise ValueError(f"channels.telegram.accounts.{aid} requires botToken or token")


def plugin_discord(cfg):
    dc = cfg.get("channels", {}).get("discord")
    if dc is None:
        return
    if not isinstance(dc, dict):
        raise ValueError("channels.discord must be object")
    accounts = dc.get("accounts")
    if isinstance(accounts, dict):
        for aid, acfg in accounts.items():
            if not isinstance(acfg, dict):
                raise ValueError(f"channels.discord.accounts.{aid} must be object")
            if not any(isinstance(acfg.get(k), str) and acfg.get(k).strip() for k in ("botToken", "token")):
                raise ValueError(f"channels.discord.accounts.{aid} requires botToken or token")


def check_enum_constraints(cfg):
    tools = cfg.get("tools", {}) if isinstance(cfg.get("tools", {}), dict) else {}
    exec_cfg = tools.get("exec", {}) if isinstance(tools.get("exec", {}), dict) else {}
    ask = exec_cfg.get("ask")
    if ask is not None and ask not in ALLOWED_TOOLS_EXEC_ASK:
        allowed = ", ".join(sorted(ALLOWED_TOOLS_EXEC_ASK))
        raise ValueError(f"tools.exec.ask must be one of: {allowed}; got: {ask}")


def check_agent_model_drift(cfg):
    expected = {}
    providers = cfg.get("models", {}).get("providers", {})
    if not isinstance(providers, dict):
        return
    for provider, provider_cfg in providers.items():
        if not isinstance(provider_cfg, dict):
            continue
        expected[provider] = {
            "baseUrl": provider_cfg.get("baseUrl"),
            "api": provider_cfg.get("api"),
        }

    agents_root = OPENCLAW_HOME / "agents"
    if not agents_root.exists():
        return

    drifts = []
    for models_file in agents_root.glob("*/agent/models.json"):
        try:
            data = load_json(models_file)
        except Exception as e:
            drifts.append(f"{models_file}: unreadable models.json ({e})")
            continue
        local_providers = data.get("providers", {}) if isinstance(data, dict) else {}
        if not isinstance(local_providers, dict):
            continue
        for provider, exp_cfg in expected.items():
            local_cfg = local_providers.get(provider)
            if not isinstance(local_cfg, dict):
                continue
            for field in ("baseUrl", "api"):
                exp_v = exp_cfg.get(field)
                local_v = local_cfg.get(field)
                if exp_v is None or local_v is None:
                    continue
                if exp_v != local_v:
                    drifts.append(
                        f"{models_file}: provider={provider} {field} drift "
                        f"(global={exp_v}, agent={local_v})"
                    )

    if drifts:
        shown = "\n- ".join(drifts[:8])
        more = "" if len(drifts) <= 8 else f"\n... and {len(drifts) - 8} more"
        raise ValueError(f"agent models drift detected:\n- {shown}{more}")


def run_openclaw_schema_validate(cfg):
    with tempfile.TemporaryDirectory(prefix="oc-guard-validate-") as td:
        temp_home = Path(td)
        temp_cfg = temp_home / "openclaw.json"
        dump_json(temp_cfg, cfg)
        env = os.environ.copy()
        env["OPENCLAW_CONFIG_PATH"] = str(temp_cfg)
        proc = run([str(OPENCLAW_BIN), "config", "validate", "--json"], timeout=30, check=False, env=env)
        out = ((proc.stdout or "") + (proc.stderr or "")).strip()
        if proc.returncode != 0:
            raise ValueError(f"openclaw config validate failed: {out}")
        if out:
            text = extract_json_object(out)
            if text:
                data = json.loads(text)
                if not data.get("valid", False):
                    raise ValueError(f"openclaw config validate invalid: {out}")


def validate_config(cfg):
    if not isinstance(cfg, dict):
        raise ValueError("config must be object")
    check_provider_models(cfg)
    check_channels_and_bindings(cfg)
    plugin_feishu(cfg)
    plugin_telegram(cfg)
    plugin_discord(cfg)
    check_enum_constraints(cfg)
    check_agent_model_drift(cfg)


def risk_of_path(path: str) -> str:
    high_prefixes = (
        "/channels",
        "/bindings",
        "/models/providers",
        "/agents/defaults/model",
        "/agents/list",
        "/agents/by-id",
    )
    medium_prefixes = (
        "/messages",
        "/commands",
        "/gateway",
        "/plugins",
        "/tools",
    )
    if path.startswith(high_prefixes):
        return "high"
    if path.startswith(medium_prefixes):
        return "medium"
    return "low"


def merge_risk(risks):
    if "high" in risks:
        return "high"
    if "medium" in risks:
        return "medium"
    return "low"


def generate_proposal(requirement: str, config_path: Path):
    if not OPENCODE_BIN.exists():
        fail(f"opencode not found: {OPENCODE_BIN}")
    prompt = f"""
你是 openclaw 配置提案助手。
目标：根据用户需求生成 JSON 提案，不要修改任何文件。

用户需求：{requirement}
配置文件路径：{config_path}

严格要求：
1) 只输出 JSON，对象格式如下：
{{
  "intent": "...",
  "changes": [
    {{"op": "set", "path": "/...", "value": ...}}
  ],
  "post_checks": ["..."]
}}
2) path 使用 JSON 路径；支持：
   - /bindings/by-agent/<agentId>/...
   - /agents/by-id/<agentId>/...
   - 其余按 openclaw.json 实际结构
3) 不要输出任何 shell 命令，不要解释文本。
4) 禁止 invent 字段，必须尽量复用现有结构。
""".strip()
    proc = run([str(OPENCODE_BIN), "run", prompt], timeout=120, check=False)
    stdout = (proc.stdout or "").strip()
    stderr = (proc.stderr or "").strip()
    raw = stdout or stderr
    if not raw:
        fail("opencode returned empty proposal")

    text = extract_json_object(raw)
    if not text:
        payload = {
            "returncode": proc.returncode,
            "stdout": stdout,
            "stderr": stderr,
        }
        OPENCODE_DEBUG_PATH.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        log(
            "opencode output is non-json; "
            f"rc={proc.returncode}, stdout_len={len(stdout)}, stderr_len={len(stderr)}, "
            f"debug_file={OPENCODE_DEBUG_PATH}"
        )
        fail(f"opencode output is not valid JSON; debug file: {OPENCODE_DEBUG_PATH}")
    try:
        return json.loads(text)
    except Exception as e:
        payload = {
            "returncode": proc.returncode,
            "stdout": stdout,
            "stderr": stderr,
            "extracted_json": text,
            "parse_error": str(e),
        }
        OPENCODE_DEBUG_PATH.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        log(
            "opencode proposal parse failed; "
            f"rc={proc.returncode}, stdout_len={len(stdout)}, stderr_len={len(stderr)}, "
            f"debug_file={OPENCODE_DEBUG_PATH}"
        )
        fail(f"failed to parse proposal JSON: {e}; debug file: {OPENCODE_DEBUG_PATH}")


def apply_changes(cfg, proposal):
    changes = proposal.get("changes")
    if not isinstance(changes, list) or not changes:
        raise ValueError("proposal.changes must be non-empty list")
    modified = copy.deepcopy(cfg)
    applied = []
    risks = []
    for c in changes:
        if not isinstance(c, dict):
            raise ValueError("each change must be object")
        op = c.get("op", "set")
        path = c.get("path")
        if not isinstance(path, str):
            raise ValueError("change.path must be string")
        if not path.startswith(ALLOWED_PATH_PREFIXES):
            raise ValueError(f"path not allowed by policy: {path}")
        if op == "set":
            if "value" not in c:
                raise ValueError(f"missing value for set: {path}")
            set_path(modified, path, c["value"])
            shown = mask_value(path, c["value"])
            applied.append({"op": op, "path": path, "value": shown})
        elif op == "delete":
            delete_path(modified, path)
            applied.append({"op": op, "path": path})
        else:
            raise ValueError(f"unsupported op: {op}")
        risks.append(risk_of_path(path))
    return modified, applied, merge_risk(risks)


def check_gateway_running():
    p = run([str(OPENCLAW_BIN), "gateway", "status"], timeout=20, check=False)
    text = (p.stdout or "") + (p.stderr or "")
    return "Runtime: running" in text, text


def select_canary_agents(cfg):
    agents = cfg.get("agents", {}).get("list", [])
    if not isinstance(agents, list):
        return []
    ids = [a.get("id") for a in agents if isinstance(a, dict) and isinstance(a.get("id"), str)]
    preferred = [aid for aid in ("main", "bro") if aid in ids]
    if preferred:
        return preferred
    return ids[:1]


def run_canary_for_agent(agent_id):
    probe = f"请仅回复：OC_GUARD_CANARY_{agent_id}"
    proc = run(
        [
            str(OPENCLAW_BIN),
            "agent",
            "--agent",
            agent_id,
            "--message",
            probe,
            "--json",
        ],
        timeout=120,
        check=False,
    )
    out = ((proc.stdout or "") + (proc.stderr or "")).strip()
    if proc.returncode != 0:
        return False, f"agent={agent_id} command failed: {out[:300]}"
    text = extract_json_object(out)
    if not text:
        return False, f"agent={agent_id} returned non-json output"
    data = json.loads(text)
    if data.get("status") != "ok":
        return False, f"agent={agent_id} status != ok"
    payloads = data.get("result", {}).get("payloads", [])
    if not isinstance(payloads, list) or not payloads:
        return False, f"agent={agent_id} empty payloads"
    has_content = any(
        isinstance(item, dict) and (
            (isinstance(item.get("text"), str) and item.get("text").strip())
            or (isinstance(item.get("mediaUrl"), str) and item.get("mediaUrl").strip())
        )
        for item in payloads
    )
    if not has_content:
        return False, f"agent={agent_id} payloads have no content"
    return True, f"agent={agent_id} canary ok"


def run_post_apply_canary(cfg):
    targets = select_canary_agents(cfg)
    if not targets:
        return ["canary skipped: no agents configured"]
    notes = []
    for aid in targets:
        ok, msg = run_canary_for_agent(aid)
        notes.append(msg)
        if not ok:
            raise ValueError(f"post-apply canary failed: {msg}")
    return notes


def do_plan(requirement, proposal_file, config_file):
    cfg = load_json(config_file)
    proposal = load_json(Path(proposal_file)) if proposal_file else generate_proposal(requirement, config_file)
    modified, applied, risk = apply_changes(cfg, proposal)
    validate_config(modified)
    run_openclaw_schema_validate(modified)

    LAST_PROPOSAL_PATH.write_text(json.dumps(proposal, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report = {
        "intent": proposal.get("intent"),
        "risk": risk,
        "changes": applied,
        "proposalFile": str(LAST_PROPOSAL_PATH),
    }
    LAST_PLAN_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = []
    lines.append(f"意图 | Intent: {proposal.get('intent', '(none)')}")
    lines.append(f"风险等级 | Risk: {risk}")
    lines.append("校验阶段 | Validation Stages:")
    lines.append("- custom-validate: pass")
    lines.append("- openclaw-config-validate: pass")
    lines.append("变更列表 | Changes:")
    for item in applied:
        if item["op"] == "set":
            lines.append(f"- 设置 | set {item['path']} = {item['value']}")
        else:
            lines.append(f"- 删除 | delete {item['path']}")
    lines.append(f"提案文件 | Proposal File: {LAST_PROPOSAL_PATH}")
    lines.append(f"计划文件 | Plan File: {LAST_PLAN_PATH}")
    return "\n".join(lines)


def do_apply(requirement, proposal_file, config_file, confirm):
    cfg = load_json(config_file)
    proposal = load_json(Path(proposal_file)) if proposal_file else generate_proposal(requirement, config_file)
    modified, applied, risk = apply_changes(cfg, proposal)
    validate_config(modified)
    run_openclaw_schema_validate(modified)

    if risk == "high" and not confirm:
        fail("高风险变更需要 --confirm | High-risk changes require --confirm", status="阻断")

    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    ts = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = BACKUP_DIR / f"openclaw.json.{ts}.bak"
    dump_json(LAST_PROPOSAL_PATH, proposal)
    shutil.copy2(config_file, backup_file)
    dump_json(config_file, modified)

    log(f"Backup created: {backup_file}")
    log(f"Applied {len(applied)} changes, risk={risk}")

    restarted = run([str(OPENCLAW_BIN), "gateway", "restart"], timeout=60, check=False)
    if restarted.returncode != 0:
        log("Gateway restart failed, rolling back")
        shutil.copy2(backup_file, config_file)
        run([str(OPENCLAW_BIN), "gateway", "restart"], timeout=60, check=False)
        fail("restart failed after apply; rolled back")

    ok, status_text = check_gateway_running()
    if not ok:
        log("Gateway unhealthy after apply, rolling back")
        shutil.copy2(backup_file, config_file)
        run([str(OPENCLAW_BIN), "gateway", "restart"], timeout=60, check=False)
        fail("gateway unhealthy after apply; rolled back")

    try:
        canary_notes = run_post_apply_canary(modified)
    except Exception as e:
        log(f"Post-apply canary failed, rolling back: {e}")
        shutil.copy2(backup_file, config_file)
        run([str(OPENCLAW_BIN), "gateway", "restart"], timeout=60, check=False)
        fail(f"post-apply canary failed; rolled back: {e}")

    lines = [
        f"已应用变更数 | Applied Changes: {len(applied)}",
        f"风险等级 | Risk: {risk}",
        "网关状态 | Gateway: running",
        "校验阶段 | Validation Stages:",
        "- custom-validate: pass",
        "- openclaw-config-validate: pass",
        "- gateway-health: pass",
        f"备份文件 | Backup File: {backup_file}",
        "Canary:",
        "变更列表 | Changes:",
    ]
    for note in canary_notes:
        lines.append(f"- {note}")
    for item in applied:
        if item["op"] == "set":
            lines.append(f"- 设置 | set {item['path']} = {item['value']}")
        else:
            lines.append(f"- 删除 | delete {item['path']}")
    return "\n".join(lines)


def main():
    parser = GuardArgumentParser(prog="oc-guard", description="Safe OpenClaw configuration guard", add_help=False)
    parser.add_argument("mode", nargs="?", choices=["plan", "apply"], help="plan or apply")
    parser.add_argument("requirement", nargs="?", default="", help="natural language requirement")
    parser.add_argument("--proposal", help="use proposal JSON file directly")
    parser.add_argument("--config", default=str(CONFIG_PATH), help="config path")
    parser.add_argument("--confirm", action="store_true", help="required for high-risk apply")
    parser.add_argument("-h", "--help", action="store_true", help="show this help message")
    args = parser.parse_args()

    request_id = build_request_id()

    if args.help:
        emit_receipt("QUERY", request_id, "成功", parser.format_help().strip())
        return

    if not args.mode:
        fail("缺少操作类型，必须是 plan 或 apply | Missing mode: plan or apply required", status="阻断", code=2)

    cfg_path = Path(args.config)
    if not cfg_path.exists():
        fail(f"配置文件不存在 | Config not found: {cfg_path}", status="阻断")
    if not OPENCLAW_BIN.exists():
        fail(f"openclaw 不存在 | openclaw not found: {OPENCLAW_BIN}", status="阻断")
    if not args.proposal and not args.requirement.strip():
        fail("缺少需求文本：未提供 --proposal 时必须提供需求 | Missing requirement when --proposal is not provided", status="阻断", code=2)

    operation = args.mode.upper()

    if args.mode == "plan":
        content = do_plan(args.requirement, args.proposal, cfg_path)
    else:
        content = do_apply(args.requirement, args.proposal, cfg_path, args.confirm)
    emit_receipt(operation, request_id, "成功", content)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except GuardError as e:
        operation = "QUERY"
        if len(sys.argv) > 1 and sys.argv[1] in {"plan", "apply"}:
            operation = sys.argv[1].upper()
        content = decorate_non_executed(e.status, e.message)
        emit_receipt(operation, build_request_id(), e.status, content)
        sys.exit(e.code)
    except Exception as e:
        msg = str(e)
        ERROR_PATH.write_text(msg + "\n", encoding="utf-8")
        log(f"ERROR: {msg}")
        operation = "QUERY"
        if len(sys.argv) > 1 and sys.argv[1] in {"plan", "apply"}:
            operation = sys.argv[1].upper()
        emit_receipt(operation, build_request_id(), "失败", msg)
        sys.exit(1)
