#!/usr/bin/env python3
"""
pdf_remove_watermark.py — 通用 PDF 水印移除工具
支持 4 种策略：
  1. xobject — XObject 字体特征法（覆盖页面 80%+ 的子集字体 XObject）
  2. alpha   — 透明/半透明图层法（ExtGState ca/CA < 0.6 的 XObject）
  3. text    — 文字水印检测（大字号 + 斜向 / 水印关键词，pymupdf redact API）
  4. image   — 重复图片 XObject 法（每页相同位置 → 水印图片）

依赖：pymupdf (fitz), pdfplumber, pypdf
"""

from __future__ import annotations

import argparse
import io
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Optional

import fitz                        # pymupdf
import pdfplumber
from pypdf import PdfReader, PdfWriter
from pypdf.generic import (
    ArrayObject, DictionaryObject, FloatObject,
    NameObject, NumberObject, DecodedStreamObject,
)

# ─── 常量 ──────────────────────────────────────────────────────────────────────
SUBSET_FONT_RE = re.compile(r'^[A-Z]{6}\+')  # 子集嵌入字体标记，如 AAAAAB+Helvetica-Bold
WATERMARK_KEYWORDS_RE = re.compile(
    r'DRAFT|CONFIDENTIAL|SAMPLE|COPY|TOP.?SECRET|PROPRIETARY'
    r'|草稿|保密|样本|仅供参考|内部资料|水印|机密|秘密|绝密',
    re.IGNORECASE,
)
FULL_PAGE_RATIO = 0.80   # XObject bbox 覆盖整页的比例阈值
LOW_ALPHA_THRESHOLD = 0.6  # 透明度阈值，低于此值视为半透明水印
BIG_FONT_SIZE = 20        # 文字水印的字号阈值（pt）
TILT_THRESHOLD = 0.3      # 斜向文字判断：|dir[1]| > 此值


# ─── 辅助：从 pypdf XObject 提取字体名 ────────────────────────────────────────

def _get_xobj_font_names(xobj: DictionaryObject) -> list[str]:
    """返回 XObject resources 中的字体名列表。"""
    names: list[str] = []
    resources = xobj.get('/Resources')
    if resources is None:
        return names
    fonts = resources.get('/Font')
    if fonts is None:
        return names
    for key in fonts:
        font_obj = fonts[key]
        if isinstance(font_obj, DictionaryObject):
            base_font = font_obj.get('/BaseFont')
            if base_font:
                names.append(str(base_font))
    return names


def _xobj_bbox_dims(xobj: DictionaryObject) -> tuple[float, float]:
    """返回 (width, height) of XObject BBox；若无则 (0, 0)。"""
    bbox = xobj.get('/BBox')
    if bbox is None:
        return 0.0, 0.0
    try:
        coords = [float(v) for v in bbox]
        w = abs(coords[2] - coords[0])
        h = abs(coords[3] - coords[1])
        return w, h
    except Exception:
        return 0.0, 0.0


def _xobj_has_low_alpha(xobj: DictionaryObject) -> bool:
    """检测 XObject 的 ExtGState 是否含低透明度设置。"""
    resources = xobj.get('/Resources')
    if resources is None:
        return False
    ext_gs = resources.get('/ExtGState')
    if ext_gs is None:
        return False
    for gs_key in ext_gs:
        gs = ext_gs[gs_key]
        if not isinstance(gs, DictionaryObject):
            continue
        for alpha_key in ('/ca', '/CA'):
            val = gs.get(alpha_key)
            if val is not None:
                try:
                    if float(val) < LOW_ALPHA_THRESHOLD:
                        return True
                except Exception:
                    pass
    return False


# ─── 策略1 & 2：XObject 结构分析（用 pypdf）──────────────────────────────────

