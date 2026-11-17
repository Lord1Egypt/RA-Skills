#!/usr/bin/env python3
"""
sync_openclaw_config.py — openclaw.json multi-location sync tool

用途：
    任何需要修改 openclaw.json 的钩子（或直接改配置）执行完后，
    调用此脚本确保 runtime 配置同步到额外的持久化路径，容器重建后不丢失。

路径：
    runtime（source of truth）：~/.openclaw/openclaw.json
    额外同步目标：由环境变量 INIT_HOOKS_SYNC_PATHS 配置（冒号分隔，可为空）。
        不存在的路径自动跳过、不报错。

    ⚠️ 不同部署环境的持久化路径不同：
        - 纯本地 / 单机：通常无需额外同步，留空即可（只维护 runtime 一份）。
        - 容器 / K8s：把 runtime 之外的持久化挂载点填进 INIT_HOOKS_SYNC_PATHS，例如：
              export INIT_HOOKS_SYNC_PATHS="/app/clawconfig/openclaw.json:/app/k8s-config/clawconfig/openclaw.json"
          （上面两条只是常见示例，请按你自己的容器/挂载布局替换。）

用法：
    # 同步当前 runtime 配置到 INIT_HOOKS_SYNC_PATHS 里的目标（最常用）
    python3 sync_openclaw_config.py

    # 按用户明确要求 patch 某个字段：patch 内容由用户给出（写成 JSON 文件），
    # 脚本没有任何预置默认值，不主动开启/关闭任何配置项
    python3 sync_openclaw_config.py --patch "$(cat ~/user-patch.json)"

    # 执行一个修改 openclaw.json 的脚本，执行完后自动同步
    python3 sync_openclaw_config.py --run ~/scripts/patch_config.py

    # 执行一段 inline shell，执行完后自动同步
    python3 sync_openclaw_config.py --run-inline "echo done"

    # 只检查所有配置是否一致（不写入）
    python3 sync_openclaw_config.py --check
"""

import json
import os
import sys
import subprocess
import argparse
from pathlib import Path
from typing import Optional

HOME = Path.home()

RUNTIME = HOME / ".openclaw" / "openclaw.json"

# RUNTIME 是 source of truth，不列入同步目标，避免无意义自写。
# 额外持久化目标由环境变量 INIT_HOOKS_SYNC_PATHS 提供（冒号分隔），
# 让本 skill 跨部署环境通用：本地留空，容器/K8s 按自己的挂载布局填。
def _load_sync_targets() -> list:
    raw = os.environ.get("INIT_HOOKS_SYNC_PATHS", "").strip()
    if not raw:
        return []
    return [Path(p).expanduser() for p in raw.split(os.pathsep) if p.strip()]


SYNC_TARGETS = _load_sync_targets()
ALL_PATHS = [RUNTIME] + SYNC_TARGETS


def load_json(path: Path) -> Optional[dict]:
    if not path.exists():
        return None
    try:
        with open(path) as f:
            return json.load(f)
    except Exception as e:
        print(f"[sync] ⚠️  读取 {path} 失败: {e}", file=sys.stderr)
        return None


def write_json(path: Path, data: dict) -> bool:
    try:
        with open(path, "w") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"[sync] ⚠️  写入 {path} 失败: {e}", file=sys.stderr)
        return False


def deep_merge(base: dict, patch: dict) -> dict:
    """递归合并 patch 到 base（patch 优先）"""
    result = base.copy()
    for k, v in patch.items():
        if k in result and isinstance(result[k], dict) and isinstance(v, dict):
            result[k] = deep_merge(result[k], v)
        else:
            result[k] = v
    return result


def do_sync(cfg: dict, verbose: bool = True) -> int:
    """将 cfg 写入 SYNC_TARGETS（不含 RUNTIME），返回失败数量。"""
    failures = 0
    for path in SYNC_TARGETS:
        if not path.exists():
            if verbose:
                print(f"[sync] ⏭  {path} 不存在，跳过")
            continue
        if write_json(path, cfg):
            if verbose:
                print(f"[sync] ✅ {path}")
        else:
            failures += 1
    return failures


