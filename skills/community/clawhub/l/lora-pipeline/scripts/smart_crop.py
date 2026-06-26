from PIL import Image
import sys
import os

def smart_crop(img_path, side, ratio=0.6):
    """
    side: 'left' or 'right'
    ratio: percentage of width to keep
    """
    if not os.path.exists(img_path):
        print("File not found")
        return

    img = Image.open(img_path)
    w, h = img.size

    if side == 'left':
        crop_area = (0, 0, int(w * ratio), h)
    elif side == 'right':
        crop_area = (int(w * (1 - ratio)), 0, w, h)
    else:
        print("Side must be 'left' or 'right'")
        return

    basename = os.path.basename(img_path)
    name, ext = os.path.splitext(basename)
    out_path = os.path.join(os.path.dirname(img_path), f"{name}_crop_{side}{ext}")

    cropped = img.crop(crop_area)
    cropped.save(out_path)
    print(f"Saved: {out_path} ({cropped.size[0]}x{cropped.size[1]})")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 smart_crop.py <img_path> <left|right> [ratio]")
    else:
        ratio = float(sys.argv[3]) if len(sys.argv) > 3 else 0.6
        smart_crop(sys.argv[1], sys.argv[2], ratio)
