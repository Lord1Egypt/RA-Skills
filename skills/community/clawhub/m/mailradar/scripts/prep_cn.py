# -*- coding: utf-8 -*-
"""筛选需中文翻译/归纳的全部线程，输出 cn_inbox_full.json（完整字段 + 清洗后正文片段，供 LLM 翻译）。
规则：
  Tab② 重点门店：选取全部「非纯自发送(self_only_sent)」的线程（不再每店 cap），覆盖模块全部内容。
  Tab③ 其他待办：选取全部 other_todos（98 条），覆盖模块全部内容。
每个条目附带 fresh 清洗正文片段（上限 1100 字），便于翻译归纳（含发件人休假等 party_notes）。
"""
import json, datetime, re, os

SELF_EMAIL = os.environ.get("MAILBOARD_ME", "your-name@company.com")

# ---------- load ----------
d = json.load(open('workboard2_data.json', encoding='utf-8'))
bodies = {}
for fn in ['flagged_bodies.json', 'other_bodies.json']:
    try:
        raw = json.load(open(fn, encoding='utf-8'))
    except Exception:
        continue
    for m in raw['data']['messages']:
        bodies[m['message_id']] = m

# ---------- fresh text helpers ----------
# 扩充引文/邮件头剥离标记（与 extract4 保持一致），避免 MAIL/From/To/Cc/Sent/Subject 等引用头泄漏
QUOTE_MARKS = ['\nFrom:', '\nOn ', '-----原始邮件-----', '\n> ', '\n\nFrom ',
               ' MAIL:', ' From:', ' To:', ' Cc:', ' Sent:', ' Subject:',
               '\n发件人：', '\n收件人：', '\n抄送：', '\n主题：', '\n发送时间：']
# 跨语言引用邮件头：Am/Il/Le/El/Dňa/Dne ... schrieb/ha scritto/a écrit/escribió/napísal/napsal；英文 On ... wrote:（冒号/换行收尾）
WROTE_PATTERN = re.compile(
    r'(?m)(?:^|[>\s]*)(?:Am|Il|Le|El|Dňa|Dne)\b'
    r'.{0,200}?\b(?:schrieb|ha scritto|a écrit|escribió|napísal|napsal)\b(?=\s*[:\n])',
    re.I)
EN_WROTE = re.compile(r'(?m)^[>\s]*On\b.{0,200}?\bwrote\b(?=\s*[:\n])', re.I)
def fresh_part(body):
    if not body:
        return ''
    positions = []
    for mk in QUOTE_MARKS:
        i = body.find(mk)
        if i > 0:
            positions.append(i)
    for pat in (WROTE_PATTERN, EN_WROTE):
        m = pat.search(body)
        if m and m.start() > 0:
            positions.append(m.start())
    if positions:
        body = body[:min(positions)]
    return body.strip()

def clean(body, maxlen=1100):
    fp = fresh_part(body)
    fp = re.sub(r'\s+', ' ', fp)
    return fp[:maxlen]

def parties_from_body(b):
    if not b:
        return {'head_from': None, 'to': [], 'cc': []}
    def norm(item):
        if not isinstance(item, dict):
            return None
        return {'name': (item.get('name') or '').strip(),
                'email': (item.get('mail_address') or '').strip()}
    hf = norm(b.get('head_from')) if isinstance(b.get('head_from'), dict) else None
    to = [x for x in (norm(x) for x in (b.get('to') or [])) if x and x['email']]
    cc = [x for x in (norm(x) for x in (b.get('cc') or [])) if x and x['email']]
    return {'head_from': hf, 'to': to, 'cc': cc}

def is_self_only_sent(msgs):
    if not msgs:
        return False
    for m in msgs:
        if m.get('direction') != '发出':
            return False
        b = bodies.get(m['id'])
        hf = (b.get('head_from') or {}) if b else {}
        if (hf.get('mail_address') or '').lower() != SELF_EMAIL:
            return False
    return True

# ---------- thread_id -> bodies ----------
tid_bodies = {}
for mid, b in bodies.items():
    tid = b.get('thread_id')
    if tid:
        tid_bodies.setdefault(tid, []).append(b)

