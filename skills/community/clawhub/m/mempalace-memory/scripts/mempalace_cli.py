#!/usr/bin/env python3
"""
MemPalace Enhanced CLI Wrapper v5 - 第一性原则重构
================================================
核心理念:个人AI助手记忆系统 = 确定性召回 > 多样性探索

与v4的本质区别:
- v4: MMR 默认开启,以多样性为代价换取召回广度
- v5: MMR 默认为关闭,以精确召回为核心,按需启用
- v5: 中文关键词boost + identity优先注入
- v5: 存储前凭证检测

设计原则(第一性):
1. 相关性 100% 优先:mempalace 原生排序就是最优的,不打乱
2. 中文硬匹配优先:BM25/关键词 > 向量语义(中文嵌入质量有限)
3. Identity 永远在上下文里:USER.md/SOUL.md 优先注入
4. 安全不可妥协:凭证在存储前拦截,不依赖后处理
"""
import sys
import os
import json
import argparse
import re
import time

MEMPALACE_CLI = '/Users/mars/Library/Python/3.9/bin/mempalace'
WORKSPACE = os.path.expanduser('~/.openclaw/workspace')

# ─────────────────────────────────────────────────────────────────
# IDENTITY PRIORITY FILES - 第一性原则:这些文件永远优先
# ─────────────────────────────────────────────────────────────────
IDENTITY_FILES = {
    'USER.md', 'SOUL.md', 'MEMORY.md', 'AGENTS.md', 'HEARTBEAT.md',
    'BOOTSTRAP.md', 'IDENTITY.md', 'TOOLS.md', 'SOUL.md',
}
# Boost权重:USER.md 最高,其他 identity 文件次之
IDENTITY_BOOST = {
    'USER.md': 100.0,   # 最优先:关于城的核心信息
    'SOUL.md': 50.0,    # 次优先:我的灵魂定义
    'MEMORY.md': 30.0,  # 长期记忆摘要
    'AGENTS.md': 10.0,  # 工作区定义
    'HEARTBEAT.md': 5.0, # 心跳任务
}

def call_mempalace(args, timeout=30):
    """Call mempalace CLI directly."""
    import subprocess
    env = os.environ.copy()
    env['PATH'] = f'/Users/mars/Library/Python/3.9/bin:{env.get("PATH", "")}'
    result = subprocess.run(
        [MEMPALACE_CLI] + args,
        capture_output=True, text=True, timeout=timeout,
        env=env
    )
    return result.stdout, result.stderr, result.returncode


# ─────────────────────────────────────────────────────────────────
# 1. PARSE - correctly split individual [N] results
# ─────────────────────────────────────────────────────────────────

def parse_search_output(output: str, query: str = '') -> list:
    """Parse mempalace CLI markdown output into structured results."""
    results = []
    blocks = re.split(r'\n\s*─{5,}\s*\n', output)
    for block in blocks:
        block = block.strip()
        if not block:
            continue
        if re.match(r'\[\d+\]', block):
            result = _extract_result(block)
            if result:
                results.append(result)
            continue
        first_result_start = block.find('[1]')
        if first_result_start != -1:
            first_block = block[first_result_start:]
            result = _extract_result(first_block)
            if result:
                results.append(result)
    return results


def _extract_result(block: str) -> dict:
    """Extract source, score, and content from a result block."""
    header_match = re.match(r'\[(\d+)\]\s+(\S+)\s+/\s+(\S+)', block)
    if not header_match:
        return None
    source_match = re.search(r'Source:\s*(.+?)(?:\n|$)', block)
    match_score_match = re.search(r'Match:\s*([-\d.]+)', block)
    source = source_match.group(1).strip() if source_match else ''
    raw_score = float(match_score_match.group(1)) if match_score_match else 0.0
    match_pos = block.find('Match:')
    if match_pos == -1:
        return {
            'content': block[header_match.end():].strip(),
            'score': raw_score,
            'source': source,
            'match_score': raw_score
        }
    line_end = block.find('\n', match_pos)
    blank = block.find('\n\n', line_end)
    content = block[blank + 2:].strip() if blank != -1 else block[line_end + 1:].strip()
    return {
        'content': content,
        'score': raw_score,
        'source': source,
        'match_score': raw_score
    }


