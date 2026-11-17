#!/usr/bin/env python3
"""collect_mcp.py — 从常见宿主的配置文件确定性采集 MCP server 原始证据。

为 mcp-server-audit Skill 提供证据层。设计原则与同仓库 delivery-spec-audit
的 extract_spec.py 一致:只采集「事实」,不做「评分」——某个配置是否可接受
取决于部署语境(本机个人用 / 容器隔离 / 共享主机),语义判断由 Agent 完成。

支持的宿主(存在才读,全部可选):
  Claude Code      ~/.claude.json (mcpServers,含 projects 级覆盖)
  Codex            ~/.codex/config.toml ([mcp_servers.*])
  Cursor           ~/.cursor/mcp.json (mcpServers)
  Windsurf         ~/.codeium/windsurf/mcp_config.json (mcpServers)
  项目级 .mcp.json  --repo <path> 时扫描 <path>/.mcp.json
  任意显式文件      --json-file <path> (json 或 toml)

每条 server 输出的证据字段:
  name / host / scope / transport(stdio 或 remote,推断)
  command / args / url / cwd
  env_keys(只输出键名 + has_value 布尔,绝不输出值)
  header_keys(同上,只键名)
  flags(确定性风险标记,见 flags_for)

安全边界:
  - 只读配置文件;不执行任何 server;不发起网络请求;
  - env 值、header 值一律不输出;
  - 输出 JSON,供 Agent 直接消费。

用法:
    python3 collect_mcp.py                  # 扫描本机全部已知位置
    python3 collect_mcp.py --host claude    # 只看某个宿主
    python3 collect_mcp.py --repo /path     # 额外扫描项目级 .mcp.json
    python3 collect_mcp.py --json-file x.toml  # 审查任意配置文件
"""

import argparse
import json
import re
import sys
from pathlib import Path

SHELL_WRAPPERS = {"sh", "bash", "zsh", "fish", "cmd", "cmd.exe", "powershell", "pwsh"}
PACKAGE_RUNNERS = {"npx", "uvx", "bunx", "pipx", "pnpm"}


def redact_mapping(mapping):
    """只保留键名与有无值,绝不透传值。"""
    if not isinstance(mapping, dict):
        return {}
    return {str(k): {"has_value": bool(str(v).strip())} for k, v in mapping.items()}


def infer_transport(entry):
    if isinstance(entry, dict):
        if entry.get("url"):
            t = str(entry.get("type") or entry.get("transport") or "").strip().lower()
            return t if t else "remote(url)"
        if entry.get("command"):
            return "stdio"
    return "unknown"


def flags_for(command, args, url):
    flags = []
    cmd = str(command or "").strip()
    argv = [str(a) for a in (args or []) if not isinstance(a, (dict, list))]
    joined = " ".join([cmd] + argv)
    base = Path(cmd).name.lower() if cmd else ""
    base_stripped = base[:-4] if base.endswith(".exe") else base

    if base_stripped in SHELL_WRAPPERS:
        flags.append("shell_interpreter")
    if base_stripped in PACKAGE_RUNNERS:
        flags.append("package_runner_fetched")
        if "-y" in argv or "--yes" in argv:
            flags.append("auto_yes_install")
        if base_stripped == "pnpm" and "dlx" in argv[:2]:
            flags.append("package_runner_fetched_dlx")
    if re.search(r"\|\s*(sh|bash|zsh)\b", joined):
        flags.append("pipe_to_shell")
    if re.search(r"(curl|wget)\b[^|]*\|\s*", joined):
        flags.append("remote_fetch_piped")
    if url:
        u = str(url)
        if "://" not in u:
            flags.append("url_no_scheme")
        if re.search(r"(token|key|apikey|api_key|password|secret)=", u, re.I):
            flags.append("credential_in_url")
        if u.startswith("http://"):
            flags.append("plain_http")
    return flags


def normalize(name, entry, host, scope):
    if not isinstance(entry, dict):
        return {"name": str(name), "host": host, "scope": scope, "error": "entry_not_object"}
    command = entry.get("command")
    args = entry.get("args")
    url = entry.get("url")
    headers = entry.get("headers") if isinstance(entry.get("headers"), dict) else {}
    env = entry.get("env") if isinstance(entry.get("env"), dict) else {}
    return {
        "name": str(name),
        "host": host,
        "scope": scope,
        "transport": infer_transport(entry),
        "command": command if isinstance(command, str) else None,
        "args": args if isinstance(args, list) else None,
        "url": url if isinstance(url, str) else None,
        "cwd": entry.get("cwd"),
        "env_keys": redact_mapping(env),
        "env_file": entry.get("envFile"),
        "header_keys": [str(k) for k in headers.keys()],
        "flags": flags_for(command, args, url),
        "raw_type": entry.get("type") or entry.get("transport"),
    }


