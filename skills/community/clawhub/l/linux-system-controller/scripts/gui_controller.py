#!/usr/bin/env python3
"""
GUI Controller - Mouse, keyboard, screenshot, and visual control for Linux.

Capabilities:
  - Mouse: move, click, double-click, right-click, drag, scroll, get position
  - Keyboard: type text, press hotkeys, key combinations
  - Screenshot: full screen, region, save to file
  - OCR: extract text from screen regions (requires tesseract-ocr)
  - Visual: find image/pattern on screen, click by color

Requirements: Linux with X11, pyautogui, pillow, tesseract-ocr (optional for OCR)
"""

import sys
import os
import json
import argparse

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')


def check_pyautogui():
    """Check if pyautogui is available."""
    try:
        import pyautogui
        pyautogui.PAUSE = 0.1  # Small delay for better reliability
        pyautogui.FAILSAFE = True  # Move mouse to corner to abort
        return pyautogui
    except ImportError:
        print("Installing pyautogui...", file=sys.stderr)
        import subprocess
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "pyautogui", "-q"],
            stdout=subprocess.DEVNULL
        )
        import pyautogui
        pyautogui.PAUSE = 0.1
        pyautogui.FAILSAFE = True
        return pyautogui


def check_pillow():
    """Check if pillow is available."""
    try:
        from PIL import Image, ImageGrab
        return Image, ImageGrab
    except ImportError:
        print("Installing pillow...", file=sys.stderr)
        import subprocess
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "pillow", "-q"],
            stdout=subprocess.DEVNULL
        )
        from PIL import Image, ImageGrab
        return Image, ImageGrab


def check_tesseract():
    """Check if pytesseract is available."""
    try:
        import pytesseract
        return pytesseract
    except ImportError:
        print("Installing pytesseract...", file=sys.stderr)
        import subprocess
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "pytesseract", "-q"],
            stdout=subprocess.DEVNULL
        )
        import pytesseract
        return pytesseract


# ============ Mouse ============

def mouse_move(x, y):
    """Move mouse to coordinates."""
    pyautogui = check_pyautogui()
    pyautogui.moveTo(x, y)
    return {"success": True, "position": {"x": x, "y": y}}


def mouse_click(x=None, y=None, button='left'):
    """Click mouse at coordinates."""
    pyautogui = check_pyautogui()
    if x is not None and y is not None:
        pyautogui.click(x, y, button=button)
    else:
        pyautogui.click(button=button)
    pos = pyautogui.position()
    return {"success": True, "position": {"x": pos.x, "y": pos.y}, "button": button}


def mouse_right_click(x=None, y=None):
    """Right click mouse."""
    return mouse_click(x, y, button='right')


def mouse_double_click(x=None, y=None):
    """Double click mouse."""
    pyautogui = check_pyautogui()
    if x is not None and y is not None:
        pyautogui.doubleClick(x, y)
    else:
        pyautogui.doubleClick()
    pos = pyautogui.position()
    return {"success": True, "position": {"x": pos.x, "y": pos.y}}


def mouse_drag(start_x, start_y, end_x, end_y, duration=0.5):
    """Drag mouse from start to end."""
    pyautogui = check_pyautogui()
    pyautogui.dragTo(end_x, end_y, duration=duration, button='left')
    return {"success": True, "from": {"x": start_x, "y": start_y}, "to": {"x": end_x, "y": end_y}}


def mouse_scroll(direction='down', clicks=1):
    """Scroll mouse wheel."""
    pyautogui = check_pyautogui()
    amount = -clicks if direction == 'down' else clicks
    pyautogui.scroll(amount)
    return {"success": True, "direction": direction, "clicks": clicks}


def mouse_position():
    """Get current mouse position."""
    pyautogui = check_pyautogui()
    pos = pyautogui.position()
    return {"position": {"x": pos.x, "y": pos.y}}


# ============ Keyboard ============

def keyboard_type(text):
    """Type text."""
    pyautogui = check_pyautogui()
    pyautogui.typewrite(text, interval=0.01)
    return {"success": True, "text": text}


def keyboard_press(keys):
    """Press hotkey combination (e.g., 'ctrl+c', 'alt+tab')."""
    pyautogui = check_pyautogui()
    pyautogui.hotkey(*keys.split('+'))
    return {"success": True, "keys": keys}


