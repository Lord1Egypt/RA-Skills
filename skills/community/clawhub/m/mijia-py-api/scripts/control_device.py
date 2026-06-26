"""
米家设备控制 / Mijia Device Control (中文/English)

读取或设置设备属性。
Read or set device properties.

用法 / Usage:
  python control_device.py --did "DID" --prop "power"            # 读取 / read
  python control_device.py --name "设备名" --prop "power"        # 按名称读取 / read by name
  python control_device.py --did "DID" --prop "power" --value 0  # 设置 / set

属性名通过 --get_device_info 获取 / Get prop names via --get_device_info
"""

import argparse
import subprocess
import sys

# Windows GBK 兼容 / Windows GBK compat
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')


def run_mijia(*args):
    """运行 mijiaAPI CLI 并返回输出 / Run mijiaAPI CLI and return output"""
    result = subprocess.run(
        [sys.executable, "-m", "mijiaAPI", *args],
        capture_output=True, text=True, timeout=15
    )
    if result.returncode != 0:
        print(f"错误 / Error: {result.stderr.strip()}", file=sys.stderr)
        return None
    return result.stdout


def main():
    parser = argparse.ArgumentParser(
        description="米家设备控制 / Mijia Device Control"
    )
    parser.add_argument("--did", help="设备 DID / Device DID")
    parser.add_argument("--name", help="设备名称 / Device name (as set in Mijia app)")
    parser.add_argument("--prop", help="属性名 / Property name (e.g. power, temperature, humidity)")
    parser.add_argument("--value", help="设置值 / Value to set (留空=读取/empty=read)")
    parser.add_argument("--info", action="store_true", help="获取设备 MIoT 信息 / Get device info")

    args = parser.parse_args()

    if args.info:
        # 获取设备 MIoT 信息 / Get device info
        target = args.did or args.name
        if not target:
            print("请提供 --did (model名) 或 --name / Provide --did (model) or --name", file=sys.stderr)
            sys.exit(1)
        print(f"获取设备 MIoT 信息 / Getting device info...", flush=True)
        out = run_mijia("--get_device_info", target)
        if out:
            print(out, flush=True)
        return

    if args.value is not None:
        # 设置属性 / Set property
        target_args = []
        if args.did:
            target_args = ["--did", args.did]
        elif args.name:
            target_args = ["--dev_name", args.name]
        else:
            print("请提供 --did 或 --name / Provide --did or --name", file=sys.stderr)
            sys.exit(1)

        print(f"设置 / Setting: prop={args.prop} value={args.value}", flush=True)
        out = run_mijia("set", *target_args, "--prop_name", args.prop, "--value", str(args.value))
    else:
        # 读取属性 / Get property
        target_args = []
        if args.did:
            target_args = ["--did", args.did]
        elif args.name:
            target_args = ["--dev_name", args.name]
        else:
            print("请提供 --did 或 --name / Provide --did or --name", file=sys.stderr)
            sys.exit(1)

        print(f"读取 / Reading: prop={args.prop}", flush=True)
        out = run_mijia("get", *target_args, "--prop_name", args.prop)

    if out:
        print(f"结果 / Result:\n{out}", flush=True)
    else:
        print("操作失败 / Operation failed", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
