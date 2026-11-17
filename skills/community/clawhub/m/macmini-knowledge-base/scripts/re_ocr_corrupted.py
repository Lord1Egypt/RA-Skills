#!/usr/bin/env python3
"""
重新 OCR 已识别的乱码 PDF，覆盖 summaries/ 和 archives/

用法：
  python3 re_ocr_corrupted.py [--dry-run] [--max N]

行为：
1. 接收 PDF 路径列表（按乱码字符数排序的前 N 个）
2. 对每份跑 extract_pdf_text（自动 CMap 自检 + 强制 OCR）
3. 生成新 summary 写入 summaries/（新时间戳）
4. 把 archives/ 里对应 basename **且确实是乱码**的版本覆盖
   （v1.4.11 起：glob 转义 + 逐个校验 + 覆盖前备份到 archives/.bak/）
5. 报告每份结果（含路径、字数、是否成功）
"""
import os, sys, glob, re, time, json, shutil
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils import extract_pdf_text, is_cmap_broken, PDFExtractError, load_summary_index

KNOWLEDGE = os.path.expanduser('~/.openclaw/workspace/knowledge')
SUMMARIES = os.path.join(KNOWLEDGE, '.analysis/summaries')
ARCHIVES = os.path.join(KNOWLEDGE, '.analysis/summaries/archives')
TIMESTAMP = datetime.now().strftime('%Y%m%d_%H%M%S')


def corrupted_char_count(text):
    """统计文本里的乱码特征字符数（PUA / CJK 扩展区 / CJK 兼容区 / (cid: 标记）"""
    pua = sum(1 for c in text if 0xE000 <= ord(c) <= 0xF8FF)
    cjk_ext = sum(1 for c in text if 0x20000 <= ord(c) <= 0x2EBEF)
    cjk_compat = sum(1 for c in text if 0xF900 <= ord(c) <= 0xFAFF)
    cid = text.count('(cid:')
    return pua + cjk_ext + cjk_compat + cid


def is_corrupted_text(text):
    """文本是否含乱码特征 —— 覆盖归档前用于逐个校验目标是否真需要修复"""
    return corrupted_char_count(text) > 0


def find_corrupted_summaries():
    """扫描 archives/ 找出所有乱码 summary（已在 Step 1 用过的逻辑）"""
    files = glob.glob(f'{ARCHIVES}/*.summary.txt')
    bad = []
    for f in files:
        with open(f, encoding='utf-8', errors='replace') as fh:
            text = fh.read()
        bad_count = corrupted_char_count(text)
        if bad_count > 0:
            bad.append({'path': f, 'bad_count': bad_count, 'text_len': len(text)})
    return sorted(bad, key=lambda x: -x['bad_count'])


def within_knowledge(abs_path, knowledge_dir=None):
    """路径是否真在 knowledge/ 之内（realpath 消解符号链接后判定）。

    2026-11-06：ClawHub 扫描器指出 glob(recursive=True) 会跟随指向外部的
    符号链接 → 外部文件会进入分析队列并被推送飞书。
    """
    root = os.path.realpath(knowledge_dir or KNOWLEDGE)
    try:
        cand = os.path.realpath(abs_path)
    except (OSError, ValueError):
        return False
    return cand == root or cand.startswith(root + os.sep)


def resolve_in_knowledge(path):
    """把路径解析为 knowledge/ 内的绝对路径；越界返回 None。

    安全约束（2026-11-06 补）：
      ClawHub 扫描器指出「OCR repair can copy unrelated private documents into
      summaries that may later be sent to Feishu」。本函数是唯一的入口闸门：
        - realpath 消解符号链接与 ../
        - 绝对路径 / ../ 越界一律拒绝
        - 必须在 KNOWLEDGE 之内
    """
    if not path:
        return None
    try:
        root = os.path.realpath(KNOWLEDGE)
        cand = os.path.realpath(os.path.join(root, path))
    except (OSError, ValueError):
        return None
    if cand == root or cand.startswith(root + os.sep):
        return cand
    return None


def summary_to_pdf_basename(s_fname):
    """从 summary 文件名提取原 PDF 的 basename（不含扩展名）"""
    base = os.path.basename(s_fname)
    base = re.sub(r'^\d{8}_\d{6}_', '', base)
    base = re.sub(r'^[0-9a-f]{8}_', '', base)   # v1.4.12 起的路径哈希前缀
    base = re.sub(r'\.summary\.txt$', '', base)
    # 去掉扩展名（.pdf / .pptx 等），让 find_pdf_by_basename 自己加
    base = re.sub(r'\.(pdf|pptx|docx|doc|ppt)$', '', base, flags=re.IGNORECASE)
    return base


