# -*- coding: utf-8 -*-
"""pdf.py — приём PDF и чтение страниц.

Команды:
  open   <путь к PDF>             создать (или продолжить) задание, извлечь текст страниц,
                                  определить вид каждой страницы (text / mixed / scan / scan_text / broken)
  ocr    <job> [--pages 1-8] [--force]
                                  распознать сканы и растровые картинки (rapidocr, без сети);
                                  текст попадает в pages/NNNN.txt, рамки — в ocr/NNNN.json;
                                  --force с --pages — распознать и фоновые картинки (decor_pages)
  pages  <job> [--pages 1-8]      напечатать текст страниц (порциями, с ограничением объёма)
  render <job> --pages 3 [--dpi 110]
                                  отрисовать страницы в PNG (посмотреть графики глазами)
  jobs                            список заданий в папке состояния

Входной PDF только читается и копируется в папку задания; всё остальное пишется
внутрь OUROBOROS_SKILL_STATE_DIR/jobs/<job>/.
"""
from __future__ import annotations

import argparse
import os
import re
import shutil
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import _core as core  # noqa: E402

MAX_PDF_MB = 300
PAGES_OUT_CAP = 40_000


def cmd_open(args) -> None:
    pymupdf = core.require_pymupdf()
    src = Path(args.pdf).expanduser()
    if not src.is_file():
        core.fail("Файл не найден: %s" % src, "Передайте полный путь к PDF-файлу.")
    size_mb = src.stat().st_size / 1e6
    if size_mb > MAX_PDF_MB:
        core.fail("Файл %.0f МБ больше лимита %d МБ." % (size_mb, MAX_PDF_MB))
    with open(src, "rb") as fh:
        if b"%PDF" not in fh.read(1024):
            core.fail("Это не PDF-файл (нет сигнатуры %PDF).", "Навык работает только с PDF.")

    try:
        probe = pymupdf.open(src)
    except Exception as e:
        core.fail("PDF не открывается: %s" % e, "Файл повреждён или это не PDF.")
    if probe.needs_pass:
        core.fail("PDF защищён паролем.", "Попросите у пользователя версию без пароля.")
    if probe.page_count == 0:
        core.fail("В PDF нет страниц.")
    probe.close()

    sha = core.file_sha(src)
    job = "%s-%s" % (core.slugify(src.stem), sha[:8])
    jdir = core.job_dir(job, must_exist=False)
    (jdir / "pages").mkdir(parents=True, exist_ok=True)
    local = jdir / "source.pdf"
    if not local.is_file() or local.stat().st_size != src.stat().st_size:
        part = jdir / "source.pdf.part"
        shutil.copyfile(src, part)
        os.replace(part, local)
    doc = pymupdf.open(local)

    deadline = core.Deadline()
    meta = core.read_json(jdir / "meta.json", {}) or {}
    done = int(meta.get("pages_extracted", 0))
    total = doc.page_count
    page_info = meta.get("page_info", [])
    for n in range(done + 1, total + 1):
        page = doc[n - 1]
        text = page.get_text("text", sort=True)
        (jdir / "pages" / ("%04d.txt" % n)).write_text(text, encoding="utf-8")
        letters = sum(ch.isalpha() for ch in text)
        info = {
            "n": n,
            "chars": len(text),
            "letters": letters,
            "images": len(page.get_images()),
            "w": round(page.rect.width, 1),
            "h": round(page.rect.height, 1),
        }
        info.update(_classify(page, text, letters))
        page_info.append(info)
        done = n
        if deadline.expired():
            break
    for info in page_info:
        if "kind" not in info and not deadline.expired():
            page = doc[int(info["n"]) - 1]
            text = page.get_text("text", sort=True)
            info.update(_classify(page, text, int(info.get("letters", sum(ch.isalpha() for ch in text)))))

    textless = [p["n"] for p in page_info if p["letters"] < 25]
    md = doc.metadata or {}
    meta.update(
        {
            "job": job,
            "source_name": src.name,
            "sha256": sha,
            "pages_total": total,
            "pages_extracted": done,
            "page_info": page_info,
            "pdf_title": (md.get("title") or "").strip(),
            "pdf_author": (md.get("author") or "").strip(),
            "pdf_created": (md.get("creationDate") or "").strip(),
            "pages_without_text": textless,
        }
    )
    core.write_json(jdir / "meta.json", meta)

    complete = done >= total
    total_chars = sum(p["chars"] for p in page_info)
    resp = {
        "ok": True,
        "job": job,
        "complete": complete,
        "pages_total": total,
        "pages_extracted": done,
        "text_chars": total_chars,
        "pdf_title": meta["pdf_title"],
        "pdf_author": meta["pdf_author"],
        "pages_without_text": textless[:60],
        "job_dir": str(jdir),
        "elapsed_sec": deadline.elapsed(),
    }
    kinds: dict = {}
    for p in page_info:
        kinds[p.get("kind", "text")] = kinds.get(p.get("kind", "text"), 0) + 1
    resp["page_kinds"] = kinds
    needs = _needs_ocr(meta)
    if needs:
        resp["needs_ocr"] = needs[:80]
    if not complete:
        resp["next"] = "Документ большой: повторите тот же вызов pdf.py open — извлечение продолжится со страницы %d." % (done + 1)
    elif needs:
        what = []
        if kinds.get("scan") or kinds.get("broken"):
            what.append("сканы без текстового слоя")
        if kinds.get("mixed"):
            what.append("растровые картинки с текстом (графики)")
        resp["next"] = ("В документе есть %s: страницы %s. Запустите pdf.py ocr %s — распознавание запишет текст в страницы; "
                        "до этого pages на этих страницах пусты или неполны." % (", ".join(what), needs[:20], job))
    else:
        resp["next"] = "Читайте страницы порциями: pdf.py pages %s --pages 1-8" % job
    decor_pages = [p["n"] for p in page_info if p.get("decor") and p.get("kind") == "text"]
    if decor_pages:
        resp["decor_pages"] = decor_pages[:60]
        resp["decor_note"] = ("На страницах %s есть только картинки во всю ширину листа (обложка, шапка раздела, фоновое фото) — "
                              "распознавание им не назначено, текст этих страниц есть в слое. Графики с подписями в текстовом слое "
                              "читаются через pdf.py pages как обычно. Если на такой картинке всё же есть данные — "
                              "pdf.py ocr %s --pages N --force." % (decor_pages[:20], job))
    if kinds.get("scan_text"):
        resp["note"] = ("Страницы вида scan_text — сканы с готовым текстовым слоем (после чужого OCR): текст читается из слоя, "
                        "распознавание им не нужно.")
    core.out(resp)


