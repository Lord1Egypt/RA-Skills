#!/usr/bin/env python3
"""Preview/apply guarded WebChat memory integration; never prints config values."""
from __future__ import annotations
import argparse
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import stat
import sys
SKILL_ROOT = Path(__file__).absolute().parents[1]
if str(SKILL_ROOT) not in sys.path:
    sys.path.insert(0, str(SKILL_ROOT))
from core.safe_fs import atomic_write_bytes, check_file, ensure_directory, lexical_path, read_bytes
from core.safe_fs import UnsafePathError, _windows_dacl_signature, _windows_read_dacl, _windows_security_api

GUARD_MARKER = "// hui-yi 1.2.13: honor allowedChatTypes before deterministic recall."
SCOPE_MARKER = "// hui-yi 1.2.13: limit automatic recall to authenticated webchat entry."
EXPECTED_RUNTIME_SHA256 = "a56adeaaae73a2805235c1578a3fcb8d8c56291014d1ca5aab84b05bdde7a766"
ORIGINAL_RUNTIME_SHA256 = "b709fab02c05e8d90846a96e9fc58b86ac14055af8b5e2402dcbad1c83645eae"
PLUGIN_ID = "hui-yi-native-memory"
RECALL_GUIDANCE = (
    "记忆是带来源和日期的证据，不是永远有效的事实。优先当前用户消息及较新的明确更正；"
    "旧记录中的持仓、金额、状态只可作为当时记录，不得冒充当前事实。"
    "重复次数只能强化相关证据，不能压过新更正或让不相关片段命中。"
    "区分用户原话、助手推测、工具内容和测试样本；不使用凭据或未经验证的推测。"
    "需要个人背景时先查主记忆及近期记录，再查低频冷记忆；保留简短来源，"
    "一次涉及多个主题时拆成最多三个短查询分别检索；已命中一个主题不能代替核实其他主题。"
    "冲突无法消解时明确说明不确定，不补造事实。"
)

def object_at(parent, key):
    value = parent.setdefault(key, {})
    if not isinstance(value, dict):
        raise ValueError("expected config object")
    return value

def merge_values(current, values):
    return list(dict.fromkeys([*(current if isinstance(current, list) else []), *values]))

def build_config(original: dict, agent_id: str = "main", timezone_name: str = "Asia/Shanghai", runtime_entry: str | None = None, plugin_dir: str | None = None) -> dict:
    search_profiles = [original.get("memory", {}).get("search", {})]
    for agent in original.get("agents", {}).get("list", []):
        if isinstance(agent, dict) and agent.get("id") == agent_id:
            override = agent.get("memory", {}).get("search", {})
            if override.get("rememberAcrossConversations") is True:
                raise ValueError("agent-specific cross-conversation scope needs operator review")
            search_profiles.append(override)
    if any("sessions" in profile.get("sources", []) or profile.get("experimental", {}).get("sessionMemory") is True for profile in search_profiles):
        raise ValueError("existing transcript indexing scope needs operator review")
    result = deepcopy(original)
    plugins = object_at(result, "plugins")
    plugins["enabled"] = True
    entries = object_at(plugins, "entries")
    memory_entry = object_at(entries, "memory-core")
    memory_entry["enabled"] = True
    memory_config = object_at(memory_entry, "config")
    dreaming = object_at(memory_config, "dreaming")
    dreaming.update(enabled=True, timezone=timezone_name, verboseLogging=False)
    dreaming.setdefault("frequency", "0 3 * * *")
    object_at(dreaming, "storage").update(mode="separate", separateReports=True)
    deep = object_at(object_at(dreaming, "phases"), "deep")
    deep["enabled"] = True
    deep["minScore"] = max(float(deep.get("minScore", .75)), .75)
    deep["minRecallCount"] = max(int(deep.get("minRecallCount", 3)), 3)
    deep["minUniqueQueries"] = max(int(deep.get("minUniqueQueries", 3)), 3)
    deep["maxPriorEntryLossFraction"] = 0
    excluded = object_at(object_at(memory_config, "memoryPolicy"), "excludeSessions")
    # Open external channels can contain other people's messages. This profile
    # admits internal WebChat; authentication is the host's responsibility and
    # owner promotion is separately checked by dreaming. Never guess owner IDs.
    excluded["channels"] = merge_values(excluded.get("channels"), list(result.get("channels", {})))
    excluded["chatTypes"] = merge_values(excluded.get("chatTypes"), ["group", "channel"])
    excluded["hookExternalContentSources"] = merge_values(excluded.get("hookExternalContentSources"), ["gmail", "email", "webhook"])
    active_entry = object_at(entries, "active-memory")
    # Only the persistent adapter may register recall callbacks. A host update
    # cannot re-enable the built-in plugin by replacing its code on disk.
    active_entry["enabled"] = False
    active = active_entry.get("config", {})
    if active.get("allowedChatIds"):
        raise ValueError("existing chat allowlist needs explicit operator review")
    other_agents = set(active.get("agents", [])) - {agent_id}
    if other_agents:
        raise ValueError("existing other-agent Active Memory profile needs operator review")
    # Preserve inactive native settings for rollback; the adapter uses only the
    # public primary-cache SDK and never loads the native plugin implementation.
    adapter = object_at(entries, PLUGIN_ID)
    adapter["enabled"] = True
    # Third-party conversation hooks need an explicit host grant. The adapter
    # independently enforces private WebChat, agent and active tool authority.
    object_at(adapter, "hooks").update(allowConversationAccess=True,
                                       allowPromptInjection=True)
    adapter_config = object_at(adapter, "config")
    adapter_config.update(agents=[agent_id], maxEntries=3, maxChars=1800,
                          promptAppend=RECALL_GUIDANCE)
    if runtime_entry:
        adapter_config["runtimeEntry"] = runtime_entry
    plugin_path = plugin_dir or str(SKILL_ROOT / "templates" / "native-memory-plugin")
    load = object_at(plugins, "load")
    load["paths"] = merge_values(load.get("paths"), [plugin_path])
    if isinstance(plugins.get("allow"), list):
        plugins["allow"] = merge_values(plugins["allow"], [PLUGIN_ID])
    if PLUGIN_ID in plugins.get("deny", []):
        raise ValueError("adapter is explicitly denied by host configuration")
    search = object_at(object_at(result, "memory"), "search")
    search["enabled"] = True
    search["rememberAcrossConversations"] = False
    hooks = object_at(object_at(object_at(result, "hooks"), "internal"), "entries")
    object_at(hooks, "hui-yi-signal-hook")["enabled"] = False
    return result

