# -*- coding: utf-8 -*-
"""_ocr.py — распознавание текста на сканах и растровых картинках (общий модуль, не точка входа).

Движок — rapidocr (PP-OCRv6, модели лежат внутри pip-пакета, сеть не нужна).
Кириллица: модель cyrillic_PP-OCRv5 ищется в пакете `pdf_rezume_ocr_cyrillic`
или в <state>/models/; без неё русские сканы распознаются латинской моделью
(результат будет плохим, и скрипт об этом предупредит).

Единицы измерения: координаты в пунктах PDF (страница после remove_rotation),
цвета — '#rrggbb'.
"""
from __future__ import annotations

import contextlib
import io
import os
import re
import statistics
import sys
from pathlib import Path

# onnxruntime (движок под rapidocr) по умолчанию собирает телеметрию: пишет базу событий в ~/.cache
# поэтому телеметрия выключается до первого импорта библиотеки. Это единственная переменная
os.environ["ORT_DISABLE_TELEMETRY"] = "1"

DPI = 200
MAX_RENDER_PX = 4500
MAX_ROWS = 1500
MIN_SCORE = 0.55
SIZE_RATIO = 1.12
_ASC_RE = re.compile(r"[A-ZА-ЯЁbdfhklt0-9\[\](){}|/!?$%&@#]")
_DESC_RE = re.compile(r"[gjpqyуДЦЩруф]")


def size_ratio(text: str) -> float:
    asc, desc = bool(_ASC_RE.search(text)), bool(_DESC_RE.search(text))
    if asc and desc:
        return SIZE_RATIO
    if asc or desc:
        return 0.95
    return 0.72


def ink_ratio(text: str) -> float:
    asc, desc = bool(_ASC_RE.search(text)), bool(_DESC_RE.search(text))
    if asc and desc:
        return 0.93
    if asc or desc:
        return 0.73
    return 0.52


def ink_height(rgb, x0: int, y0: int, x1: int, y1: int) -> float | None:
    import numpy as np
    h, w = rgb.shape[:2]
    x0, x1 = max(0, x0), min(w, x1)
    y0, y1 = max(0, y0), min(h, y1)
    if x1 - x0 < 6 or y1 - y0 < 6:
        return None
    box = rgb[y0:y1, x0:x1].astype(int)
    ring = np.concatenate([box[:1].reshape(-1, 3), box[-1:].reshape(-1, 3), box[:, :1].reshape(-1, 3), box[:, -1:].reshape(-1, 3)])
    bg = np.median(ring, axis=0)
    ink = (np.abs(box - bg).sum(axis=2) > 90).mean(axis=1)
    floor = float(np.percentile(ink, 10))
    mask = list(ink > floor + max(0.004, 1.0 / (x1 - x0)))
    mask = [m or (0 < i < len(mask) - 1 and mask[i - 1] and mask[i + 1]) for i, m in enumerate(mask)]
    best, start = (0, 0), None
    for i, m in enumerate(mask + [False]):
        if m and start is None:
            start = i
        elif not m and start is not None:
            if i - start > best[1] - best[0]:
                best = (start, i)
            start = None
    if best[1] - best[0] < 3:
        return None
    return float(best[1] - best[0])
CYRILLIC_FILE = "cyrillic_PP-OCRv5_rec_mobile.onnx"
CYRILLIC_PACKAGE = "pdf_rezume_ocr_cyrillic"

_CYR_RE = re.compile(r"[А-Яа-яЁё]")
_LAT_RE = re.compile(r"[A-Za-z]")


@contextlib.contextmanager
def quiet():
    saved_out = sys.stdout
    sys.stdout = io.StringIO()
    try:
        sys.__stdout__.flush()
    except Exception:
        pass
    dup = None
    try:
        dup = os.dup(1)
        os.dup2(2, 1)
    except Exception:
        dup = None
    try:
        yield
    finally:
        sys.stdout = saved_out
        if dup is not None:
            try:
                os.dup2(dup, 1)
                os.close(dup)
            except Exception:
                pass


def _model_has_dict(path: Path) -> bool:
    try:
        import onnxruntime  # type: ignore
        sess = onnxruntime.InferenceSession(str(path), providers=["CPUExecutionProvider"])
        return "character" in sess.get_modelmeta().custom_metadata_map
    except Exception:
        return False


