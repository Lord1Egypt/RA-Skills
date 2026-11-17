# -*- coding: utf-8 -*-
# Re-extract email data into the 3-section workboard structure:
#  1) volume  2) key-store progress+todos  3) other order/delivery/lead-time todos
import json, re, os, datetime, calendar
from collections import defaultdict, Counter

TODAY = datetime.date.today()

# ---------- load full bodies ----------
def load_bodies(fn):
    raw = json.load(open(fn, encoding='utf-8'))
    out = {}
    for m in raw['data']['messages']:
        out[m['message_id']] = m
    return out

fb = load_bodies('flagged_bodies.json')
ob = load_bodies('other_bodies.json')
bodies = {**fb, **ob}
# 合并今日新拉取邮件（含西葡地区 Brandzone/Endcap/Table-Top/POSM 等非建店业务），按 message_id 去重
if os.path.exists('today_bodies.json'):
    tb = load_bodies('today_bodies.json')
    before = len(bodies)
    bodies.update(tb)
    print('merged today_bodies: +%d new messages (total %d)' % (len(bodies) - before, len(bodies)))
print('total bodies', len(bodies))

det = json.load(open('email_detail.json', encoding='utf-8'))
items = det['flagged'] + det['other']

# ---------- text helpers ----------
# 扩充引文/邮件头剥离标记：包含 MAIL/From/To/Cc/Sent/Subject 等内联或换行形式，避免引用邮件头泄漏到「原文进展」
QUOTE_MARKS = ['\nFrom:', '\nOn ', '-----原始邮件-----', '\n> ', '\n\nFrom ',
               ' MAIL:', ' From:', ' To:', ' Cc:', ' Sent:', ' Subject:',
               '\n发件人：', '\n收件人：', '\n抄送：', '\n主题：', '\n发送时间：']
# 跨语言引用邮件头剥离：Am/Il/Le/El/Dňa/Dne ... schrieb/ha scritto/a écrit/escribió/napísal/napsal
# 以及英文 On ... wrote:（需冒号/换行收尾，避免误伤正文）。客户端常在引用正文前插入一行「X 于某时写道:」。
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

def split_sentences(txt):
    txt = re.sub(r'\s+', ' ', txt)
    parts = re.split(r'(?<=[.!?])\s+', txt)
    return [p.strip() for p in parts if p.strip()]

STATUS_RE = re.compile(r'\b(completed|signed|approved|confirmed|confirmed|ready|in progress|started|finished|received|installed|won|accepted|delivered|submitted|finalized|reviewed|agreed|ongoing|pending|waiting|scheduled|opened|launched|kick[\s-]?off|aligned|resolved)\b', re.I)
ACTION_RE = re.compile(r'\b(please|kindly|could you|can you|would you|need|required|should|must|confirm|provide|send|arrange|prepare|review|approve|sign|follow up|let me know|share|update|check|verify|schedule|finalize|submit|order|place|deliver|reply|proceed|remind)\b', re.I)
DATE_HINT_RE = re.compile(r'\b(by|before|end of|until|due|最晚|截止|at the latest)\b', re.I)

# 「需要反馈」词义：等待对方回音 / 确认 / 批复 等（用于待办标红置顶 + 截止前1天催办）
FB_RE = re.compile(r'\b(confirm|reply|re:|approve|approval|review|feedback|let me know|let us know|awaiting|response|revert|hear from|回复|确认|审批|反馈|等回复|等确认|等反馈|回音|答复)\b', re.I)

def progress_snippet(body, maxlen=300):
    fp = fresh_part(body)
    if not fp:
        return ''
    lines = [l.strip() for l in fp.split('\n') if l.strip()]
    # prefer lines that convey status
    status_lines = [l for l in lines if STATUS_RE.search(l)]
    chosen = status_lines[:3] if status_lines else lines[:3]
    snip = ' '.join(chosen)
    snip = re.sub(r'\s+', ' ', snip)
    return snip[:maxlen]

