#!/usr/bin/env python3
"""
Xiaomi Mijia Fan Control CLI
用法：
  fan_cli.py on                    开风扇
  fan_cli.py off                   关风扇
  fan_cli.py toggle                切换开关
  fan_cli.py status                查看状态
  fan_cli.py speed [1-100]         设置风速（0=关闭，1-100对应档位）
  fan_cli.py swing [on|off]        摆风
  fan_cli.py list                  列出所有设备

环境变量：
  MIJIA_FAN_DID          必填，风扇设备 DID
  MIJIA_FAN_SIID         可选，默认 2（属性服务ID）
  MIJIA_FAN_POWER_PIID   可选，默认 1（电源属性ID）
  MIJIA_FAN_SPEED_PIID   可选，默认 2（风速属性ID）
  MIJIA_FAN_SWING_PIID   可选，默认 5（摆风属性ID）
"""
import argparse
import os
import sys
import json

MIJIA_FAN_DID = os.environ.get("MIJIA_FAN_DID")
MIJIA_FAN_SIID = int(os.environ.get("MIJIA_FAN_SIID", "2"))
MIJIA_FAN_POWER_PIID = int(os.environ.get("MIJIA_FAN_POWER_PIID", "1"))
MIJIA_FAN_SPEED_PIID = int(os.environ.get("MIJIA_FAN_SPEED_PIID", "2"))
MIJIA_FAN_SWING_PIID = int(os.environ.get("MIJIA_FAN_SWING_PIID", "5"))

if MIJIA_FAN_DID:
    DEVICE_ID = MIJIA_FAN_DID
else:
    DEVICE_ID = None


def get_api():
    from mijiaAPI import mijiaAPI
    api = mijiaAPI()
    api.login()
    return api


def get_prop(api, piid, siid=MIJIA_FAN_SIID):
    return api.get_devices_prop({
        'did': DEVICE_ID,
        'siid': siid,
        'piid': piid,
    })


def set_prop(api, piid, value, siid=MIJIA_FAN_SIID):
    return api.set_devices_prop({
        'did': DEVICE_ID,
        'siid': siid,
        'piid': piid,
        'value': value,
    })


def require_device():
    if not DEVICE_ID:
        print("Error: MIJIA_FAN_DID environment variable not set.")
        print("Set it with: export MIJIA_FAN_DID='your_device_id'")
        print("Tip: Run 'fan_cli.py list' to see all device IDs.")
        sys.exit(1)


def cmd_on(args, api):
    require_device()
    result = set_prop(api, MIJIA_FAN_POWER_PIID, True)
    code = result.get('code', -1)
    if code == 0:
        print("✅ 风扇已开启")
    else:
        print(f"❌ 操作失败，错误码: {code}")


def cmd_off(args, api):
    require_device()
    result = set_prop(api, MIJIA_FAN_POWER_PIID, False)
    code = result.get('code', -1)
    if code == 0:
        print("✅ 风扇已关闭")
    else:
        print(f"❌ 操作失败，错误码: {code}")


def cmd_toggle(args, api):
    require_device()
    status = get_prop(api, MIJIA_FAN_POWER_PIID)
    current = status.get('value', False)
    new_val = not current
    result = set_prop(api, MIJIA_FAN_POWER_PIID, new_val)
    code = result.get('code', -1)
    if code == 0:
        print(f"✅ 风扇已切换为 {'开启' if new_val else '关闭'}")
    else:
        print(f"❌ 操作失败，错误码: {code}")


def cmd_status(args, api):
    require_device()
    power = get_prop(api, MIJIA_FAN_POWER_PIID)
    speed = get_prop(api, MIJIA_FAN_SPEED_PIID)
    swing = get_prop(api, MIJIA_FAN_SWING_PIID)
    update_time = power.get('updateTime', 0)

    print(f"电源: {'开启 🔵' if power.get('value') else '关闭 ⚪'}")
    print(f"风速: {speed.get('value', 'N/A')}")
    print(f"摆风: {'开启 🌪️' if swing.get('value') else '关闭'}")
    print(f"更新时间戳: {update_time}")


def cmd_speed(args, api):
    require_device()
    value = args.value
    # 如果风速为0，视为关闭
    if value == 0:
        set_prop(api, MIJIA_FAN_POWER_PIID, False)
        print("✅ 风速设为0，风扇关闭")
    else:
        # 先确保开启，再设风速
        set_prop(api, MIJIA_FAN_POWER_PIID, True)
        result = set_prop(api, MIJIA_FAN_SPEED_PIID, value)
        code = result.get('code', -1)
        if code == 0:
            print(f"✅ 风速已设为 {value}")
        else:
            print(f"❌ 操作失败，错误码: {code}")


def cmd_swing(args, api):
    require_device()
    val = 1 if args.value == 'on' else 0
    result = set_prop(api, MIJIA_FAN_SWING_PIID, val)
    code = result.get('code', -1)
    if code == 0:
        print(f"✅ 摆风已{'开启' if val else '关闭'}")
    else:
        print(f"❌ 操作失败，错误码: {code}")


def cmd_list(args, api):
    """列出所有米家设备并高亮风扇类设备"""
    devices = api.get_device_list()
    print(f"\n{'='*50}")
    print(f"{'米家设备列表':^50}")
    print(f"{'='*50}")
    fan_keywords = ['fan', '风扇', '直流', '循环']
    for i, d in enumerate(devices, 1):
        name = d.get('name', '未知设备')
        did = d.get('did', '')
        model = d.get('model', '')
        is_fan = any(k in name.lower() or k in model.lower() for k in fan_keywords)
        marker = " ⭐ (可能是风扇)" if is_fan else ""
        print(f"{i}. {name}{marker}")
        print(f"   DID: {did}")
        print(f"   Model: {model}")
        print()
    print(f"总计 {len(devices)} 台设备")
    print(f"\n请设置环境变量 export MIJIA_FAN_DID='<DID>'")


def main():
    parser = argparse.ArgumentParser(
        description="Xiaomi Mijia 风扇控制工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    sub = parser.add_subparsers(dest='command', help='子命令')

    sub.add_parser('on',       help='开风扇')
    sub.add_parser('off',      help='关风扇')
    sub.add_parser('toggle',   help='切换开关')
    sub.add_parser('status',   help='查看状态')
    sub.add_parser('list',     help='列出所有设备')

    p_speed = sub.add_parser('speed', help='设置风速 (0=关, 1-100=档位)')
    p_speed.add_argument('value', type=int, help='风速值 0-100')

    p_swing = sub.add_parser('swing', help='设置摆风 on/off')
    p_swing.add_argument('value', choices=['on', 'off'], help='摆风开关')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    # list 命令不需要 DID
    if args.command == 'list':
        api = get_api()
        cmd_list(args, api)
        return

    api = get_api()

    cmd_map = {
        'on': cmd_on,
        'off': cmd_off,
        'toggle': cmd_toggle,
        'status': cmd_status,
        'speed': cmd_speed,
        'swing': cmd_swing,
    }
    cmd_map[args.command](args, api)


if __name__ == '__main__':
    main()
