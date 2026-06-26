"""
Course Promo Image Generator
Creates professional 1080x1350 course promotional images with Pillow.
"""

from PIL import Image, ImageDraw, ImageFont
import os, sys

# === CONFIGURATION ===
OUTPUT_DIR = os.environ.get("IG_PIPELINE_OUTPUT_DIR", r".\output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# === COLORS ===
BG_TOP = (10, 15, 40)
BG_BOTTOM = (20, 40, 90)
ACCENT = (255, 180, 50)
WHITE = (255, 255, 255)
LIGHT_GRAY = (200, 210, 230)
W, H = 1080, 1350

# === FONTS ===
def get_font(size, bold=False):
    for fp in [
        "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/tahoma.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/TTF/DejaVuSans.ttf",
    ]:
        if os.path.exists(fp):
            try:
                return ImageFont.truetype(fp, size)
            except Exception:
                pass
    return ImageFont.load_default()

def generate_course_promo(
    course_name,
    institution,
    duration,
    bullets,
    hook_lines,
    cta_text,
    handle,
    output_filename="course_promo.png",
    output_dir=None
):
    """
    Generate a course promo image.

    Args:
        course_name:     e.g. "Diploma in Artificial Intelligence"
        institution:     e.g. "CADDESK Centre"
        duration:        e.g. "90 Weeks"
        bullets:         list of 4-6 learning outcomes
        hook_lines:      list of 1-3 bold headline lines
        cta_text:        call-to-action text
        handle:          Instagram handle, e.g. "@caddeskcentre"
        output_filename: filename for the output PNG
        output_dir:      output directory (defaults to IG_PIPELINE_OUTPUT_DIR or ./output)

    Returns:
        Path to the saved image file.
    """
    out = output_dir or OUTPUT_DIR
    os.makedirs(out, exist_ok=True)

    img = Image.new("RGB", (W, H), BG_TOP)
    draw = ImageDraw.Draw(img)

    # Gradient background
    for y in range(H):
        t = y / H
        r = int(BG_TOP[0] + (BG_BOTTOM[0] - BG_TOP[0]) * t)
        g = int(BG_TOP[1] + (BG_BOTTOM[1] - BG_TOP[1]) * t)
        b = int(BG_TOP[2] + (BG_BOTTOM[2] - BG_TOP[2]) * t)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    # Top accent bar
    draw.rectangle([(0, 0), (W, 8)], fill=ACCENT)

    # Geometric corner accents
    draw.polygon([(W - 200, 0), (W, 0), (W, 200)], fill=(255, 180, 50, 40))
    draw.polygon([(W - 120, 0), (W, 0), (W, 120)], fill=(255, 180, 50, 20))

    # Institution name
    title_font = get_font(72, bold=True)
    inst_w = draw.textbbox((0, 0), institution.upper(), font=title_font)[2]
    draw.text(((W - inst_w) // 2, 50), institution.upper(), font=title_font, fill=ACCENT)

    # Divider
    draw.rectangle([(W // 2 - 100, 135), (W // 2 + 100, 140)], fill=ACCENT)

    # Course badge
    sub_font = get_font(42)
    badge_w = draw.textbbox((0, 0), course_name.upper(), font=sub_font)[2]
    draw.text(((W - badge_w) // 2, 165), course_name.upper(), font=sub_font, fill=WHITE)

    # Hook lines
    y_pos = 280
    for line in hook_lines:
        hook_font = get_font(80, bold=True)
        lw = draw.textbbox((0, 0), line, font=hook_font)[2]
        draw.text(((W - lw) // 2, y_pos), line, font=hook_font, fill=WHITE)
        y_pos += 90

    # Section label
    y_pos = 530
    small_font = get_font(26)
    sl_w = draw.textbbox((0, 0), "WHAT YOU'LL MASTER", font=small_font)[2]
    draw.text(((W - sl_w) // 2, y_pos), "WHAT YOU'LL MASTER", font=small_font, fill=ACCENT)
    y_pos += 40

    # Bullet points
    body_font = get_font(32)
    bullet_y = y_pos + 15
    for bullet in bullets:
        cx, cy = 200, bullet_y + 15
        draw.polygon([(cx, cy - 10), (cx + 10, cy), (cx, cy + 10), (cx - 10, cy)], fill=ACCENT)
        draw.text((230, bullet_y), bullet, font=body_font, fill=LIGHT_GRAY)
        bullet_y += 52

    # Duration divider
    y_pos = bullet_y + 25
    div_line = "-" * 20
    div_w = draw.textbbox((0, 0), div_line, font=small_font)[2]
    draw.text(((W - div_w) // 2, y_pos), div_line, font=small_font, fill=(100, 120, 160))

    y_pos += 45
    cta_font = get_font(38, bold=True)
    dur_w = draw.textbbox((0, 0), duration.upper(), font=cta_font)[2]
    draw.text(((W - dur_w) // 2, y_pos), duration.upper(), font=cta_font, fill=ACCENT)

    # Bottom CTA strip
    strip_y = H - 300
    for y in range(strip_y, H):
        t = (y - strip_y) / (H - strip_y)
        r = int(10 + 5 * t)
        g = int(15 + 10 * t)
        b = int(40 + 20 * t)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    draw.rectangle([(0, H - 10), (W, H)], fill=ACCENT)

    cta_y = H - 240
    c1_w = draw.textbbox((0, 0), cta_text, font=body_font)[2]
    draw.text(((W - c1_w) // 2, cta_y), cta_text, font=body_font, fill=LIGHT_GRAY)

    cta_y += 50
    cta2_w = draw.textbbox((0, 0), "Enroll Today at " + institution, font=cta_font)[2]
    draw.text(((W - cta2_w) // 2, cta_y), "Enroll Today at " + institution, font=cta_font, fill=WHITE)

    h_w = draw.textbbox((0, 0), handle, font=small_font)[2]
    draw.text(((W - h_w) // 2, H - 90), handle, font=small_font, fill=(150, 160, 200))

    output_path = os.path.join(out, output_filename)
    img.save(output_path, "PNG", quality=95)
    print(f"[OK] Saved: {output_path}")
    return output_path

# === CLI ===
if __name__ == "__main__":
    # Defaults for testing
    path = generate_course_promo(
        course_name=os.environ.get("COURSE_NAME", "Diploma in Artificial Intelligence"),
        institution=os.environ.get("INSTITUTION", "CADDESK Centre"),
        duration=os.environ.get("DURATION", "90 Weeks"),
        bullets=[
            "Machine Learning & Data Science",
            "Building Intelligent Systems",
            "Algorithm Development",
            "Real-World AI Projects",
        ],
        hook_lines=["Your Future in AI", "Starts Here."],
        cta_text=os.environ.get("CTA_TEXT", "Ready to shape the future with AI?"),
        handle=os.environ.get("IG_HANDLE", "@caddeskcentre"),
        output_filename=os.environ.get("OUTPUT_FILENAME", "course_promo.png"),
        output_dir=os.environ.get("IG_PIPELINE_OUTPUT_DIR", None),
    )
    print(f"Image: {path}")