def cyrillic_model_path(state_dir: Path | None = None) -> Path | None:
    candidates: list[Path] = []
    try:
        import pdf_rezume_ocr_cyrillic  # type: ignore  # отдельный pip-пакет с моделью; необязателен
        candidates.append(Path(pdf_rezume_ocr_cyrillic.model_path()))
    except Exception:
        pass
    if state_dir is not None:
        candidates.append(Path(state_dir) / "models" / CYRILLIC_FILE)
    for p in candidates:
        if p.is_file() and _model_has_dict(p):
            return p
    return None


class Engine:

    def __init__(self, state_dir: Path | None = None):
        import logging
        logging.disable(logging.CRITICAL)
        with quiet():
            import rapidocr
            from rapidocr import RapidOCR  # noqa: WPS433 — тяжёлый импорт только по требованию
            import numpy as np
            self.np = np
            # путь к моделям — строкой: иначе rapidocr кладёт в конфиг PosixPath, а omegaconf < 2.2 его не принимает
            base = {"Global.log_level": "error", "Global.use_cls": False,
                    "Global.model_root_dir": str(Path(rapidocr.__file__).resolve().parent / "models")}
            self.lat = RapidOCR(params=dict(base))
            self.cyr = None
            cyr_path = cyrillic_model_path(state_dir)
            if cyr_path is not None:
                self.cyr = RapidOCR(params={
                    **base,
                    "Rec.model_path": str(cyr_path),
                    "Rec.lang_type": "cyrillic",
                })
        self.has_cyrillic = self.cyr is not None

    def recognize(self, img) -> list[dict]:
        np = self.np
        with quiet():
            out = self.lat(img, return_word_box=True)
        rows: list[dict] = []
        if getattr(out, "boxes", None) is None or getattr(out, "txts", None) is None:
            return rows
        boxes = [np.asarray(b, dtype=float).tolist() for b in out.boxes]
        txts, scores = list(out.txts), [float(s) for s in out.scores]
        if len(boxes) > MAX_ROWS:
            keep = sorted(range(len(boxes)), key=lambda i: -scores[i])[:MAX_ROWS]
            keep.sort()
            boxes = [boxes[i] for i in keep]; txts = [txts[i] for i in keep]; scores = [scores[i] for i in keep]
            out_boxes = [out.boxes[i] for i in keep]
            word_results = [out.word_results[i] for i in keep] if getattr(out, "word_results", None) else ()
        else:
            out_boxes, word_results = out.boxes, (getattr(out, "word_results", None) or ())
        word_boxes: list = []
        try:
            for wr in word_results:
                ws = []
                for item in wr:
                    if len(item) >= 3 and item[2] is not None:
                        q = np.asarray(item[2], dtype=float)
                        ws.append((str(item[0]), [float(q[:, 0].min()), float(q[:, 1].min()), float(q[:, 0].max()), float(q[:, 1].max())]))
                word_boxes.append(ws)
        except Exception:
            word_boxes = []
        crops = self._crops(img, out_boxes)
        weak = [i for i, s in enumerate(scores) if s < 0.85]
        if weak:
            with quiet():
                flipped = self._rec_crops(self.lat, [np.ascontiguousarray(crops[i][::-1, ::-1]) for i in weak])
            for i, (t2, s2) in zip(weak, flipped):
                if t2.strip() and s2 > scores[i] + 0.1:
                    txts[i], scores[i] = t2, s2
        cyr = None
        if self.cyr is not None:
            with quiet():
                cyr = self._rec_crops(self.cyr, crops)
        for i, (quad, text, score) in enumerate(zip(boxes, txts, scores)):
            script = "lat"
            if cyr is not None and i < len(cyr):
                t2, s2 = cyr[i]
                if t2.strip() and (s2 >= score + 0.05 or (_LAT_RE.search(text) is None and s2 >= score - 0.1)):
                    text, score, script = t2, s2, "cyr"
            text = clean_text(text)
            if not text or score < MIN_SCORE or not plausible(text):
                continue
            row = {"quad": [[round(x, 1), round(y, 1)] for x, y in quad], "text": text,
                   "score": round(score, 3), "script": script}
            if script == "lat" and i < len(word_boxes) and word_boxes[i]:
                row["words"] = word_boxes[i]
            rows.append(row)
        return rows

    def _crops(self, img, boxes) -> list:
        np = self.np
        try:
            from rapidocr.utils.process_img import get_rotate_crop_image  # type: ignore
        except Exception:
            get_rotate_crop_image = None
        crops = []
        for b in boxes:
            pts = np.asarray(b, dtype=np.float32)
            if get_rotate_crop_image is not None:
                crops.append(get_rotate_crop_image(img, pts))
            else:
                x0, y0 = pts[:, 0].min(), pts[:, 1].min()
                x1, y1 = pts[:, 0].max(), pts[:, 1].max()
                crops.append(img[int(y0):int(y1) + 1, int(x0):int(x1) + 1])
        return crops

    @staticmethod
    def _rec_crops(engine, crops: list) -> list[tuple[str, float]]:
        if not crops:
            return []
        try:
            rec = engine.recognize_txt(crops)
        except Exception:
            return [("", 0.0)] * len(crops)
        if rec.txts is None:
            return [("", 0.0)] * len(crops)
        return [(str(t), float(s)) for t, s in zip(rec.txts, rec.scores)]