def do_check() -> bool:
    """检查所有配置是否一致，返回 True 表示一致"""
    configs = {}
    for path in ALL_PATHS:
        cfg = load_json(path)
        if cfg is not None:
            configs[str(path)] = cfg

    if len(configs) <= 1:
        print(f"[sync] ⚠️  只有 {len(configs)} 处配置文件存在，无法比对（其他路径不存在属正常）")
        return True

    paths = list(configs.keys())
    base_path = paths[0]
    base = configs[base_path]
    all_same = True
    for p in paths[1:]:
        if configs[p] != base:
            print(f"[sync] ❌ {p} 与 {base_path} 不一致")
            all_same = False
    if all_same:
        print(f"[sync] ✅ 所有存在的配置文件内容一致（{len(configs)} 处）")
    return all_same


def main():
    parser = argparse.ArgumentParser(description="openclaw.json multi-location sync tool")
    parser.add_argument("--patch",      help="JSON 字符串，deep merge 到 runtime 配置")
    parser.add_argument("--run",        help="先执行此脚本（py/sh），再同步")
    parser.add_argument("--run-inline", help="先执行此 shell 命令，再同步")
    parser.add_argument("--check",      action="store_true", help="只检查一致性，不写入")
    args = parser.parse_args()

    if args.check:
        ok = do_check()
        sys.exit(0 if ok else 1)

    # 先执行外部脚本/命令
    if args.run:
        script_path = Path(args.run).expanduser()
        if not script_path.exists():
            print(f"[sync] ❌ 脚本不存在: {script_path}", file=sys.stderr)
            sys.exit(1)
        suffix = script_path.suffix.lower()
        cmd = ["python3", str(script_path)] if suffix == ".py" else ["bash", str(script_path)]
        print(f"[sync] 执行脚本: {' '.join(cmd)}")
        try:
            result = subprocess.run(cmd)
            if result.returncode != 0:
                print(f"[sync] ⚠️  脚本执行失败（exit {result.returncode}），仍尝试同步...", file=sys.stderr)
        except FileNotFoundError as e:
            print(f"[sync] ❌ 找不到执行器: {e}，仍尝试同步...", file=sys.stderr)
        except OSError as e:
            print(f"[sync] ❌ 脚本执行异常: {e}，仍尝试同步...", file=sys.stderr)

    if args.run_inline:
        print(f"[sync] 执行 inline: {args.run_inline}")
        try:
            result = subprocess.run(["bash", "-c", args.run_inline])
            if result.returncode != 0:
                print(f"[sync] ⚠️  inline 执行失败（exit {result.returncode}），仍尝试同步...", file=sys.stderr)
        except FileNotFoundError as e:
            print(f"[sync] ❌ 找不到 bash: {e}，仍尝试同步...", file=sys.stderr)
        except OSError as e:
            print(f"[sync] ❌ inline 执行异常: {e}，仍尝试同步...", file=sys.stderr)

    # 读取 runtime 配置
    cfg = load_json(RUNTIME)
    if cfg is None:
        print(f"[sync] ❌ 读取 runtime 配置失败: {RUNTIME}", file=sys.stderr)
        sys.exit(1)

    # 应用 patch
    if args.patch:
        try:
            patch_dict = json.loads(args.patch)
        except json.JSONDecodeError as e:
            print(f"[sync] ❌ --patch JSON 解析失败: {e}", file=sys.stderr)
            sys.exit(1)
        cfg = deep_merge(cfg, patch_dict)
        # 先写回 runtime
        if not write_json(RUNTIME, cfg):
            print(f"[sync] ❌ 写入 runtime 失败", file=sys.stderr)
            sys.exit(1)
        print(f"[sync] ✅ patch 已应用到 {RUNTIME}")

    # 同步到额外目标（INIT_HOOKS_SYNC_PATHS）
    if not SYNC_TARGETS:
        print("[sync] ℹ️  未配置 INIT_HOOKS_SYNC_PATHS，仅维护 runtime 一份（本地环境属正常）")
        print(f"[sync] 🎉 完成（runtime: {RUNTIME}）")
        sys.exit(0)
    print(f"[sync] 同步配置到额外目标（共 {len(SYNC_TARGETS)} 处）...")
    failures = do_sync(cfg)
    if failures > 0:
        print(f"[sync] ⚠️  {failures} 处同步失败（见上方报错）", file=sys.stderr)
        sys.exit(1)
    else:
        print(f"[sync] 🎉 同步完成")


if __name__ == "__main__":
    main()