# ─────────────────────────────────────────────────────────────────
# 2. CHINESE KEYWORD BOOST - 解决中文嵌入质量问题
# ─────────────────────────────────────────────────────────────────

def is_chinese_text(text: str) -> bool:
    """检测文本是否包含中文(用于判断是否使用关键词boost)。"""
    return bool(re.search(r'[\u4e00-\u9fff]', text))

def extract_chinese_tokens(text: str, min_len: int = 2) -> set:
    """提取中文bigram tokens(中文分词)。"""
    tokens = set()
    for i in range(len(text) - 1):
        c1, c2 = text[i], text[i+1]
        if '\u4e00' <= c1 <= '\u9fff' and '\u4e00' <= c2 <= '\u9fff':
            tokens.add(text[i:i+2])
    # 也提取英文词
    for w in re.findall(r'[a-zA-Z0-9]{2,}', text):
        tokens.add(w.lower())
    return tokens

def keyword_boost_score(content: str, query: str) -> float:
    """
    中文关键词匹配得分。
    如果内容包含查询的所有中文bigram,给 +0.5 boost。
    如果部分包含,按比例给分。
    """
    if not is_chinese_text(query):
        return 0.0

    query_tokens = extract_chinese_tokens(query)
    if not query_tokens:
        return 0.0

    content_tokens = extract_chinese_tokens(content)
    if not content_tokens:
        return 0.0

    overlap = len(query_tokens & content_tokens)
    ratio = overlap / len(query_tokens)

    # 全匹配给 +0.5 boost(相当于一个 top-1 结果的分数差距)
    # 部分匹配按比例
    return 0.5 * ratio


# ─────────────────────────────────────────────────────────────────
# 3. IDENTITY BOOST - 第一性:城的信息永远优先
# ─────────────────────────────────────────────────────────────────

def identity_boost_score(source: str, content: str, query: str) -> float:
    """
    根据source文件的重要性给予额外boost。
    第一性原则:USER.md/SOUL.md 是关于城的核心定义,必须优先于其他任何文档。
    """
    basename = source.split('/')[-1].split('\\')[-1]

    # 文件名直接匹配
    if basename in IDENTITY_BOOST:
        return IDENTITY_BOOST[basename]

    # 如果查询包含"城"且content包含城的定义,给予boost
    if '城' in query and '城' in content and basename in IDENTITY_FILES:
        return 20.0

    return 0.0


# ─────────────────────────────────────────────────────────────────
# 4. DEDUP - same-source dedup + Levenshtein
# ─────────────────────────────────────────────────────────────────

def dedup_results(results, threshold=0.85):
    """Same-source dedup → keep highest score per source, then Levenshtein dedup."""
    if not results:
        return []

    def levenshtein(s1, s2):
        if len(s1) < len(s2):
            return levenshtein(s2, s1)
        if len(s2) == 0:
            return len(s1)
        prev = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            curr = [i + 1]
            for j, c2 in enumerate(s2):
                curr.append(min(prev[j + 1] + 1, curr[j] + 1, prev[j] + (c1 != c2)))
            prev = curr
        return prev[-1]

    def similarity(s1, s2):
        s1 = s1.lower(); s2 = s2.lower()
        max_len = max(len(s1), len(s2))
        if max_len == 0:
            return 1.0
        return 1.0 - (levenshtein(s1, s2) / max_len)

    # Step 1: keep highest-scoring result per source
    by_source = {}
    for r in results:
        src = r.get('source', '')
        if src not in by_source or r.get('score', 0) > by_source[src].get('score', 0):
            by_source[src] = r

    # Step 2: Levenshtein dedup
    deduped = []
    for r in by_source.values():
        content = r.get('content', '')
        is_dup = any(similarity(content, e.get('content', '')) > threshold for e in deduped)
        if not is_dup:
            deduped.append(r)

    return deduped


# ─────────────────────────────────────────────────────────────────
# 5. MMR - Optional diversity reranking (NOT default)
# ─────────────────────────────────────────────────────────────────