_BAD_CHARS_RE = re.compile("[\\ufffd\\ue000-\\uf8ff\\x00-\\x08\\x0b\\x0c\\x0e-\\x1f]")
_WORD_RE = re.compile(r"[A-Za-zА-Яа-яЁё]{4,}")
_VOWEL_RE = re.compile(r"[aeiouyAEIOUYаеёиоуыэюяАЕЁИОУЫЭЮЯ]")


def _classify(page, text: str, letters: int) -> dict:
    if page.rotation:
        page.remove_rotation()
    W, H = page.rect.width, page.rect.height
    area = max(1.0, W * H)
    regions, decor, full = [], [], 0.0
    try:
        infos = page.get_image_info()
    except Exception:
        infos = []
    for inf in infos:
        b = inf.get("bbox")
        if not b:
            continue
        x0, y0 = max(0.0, b[0]), max(0.0, b[1])
        x1, y1 = min(W, b[2]), min(H, b[3])
        a = max(0.0, x1 - x0) * max(0.0, y1 - y0) / area
        if a >= 0.85:
            full = max(full, a)
        elif a >= 0.03 and (x1 - x0) >= 40 and (y1 - y0) >= 24:
            box = [round(x0, 1), round(y0, 1), round(x1, 1), round(y1, 1)]
            # картинка «в обрез» от левого до правого края — фон, шапка, фото обложки, а не график
            (decor if x0 <= 0.01 * W and x1 >= 0.99 * W else regions).append(box)
    stripped = text.strip()
    bad = len(_BAD_CHARS_RE.findall(stripped))
    words = _WORD_RE.findall(stripped)
    no_vowel = sum(1 for w in words if not _VOWEL_RE.search(w))
    garbled = letters >= 25 and (bad > 0.15 * len(stripped) or (len(words) >= 12 and no_vowel > 0.45 * len(words)))
    if letters < 25:
        kind = "scan" if (full > 0 or regions or decor) else "text"
    elif garbled:
        kind = "broken"
    elif full > 0 and _invisible_text(page):
        kind = "scan_text"
    elif regions:
        kind = "mixed"
    else:
        kind = "text"
    out = {"kind": kind}
    if regions and kind == "mixed":
        out["regions"] = _merge_regions(regions)[:24]
    if decor and kind in ("text", "mixed"):
        out["decor"] = _merge_regions(decor)[:8]
    if bad:
        out["bad_chars"] = bad
    return out


