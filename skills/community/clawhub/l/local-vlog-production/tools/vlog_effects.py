"""Portable Pillow/numpy effects. Coordinates and timing come from the timeline.

Photo 01: diagonal placement, paper edge and soft shadow; the background is
never blurred. Title B: layered sticker, brief rebound, then a stable hold.
Title page C is a supplied image, not an AI brush-image generator.
"""
from __future__ import annotations

import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageColor, ImageDraw, ImageFilter, ImageFont, ImageOps


def smooth(value: float) -> float:
    value = max(0.0, min(1.0, value))
    return value * value * (3.0 - 2.0 * value)


def load_image(path: Path) -> Image.Image:
    with Image.open(path) as source:
        metadata = repr(source.info).lower()
        if source.mode.startswith(("I", "F")) or any(tag in metadata for tag in ("hdrgm", "hdrgainmap", "hdr-gain-map", "gainmap", "smpte2084", "arib-std-b67")):
            raise ValueError(f"HDR/high-bit-depth image requires reviewed SDR preprocessing: {path.name}")
        return ImageOps.exif_transpose(source).convert("RGB")


def fit_image(image: Image.Image, size: tuple[int, int], fit="cover",
              center=(0.5, 0.5), background="#17221f") -> Image.Image:
    if fit == "cover":
        return ImageOps.fit(image, size, Image.Resampling.LANCZOS,
                            centering=tuple(center))
    result = Image.new("RGB", size, background)
    foreground = ImageOps.contain(image, size, Image.Resampling.LANCZOS)
    result.paste(foreground, ((size[0] - foreground.width) // 2,
                             (size[1] - foreground.height) // 2))
    return result


def _text_sprite(spec: dict, width: int, resolve) -> Image.Image:
    scale = width / 1080.0
    title = spec["type"] == "sticker_title"
    size = int(spec.get("font_size", max(12, round((86 if title else 47) * scale))))
    font = ImageFont.truetype(str(resolve(spec["font"])), size)
    text = spec["text"]
    stroke = max(1, round((16 if title else 3) * scale))
    depth = max(1, round(13 * scale)) if title else 0
    pad = stroke + depth + 5
    spacing = max(2, round(size * 0.16))
    probe = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    box = probe.multiline_textbbox((0, 0), text, font=font, spacing=spacing,
                                   align="center", stroke_width=stroke)
    sprite = Image.new("RGBA", (box[2] - box[0] + 2 * pad,
                                box[3] - box[1] + 2 * pad))
    draw = ImageDraw.Draw(sprite)
    position = (pad - box[0], pad - box[1])
    args = dict(font=font, spacing=spacing, align="center")
    fill = spec.get("color", "#214C41" if title else "#FFFFFF")
    outline = spec.get("outline", "#FFF7E5" if title else "#16231F")
    if title:
        shadow = spec.get("shadow", "#AF765C")
        for offset in range(depth, 0, -max(1, round(2 * scale))):
            draw.multiline_text((position[0] + offset, position[1] + offset), text,
                                fill=shadow, stroke_width=stroke,
                                stroke_fill=shadow, **args)
        draw.multiline_text(position, text, fill=fill, stroke_width=stroke,
                            stroke_fill="#14251F", **args)
        draw.multiline_text(position, text, fill=fill,
                            stroke_width=max(1, round(stroke * 0.81)),
                            stroke_fill=outline, **args)
        draw.multiline_text(position, text, fill=fill,
                            stroke_width=max(1, round(2 * scale)),
                            stroke_fill="#14251F", **args)
    else:
        draw.multiline_text(position, text, fill=fill, stroke_width=stroke,
                            stroke_fill=outline, **args)
    max_width = round(width * spec.get("max_width", 0.90))
    if sprite.width > max_width:
        ratio = max_width / sprite.width
        sprite = sprite.resize((max_width, max(1, round(sprite.height * ratio))),
                               Image.Resampling.LANCZOS)
    return sprite


def prepare_overlay(spec: dict, width: int, height: int, resolve) -> dict:
    prepared = dict(spec, width=width, height=height)
    if spec["type"] in {"sticker_title", "subtitle"}:
        prepared["sprite"] = _text_sprite(spec, width, resolve)
        return prepared
    photo = load_image(resolve(spec["source"]))
    border = max(2, round(18 * width / 1080))
    bottom = max(4, round(42 * width / 1080))
    full = spec["type"] == "full_photo"
    if full:
        photo = fit_image(photo, (width, height), "cover",
                          spec.get("crop_center", [0.5, 0.5]))
        prepared["full_image"] = photo
    else:
        limits = spec.get("max_size", [0.82, 0.53])
        photo = ImageOps.contain(photo, (max(1, round(width * limits[0]) - 2 * border),
                                         max(1, round(height * limits[1]) - border - bottom)),
                                 Image.Resampling.LANCZOS)
    card = Image.new("RGBA", (photo.width + 2 * border, photo.height + border + bottom),
                     spec.get("paper_color", "#F6F4EE"))
    card.paste(photo, (border, border))
    ImageDraw.Draw(card).rectangle((0, 0, card.width - 1, card.height - 1),
                                   outline="#DAD7CF", width=max(1, round(width / 1080)))
    prepared.update(card=card, border=border, bottom=bottom)
    return prepared


def _quad(effect: dict, age: float):
    width, height = effect["width"], effect["height"]
    full = effect["type"] == "full_photo"
    entry = effect.get("entry", 0.65)
    u = max(0.0, min(1.0, age / entry))
    ease = 1.0 - (1.0 - u) ** 3
    center = effect.get("center", [0.5, 0.49])
    cx = width * (center[0] + 0.50 * (1.0 - ease))
    cy = height * (center[1] - 0.21 * (1.0 - ease))
    scale = (0.78 if full else 1.0) * (1.04 - 0.04 * ease)
    pitch, yaw, roll = np.radians([-15 * (1 - ease), 7 * (1 - ease),
                                   7.5 * (1 - ease) + effect.get("angle", -1.2) * ease])
    rx = np.array([[1, 0, 0], [0, math.cos(pitch), -math.sin(pitch)],
                   [0, math.sin(pitch), math.cos(pitch)]])
    ry = np.array([[math.cos(yaw), 0, math.sin(yaw)], [0, 1, 0],
                   [-math.sin(yaw), 0, math.cos(yaw)]])
    rz = np.array([[math.cos(roll), -math.sin(roll), 0],
                   [math.sin(roll), math.cos(roll), 0], [0, 0, 1]])
    cw, ch = effect["card"].size
    points = np.array([[-cw / 2, -ch / 2, 0], [cw / 2, -ch / 2, 0],
                       [cw / 2, ch / 2, 0], [-cw / 2, ch / 2, 0]])
    points = points @ (rz @ ry @ rx).T * scale
    distance = 1600 * width / 1080
    perspective = distance / (distance + points[:, 2])
    quad = np.column_stack((cx + points[:, 0] * perspective,
                            cy + points[:, 1] * perspective))
    fill = smooth((age - entry) / effect.get("expand", 0.28)) if full else 0.0
    if fill:
        b, bottom = effect["border"], effect["bottom"]
        target = np.array([[-b, -b], [width + b, -b],
                           [width + b, height + bottom], [-b, height + bottom]])
        quad = quad * (1 - fill) + target * fill
    alpha = smooth(u / 0.16)
    fade = effect.get("fade_out", 0.0 if full else 0.15)
    if fade:
        alpha *= smooth((effect["duration"] - age) / fade)
    return quad, alpha, u, fill


def _warp(card: Image.Image, quad: np.ndarray, size) -> Image.Image:
    # Pillow expects the inverse mapping: output quadrilateral -> source rectangle.
    source = [(0, 0), (card.width, 0), (card.width, card.height), (0, card.height)]
    rows, values = [], []
    for (x, y), (sx, sy) in zip(quad, source):
        rows.extend([[x, y, 1, 0, 0, 0, -sx * x, -sx * y],
                     [0, 0, 0, x, y, 1, -sy * x, -sy * y]])
        values.extend([sx, sy])
    coefficients = np.linalg.solve(np.array(rows), np.array(values))
    return card.transform(size, Image.Transform.PERSPECTIVE, coefficients,
                           Image.Resampling.BICUBIC)


def _photo_once(background: Image.Image, effect: dict, age: float) -> Image.Image:
    if effect["type"] == "full_photo" and age >= effect.get("entry", 0.65) + effect.get("expand", 0.28):
        return effect["full_image"].copy()
    quad, alpha, u, fill = _quad(effect, age)
    if alpha <= 0:
        return background
    width, height = background.size
    mask_size = (max(1, width // 4), max(1, height // 4))
    mask = Image.new("L", mask_size)
    offset = np.array([11 + 7 * (1 - u), 17 + 20 * (1 - u)]) * width / 1080
    polygon = (quad + offset) * np.array([mask_size[0] / width, mask_size[1] / height])
    ImageDraw.Draw(mask).polygon([tuple(point) for point in polygon],
                                 fill=round(90 * alpha * (1 - fill)))
    mask = mask.filter(ImageFilter.GaussianBlur((21 + 16 * (1 - u)) * width / 1080 / 4))
    mask = mask.resize((width, height), Image.Resampling.BILINEAR)
    result = background.copy()
    result.paste((0, 0, 0), (0, 0, width, height), mask)
    top = _warp(effect["card"], quad, background.size)
    if alpha < 0.999:
        top.putalpha(top.getchannel("A").point(lambda value: round(value * alpha)))
    result.paste(top, (0, 0), top)
    return result


def composite(background: Image.Image, effect: dict, timestamp: float) -> Image.Image:
    age = timestamp - effect["start"]
    if age < 0 or age >= effect["duration"]:
        return background
    if effect["type"] in {"photo_card", "full_photo"}:
        entry_end = effect.get("entry", 0.65)
        moving = age < entry_end + (effect.get("expand", 0.28) if effect["type"] == "full_photo" else 0)
        if moving and effect.get("motion_samples", 3) == 3:
            q1 = _quad(effect, max(0, age - 1 / 120))[0]
            q2 = _quad(effect, age + 1 / 120)[0]
            speed = float(np.max(np.linalg.norm(q2 - q1, axis=1))) * 60
            half = min(1 / 120, (2.5 * background.width / 1080) / max(speed, 1))
            samples = [_photo_once(background, effect, max(0, age + delta))
                       for delta in (-half, 0, half)]
            return Image.blend(Image.blend(samples[0], samples[1], 0.5), samples[2], 1 / 3)
        return _photo_once(background, effect, age)
    sprite = effect["sprite"]
    width, height = background.size
    center = effect.get("center", [0.5, 0.22 if effect["type"] == "sticker_title" else 0.88])
    cx, cy = center[0] * width, center[1] * height
    if effect["type"] == "sticker_title":
        phase = smooth(age / 0.36)
        direction = effect.get("direction", -1)
        cx += direction * 72 * width / 1080 * (1 - phase)
        cy -= 26 * height / 1920 * (1 - phase)
        scale = 1 + 0.075 * math.sin(min(age / 0.46, 1) * math.pi) * math.exp(-age * 2)
        angle = effect.get("angle", -2) + direction * 8 * (1 - phase)
        angle += 1.1 * math.sin(age * 25) * math.exp(-age * 7) if age < 0.9 else 0
        if age >= 0.9:
            scale, angle = 1, effect.get("angle", -2)
        sprite = sprite.resize((max(1, round(sprite.width * scale)),
                                max(1, round(sprite.height * scale))), Image.Resampling.LANCZOS)
        sprite = sprite.rotate(angle, Image.Resampling.BICUBIC, expand=True)
        opacity = smooth(age / 0.075)
        if opacity < 0.999:
            sprite.putalpha(sprite.getchannel("A").point(lambda value: round(value * opacity)))
    result = background.copy()
    result.paste(sprite, (round(cx - sprite.width / 2), round(cy - sprite.height / 2)), sprite)
    return result