def mmr_rerank(results, query, lambda_param=0.7, limit=5):
    """MMR diversity reranking - only when explicitly requested."""
    if not results or len(results) <= limit:
        return results

    def levenshtein(s1, s2):
        if len(s1) < len(s2):
            return levenshtein(s2, s1)
        if len(s2) == 0:
            return len(s1)
        prev = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            curr = [i + 1]
            for j, c2 in enumerate(s2):
                curr.append(min(prev[j + 1] + 1, curr[j] + 1, prev[j] + (c1 != c2)))
            prev = curr
        return prev[-1]

    def similarity(s1, s2):
        s1 = s1.lower(); s2 = s2.lower()
        max_len = max(len(s1), len(s2))
        if max_len == 0:
            return 1.0
        return 1.0 - (levenshtein(s1, s2) / max_len)

    selected = []
    remaining = list(results)
    max_s = max((r.get('score', 0) for r in remaining), default=1)
    min_s = min((r.get('score', 0) for r in remaining), default=0)
    score_range = max_s - min_s if max_s != min_s else 1.0

    def norm(r):
        return (r.get('score', 0) - min_s) / score_range

    while len(selected) < limit and remaining:
        best_score = -float('inf')
        best_item, best_idx = None, -1
        for idx, item in enumerate(remaining):
            relevance = norm(item)
            max_sim = max((similarity(item.get('content', ''), s.get('content', '')) for s in selected), default=0)
            diversity = 1.0 - max_sim
            mmr_score = lambda_param * relevance + (1 - lambda_param) * diversity
            if mmr_score > best_score:
                best_score, best_item, best_idx = mmr_score, item, idx
        if best_item is not None:
            selected.append(best_item)
            remaining.pop(best_idx)
        else:
            break
    return selected


# ─────────────────────────────────────────────────────────────────
# 6. STRIP - remove OpenClaw metadata
# ─────────────────────────────────────────────────────────────────

STRIP_PATTERNS = [
    (r'^\[message_id:\s*[^\]]+\]\s*', ''),
    (r'^Sender\s*\(untrusted metadata\):\s*```json\s*\n[\s\S]*?```\s*\n', ''),
    (r'^```json\s*\n[\s\S]*?```\s*\n', ''),
    (r'^\[user:ou_[^\]]+\]\s*', ''),
    (r'^Conversation info[\s\S]*?```\s*\n', ''),
    (r'^```\w*\s*\n', ''),
]

def strip_metadata(text: str) -> str:
    for pat, repl in STRIP_PATTERNS:
        text = re.sub(pat, repl, text, flags=re.MULTILINE)
    return text.strip()


# ─────────────────────────────────────────────────────────────────
# 7. CREDENTIAL FILTER
# ─────────────────────────────────────────────────────────────────

_CRED_PATTERNS = [
    (r'ghp_[a-zA-Z0-9]{36}', '[GITHUB_TOKEN]'),
    (r'gho_[a-zA-Z0-9]{36}', '[GITHUB_TOKEN]'),
    (r'github_pat_[a-zA-Z0-9_]{22,}', '[GITHUB_TOKEN]'),
    (r'(?<!\d)mars\d{5,}(?!\d)', '[PASSWORD]'),
    (r'(?<!\d)Mars\d{5,}(?!\d)', '[PASSWORD]'),
]
_CRED_BLOCK_PATTERNS = [
    r'ghp_[a-zA-Z0-9]{36}', r'gho_[a-zA-Z0-9]{36}',
    r'(?<!\d)mars\d{5,}(?!\d)', r'(?<!\d)Mars\d{5,}(?!\d)',
    r'(?i)(?:password|passwd|pwd|密码|secret|api_?key|token)\s*[:=]\s*[a-zA-Z0-9_\-]{4,}',
]

def filter_credentials(content: str) -> str:
    for pat, repl in _CRED_PATTERNS:
        content = re.sub(pat, repl, content)
    return content

def has_plaintext_credential(content: str) -> bool:
    for pat in _CRED_BLOCK_PATTERNS:
        if re.search(pat, content, re.IGNORECASE):
            return True
    return False


# ─────────────────────────────────────────────────────────────────
# 8. COMMANDS - v5 重构
# ─────────────────────────────────────────────────────────────────