def _invisible_text(page) -> bool:
    try:
        contents = page.read_contents()
    except Exception:
        return False
    return re.search(rb"(?<![\d.])[37]\s+Tr(?![A-Za-z])", contents) is not None


def _merge_regions(rects: list) -> list:
    rects = sorted(rects, key=lambda r: (r[1], r[0]))
    out: list = []
    for r in rects:
        for o in out:
            if r[0] < o[2] + 6 and r[2] > o[0] - 6 and r[1] < o[3] + 6 and r[3] > o[1] - 6:
                o[0], o[1], o[2], o[3] = min(o[0], r[0]), min(o[1], r[1]), max(o[2], r[2]), max(o[3], r[3])
                break
        else:
            out.append(list(r))
    return [[round(v, 1) for v in o] for o in out]


OCR_MARK = "[Текст на картинках страницы, распознан OCR]"


def _write_text(path: Path, text: str) -> None:
    tmp = path.with_suffix(".tmp")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, path)


def _needs_ocr(meta: dict) -> list[int]:
    return [p["n"] for p in meta.get("page_info", []) if p.get("kind") in ("scan", "broken", "mixed") and not p.get("ocr")]


def _drop_layer_rows(page, rows: list[dict]) -> list[dict]:
    words = [w[:4] for w in page.get_text("words") if w[4].strip()]
    if not words or not rows:
        return rows
    import numpy as np
    W = np.array(words, dtype=float)
    keep = []
    for r in rows:
        x0, y0, x1, y1 = r["bbox"]
        area = max((x1 - x0) * (y1 - y0), 1e-6)
        ix = np.clip(np.minimum(x1, W[:, 2]) - np.maximum(x0, W[:, 0]), 0, None)
        iy = np.clip(np.minimum(y1, W[:, 3]) - np.maximum(y0, W[:, 1]), 0, None)
        if float((ix * iy).sum()) / area < 0.35:
            keep.append(r)
    return keep


