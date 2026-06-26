#!/usr/bin/env python3
"""
工具2：论文入库
- fetch_arxiv:      下载 arxiv 论文元数据 + PDF，用 pymupdf 提取全文
- process_pdf:      从本地 PDF 路径提取全文（用于用户上传的 PDF）
- check_duplicate:  检查是否已入库
- save:             写 MD + PDF 到 Gitea，更新 index.json
"""
import sys, json, os, re
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils.gitea_client import GiteaClient
from utils.arxiv_client import ArxivClient

GITEA_URL   = os.environ.get('GITEA_URL', 'http://43.156.243.152:3000')
SYSTEM_REPO = os.environ.get('GITEA_SYSTEM_REPO', 'AIFusionBot/system-config')


# ── PDF 文字提取 ───────────────────────────────────────────────

def extract_pdf_text(pdf_path):
    """用 pymupdf 提取 PDF 全文，返回 (text, page_count, is_scanned)"""
    try:
        import fitz  # pymupdf
    except ImportError:
        return '', 0, False

    try:
        doc = fitz.open(pdf_path)
        pages = []
        for page in doc:
            pages.append(page.get_text())
        full_text = '\n'.join(pages)
        page_count = len(doc)
        doc.close()

        # 判断是否扫描版：全文字符数极少则认为是扫描版
        is_scanned = len(full_text.strip()) < 200
        return full_text, page_count, is_scanned
    except Exception as e:
        return '', 0, False


# ── 辅助 ──────────────────────────────────────────────────────

def load_user_info(gitea, feishu_user_id):
    users, _ = gitea.read_json(SYSTEM_REPO, 'users.json')
    if not users:
        return None
    return users.get('users', {}).get(feishu_user_id)


def load_index(gitea, repo):
    data, sha = gitea.read_json(repo, 'index.json')
    if data is None:
        return {'total': 0, 'last_updated': '', 'papers': []}, None
    return data, sha


def is_duplicate(index, arxiv_id):
    if not arxiv_id:
        return False, None
    for p in index.get('papers', []):
        if p.get('arxiv_id') == arxiv_id:
            return True, p.get('md_path', '')
    return False, None


def slugify(title, n=3):
    words = [w for w in re.findall(r'[a-zA-Z]+', title.lower()) if len(w) > 2]
    return '_'.join(words[:n]) or 'paper'


def make_filename(paper_data):
    year     = paper_data.get('year', 'unknown')
    arxiv_id = paper_data.get('arxiv_id') or ''
    title    = paper_data.get('title', 'untitled')
    slug     = slugify(title)
    if arxiv_id:
        safe = arxiv_id.replace('/', '_')
        return f"{year}_{safe}_{slug}"
    return f"{year}_nondoi_{slug}"


def format_md(p):
    """把 paper_data dict 格式化成完整 MD 字符串"""
    authors_str  = ', '.join(p.get('authors') or []) or 'Unknown'
    keywords_str = ', '.join(p.get('keywords') or [])
    score        = p.get('relevance_score', 'N/A')
    reason       = p.get('relevance_reason', '')
    created_at   = datetime.now().strftime('%Y-%m-%d')

    # 各章节要点
    cs = p.get('chapter_summaries') or {}
    chapter_text = ''
    if isinstance(cs, dict):
        for k, v in cs.items():
            chapter_text += f'\n### {k}\n{v}\n'
    elif isinstance(cs, list):
        for item in cs:
            if isinstance(item, dict):
                chapter_text += f'\n### {item.get("title","")}\n{item.get("summary","")}\n'

    methods_text     = '\n'.join(f'- {m}' for m in (p.get('core_methods') or [])) or '（待补充）'
    conclusions_text = '\n'.join(f'- {c}' for c in (p.get('main_conclusions') or [])) or '（待补充）'

    return f"""# {p.get('title', 'Unknown Title')}

## 基本信息

| 项目 | 内容 |
|------|------|
| 作者 | {authors_str} |
| 年份 | {p.get('year', 'Unknown')} |
| 来源 | {p.get('source_url', '')} |
| arxiv 分类 | {p.get('category', 'other')} |
| 关键词 | {keywords_str} |
| 相关性评分 | {score}/10 — {reason} |
| 入库时间 | {created_at} |

---

## 原文摘要

{(p.get('original_abstract') or '').strip()}

---

## AI 综述

{(p.get('ai_overview') or '').strip()}

---

## 目录结构

{(p.get('table_of_contents') or '').strip()}

---

## 各章节要点
{chapter_text}
---

## 核心方法

{methods_text}

---

## 主要结论

{conclusions_text}
"""