def todo_lines(body, maxn=4):
    fp = fresh_part(body)
    if not fp:
        return []
    res = []
    for s in split_sentences(fp):
        if len(s) < 8:
            continue
        if ACTION_RE.search(s) or (DATE_HINT_RE.search(s) and len(s) < 200):
            res.append(s)
        if len(res) >= maxn:
            break
    return res

# ---------- bounce / system non-delivery filter ----------
BOUNCE_RE = re.compile(
    r'(undeliverable|returned mail|returned to sender|delivery status notification|failure notice|'
    r'delivery failure|delivery has failed|mail delivery failed|unable to deliver|'
    r'permanent delivery failure|nondelivery report|undelivered mail|message not delivered|'
    r'delivery report \(failure\)|邮件退信|退信|投递失败|无法送达|邮件退回|发送失败|退回的邮件|投递状态通知)',
    re.I)
BOUNCE_SENDER_RE = re.compile(r'(mailer-daemon|postmaster|mail delivery system|microsoft outlook|no.?reply|don?ot?reply|do-not-reply|系统退信|投递系统|daemon)', re.I)
def is_bounce(subj, body='', sender=''):
    s = (subj or '').strip()
    if BOUNCE_RE.search(s):
        return True
    if sender and BOUNCE_SENDER_RE.search(sender):
        return True
    b = body or ''
    if 'Delivery has failed to these recipients or groups' in b:
        return True
    if 'Delivery Status Notification' in s and 'failure' in b.lower():
        return True
    if '邮件退信' in b or '投递失败' in b or '无法送达' in b:
        return True
    return False

# ---------- participants & self-sent ----------
SELF_EMAIL = os.environ.get('MAILBOARD_ME') or 'your-name@company.com'

def parties_from_body(b):
    """Return dict {head_from, to, cc} extracted from a bodies entry.
    Each list item is {name, email}; head_from is a single dict (or None)."""
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
    """Thread is self-only-sent iff every message has direction='发出' and the
    sender (head_from email) is 陈哲 himself."""
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

# ---------- store classification ----------
def sender_name(it, bodies):
    b = bodies.get(it.get('id'))
    if b and isinstance(b.get('head_from'), dict):
        return b['head_from'].get('name') or b['head_from'].get('email') or ''
    return it.get('from', '')

def classify_store(it, bodies):
    subj = it.get('subject', '') or ''
    b = bodies.get(it.get('id'))
    body = (b.get('body_plain_text', '') if b else '') or it.get('content', '')
    txt = (subj + ' ' + body[:2000]).lower()
    tags = []
    if re.search(r'cologne|köln|koeln', txt):
        # sub-location within cologne
        if 'mova' in txt:
            tags.append(('Cologne', 'MOVA Cologne SIS'))
        elif re.search(r'dreame.*(saturn|shop|sis)|saturn', txt):
            tags.append(('Cologne', 'DREAME Cologne SIS'))
        else:
            tags.append(('Cologne', 'Cologne SIS'))
    if re.search(r'rome|roma|romaest', txt):
        tags.append(('Rome', 'Rome Flagship'))
    if re.search(r'düsseldorf|dusseldorf|duesseldorf', txt):
        tags.append(('Dusseldorf', 'Düsseldorf Flagship'))
    if re.search(r'zurich|zürich|glatt', txt):
        tags.append(('Zurich', 'Zurich Glatt Flagship'))
    return tags

STORE_ORDER = ['Cologne', 'Rome', 'Dusseldorf', 'Zurich']
STORE_LABEL = {
    'Cologne': '科隆店中店',
    'Rome': '罗马旗舰店',
    'Dusseldorf': '杜塞旗舰店',
    'Zurich': '苏黎世 Glatt 旗舰店',
}

