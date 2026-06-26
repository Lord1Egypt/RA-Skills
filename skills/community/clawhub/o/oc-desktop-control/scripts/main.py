#!/usr/bin/env python3
"""
Desktop Control - CLI Entry Point

Commands:
  connect     - Connect to desktop environment
  screenshot  - Capture screenshot
  mouse       - Mouse control (move, click, drag, scroll)
  keyboard    - Keyboard control (type, press)
  app         - Application management
  file        - File operations
  automation  - Run automation scripts
"""

import argparse
import base64
import json
import os
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
LIB_DIR = SCRIPT_DIR.parent / 'lib'
sys.path.insert(0, str(LIB_DIR))

from desktop_controller import LocalDisplayController


def cmd_screenshot(args):
    """Capture screenshot"""
    controller = LocalDisplayController()
    controller.connect()

    try:
        region = None
        if args.region:
            parts = args.region.split(',')
            region = tuple(int(p) for p in parts)

        if args.base64:
            data = controller.screenshot_base64(region)
            print(data)
        else:
            image_data = controller.screenshot(region)
            if args.output:
                Path(args.output).write_bytes(image_data)
                print(f"✅ Screenshot saved to: {args.output}")
            else:
                # Output to stdout as base64
                print(base64.b64encode(image_data).decode('utf-8'))
    finally:
        controller.disconnect()


def cmd_mouse(args):
    """Mouse control"""
    controller = LocalDisplayController()
    controller.connect()

    try:
        if args.action == 'move':
            controller.mouse_move(args.x, args.y)
            print(f"✅ Mouse moved to ({args.x}, {args.y})")

        elif args.action == 'click':
            controller.mouse_click(args.x, args.y, args.button, args.clicks)
            coord = f"({args.x}, {args.y})" if args.x and args.y else "current position"
            print(f"✅ Mouse clicked {args.button} {args.clicks}x at {coord}")

        elif args.action == 'drag':
            fx, fy = map(int, args.from_coord.split(','))
            tx, ty = map(int, args.to_coord.split(','))
            controller.mouse_drag(fx, fy, tx, ty, args.button)
            print(f"✅ Mouse dragged from ({fx},{fy}) to ({tx},{ty})")

        elif args.action == 'scroll':
            controller.mouse_scroll(args.direction, args.amount, args.x, args.y)
            print(f"✅ Scrolled {args.direction} {args.amount}x")

        elif args.action == 'position':
            x, y = controller.mouse_position()
            print(f"Mouse position: ({x}, {y})")

    finally:
        controller.disconnect()


def cmd_keyboard(args):
    """Keyboard control"""
    controller = LocalDisplayController()
    controller.connect()

    try:
        if args.action == 'type':
            controller.type_text(args.text, args.delay)
            print(f"✅ Typed: {args.text}")

        elif args.action == 'press':
            keys = args.keys.split(',')
            controller.key_press(keys)
            print(f"✅ Pressed: {keys}")

        elif args.action == 'hold':
            controller.key_down(args.key)
            print(f"✅ Holding: {args.key}")

        elif args.action == 'release':
            controller.key_up(args.key)
            print(f"✅ Released: {args.key}")

    finally:
        controller.disconnect()


def cmd_app(args):
    """Application management"""
    controller = LocalDisplayController()
    controller.connect()

    try:
        if args.action == 'open':
            controller.open_application(args.name)
            print(f"✅ Opened: {args.name}")

        elif args.action == 'close':
            controller.close_application(args.name)
            print(f"✅ Closed: {args.name}")

        elif args.action == 'desktop':
            controller.key_press(['command'])  # Show desktop
            print("✅ Switched to desktop")

    finally:
        controller.disconnect()


def cmd_file(args):
    """File operations"""
    controller = LocalDisplayController()
    controller.connect()

    try:
        if args.action == 'read':
            data = controller.read_file(args.path)
            if data:
                if args.base64:
                    print(base64.b64encode(data).decode('utf-8'))
                else:
                    try:
                        print(data.decode('utf-8'))
                    except UnicodeDecodeError:
                        print(base64.b64encode(data).decode('utf-8'))
            else:
                print(f"❌ Failed to read: {args.path}", file=sys.stderr)

        elif args.action == 'write':
            content = args.content.encode('utf-8')
            if args.base64:
                content = base64.b64decode(args.content)
            success = controller.write_file(args.path, content)
            if success:
                print(f"✅ Written: {args.path}")
            else:
                print(f"❌ Failed to write: {args.path}", file=sys.stderr)

    finally:
        controller.disconnect()


def cmd_automation(args):
    """Run automation scripts"""
    controller = LocalDisplayController()
    controller.connect()

    try:
        if args.action == 'run':
            results = controller.execute_script(args.script)
            print(f"✅ Executed {len(results)} commands")
            for r in results:
                print(f"  Line {r['line']}: {r['result']}")

        elif args.action == 'wait':
            # Simple wait for now
            controller.wait(args.timeout * 1000)
            print(f"✅ Waited {args.timeout}s")

    finally:
        controller.disconnect()


def cmd_connect(args):
    """Connect to desktop (placeholder for VNC/RDP)"""
    print("✅ Connected to local display")
    print("Currently only local display is supported")
    print("VNC/RDP support coming soon!")