def cmd_search(query, limit=5, use_mmr=False, dedup=True, strip=True):
    """
    v5 核心搜索逻辑:
    1. mempalace 原生检索
    2. strip + credential_filter
    3. 同源去重
    4. 中文关键词boost
    5. Identity优先boost
    6. 最终排序(原生分数 + boosts)
    7. MMR(可选,默认关闭)
    """
    t0 = time.time()
    out, err, code = call_mempalace(['search', query, '--results', str(limit * 3)])

    if code != 0:
        return {'status': 'error', 'error': err}

    results = parse_search_output(out, query)
    if not results:
        return {'status': 'ok', 'query': query, 'results': [], 'steps': ['parse_error']}

    steps = ['mempalace_native']

    # Strip metadata
    if strip:
        for r in results:
            r['content'] = strip_metadata(r['content'])
        steps.append('strip')

    # Credential filter
    for r in results:
        r['content'] = filter_credentials(r['content'])
    steps.append('credential_filter')

    # Deduplicate
    before_dedup = len(results)
    if dedup:
        results = dedup_results(results)
        steps.append(f'dedup({before_dedup}→{len(results)})')

    # ── 第一性原则核心:精确召回,不打乱原生排序 ──
    # 计算最终得分 = mempalace原生分数 + identity_boost + keyword_boost
    for r in results:
        identity_boost = identity_boost_score(r['source'], r['content'], query)
        kw_boost = keyword_boost_score(r['content'], query) if is_chinese_text(query) else 0.0
        r['_identity_boost'] = identity_boost
        r['_kw_boost'] = kw_boost
        r['final_score'] = r['score'] + identity_boost + kw_boost

    # 按最终得分排序(不打乱原生排序,只做微调)
    results = sorted(results, key=lambda x: x.get('final_score', 0), reverse=True)
    steps.append('identity_kw_boost')

    # MMR(可选,默认关闭)
    before_mmr = len(results)
    if use_mmr:
        results = mmr_rerank(results, query, lambda_param=0.7, limit=limit)
        steps.append(f'mmr({before_mmr}→{len(results)})')
    else:
        results = results[:limit]
        steps.append(f'top({len(results)})')

    elapsed_ms = round((time.time() - t0) * 1000)

    return {
        'status': 'ok',
        'query': query,
        'steps': steps,
        'elapsed_ms': elapsed_ms,
        'results': [
            {
                'content': r['content'],
                'score': round(r['score'], 4),
                'final_score': round(r['final_score'], 4),
                'source': r.get('source', '?'),
                'match_score': round(r.get('match_score', 0), 3),
                '_boosts': {
                    'identity': r.get('_identity_boost', 0),
                    'keyword': r.get('_kw_boost', 0)
                }
            }
            for r in results[:limit]
        ]
    }


def cmd_remember(content: str, agent: str = 'main', room: str = 'general', source: str = ''):
    """
    存储记忆（带凭证检测）。
    第一性原则：在凭证写入存储前拦截。
    - 如果原始内容包含凭证：直接拒绝（fail-secure）
    - 如果必须过滤后存储：警告 + 过滤存储
    """
    # 前置检查：凭证检测
    if has_plaintext_credential(content):
        filtered = filter_credentials(content)
        # 过滤后仍检测到凭证 = 无法安全处理，拒绝
        if has_plaintext_credential(filtered):
            return {
                'status': 'error',
                'error': 'CREDENTIAL_DETECTED',
                'message': '内容包含无法过滤的明文凭证，拒绝存储',
                'hint': '凭证应加密存储在 ~/.openclaw/.credentials，content中不应出现明文'
            }
        # 过滤生效：警告但仍存储（凭证部分被替换）
        clean_content = filtered
        warn = '⚠️ 凭证已过滤，请勿在内容中直接包含密码/token'
    else:
        clean_content = content
        warn = None

    # 调用 super_mem_cli.py store
    try:
        import subprocess
        env = os.environ.copy()
        env['PATH'] = f'/Users/mars/Library/Python/3.9/bin:{env.get("PATH", "")}'
        r = subprocess.run(
            ['/usr/bin/python3',
             '/Users/mars/.openclaw/workspace/skills/mempalace-memory/scripts/super_mem_cli.py',
             'remember', clean_content,
             '--agent', agent, '--room', room, '--source', source],
            capture_output=True, text=True, timeout=15, env=env
        )
        if r.returncode == 0:
            try:
                result = json.loads(r.stdout)
                if warn:
                    result['warning'] = warn
                return result
            except:
                return {'status': 'ok', 'action': 'remember', 'content_preview': clean_content[:80], 'warning': warn}
        else:
            return {'status': 'error', 'error': r.stderr[:200]}
    except Exception as e:
        return {'status': 'error', 'error': str(e)}