# ── 四个 action ────────────────────────────────────────────────

def action_fetch_arxiv(params):
    arxiv_url = (params.get('arxiv_url') or '').strip()
    if not arxiv_url:
        return {'success': False, 'error': '缺少 arxiv_url'}

    client   = ArxivClient()
    arxiv_id = client.parse_id(arxiv_url)
    if not arxiv_id:
        return {'success': False, 'error': f'无法解析 arxiv ID：{arxiv_url}'}

    # 获取元数据
    meta = client.fetch_metadata(arxiv_id)
    if not meta['success']:
        return meta

    # 下载 PDF
    pdf_path   = f'/tmp/arxiv_{arxiv_id.replace("/", "_")}.pdf'
    pdf_result = client.download_pdf(arxiv_id, pdf_path)

    # 提取全文
    full_text, page_count, is_scanned = '', 0, False
    if pdf_result['success']:
        full_text, page_count, is_scanned = extract_pdf_text(pdf_path)

    return {
        'success':          True,
        'arxiv_id':         arxiv_id,
        'title':            meta['title'],
        'authors':          meta['authors'],
        'year':             meta['year'],
        'original_abstract': meta['abstract'],
        'official_category': meta['category'],
        'source_url':       f'https://arxiv.org/abs/{arxiv_id}',
        'full_text':        full_text,
        'page_count':       page_count,
        'is_scanned':       is_scanned,
        'pdf_saved_path':   pdf_path if pdf_result['success'] else None,
        'pdf_downloaded':   pdf_result['success'],
        'pdf_error':        pdf_result.get('error', '') if not pdf_result['success'] else ''
    }


def action_process_pdf(params):
    pdf_path = (params.get('pdf_path') or '').strip()
    if not pdf_path:
        return {'success': False, 'error': '缺少 pdf_path'}
    if not os.path.exists(pdf_path):
        return {'success': False, 'error': f'文件不存在：{pdf_path}'}

    full_text, page_count, is_scanned = extract_pdf_text(pdf_path)

    if is_scanned:
        return {
            'success':    True,
            'is_scanned': True,
            'full_text':  '',
            'page_count': page_count,
            'message':    '这是扫描版 PDF，无法提取文字'
        }

    return {
        'success':    True,
        'is_scanned': False,
        'full_text':  full_text,
        'page_count': page_count,
        'pdf_path':   pdf_path
    }


def action_check_duplicate(params):
    feishu_user_id = (params.get('feishu_user_id') or '').strip()
    arxiv_id       = (params.get('arxiv_id') or '').strip()

    if not feishu_user_id:
        return {'success': False, 'error': '缺少 feishu_user_id'}
    if not arxiv_id:
        return {'success': True, 'is_duplicate': False}

    gitea     = GiteaClient()
    user_info = load_user_info(gitea, feishu_user_id)
    if not user_info:
        return {'success': False, 'error': '用户未注册'}

    index, _ = load_index(gitea, user_info['repo'])
    dup, existing_path = is_duplicate(index, arxiv_id)

    result = {'success': True, 'is_duplicate': dup}
    if dup and existing_path:
        result['existing_md_path'] = existing_path
        result['existing_md_url']  = f"{GITEA_URL}/{user_info['repo']}/src/branch/main/{existing_path}"
    return result