def cmd_ocr(args) -> None:
    pymupdf = core.require_pymupdf()
    jdir = core.job_dir(args.job)
    meta = core.read_json(jdir / "meta.json", {})
    if int(meta.get("pages_extracted", 0)) < int(meta.get("pages_total", 0)):
        core.fail("Извлечение текста не завершено.", "Сначала повторите pdf.py open — до complete: true.")
    todo = _needs_ocr(meta)
    forced = set()
    if args.pages:
        wanted = set(core.parse_pages(args.pages, int(meta.get("pages_total", 0))))
        todo = [n for n in todo if n in wanted]
        if getattr(args, "force", False):
            forced = {p["n"] for p in meta.get("page_info", []) if p["n"] in wanted and p.get("decor") and not p.get("ocr")}
            todo = sorted(set(todo) | forced)
    if not todo:
        rest_all = _needs_ocr(meta)
        core.out({"ok": True, "job": args.job, "pages_done": [], "complete": not rest_all, "pages_left": rest_all[:60],
                  "note": ("Страниц для распознавания нет: текстовый слой есть на всех страницах." if not rest_all
                           else "В указанном диапазоне распознавать нечего; остались страницы %s." % rest_all[:20])})
    try:
        import _ocr as ocr
        engine = ocr.Engine(core.state_dir())
    except Exception as e:
        core.fail(
            "Модуль распознавания недоступен: %s: %s" % (type(e).__name__, str(e)[:300]),
            "Зависимость rapidocr объявлена в SKILL.md и ставится платформой после ревью. Если она не установилась, "
            "сканы придётся читать глазами (pdf.py render) — предупредите пользователя.",
        )
    info = {p["n"]: p for p in meta.get("page_info", [])}
    doc = pymupdf.open(jdir / "source.pdf")
    (jdir / "ocr").mkdir(exist_ok=True)
    deadline = core.Deadline(200)
    done, cyr_pages, busy_pages = [], [], []
    for n in todo:
        page = doc[n - 1]
        if page.rotation:
            page.remove_rotation()
        p = info[n]
        if n in forced and p["kind"] == "text":
            p["kind"], p["regions"] = "mixed", p.get("decor")
        regions = p.get("regions") if p["kind"] == "mixed" else None
        rows = ocr.page_rows(engine, pymupdf, page, regions)
        if p["kind"] == "mixed":
            rows = _drop_layer_rows(page, rows)
        rows = ocr.merge_fragments(rows)
        rows = ocr.reading_order(rows, page.rect.width)
        cyr, lat = ocr.script_share(rows)
        core.write_json(jdir / "ocr" / ("%04d.json" % n), {
            "page": n, "kind": p["kind"], "dpi": ocr.DPI, "cyrillic_model": engine.has_cyrillic,
            "rows": rows,
        })
        text_path = jdir / "pages" / ("%04d.txt" % n)
        ocr_text = ocr.rows_text(rows)
        if p["kind"] in ("scan", "broken"):
            _write_text(text_path, ocr_text)
        elif p["kind"] == "mixed" and ocr_text.strip():
            base = core.page_text(jdir, n).split("\n\n" + OCR_MARK)[0].rstrip()
            _write_text(text_path, base + "\n\n" + OCR_MARK + "\n" + ocr_text)
        p["ocr"] = True
        p["ocr_rows"] = len(rows)
        glyphs = len(re.sub(r"[\s\W\d_]", "", ocr_text))
        if not engine.has_cyrillic and len(rows) >= 5 and (cyr > lat or glyphs < 0.35 * max(1, len(re.sub(r"\s", "", ocr_text)))):
            cyr_pages.append(n)
        if sum(1 for r in rows if r.get("busy")) > max(2, len(rows) // 3):
            busy_pages.append(n)
        done.append(n)
        core.write_json(jdir / "meta.json", meta)
        if deadline.expired():
            break
    rest = _needs_ocr(meta)
    resp = {
        "ok": True, "job": args.job, "pages_done": done, "pages_left": rest[:60], "complete": not rest,
        "cyrillic_model": engine.has_cyrillic, "elapsed_sec": deadline.elapsed(),
    }
    warnings = []
    if cyr_pages:
        warnings.append("На страницах %s распознавание почти не нашло букв: скорее всего, текст на русском, а модели кириллицы нет "
                        "(пакет pdf_rezume_ocr_cyrillic не установлен) — читать эти страницы по OCR нельзя, скажите об этом пользователю."
                        % cyr_pages[:20])
    if busy_pages:
        warnings.append("На страницах %s текст лежит на пёстром фоне: распознавание там менее надёжно — при сомнении посмотрите страницу через pdf.py render." % busy_pages[:20])
    if warnings:
        resp["warnings"] = warnings
    if rest:
        resp["next"] = "Распознано %d стр., осталось %d: повторите тот же вызов pdf.py ocr %s." % (len(done), len(rest), args.job)
    elif cyr_pages and len(cyr_pages) >= len(done):
        resp["next"] = "Распознанный текст непригоден (см. warnings): резюме по этим страницам невозможно без модели кириллицы."
    else:
        resp["next"] = "Текст со сканов записан в страницы: читайте pdf.py pages как обычно; дальше — facts.py add."
    core.out(resp)


def _compact(text: str) -> str:
    lines = [re.sub(r"[ \t\u00a0]{2,}", " ", ln).strip() for ln in text.splitlines()]
    return re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).strip()