# ---------- order/delivery/lead-time classification ----------
ODL_KW = {
    '下单': re.compile(r'\b(order|purchase order|p\.o\.|po |placement|place an order|reorder| procurement|采购|下单|订货)\b', re.I),
    '交付': re.compile(r'\b(deliver|delivery|shipment|ship|dispatch|fulfill|consignment|发货|交付|送货|到货|物流)\b', re.I),
    '交期': re.compile(r'\b(lead time|lead-time|生产周期|货期|交期|eta|etd|production time|工期|timeline|schedule of works)\b', re.I),
}
def classify_odl(it):
    subj = it.get('subject', '') or ''
    txt = subj + ' ' + (it.get('fresh', '') or it.get('content', ''))[:1800]
    hits = {k: bool(rx.search(txt)) for k, rx in ODL_KW.items()}
    if not any(hits.values()):
        return None
    # priority: 交期(lead time) > 交付(delivery) > 下单(order) for labeling primary
    for k in ['交期', '交付', '下单']:
        if hits[k]:
            return k, hits
    return None

# ---------- Iberia (西葡) non-store business tracking ----------
# 西葡地区非建店业务：西班牙/葡萄牙地区的 Brandzone / Endcap / Table-Top / POSM 等零售展示项目
IBERIA_REGION = re.compile(r'(spain|españa|portugal|lisboa|madrid|barcelona|porto|iberia|ibéric)', re.I)
IBERIA_TYPE = [
    ('Brandzone', re.compile(r'brandzone', re.I)),
    ('Endcap', re.compile(r'endcap', re.I)),
    ('Table-Top', re.compile(r'table[\s-]?top', re.I)),
    ('POSM', re.compile(r'posm', re.I)),
]
MONICA_RE = re.compile(r'monica', re.I)
IBERIA_ORDER = ['Brandzone', 'Endcap', 'Table-Top', 'POSM', 'Retail Project']

def classify_iberia(blob, subject=''):
    """blob = subject + body. Return (project_type, country) or None.
    Project TYPE is decided by SUBJECT keywords first (so the same conversation is
    not split into Endcap vs Retail Project by body noise), falling back to body."""
    if not IBERIA_REGION.search(blob):
        return None
    subj_low = (subject or '').lower()
    ptype = 'Retail Project'
    for name, rx in IBERIA_TYPE:
        if rx.search(subj_low):
            ptype = name
            break
    else:
        for name, rx in IBERIA_TYPE:
            if rx.search(blob):
                ptype = name
                break
    low = blob.lower()
    if re.search(r'(spain|españa|madrid|barcelona)', low):
        country = 'Spain'
    elif re.search(r'(portugal|lisboa|porto)', low):
        country = 'Portugal'
    else:
        country = 'Iberia'
    return (ptype, country)

def _norm_date(s):
    s = (s or '').strip()
    m = re.match(r'^(\d{4})-(\d{1,2})-(\d{1,2})$', s)
    if m:
        try:
            return datetime.date(int(m.group(1)), int(m.group(2)), int(m.group(3))).isoformat()
        except Exception:
            return None
    m = re.match(r'^(\d{1,2})[.\/](\d{1,2})[.\/](\d{2,4})$', s)
    if m:
        y = int(m.group(3))
        if y < 100:
            y += 2000
        try:
            return datetime.date(y, int(m.group(2)), int(m.group(1))).isoformat()
        except Exception:
            return None
    m = re.match(r'^([A-Za-z]{3,9})\s+(\d{1,2})$', s, re.I)
    if m:
        mon = {'jan':1,'feb':2,'mar':3,'apr':4,'may':5,'jun':6,'jul':7,'aug':8,'sep':9,'oct':10,'nov':11,'dec':12}.get(m.group(1)[:3].lower())
        if mon:
            yr = TODAY.year if mon >= TODAY.month else TODAY.year + 1
            try:
                return datetime.date(yr, mon, int(m.group(2))).isoformat()
            except Exception:
                return None
    return None

DATE_RE = re.compile(
    r'\b\d{4}-\d{1,2}-\d{1,2}\b'
    r'|\b\d{1,2}[.\/]\d{1,2}[.\/]\d{2,4}\b'
    r'|\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.?\s+\d{1,2}\b'
    r'|\b\d{1,2}\s+(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.?\b', re.I)
