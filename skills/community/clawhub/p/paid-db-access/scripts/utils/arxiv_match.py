#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
arXiv 论文匹配工具
输入：论文标题列表（JSON 或 命令行参数）
输出：匹配到的 arXiv ID 和 PDF 直链

使用方式：
  echo '[{"title":"xxx","authors":"..."},...]' | python arxiv_match.py
  python arxiv_match.py --title "论文标题"
  python arxiv_match.py --batch papers.json --out results.json
"""

import argparse
import json
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path


def search_arxiv(title, paper_doi=None, max_results=3, delay=1.5):
    """按标题在 arXiv 搜索，返回最佳匹配（含 DOI 反向验证）

    Args:
        title: 论文标题（原始来源）
        paper_doi: 论文 DOI（可选，用于反向验证）
        max_results: 最多取几个 arXiv 结果
        delay: API 请求间隔

    Returns:
        dict | None — 匹配结果，含 arxiv_id/pdf_url/match_confidence 等字段
        返回 None = 未找到或验证不通过
    """
    import re
    # 清理标题：去掉特殊字符，截断
    clean = title.strip()
    clean = re.sub(r'[\(\)\[\]]', ' ', clean)
    clean = ' '.join(clean.split()[:15])

    q = urllib.parse.quote(clean[:200])
    url = f'http://export.arxiv.org/api/query?search_query=ti:{q}&max_results={max_results}'

    try:
        time.sleep(delay)
        r = urllib.request.urlopen(url, timeout=20)
        text = r.read().decode('utf-8')
    except Exception as e:
        return {'error': str(e)}

    results = []
    entries = text.split('<entry>')
    for entry in entries[1:]:
        arxiv_id = ''
        found_title = ''
        found_doi = ''
        year = ''
        for line in entry.split('\n'):
            line = line.strip()
            if '<id>' in line and 'arxiv.org/abs/' in line:
                arxiv_url = line.replace('<id>', '').replace('</id>', '')
                arxiv_id = arxiv_url.split('/abs/')[-1]
            if '<title>' in line:
                found_title = line.replace('<title>', '').replace('</title>', '').strip()
            if '<arxiv:doi>' in line:
                found_doi = line.replace('<arxiv:doi>', '').replace('</arxiv:doi>', '').strip().lower()
            if '<published>' in line:
                year = line.replace('<published>', '').replace('</published>', '').strip()[:4]

        if arxiv_id:
            results.append({
                'arxiv_id': arxiv_id,
                'arxiv_url': f'http://arxiv.org/abs/{arxiv_id}',
                'pdf_url': f'http://arxiv.org/pdf/{arxiv_id}.pdf',
                'title': found_title,
                'year': year,
                'doi': found_doi,
            })

    if not results:
        return None

    # ── 标题相似度排序 ──
    scored = []
    orig_words = set(w for w in clean.lower().split() if len(w) > 2)
    for r in results:
        found_words = set(w for w in r['title'].lower().split() if len(w) > 2)
        overlap = len(orig_words & found_words)
        ratio = overlap / max(len(orig_words), 1)
        scored.append((overlap, ratio, r))
    scored.sort(key=lambda x: (x[0], x[1]), reverse=True)
    best_overlap, best_ratio, best = scored[0]

    # ══════════════════════════════════════════════════
    # 🔑 DOI 反向验证（优先于标题置信度判断）
    # ══════════════════════════════════════════════════
    doi_verified = False
    no_doi_available = False

    if paper_doi:
        paper_doi_norm = paper_doi.strip().lower()
        if paper_doi_norm.startswith('http'):
            # 提取纯 DOI 部分
            m = re.search(r'(10\.\S+)', paper_doi_norm)
            if m:
                paper_doi_norm = m.group(1)

        if best['doi']:
            # arXiv 返回了 DOI → 比对
            if paper_doi_norm in best['doi'] or best['doi'] in paper_doi_norm:
                doi_verified = True
            else:
                # DOI 不匹配 → 拒绝
                best['match_confidence'] = 'REJECTED'
                best['match_score'] = f'DOI mismatch: orig={paper_doi_norm} vs arxiv={best["doi"]}'
                best['pdf_url'] = None
                return best
        else:
            # arXiv 没返回 DOI → 无法验证
            no_doi_available = True
    else:
        # 原始论文没有 DOI → 无法验证
        no_doi_available = True

    # ── 决定置信度 ──
    if doi_verified:
        # DOI 验证通过 → 最高置信度
        confidence = 'DOI_VERIFIED'
        best['match_score'] = (f'{best_overlap}/{len(orig_words)} words '
                               f'(DOI verified: {paper_doi_norm})')
    elif no_doi_available:
        # 无法验证 DOI → 降级：不提供 PDF 链接，只标信息
        confidence = 'NO_DOI'
        best['match_score'] = (f'{best_overlap}/{len(orig_words)} words '
                               f'(NO_DOI: cannot verify — use manual download)')
        best['pdf_url'] = None  # 不给 PDF 链接！用户需手动下载
    else:
        # 仅标题匹配（兼容旧逻辑，理论上不应走到这）
        if best_overlap >= 6 and best_ratio >= 0.5:
            confidence = 'HIGH'
        elif best_overlap >= 4 and best_ratio >= 0.4:
            confidence = 'MEDIUM'
        else:
            confidence = 'LOW'
        best['match_score'] = f'{best_overlap}/{len(orig_words)} words ({confidence})'

    best['match_confidence'] = confidence
    best['matched_title'] = best.get('title', '')
    best['doi_verified'] = doi_verified

    # LOW 也不提供 PDF
    if confidence == 'LOW':
        best['pdf_url'] = None

    return best


def batch_match(papers, delay=1.5):
    """批量匹配论文（含 DOI 反向验证）"""
    results = []
    total = len(papers)
    verified = 0
    rejected = 0
    no_doi = 0

    for i, paper in enumerate(papers):
        title = paper.get('title', '')
        paper_doi = paper.get('doi', '')
        if not title:
            results.append({**paper, 'arxiv': None, 'note': 'no title'})
            continue

        print(f'  [{i+1}/{total}] {title[:60]}...', end=' ', flush=True)
        match = search_arxiv(title, paper_doi=paper_doi, delay=delay)

        if match and 'error' not in match:
            conf = match.get('match_confidence', '?')
            match_title = match.pop('matched_title', '')
            match_score = match.pop('match_score', '?')
            doi_ok = match.pop('doi_verified', False)
            paper['arxiv'] = match

            if conf == 'DOI_VERIFIED':
                paper['arxiv_pdf'] = match['pdf_url']
                paper['note'] = f'arxiv DOI verified ✅ ({match_score})'
                verified += 1
                print(f'DOI_VERIFIED ✅')
            elif conf == 'NO_DOI':
                paper['arxiv_pdf'] = None
                paper['warning'] = (f'NO_DOI: cannot verify arXiv match. '
                                    f'arXiv title: {match_title[:100]}. '
                                    f'Fall back to manual download.')
                paper['note'] = f'no DOI verification possible — use manual download'
                no_doi += 1
                print(f'NO_DOI ⚠️  (manual download)')
            elif conf == 'REJECTED':
                paper['arxiv_pdf'] = None
                paper['warning'] = f'DOI mismatch rejected ❌. {match_score}'
                paper['note'] = 'arxiv DOI mismatch — rejected'
                rejected += 1
                print(f'REJECTED ❌')
            elif conf == 'LOW':
                paper['arxiv_pdf'] = None
                paper['warning'] = f'Low confidence match. arXiv: {match_title[:100]}'
                paper['note'] = f'low title match — rejected'
                print(f'LOW ❌')
            else:
                # HIGH/MEDIUM without DOI (legacy, should be rare)
                print(f'{conf} (legacy, no DOI verification)')
        else:
            paper['arxiv'] = None
            paper['arxiv_pdf'] = None
            paper['note'] = 'no arxiv version found'
            print('NOT FOUND')

        results.append(paper)

    print(f'\n  Verified: {verified} | No DOI: {no_doi} | Rejected: {rejected} | Total: {total}')
    return results


def main():
    parser = argparse.ArgumentParser(description='按标题匹配 arXiv 论文')
    parser.add_argument('--title', help='单个论文标题')
    parser.add_argument('--batch', help='批量输入 JSON 文件路径')
    parser.add_argument('--out', help='输出 JSON 文件路径')
    parser.add_argument('--delay', type=float, default=1.5,
                       help='请求间隔秒数 (默认 1.5)')
    args = parser.parse_args()

    # 单个标题匹配
    if args.title:
        result = search_arxiv(args.title, delay=args.delay)
        if result:
            if 'error' in result:
                print(json.dumps(result, indent=2, ensure_ascii=False))
            else:
                print(f"Title: {args.title}")
                print(f"arXiv ID: {result['arxiv_id']}")
                print(f"arXiv URL: {result['arxiv_url']}")
                print(f"PDF: {result['pdf_url']}")
                print(f"Match: {result.get('match_score', '?')}")
        else:
            print("No match found on arXiv.")
        return

    # 批量匹配
    papers = []
    if args.batch:
        with open(args.batch, 'r', encoding='utf-8') as f:
            papers = json.load(f)
    else:
        # 从 stdin 读取
        raw = sys.stdin.read().strip()
        if raw:
            papers = json.loads(raw)

    if not papers:
        print("[WARN] No papers to match. Pipe JSON array or use --batch.")
        print("  Example: echo '[{\"title\":\"...\"}]' | python arxiv_match.py")
        return

    print(f"\nMatching {len(papers)} papers against arXiv...\n")
    results = batch_match(papers, delay=args.delay)

    found = sum(1 for p in results if p.get('arxiv'))
    print(f"\n=== Done: {found}/{len(results)} papers matched on arXiv ===\n")

    if args.out:
        with open(args.out, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"Saved to {args.out}")

    # 汇总
    for i, p in enumerate(results):
        if p.get('arxiv_pdf'):
            print(f"  [{i+1}] {p['note']}")
            print(f"       PDF: {p['arxiv_pdf']}")
        elif p.get('warning'):
            print(f"  [{i+1}] [WARN] {p['warning']}")
        else:
            print(f"  [{i+1}] {p['note']} - {p.get('title', '?')[:60]}")


if __name__ == '__main__':
    main()
