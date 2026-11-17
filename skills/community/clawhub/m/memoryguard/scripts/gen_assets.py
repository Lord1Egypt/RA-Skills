"""Generate PNG visual assets for README - replaces SVGs that GitHub won't render."""
from PIL import Image, ImageDraw, ImageFont
import os

INK = (8, 18, 31)
SLATE = (18, 36, 58)
SLATE2 = (13, 27, 42)
CYAN = (56, 213, 200)
AMBER = (243, 181, 98)
RED = (234, 106, 106)
PAPER = (238, 244, 248)
GRAY = (62, 85, 107)
DARK = (42, 63, 85)

def font(size, bold=False, mono=False):
    try:
        if mono:
            return ImageFont.truetype('C:/Windows/Fonts/consola.ttf', size)
        name = 'C:/Windows/Fonts/segoeuib.ttf' if bold else 'C:/Windows/Fonts/segoeui.ttf'
        return ImageFont.truetype(name, size)
    except Exception:
        return ImageFont.load_default()

OUT = os.path.join(os.path.dirname(__file__), '..', 'docs', 'assets')
os.makedirs(OUT, exist_ok=True)

# ============ HERO (1600x960) ============
W, H = 1600, 960
img = Image.new('RGB', (W, H), INK)
d = ImageDraw.Draw(img)

d.rectangle([0, 0, W, 56], fill=SLATE)
d.rounded_rectangle([24, 16, 220, 40], radius=4, fill=CYAN)
d.text((32, 18), 'MemoryGuard', font=font(18, True), fill=INK)

# Card 1: Event Stream
cx, cy, cw, ch = 24, 80, 760, 380
d.rounded_rectangle([cx, cy, cx+cw, cy+ch], radius=8, fill=SLATE2, outline=(30, 58, 82))
d.rectangle([cx, cy, cx+cw, cy+40], fill=SLATE)
d.text((cx+16, cy+12), 'Recent Events', font=font(16, True), fill=CYAN)

events = [
    ('Agent-1 wrote memory', CYAN, 'classify -> fact'),
    ('Agent-2 wrote memory', AMBER, 'supersede -> old v1'),
    ('Agent-1 wrote token', RED, 'quarantine -> blocked'),
    ('Agent-3 wrote memory', CYAN, 'dedup -> skipped'),
]
for i, (txt, color, action) in enumerate(events):
    y = cy + 56 + i * 56
    d.rounded_rectangle([cx+16, y, cx+cw-16, y+44], radius=4, fill=SLATE)
    d.rectangle([cx+24, y+8, cx+32, y+36], fill=color)
    d.text((cx+44, y+10), txt, font=font(15), fill=PAPER)
    d.text((cx+44, y+28), action, font=font(13), fill=GRAY)
    d.text((cx+cw-100, y+14), '2s ago', font=font(12), fill=DARK)

# Card 2: Supersede chain
cx2 = 816
d.rounded_rectangle([cx2, cy, cx2+cw, cy+ch], radius=8, fill=SLATE2, outline=(30, 58, 82))
d.rectangle([cx2, cy, cx2+cw, cy+40], fill=SLATE)
d.text((cx2+16, cy+12), 'Supersede Chain', font=font(16, True), fill=AMBER)

d.rounded_rectangle([cx2+16, cy+56, cx2+cw-16, cy+116], radius=4, fill=SLATE)
d.rectangle([cx2+24, cy+64, cx2+32, cy+108], fill=GRAY)
d.text((cx2+44, cy+66), 'Use PostgreSQL for analytics', font=font(15), fill=GRAY)
d.text((cx2+44, cy+86), 'superseded by v2', font=font(13), fill=DARK)

d.text((cx2+360, cy+124), 'v', font=font(20, True), fill=CYAN)

d.rounded_rectangle([cx2+16, cy+140, cx2+cw-16, cy+200], radius=4, fill=SLATE)
d.rectangle([cx2+24, cy+148, cx2+32, cy+192], fill=CYAN)
d.text((cx2+44, cy+150), 'Use SQLite locally; Postgres for prod', font=font(15), fill=PAPER)
d.text((cx2+44, cy+170), 'active v2', font=font(13), fill=CYAN)