DL_KW = re.compile(r'\b(by|before|until|deadline|due|at the latest|end of|no later than|latest|截止|最晚|之前|需|必须|到位|完成|we need|must|installed by)\b', re.I)
ENDMONTH_RE = re.compile(r'end of\s+(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*', re.I)
MONTH_NUM = {'jan':1,'feb':2,'mar':3,'apr':4,'may':5,'jun':6,'jul':7,'aug':8,'sep':9,'oct':10,'nov':11,'dec':12}

def extract_ddl(body, maxn=4):
    """Extract deadline-ish dates from a mail body (fresh part)."""
    fp = fresh_part(body)
    res = []
    for m in ENDMONTH_RE.finditer(fp):
        mon = MONTH_NUM.get(m.group(1)[:3].lower())
        if not mon:
            continue
        yr = TODAY.year if mon >= TODAY.month else TODAY.year + 1
        last = calendar.monthrange(yr, mon)[1]
        d = datetime.date(yr, mon, last).isoformat()
        start = max(0, m.start() - 50)
        ctx = re.sub(r'\s+', ' ', fp[start:m.end() + 10]).strip()
        res.append({'date': d, 'text': ctx[:90]})
        if len(res) >= maxn:
            break
    if len(res) < maxn:
        for m in DATE_RE.finditer(fp):
            d = _norm_date(m.group(0))
            if not d:
                continue
            start = max(0, m.start() - 50)
            end = min(len(fp), m.end() + 15)
            ctx = re.sub(r'\s+', ' ', fp[start:end]).strip()
            if DL_KW.search(ctx):
                res.append({'date': d, 'text': ctx[:90]})
                if len(res) >= maxn:
                    break
    res.sort(key=lambda x: x['date'])
    return res

def _dir_of(mm):
    hf = mm.get('head_from') or {}
    em = hf.get('mail_address') if isinstance(hf, dict) else ''
    return '发出' if (em or '').lower() == SELF_EMAIL else '收到'

def _person(mm, key):
    v = mm.get(key) or {}
    if isinstance(v, dict):
        return {'name': (v.get('name') or ''), 'email': (v.get('mail_address') or '')}
    return {'name': '', 'email': ''}

def _people_list(mm, key):
    out = []
    for x in (mm.get(key) or []):
        if isinstance(x, dict):
            out.append({'name': (x.get('name') or ''), 'email': (x.get('mail_address') or '')})
    return out

# ---------- consolidate fragmented iberia threads ----------
# Email threads about the same project get split into many thread_ids by
# reply-prefix noise (Re:/R:/R: R: ...). Merge them by a normalized subject root
# so the 西葡模块 shows clean project cards instead of 10 near-identical cards.
REPLY_PREFIX_RE = re.compile(r'^(\s*(?:re|r|aw|fwd|fw)\s*[:\-]\s*)+', re.I)

def _norm_iberia_root(subj):
    s = REPLY_PREFIX_RE.sub('', (subj or ''))
    s = re.sub(r'\d{5,}', '', s)  # drop project/order numbers wherever they appear
    s = re.sub(r'\s+', ' ', s).strip().lower()
    words = [w for w in re.split(r'[^a-z0-9à-ÿ&]+', s) if w]
    return 'w-' + '-'.join(words[:6])