def cmd_pages(args) -> None:
    jdir = core.job_dir(args.job)
    meta = core.read_json(jdir / "meta.json", {})
    total = int(meta.get("pages_extracted", 0))
    wanted = core.parse_pages(args.pages, total)
    pages, used, last = [], 0, None
    for n in wanted:
        text = _compact(core.page_text(jdir, n))
        if pages and used + len(text) > PAGES_OUT_CAP:
            break
        if len(text) > PAGES_OUT_CAP:
            text = text[:PAGES_OUT_CAP] + "\n[…страница обрезана по лимиту вывода…]"
        pages.append({"page": n, "text": text})
        used += len(text)
        last = n
    rest = [n for n in wanted if last is not None and n > last]
    resp = {"ok": True, "job": args.job, "pages_total": meta.get("pages_total"), "pages": pages}
    if rest:
        resp["next_pages"] = "%d-%d" % (rest[0], rest[-1])
        resp["note"] = "Показано до страницы %d из запрошенных; остальное — следующим вызовом." % last
    pending = [n for n in _needs_ocr(meta) if n in wanted]
    if pending:
        resp["pages_pending_ocr"] = pending[:60]
        resp["warnings"] = ["Страницы %s — сканы или картинки с текстом, ещё не распознанные: текст неполный. "
                            "Запустите pdf.py ocr %s и прочтите их снова." % (pending[:20], args.job)]
    core.out(resp)


def cmd_render(args) -> None:
    pymupdf = core.require_pymupdf()
    jdir = core.job_dir(args.job)
    meta = core.read_json(jdir / "meta.json", {})
    pdf_path = jdir / "source.pdf"
    doc = pymupdf.open(pdf_path)
    wanted = core.parse_pages(args.pages, doc.page_count)[:12]
    dpi = max(50, min(int(args.dpi), 200))
    folder = jdir / "png"
    folder.mkdir(exist_ok=True)
    files = []
    for n in wanted:
        target = folder / ("%04d.png" % n)
        doc[n - 1].get_pixmap(dpi=dpi).save(target)
        files.append({"page": n, "png": str(target)})
    core.out(
        {
            "ok": True,
            "job": args.job,
            "files": files,
            "note": "Откройте PNG своим инструментом просмотра изображений (view_image / vlm_query). Если инструмент не пускает "
                    "в папку состояния навыка (так в light-режиме Ouroboros до v7), визуальную проверку пропустите — "
                    "текст с картинок даёт pdf.py ocr. За один вызов — не больше 12 страниц.",
            "pages_total": meta.get("pages_total"),
        }
    )


def cmd_jobs(_args) -> None:
    rows = []
    for d in sorted(core.jobs_root().iterdir()):
        meta = core.read_json(d / "meta.json")
        if meta:
            rows.append(
                {
                    "job": meta.get("job"),
                    "source": meta.get("source_name"),
                    "pages": meta.get("pages_total"),
                    "summary_ready": core.output_paths(d)["summary_pdf"].is_file(),
                    "translation_ready": core.output_paths(d)["translation_pdf"].is_file(),
                }
            )
    core.out({"ok": True, "jobs": rows})


def main() -> None:
    core.setup_stdio()
    ap = core.JsonArgumentParser(prog="pdf.py", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd")
    p = sub.add_parser("open"); p.add_argument("pdf"); p.set_defaults(fn=cmd_open)
    p = sub.add_parser("ocr"); p.add_argument("job"); p.add_argument("--pages"); p.add_argument("--force", action="store_true")
    p.set_defaults(fn=cmd_ocr)
    p = sub.add_parser("pages"); p.add_argument("job"); p.add_argument("--pages"); p.set_defaults(fn=cmd_pages)
    p = sub.add_parser("render"); p.add_argument("job"); p.add_argument("--pages", required=True)
    p.add_argument("--dpi", default=110, type=int); p.set_defaults(fn=cmd_render)
    p = sub.add_parser("jobs"); p.set_defaults(fn=cmd_jobs)
    args = ap.parse_args()
    if not getattr(args, "fn", None):
        core.fail("Не указана команда.", "Доступно: open, ocr, pages, render, jobs.")
    args.fn(args)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as e:
        core.fail("Внутренняя ошибка pdf.py: %s: %s" % (type(e).__name__, e))
