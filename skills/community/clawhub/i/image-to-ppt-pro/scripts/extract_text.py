#!/usr/bin/env python3
"""
extract_text.py — OCR extraction of text from PPT images
Usage: python scripts/extract_text.py [image_path]

Dependencies (auto-installed on first run):
  pip install pytesseract Pillow --break-system-packages
  apt-get install -y tesseract-ocr tesseract-ocr-chi-sim
"""
import sys, subprocess
from PIL import Image

def ensure_deps():
    try:
        import pytesseract
        pytesseract.get_tesseract_version()
        return pytesseract
    except Exception:
        print("Installing tesseract-ocr...")
        subprocess.run(["apt-get","install","-y","-q",
                        "tesseract-ocr","tesseract-ocr-chi-sim"], check=True)
        subprocess.run([sys.executable,"-m","pip","install","pytesseract",
                        "--break-system-packages","-q"], check=True)
        import pytesseract
        return pytesseract

def ocr_region(img, x1, y1, x2, y2, scale=2, lang="chi_sim+eng"):
    """Crop region and enlarge before OCR, higher scale = better accuracy"""
    crop = img.crop((int(x1),int(y1),int(x2),int(y2)))
    if scale > 1:
        crop = crop.resize((crop.width*scale, crop.height*scale), Image.LANCZOS)
    raw = tess.image_to_string(crop, lang=lang).strip()
    return "\n".join(line for line in raw.splitlines() if line.strip())

tess = ensure_deps()

img_path = sys.argv[1] if len(sys.argv)>1 else "/mnt/user-data/uploads/your_image.jpg"
img = Image.open(img_path).convert("RGB")
W, H = img.size
print(f"Image size: {W} × {H} px\n")

# ── Full image scan ────────────────────────────────────────────────────────────────
print("=" * 40)
print("Full image scan (quickly get all text)")
print("=" * 40)
full = tess.image_to_string(img, lang="chi_sim+eng").strip()
print(full if full else "(No text recognized)")

# ── Region precise extraction ─────────────────────────────────────────────────────────────
print("\n" + "=" * 40)
print("Region precise extraction")
print("=" * 40)
regions = {
    "Header":  (W*.02, H*.01, W*.88, H*.13),
    "Footer Left":  (W*.02, H*.87, W*.38, H*.99),
    "Footer Center":  (W*.38, H*.87, W*.72, H*.99),
    "Footer Right":  (W*.72, H*.87, W*.98, H*.99),
}
for name, (x1,y1,x2,y2) in regions.items():
    text = ocr_region(img, x1,y1,x2,y2)
    print(f"\n[{name}]")
    print(text if text else "(Empty)")

print("\n# Custom region:")
print("# text = ocr_region(img, x1, y1, x2, y2, scale=2)")
print("# print(text)")
