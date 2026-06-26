"""Create a contact sheet from project keyframes or character images."""
import argparse
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def load_font(size):
    for path in [r"C:\Windows\Fonts\malgun.ttf", r"C:\Windows\Fonts\arial.ttf"]:
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            pass
    return ImageFont.load_default()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", required=True)
    ap.add_argument("--glob", default="keyframes/*.png")
    ap.add_argument("--out", default=None)
    ap.add_argument("--cols", type=int, default=3)
    ap.add_argument("--thumb-width", type=int, default=416)
    ap.add_argument("--thumb-height", type=int, default=240)
    args = ap.parse_args()

    project = Path(args.project)
    files = sorted(project.glob(args.glob))
    if not files:
        raise FileNotFoundError(f"No images matched {project / args.glob}")
    rows = math.ceil(len(files) / args.cols)
    label_h = 28
    sheet = Image.new("RGB", (args.cols * args.thumb_width, rows * (args.thumb_height + label_h)), "white")
    draw = ImageDraw.Draw(sheet)
    font = load_font(18)

    for idx, path in enumerate(files):
        col = idx % args.cols
        row = idx // args.cols
        x = col * args.thumb_width
        y = row * (args.thumb_height + label_h)
        im = Image.open(path).convert("RGB")
        im.thumbnail((args.thumb_width, args.thumb_height), Image.LANCZOS)
        tile = Image.new("RGB", (args.thumb_width, args.thumb_height), (20, 20, 20))
        tile.paste(im, ((args.thumb_width - im.width) // 2, (args.thumb_height - im.height) // 2))
        sheet.paste(tile, (x, y))
        draw.rectangle([x, y + args.thumb_height, x + args.thumb_width, y + args.thumb_height + label_h], fill=(0, 0, 0))
        draw.text((x + 8, y + args.thumb_height + 3), path.stem, fill="white", font=font)

    out = Path(args.out) if args.out else project / "final" / "keyframe_contact_sheet.jpg"
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out, quality=92)
    print(out.resolve())


if __name__ == "__main__":
    main()