def _merge_iberia_item(group):
    primary = max(group, key=lambda t: (t['count'], t['last'] or ''))
    dates = sorted({d for t in group for d in (t.get('dates') or [])})
    allp, seen = [], set()
    for t in group:
        for r in (t.get('all_partners') or []):
            k = (r.get('email') or '').lower()
            if k and k not in seen:
                seen.add(k); allp.append(r)
    ddl, seen2 = [], set()
    for t in group:
        for dd in (t.get('ddl') or []):
            if repr(dd) not in seen2:
                seen2.add(repr(dd)); ddl.append(dd)
    ddl = ddl[:4]
    todos, seen3 = [], set()
    for t in group:
        for td in (t.get('todos') or []):
            if td not in seen3:
                seen3.add(td); todos.append(td)
    todos = todos[:6]
    return {
        'thread_id': primary['thread_id'],
        'subject': REPLY_PREFIX_RE.sub('', primary.get('subject') or '').strip(),
        'country': primary.get('country'),
        'dates': dates,
        'first': dates[0] if dates else '',
        'last': dates[-1] if dates else '',
        'count': sum(t['count'] for t in group),
        'dirs': sorted({d for t in group for d in (t.get('dirs') or [])}),
        'responsible': '',
        'ddl': ddl,
        'progress': primary.get('progress') or '',
        'todos': todos,
        'head_from': primary.get('head_from'),
        'to': primary.get('to'),
        'cc': primary.get('cc'),
        'all_partners': allp,
        'monica': any(t.get('monica') for t in group),
        'self_only_sent': any(t.get('self_only_sent') for t in group),
        'ptype': primary.get('ptype', 'Retail Project'),
        'src_thread_ids': [t['thread_id'] for t in group],
    }

def merge_iberia_sections(sections):
    """Merge fragmented threads GLOBALLY (across project types) by normalized
    subject root, so the same conversation isn't shown as both Endcap and
    Retail Project. The merged card keeps the primary (bulk) thread's type."""
    all_items = []
    for items in sections.values():
        all_items.extend(items)
    groups = defaultdict(list)
    for t in all_items:
        groups[_norm_iberia_root(t.get('subject'))].append(t)
    out = []
    for grp in groups.values():
        out.append(grp[0] if len(grp) == 1 else _merge_iberia_item(grp))
    return out

def build_iberia():
    threads = defaultdict(list)
    for m in bodies.values():
        tid = m.get('thread_id')
        if tid:
            threads[tid].append(m)
    sections = defaultdict(list)
    for tid, msgs in threads.items():
        msgs = sorted(msgs, key=lambda x: x.get('date_formatted') or '')
        latest = msgs[-1]
        blob = ' '.join(((mm.get('subject') or '') + ' ' + (mm.get('body_plain_text') or '')[:1500]) for mm in msgs)
        cls = classify_iberia(blob, latest.get('subject'))
        if not cls:
            continue
        ptype, country = cls
        # 排除建店类（Cologne/Rome/Dusseldorf/Zurich 等店中店/旗舰店）— 归入模块②，不进「西葡非建店」
        if classify_store({'id': latest.get('message_id'), 'subject': latest.get('subject', '')}, bodies):
            continue
        dts = [mm.get('date_formatted') for mm in msgs if mm.get('date_formatted')]
        f0 = _person(latest, 'head_from')
        to0 = _people_list(latest, 'to')
        cc0 = _people_list(latest, 'cc')
        allp, seen = [], set()
        for mm in msgs:
            for r in [_person(mm, 'head_from')] + _people_list(mm, 'to') + _people_list(mm, 'cc'):
                k = (r.get('email') or '').lower()
                if k and k not in seen:
                    seen.add(k)
                    allp.append(r)
        monica = any(MONICA_RE.search((r.get('name') or '') + ' ' + (r.get('email') or '')) for r in allp)
        body_latest = latest.get('body_plain_text') or ''
        ddl = extract_ddl(body_latest)
        self_only = all(_dir_of(mm) == '发出' and (((mm.get('head_from') or {}).get('mail_address') or '').lower() == SELF_EMAIL) for mm in msgs)
        sections[ptype].append({
            'thread_id': tid,
            'ptype': ptype,
            'subject': latest.get('subject') or '',
            'country': country,
            'dates': dts,
            'first': dts[0] if dts else '',
            'last': dts[-1] if dts else '',
            'count': len(msgs),
            'dirs': sorted(set(_dir_of(mm) for mm in msgs)),
            'responsible': '',
            'ddl': ddl[:4],
            'progress': progress_snippet(body_latest),
            'todos': list(dict.fromkeys(todo_lines(body_latest)))[:4],
            'head_from': f0,
            'to': to0,
            'cc': cc0,
            'all_partners': allp,
            'monica': monica,
            'self_only_sent': self_only,
        })
    items_all = merge_iberia_sections(sections)
    by_type = defaultdict(list)
    for it in items_all:
        by_type[it['ptype']].append(it)
    sec_list = []
    monica_total = 0
    for ptype in IBERIA_ORDER:
        if by_type.get(ptype):
            items = by_type[ptype]
            monica_total += sum(1 for t in items if t['monica'])
            sec_list.append({'type': ptype, 'count': len(items), 'items': items})
    total = sum(s['count'] for s in sec_list)
    return {'sections': sec_list, 'total': total, 'monica_count': monica_total,
            'thread_ids': [t['thread_id'] for s in sec_list for t in s['items']]}