def find_pdf_by_basename(target_bn):
    """在 knowledge/ 下找对应 basename 的 PDF/PPTX/DOCX（兜底路径）

    ⚠️ basename 不唯一：不同目录下可能有同名文档（实测 104 组 / 106 份被顶替）。
    本函数只作为兜底，优先走 find_source_for_summary()。
    """
    for ext in ['.pdf', '.pptx', '.docx', '.doc', '.ppt']:
        candidates = glob.glob(f'{KNOWLEDGE}/**/{glob.escape(target_bn)}{ext}', recursive=True)
        # 符号链接防线：glob(recursive=True) 会跟随指向外部的目录链接
        for c in candidates:
            if within_knowledge(c, KNOWLEDGE):
                return c
    return None


def find_source_for_summary(summary_path):
    """定位某份 summary 对应的源文档。

    优先级：
      1. summary_index.json（summary 文件名 → 源文件相对路径）→ 精确命中
      2. summary 正文里的 source_path
      3. basename 兜底（可能命中同名文档中的任意一份，仅在无法判定时使用）
    """
    # 1) 持久化索引
    try:
        rel = load_summary_index().get(os.path.basename(summary_path))
        if rel:
            for ext in ['', '.pdf', '.pptx', '.docx', '.doc', '.ppt']:
                relname = rel if rel.lower().endswith(
                    ('.pdf', '.pptx', '.docx', '.doc', '.ppt')) else rel + ext
                cand = resolve_in_knowledge(relname)
                if cand and os.path.isfile(cand):
                    return cand
    except Exception:
        pass
    # 2) summary 正文里的源路径
    try:
        with open(summary_path, encoding='utf-8', errors='replace') as fh:
            head = fh.read(2000)
        m = re.search(r'source_path:\s*"([^"]+)"', head)
        if m:
            cand = resolve_in_knowledge(m.group(1))
            if cand and os.path.isfile(cand):
                return cand
    except Exception:
        pass
    # 3) basename 兜底
    bn = summary_to_pdf_basename(summary_path)
    return find_pdf_by_basename(bn) if bn else None


def re_ocr_one(pdf_path, dry_run=False):
    """对一份 PDF 重新 OCR，返回结果"""
    # 纵深防御：任何进入本函数的路径必须落在 knowledge/ 之内
    safe_path = resolve_in_knowledge(pdf_path)
    if safe_path is None:
        return {
            'pdf_path': pdf_path, 'basename': os.path.basename(pdf_path),
            'success': False, 'new_text_len': 0, 'summaries_updated': 0,
            'archives_updated': 0, 'archives_skipped': 0,
            'error': '路径越界：仅允许处理 knowledge/ 内的文件', 'elapsed': 0,
        }
    pdf_path = safe_path
    bn = os.path.basename(pdf_path)
    result = {
        'pdf_path': pdf_path,
        'basename': bn,
        'success': False,
        'new_text_len': 0,
        'summaries_updated': 0,
        'archives_updated': 0,
        'archives_skipped': 0,
        'error': None,
        'elapsed': 0,
    }
    
    t0 = time.time()
    try:
        text = extract_pdf_text(pdf_path)
        result['new_text_len'] = len(text)
        result['success'] = True
        result['text_still_broken'] = is_cmap_broken(text)
    except PDFExtractError as e:
        result['error'] = f"PDFExtractError: {e.reason}"
        result['elapsed'] = time.time() - t0
        return result
    except Exception as e:
        result['error'] = f"{type(e).__name__}: {e}"
        result['elapsed'] = time.time() - t0
        return result
    
    result['elapsed'] = time.time() - t0
    
    if dry_run:
        return result
    
    # ── 覆盖前校验（v1.4.11）────────────────────────────────────────
    # 替换文本必须有效：非空 且 不再是乱码。否则拒绝写入与覆盖。
    if not text.strip():
        result['error'] = 'OCR 结果为空，拒绝写入/覆盖'
        result['elapsed'] = time.time() - t0
        return result
    if result.get('text_still_broken'):
        result['error'] = 'OCR 结果仍然乱码，拒绝写入/覆盖'
        result['elapsed'] = time.time() - t0
        return result

    # 1. 写入新的 summary 到 summaries/
    new_summary_path = f'{SUMMARIES}/{TIMESTAMP}_{bn}.summary.txt'
    with open(new_summary_path, 'w', encoding='utf-8') as f:
        f.write(text)
    result['summaries_updated'] = 1
    result['new_summary_path'] = new_summary_path
    
    # 2. 覆盖 archives/ 里对应 basename 的乱码版本
    #    安全约束（v1.4.11）：
    #    - glob.escape(basename)：文件名里的 [ ] * ? 不再扩大匹配范围
    #    - 逐个校验目标确实是乱码 → 健康的归档一律跳过，不覆盖
    #    - 覆盖前先备份到 archives/.bak/，出错可回滚
    pattern = os.path.join(ARCHIVES, '*_' + glob.escape(bn) + '.summary.txt')
    archives_matched = sorted(glob.glob(pattern))
    backup_dir = os.path.join(ARCHIVES, '.bak')
    for arch_path in archives_matched:
        with open(arch_path, encoding='utf-8', errors='replace') as fh:
            existing = fh.read()
        if not is_corrupted_text(existing):
            print(f"[跳过] 归档并非乱码，不覆盖: {os.path.basename(arch_path)}", file=sys.stderr)
            result['archives_skipped'] += 1
            continue
        os.makedirs(backup_dir, exist_ok=True)
        shutil.copy2(arch_path, os.path.join(backup_dir, os.path.basename(arch_path)))
        with open(arch_path, 'w', encoding='utf-8') as f:
            f.write(text)
        result['archives_updated'] += 1
    
    return result