def load_json_file(path):
    p = Path(path).expanduser()
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        return {"__parse_error__": str(e)}


def load_toml_subset(path):
    """Python 3.9 兼容的极简 TOML 子集解析,只覆盖 [mcp_servers.name] 配置形态。

    支持:key = "string" / [bare.array] / true|false / 裸值;
    不支持:多行字符串、内联表、${变量}展开(原样保留为字符串)。
    解析失败不会抛异常——返回带 __parse_error__ 的占位。
    """
    p = Path(path).expanduser()
    if not p.exists():
        return None
    servers = {}
    current = None
    try:
        text = p.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        return {"__parse_error__": str(e)}
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        m = re.match(r"^\[\[?([^\]]+)\]?\]$", line)
        if m:
            sect = m.group(1).strip()
            parts = [x.strip().strip('"').strip("'") for x in sect.split(".")]
            if parts and parts[0] == "mcp_servers" and len(parts) > 1:
                current = parts[1]
                servers.setdefault(current, {})
            else:
                current = None
            continue
        if current is not None:
            m = re.match(r"^([A-Za-z0-9_\-]+)\s*=\s*(.+)$", line)
            if m:
                k, v = m.group(1), m.group(2).strip()
                # 去掉行尾注释(仅当值是裸词或数组时;字符串内 # 不处理——保守起见字符串优先)
                if v.startswith('"'):
                    mm = re.match(r'^"((?:[^"\\]|\\.)*)"', v)
                    v = mm.group(1) if mm else v.strip('"')
                elif v.startswith("["):
                    v = [x.strip().strip('"').strip("'") for x in v.strip("[]").split(",") if x.strip()]
                elif v in ("true", "false"):
                    v = v == "true"
                else:
                    v = v.split("#", 1)[0].strip()
                servers[current][k] = v
    return {"mcpServers": servers}


def collect(repo=None, extra_file=None, only_host=None):
    home = Path.home()
    found = []

    def add(host, scope, data, source):
        if data is None:
            return
        if isinstance(data, dict) and "__parse_error__" in data:
            found.append({"name": "<parse_error>", "host": host, "scope": scope,
                          "source": source, "error": data["__parse_error__"]})
            return
        servers = data.get("mcpServers") or {}
        for name, entry in servers.items():
            found.append(normalize(name, entry, host, scope))

    if only_host in (None, "claude"):
        cc = load_json_file(home / ".claude.json")
        if isinstance(cc, dict):
            add("claude-code", "user", {"mcpServers": cc.get("mcpServers") or {}}, "~/.claude.json")
            for proj, pdata in (cc.get("projects") or {}).items():
                if isinstance(pdata, dict) and pdata.get("mcpServers"):
                    add("claude-code", f"project:{proj}", {"mcpServers": pdata["mcpServers"]}, str(proj))

    if only_host in (None, "codex"):
        add("codex", "user", load_toml_subset(home / ".codex" / "config.toml"), "~/.codex/config.toml")

    if only_host in (None, "cursor"):
        add("cursor", "user", load_json_file(home / ".cursor" / "mcp.json"), "~/.cursor/mcp.json")

    if only_host in (None, "windsurf"):
        add("windsurf", "user",
            load_json_file(home / ".codeium" / "windsurf" / "mcp_config.json"),
            "~/.codeium/windsurf/mcp_config.json")

    if repo:
        rp = Path(repo).expanduser()
        cand = rp / ".mcp.json"
        if cand.exists():
            add("project-file", f"repo:{rp.name}", load_json_file(cand), str(cand))

    if extra_file:
        ep = Path(extra_file).expanduser()
        data = load_json_file(ep)
        if (data is None or (isinstance(data, dict) and "__parse_error__" in data)) and ep.suffix == ".toml":
            data = load_toml_subset(ep)
        add("adhoc-file", "explicit", data, str(ep))

    return {
        "servers": found,
        "counts": {
            "total": len(found),
            "with_flags": sum(1 for s in found if s.get("flags")),
            "parse_errors": sum(1 for s in found if s.get("error")),
        },
    }


def main():
    ap = argparse.ArgumentParser(description="Collect MCP server config evidence (values redacted)")
    ap.add_argument("--repo", help="also scan <repo>/.mcp.json")
    ap.add_argument("--host", help="only this host: claude|codex|cursor|windsurf")
    ap.add_argument("--json-file", help="audit an explicit config file (json or toml)")
    args = ap.parse_args()
    out = collect(repo=args.repo, extra_file=args.json_file, only_host=args.host)
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    sys.exit(main())