def analyze_xobjects(pdf_path: str, aggressive: bool = False) -> dict:
    """
    分析每页的 XObject，返回水印候选列表。

    返回结构：
    {
      page_idx: {
        "xobject": [xobj_name, ...],  # 策略1 命中
        "alpha":   [xobj_name, ...],  # 策略2 命中
        "image_repeat": [xobj_name, ...]  # 策略4 命中
      }
    }
    """
    reader = PdfReader(pdf_path)
    results: dict[int, dict] = {}

    # 策略4：收集每页 XObject 引用，统计跨页重复
    page_xobj_refs: list[dict] = []  # [{name: ref_id, ...}, ...]

    for page_idx, page in enumerate(reader.pages):
        w_pt = float(page.mediabox.width)
        h_pt = float(page.mediabox.height)

        resources = page.get('/Resources')
        if resources is None:
            page_xobj_refs.append({})
            continue

        xobjects = resources.get('/XObject')
        if xobjects is None:
            page_xobj_refs.append({})
            continue

        xobj_candidates_s1: list[str] = []
        xobj_candidates_s2: list[str] = []
        page_ref_map: dict[str, int] = {}

        for name in xobjects:
            xobj = xobjects[name]
            if not isinstance(xobj, DictionaryObject):
                try:
                    xobj = xobj.get_object()
                except Exception:
                    continue
            if not isinstance(xobj, DictionaryObject):
                continue

            # 记录引用 id（用于策略4）
            try:
                ref_id = xobjects.raw_get(name).idnum  # type: ignore[attr-defined]
                page_ref_map[str(name)] = ref_id
            except Exception:
                page_ref_map[str(name)] = id(xobj)

            # 策略1：bbox 覆盖整页 + 只有子集字体
            xobj_w, xobj_h = _xobj_bbox_dims(xobj)
            covers_page = xobj_w > w_pt * FULL_PAGE_RATIO and xobj_h > h_pt * FULL_PAGE_RATIO
            if covers_page:
                font_names = _get_xobj_font_names(xobj)
                all_subset = font_names and all(SUBSET_FONT_RE.match(f.lstrip('/')) for f in font_names)
                if all_subset:
                    xobj_candidates_s1.append(str(name))
                elif aggressive and font_names:
                    # 激进模式：只要覆盖整页且有字体就标记
                    xobj_candidates_s1.append(str(name))

            # 策略2：低透明度 XObject（不要求覆盖整页）
            if _xobj_has_low_alpha(xobj):
                xobj_candidates_s2.append(str(name))

        page_xobj_refs.append(page_ref_map)
        results[page_idx] = {
            'xobject': xobj_candidates_s1,
            'alpha': xobj_candidates_s2,
            'image_repeat': [],
        }

    # 策略4：找到在每页相同位置出现的图片 XObject（跨页重复）
    n_pages = len(reader.pages)
    if n_pages >= 2:
        # 统计每个 ref_id 出现的页数
        ref_page_count: Counter[int] = Counter()
        for ref_map in page_xobj_refs:
            seen_refs = set(ref_map.values())
            for rid in seen_refs:
                ref_page_count[rid] += 1

        # 出现在超过一半页面的同一图片 ref → 视为水印
        repeat_threshold = max(2, n_pages // 2)
        repeat_refs = {rid for rid, cnt in ref_page_count.items() if cnt >= repeat_threshold}

        for page_idx, ref_map in enumerate(page_xobj_refs):
            for name, rid in ref_map.items():
                if rid in repeat_refs:
                    if page_idx not in results:
                        results[page_idx] = {'xobject': [], 'alpha': [], 'image_repeat': []}
                    if name not in results[page_idx]['image_repeat']:
                        results[page_idx]['image_repeat'].append(name)

    return results


def _remove_xobj_from_content_stream(content_data: bytes, xobj_names: set[str]) -> bytes:
    """
    从 PDF 内容流中删除对指定 XObject 的 Do 调用。
    匹配模式：  /Name Do
    """
    pattern = re.compile(
        rb'(?:/(?:' + b'|'.join(re.escape(n.lstrip('/').encode()) for n in xobj_names) + rb'))\\s+Do(?=\\s|$)',
        re.MULTILINE,
    )
    return pattern.sub(b'', content_data)


def remove_xobjects_pypdf(pdf_path: str, out_path: str,
                           xobj_results: dict, methods: set[str],
                           aggressive: bool, detect_only: bool) -> list[str]:
    """
    用 pypdf 移除 XObject 水印（策略1/2/4）。
    返回报告列表。
    """
    reader = PdfReader(pdf_path)
    writer = PdfWriter()
    writer.append(reader)

    report: list[str] = []
    for page_idx, findings in xobj_results.items():
        to_remove: set[str] = set()

        if 'xobject' in methods and findings.get('xobject'):
            for n in findings['xobject']:
                confidence = 'HIGH' if aggressive else 'HIGH'
                report.append(f'  页{page_idx+1} [策略1-XObject字体] {n} (confidence={confidence})')
                to_remove.add(n)

        if 'alpha' in methods and findings.get('alpha'):
            for n in findings['alpha']:
                confidence = 'HIGH' if aggressive else 'MEDIUM'
                report.append(f'  页{page_idx+1} [策略2-半透明图层] {n} (confidence={confidence})')
                if aggressive:
                    to_remove.add(n)
                else:
                    report[-1] += ' → 仅报告（需 --aggressive 才移除）'

        if 'image' in methods and findings.get('image_repeat'):
            for n in findings['image_repeat']:
                confidence = 'HIGH' if aggressive else 'MEDIUM'
                report.append(f'  页{page_idx+1} [策略4-重复图片] {n} (confidence={confidence})')
                if aggressive:
                    to_remove.add(n)
                else:
                    report[-1] += ' → 仅报告（需 --aggressive 才移除）'

        if detect_only or not to_remove:
            continue

        # 修改页面内容流，删除 Do 调用
        page = writer.pages[page_idx]
        content = page.get('/Contents')
        if content is None:
            continue

        # 规范化为 list
        if hasattr(content, '__iter__') and not hasattr(content, 'get_data'):
            content_list = list(content)
        else:
            content_list = [content]

        for c in content_list:
            try:
                c_obj = c.get_object()
                raw = c_obj.get_data()
                new_raw = _remove_xobj_from_content_stream(raw, to_remove)
                if new_raw != raw:
                    new_stream = DecodedStreamObject()
                    new_stream.set_data(new_raw)
                    c_obj._data = new_stream._data  # type: ignore[attr-defined]
            except Exception as e:
                report.append(f'    警告：修改内容流失败 page{page_idx}: {e}')

        # 从 Resources/XObject 中移除条目
        try:
            resources = page.get('/Resources')
            if resources:
                xobjects = resources.get('/XObject')
                if xobjects:
                    for n in to_remove:
                        key = NameObject(n if n.startswith('/') else '/' + n)
                        if key in xobjects:
                            del xobjects[key]
        except Exception as e:
            report.append(f'    警告：移除 XObject 资源失败 page{page_idx}: {e}')

    if not detect_only:
        with open(out_path, 'wb') as f:
            writer.write(f)

    return report


# ─── 策略3：文字水印检测（pymupdf redact API）────────────────────────────────

def analyze_text_watermarks(pdf_path: str) -> dict[int, list[tuple]]:
    """
    用 pymupdf 扫描每页文字，返回水印字符 bbox 列表。
    返回：{page_idx: [(bbox_tuple, text, reason), ...]}
    """
    doc = fitz.open(pdf_path)
    result: dict[int, list[tuple]] = {}

    for page_idx, page in enumerate(doc):
        candidates = []
        blocks = page.get_text('dict')['blocks']
        for block in blocks:
            if block.get('type') != 0:  # 0 = 文字块
                continue
            for line in block.get('lines', []):
                dir_vec = line.get('dir', (1.0, 0.0))
                is_tilted = abs(dir_vec[1]) > TILT_THRESHOLD  # 斜向文字
                for span in line.get('spans', []):
                    text = span.get('text', '').strip()
                    if not text:
                        continue
                    size = span.get('size', 0)
                    is_big = size > BIG_FONT_SIZE
                    is_keyword = bool(WATERMARK_KEYWORDS_RE.search(text))

                    reasons = []
                    if is_big and is_tilted:
                        reasons.append(f'大字号({size:.0f}pt)+斜向')
                    if is_keyword:
                        reasons.append(f'水印关键词"{text}"')

                    if reasons:
                        candidates.append((span['bbox'], text, ', '.join(reasons)))

        if candidates:
            result[page_idx] = candidates

    doc.close()
    return result


def remove_text_watermarks_fitz(pdf_path: str, out_path: str,
                                 text_findings: dict[int, list[tuple]],
                                 detect_only: bool, aggressive: bool) -> list[str]:
    """
    用 pymupdf redact API 涂抹文字水印。
    返回报告列表。
    """
    report: list[str] = []
    doc = fitz.open(pdf_path)

    for page_idx, candidates in text_findings.items():
        page = doc[page_idx]
        for bbox, text, reason in candidates:
            report.append(f'  页{page_idx+1} [策略3-文字水印] "{text}" ({reason})')
            if not detect_only:
                rect = fitz.Rect(bbox)
                # 用白色涂抹，不留痕迹
                page.add_redact_annot(rect, fill=(1, 1, 1))

        if not detect_only and candidates:
            # apply_redactions: 移除文字层 + 填充背景
            page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE)

    if not detect_only:
        doc.save(out_path, garbage=4, deflate=True)
    doc.close()
    return report