# ============ Screenshot ============

def screenshot_full(output_file=None):
    """Take full screenshot."""
    Image, ImageGrab = check_pillow()
    screenshot = ImageGrab.grab()

    if output_file:
        screenshot.save(output_file)
        return {"success": True, "file": output_file, "size": screenshot.size}
    else:
        # Save to default location
        import time
        filename = f"screenshot_{int(time.time())}.png"
        filepath = os.path.join(os.getcwd(), filename)
        screenshot.save(filepath)
        return {"success": True, "file": filepath, "size": screenshot.size}


def screenshot_region(x, y, width, height, output_file=None):
    """Take screenshot of region."""
    Image, ImageGrab = check_pillow()
    screenshot = ImageGrab.grab(bbox=(x, y, x + width, y + height))

    if output_file:
        screenshot.save(output_file)
        return {"success": True, "file": output_file, "size": screenshot.size}
    else:
        import time
        filename = f"region_{int(time.time())}.png"
        filepath = os.path.join(os.getcwd(), filename)
        screenshot.save(filepath)
        return {"success": True, "file": filepath, "size": screenshot.size}


def screenshot_size():
    """Get screen size."""
    pyautogui = check_pyautogui()
    size = pyautogui.size()
    return {"width": size.width, "height": size.height}


# ============ OCR ============

def visual_ocr(x=None, y=None, width=None, height=None, lang='eng'):
    """Extract text from screen using OCR."""
    try:
        pytesseract = check_tesseract()
    except Exception:
        return {"error": "tesseract-ocr not installed. Install with: apt-get install tesseract-ocr"}

    Image, ImageGrab = check_pillow()

    if x is not None and y is not None and width is not None and height is not None:
        screenshot = ImageGrab.grab(bbox=(x, y, x + width, y + height))
    else:
        screenshot = ImageGrab.grab()

    try:
        text = pytesseract.image_to_string(screenshot, lang=lang)
        return {"success": True, "text": text.strip()}
    except Exception as e:
        return {"error": f"OCR failed: {e}"}


# ============ Visual ============

