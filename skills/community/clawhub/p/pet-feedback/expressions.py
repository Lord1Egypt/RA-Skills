#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
expressions.py — 桌宠表情绘制模块（pet-feedback Skill）

用 pygame 基础图形（圆、弧、线、多边形）程序化绘制桌宠表情，
无需任何图片素材，适配 7 寸触摸屏/任意分辨率。

情绪（与 pet-camera-vision 的情绪集合一一对应）：
  happy, sad, angry, surprised, fearful, disgusted, neutral, worried, sleepy, excited

状态 phase（显示在表情旁的小徽标）：
  idle, listening, thinking, talking, sleeping

用法：
  from expressions import draw_pet, render
  render(surface, emotion="happy", phase="talking", message="你好呀", font_path=None)
"""

import math

import pygame

# 情绪 → 脸部参数
FACE = {
    "happy":    dict(face=(255, 224, 130), eye="arc_up",  mouth="smile", blush=True),
    "excited":  dict(face=(255, 214, 100), eye="wide",    mouth="smile", blush=True, star=True),
    "sad":      dict(face=(215, 225, 235), eye="droopy",  mouth="frown"),
    "worried":  dict(face=(225, 220, 210), eye="droopy",  mouth="wavy", brow="raise"),
    "angry":    dict(face=(245, 210, 190), eye="slant",   mouth="frown", brow="slant"),
    "surprised":dict(face=(255, 236, 200), eye="wide",    mouth="o"),
    "fearful":  dict(face=(235, 225, 220), eye="wide",    mouth="wavy", brow="raise"),
    "disgusted":dict(face=(230, 230, 215), eye="squint",  mouth="wavy"),
    "neutral":  dict(face=(240, 226, 205), eye="round",   mouth="flat"),
    "sleepy":   dict(face=(228, 233, 238), eye="line",    mouth="flat"),
}

# 状态 → 徽标颜色（RGB）
PHASE_COLOR = {
    "idle": (150, 150, 150),
    "listening": (80, 200, 120),
    "thinking": (240, 190, 80),
    "talking": (90, 160, 240),
    "sleeping": (140, 140, 190),
}


def _search_cjk_font():
    """查找常见中文字体路径（树莓派/桌面 Linux/Windows）。"""
    candidates = [
        "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
        "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf",
        "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/simhei.ttf",
        "/System/Library/Fonts/PingFang.ttc",
    ]
    import os
    for p in candidates:
        if os.path.exists(p):
            return p
    return None


def get_font(size, font_path=None):
    path = font_path or _search_cjk_font()
    if path:
        try:
            return pygame.font.Font(path, size)
        except Exception:
            pass
    return pygame.font.Font(None, size)


def _draw_eye(surf, cx, cy, r, style, color=(40, 40, 45)):
    """按样式绘制一只眼睛。r 为眼框半径。"""
    if style == "arc_up":            # 开心：∩ 型（眯眼笑）
        pygame.draw.arc(surf, color, [cx - r, cy - r, 2 * r, 2 * r], math.pi, 2 * math.pi, max(2, r // 3))
    elif style == "droopy":          # 难过/担忧：∪ 型下弯
        pygame.draw.arc(surf, color, [cx - r, cy - r, 2 * r, 2 * r], 0, math.pi, max(2, r // 3))
    elif style == "slant":           # 生气：内斜线
        pygame.draw.line(surf, color, (cx - r, cy - r), (cx + r, cy + r // 2), max(2, r // 3))
    elif style == "line":            # 睡觉：横线
        pygame.draw.line(surf, color, (cx - r, cy), (cx + r, cy), max(2, r // 3))
    elif style == "squint":          # 嫌弃：眯眼（短横线 + 下弧）
        pygame.draw.line(surf, color, (cx - r, cy), (cx + r, cy), max(2, r // 3))
        pygame.draw.arc(surf, color, [cx - r, cy - r // 2, 2 * r, r], 0, math.pi, max(2, r // 4))
    elif style == "wide":            # 惊讶/兴奋：大圆 + 小瞳孔
        pygame.draw.circle(surf, color, (cx, cy), int(r * 1.2))
        pygame.draw.circle(surf, (255, 255, 255), (cx, cy), int(r * 0.5))
    else:                            # round：普通圆眼
        pygame.draw.circle(surf, color, (cx, cy), r)


def _draw_mouth(surf, cx, cy, r, style, color=(60, 40, 40)):
    """按样式绘制嘴。r 为嘴框半径。"""
    if style == "smile":
        pygame.draw.arc(surf, color, [cx - r, cy - r, 2 * r, 2 * r], 0, math.pi, max(2, r // 3))
    elif style == "frown":
        pygame.draw.arc(surf, color, [cx - r, cy - r, 2 * r, 2 * r], math.pi, 2 * math.pi, max(2, r // 3))
    elif style == "o":
        pygame.draw.circle(surf, color, (cx, cy), int(r * 0.55))
        pygame.draw.circle(surf, (255, 240, 220), (cx, cy), int(r * 0.3))
    elif style == "wavy":
        pts = []
        n = 5
        for i in range(n + 1):
            x = cx - r + 2 * r * i / n
            y = cy + (r // 2) * (1 if i % 2 == 0 else -1)
            pts.append((x, y))
        pygame.draw.lines(surf, color, False, pts, max(2, r // 4))
    else:  # flat
        pygame.draw.line(surf, color, (cx - r, cy), (cx + r, cy), max(2, r // 3))


def _draw_brow(surf, cx, cy, r, style, color=(60, 40, 40)):
    if style == "slant":  # 生气眉：内斜
        pygame.draw.line(surf, color, (cx - r, cy - r), (cx + r, cy + r // 2), max(2, r // 4))
    elif style == "raise":  # 担忧眉：上弯
        pygame.draw.arc(surf, color, [cx - r, cy - r, 2 * r, 2 * r], math.pi, 2 * math.pi, max(2, r // 4))


def _draw_bubble(surf, x, y, w, h, color):
    pygame.draw.rect(surf, color, (x, y, w, h), border_radius=h // 3)
    # 小尾巴
    pygame.draw.polygon(surf, color, [(x + w // 2 - 8, y + h), (x + w // 2 + 8, y + h), (x + w // 2, y + h + 10)])


def _draw_phase(surf, w, h, phase):
    """在画面上方绘制状态徽标（气泡 + 圆点，无需字体）。"""
    color = PHASE_COLOR.get(phase, (150, 150, 150))
    bx, by, bw, bh = w - 110, 16, 94, 40
    _draw_bubble(surf, bx, by, bw, bh, color)
    n = {"listening": 3, "thinking": 3, "talking": 3, "idle": 1, "sleeping": 2}.get(phase, 1)
    dot_r = 5
    for i in range(n):
        pygame.draw.circle(surf, (255, 255, 255), (bx + 18 + i * 24, by + bh // 2), dot_r)
    if phase == "sleeping":
        # Z 字母（三条线段）
        zx, zy = bx + 70, by + bh // 2 - 8
        pygame.draw.lines(surf, (255, 255, 255), False, [(zx - 8, zy), (zx + 8, zy), (zx - 8, zy + 10), (zx + 8, zy + 10)], 3)


def draw_pet(surface, cx, cy, r, emotion="happy", phase="talking"):
    """在 (cx, cy) 处画一个半径为 r 的桌宠脸。"""
    params = FACE.get(emotion, FACE["neutral"])
    face_color = params["face"]

    # 脸
    pygame.draw.circle(surface, face_color, (cx, cy), r)
    pygame.draw.circle(surface, (120, 90, 60), (cx, cy), r, width=max(2, r // 20))

    # 腮红
    if params.get("blush"):
        pygame.draw.circle(surface, (255, 150, 150), (cx - int(r * 0.62), cy + int(r * 0.35)), int(r * 0.16))
        pygame.draw.circle(surface, (255, 150, 150), (cx + int(r * 0.62), cy + int(r * 0.35)), int(r * 0.16))

    # 眼睛
    eye_r = int(r * 0.16)
    eye_y = cy - int(r * 0.18)
    eye_dx = int(r * 0.45)
    _draw_eye(surface, cx - eye_dx, eye_y, eye_r, params["eye"])
    _draw_eye(surface, cx + eye_dx, eye_y, eye_r, params["eye"])

    # 眉毛
    brow = params.get("brow")
    if brow:
        _draw_brow(surface, cx - eye_dx, eye_y - eye_r, eye_r, brow)
        _draw_brow(surface, cx + eye_dx, eye_y - eye_r, eye_r, brow)

    # 嘴
    _draw_mouth(surface, cx, cy + int(r * 0.28), int(r * 0.34), params["mouth"])

    # 兴奋星星眼点缀
    if params.get("star"):
        for (sx, sy) in [(cx - eye_dx, eye_y), (cx + eye_dx, eye_y)]:
            pts = []
            for i in range(10):
                ang = -math.pi / 2 + i * math.pi / 5
                rad = eye_r * 1.5 if i % 2 == 0 else eye_r * 0.6
                pts.append((sx + rad * math.cos(ang), sy + rad * math.sin(ang)))
            pygame.draw.polygon(surface, (255, 210, 60), pts)


def render(surface, emotion="happy", phase="talking", message=None, font_path=None):
    """在整张 surface 上渲染桌宠（脸 + 状态徽标 + 底部状态栏/消息）。"""
    w, h = surface.get_size()
    surface.fill((24, 28, 38))  # 深色背景

    r = int(min(w, h) * 0.22)
    cx, cy = w // 2, h // 2
    draw_pet(surface, cx, cy, r, emotion=emotion, phase=phase)
    _draw_phase(surface, w, h, phase)

    # 底部状态栏：情绪 + 状态（英文，保证任何字体可显示）
    bar = pygame.Rect(0, h - 44, w, 44)
    pygame.draw.rect(surface, (34, 40, 54), bar)
    font = get_font(22, font_path)
    status = "%s  ·  %s" % (emotion, phase)
    text = font.render(status, True, (220, 228, 240))
    surface.blit(text, (16, h - 44 + (44 - text.get_height()) // 2))

    # 消息文字（可选，需要中文字体；找不到字体时静默跳过）
    if message:
        mfont = get_font(24, font_path)
        mtext = mfont.render(message, True, (255, 255, 255))
        mrect = mtext.get_rect(center=(w // 2, h - 44 - 34))
        surface.blit(mtext, mrect)
