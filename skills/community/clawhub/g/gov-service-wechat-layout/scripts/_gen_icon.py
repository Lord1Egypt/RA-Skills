"""Generate a 512x512 PNG icon for the gov-service-wechat-layout skill.

Brand color #ff6d4d (theme slot). A white "article card" on the brand
background, with a title bar and body lines — reads as a WeChat article
at a glance. Run with the managed Python venv that has Pillow installed.
"""
from PIL import Image, ImageDraw

S = 512
BRAND = (255, 109, 77, 255)  # #ff6d4d
WHITE = (255, 255, 255, 255)
LINE = (223, 226, 230, 255)

img = Image.new("RGBA", (S, S), BRAND)
d = ImageDraw.Draw(img)

# white "article card"
card = (92, 84, 420, 444)
d.rounded_rectangle(card, radius=30, fill=WHITE)

# title bar
d.rounded_rectangle((138, 138, 300, 180), radius=12, fill=BRAND)

# body lines
y = 224
widths = [286, 286, 286, 250, 196]
for w in widths:
    d.rounded_rectangle((138, y, 138 + w, y + 16), radius=8, fill=LINE)
    y += 44

out = r"C:/Users/Quinn/.workbuddy/skills/gov-service-wechat-layout/assets/icon.png"
img.save(out)
print("saved", out, img.size)