def cmd_wake_up():
    """唤醒:返回完整上下文(L0 identity + L1 essential story)。"""
    out, err, code = call_mempalace(['wake-up'], timeout=30)
    if code == 0:
        return {'status': 'ok', 'context': out}
    return {'status': 'error', 'error': err}


def cmd_status():
    """健康检查。"""
    out, err, code = call_mempalace(['status'], timeout=15)
    if code == 0:
        return {'status': 'ok', 'output': out}
    return {'status': 'error', 'error': err}


def cmd_mine(path=None):
    """挖掘目录生成新记忆。"""
    target = path or WORKSPACE
    out, err, code = call_mempalace(['mine', target, '--mode', 'projects'], timeout=120)
    if code == 0:
        return {'status': 'ok', 'path': target, 'output': out}
    return {'status': 'error', 'error': err}


def cmd_forget(memory_id):
    """从 ChromaDB 删除记忆。"""
    try:
        import chromadb
        palace_path = os.path.expanduser('~/.mempalace/palace')
        client = chromadb.PersistentClient(path=palace_path)
        for col in client.list_collections():
            try:
                collection = client.get_collection(col.name)
                item = collection.get(ids=[memory_id])
                if item and item['ids']:
                    collection.delete(ids=[memory_id])
                    return {'status': 'ok', 'action': 'forget', 'id': memory_id}
            except Exception:
                pass
        return {'status': 'ok', 'action': 'forget', 'id': memory_id, 'note': 'not found'}
    except Exception as e:
        return {'status': 'error', 'error': str(e)}


# ─────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='MemPalace Enhanced CLI v5 - 第一性原则精确召回',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  # 精确召回(默认,关闭MMR):
  mempalace_cli.py search "城的身份 CEO"

  # 开启MMR多样性模式:
  mempalace_cli.py search "城的身份 CEO" --use-mmr

  # 存储记忆(含凭证检测):
  mempalace_cli.py remember "城总今天有新的任务安排"
'''
    )
    subparsers = parser.add_subparsers(dest='cmd')

    p_search = subparsers.add_parser('search')
    p_search.add_argument('query', help='搜索查询')
    p_search.add_argument('--limit', type=int, default=5)
    p_search.add_argument('--use-mmr', dest='use_mmr', action='store_true', default=False,
                         help='开启MMR多样性重排(默认关闭,精确召回优先)')
    p_search.add_argument('--mmr', dest='use_mmr', action='store_true', default=False,
                         help='开启MMR多样性重排')
    p_search.add_argument('--no-dedup', dest='dedup', action='store_false', default=True)
    p_search.add_argument('--no-strip', dest='strip', action='store_false', default=True)

    subparsers.add_parser('status')
    subparsers.add_parser('wake-up')

    p_mine = subparsers.add_parser('mine')
    p_mine.add_argument('--path', help='挖掘路径')

    p_forget = subparsers.add_parser('forget')
    p_forget.add_argument('memory_id', help='记忆ID')

    p_remember = subparsers.add_parser('remember')
    p_remember.add_argument('content', help='要记忆的内容')
    p_remember.add_argument('--agent', '-a', default='main')
    p_remember.add_argument('--room', '-r', default='general')
    p_remember.add_argument('--source', '-s', default='')

    args = parser.parse_args()

    if args.cmd == 'search':
        result = cmd_search(args.query, args.limit, args.use_mmr, args.dedup, args.strip)
    elif args.cmd == 'remember':
        result = cmd_remember(args.content, args.agent, args.room, args.source)
    elif args.cmd == 'status':
        result = cmd_status()
    elif args.cmd == 'wake-up':
        result = cmd_wake_up()
    elif args.cmd == 'mine':
        result = cmd_mine(args.path)
    elif args.cmd == 'forget':
        result = cmd_forget(args.memory_id)
    else:
        parser.print_help()
        sys.exit(0)

    print(json.dumps(result, ensure_ascii=False, indent=2))