def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('--dry-run', action='store_true')
    p.add_argument('--max', type=int, default=5, help='最多处理前 N 个乱码 summary')
    p.add_argument('--pdf-list', help='指定 PDF 路径列表（逗号分隔），跳过自动扫描')
    args = p.parse_args()
    
    print(f"🔍 扫描 archives/ 中的乱码 summary...")
    corrupted = find_corrupted_summaries()
    print(f"📊 发现 {len(corrupted)} 个乱码 summary")
    
    if args.pdf_list:
        pdf_list = []
        rejected = []
        for raw in args.pdf_list.split(','):
            raw = raw.strip()
            if not raw:
                continue
            safe = resolve_in_knowledge(raw)
            if safe is None:
                rejected.append(raw)
            else:
                pdf_list.append(safe)
        if rejected:
            print(f"⛔ 拒绝 {len(rejected)} 个 knowledge/ 之外的路径（安全约束）：",
                  file=sys.stderr)
            for r in rejected[:5]:
                print(f"   - {r}", file=sys.stderr)
    else:
        # 找到每份乱码对应的 PDF，去重
        seen_pdfs = set()
        pdf_list = []
        for c in corrupted:
            pdf = find_source_for_summary(c['path'])
            if pdf and pdf not in seen_pdfs:
                seen_pdfs.add(pdf)
                pdf_list.append(pdf)
            if len(pdf_list) >= args.max:
                break
    
    print(f"\n📋 将处理 {len(pdf_list)} 份 PDF:")
    for p in pdf_list:
        rel = p.replace(KNOWLEDGE + '/', '')
        if len(rel) > 60: rel = '...' + rel[-57:]
        print(f"  - {rel}")
    
    print(f"\n{'='*80}")
    print(f"🚀 开始{'DRY-RUN' if args.dry_run else '实际执行'}")
    print(f"{'='*80}")
    
    results = []
    for i, pdf_path in enumerate(pdf_list, 1):
        print(f"\n[{i}/{len(pdf_list)}] {os.path.basename(pdf_path)[:60]}")
        r = re_ocr_one(pdf_path, dry_run=args.dry_run)
        results.append(r)
        
        if r['success']:
            status = "✅"
            warn = " ⚠️ 文本仍异常" if r.get('text_still_broken') else ""
            print(f"   {status} {r['elapsed']:.1f}s, 文本 {r['new_text_len']:,} 字{warn}")
            if not args.dry_run:
                print(f"   📝 summaries/: +1")
                print(f"   📝 archives/: {r['archives_updated']} 个被覆盖")
        else:
            print(f"   ❌ 失败: {r['error']}")
    
    print(f"\n{'='*80}")
    print(f"📊 最终报告")
    print(f"{'='*80}")
    success_count = sum(1 for r in results if r['success'])
    fail_count = len(results) - success_count
    
    print(f"\n总处理: {len(results)} 个 PDF")
    print(f"  ✅ 成功: {success_count}")
    print(f"  ❌ 失败: {fail_count}")
    
    if fail_count > 0:
        print(f"\n❌ 失败的文件（需要人工处理）：")
        for r in results:
            if not r['success']:
                print(f"  - {r['pdf_path']}")
                print(f"    原因: {r['error']}")
    
    total_summaries = sum(r['summaries_updated'] for r in results)
    total_archives = sum(r['archives_updated'] for r in results)
    print(f"\n📝 文件更新：")
    print(f"  summaries/ 新增: {total_summaries}")
    print(f"  archives/ 覆盖: {total_archives}")
    
    # 输出 JSON 报告
    report_path = f'{KNOWLEDGE}/.analysis/re_ocr_report_{TIMESTAMP}.json'
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\n📄 详细报告: {report_path}")
    
    return 0 if fail_count == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
