# -*- coding: utf-8 -*-
"""IMAP 客户端（需求 §6.1/§6.5）：游标读取、正文清洗、.ics 附件解析、发件人过滤。

只读访问（readonly select + BODY.PEEK），不改邮箱任何状态。
"""
import email
import imaplib
import re
from email import policy
from email.header import decode_header, make_header
from email.utils import parsedate_to_datetime
from html.parser import HTMLParser

import ics_parser


class AccountError(Exception):
    def __init__(self, code, message, hint=None):
        super().__init__(message)
        self.code = code
        self.hint = hint


class _HTMLText(HTMLParser):
    """朴素 HTML→纯文本：丢 script/style，块级标签换行。"""
    _BLOCK = {'p', 'div', 'br', 'tr', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'table'}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []
        self._skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'):
            self._skip += 1
        elif tag in self._BLOCK:
            self.parts.append('\n')

    def handle_endtag(self, tag):
        if tag in ('script', 'style') and self._skip:
            self._skip -= 1
        elif tag in self._BLOCK:
            self.parts.append('\n')

    def handle_data(self, data):
        if not self._skip:
            self.parts.append(data)

    def text(self):
        return re.sub(r'\n{3,}', '\n\n', re.sub(r'[ \t]+', ' ', ''.join(self.parts))).strip()


def _decode_hdr(value):
    if not value:
        return ''
    try:
        return str(make_header(decode_header(value)))
    except Exception:
        return str(value)


def _addr_of(from_header):
    """取发件人地址（小写）。"""
    m = re.search(r'<([^>]+)>', from_header or '')
    return (m.group(1) if m else (from_header or '')).strip().lower()


def _sender_allowed(acct, from_addr, from_header):
    """黑名单优先于白名单（需求 §3.1）。匹配：子串（大小写不敏感）。"""
    header_low = (from_header or '').lower()
    for b in acct.get('sender_blocklist') or []:
        if str(b).lower() in header_low or str(b).lower() == from_addr:
            return False
    allow = acct.get('sender_allowlist') or []
    if not allow:
        return True
    return any(str(a).lower() in header_low or str(a).lower() == from_addr for a in allow)


def _extract_body(msg, max_chars, strip_signatures):
    """text/plain 优先，其次 HTML 转纯文本；剥签名；截断。"""
    plain, html = None, None
    for part in msg.walk():
        ctype = part.get_content_type()
        if ctype == 'text/plain' and plain is None and not part.get_filename():
            plain = part.get_content()
        elif ctype == 'text/html' and html is None and not part.get_filename():
            html = part.get_content()
    body = plain if plain is not None else (html and _HTMLText_html_to_text(html))
    if body is None:
        return '', False
    body = body.strip()
    if strip_signatures:
        body = _strip_signature(body)
    truncated = len(body) > max_chars
    if truncated:
        body = body[:max_chars] + '\n[……正文超长已截断]'
    return body, truncated


def _HTMLText_html_to_text(html):
    p = _HTMLText()
    try:
        p.feed(html)
        return p.text()
    except Exception:
        return re.sub(r'<[^>]+>', ' ', html)


def _strip_signature(body):
    lines, out, cut = body.split('\n'), [], False
    for ln in lines:
        s = ln.strip()
        if re.fullmatch(r'--+\s*', s):  # 标准签名分隔符
            break
        if s.startswith('>'):  # 历史引用行
            continue
        if re.match(r'^(On .+wrote:|在.+写道[:：]\s*|-------- Forwarded message --------|-------- 转发邮件 --------)$', s):
            break
        out.append(ln)
    return '\n'.join(out).rstrip()


def _extract_ics(msg, tz):
    """仅解析 .ics 附件（text/calendar 或 *.ics），其余附件一律忽略。"""
    events = []
    for part in msg.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        fname = (part.get_filename() or '')
        ctype = part.get_content_type()
        if not (fname.lower().endswith('.ics') or ctype == 'text/calendar'):
            continue
        try:
            # 用原始字节自行按 UTF-8 解码（RFC5545 默认 UTF-8），
            # 避免 get_content() 依 MIME charset 推断导致中文乱码
            payload = part.get_payload(decode=True)
            if payload is None:
                payload = part.get_content()
            if isinstance(payload, bytes):
                payload = payload.decode('utf-8', errors='replace')
            events.extend(ics_parser.parse(payload, tz))
        except Exception:
            continue
    return events


def _connect(acct, password):
    try:
        if acct.get('ssl', True):
            m = imaplib.IMAP4_SSL(acct['host'], int(acct.get('port', 993)))
        else:
            m = imaplib.IMAP4(acct['host'], int(acct.get('port', 143)))
        m.login(acct['username'], password)
        return m
    except imaplib.IMAP4.error as e:
        raise AccountError('E_IMAP', '登录失败（%s）：%s' % (acct['username'], e),
                           hint='检查用户名与客户端专用密码；部分邮箱需先开启 IMAP 并生成授权码')
    except OSError as e:
        raise AccountError('E_IMAP', '无法连接 %s:%s：%s' % (acct['host'], acct.get('port', 993), e),
                           hint='检查网络与服务器地址/端口')