# ─── 主流程 ───────────────────────────────────────────────────────────────────

def run(args: argparse.Namespace) -> None:
    pdf_path = args.input
    if not Path(pdf_path).exists():
        print(f'错误：输入文件不存在: {pdf_path}', file=sys.stderr)
        sys.exit(1)

    out_path = args.outfile or str(Path(pdf_path).with_stem(Path(pdf_path).stem + '_clean'))
    detect_only: bool = args.detect_only
    aggressive: bool = args.aggressive
    method: str = args.method  # all | xobject | alpha | text | image

    # 解析要启用的方法集合
    if method == 'all':
        enabled_xobj_methods = {'xobject', 'alpha', 'image'}
        do_text = True
    elif method == 'xobject':
        enabled_xobj_methods = {'xobject'}
        do_text = False
    elif method == 'alpha':
        enabled_xobj_methods = {'alpha'}
        do_text = False
    elif method == 'image':
        enabled_xobj_methods = {'image'}
        do_text = False
    elif method == 'text':
        enabled_xobj_methods = set()
        do_text = True
    else:
        print(f'未知 method: {method}', file=sys.stderr)
        sys.exit(1)

    print(f'输入: {pdf_path}')
    print(f'模式: {"仅检测" if detect_only else "移除"} | 方法: {method} | 激进: {aggressive}')
    print()

    all_reports: list[str] = []
    watermark_found = False

    # ── XObject 结构分析（策略1/2/4）─────────────────────────────────────────
    if enabled_xobj_methods:
        print('[分析] XObject 结构…')
        xobj_results = analyze_xobjects(pdf_path, aggressive=aggressive)

        any_xobj = any(
            bool(v.get('xobject') or v.get('alpha') or v.get('image_repeat'))
            for v in xobj_results.values()
        )
        if any_xobj:
            watermark_found = True
            print('[发现] XObject 水印候选：')
            tmp_report = remove_xobjects_pypdf(
                pdf_path,
                out_path if not do_text else out_path + '.tmp_xobj.pdf',
                xobj_results,
                enabled_xobj_methods,
                aggressive=aggressive,
                detect_only=detect_only,
            )
            all_reports.extend(tmp_report)
            for line in tmp_report:
                print(line)

            # 如果还要跑文字策略，把 xobj 处理后的临时文件传给下一步
            if do_text and not detect_only:
                xobj_out = out_path + '.tmp_xobj.pdf'
                if Path(xobj_out).exists():
                    pdf_path = xobj_out
        else:
            print('[跳过] 未检测到 XObject 水印')

    # ── 文字水印（策略3）─────────────────────────────────────────────────────
    if do_text:
        print('[分析] 文字水印…')
        text_findings = analyze_text_watermarks(pdf_path)
        if text_findings:
            watermark_found = True
            print('[发现] 文字水印候选：')
            tmp_report = remove_text_watermarks_fitz(
                pdf_path,
                out_path,
                text_findings,
                detect_only=detect_only,
                aggressive=aggressive,
            )
            all_reports.extend(tmp_report)
            for line in tmp_report:
                print(line)
        else:
            print('[跳过] 未检测到文字水印')
            if not detect_only and enabled_xobj_methods:
                # xobj 已写到 out_path，不需再写
                pass
            elif not detect_only:
                import shutil
                shutil.copy2(pdf_path, out_path)

    # 清理临时文件
    tmp_xobj = out_path + '.tmp_xobj.pdf'
    if Path(tmp_xobj).exists():
        Path(tmp_xobj).unlink()

    # ── 汇总报告 ─────────────────────────────────────────────────────────────
    print()
    if not watermark_found:
        print('✅ 未检测到水印。')
    elif detect_only:
        print(f'📋 检测完成，共发现 {len(all_reports)} 处水印候选（仅报告，未修改文件）。')
    else:
        print(f'✅ 水印移除完成，输出：{out_path}')
        print(f'   共处理 {len(all_reports)} 处水印。')

    if not watermark_found and not detect_only:
        # 无水印时输出原始文件副本
        import shutil
        shutil.copy2(args.input, out_path)
        print(f'ℹ️  输出原始文件副本：{out_path}')


# ─── CLI ─────────────────────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog='pdf_remove_watermark.py',
        description=(
            '通用 PDF 水印移除工具\n'
            '支持 4 种策略：\n'
            '  xobject — XObject 字体特征法（覆盖整页的子集字体 Form XObject）\n'
            '  alpha   — 半透明图层法（ExtGState ca/CA < 0.6）\n'
            '  text    — 文字水印（大字号+斜向 / 关键词，pymupdf redact）\n'
            '  image   — 重复图片法（每页相同图片 XObject）\n'
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument('input', help='输入 PDF 路径')
    parser.add_argument('--outfile', '-o', help='输出 PDF 路径（默认：input_clean.pdf）')
    parser.add_argument(
        '--method', '-m',
        choices=['all', 'xobject', 'alpha', 'text', 'image'],
        default='all',
        help='使用的检测方法（默认：all）',
    )
    parser.add_argument(
        '--detect-only', '-d',
        action='store_true',
        help='仅检测，不修改文件',
    )
    parser.add_argument(
        '--aggressive', '-a',
        action='store_true',
        help='激进模式：置信度较低的候选也一并移除',
    )
    return parser


if __name__ == '__main__':
    parser = build_parser()
    args = parser.parse_args()
    run(args)
