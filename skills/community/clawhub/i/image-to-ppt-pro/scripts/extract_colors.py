#!/usr/bin/env python3
"""
extract_colors.py — Precisely extract colors from various regions of PPT images
Usage: python scripts/extract_colors.py [image_path]
"""
import sys
from PIL import Image

def sample(img, x1, y1, x2, y2, n=8):
    """Grid sampling taking median of each channel, inset 5px to avoid borders/shadows"""
    x1,y1,x2,y2 = int(x1)+5,int(y1)+5,int(x2)-5,int(y2)-5
    if x2<=x1 or y2<=y1:
        px = img.getpixel((x1,y1))[:3]
        return f"{px[0]:02X}{px[1]:02X}{px[2]:02X}"
    xs = [x1+(x2-x1)*i//(n-1) for i in range(n)]
    ys = [y1+(y2-y1)*i//(n-1) for i in range(n)]
    cols = [img.getpixel((x,y))[:3] for x in xs for y in ys]
    r = sorted(c[0] for c in cols)[len(cols)//2]
    g = sorted(c[1] for c in cols)[len(cols)//2]
    b = sorted(c[2] for c in cols)[len(cols)//2]
    return f"{r:02X}{g:02X}{b:02X}"

def main():
    img_path = sys.argv[1] if len(sys.argv)>1 else "/mnt/user-data/uploads/your_image.jpg"
    img = Image.open(img_path).convert("RGB")
    W, H = img.size

    print(f"Image size: {W} × {H} px")
    print(f"Coordinate conversion: x\" = px_x × {10/W:.5f}    y\" = px_y × {5.625/H:.5f}")
    print(f"                      w\" = px_w × {10/W:.5f}    h\" = px_h × {5.625/H:.5f}\n")

    # Preset common regions by proportion, adjust coordinates based on actual image content
    regions = {
        "Background":     (W*.4,  H*.4,  W*.6,  H*.6),
        "Header":         (W*.01, H*.01, W*.99, H*.13),
        "Title Text":     (W*.03, H*.02, W*.65, H*.11),
        "Content Area":   (W*.05, H*.18, W*.95, H*.82),
        "Footer":         (W*.01, H*.87, W*.99, H*.99),
    }

    print(f"{'Region':<12} {'hex':<8}  Sampling range (px)")
    print("-" * 52)
    for name, (x1,y1,x2,y2) in regions.items():
        color = sample(img, x1,y1,x2,y2)
        print(f"{name:<12} #{color}    ({int(x1)},{int(y1)}) → ({int(x2)},{int(y2)})")

    print("\n# Custom single point sampling:")
    print(f"# img = Image.open('{img_path}').convert('RGB')")
    print(f"# r,g,b = img.getpixel((x, y))[:3]; print(f'{{r:02X}}{{g:02X}}{{b:02X}}')")

if __name__ == "__main__":
    main()
