#!/usr/bin/env python3
"""Camera Controller - cross-platform."""
import json, sys, os, argparse, time

def list_cameras():
    """List available cameras."""
    try:
        import cv2
        cameras = []
        index = 0
        while True:
            cap = cv2.VideoCapture(index)
            if not cap.read()[0]:
                cap.release()
                break
            cameras.append({"index": index, "width": cap.get(cv2.CAP_PROP_FRAME_WIDTH), "height": cap.get(cv2.CAP_PROP_FRAME_HEIGHT)})
            cap.release()
            index += 1
        return json.dumps({"cameras": cameras}, indent=2)
    except ImportError:
        return json.dumps({"cameras": [], "error": "Install opencv-python"}, indent=2)

def get_camera_params(index=0):
    """Get camera parameters."""
    try:
        import cv2
        cap = cv2.VideoCapture(index)
        params = {
            "width": cap.get(cv2.CAP_PROP_FRAME_WIDTH),
            "height": cap.get(cv2.CAP_PROP_FRAME_HEIGHT),
            "fps": cap.get(cv2.CAP_PROP_FPS),
            "brightness": cap.get(cv2.CAP_PROP_BRIGHTNESS),
            "contrast": cap.get(cv2.CAP_PROP_CONTRAST)
        }
        cap.release()
        return json.dumps({"params": params}, indent=2)
    except ImportError:
        return json.dumps({"error": "Install opencv-python"}, indent=2)

def capture_photo(output=None):
    """Capture a photo."""
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()
        if not ret:
            return json.dumps({"success": False, "error": "Failed to capture"}, indent=2)

        output_path = output or f'/tmp/photo_{int(time.time())}.png'
        cv2.imwrite(output_path, frame)
        return json.dumps({"success": True, "output": output_path}, indent=2)
    except ImportError:
        return json.dumps({"error": "Install opencv-python"}, indent=2)

def main():
    parser = argparse.ArgumentParser(description='Camera Controller')
    subparsers = parser.add_subparsers(dest='command')

    # list command
    subparsers.add_parser('list')

    # params command
    params_parser = subparsers.add_parser('params')
    params_parser.add_argument('--index', type=int, default=0)

    # capture command
    capture_parser = subparsers.add_parser('capture')
    capture_parser.add_argument('--output', help='Output path')

    args = parser.parse_args()

    if args.command == 'list':
        print(list_cameras())
    elif args.command == 'params':
        print(get_camera_params(args.index))
    elif args.command == 'capture':
        print(capture_photo(args.output))

if __name__ == '__main__':
    main()
