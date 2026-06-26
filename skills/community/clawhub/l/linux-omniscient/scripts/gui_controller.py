#!/usr/bin/env python3
"""GUI Controller - Linux version (cross-platform)."""
import subprocess, json, sys, os, argparse, time
from common import run_cmd

def screenshot(output=None):
    """Take screenshot (full screen)."""
    output_path = output or f'/tmp/screenshot_{int(time.time())}.png'
    stdout, _, code = run_cmd(['scrot', output_path])
    return json.dumps({"screenshot": output_path if code == 0 else "error"}, indent=2)

def mouse_click(x, y):
    """Click at coordinates."""
    stdout, _, code = run_cmd(['xdotool', 'mousemove', str(x), str(y), 'click', '1'])
    return json.dumps({"success": code == 0}, indent=2)

def mouse_move(x, y):
    """Move mouse to coordinates."""
    stdout, _, code = run_cmd(['xdotool', 'mousemove', str(x), str(y)])
    return json.dumps({"success": code == 0}, indent=2)

def keyboard_type(text):
    """Type text."""
    stdout, _, code = run_cmd(['xdotool', 'type', text])
    return json.dumps({"success": code == 0}, indent=2)

def visual_ocr():
    """OCR screen text."""
    try:
        import pytesseract
        from PIL import ImageGrab
        screenshot = ImageGrab.grab()
        text = pytesseract.image_to_string(screenshot)
        return json.dumps({"text": text}, indent=2)
    except ImportError:
        return json.dumps({"error": "Install pytesseract and Pillow"}, indent=2)

def visual_click_image(template):
    """Click on image template match."""
    try:
        import cv2
        import numpy as np
        from PIL import ImageGrab

        # Capture screen
        screenshot = ImageGrab.grab()
        screen_np = np.array(screenshot)

        # Load template
        template_img = cv2.imread(template, cv2.IMREAD_COLOR)
        if template_img is None:
            return json.dumps({"error": "Template not found"}, indent=2)

        # Match template
        result = cv2.matchTemplate(screen_np, template_img, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        if max_val > 0.8:
            x, y = max_loc
            h, w = template_img.shape[:2]
            center_x, center_y = x + w//2, y + h//2
            # Click at center
            stdout, _, code = run_cmd(['xdotool', 'mousemove', str(center_x), str(center_y), 'click', '1'])
            return json.dumps({"success": True, "x": center_x, "y": center_y}, indent=2)
        else:
            return json.dumps({"success": False, "message": "Template not found"}, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)

def main():
    parser = argparse.ArgumentParser(description='GUI Controller')
    subparsers = parser.add_subparsers(dest='command')

    # screenshot command
    ss_parser = subparsers.add_parser('screenshot')
    ss_parser.add_argument('mode', choices=['full', 'window', 'region'])

    # mouse command
    mouse_parser = subparsers.add_parser('mouse')
    mouse_subparsers = mouse_parser.add_subparsers(dest='mouse_cmd')
    mouse_click = mouse_subparsers.add_parser('click')
    mouse_click.add_argument('--x', type=int, required=True)
    mouse_click.add_argument('--y', type=int, required=True)
    mouse_move = mouse_subparsers.add_parser('move')
    mouse_move.add_argument('--x', type=int, required=True)
    mouse_move.add_argument('--y', type=int, required=True)

    # keyboard command
    kb_parser = subparsers.add_parser('keyboard')
    kb_subparsers = kb_parser.add_subparsers(dest='kb_cmd')
    kb_type = kb_subparsers.add_parser('type')
    kb_type.add_argument('--text', required=True)

    # visual command
    visual_parser = subparsers.add_parser('visual')
    visual_subparsers = visual_parser.add_subparsers(dest='visual_cmd')
    visual_subparsers.add_parser('ocr')
    v_click = visual_subparsers.add_parser('click-image')
    v_click.add_argument('--template', required=True)

    args = parser.parse_args()

    if args.command == 'screenshot':
        print(screenshot())
    elif args.command == 'mouse':
        if args.mouse_cmd == 'click':
            print(mouse_click(args.x, args.y))
        elif args.mouse_cmd == 'move':
            print(mouse_move(args.x, args.y))
    elif args.command == 'keyboard':
        if args.kb_cmd == 'type':
            print(keyboard_type(args.text))
    elif args.command == 'visual':
        if args.visual_cmd == 'ocr':
            print(visual_ocr())
        elif args.visual_cmd == 'click-image':
            print(visual_click_image(args.template))

if __name__ == '__main__':
    main()