def visual_find(template_path, confidence=0.8):
    """Find image template on screen."""
    pyautogui = check_pyautogui()
    try:
        location = pyautogui.locateOnScreen(template_path, confidence=confidence)
        if location:
            return {
                "success": True,
                "location": {
                    "left": location.left,
                    "top": location.top,
                    "width": location.width,
                    "height": location.height,
                    "center": {"x": location.left + location.width // 2, "y": location.top + location.height // 2}
                }
            }
        else:
            return {"error": "Template not found on screen"}
    except Exception as e:
        return {"error": f"Failed to find template: {e}"}


def visual_click_image(template_path, confidence=0.8):
    """Find and click image template."""
    result = visual_find(template_path, confidence)
    if "error" in result:
        return result

    center = result["location"]["center"]
    pyautogui = check_pyautogui()
    pyautogui.click(center["x"], center["y"])
    return {"success": True, "clicked": center}


def visual_pixel(x, y):
    """Get pixel color at coordinates."""
    Image, ImageGrab = check_pillow()
    screenshot = ImageGrab.grab()
    pixel = screenshot.getpixel((x, y))

    # Convert RGB to hex
    color_hex = f"#{pixel[0]:02x}{pixel[1]:02x}{pixel[2]:02x}"
    return {"success": True, "position": {"x": x, "y": y}, "color": {"r": pixel[0], "g": pixel[1], "b": pixel[2], "hex": color_hex}}


def main():
    parser = argparse.ArgumentParser(description="GUI Controller for Linux")
    subparsers = parser.add_subparsers(dest='category', help='Category to control')

    # Mouse
    mouse_parser = subparsers.add_parser('mouse', help='Mouse control')
    mouse_subparsers = mouse_parser.add_subparsers(dest='action', help='Mouse action')
    mouse_subparsers.add_parser('position', help='Get mouse position')
    mouse_move_parser = mouse_subparsers.add_parser('move', help='Move mouse')
    mouse_move_parser.add_argument('--x', type=int, required=True)
    mouse_move_parser.add_argument('--y', type=int, required=True)
    mouse_click_parser = mouse_subparsers.add_parser('click', help='Click mouse')
    mouse_click_parser.add_argument('--x', type=int)
    mouse_click_parser.add_argument('--y', type=int)
    mouse_subparsers.add_parser('right-click', help='Right click')
    mouse_subparsers.add_parser('double-click', help='Double click')
    mouse_drag_parser = mouse_subparsers.add_parser('drag', help='Drag mouse')
    mouse_drag_parser.add_argument('--start-x', type=int, required=True)
    mouse_drag_parser.add_argument('--start-y', type=int, required=True)
    mouse_drag_parser.add_argument('--end-x', type=int, required=True)
    mouse_drag_parser.add_argument('--end-y', type=int, required=True)
    mouse_scroll_parser = mouse_subparsers.add_parser('scroll', help='Scroll')
    mouse_scroll_parser.add_argument('--direction', choices=['up', 'down'], default='down')
    mouse_scroll_parser.add_argument('--clicks', type=int, default=10)

    # Keyboard
    keyboard_parser = subparsers.add_parser('keyboard', help='Keyboard control')
    keyboard_subparsers = keyboard_parser.add_subparsers(dest='action', help='Keyboard action')
    keyboard_type_parser = keyboard_subparsers.add_parser('type', help='Type text')
    keyboard_type_parser.add_argument('--text', required=True)
    keyboard_press_parser = keyboard_subparsers.add_parser('press', help='Press keys')
    keyboard_press_parser.add_argument('--keys', required=True)

    # Screenshot
    screenshot_parser = subparsers.add_parser('screenshot', help='Screenshot')
    screenshot_subparsers = screenshot_parser.add_subparsers(dest='action', help='Screenshot action')
    screenshot_subparsers.add_parser('full', help='Full screen screenshot')
    screenshot_region_parser = screenshot_subparsers.add_parser('region', help='Region screenshot')
    screenshot_region_parser.add_argument('--x', type=int, required=True)
    screenshot_region_parser.add_argument('--y', type=int, required=True)
    screenshot_region_parser.add_argument('--width', type=int, required=True)
    screenshot_region_parser.add_argument('--height', type=int, required=True)
    screenshot_subparsers.add_parser('size', help='Get screen size')

    # Visual
    visual_parser = subparsers.add_parser('visual', help='Visual recognition')
    visual_subparsers = visual_parser.add_subparsers(dest='action', help='Visual action')
    visual_subparsers.add_parser('ocr', help='OCR')
    visual_find_parser = visual_subparsers.add_parser('find', help='Find template')
    visual_find_parser.add_argument('--template', required=True)
    visual_click_image_parser = visual_subparsers.add_parser('click-image', help='Click image')
    visual_click_image_parser.add_argument('--template', required=True)
    visual_pixel_parser = visual_subparsers.add_parser('pixel', help='Get pixel color')
    visual_pixel_parser.add_argument('--x', type=int, required=True)
    visual_pixel_parser.add_argument('--y', type=int, required=True)

    args = parser.parse_args()

    if not args.category:
        parser.print_help()
        sys.exit(1)

    result = {}

    # Mouse
    if args.category == 'mouse':
        if args.action == 'position':
            result = mouse_position()
        elif args.action == 'move':
            result = mouse_move(args.x, args.y)
        elif args.action == 'click':
            result = mouse_click(args.x, args.y)
        elif args.action == 'right-click':
            result = mouse_right_click(args.x, args.y)
        elif args.action == 'double-click':
            result = mouse_double_click(args.x, args.y)
        elif args.action == 'drag':
            result = mouse_drag(args.start_x, args.start_y, args.end_x, args.end_y)
        elif args.action == 'scroll':
            result = mouse_scroll(args.direction, args.clicks)

    # Keyboard
    elif args.category == 'keyboard':
        if args.action == 'type':
            result = keyboard_type(args.text)
        elif args.action == 'press':
            result = keyboard_press(args.keys)

    # Screenshot
    elif args.category == 'screenshot':
        if args.action == 'full':
            result = screenshot_full()
        elif args.action == 'region':
            result = screenshot_region(args.x, args.y, args.width, args.height)
        elif args.action == 'size':
            result = screenshot_size()

    # Visual
    elif args.category == 'visual':
        if args.action == 'ocr':
            result = visual_ocr()
        elif args.action == 'find':
            result = visual_find(args.template)
        elif args.action == 'click-image':
            result = visual_click_image(args.template)
        elif args.action == 'pixel':
            result = visual_pixel(args.x, args.y)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