def _select(m, acct):
    typ, _ = m.select(acct.get('folder', 'INBOX'), readonly=True)
    if typ != 'OK':
        raise AccountError('E_IMAP', '文件夹不存在：%s' % acct.get('folder', 'INBOX'))
    uidvalidity = None
    try:
        _, uv = m.response('UIDVALIDITY')
        if uv and uv[0]:
            uidvalidity = int(uv[0])
    except Exception:
        pass
    return uidvalidity


def _search_uids(m, criteria):
    typ, data = m.uid('search', None, criteria)
    if typ != 'OK':
        raise AccountError('E_IMAP', 'UID 搜索失败')
    return sorted(int(x) for x in (data[0].split() if data and data[0] else []))


def _fetch_mail(m, uid, mail_cfg, tz):
    """取信并清洗。"""
    typ, data = m.uid('fetch', str(uid), '(BODY.PEEK[])')
    if typ != 'OK' or not data or data[0] is None:
        raise AccountError('E_IMAP', '读取邮件 UID %d 失败' % uid)
    raw = data[0][1]
    msg = email.message_from_bytes(raw, policy=policy.default)
    subject = _decode_hdr(msg.get('Subject'))
    from_hdr = _decode_hdr(msg.get('From'))
    date = ''
    try:
        date = parsedate_to_datetime(msg.get('Date')).astimezone(tz).isoformat(timespec='seconds')
    except Exception:
        pass
    body, truncated = _extract_body(msg, mail_cfg['max_body_chars'], mail_cfg['strip_signatures'])
    ics_events = _extract_ics(msg, tz) if mail_cfg.get('parse_ics_attachments') else []
    return {'uid': uid, 'subject': subject, 'from': from_hdr, 'date': date,
            'body': body, 'body_truncated': truncated, 'ics_events': ics_events}


def check(acct, password):
    """doctor 用：连通性 + 文件夹存在性检查。返回 UIDVALIDITY。"""
    m = _connect(acct, password)
    try:
        return _select(m, acct)
    finally:
        try:
            m.logout()
        except Exception:
            pass


def fetch_new(acct, password, last_uid, limit, mail_cfg, tz, backfill_days=0):
    """取 last_uid 之后的新邮件（最多 limit 封）。

    返回：{'uidvalidity', 'first_run', 'init_uid', 'has_more', 'mails', 'filtered'}
    first_run=True 表示游标未初始化：只初始化游标（backfill_days>0 时回溯），
    不返回待处理邮件。
    """
    m = _connect(acct, password)
    try:
        uidvalidity = _select(m, acct)
        all_uids = _search_uids(m, 'ALL')
        if last_uid <= 0:
            if backfill_days and backfill_days > 0:
                from datetime import datetime, timedelta
                since = (datetime.now(tz) - timedelta(days=backfill_days)).strftime('%d-%b-%Y')
                window = _search_uids(m, 'SINCE %s' % since)
                init = (min(window) - 1) if window else (max(all_uids) if all_uids else 0)
            else:
                init = max(all_uids) if all_uids else 0
            return {'uidvalidity': uidvalidity, 'first_run': True, 'init_uid': init,
                    'has_more': False, 'mails': [], 'filtered': []}
        new_uids = [u for u in _search_uids(m, 'UID %d:*' % (last_uid + 1)) if u > last_uid]
        batch = new_uids[:limit]
        has_more = len(new_uids) > limit
        mails, filtered = [], []
        for uid in batch:
            try:
                info = _fetch_mail(m, uid, mail_cfg, tz)
            except AccountError:
                raise
            if not _sender_allowed(acct, _addr_of(info['from']), info['from']):
                info['filtered'] = True
                filtered.append({'uid': uid, 'subject': info['subject'], 'from': info['from']})
                continue
            info['filtered'] = False
            mails.append(info)
        return {'uidvalidity': uidvalidity, 'first_run': False, 'init_uid': None,
                'has_more': has_more, 'mails': mails, 'filtered': filtered}
    finally:
        try:
            m.logout()
        except Exception:
            pass


def list_recent(acct, password, limit=10, from_filter=None):
    """交互式：最近 limit 封邮件的摘要（FR-09）。from_filter 为发件人子串。"""
    m = _connect(acct, password)
    try:
        _select(m, acct)
        uids = _search_uids(m, 'ALL')[-limit:]
        out = []
        for uid in reversed(uids):  # 新的在前
            typ, data = m.uid('fetch', str(uid), '(BODY.PEEK[HEADER.FIELDS (SUBJECT FROM DATE)])')
            if typ != 'OK' or not data or data[0] is None:
                continue
            msg = email.message_from_bytes(data[0][1], policy=policy.default)
            subject = _decode_hdr(msg.get('Subject'))
            from_hdr = _decode_hdr(msg.get('From'))
            if from_filter and from_filter.lower() not in (from_hdr or '').lower():
                continue
            out.append({'uid': uid, 'subject': subject, 'from': from_hdr, 'date': msg.get('Date', '')})
        return out
    finally:
        try:
            m.logout()
        except Exception:
            pass


def read_one(acct, password, uid, mail_cfg, tz):
    """交互式：读单封邮件（清洗后正文 + .ics 解析结果）。"""
    m = _connect(acct, password)
    try:
        _select(m, acct)
        return _fetch_mail(m, int(uid), mail_cfg, tz)
    finally:
        try:
            m.logout()
        except Exception:
            pass