def changed_paths(before, after, prefix=""):
    if isinstance(before, dict) and isinstance(after, dict):
        out=[]
        for key in sorted(before.keys() | after.keys()):
            path = prefix + "." + key if prefix else key
            if key not in before or key not in after:
                out.append(path)
            else:
                out.extend(changed_paths(before[key], after[key], path))
        return out
    return [] if before == after else [prefix]

def verify_runtime_guard(entry: Path) -> None:
    raw = read_bytes(entry)
    digest = hashlib.sha256(raw).hexdigest()
    if digest not in {EXPECTED_RUNTIME_SHA256, ORIGINAL_RUNTIME_SHA256}:
        raise ValueError("runtime integrity changed; re-audit before enabling")
    text = raw.decode("utf-8")
    if digest == EXPECTED_RUNTIME_SHA256 and (SCOPE_MARKER not in text or '(ctx.messageProvider ?? "").trim().toLowerCase() !== "webchat"' not in text):
        raise ValueError("native Active Memory webchat scope guard is not installed")
    if digest == EXPECTED_RUNTIME_SHA256 and GUARD_MARKER not in text:
        raise ValueError("native Active Memory guard is not installed")
    if digest == EXPECTED_RUNTIME_SHA256:
        tail = text.split(GUARD_MARKER, 1)[1].split("toolAuthority.assertActive()", 1)[0]
        if "isAllowedChatType(invocationConfig, destinationContext)" not in tail:
            raise ValueError("native Active Memory guard condition is missing")
    package = json.loads(read_bytes(entry.parents[3] / "package.json"))
    if package.get("version") != "2026.9.5":
        raise ValueError("runtime version changed; re-audit integration before enabling")

def verify_adapter(plugin_dir: Path) -> None:
    manifest=json.loads(read_bytes(plugin_dir / "openclaw.plugin.json"))
    if manifest.get("id") != PLUGIN_ID:
        raise ValueError("native memory adapter identity mismatch")
    if not read_bytes(plugin_dir / "index.mjs"):
        raise ValueError("native memory adapter is missing")

def _windows_explicit_backup_acl(descriptor: bytes) -> bytes:
    """Freeze source ACEs in order; change only inherited-origin metadata."""
    control, original = _windows_dacl_signature(descriptor)
    if not control & 4 or original is None or len(original) < 8:
        raise UnsafePathError("backup requires a present, non-null source DACL")
    length = int.from_bytes(original[2:4], "little")
    count = int.from_bytes(original[4:6], "little")
    if length != len(original):
        raise UnsafePathError("invalid source DACL length")
    entries = []
    offset = 8
    for _ in range(count):
        if offset + 4 > length:
            raise UnsafePathError("invalid source DACL entry")
        size = int.from_bytes(original[offset + 2:offset + 4], "little")
        if size < 4 or offset + size > length:
            raise UnsafePathError("invalid source DACL entry size")
        ace = bytearray(original[offset:offset + size])
        ace[1] &= ~0x10  # INHERITED_ACE: keep SID, mask, other flags and ordering.
        entries.append(bytes(ace))
        offset += size
    acl = bytearray(original[:8] + b"".join(entries))
    acl[2:4] = len(acl).to_bytes(2, "little")
    return bytes(acl)