def main():
    parser = argparse.ArgumentParser(
        description='Desktop Control - Remote desktop automation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Screenshot
  python3 main.py screenshot --output screen.png

  # Mouse control
  python3 main.py mouse move --x 500 --y 300
  python3 main.py mouse click --x 500 --y 300 --button left

  # Keyboard
  python3 main.py keyboard type "Hello World"
  python3 main.py keyboard press --keys ctrl,c

  # Run script
  python3 main.py automation run --script script.txt
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # connect command
    connect_parser = subparsers.add_parser('connect', help='Connect to desktop')
    connect_parser.add_argument('--host', help='Remote host')
    connect_parser.add_argument('--port', type=int, help='Remote port')
    connect_parser.add_argument('--password', help='Password')
    connect_parser.add_argument('--local', action='store_true', help='Use local display')
    connect_parser.set_defaults(func=cmd_connect)

    # screenshot command
    screenshot_parser = subparsers.add_parser('screenshot', help='Capture screenshot')
    screenshot_parser.add_argument('--output', '-o', help='Output file path')
    screenshot_parser.add_argument('--region', '-r', help='Region: x,y,width,height')
    screenshot_parser.add_argument('--base64', action='store_true', help='Output as base64')
    screenshot_parser.set_defaults(func=cmd_screenshot)

    # mouse command
    mouse_parser = subparsers.add_parser('mouse', help='Mouse control')
    mouse_subparsers = mouse_parser.add_subparsers(dest='action', help='Mouse actions')

    move_parser = mouse_subparsers.add_parser('move', help='Move mouse')
    move_parser.add_argument('--x', type=int, required=True)
    move_parser.add_argument('--y', type=int, required=True)

    click_parser = mouse_subparsers.add_parser('click', help='Click mouse')
    click_parser.add_argument('--x', type=int)
    click_parser.add_argument('--y', type=int)
    click_parser.add_argument('--button', default='left', choices=['left', 'right', 'middle'])
    click_parser.add_argument('--clicks', type=int, default=1)

    drag_parser = mouse_subparsers.add_parser('drag', help='Drag mouse')
    drag_parser.add_argument('--from-coord', required=True, help='From: x,y')
    drag_parser.add_argument('--to-coord', required=True, help='To: x,y')
    drag_parser.add_argument('--button', default='left')

    scroll_parser = mouse_subparsers.add_parser('scroll', help='Scroll')
    scroll_parser.add_argument('--direction', required=True, choices=['up', 'down', 'left', 'right'])
    scroll_parser.add_argument('--amount', type=int, default=1)
    scroll_parser.add_argument('--x', type=int)
    scroll_parser.add_argument('--y', type=int)

    position_parser = mouse_subparsers.add_parser('position', help='Get position')

    mouse_parser.set_defaults(func=cmd_mouse)

    # keyboard command
    keyboard_parser = subparsers.add_parser('keyboard', help='Keyboard control')
    keyboard_subparsers = keyboard_parser.add_subparsers(dest='action', help='Keyboard actions')

    type_parser = keyboard_subparsers.add_parser('type', help='Type text')
    type_parser.add_argument('text', help='Text to type')
    type_parser.add_argument('--delay', type=float, help='Delay between keystrokes')

    press_parser = keyboard_subparsers.add_parser('press', help='Press keys')
    press_parser.add_argument('--keys', required=True, help='Keys: key1,key2,...')

    hold_parser = keyboard_subparsers.add_parser('hold', help='Hold key')
    hold_parser.add_argument('--key', required=True)

    release_parser = keyboard_subparsers.add_parser('release', help='Release key')
    release_parser.add_argument('--key', required=True)

    keyboard_parser.set_defaults(func=cmd_keyboard)

    # app command
    app_parser = subparsers.add_parser('app', help='Application management')
    app_subparsers = app_parser.add_subparsers(dest='action', help='App actions')

    open_parser = app_subparsers.add_parser('open', help='Open app')
    open_parser.add_argument('--name', required=True)

    close_parser = app_subparsers.add_parser('close', help='Close app')
    close_parser.add_argument('--name', required=True)

    desktop_parser = app_subparsers.add_parser('desktop', help='Show desktop')

    app_parser.set_defaults(func=cmd_app)

    # file command
    file_parser = subparsers.add_parser('file', help='File operations')
    file_subparsers = file_parser.add_subparsers(dest='action', help='File actions')

    read_parser = file_subparsers.add_parser('read', help='Read file')
    read_parser.add_argument('--path', required=True)
    read_parser.add_argument('--base64', action='store_true')

    write_parser = file_subparsers.add_parser('write', help='Write file')
    write_parser.add_argument('--path', required=True)
    write_parser.add_argument('--content', required=True)
    write_parser.add_argument('--base64', action='store_true')

    file_parser.set_defaults(func=cmd_file)

    # automation command
    auto_parser = subparsers.add_parser('automation', help='Automation')
    auto_subparsers = auto_parser.add_subparsers(dest='action', help='Automation actions')

    run_parser = auto_subparsers.add_parser('run', help='Run script')
    run_parser.add_argument('--script', required=True)

    wait_parser = auto_subparsers.add_parser('wait', help='Wait')
    wait_parser.add_argument('--timeout', type=int, default=5, help='Seconds to wait')

    auto_parser.set_defaults(func=cmd_automation)

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(1)

    args.func(args)


if __name__ == '__main__':
    main()