# ---------- Tab② : all non-self threads ----------
out_stores = {}
total_threads = 0
skipped_self = 0
for sk in ['Cologne', 'Rome', 'Dusseldorf', 'Zurich']:
    sv = d['stores'][sk]
    items = []
    for sec in sv['sections']:
        for t in sec['items']:
            if t.get('self_only_sent'):
                skipped_self += 1
                continue
            tid = t.get('thread_id')
            bs = tid_bodies.get(tid, [])
            bs_sorted = sorted(bs, key=lambda x: x.get('internal_date') or x.get('date_formatted') or '')
            latest = bs_sorted[-1] if bs_sorted else None
            excerpt = clean(latest.get('body_plain_text', '') if latest else '')
            items.append({
                'thread_id': tid,
                'subject': t.get('subject'),
                'last': t.get('last'),
                'first': t.get('first'),
                'count': t.get('count'),
                'dirs': t.get('dirs'),
                'responsible': t.get('responsible'),
                'ddl': t.get('ddl'),
                'progress': (t.get('progress') or ''),
                'todos': t.get('todos') or [],
                'head_from': t.get('head_from'),
                'to': t.get('to'),
                'cc': t.get('cc'),
                'all_partners': t.get('all_partners'),
                'sub': sec.get('sub'),
                'fresh': excerpt,
            })
    out_stores[sk] = {'label': sv['label'], 'count': len(items), 'items': items}
    total_threads += len(items)

# ---------- Tab③ : all other_todos ----------
ot = d.get('other_todos', [])
out_todos = []
for o in ot:
    oid = o.get('id')
    b = bodies.get(oid)
    excerpt = clean(b.get('body_plain_text', '') if b else '')
    # participants for todo (from body, fallback to store thread meta)
    if b:
        parts = parties_from_body(b)
    else:
        parts = {'head_from': {'name': (o.get('responsible') or ''), 'email': ''},
                 'to': [], 'cc': []}
    out_todos.append({
        'id': oid,
        'subject': o.get('subject'),
        'date': o.get('date'),
        'direction': o.get('direction'),
        'type': o.get('type'),
        'responsible': o.get('responsible'),
        'ddl': o.get('ddl'),
        'needs_feedback': o.get('needs_feedback'),
        'todos': o.get('todos') or [],
        'summary': (o.get('summary') or '')[:600],
        'head_from': parts['head_from'],
        'to': parts['to'],
        'cc': parts['cc'],
        'fresh': excerpt,
    })

# ---------- Tab③-iberia : 西葡非建店（与 Tab② 同规则：全部非 self_only_sent + 清洗正文） ----------
iv = d.get('iberia_view', {'sections': []})
out_iberia = {'label': '西葡地区非建店业务跟踪', 'count': 0, 'items': []}
skipped_ib_self = 0
for sec in iv.get('sections', []):
    for t in sec.get('items', []):
        if t.get('self_only_sent'):
            skipped_ib_self += 1
            continue
        tid = t.get('thread_id')
        bs = tid_bodies.get(tid, [])
        bs_sorted = sorted(bs, key=lambda x: x.get('internal_date') or x.get('date_formatted') or '')
        latest = bs_sorted[-1] if bs_sorted else None
        excerpt = clean(latest.get('body_plain_text', '') if latest else '')
        out_iberia['items'].append({
            'thread_id': tid,
            'ptype': sec.get('type'),
            'subject': t.get('subject'),
            'last': t.get('last'),
            'first': t.get('first'),
            'count': t.get('count'),
            'dirs': t.get('dirs'),
            'responsible': t.get('responsible'),
            'ddl': t.get('ddl'),
            'progress': (t.get('progress') or ''),
            'todos': t.get('todos') or [],
            'head_from': t.get('head_from'),
            'to': t.get('to'),
            'cc': t.get('cc'),
            'all_partners': t.get('all_partners'),
            'fresh': excerpt,
        })
out_iberia['count'] = len(out_iberia['items'])

out = {
    'generated_at': datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
    'rules': '三段式中文归纳：items=邮件沟通事项；needs_action=需确认/反馈；party_notes=对方告知(含发件人休假等状态)；risk=风险。方向语义：A→B 说「我要休假」=A 休假。删问候/落款。仅展示发件人+收件人(抄送不显示)。',
    'stores': out_stores,
    'other_todos': out_todos,
    'iberia': out_iberia,
}
json.dump(out, open('cn_inbox_full.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('Tab② threads (non-self):', total_threads, '| skipped self_only_sent:', skipped_self)
print('Tab③ todos:', len(out_todos))
print('Tab③-iberia threads (non-self):', out_iberia['count'], '| skipped self_only_sent:', skipped_ib_self)
for sk, s in out_stores.items():
    print('  ', sk, s['label'], '=>', s['count'], 'threads')