# ---------- assemble ----------
enriched = []
for gi, grp in enumerate([det['flagged'], det['other']]):
    is_flagged_src = (gi == 0)
    for it in grp:
        b = bodies.get(it.get('id'))
        full_body = (b.get('body_plain_text', '') if b else '') or it.get('content', '')
        # 系统退信（投递失败）直接忽略，不纳入任何信息范围
        if is_bounce(it.get('subject', ''), full_body):
            continue
        fp = fresh_part(full_body)
        tags = classify_store(it, bodies)
        primary = tags[0][0] if tags else None
        parties = parties_from_body(b)
        enriched.append({
            'id': it.get('id'),
            'date': it.get('date'),
            'direction': it.get('direction'),
            'subject': it.get('subject', ''),
            'from': parties['head_from'] or {'name': '', 'email': (it.get('from') or '')},
            'to': parties['to'],
            'cc': parties['cc'],
            'responsible': it.get('responsible'),
            'ddl': it.get('ddl', []),
            'labels': it.get('labels'),
            'flagged': is_flagged_src,
            'content': it.get('content', ''),
            'full_body': full_body,
            'fresh': fp,
            'stores': tags,
            'primary_store': primary,
            'progress': progress_snippet(full_body),
            'todos': todo_lines(full_body),
        })

# volume
def ddir(it): return it['direction']
vol = {
    'total': len(enriched),
    'received': sum(1 for i in enriched if i['direction'] == '收到'),
    'sent': sum(1 for i in enriched if i['direction'] == '发出'),
    'flagged': sum(1 for i in enriched if i['flagged']),
    'with_ddl': sum(1 for i in enriched if i['ddl']),
}
by_date = Counter(i['date'] for i in enriched if i['date'])
by_dir = Counter(i['direction'] for i in enriched)
key_items = [i for i in enriched if i['stores']]
vol['key_store_emails'] = len(key_items)

# ---------- key stores: group by thread ----------
# we need thread_id; rebuild from bodies
def thread_of(it):
    b = bodies.get(it['id'])
    return b.get('thread_id') if b else it['id']

store_view = {}
for sk in STORE_ORDER:
    sis = defaultdict(list)
    for it in enriched:
        for (s, sub) in it['stores']:
            if s == sk:
                sis[sub].append(it)
    sections = []
    for sub, its in sis.items():
        threads = defaultdict(list)
        for it in its:
            threads[thread_of(it)].append(it)
        thread_list = []
        for tid, msgs in threads.items():
            msgs.sort(key=lambda x: x['date'] or '')
            latest = msgs[-1]
            dts = [m['date'] for m in msgs if m['date']]
            all_ddl = []
            for m in msgs:
                all_ddl.extend(m['ddl'])
            all_ddl.sort(key=lambda d: d.get('date', ''))
            todos = []
            for m in msgs:
                todos.extend(m['todos'])
            # participants: take from the latest message (richest context for 'who is on this thread NOW')
            # but also union all distinct partners across the thread for richer display
            head_from = latest.get('from') or {}
            to_latest = latest.get('to') or []
            cc_latest = latest.get('cc') or []
            # union of all to/cc across thread
            all_to = []
            seen = set()
            for m in msgs:
                for r in (m.get('to') or []) + (m.get('cc') or []):
                    key = (r.get('email') or '').lower()
                    if key and key not in seen:
                        seen.add(key); all_to.append(r)
            thread_list.append({
                'thread_id': tid,
                'subject': latest['subject'],
                'dates': dts,
                'first': dts[0] if dts else '',
                'last': dts[-1] if dts else '',
                'count': len(msgs),
                'dirs': sorted(set(m['direction'] for m in msgs)),
                'responsible': latest['responsible'],
                'ddl': all_ddl[:4],
                'progress': latest['progress'],
                'todos': list(dict.fromkeys(todos))[:4],
                'head_from': head_from,
                'to': to_latest,
                'cc': cc_latest,
                'all_partners': all_to,
                'self_only_sent': is_self_only_sent(msgs),
            })
        thread_list.sort(key=lambda t: t['last'] or '', reverse=True)
        sections.append({
            'sub': sub,
            'count': len(its),
            'threads': len(thread_list),
            'with_ddl': sum(1 for t in thread_list if t['ddl']),
            'items': thread_list,
        })
    store_view[sk] = {
        'label': STORE_LABEL[sk],
        'emails': len([i for i in enriched if any(s == sk for s, _ in i['stores'])]),
        'sections': sections,
    }