d.rounded_rectangle([cx2+16, cy+220, cx2+360, cy+360], radius=4, fill=(10, 22, 32))
d.text((cx2+32, cy+232), 'Evidence', font=font(14, True), fill=GRAY)
d.text((cx2+32, cy+256), 'Source: Agent-2 write', font=font(13), fill=DARK)
d.text((cx2+32, cy+276), 'Reason: semantic supersede', font=font(13), fill=DARK)
d.text((cx2+32, cy+296), 'Confidence: 0.87', font=font(13), fill=DARK)
d.text((cx2+32, cy+316), 'Old version preserved', font=font(13), fill=CYAN)

# Card 3: Version History
cy2 = 480
d.rounded_rectangle([24, cy2, 784, cy2+456], radius=8, fill=SLATE2, outline=(30, 58, 82))
d.rectangle([24, cy2, 784, cy2+40], fill=SLATE)
d.text((40, cy2+12), 'Version History', font=font(16, True), fill=CYAN)

versions = [
    ('v3  current', CYAN, 'Use SQLite locally; Postgres for prod'),
    ('v2  superseded', AMBER, 'Use PostgreSQL for analytics'),
    ('v1  original', GRAY, 'Use SQLite for everything'),
]
for i, (label, color, txt) in enumerate(versions):
    y = cy2 + 56 + i * 72
    d.rounded_rectangle([40, y, 768, y+60], radius=4, fill=SLATE)
    d.rounded_rectangle([52, y+12, 124, y+44], radius=4, fill=(color[0]//4, color[1]//4, color[2]//4))
    d.text((60, y+20), label, font=font(14, True), fill=color)
    d.text((140, y+16), txt, font=font(15), fill=PAPER if i == 0 else GRAY)

d.rounded_rectangle([40, cy2+300, 180, cy2+340], radius=20, fill=(15, 42, 32))
d.text((60, cy2+310), 'Rollback', font=font(15, True), fill=CYAN)

# Card 4: Quarantine
d.rounded_rectangle([816, cy2, 1576, cy2+456], radius=8, fill=SLATE2, outline=(30, 58, 82))
d.rectangle([816, cy2, 1576, cy2+40], fill=SLATE)
d.text((832, cy2+12), 'Quarantine', font=font(16, True), fill=RED)

quarantined = ['DEMO_TOKEN_not_real_123', 'REDACTED-SECRET', 'sk-1234567890abcdef']
for i, item in enumerate(quarantined):
    y = cy2 + 56 + i * 72
    d.rounded_rectangle([832, y, 1560, y+60], radius=4, fill=(26, 18, 18), outline=(58, 32, 32))
    d.rectangle([844, y+12, 852, y+48], fill=RED)
    d.text((864, y+14), item, font=font(15, True, True), fill=RED)
    d.text((864, y+36), 'auto-quarantined: credential detected', font=font(13), fill=(120, 60, 60))

d.rounded_rectangle([832, cy2+290, 980, cy2+322], radius=16, fill=(26, 18, 18))
d.ellipse([848, cy2+298, 862, cy2+312], fill=RED)
d.text((870, cy2+298), '3 items isolated', font=font(13), fill=RED)

img.save(os.path.join(OUT, 'hero-governance-console.png'))
print('Hero saved')

# ============ EVIDENCE (1600x960) ============
img2 = Image.new('RGB', (1600, 960), INK)
d2 = ImageDraw.Draw(img2)

# Panel 1: Conflict
d2.rounded_rectangle([24, 24, 784, 464], radius=8, fill=SLATE2, outline=(30, 58, 82))
d2.rectangle([24, 24, 784, 72], fill=SLATE)
d2.text((40, 36), 'Conflict', font=font(18, True), fill=AMBER)
d2.rounded_rectangle([48, 96, 760, 168], radius=4, fill=SLATE)
d2.rectangle([60, 108, 68, 156], fill=AMBER)
d2.text((80, 110), 'Agent-1: Use PostgreSQL for prod', font=font(15), fill=PAPER)
d2.text((80, 132), 'fact | confidence 0.92', font=font(13), fill=GRAY)
d2.text((360, 180), 'CONFLICT', font=font(20, True), fill=RED)
d2.rounded_rectangle([48, 220, 760, 292], radius=4, fill=(26, 18, 18), outline=(58, 32, 32))
d2.rectangle([60, 232, 68, 280], fill=RED)
d2.text((80, 234), 'Agent-2: Use MySQL for prod', font=font(15), fill=RED)
d2.text((80, 256), 'fact | confidence 0.88', font=font(13), fill=(120, 60, 60))
d2.rounded_rectangle([48, 320, 200, 360], radius=20, fill=(40, 30, 10))
d2.text((68, 330), 'Resolve', font=font(15, True), fill=AMBER)

# Panel 2: Quarantine
d2.rounded_rectangle([816, 24, 1576, 464], radius=8, fill=SLATE2, outline=(30, 58, 82))
d2.rectangle([816, 24, 1576, 72], fill=SLATE)
d2.text((832, 36), 'Quarantine', font=font(18, True), fill=RED)
for i, item in enumerate(quarantined):
    y = 96 + i * 80
    d2.rounded_rectangle([840, y, 1552, y+64], radius=4, fill=(26, 18, 18), outline=(58, 32, 32))
    d2.rectangle([852, y+12, 860, y+52], fill=RED)
    d2.text((872, y+14), item, font=font(15, True, True), fill=RED)
    d2.text((872, y+38), 'isolated | not in active memory', font=font(13), fill=(120, 60, 60))

# Panel 3: Supersede chain
d2.rounded_rectangle([24, 496, 784, 936], radius=8, fill=SLATE2, outline=(30, 58, 82))
d2.rectangle([24, 496, 784, 544], fill=SLATE)
d2.text((40, 508), 'Supersede Chain', font=font(18, True), fill=CYAN)
d2.rounded_rectangle([48, 568, 760, 640], radius=4, fill=SLATE)
d2.rectangle([60, 580, 68, 628], fill=GRAY)
d2.text((80, 582), 'v1: Use SQLite for everything', font=font(15), fill=GRAY)
d2.text((80, 604), 'superseded', font=font(13), fill=DARK)
d2.text((380, 652), 'v', font=font(20, True), fill=CYAN)
d2.rounded_rectangle([48, 688, 760, 760], radius=4, fill=SLATE)
d2.rectangle([60, 700, 68, 748], fill=CYAN)
d2.text((80, 702), 'v2: Use SQLite locally; Postgres for prod', font=font(15), fill=PAPER)
d2.text((80, 724), 'active', font=font(13), fill=CYAN)
d2.rounded_rectangle([48, 800, 180, 840], radius=20, fill=(15, 42, 32))
d2.text((68, 810), 'Restore v1', font=font(14, True), fill=CYAN)

# Panel 4: Version History
d2.rounded_rectangle([816, 496, 1576, 936], radius=8, fill=SLATE2, outline=(30, 58, 82))
d2.rectangle([816, 496, 1576, 544], fill=SLATE)
d2.text((832, 508), 'Version History', font=font(18, True), fill=CYAN)
d2.line([872, 580, 872, 880], fill=(30, 58, 82), width=2)
for y, label, color, txt in [
    (600, 'v3  current', CYAN, 'Use SQLite locally; Postgres for prod'),
    (700, 'v2  superseded', AMBER, 'Use PostgreSQL for analytics'),
    (800, 'v1  original', GRAY, 'Use SQLite for everything'),
]:
    d2.ellipse([862, y-10, 882, y+10], fill=color)
    d2.text((900, y-10), label, font=font(14, True), fill=color)
    d2.text((900, y+12), txt, font=font(14), fill=GRAY)
d2.rounded_rectangle([840, 860, 960, 900], radius=20, fill=(15, 42, 32))
d2.text((860, 870), 'Rollback', font=font(14, True), fill=CYAN)

img2.save(os.path.join(OUT, 'governance-evidence.png'))
print('Evidence saved')

# ============ DEMO (1440x900) ============
img3 = Image.new('RGB', (1440, 900), INK)
d3 = ImageDraw.Draw(img3)
d3.rectangle([0, 0, 1440, 52], fill=SLATE)
d3.text((500, 16), 'Agent writes  ->  Auto-organize  ->  Rollback', font=font(16, True), fill=CYAN)

# Left: Write panel
d3.rounded_rectangle([20, 72, 480, 572], radius=8, fill=SLATE2, outline=(30, 58, 82))
d3.rectangle([20, 72, 480, 112], fill=SLATE)
d3.text((36, 82), 'Agent Write', font=font(16, True), fill=CYAN)
d3.rounded_rectangle([36, 128, 460, 188], radius=4, fill=SLATE)
d3.rectangle([48, 140, 56, 176], fill=CYAN)
d3.text((68, 142), 'Use PostgreSQL for prod analytics', font=font(14), fill=PAPER)
d3.text((68, 162), 'new write -> triggers organize', font=font(12), fill=GRAY)

# Old memory
d3.rounded_rectangle([36, 204, 460, 260], radius=4, fill=SLATE)
d3.rectangle([48, 216, 56, 248], fill=GRAY)
d3.text((68, 218), 'Use SQLite for everything', font=font(14), fill=GRAY)
d3.text((68, 238), 'old memory -> will be superseded', font=font(12), fill=DARK)

# Arrow
d3.text((228, 268), 'v supersede', font=font(14, True), fill=CYAN)

# New active
d3.rounded_rectangle([36, 296, 460, 352], radius=4, fill=(15, 42, 32))
d3.rectangle([48, 308, 56, 340], fill=CYAN)
d3.text((68, 310), 'Use SQLite locally; Postgres for prod', font=font(14), fill=PAPER)
d3.text((68, 330), 'active v2 | old v1 preserved', font=font(12), fill=CYAN)

# Actions
d3.rounded_rectangle([36, 376, 168, 408], radius=16, fill=(26, 51, 64))
d3.ellipse([48, 384, 60, 396], fill=CYAN)
d3.text((68, 384), 'classified', font=font(12), fill=CYAN)

d3.rounded_rectangle([180, 376, 320, 408], radius=16, fill=(26, 51, 64))
d3.ellipse([192, 384, 204, 396], fill=AMBER)
d3.text((212, 384), 'superseded', font=font(12), fill=AMBER)

d3.rounded_rectangle([332, 376, 440, 408], radius=16, fill=(26, 51, 64))
d3.ellipse([344, 384, 356, 396], fill=RED)
d3.text((364, 384), 'no secret', font=font(12), fill=RED)

# Right: Version history
d3.rounded_rectangle([500, 72, 1420, 572], radius=8, fill=SLATE2, outline=(30, 58, 82))
d3.rectangle([500, 72, 1420, 112], fill=SLATE)
d3.text((516, 82), 'Version History & Rollback', font=font(16, True), fill=CYAN)
d3.line([556, 140, 556, 520], fill=(30, 58, 82), width=2)

for y, label, color, txt, active in [
    (160, 'v2  active', CYAN, 'Use SQLite locally; Postgres for prod', True),
    (280, 'v1  superseded', AMBER, 'Use SQLite for everything', False),
]:
    d3.ellipse([546, y-10, 566, y+10], fill=color)
    d3.rounded_rectangle([580, y-30, 1400, y+30], radius=4, fill=(15, 42, 32) if active else SLATE)
    d3.rectangle([592, y-22, 600, y+22], fill=color)
    d3.text((612, y-18), label, font=font(14, True), fill=color)
    d3.text((612, y+4), txt, font=font(14), fill=PAPER if active else GRAY)

# Rollback arrow
d3.text((556, 360), 'rollback ->', font=font(14, True), fill=CYAN)
d3.rounded_rectangle([580, 420, 700, 460], radius=20, fill=(15, 42, 32))
d3.text((600, 430), 'Restore', font=font(14, True), fill=CYAN)

# Bottom: quarantine bar
d3.rounded_rectangle([20, 600, 1420, 720], radius=8, fill=SLATE2, outline=(30, 58, 82))
d3.rectangle([20, 600, 1420, 636], fill=SLATE)
d3.text((36, 610), 'Quarantine (auto-isolated)', font=font(14, True), fill=RED)
d3.rounded_rectangle([36, 652, 1400, 700], radius=4, fill=(26, 18, 18), outline=(58, 32, 32))
d3.rectangle([48, 664, 56, 688], fill=RED)
d3.text((68, 666), 'DEMO_TOKEN_not_real_123', font=font(14, True, True), fill=RED)
d3.text((380, 666), 'not in active memory', font=font(13), fill=(120, 60, 60))

# Stats
d3.text((720, 780), '22 MCP tools  -  Auto-organize  -  SQLite backend  -  No account  -  No telemetry', font=font(18), fill=GRAY, anchor='ms')
d3.text((720, 830), 'pip install agent-memguard', font=font(22, True, True), fill=CYAN, anchor='ms')

img3.save(os.path.join(OUT, 'write-organize-rollback.png'))
print('Demo saved')

print('All PNGs generated')
