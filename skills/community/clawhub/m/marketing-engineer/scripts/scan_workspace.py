#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工作区全景扫描器（通用版 v2, 2026-09-22）

作用：扫描任意 Marketing Engineer 工作区，产出「文件夹一句话含义 + 每个文件的日期/状态/说明」，
供驾驶舱「工作区全景」视图渲染；也被 serve_dashboard.py 调用实现「每次打开实时扫描」。

用法：
  python3 scan_workspace.py <工作区根目录>        # 生成 <root>/.cache/workspace_map.json
  python3 scan_workspace.py                        # 默认：脚本所在目录的上一级
  from scan_workspace import build_map; build_map(ROOT)   # 供服务端调用

状态判定优先级（STATUS_RULES）：
  1) 注册表命中（可选 <root>/workspace-registry.json）→ 最权威，人工指定
  2) 发布台账命中（**/results/channel-posts.md 中的 URL 出现在 outputs/ 下的文件里）→ 已发布（带渠道+时间）
  3) 文件头「状态：…」标记 → 已发布 / 待审核 / 全文已备 / 需出稿 / 草稿
  4) 目录规则兜底 → 定稿口径 / 方案 / 情报 / 源稿 / 内部 / 素材 / 构建物 / 记忆

目录含义：内置通用词典 FOLDER_DESC + NAME_HINT；工作区可在根目录放
`workspace-folders.json`（格式 {"目录相对路径": ["中文名", "角色", "一句话说明"]}）覆盖/补充，
这样每个项目的目录册可以不改脚本就定制。
"""
import os, re, json, datetime, sys

SKIP_DIRS = {'.git', 'node_modules', '__pycache__', '.venv', 'venv', '.cache',
             '.pytest_cache', '.next', 'dist', 'build'}
SKIP_FILES = {'.DS_Store', 'Thumbs.db'}
SKIP_EXT = {'.pyc', '.pyo', '.lock'}

# ---------------- 文件夹含义册（通用；项目可用 workspace-folders.json 覆盖） ----------------
FOLDER_DESC = {
    '': ('营销工作区根目录', '根层',
         '分层：定稿口径 → 垂直域 → 结构方案 → 构建 → 记忆。'),
    'shared-knowledge': ('唯一可引用来源', '根层',
         '品牌、产品、渠道的定稿口径；改这里 = 改全局。'),
    'shared-knowledge/product-lines': ('产品线定位卡', '根层', '每条产品线一张：定位/受众/卖点/边界。'),
    'shared-knowledge/assets': ('视觉与字体资产', '根层', '品牌规范附件与字体。'),
    'strategy': ('结构性方案', '结构层', '品牌落地、营销总案、竞品方案；不直接对外。'),
    'content': ('内容生产域', '垂直域', '稿件大本营：packs 按周放稿，outputs 放成品源稿。'),
    'content/packs': ('按周内容包', '垂直域', 'week-日期 命名，含该周各渠道稿件与配图。'),
    'content/knowledge': ('内容主题知识', '垂直域', '选题与主题的背景知识。'),
    'geo-seo': ('GEO / SEO 域', '垂直域', '关键词地图、方法论、源稿与效果复盘。'),
    'geo-seo/knowledge': ('关键词地图', '垂直域', '词域划分与选题判断依据。'),
    'geo-seo/outputs': ('对外源稿', '垂直域', '已发布或待发的文章 Markdown。'),
    'geo-seo/results-and-learnings': ('效果数据与复盘', '垂直域', '引擎覆盖、收录与引用数据。'),
    'launch-campaigns': ('上线推广战役', '垂直域', 'brief + tickets + outputs + results。'),
    'competitor-intel': ('竞品情报域', '垂直域', '对标名单、对比矩阵、调研报告。'),
    'competitor-intel/knowledge': ('对标名单与矩阵', '垂直域', '核心对标与逐维对比；对外点名需审批。'),
    'competitor-intel/research': ('调研报告', '垂直域', '周报与深度调研，带来源+日期。'),
    'outbound': ('主动触达域', '垂直域', '外联名单与话术。'),
    'scripts': ('构建脚本', '构建层', '驾驶舱构建、工作区扫描、本地服务。'),
    'raw': ('原始素材归档', '素材', '未处理的抓取件与中间产物。'),
    'generated-images': ('生图默认输出目录', '素材', '正式素材应转移到对应域的 assets/。'),
    '.workbuddy': ('AI 记忆与自动化', '记忆层', '日志、长期笔记、自动化记录；项目数据勿删。'),
}

# 未单独登记的目录：按「目录末段名」给通用一句话说明（避免"尚未登记"套话）
NAME_HINT = {
    'assets': '配图、封面等素材',
    'raw': '未处理的原始抓取/中间产物',
    'outputs': '成品产出',
    'plans': '计划文档',
    'workflows': '流程与 SOP',
    'knowledge': '该域的主题知识与判断依据',
    'results': '结果记录',
    'results-and-learnings': '效果数据与复盘',
    'tickets': '工单（一个任务一张单）',
    'screenshots': '截图证据',
    'jsonld': 'JSON-LD 结构化数据样例',
    'scripts': '脚本',
    'covers': '封面图',
    'distribution': '分发物料',
    'technical': '技术实现资料',
    'fonts': '字体资产',
    'automations': '各自动化的执行记录',
    'memory': 'AI 工作记忆与日志',
    'packs': '按周内容包',
    'research': '调研报告',
    'geo': 'GEO 相关内容',
    'content': '内容稿件',
    'competitor-intel': '竞品情报',
    'geo-seo': 'GEO / SEO 内容',
    'shared-knowledge': '定稿口径',
    'launch-campaigns': '推广战役',
}

# ---------------- 状态规则 ----------------
STATUS_META = {
    '已发布': ('p-done', '已对外发布（台账有 URL 与发布时间）'),
    '待审核': ('p-warn', '稿件已成稿，等你人工审核'),
    '全文已备': ('p-accent', '全文已写完，排在后续日期发布'),
    '需出稿': ('p-block', '排期已定但稿子还没写'),
    '草稿': ('p-warn', '草稿状态，待完善后送审'),
    '定稿口径': ('p-ok', '内部权威口径，是对外内容的唯一来源'),
    '方案': ('p-ok', '内部结构性方案，不直接对外'),
    '情报': ('p-ok', '内部竞品情报与研究，不直接对外'),
    '源稿': ('p-accent', '对外内容的源稿，可能已发布或部分发布'),
    '内部': ('p-ok', '过程性文档（计划/工作流/复盘/知识）'),
    '构建物': ('p-mute', '脚本/页面/缓存等构建产物，不是内容'),
    '素材': ('p-mute', '图片与字体等素材'),
    '记忆': ('p-mute', 'AI 记忆与自动化记录，不对外'),
}
STATUS_ORDER = ['已发布', '待审核', '全文已备', '需出稿', '草稿', '定稿口径', '方案', '情报',
                '源稿', '内部', '构建物', '素材', '记忆']

DIR_DEFAULT_STATUS = [
    ('shared-knowledge', '定稿口径'),
    ('strategy', '方案'),
    ('competitor-intel', '情报'),
    ('.workbuddy', '记忆'),
    ('scripts', '构建物'),
    ('generated-images', '素材'),
    ('raw', '素材'),
]


def load_folder_overrides(root):
    """工作区可选 workspace-folders.json 覆盖目录说明：
    {"目录相对路径": ["中文名", "角色", "一句话说明"]}"""
    p = os.path.join(root, 'workspace-folders.json')
    if not os.path.exists(p):
        return {}
    try:
        d = json.load(open(p, encoding='utf-8'))
        return {k: tuple(v) for k, v in d.items() if isinstance(v, list) and len(v) == 3}
    except Exception:
        return {}


def load_registry(root):
    """可选注册表：<root>/workspace-registry.json
    {"文件相对路径": {"status": "待审核", "date": "09-22", "channels": ["公众号"], "url": ""}}
    有它则以它为准（内容库显示什么，全景就显示什么）。"""
    for name in ('workspace-registry.json', '.cache/registry.json'):
        p = os.path.join(root, name)
        if os.path.exists(p):
            try:
                return json.load(open(p, encoding='utf-8'))
            except Exception:
                return {}
    return {}


# ---------------- 台账解析（已发布真相源） ----------------
def parse_ledger(root):
    """从发布台账提取 (url, 发布时间, 渠道)"""
    out, ledgers = [], []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            if fn == 'channel-posts.md':
                ledgers.append(os.path.join(dirpath, fn))
    for lp in ledgers:
        txt = open(lp, encoding='utf-8', errors='ignore').read()
        cur_channel = url = date = None
        for ln in txt.splitlines():
            m = re.match(r'^#{2,3}\s+(.*)', ln)
            if m:
                if url:
                    out.append({'url': url, 'date': date, 'channel': cur_channel})
                cur_channel = m.group(1).strip()
                url = date = None
            mu = re.match(r'^-?\s*\*\*URL\*\*[：:]\s*(\S+)', ln) or re.search(r'(https?://\S+)', ln)
            md = re.match(r'^-?\s*\*\*发布时间\*\*[：:]\s*([0-9\-]{8,10}[^｜|]*)', ln)
            if md:
                date = md.group(1).strip()
            if mu:
                u = mu.group(1).rstrip('）)')
                if u.startswith('http'):
                    url = url or u
        if url:
            out.append({'url': url, 'date': date, 'channel': cur_channel})
    seen, uniq = set(), []
    for e in out:
        if e['url'] in seen:
            continue
        seen.add(e['url'])
        uniq.append(e)
    return uniq


def first_heading_or_line(txt):
    for ln in txt.splitlines():
        s = ln.strip().lstrip('#').strip()
        if not s or s.startswith('---') or s.startswith('```'):
            continue
        s = re.sub(r'^[>*-]+\s*', '', s)
        s = re.sub(r'\*\*(.+?)\*\*', r'\1', s)
        return s[:60]
    return ''


def infer_status(rel, txt):
    """返回 (status, channel, published_at, url)"""
    head = '\n'.join(txt.splitlines()[:12])
    m = re.search(r'状态[：:]\s*([^\n｜|]{0,40})', head)
    if m:
        s = m.group(1)
        for kw in ('已发布', '全文已备', '需出稿', '草稿', '待审核', '待审'):
            if kw in s:
                return kw, '', '', ''
    for pref, st in DIR_DEFAULT_STATUS:
        if rel == pref or rel.startswith(pref + '/'):
            return st, '', '', ''
    parts = rel.split('/')
    tail = parts[-2] if len(parts) > 1 else ''
    if tail == 'outputs':
        return '源稿', '', '', ''
    if tail in ('plans', 'workflows', 'knowledge', 'results-and-learnings', 'research'):
        return '内部', '', '', ''
    if rel.endswith(('.png', '.jpg', '.jpeg', '.webp', '.gif', '.svg')):
        return '素材', '', '', ''
    if rel.endswith(('.html', '.py')):
        return '构建物', '', '', ''
    return '内部', '', '', ''


def build_map(root):
    folder_desc = dict(FOLDER_DESC)
    folder_desc.update(load_folder_overrides(root))
    ledger = parse_ledger(root)
    ledger_by_url = {e['url']: e for e in ledger}
    registry = load_registry(root)

    files, dirs = [], {}
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS)
        rel_dir = os.path.relpath(dirpath, root).replace('\\', '/')
        rel_dir = '' if rel_dir == '.' else rel_dir
        for fn in sorted(filenames):
            if fn in SKIP_FILES or os.path.splitext(fn)[1] in SKIP_EXT:
                continue
            fp = os.path.join(dirpath, fn)
            rel = (rel_dir + '/' + fn).lstrip('/')
            try:
                st = os.stat(fp)
            except OSError:
                continue
            mtime = datetime.datetime.fromtimestamp(st.st_mtime)
            txt = ''
            if fn.endswith(('.md', '.txt', '.json', '.yaml', '.yml')):
                try:
                    txt = open(fp, encoding='utf-8', errors='ignore').read()
                except Exception:
                    txt = ''
            status, channel, pub_at, url = infer_status(rel, txt)
            # 台账命中升级为「已发布」——仅限 outputs/ 成品目录，排除台账自身与说明文件
            is_output = ('/outputs/' in '/' + rel) or rel.startswith('outputs/')
            excluded = fn.startswith('README') or fn == 'channel-posts.md' or '/results/' in '/' + rel
            if is_output and not excluded:
                for u, e in ledger_by_url.items():
                    if u and u in txt:
                        status, channel, pub_at, url = '已发布', (e.get('channel') or ''), (e.get('date') or ''), u
                        break
            if rel in registry:
                r = registry[rel]
                status = r.get('status') or status
                channel = '、'.join(r.get('channels') or []) or channel
                pub_at = r.get('date') or pub_at
                url = r.get('url') or url
            note = first_heading_or_line(txt) if txt else fn.rsplit('.', 1)[0]
            files.append({
                'path': rel, 'name': fn, 'dir': rel_dir or '（根目录）',
                'date': mtime.strftime('%Y-%m-%d'),
                'datetime': mtime.strftime('%Y-%m-%d %H:%M'),
                'size': st.st_size, 'status': status,
                'cls': STATUS_META.get(status, ('p-todo', ''))[0],
                'channel': channel, 'published_at': pub_at, 'url': url,
                'note': note,
            })
            dirs[rel_dir] = dirs.get(rel_dir, 0) + 1
            pd = rel_dir
            while pd:                      # 逐级向上累计，保证中间层目录也进树且计数含子目录
                pd = pd.rsplit('/', 1)[0] if '/' in pd else ''
                dirs[pd] = dirs.get(pd, 0) + 1

    folder_list = []
    for rel_dir, cnt in sorted(dirs.items()):
        if rel_dir in folder_desc:
            title, role, desc = folder_desc[rel_dir]
        else:
            parts = rel_dir.split('/')
            leaf = parts[-1]
            parent_title = None
            for i in range(len(parts) - 1, 0, -1):
                p = '/'.join(parts[:i])
                if p in folder_desc:
                    parent_title = folder_desc[p][0]
                    break
                if i == 1 and '' in folder_desc:
                    parent_title = folder_desc[''][0]
            title = (parent_title + ' · ' if parent_title else '') + leaf
            role = '子目录'
            if leaf in NAME_HINT:
                desc = NAME_HINT[leaf]
            elif re.match(r'^week-\d{4}-\d{2}-\d{2}$', leaf):
                desc = '该周内容包（按周存放的渠道稿件）'
            elif leaf.startswith('week-'):
                desc = '专题周内容包'
            elif re.match(r'^[0-9a-f]{8}-[0-9a-f]{4}-', leaf) or (len(leaf) == 36 and leaf.count('-') == 4):
                desc = '单次自动化的执行记录（以自动化 ID 命名）'
            elif re.match(r'^\d{4}-\d{2}$', leaf):
                desc = '按月份归档的效果数据'
            else:
                desc = '该域的子目录'
        folder_list.append({'path': rel_dir or '（根目录）', 'title': title, 'role': role,
                            'desc': desc, 'count': cnt,
                            'name': (rel_dir.split('/')[-1] if rel_dir else '（根目录）'),
                            'depth': 0 if not rel_dir else len(rel_dir.split('/'))})

    status_count = {}
    for f in files:
        status_count[f['status']] = status_count.get(f['status'], 0) + 1

    return {
        'generated_at': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'root': root,
        'total_files': len(files),
        'total_dirs': len(folder_list),
        'folders': folder_list,
        'files': files,
        'status_count': status_count,
        'status_meta': {k: {'cls': v[0], 'desc': v[1]} for k, v in STATUS_META.items()},
        'status_order': STATUS_ORDER,
        'ledger_count': len(ledger),
    }


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    root = os.path.abspath(os.path.expanduser(root))
    data = build_map(root)
    out = os.path.join(root, '.cache', 'workspace_map.json')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    json.dump(data, open(out, 'w', encoding='utf-8'), ensure_ascii=False)
    print(f"扫描完成：{data['total_files']} 个文件 / {data['total_dirs']} 个目录 / 台账 {data['ledger_count']} 条")
    for k in STATUS_ORDER:
        if k in data['status_count']:
            print(f"  {k}: {data['status_count'][k]}")
    print('→', out)


if __name__ == '__main__':
    main()