def _windows_freeze_backup_dacl(destination: Path, descriptor: bytes) -> None:
    """Protect the empty backup from permissions inherited from its new parent."""
    check_file(destination)
    if read_bytes(destination):
        raise UnsafePathError("backup DACL must be installed before content")
    expected = _windows_explicit_backup_acl(descriptor)
    ctypes, wintypes, api = _windows_security_api()
    acl = ctypes.create_string_buffer(expected)
    api.IsValidAcl.argtypes = [ctypes.c_void_p]
    api.IsValidAcl.restype = wintypes.BOOL
    if not api.IsValidAcl(acl):
        raise UnsafePathError("invalid frozen backup DACL")
    error = api.SetNamedSecurityInfoW(
        str(destination), 1, 4 | 0x80000000, None, None, acl, None
    )  # DACL_SECURITY_INFORMATION | PROTECTED_DACL_SECURITY_INFORMATION
    if error:
        raise ctypes.WinError(error)
    actual = _windows_read_dacl(destination)
    control, actual_acl = _windows_dacl_signature(actual)
    # The protected ACL cannot acquire any ACE from the destination directory.
    # SID/mask/order and all flags except inherited-origin must remain identical.
    if not control & 0x1000 or actual_acl != expected:
        raise UnsafePathError("backup DACL permissions were not frozen exactly")


def protected_backup(source: Path, destination: Path, data: bytes) -> None:
    check_file(source)
    ensure_directory(destination.parent)
    dacl = _windows_read_dacl(source) if os.name == "nt" else None
    atomic_write_bytes(destination, b"", exclusive=True)
    if dacl is not None:
        _windows_freeze_backup_dacl(destination, dacl)
        if _windows_dacl_signature(_windows_read_dacl(source)) != _windows_dacl_signature(dacl):
            raise UnsafePathError("source DACL changed during backup preparation")
    else:
        os.chmod(destination, stat.S_IMODE(source.stat().st_mode))
    atomic_write_bytes(destination, data)

def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config-path", required=True)
    parser.add_argument("--runtime-entry", required=True, help="guarded active-memory/index.js")
    parser.add_argument("--plugin-dir", help="installed templates/native-memory-plugin directory")
    parser.add_argument("--backup-dir", required=True)
    parser.add_argument("--agent-id", default="main")
    parser.add_argument("--timezone", default="Asia/Shanghai")
    parser.add_argument("--diagnostics", action="store_true", help="enable count-only cache/model-input audit logs; no prompt text")
    parser.add_argument("--apply", action="store_true")
    args=parser.parse_args(argv)
    config=lexical_path(args.config_path)
    raw=read_bytes(config)
    original=json.loads(raw)
    updated=build_config(original,args.agent_id,args.timezone,str(lexical_path(args.runtime_entry)),args.plugin_dir)
    if args.diagnostics:
        updated["plugins"]["entries"][PLUGIN_ID]["config"]["diagnostics"] = True
    changes=changed_paths(original,updated)
    report={"mode":"apply" if args.apply else "preview", "changed_paths":changes,
            "scope":"webchat entry only; host authenticates clients; external channels excluded",
            "cross_conversation_private_recall":False,
            "background_model_calls":True, "legacy_signal_hook_disabled":True,
            "built_in_active_memory_disabled":True,"upgrade_behavior":"adapter skips unverified runtime",
            "conversation_hook_access":True,"prompt_context_injection":True,
            "count_only_diagnostics":updated["plugins"]["entries"][PLUGIN_ID]["config"].get("diagnostics",False)}
    if args.apply:
        verify_runtime_guard(lexical_path(args.runtime_entry))
        verify_adapter(lexical_path(args.plugin_dir) if args.plugin_dir else SKILL_ROOT / "templates" / "native-memory-plugin")
    if args.apply and changes:
        if read_bytes(config) != raw:
            raise ValueError("runtime config changed during preparation")
        backup=lexical_path(args.backup_dir) / ("openclaw-before-hui-yi-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ") + ".json")
        protected_backup(config,backup,raw)
        if read_bytes(config) != raw:
            raise ValueError("runtime config changed during backup")
        atomic_write_bytes(config,(json.dumps(updated,ensure_ascii=False,indent=2)+"\n").encode("utf-8"))
        assert json.loads(read_bytes(config)) == updated
        report.update(backup_path=str(backup), original_sha256=hashlib.sha256(raw).hexdigest(),
                      updated_sha256=hashlib.sha256(read_bytes(config)).hexdigest())
    print(json.dumps(report,ensure_ascii=False,indent=2))
    return 0

if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError) as exc:
        print(json.dumps({"ok":False,"error_type":type(exc).__name__}),file=sys.stderr)
        raise SystemExit(1)