_FOREIGN_RE = re.compile("[\\u0600-\\u06ff\\u0900-\\u0dff\\u0e00-\\u0e7f\\u1100-\\u11ff\\u3000-\\u30ff\\u3400-\\u9fff\\uac00-\\ud7af\\uff00-\\uffef]")


def plausible(text: str) -> bool:
    if _FOREIGN_RE.search(text):
        return False
    tokens = text.split()
    if len(tokens) >= 5 and sum(1 for t in tokens if len(re.sub(r"\W", "", t)) <= 2) > 0.6 * len(tokens):
        return False
    return True


def clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", str(text)).strip()
    text = re.sub(r"^[■□]\s*", "", text)
    if not text:
        return text
    if _CYR_RE.search(text) is None:
        text = re.sub(r"(?<![A-Za-z])Al(?![a-z])", "AI", text)
        text = re.sub(r"\bGenAl\b", "GenAI", text)
    return text


def render(pymupdf, page, dpi: int = DPI):
    import numpy as np
    side = max(page.rect.width, page.rect.height, 1.0)
    dpi = max(36, min(dpi, int(MAX_RENDER_PX * 72 / side)))
    pix = page.get_pixmap(dpi=dpi, alpha=False)
    arr = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.h, pix.w, pix.n)
    if pix.n >= 3:
        rgb = arr[:, :, :3]
    else:
        rgb = np.repeat(arr[:, :, :1], 3, axis=2)
    return rgb[:, :, ::-1].copy(), rgb, dpi / 72.0


def _hex(rgb) -> str:
    return "#%02x%02x%02x" % tuple(int(max(0, min(255, round(v)))) for v in rgb)


