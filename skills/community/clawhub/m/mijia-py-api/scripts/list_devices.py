"""
米家设备列表 / Mijia Device List Snapshot (中文/English)

获取所有家庭、房间和设备的 JSON 快照。
Get JSON snapshot of all homes, rooms, and devices.
"""

import json
import subprocess
import sys

# Windows GBK 兼容 / Windows GBK compat
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')


def run_mijia(*args):
    """运行 mijiaAPI CLI 并返回输出 / Run mijiaAPI CLI and return output"""
    result = subprocess.run(
        [sys.executable, "-m", "mijiaAPI", *args],
        capture_output=True, text=True, timeout=30
    )
    if result.returncode != 0:
        print(f"错误 / Error: {result.stderr}", file=sys.stderr)
        return None
    return result.stdout


def main():
    print("=== 米家设备列表 / Mijia Device List ===", flush=True)

    # 1. 获取家庭列表 / Get homes
    homes_out = run_mijia("--list_homes")
    if homes_out:
        print(f"\n📋 家庭 / Homes:\n{homes_out}", flush=True)

    # 2. 获取场景列表 / Get scenes
    scenes_out = run_mijia("--list_scenes")
    if scenes_out:
        print(f"\n🎬 场景 / Scenes:\n{scenes_out}", flush=True)

    # 3. 获取耗材信息 / Get consumables
    cons_out = run_mijia("--list_consumable_items")
    if cons_out:
        print(f"\n🔋 耗材 / Consumables:\n{cons_out}", flush=True)


if __name__ == "__main__":
    main()
