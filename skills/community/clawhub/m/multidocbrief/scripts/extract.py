#!/usr/bin/env python3
"""
Нормализация разнородных входных документов в единый корпус для анализа.

Вход:  любые файлы и/или папки (рекурсивно): txt, md, csv, tsv, json, docx, pdf, pptx,
       xlsx, png, jpg, jpeg, webp, bmp, gif, tif, tiff; legacy doc/ppt/xls/rtf/odt —
       через LibreOffice, если он установлен.
Выход (в --out):
  manifest.json   — реестр документов: ID (D1, D2…), тип, объём, оценка токенов,
                    список изображений с причиной, предупреждения
  corpus.md       — весь текст, размеченный якорями [D1 · стр. 3] для ссылок
  texts/D1.md     — текст каждого документа отдельно (для поочерёдного чтения)
  images/*.jpg    — изображения, которые нужно посмотреть глазами: картинки-входы,
                    сканы и «визуальные» страницы PDF, слайды с графиками,
                    встроенные в docx рисунки. Уменьшены до --max-side
                    (большие картинки не помещаются в контекст локальной LLM).

Детерминизм: порядок документов = порядок аргументов, внутри папок — сортировка по имени.
Одинаковые по содержимому файлы (sha1) берутся один раз.

Пример:
  python extract.py /mnt/user-data/uploads --out work --max-side 1568
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

try:  # пакет docbrief
    from . import ooxml
    from . import pdf as pdfmod
except ImportError:  # скрипт рядом с ooxml.py и pdf.py (скилл)
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import ooxml
    import pdf as pdfmod

TEXT_EXT = {".txt", ".md", ".csv", ".tsv", ".json", ".log"}
IMAGE_EXT = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".gif", ".tif", ".tiff"}
LEGACY = {".doc": "docx", ".rtf": "docx", ".odt": "docx", ".ppt": "pptx", ".odp": "pptx",
          ".xls": "xlsx", ".ods": "xlsx"}
SUPPORTED = TEXT_EXT | IMAGE_EXT | {".docx", ".pdf", ".pptx", ".xlsx", ".xlsm"} | set(LEGACY)

TYPE_LABEL = {"text": "TXT", "docx": "DOCX", "pdf": "PDF", "pptx": "PPTX", "xlsx": "XLSX", "image": "IMG"}
CHARS_PER_TOKEN = 3.0  # грубая оценка для смешанного русского/английского текста


# ----------------------------------------------------------------------------- utils
def sha1(path: Path) -> str:
    h = hashlib.sha1()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def read_text_file(path: Path) -> str:
    """Кодировка: BOM (UTF-8/UTF-16/UTF-32) → строгий UTF-8 → charset_normalizer → cp1251/koi8-r/cp866."""
    raw = path.read_bytes()
    for bom, enc in ((b"\xef\xbb\xbf", "utf-8-sig"), (b"\xff\xfe\x00\x00", "utf-32"), (b"\x00\x00\xfe\xff", "utf-32"),
                     (b"\xff\xfe", "utf-16"), (b"\xfe\xff", "utf-16")):
        if raw.startswith(bom):
            return raw.decode(enc, errors="replace")
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        pass
    if raw[:200].count(b"\x00") > 20:  # UTF-16 без BOM
        even = raw[0::2].count(0)
        return raw.decode("utf-16-be" if even > len(raw) // 4 else "utf-16-le", errors="replace")
    # кириллица: во всех трёх кодировках старшие байты — русские буквы, поэтому сравниваем,
    # где чаще встречаются самые частые строчные буквы русского языка
    frequent = set("оеаинтсрвлкмдпу")

    def score(t: str) -> int:
        return sum(1 for ch in t if ch in frequent)

    cands = {enc: raw.decode(enc, errors="replace") for enc in ("cp1251", "koi8-r", "cp866")}
    best_enc = max(cands, key=lambda k: score(cands[k]))
    letters = sum(1 for ch in cands[best_enc] if ch.isalpha())
    if letters and score(cands[best_enc]) > 0.25 * letters:
        return cands[best_enc]
    try:
        from charset_normalizer import from_bytes
        best = from_bytes(raw).best()
        if best is not None:
            return str(best)
    except Exception:  # noqa: BLE001
        pass
    return cands["cp1251"]


def clean(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n").replace("\xa0", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def soffice() -> str | None:
    """LibreOffice: переменная SOFFICE_PATH → PATH → типовые пути Windows/macOS."""
    import os
    if os.environ.get("DOCBRIEF_NO_SOFFICE"):  # принудительно без LibreOffice (тесты, медленный сервер)
        return None
    env = os.environ.get("SOFFICE_PATH")
    if env and Path(env).exists():
        return env
    found = shutil.which("soffice") or shutil.which("libreoffice")
    if found:
        return found
    for cand in (r"C:\Program Files\LibreOffice\program\soffice.exe",
                 r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
                 "/Applications/LibreOffice.app/Contents/MacOS/soffice"):
        if Path(cand).exists():
            return cand
    return None


def soffice_convert(src: Path, fmt: str, outdir: Path) -> Path | None:
    exe = soffice()
    if not exe:
        return None
    outdir.mkdir(parents=True, exist_ok=True)
    try:
        # отдельный профиль LibreOffice: конвертация работает, даже если у пользователя открыт LibreOffice
        profile = Path(tempfile.gettempdir()) / "mdb_lo_profile"
        subprocess.run([exe, f"-env:UserInstallation={profile.as_uri()}", "--headless", "--convert-to", fmt,
                        "--outdir", str(outdir), str(src)],
                       check=True, capture_output=True, timeout=300)
    except Exception:
        return None
    out = outdir / (src.stem + "." + fmt.split(":")[0])
    return out if out.exists() else None


def save_image(img, dest: Path, max_side: int, quality: int) -> tuple[int, int]:
    """Пропорциональное уменьшение по длинной стороне + JPEG (наработка from_big_to_small,
    но без искажения пропорций).
    """
    from PIL import Image
    if img.mode in ("RGBA", "LA", "P"):
        img = img.convert("RGBA")
        bg = Image.new("RGB", img.size, (255, 255, 255))
        bg.paste(img, mask=img.split()[-1])
        img = bg
    elif img.mode != "RGB":
        img = img.convert("RGB")
    w, h = img.size
    scale = min(1.0, max_side / max(w, h))
    if scale < 1.0:
        img = img.resize((max(1, round(w * scale)), max(1, round(h * scale))), Image.Resampling.LANCZOS)
    dest.parent.mkdir(parents=True, exist_ok=True)
    img.save(dest, "JPEG", quality=quality, optimize=True)
    return img.size


table_to_md = ooxml.table_to_md
chart_xml_to_text = ooxml.chart_xml_to_text


# --------------------------------------------------------------------------- handlers
class Doc:
    def __init__(self, did: str, path: Path, kind: str):
        self.id, self.path, self.kind = did, path, kind
        self.units: list[tuple[str, str]] = []   # (якорь, текст)
        self.images: list[dict] = []
        self.warnings: list[str] = []
        self.unit_count = 0
        self.unit_name = ""


def handle_text(doc: Doc, path: Path, **_):
    doc.unit_name = "файл"
    doc.unit_count = 1
    doc.units.append((f"{doc.id}", clean(read_text_file(path))))


def handle_image(doc: Doc, path: Path, out: Path, max_side: int, quality: int, **_):
    from PIL import Image, ImageOps
    doc.unit_name = "изобр."
    doc.unit_count = 1
    try:
        with Image.open(path) as im:
            im.seek(0)
            im = ImageOps.exif_transpose(im)
            orig = im.size
            dest = out / "images" / f"{doc.id}.jpg"
            size = save_image(im, dest, max_side, quality)
        doc.images.append({"file": str(dest.relative_to(out)), "ref": doc.id, "reason": "входное изображение",
                           "orig_size": list(orig), "size": list(size)})
        doc.units.append((doc.id, "[Изображение: содержимое нужно прочитать визуально — см. images/"
                                  f"{doc.id}.jpg]"))
    except Exception as e:
        doc.warnings.append(f"не удалось открыть изображение: {e}")


def _save_media(doc: "Doc", media: list[tuple[str, bytes]], out: Path, max_side: int, quality: int,
                ref_fmt: str, reason: str, min_bytes: int = 12_000, min_side: int = 200) -> int:
    """Картинки из docx/pptx: мелочь (иконки, логотипы, буллеты) отбрасываем."""
    from PIL import Image
    k = 0
    for name, data in media:
        if len(data) < min_bytes:
            continue
        try:
            im = Image.open(io.BytesIO(data))
            im.load()
            if min(im.size) < min_side:
                continue
        except Exception:  # noqa: BLE001  (emf/wmf и прочее, что Pillow не открывает)
            continue
        k += 1
        dest = out / "images" / f"{doc.id}_img{k:02d}.jpg"
        size = save_image(im, dest, max_side, quality)
        doc.images.append({"file": str(dest.relative_to(out)), "ref": ref_fmt.format(k=k),
                           "reason": reason, "size": list(size)})
    return k


def handle_docx(doc: Doc, path: Path, out: Path, max_side: int, quality: int, **_):
    r = ooxml.read_docx(path)
    parts = []
    if r["header"]:
        parts.append(f"[Колонтитул] {r['header']}")
    parts.append(r["text"])
    parts += r["charts"]
    _save_media(doc, r["media"], out, max_side, quality, doc.id + " · рис. {k}", "рисунок внутри документа")
    text = clean("\n\n".join(p for p in parts if p))
    doc.unit_name = "стр.(оц.)"
    doc.unit_count = max(1, round(len(text) / 2500))
    doc.units.append((doc.id, text))
    if doc.images:
        doc.units.append((doc.id, f"[В документе {len(doc.images)} рисунк(а/ов) — см. images/{doc.id}_img*.jpg]"))


def _pdf_page_is_visual(pr, text: str) -> str | None:
    """Нужно ли смотреть страницу глазами. Возвращает причину или None."""
    n = len(text.strip())
    img_share = pr.image_area / pr.page_area
    if n < 30 and pr.spans and sum(len(sp[-1]) for sp in pr.spans) > 100:
        return "текст не декодируется (шрифт без кодировки)"
    if n < 30 and (img_share > 0.05 or pr.path_ops > 10):
        return "нет текстового слоя (скан/графика)"
    if img_share > 0.25:
        return "крупные изображения"
    if pr.path_ops > 40:
        return "векторная графика (график/схема)"
    if n < 200 and (img_share > 0 or pr.path_ops > 10):
        return "мало текста + графика"
    return None


def handle_pdf(doc: Doc, path: Path, out: Path, max_side: int, quality: int, dpi: int,
               pdf_render: str, max_visual: int, **_):
    pdoc, pages = pdfmod.read_pdf(path)
    doc.warnings += pdoc.warnings[:3]
    doc.unit_name = "стр."
    doc.unit_count = len(pages)
    renderer = pdfmod.renderer() if pdf_render != "none" else None
    rendered, no_raster = 0, []
    for i, pr in enumerate(pages, start=1):
        text = clean(pr.text())
        reason = None
        if pdf_render == "all":
            reason = "все страницы"
        elif pdf_render == "auto":
            reason = _pdf_page_is_visual(pr, text)
        if reason and rendered < max_visual:
            im, how = None, ""
            if renderer:
                im = pdfmod.render_page(path, i, dpi)
                how = "страница целиком"
            if im is None and pr.images:  # растеризатора нет — берём крупнейшую картинку страницы (скан)
                share, stm = max(pr.images, key=lambda t: t[0])
                if share > 0.05:
                    try:
                        im = pdfmod.image_to_pil(pdoc, stm)
                        how = "картинка со страницы"
                    except Exception:  # noqa: BLE001
                        im = None
            if im is not None:
                dest = out / "images" / f"{doc.id}_p{i:03d}.jpg"
                size = save_image(im, dest, max_side, quality)
                doc.images.append({"file": str(dest.relative_to(out)), "ref": f"{doc.id} · стр. {i}",
                                   "reason": f"{reason}; {how}", "size": list(size)})
                rendered += 1
                if len(text) < 200:
                    text = (text + "\n" if text else "") + f"[Страница-изображение — см. images/{dest.name}]"
            else:
                no_raster.append(i)
        elif reason:
            doc.warnings.append(f"стр. {i}: визуальная, но превышен лимит --max-visual={max_visual}")
        doc.units.append((f"{doc.id} · стр. {i}", text or "[пусто]"))
    if no_raster:
        pages_s = ", ".join(map(str, no_raster[:10])) + (" …" if len(no_raster) > 10 else "")
        doc.warnings.append(f"стр. {pages_s}: векторная графика, растеризатора нет — учтён только текст подписей "
                            f"(для картинок страниц нужен pdftoppm, Ghostscript или PyMuPDF)")
    if doc.unit_count and sum(len(t) for _, t in doc.units) < 100 * doc.unit_count and not doc.images:
        doc.warnings.append("PDF почти без текстового слоя (скан?) — картинки страниц извлечь не удалось")


def handle_pptx(doc: Doc, path: Path, out: Path, max_side: int, quality: int, dpi: int,
                pptx_render: str, max_visual: int, **_):
    r = ooxml.read_pptx(path)
    doc.unit_name = "слайд."
    doc.unit_count = len(r["slides"])
    visual: dict[int, str] = {}
    for i, sl in enumerate(r["slides"], start=1):
        parts = [sl["text"]] + ([f"[Заметки докладчика] {sl['notes']}"] if sl["notes"] else [])
        text = clean("\n".join(p for p in parts if p))
        if pptx_render == "all":
            visual[i] = "все слайды"
        elif pptx_render == "auto":
            if sl["flags"]:
                visual[i] = ", ".join(sorted(sl["flags"]))
            elif len(text) < 60 and sl["pictures"]:
                visual[i] = "мало текста"
        doc.units.append((f"{doc.id} · слайд {i}", text or "[без текста]"))
    if not visual or pptx_render == "none":
        return
    # 1) слайд целиком: LibreOffice → PDF → растеризатор (если оба есть)
    if soffice() and pdfmod.renderer():
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as td:
            pdf_path = soffice_convert(path, "pdf", Path(td))
            if pdf_path:
                rendered = 0
                for i in sorted(visual):
                    if rendered >= max_visual:
                        doc.warnings.append(f"слайдов с графикой больше лимита --max-visual={max_visual}")
                        break
                    im = pdfmod.render_page(pdf_path, i, dpi)
                    if im is None:
                        continue
                    dest = out / "images" / f"{doc.id}_s{i:03d}.jpg"
                    size = save_image(im, dest, max_side, quality)
                    doc.images.append({"file": str(dest.relative_to(out)), "ref": f"{doc.id} · слайд {i}",
                                       "reason": visual[i], "size": list(size)})
                    rendered += 1
                return
    # 2) без LibreOffice/растеризатора: диаграммы уже в тексте числами, картинки слайдов берём из файла
    from PIL import Image
    rendered = 0
    for i in sorted(visual):
        pics = [p for p in r["slides"][i - 1]["pictures"] if p[2] > 0.08]
        if not pics or rendered >= max_visual:
            continue
        name, data, share = max(pics, key=lambda p: p[2])
        try:
            im = Image.open(io.BytesIO(data))
            im.load()
        except Exception:  # noqa: BLE001
            continue
        dest = out / "images" / f"{doc.id}_s{i:03d}.jpg"
        size = save_image(im, dest, max_side, quality)
        doc.images.append({"file": str(dest.relative_to(out)), "ref": f"{doc.id} · слайд {i}",
                           "reason": f"{visual[i]}; картинка со слайда", "size": list(size)})
        rendered += 1


def handle_xlsx(doc: Doc, path: Path, max_rows: int = 200, **_):
    import openpyxl
    wb = openpyxl.load_workbook(str(path), read_only=True, data_only=True)
    doc.unit_name = "лист."
    doc.unit_count = len(wb.sheetnames)
    for ws in wb.worksheets:
        rows = []
        for r_i, row in enumerate(ws.iter_rows(values_only=True)):
            if r_i >= max_rows:
                doc.warnings.append(f"лист «{ws.title}»: показаны первые {max_rows} строк")
                break
            vals = ["" if v is None else str(v) for v in row]
            while vals and vals[-1] == "":
                vals.pop()
            if any(vals):
                rows.append(vals[:30])
        doc.units.append((f"{doc.id} · лист «{ws.title}»", table_to_md(rows) or "[пусто]"))


HANDLERS = {"text": handle_text, "image": handle_image, "docx": handle_docx, "pdf": handle_pdf,
            "pptx": handle_pptx, "xlsx": handle_xlsx}


def kind_of(path: Path) -> str | None:
    ext = path.suffix.lower()
    if ext in TEXT_EXT:
        return "text"
    if ext in IMAGE_EXT:
        return "image"
    if ext in (".xlsx", ".xlsm"):
        return "xlsx"
    if ext in (".docx", ".pdf", ".pptx"):
        return ext[1:]
    return None


# ------------------------------------------------------------------------------ main
def collect(inputs: list[str]) -> list[Path]:
    files: list[Path] = []
    for raw in inputs:
        p = Path(raw)
        if p.is_dir():
            files += sorted((f for f in p.rglob("*") if f.is_file()), key=lambda f: str(f).lower())
        elif p.is_file():
            files.append(p)
        else:
            print(f"[!] не найден: {raw}", file=sys.stderr)
    return [f for f in files if not f.name.startswith(("~$", ".")) and f.suffix.lower() in SUPPORTED]


def run(inputs: list[str], out: Path, max_side: int = 1568, quality: int = 85, dpi: int = 150,
        pdf_render: str = "auto", pptx_render: str = "auto", max_visual: int = 30) -> dict:
    out.mkdir(parents=True, exist_ok=True)
    for sub in ("images", "texts"):
        shutil.rmtree(out / sub, ignore_errors=True)
        (out / sub).mkdir(exist_ok=True)  # в Windows открытый в просмотрщике файл не даёт удалить папку
    seen: dict[str, str] = {}
    docs: list[Doc] = []
    skipped: list[dict] = []
    tmp = Path(tempfile.mkdtemp(prefix="mdb_legacy_"))

    for path in collect(inputs):
        digest = sha1(path)
        if digest in seen:
            skipped.append({"name": path.name, "reason": f"дубликат {seen[digest]}"})
            continue
        src = path
        if path.suffix.lower() in LEGACY:
            conv = soffice_convert(path, LEGACY[path.suffix.lower()], tmp)
            if not conv:
                skipped.append({"name": path.name, "reason": "legacy-формат, LibreOffice недоступен"})
                continue
            src = conv
        kind = kind_of(src)
        doc = Doc(f"D{len(docs) + 1}", path, kind)
        try:
            HANDLERS[kind](doc, src, out=out, max_side=max_side, quality=quality, dpi=dpi,
                           pdf_render=pdf_render, pptx_render=pptx_render, max_visual=max_visual)
        except Exception as e:
            doc.warnings.append(f"ошибка извлечения: {type(e).__name__}: {e}")
        content = sum(len(re.sub(r"\[[^\]]*\]|\s", "", t)) for _, t in doc.units)
        if not content and not doc.images:  # битый или пустой файл не получает ID и не попадает в источники
            skipped.append({"name": path.name, "reason": "; ".join(doc.warnings) or "пустой файл"})
            continue
        seen[digest] = doc.id
        docs.append(doc)

    corpus_parts = []
    manifest_docs = []
    units_out = []  # плоский список фрагментов (страница/слайд/лист/файл) — для упаковки в запросы к LLM
    for doc in docs:
        units_out += [{"doc": doc.id, "anchor": anchor, "text": text} for anchor, text in doc.units]
        header = f"# [{doc.id}] {doc.path.name} ({TYPE_LABEL[doc.kind]}, {doc.unit_count} {doc.unit_name})"
        body = "\n\n".join(f"<<{anchor}>>\n{text}" for anchor, text in doc.units)
        doc_md = header + "\n\n" + body + "\n"
        (out / "texts" / f"{doc.id}.md").write_text(doc_md, encoding="utf-8", errors="replace")
        corpus_parts.append(doc_md)
        chars = sum(len(t) for _, t in doc.units)
        manifest_docs.append({
            "id": doc.id, "name": doc.path.name, "path": str(doc.path), "type": TYPE_LABEL[doc.kind],
            "units": doc.unit_count, "unit_name": doc.unit_name, "chars": chars,
            "est_tokens": int(chars / CHARS_PER_TOKEN), "text_file": f"texts/{doc.id}.md",
            "images": doc.images, "warnings": doc.warnings,
        })
    (out / "corpus.md").write_text("\n\n".join(corpus_parts), encoding="utf-8", errors="replace")
    (out / "units.json").write_text(json.dumps(units_out, ensure_ascii=False, indent=1), encoding="utf-8",
                                    errors="replace")
    shutil.rmtree(tmp, ignore_errors=True)

    total_tokens = sum(d["est_tokens"] for d in manifest_docs)
    manifest = {
        "documents": manifest_docs,
        "skipped": skipped,
        "totals": {
            "documents": len(manifest_docs),
            "by_type": {t: sum(1 for d in manifest_docs if d["type"] == t)
                        for t in sorted({d["type"] for d in manifest_docs})},
            "chars": sum(d["chars"] for d in manifest_docs),
            "est_tokens": total_tokens,
            "images": sum(len(d["images"]) for d in manifest_docs),
        },
        "reading_strategy": ("single_pass" if total_tokens <= 60_000 else "per_document_notes"),
        "settings": {"max_side": max_side, "quality": quality, "dpi": dpi,
                     "pdf_render": pdf_render, "pptx_render": pptx_render, "max_visual": max_visual},
    }
    (out / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8",
                                       errors="replace")
    return manifest


def print_summary(m: dict, out: Path):
    print(f"Корпус: {out}/corpus.md   Манифест: {out}/manifest.json")
    print(f"{'ID':<4} {'Тип':<5} {'Объём':<12} {'~токенов':>9} {'изобр.':>6}  Файл")
    for d in m["documents"]:
        vol = f"{d['units']} {d['unit_name']}"
        print(f"{d['id']:<4} {d['type']:<5} {vol:<12} {d['est_tokens']:>9} {len(d['images']):>6}  {d['name']}")
        for w in d["warnings"]:
            print(f"     [!] {w}")
    for s in m["skipped"]:
        print(f"     [пропущен] {s['name']}: {s['reason']}")
    t = m["totals"]
    print(f"Итого: {t['documents']} док., ~{t['est_tokens']} токенов текста, {t['images']} изображений "
          f"к просмотру. Стратегия чтения: {m['reading_strategy']}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("inputs", nargs="+", help="файлы и/или папки")
    ap.add_argument("--out", default="work", help="папка результата (default: work)")
    ap.add_argument("--max-side", type=int, default=1568,
                    help="макс. длинная сторона изображения, px (Claude: 1568; локальная VLM: 768–1024)")
    ap.add_argument("--quality", type=int, default=85, help="JPEG quality")
    ap.add_argument("--dpi", type=int, default=150, help="DPI рендера страниц PDF/слайдов")
    ap.add_argument("--pdf-render", choices=["auto", "all", "none"], default="auto")
    ap.add_argument("--pptx-render", choices=["auto", "all", "none"], default="auto")
    ap.add_argument("--max-visual", type=int, default=30, help="лимит рендеров на один документ")
    a = ap.parse_args()
    for stream in (sys.stdout, sys.stderr):  # консоль Windows в cp1251 не должна ронять вывод
        try:
            stream.reconfigure(errors="replace")
        except Exception:  # noqa: BLE001
            pass
    out = Path(a.out)
    m = run(a.inputs, out, a.max_side, a.quality, a.dpi, a.pdf_render, a.pptx_render, a.max_visual)
    print_summary(m, out)
    if not m["documents"]:
        sys.exit("Нет поддерживаемых документов.")


if __name__ == "__main__":
    main()