def trim_swatch(rgb, x0: int, y0: int, x1: int, y1: int) -> tuple[int, int]:
    import numpy as np
    box = rgb[y0:y1, x0:x1].astype(int)
    if box.shape[0] < 6 or box.shape[1] < 8:
        return x0, x1
    ring = np.concatenate([box[:1].reshape(-1, 3), box[-1:].reshape(-1, 3)])
    bg = np.median(ring, axis=0)
    inner = box[2:-2]
    far = (np.abs(inner - bg).sum(axis=2) > 90)
    frac = far.mean(axis=0)
    w = len(frac)
    gap_max = max(2, int(0.6 * (y1 - y0)))

    def swatch_end(order) -> int | None:
        i, n = 0, len(order)
        while i < n and i < 0.3 * n and frac[order[i]] < 0.15:
            i += 1
        j = i
        while j < n and frac[order[j]] >= 0.45:
            j += 1
        run = [frac[k] for k in order[i:j]]
        if len(run) < max(6, int(0.35 * (y1 - y0))) or (max(run) - min(run)) > 0.12:
            return None
        cols = order[i:j]
        pix = inner[:, cols][far[:, cols]]
        if len(pix) < 6:
            return None
        med = np.median(pix, axis=0)
        mad = float(np.median(np.abs(pix - med), axis=0).mean())
        if mad > 15:
            return None
        k = j
        while k < n and frac[order[k]] < 0.15:
            k += 1
        if k == j or k - j > gap_max:
            return None
        return k

    new_x0, new_x1 = x0, x1
    k = swatch_end(list(range(w)))
    if k is not None:
        new_x0 = x0 + k
    k = swatch_end(list(range(w - 1, -1, -1)))
    if k is not None:
        new_x1 = x0 + (w - k)
    lead = 0
    while lead < min(8, w // 3) and frac[lead] >= 0.9:
        lead += 1
    trail = 0
    while trail < min(8, w // 3) and frac[w - 1 - trail] >= 0.9:
        trail += 1
    new_x0 = max(new_x0, x0 + lead)
    new_x1 = min(new_x1, x1 - trail)
    if new_x1 - new_x0 < 6:
        return x0, x1
    return new_x0, new_x1


def colors(rgb, quad_px) -> tuple[str, str, bool, list | None]:
    import numpy as np
    h, w = rgb.shape[:2]
    xs = [p[0] for p in quad_px]; ys = [p[1] for p in quad_px]
    x0, x1 = int(max(0, min(xs) - 2)), int(min(w, max(xs) + 3))
    y0, y1 = int(max(0, min(ys) - 2)), int(min(h, max(ys) + 3))
    if x1 - x0 < 6 or y1 - y0 < 6:
        return "#ffffff", "#000000", False, None
    box = rgb[y0:y1, x0:x1].astype(int)
    top, bottom = box[:2].mean(axis=0), box[-2:].mean(axis=0)
    sides = np.concatenate([box[:, :2].reshape(-1, 3), box[:, -2:].reshape(-1, 3)])
    ring = np.concatenate([box[:2].reshape(-1, 3), box[-2:].reshape(-1, 3), sides])
    bg = np.median(ring, axis=0)
    inner = box[2:-2, 2:-2].reshape(-1, 3)
    lum = inner @ np.array([0.299, 0.587, 0.114])
    bg_lum = float(bg @ np.array([0.299, 0.587, 0.114]))
    if bg_lum >= 128:
        pick = inner[lum < min(np.percentile(lum, 12), bg_lum - 40)]
        fallback = np.array([0, 0, 0])
    else:
        pick = inner[lum > max(np.percentile(lum, 88), bg_lum + 40)]
        fallback = np.array([255, 255, 255])
    fg = np.median(pick, axis=0) if len(pick) >= 4 else fallback
    agree = np.abs(top - bottom).sum(axis=1) <= 60
    band = np.where(agree[:, None], (top + bottom) / 2, bg[None, :])
    if band.shape[0] >= 5:
        k = np.ones(5) / 5
        band = np.stack([np.convolve(band[:, c], k, mode="same") for c in range(3)], axis=1)
        band[:2], band[-2:] = band[2], band[-3]
    dev_band = float(np.abs(band - bg).sum(axis=1).max())
    dev_sides = float(np.abs(np.median(sides, axis=0) - bg).sum())
    busy = dev_band > 45 or dev_sides > 45
    strip = None
    if busy:
        step = max(1, band.shape[0] // 160)
        strip = [[int(v) for v in band[i]] for i in range(0, band.shape[0], step)]
    return _hex(bg), _hex(fg), busy, strip


def page_rows(engine: Engine, pymupdf, page, regions: list[list[float]] | None = None, dpi: int = DPI) -> list[dict]:
    import math
    bgr, rgb, s = render(pymupdf, page, dpi)
    tasks: list[tuple] = []
    if regions:
        H, W = bgr.shape[:2]
        for r in regions:
            x0, y0 = int(max(0, r[0] * s)), int(max(0, r[1] * s))
            x1, y1 = int(min(W, r[2] * s)), int(min(H, r[3] * s))
            if x1 - x0 < 12 or y1 - y0 < 12:
                continue
            tasks.append((bgr[y0:y1, x0:x1].copy(), x0, y0, [round(v, 2) for v in r]))
    else:
        tasks.append((bgr, 0, 0, None))
    rows: list[dict] = []
    for img, ox, oy, region in tasks:
        for r0 in engine.recognize(img):
            for r in _split_labels(r0):
                quad_px = [[x + ox, y + oy] for x, y in r["quad"]]
                xs_px = [p[0] for p in quad_px]; ys_px = [p[1] for p in quad_px]
                (ax, ay), (bx, by), (cx, cy) = quad_px[0], quad_px[1], quad_px[2]
                l1 = math.hypot(bx - ax, by - ay); l2 = math.hypot(cx - bx, cy - by)
                if l1 >= l2:
                    dx, dy, height_px = bx - ax, by - ay, l2
                else:
                    dx, dy, height_px = cx - bx, cy - by, l1
                ln = math.hypot(dx, dy) or 1.0
                dx, dy = dx / ln, dy / ln
                if dx < 0:
                    dx, dy = -dx, -dy
                angle = math.degrees(math.atan2(dy, dx))
                size_px = height_px / size_ratio(r["text"])
                if abs(angle) < 10:
                    px0, px1 = int(min(xs_px)), int(max(xs_px)) + 1
                    py0, py1 = int(min(ys_px)), int(max(ys_px)) + 1
                    tx0, tx1 = trim_swatch(rgb, px0, py0, px1, py1)
                    quad_px = [[tx0, py0], [tx1, py0], [tx1, py1], [tx0, py1]]
                    ink = ink_height(rgb, tx0, py0, tx1, py1)
                    if ink is not None and 0.35 * height_px <= ink <= 1.1 * height_px:
                        by_ink = ink / ink_ratio(r["text"])
                        if by_ink <= 1.15 * size_px:
                            size_px = by_ink
                bg, fg, busy, strip = colors(rgb, quad_px)
                quad = [[round(x / s, 2), round(y / s, 2)] for x, y in quad_px]
                xs = [p[0] for p in quad]; ys = [p[1] for p in quad]
                row = {
                    "quad": quad, "bbox": [round(min(xs), 2), round(min(ys), 2), round(max(xs), 2), round(max(ys), 2)],
                    "text": r["text"], "score": r["score"], "script": r["script"],
                    "size": round(max(3.0, size_px / s), 2), "angle": round(angle, 1),
                    "bg": bg, "fg": fg, "busy": busy, "region": region,
                }
                if strip and abs(angle) < 10:
                    row["strip"] = strip
                rows.append(row)
    return rows


def _split_labels(row: dict) -> list[dict]:
    words = row.get("words")
    text = row["text"]
    if not words or len(words) < 2 or len(words) > 4 or len(text.split()) != len(words):
        return [row]
    xs = [p[0] for p in row["quad"]]; ys = [p[1] for p in row["quad"]]
    height = max(ys) - min(ys)
    parts: list[list[tuple]] = [[words[0]]]
    for prev, cur in zip(words, words[1:]):
        gap = cur[1][0] - prev[1][2]
        wide = gap >= 0.45 * height
        capital = cur[0][:1].isupper()
        broken = prev[0][-1:] in ",&/-" or prev[0].lower() in ("and", "or", "of", "the", "for", "to", "in", "by")
        if wide and capital and not broken:
            parts.append([cur])
        else:
            parts[-1].append(cur)
    if len(parts) == 1:
        return [row]
    out = []
    for part in parts:
        x0 = min(w[1][0] for w in part); x1 = max(w[1][2] for w in part)
        pad = 0.08 * height
        x0, x1 = max(min(xs), x0 - pad), min(max(xs), x1 + pad)
        out.append(dict(row, text=" ".join(w[0] for w in part),
                        quad=[[x0, min(ys)], [x1, min(ys)], [x1, max(ys)], [x0, max(ys)]], words=part))
    return out


def merge_fragments(rows: list[dict]) -> list[dict]:
    flat = [r for r in rows if abs(r["angle"]) < 10]
    rot = [r for r in rows if abs(r["angle"]) >= 10]
    out: list[dict] = []
    for band in _bands(flat):
        band.sort(key=lambda r: r["bbox"][0])
        cur = dict(band[0])
        for nxt in band[1:]:
            merged = _merge_pair(cur, nxt)
            if merged is None:
                out.append(cur)
                cur = dict(nxt)
            else:
                cur = merged
        out.append(cur)
    return out + rot


def _bands(rows: list[dict]) -> list[list[dict]]:
    rows = sorted(rows, key=lambda r: (r["bbox"][1], r["bbox"][0]))
    bands: list[list[dict]] = []
    for r in rows:
        placed = False
        for band in bands[-6:]:
            y0 = min(b["bbox"][1] for b in band); y1 = max(b["bbox"][3] for b in band)
            ov = min(y1, r["bbox"][3]) - max(y0, r["bbox"][1])
            if ov >= 0.7 * min(y1 - y0, r["bbox"][3] - r["bbox"][1]):
                band.append(r)
                placed = True
                break
        if not placed:
            bands.append([r])
    return bands


def _merge_pair(left: dict, right: dict) -> dict | None:
    a, b = left, right
    big = max(a["size"], b["size"]) >= 18
    if abs(a["size"] - b["size"]) > (0.3 if big else 0.15) * max(a["size"], b["size"]):
        return None
    if a.get("region") != b.get("region"):
        return None
    gap = b["bbox"][0] - a["bbox"][2]
    wmin = min(a["bbox"][2] - a["bbox"][0], b["bbox"][2] - b["bbox"][0])
    if gap < -0.5 * wmin:
        return dict(a) if a["score"] >= b["score"] else dict(b)
    if not big or gap > 0.6 * max(a["size"], b["size"]):
        return None
    rtext = b["text"]
    if gap < 0:
        for k in (3, 2, 1):
            if len(a["text"]) > k and rtext.lower().startswith(a["text"][-k:].lower()):
                rtext = rtext[k:].lstrip()
                break
    merged = dict(a)
    merged["text"] = (a["text"] + " " + rtext).strip()
    x0, y0 = min(a["bbox"][0], b["bbox"][0]), min(a["bbox"][1], b["bbox"][1])
    x1, y1 = max(a["bbox"][2], b["bbox"][2]), max(a["bbox"][3], b["bbox"][3])
    merged["bbox"] = [x0, y0, x1, y1]
    merged["quad"] = [[x0, y0], [x1, y0], [x1, y1], [x0, y1]]
    merged["score"] = min(a["score"], b["score"])
    merged["busy"] = bool(a.get("busy") or b.get("busy"))
    if a.get("strip") and b.get("strip"):
        merged["strip"] = a["strip"] + b["strip"]
    else:
        merged.pop("strip", None)
    return merged


def reading_order(rows: list[dict], page_width: float) -> list[dict]:
    flat = [r for r in rows if abs(r["angle"]) < 10]
    rot = [r for r in rows if abs(r["angle"]) >= 10]
    if not flat:
        return rows
    cols = _columns(flat, page_width)
    ordered: list[dict] = []
    for col in cols:
        ordered.extend(_by_rows(col))
    return ordered + rot


def _by_rows(rows: list[dict]) -> list[dict]:
    rows = sorted(rows, key=lambda r: (r["bbox"][1], r["bbox"][0]))
    out: list[dict] = []
    row: list[dict] = []
    y0 = y1 = 0.0
    for r in rows:
        h = r["bbox"][3] - r["bbox"][1]
        if row and min(y1, r["bbox"][3]) - max(y0, r["bbox"][1]) > 0.5 * min(h, y1 - y0):
            row.append(r)
            y0, y1 = min(y0, r["bbox"][1]), max(y1, r["bbox"][3])
        else:
            out.extend(sorted(row, key=lambda q: q["bbox"][0]))
            row, y0, y1 = [r], r["bbox"][1], r["bbox"][3]
    out.extend(sorted(row, key=lambda q: q["bbox"][0]))
    return out


def _columns(rows: list[dict], page_width: float) -> list[list[dict]]:
    if len(rows) < 6 or page_width <= 0:
        return [rows]
    mids = sorted((r["bbox"][0] + r["bbox"][2]) / 2 for r in rows)
    best = None
    for a, b in zip(mids, mids[1:]):
        gap = b - a
        if gap > 0.04 * page_width and 0.25 * page_width < (a + b) / 2 < 0.75 * page_width:
            cut = (a + b) / 2
            crossing = [r for r in rows if r["bbox"][0] < cut - 2 and r["bbox"][2] > cut + 2]
            left = [r for r in rows if (r["bbox"][0] + r["bbox"][2]) / 2 < cut]
            if len(crossing) <= max(2, len(rows) // 12) and 0.2 * len(rows) <= len(left) <= 0.8 * len(rows):
                if best is None or gap > best[0]:
                    best = (gap, cut)
    if best is None:
        return [rows]
    cut = best[1]
    wide = [r for r in rows if r["bbox"][0] < cut - 2 and r["bbox"][2] > cut + 2]
    left = [r for r in rows if r not in wide and (r["bbox"][0] + r["bbox"][2]) / 2 < cut]
    right = [r for r in rows if r not in wide and r not in left]
    wide.sort(key=lambda r: r["bbox"][1])
    return [wide, left, right]


def rows_text(rows: list[dict]) -> str:
    out: list[str] = []
    prev = None
    for r in rows:
        if prev is not None:
            gap = r["bbox"][1] - prev["bbox"][3]
            if gap > 0.9 * max(prev["size"], r["size"]) or abs(r["angle"]) >= 10 or r["region"] != prev["region"]:
                out.append("")
        out.append(r["text"])
        prev = r
    return "\n".join(out).strip() + "\n"


def script_share(rows: list[dict]) -> tuple[int, int]:
    text = " ".join(r["text"] for r in rows)
    return len(_CYR_RE.findall(text)), len(_LAT_RE.findall(text))


def median_size(rows: list[dict]) -> float:
    return statistics.median([r["size"] for r in rows]) if rows else 10.0