def action_save(params):
    feishu_user_id = (params.get('feishu_user_id') or '').strip()
    paper_data     = params.get('paper_data') or {}

    if not feishu_user_id:
        return {'success': False, 'error': '缺少 feishu_user_id'}
    if not paper_data.get('title'):
        return {'success': False, 'error': 'paper_data 缺少 title'}

    gitea     = GiteaClient()
    user_info = load_user_info(gitea, feishu_user_id)
    if not user_info:
        return {'success': False, 'error': '用户未注册'}

    repo     = user_info['repo']
    category = paper_data.get('category') or 'other'
    filename = make_filename(paper_data)
    md_path  = f"{category}/{filename}.md"
    arxiv_id = paper_data.get('arxiv_id')

    # 再次查重防止并发
    index, index_sha = load_index(gitea, repo)
    dup, existing = is_duplicate(index, arxiv_id)
    if dup:
        return {
            'success':      False,
            'is_duplicate': True,
            'message':      f'论文已存在：{existing}',
            'existing_md_url': f"{GITEA_URL}/{repo}/src/branch/main/{existing}"
        }

    # 写 MD
    md_content = format_md(paper_data)
    r = gitea.upsert_file(repo, md_path, md_content,
                          f"add: {paper_data['title'][:60]}")
    if not r['success']:
        return {'success': False, 'error': f'MD 提交失败：{r.get("error")}'}

    # 写 PDF（可选）
    has_pdf     = False
    pdf_path_in = paper_data.get('pdf_local_path')

    # 兜底：agent 可能忘传 pdf_local_path，按 arxiv_id 推算标准临时路径
    if not pdf_path_in and arxiv_id:
        candidate = f'/tmp/arxiv_{arxiv_id.replace("/", "_")}.pdf'
        if os.path.exists(candidate):
            pdf_path_in = candidate

    if pdf_path_in and os.path.exists(pdf_path_in):
        pdf_repo_path = f"{category}/{filename}.pdf"
        try:
            with open(pdf_path_in, 'rb') as f:
                pdf_bytes = f.read()
            pr = gitea.upsert_file(repo, pdf_repo_path, pdf_bytes,
                                   f"add pdf: {paper_data['title'][:60]}")
            has_pdf = pr['success']
        except Exception:
            has_pdf = False  # PDF 失败不阻断主流程

    # 更新 index.json
    paper_id = f"{paper_data.get('year','unknown')}_{arxiv_id or filename}"
    index['papers'].append({
        'id':               paper_id,
        'title':            paper_data.get('title', ''),
        'authors':          paper_data.get('authors', []),
        'year':             paper_data.get('year'),
        'arxiv_id':         arxiv_id,
        'source_url':       paper_data.get('source_url', ''),
        'category':         category,
        'keywords':         paper_data.get('keywords', []),
        'abstract_summary': paper_data.get('abstract_summary', ''),
        'relevance_score':  paper_data.get('relevance_score'),
        'md_path':          md_path,
        'has_pdf':          has_pdf,
        'created_at':       datetime.now().strftime('%Y-%m-%d')
    })
    index['total']        = len(index['papers'])
    index['last_updated'] = datetime.now().strftime('%Y-%m-%d')
    gitea.write_json(repo, 'index.json', index,
                     f"index: add {paper_data['title'][:50]}", sha=index_sha)

    md_url = f"{GITEA_URL}/{repo}/src/branch/main/{md_path}"
    return {
        'success':  True,
        'paper_id': paper_id,
        'md_url':   md_url,
        'md_path':  md_path,
        'has_pdf':  has_pdf,
        'category': category
    }


# ── 入口 ──────────────────────────────────────────────────────

def main():
    params = json.loads(sys.stdin.read().strip())
    action = params.get('action', '')
    handlers = {
        'fetch_arxiv':      action_fetch_arxiv,
        'process_pdf':      action_process_pdf,
        'check_duplicate':  action_check_duplicate,
        'save':             action_save,
    }
    handler = handlers.get(action)
    if not handler:
        result = {'success': False, 'error': f'未知 action：{action}'}
    else:
        try:
            result = handler(params)
        except Exception as e:
            result = {'success': False, 'error': str(e)}
    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    main()