# ---------- Iberia (西葡) non-store business ----------
iberia_view = build_iberia()
iberia_thread_ids = set(iberia_view.get('thread_ids', []))

# ---------- other order/delivery/lead-time todos ----------
other_todos = []
for it in enriched:
    if it['stores']:
        continue
    if thread_of(it) in iberia_thread_ids:
        continue
    cls = classify_odl(it)
    if not cls:
        continue
    typ, hits = cls
    # require a todo signal: ddl present OR has action/todo lines
    if not it['ddl'] and not it['todos']:
        continue
    ddl_list = it['ddl'][:2]
    ddl_dates = [x.get('date') for x in ddl_list if x.get('date')]
    ddl_earliest = min(ddl_dates) if ddl_dates else None
    # 「需要反馈」：有 DDL 且待办/主题含「等对方回音」词义
    fb_blob = ' '.join(it.get('todos') or []) + ' ' + (it.get('subject') or '')
    needs_feedback = bool(ddl_dates) and bool(FB_RE.search(fb_blob))
    other_todos.append({
        'id': it['id'],
        'date': it['date'],
        'direction': it['direction'],
        'subject': it['subject'],
        'summary': it['content'],
        'type': typ,
        'hits': {k: v for k, v in hits.items()},
        'responsible': it['responsible'],
        'ddl': ddl_list,
        'ddl_earliest': ddl_earliest,
        'needs_feedback': needs_feedback,
        'todos': it['todos'][:3],
    })
# sort: by type then date desc
type_rank = {'交期': 0, '交付': 1, '下单': 2}
other_todos.sort(key=lambda x: (type_rank.get(x['type'], 9), x['date'] or ''), reverse=False)

data = {
    'generated_at': datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
    'today': TODAY.isoformat(),
    'window': {'start': '2026-07-01', 'end': TODAY.isoformat()},
    'volume': vol,
    'by_date': dict(sorted(by_date.items())),
    'by_dir': dict(by_dir),
    'stores': store_view,
    'iberia_view': iberia_view,
    'other_todos': other_todos,
    'stats': {
        'key_emails': vol['key_store_emails'],
        'iberia': iberia_view['total'],
        'iberia_monica': iberia_view['monica_count'],
        'other_todos': len(other_todos),
        'other_by_type': dict(Counter(t['type'] for t in other_todos)),
    },
}
json.dump(data, open('workboard2_data.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('DONE')
print('volume', vol)
print('IBERIA sections', [(s['type'], s['count']) for s in iberia_view['sections']], 'monica', iberia_view['monica_count'])
print('other_todos', len(other_todos), data['stats']['other_by_type'])
for sk in STORE_ORDER:
    sv = store_view[sk]
    print('STORE', sk, 'emails', sv['emails'], 'subs', [(s['sub'], s['count'], s['threads']) for s in sv['sections']])
