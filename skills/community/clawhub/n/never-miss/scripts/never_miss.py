#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""never-miss CLI — 唯一入口（架构设计 §4）。

约定：
- 成功：结构化 JSON 输出到 stdout，退出码 0
- 失败：{"error": {"code", "message", "hint"}} 输出到 stderr，退出码 1
- 数据目录：环境变量 NEVER_MISS_DATA > 默认 ~/.workbuddy/never-miss
- 秘密只经 stdin 进 Keychain，任何输出打码
"""
import argparse
import json
import os
import re
import sys
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import calendar_apple
import config
import fingerprint
import ics_parser
import imap_client
import journal
import keychain
import render
import state

WEEKDAYS = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(os.path.dirname(SCRIPT_DIR), 'assets', 'config.template.yaml')


def _out(obj):
    print(json.dumps(obj, ensure_ascii=False, indent=2))


def _fail(code, message, hint=None):
    sys.stderr.write(json.dumps(
        {'error': {'code': code, 'message': message, 'hint': hint}},
        ensure_ascii=False) + '\n')
    sys.exit(1)


def _cfg():
    try:
        return config.load(config.data_root())
    except config.ConfigError as e:
        _fail('E_CONFIG', str(e), e.hint)


def _tz(cfg):
    return ZoneInfo(cfg['timezone'])


def _fromiso(s, tz):
    """datetime.fromisoformat 兼容处理（'Z' 后缀 → +00:00；naive → 附加配置时区）。"""
    s = str(s).strip()
    if s.endswith('Z'):
        s = s[:-1] + '+00:00'
    dt = datetime.fromisoformat(s)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=tz)
    return dt


def _append_created(root, rec):
    with open(os.path.join(root, 'created.jsonl'), 'a', encoding='utf-8') as f:
        f.write(json.dumps(rec, ensure_ascii=False) + '\n')


# ---------- now / init / secret ----------

def cmd_now(args):
    cfg = _cfg()
    now = datetime.now(_tz(cfg))
    _out({'now': now.isoformat(timespec='seconds'), 'date': now.strftime('%Y-%m-%d'),
          'weekday': WEEKDAYS[now.weekday()], 'time': now.strftime('%H:%M'),
          'timezone': cfg['timezone']})


def cmd_init(args):
    root = config.data_root()
    for sub in ('runs', 'journal', 'ics'):
        os.makedirs(os.path.join(root, sub), exist_ok=True)
    cfg_path = config.config_path(root)
    created = not os.path.exists(cfg_path)
    if created:
        with open(TEMPLATE, 'r', encoding='utf-8') as f:
            with open(cfg_path, 'w', encoding='utf-8') as w:
                w.write(f.read())
    if not os.path.exists(os.path.join(root, 'state.json')):
        state.save(root, {'accounts': {}})
    _out({'data_dir': root, 'config': cfg_path, 'config_created': created,
          'next_steps': ['填写 config.yaml 的 accounts（可由 LLM 依对话填写）',
                         '运行 secret set <邮箱> 存入密码（stdin）',
                         '运行 doctor --write-test 逐项自检']})


def cmd_secret(args):
    email = args.email.strip().lower()
    if args.action == 'set':
        password = sys.stdin.readline().rstrip('\r\n')
        if not password:
            _fail('E_ARGS', '密码经 stdin 传入，不能为空')
        try:
            keychain.set_secret(email, password)
        except keychain.KeychainError as e:
            _fail(e.code, str(e), e.hint)
        _out({'ok': True, 'account': email, 'service': keychain.SERVICE,
              'stored': 'keychain', 'password_echo': '****'})
    elif args.action == 'check':
        try:
            exists = keychain.has_secret(email)
        except keychain.KeychainError as e:
            _fail(e.code, str(e), e.hint)
        _out({'account': email, 'exists': exists})
    else:  # delete
        try:
            keychain.delete_secret(email)
        except keychain.KeychainError as e:
            _fail(e.code, str(e), e.hint)
        _out({'ok': True, 'account': email, 'deleted': True})


# ---------- doctor ----------

def cmd_doctor(args):
    root = config.data_root()
    cfg = _cfg()
    tz = _tz(cfg)
    result = {'data_dir': root, 'platform': sys.platform}
    local = datetime.now().astimezone().utcoffset()
    cfgoff = datetime.now(tz).utcoffset()
    result['timezone'] = {
        'config': cfg['timezone'], 'system_match': local == cfgoff,
        'hint': None if local == cfgoff else
        '系统时区与配置时区不一致，日历事件时间会偏移，建议统一为 %s' % cfg['timezone'],
    }
    result['accounts'] = []
    accounts = config.enabled_accounts(cfg)
    if not accounts:
        result['accounts_hint'] = '未配置任何启用账户；对话式配置后写入 config.yaml'
    for acct in accounts:
        email = acct['username'].lower()
        item = {'account': email, 'label': acct['label']}
        try:
            if not keychain.has_secret(email):
                item.update({'keychain': 'missing', 'imap': 'skipped',
                             'hint': '运行 secret set %s，密码经 stdin 传入' % email})
                result['accounts'].append(item)
                continue
            item['keychain'] = 'ok'
            password = keychain.get_secret(email)
            imap_client.check(acct, password)
            item['imap'] = 'ok'
        except (keychain.KeychainError, imap_client.AccountError) as e:
            item['imap'] = 'error'
            item['error'] = {'code': getattr(e, 'code', 'E_IMAP'), 'message': str(e),
                             'hint': getattr(e, 'hint', None)}
        result['accounts'].append(item)
    disabled = [a['username'].lower() for a in (cfg.get('accounts') or [])
                if not a.get('enabled', True)]
    if disabled:
        result['disabled_accounts'] = disabled
    cal = {'name': cfg['calendar']['name']}
    if sys.platform == 'darwin':
        try:
            r = calendar_apple.ensure_calendar(
                cfg['calendar']['name'],
                cfg['calendar'].get('location') == 'icloud')
            cal.update({'exists': True, 'source': r['source'], 'created_this_run': r['created']})
            if args.write_test:
                calendar_apple.write_test(cfg['calendar']['name'])
                cal['write_test'] = 'ok（已写入并删除测试事件）'
        except calendar_apple.CalendarError as e:
            cal['error'] = {'code': e.code, 'message': str(e), 'hint': e.hint}
            if args.write_test:
                cal['write_test'] = 'skipped'
    else:
        cal['error'] = {'code': 'E_UNSUPPORTED', 'message': '非 macOS，无法访问日历',
                        'hint': '仅可生成 .ics 供手动导入'}
    result['calendar'] = cal
    result['ok'] = bool(
        result['timezone']['system_match']
        and accounts
        and all(a.get('imap') == 'ok' for a in result['accounts'])
        and 'error' not in cal)
    _out(result)


# ---------- create / check-conflict ----------

def cmd_create(args):
    root = config.data_root()
    cfg = _cfg()
    tz = _tz(cfg)
    try:
        ev = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        _fail('E_ARGS', 'stdin 不是合法 JSON：%s' % e)
    if not isinstance(ev, dict):
        _fail('E_ARGS', 'stdin 应为 Event JSON 对象')
    title = str(ev.get('title') or '').strip().replace('\n', ' ')
    if not title:
        _fail('E_ARGS', '缺少必需字段：title')
    if not ev.get('start'):
        _fail('E_ARGS', '缺少必需字段：start（ISO 8601；全天事件为 YYYY-MM-DD）')
    all_day = bool(ev.get('all_day'))
    location = str(ev.get('location') or '').strip()
    attendees = [str(a) for a in (ev.get('attendees') or [])]
    src = ev.get('source') or {}
    src_account = (src.get('account') or '').strip().lower()
    src_subject = str(src.get('mail_subject') or '')
    src_mail_uid = src.get('mail_uid')
    lead = int(ev.get('reminder_lead_minutes') or cfg['reminder']['lead_minutes'])

    # 时间规范化（NFR-01：时间必须准；缺失 end 用合理默认）
    try:
        if all_day or re.fullmatch(r'\d{4}-\d{2}-\d{2}', str(ev['start'])):
            all_day = True
            start_day = str(ev['start'])[:10]
            end_day = str(ev.get('end') or '')[:10] or start_day
            if end_day < start_day:
                end_day = start_day
            start_dt = _fromiso(start_day, tz)
            end_dt = _fromiso(end_day, tz)
            canon = {'start': start_day, 'end': end_day, 'all_day': True}
        else:
            start_dt = _fromiso(ev['start'], tz)
            end_raw = ev.get('end')
            if end_raw:
                end_dt = _fromiso(end_raw, tz)
                if end_dt <= start_dt:
                    end_dt = start_dt + timedelta(hours=1)
            else:
                end_dt = start_dt + timedelta(hours=1)
            canon = {'start': start_dt.isoformat(), 'end': end_dt.isoformat(), 'all_day': False}
    except ValueError as e:
        _fail('E_ARGS', '时间字段无法解析：%s（应为 ISO 8601，如 2026-09-12T10:00:00+08:00）' % e)

    uid = fingerprint.uid_of(title, canon['start'], location)
    base = cfg['calendar']['name']
    cal = base
    src_acct = config.account_by_email(cfg, src_account) if src_account else None
    if cfg['calendar'].get('per_account') and src_acct:
        cal = '%s - %s' % (base, src_acct['label'])
    desc_lines = ['[never-miss] uid:%s' % uid]
    if src_account:
        desc_lines.append('来源：%s（%s）' % (src_acct['label'] if src_acct else '?', src_account))
    else:
        desc_lines.append('来源：对话输入')
    if src_subject:
        desc_lines.append('邮件：%s' % src_subject)
    if attendees:
        desc_lines.append('参与者：%s' % '、'.join(attendees))
    description = '\n'.join(desc_lines)

    ev_echo = dict(canon)
    ev_echo.update({'title': title, 'location': location, 'attendees': attendees,
                    'reminder_lead_minutes': lead, 'uid': uid, 'calendar': cal,
                    'source': {'account': src_account or None,
                               'mail_subject': src_subject or None,
                               'mail_uid': src_mail_uid}})

    def journal_add(action, **kw):
        if args.journal:
            rec = {'action': action, 'account': src_account or '对话输入',
                   'mail_uid': src_mail_uid, 'uid': uid, 'title': title,
                   'start': canon['start']}
            rec.update(kw)
            journal.append(root, rec)

    force_ics = os.environ.get('NEVER_MISS_FORCE_ICS') == '1'
    status, conflicts, ics_path, degraded = 'created', [], None, None

    if sys.platform == 'darwin' and not force_ics:
        try:
            # 查重（跨账户去重，NFR-04）
            if calendar_apple.find_uid(base, uid) > 0:
                journal_add('duplicate')
                _out({'status': 'duplicate', 'uid': uid, 'calendar': cal, 'conflicts': [],
                      'event': ev_echo,
                      'note': '日历中已存在同 UID 事件（重复或跨账户重复），未重复创建'})
                return
            calendar_apple.ensure_calendar(cal, cfg['calendar'].get('location') == 'icloud')
            conflicts = calendar_apple.check_conflict(start_dt, end_dt, exclude_uid=uid)
            calendar_apple.create_event(cal, title, start_dt, end_dt, all_day, description,
                                        location, lead, cfg['reminder']['all_day_at'])
        except calendar_apple.CalendarError as e:
            # 降级链（FR-33/34）：日历不可写 → .ics
            degraded = {'code': e.code, 'message': str(e), 'hint': e.hint}
            status = 'ics_fallback'
    else:
        status = 'ics_fallback'
        degraded = None if force_ics else {
            'code': 'E_UNSUPPORTED',
            'message': '非 macOS 环境：不支持自动写入日历，仅生成 .ics 供手动导入',
            'hint': '需求 FR-34'}

    if status == 'ics_fallback':
        fname = '%s-%s.ics' % (uid.split('@')[0], re.sub(r'[^\w\-]+', '_', title)[:24].strip('_'))
        ics_path = os.path.join(root, 'ics', fname)
        try:
            ics_parser.write_ics(
                ics_path,
                {'title': title, 'start': canon['start'] if all_day else start_dt,
                 'end': canon['end'] if all_day else end_dt,
                 'all_day': all_day, 'location': location, 'description': description},
                uid, tz, lead, cfg['reminder']['all_day_at'])
        except Exception as e2:
            _fail('E_CALENDAR',
                  '日历写入失败且 .ics 生成失败：%s；%s' % (degraded and degraded['message'], e2),
                  degraded and degraded['hint'])

    _append_created(root, {
        'ts': datetime.now(tz).isoformat(timespec='seconds'), 'uid': uid, 'title': title,
        'start': canon['start'], 'end': canon['end'], 'all_day': all_day, 'calendar': cal,
        'status': status,
        'source': {'account': src_account or None, 'mail_subject': src_subject or None}})
    journal_add('create', conflicts=len(conflicts),
                detail=('ics_fallback: %s' % ics_path) if ics_path else None)
    _out({'status': status, 'uid': uid, 'calendar': cal, 'conflicts': conflicts,
          'ics_path': ics_path, 'degraded_reason': degraded, 'event': ev_echo,
          'note': ('创建成功；必须向用户复述完整详情（绝对时间）' if status == 'created' else
                   '已降级生成 .ics，提示用户双击导入' if status == 'ics_fallback' else None)})


def cmd_check_conflict(args):
    cfg = _cfg()
    tz = _tz(cfg)
    try:
        start = _fromiso(args.start, tz)
        end = _fromiso(args.end, tz)
    except ValueError as e:
        _fail('E_ARGS', '时间无法解析：%s' % e)
    if end <= start:
        end = start + timedelta(hours=1)
    try:
        conflicts = calendar_apple.check_conflict(start, end)
    except calendar_apple.CalendarError as e:
        _fail(e.code, str(e), e.hint)
    _out({'conflicts': conflicts})


# ---------- mail（交互式读信，FR-09） ----------

def _pick_accounts(cfg, account_flag, allow_multi=False):
    if account_flag:
        acct = config.account_by_email(cfg, account_flag)
        if not acct:
            _fail('E_ARGS', '账户不存在：%s' % account_flag)
        return [acct]
    accts = config.enabled_accounts(cfg)
    if not accts:
        _fail('E_CONFIG', '未配置任何启用账户')
    if len(accts) > 1 and not allow_multi:
        _fail('E_ARGS', '配置了多个账户，请用 --account 指定其一')
    return accts


def cmd_mail(args):
    cfg = _cfg()
    tz = _tz(cfg)
    if args.action == 'list':
        result = []
        for acct in _pick_accounts(cfg, args.account, allow_multi=True):
            email = acct['username'].lower()
            try:
                password = keychain.get_secret(email)
                mails = imap_client.list_recent(acct, password,
                                                limit=args.limit or 10,
                                                from_filter=args.from_filter)
            except (keychain.KeychainError, imap_client.AccountError) as e:
                result.append({'account': email, 'label': acct['label'],
                               'error': {'code': getattr(e, 'code', 'E_IMAP'), 'message': str(e)}})
                continue
            result.append({'account': email, 'label': acct['label'], 'mails': mails})
        _out({'accounts': result})
    else:  # read
        if not args.uid:
            _fail('E_ARGS', 'mail read 需要 --uid')
        acct = _pick_accounts(cfg, args.account)[0]
        email = acct['username'].lower()
        try:
            password = keychain.get_secret(email)
            info = imap_client.read_one(acct, password, args.uid, cfg['mail'], tz)
        except (keychain.KeychainError, imap_client.AccountError) as e:
            _fail(getattr(e, 'code', 'E_IMAP'), str(e), getattr(e, 'hint', None))
        _out(info)


# ---------- scan（自动模式，FR-24~29） ----------

def cmd_scan(args):
    root = config.data_root()
    if args.action == 'fetch':
        cmd_scan_fetch(args, root)
    else:
        cmd_scan_commit(args, root)


def cmd_scan_fetch(args, root):
    cfg = _cfg()
    tz = _tz(cfg)
    st = state.load(root)
    if args.account:
        acct = config.account_by_email(cfg, args.account)
        if not acct:
            _fail('E_ARGS', '账户不存在：%s' % args.account)
        accts = [acct] if acct.get('enabled', True) else []
    else:
        accts = config.enabled_accounts(cfg)
    accounts_out = []
    for acct in accts:
        email = acct['username'].lower()
        entry = {'account': email, 'label': acct['label']}
        try:
            password = keychain.get_secret(email)
        except keychain.KeychainError as e:
            journal.append(root, {'action': 'error', 'account': email,
                                  'code': 'E_KEYCHAIN', 'message': str(e)})
            entry.update({'status': 'error', 'cursor_moved': False,
                          'error': {'code': 'E_KEYCHAIN', 'message': str(e), 'hint': e.hint}})
            accounts_out.append(entry)
            continue  # 单账户失败不影响其他账户（NFR-08）
        cur = st.get('accounts', {}).get(email, {})
        try:
            r = imap_client.fetch_new(acct, password, cur.get('last_uid', 0),
                                      acct['max_per_run'], cfg['mail'], tz,
                                      acct.get('backfill_days', 0))
        except imap_client.AccountError as e:
            journal.append(root, {'action': 'error', 'account': email,
                                  'code': e.code, 'message': str(e)})
            entry.update({'status': 'error', 'cursor_moved': False,
                          'error': {'code': e.code, 'message': str(e), 'hint': e.hint}})
            accounts_out.append(entry)
            continue
        uv = r['uidvalidity']
        if r['first_run']:
            state.advance(st, email, r['init_uid'], uv)
            state.save(root, st)
            journal.append(root, {'action': 'run', 'account': email,
                                  'new_mail_count': 0, 'first_run': True})
            entry.update({'status': 'ok', 'first_run': True,
                          'cursor_initialized_to': r['init_uid'],
                          'mails': [], 'has_more': False})
            accounts_out.append(entry)
            continue
        stored_uv = cur.get('uidvalidity')
        if stored_uv is not None and uv is not None and uv != stored_uv:
            st.setdefault('accounts', {})[email] = {'last_uid': 0, 'uidvalidity': uv, 'last_run': None}
            state.save(root, st)
            journal.append(root, {'action': 'error', 'account': email, 'code': 'E_STATE',
                                  'message': 'UIDVALIDITY 变化（邮箱重建），游标已重置，下次运行重新初始化'})
            entry.update({'status': 'error', 'cursor_moved': False,
                          'error': {'code': 'E_STATE',
                                    'message': 'UIDVALIDITY 变化，游标已重置，下次运行重新初始化'}})
            accounts_out.append(entry)
            continue
        journal.append(root, {'action': 'run', 'account': email,
                              'new_mail_count': len(r['mails']) + len(r['filtered'])})
        for f in r['filtered']:
            journal.append(root, {'action': 'skip', 'account': email,
                                  'mail_uid': f['uid'], 'reason': 'SENDER_FILTERED',
                                  'detail': f['from']})
        for info in r['mails']:
            journal.append(root, {'action': 'fetched', 'account': email,
                                  'mail_uid': info['uid'], 'subject': info['subject']})
        entry.update({'status': 'ok', 'fetched': len(r['mails']),
                      'filtered': len(r['filtered']), 'has_more': r['has_more'],
                      'limit': acct['max_per_run'], 'mails': r['mails']})
        accounts_out.append(entry)
    _out({'accounts': accounts_out,
          'note': '游标本轮未推进；逐封处理（create --journal / journal skip / journal error）后执行 scan commit'})


def cmd_scan_commit(args, root):
    cfg = _cfg()
    st = state.load(root)
    recs = journal.records(root)
    by_acct = {}
    for r in recs:
        by_acct.setdefault(r.get('account') or '对话输入', []).append(r)
    results = []
    total = {'created': 0, 'duplicate': 0, 'skipped': 0, 'errors': 0}
    for email, rs in by_acct.items():
        entry = {'account': email}
        if email == '对话输入' or not any(r.get('action') == 'run' for r in rs):
            entry['advanced'] = False
            entry['reason'] = '本次无成功扫描（错误或非扫描记录），游标未动'
            results.append(entry)
            continue
        fetched_uids = [r['mail_uid'] for r in rs if r.get('action') == 'fetched']
        terminal = {r['mail_uid'] for r in rs
                    if r.get('action') in ('create', 'duplicate', 'skip', 'error')
                    and r.get('mail_uid') is not None}
        pending = [u for u in fetched_uids if u not in terminal]
        counts = {'created': sum(1 for r in rs if r.get('action') == 'create'),
                  'duplicate': sum(1 for r in rs if r.get('action') == 'duplicate'),
                  'skipped': sum(1 for r in rs if r.get('action') == 'skip'),
                  'errors': sum(1 for r in rs if r.get('action') == 'error')}
        for k in total:
            total[k] += counts[k]
        entry.update(counts)
        if pending:
            entry.update({'advanced': False, 'pending': pending,
                          'reason': '存在未处理完的邮件，游标未推进（下次重新处理）'})
            results.append(entry)
            continue
        cur = state.account(st, email)
        batch_uids = [r['mail_uid'] for r in rs
                      if r.get('action') in ('fetched', 'create', 'duplicate', 'skip')
                      and r.get('mail_uid') is not None]
        new_last = max([cur.get('last_uid') or 0] + batch_uids)
        state.advance(st, email, new_last, cur.get('uidvalidity'))
        entry.update({'advanced': True, 'new_last_uid': new_last})
        results.append(entry)
    summary = {'ts': datetime.now().astimezone().isoformat(timespec='seconds')}
    summary.update(total)
    st['last_run_summary'] = summary
    st['report_pending'] = True
    state.save(root, st)
    md = render.render(cfg, recs)
    report_path = render.write_report(root, md)
    journal.clear(root)
    _out({'accounts': results, 'summary': total, 'report': report_path,
          'report_pending': True,
          'note': '运行报告已落盘；下次对话时向用户汇报（query status 读取后清除待汇报标记）'})


# ---------- journal ----------

def cmd_journal(args):
    root = config.data_root()
    if args.action == 'skip':
        if not args.reason:
            _fail('E_ARGS', 'journal skip 需要 --reason（NO_SCHEDULE/AMBIGUOUS/MISSING_TIME/LOW_CONFIDENCE）')
        journal.append(root, {'action': 'skip', 'account': args.account,
                              'mail_uid': args.uid, 'reason': args.reason, 'detail': args.detail})
        _out({'ok': True})
    else:
        if not (args.code and args.message):
            _fail('E_ARGS', 'journal error 需要 --code 与 --message')
        journal.append(root, {'action': 'error', 'account': args.account,
                              'mail_uid': args.uid, 'code': args.code, 'message': args.message})
        _out({'ok': True})


# ---------- query（只读，FR-35~38） ----------

def _parse_desc_source(desc):
    src = {'account': None, 'label': None, 'mail_subject': None, 'uid': None}
    # flatText 已把换行压成 "|"，故同时按换行与 "|" 切分
    for ln in (desc or '').replace('\r', '\n').replace('|', '\n').split('\n'):
        ln = ln.strip()
        if ln.startswith('[never-miss] uid:'):
            src['uid'] = ln.split(':', 1)[1].strip()
        elif ln.startswith('来源：'):
            src['label'] = ln[3:].strip()
            m = re.search(r'（(.+)）', ln)
            src['account'] = m.group(1) if m else None
        elif ln.startswith('邮件：'):
            src['mail_subject'] = ln[3:].strip()
    return src


def cmd_query(args):
    root = config.data_root()
    cfg = _cfg()
    tz = _tz(cfg)
    if args.action == 'status':
        st = state.load(root)
        pending = bool(st.pop('report_pending', False))
        if pending:
            st['report_pending'] = False
            state.save(root, st)
        _out({'accounts': st.get('accounts', {}),
              'last_run_summary': st.get('last_run_summary'),
              'report_pending': pending,
              'report_hint': '存在未汇报的运行结果，请向用户汇报' if pending else None})
        return
    # events
    if args.created_days is not None:
        cutoff = datetime.now(tz) - timedelta(days=args.created_days)
        out = []
        path = os.path.join(root, 'created.jsonl')
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        rec = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    try:
                        if datetime.fromisoformat(rec['ts']) >= cutoff:
                            out.append(rec)
                    except (KeyError, ValueError):
                        continue
        out.sort(key=lambda r: r.get('ts', ''), reverse=True)
        _out({'range': '最近 %d 天创建' % args.created_days, 'count': len(out), 'events': out})
        return
    if args.from_date and args.to_date:
        try:
            f = _fromiso(args.from_date, tz)
            t = _fromiso(args.to_date, tz) + timedelta(days=1)  # to 当天全天包含
        except ValueError as e:
            _fail('E_ARGS', '日期无法解析：%s（应为 YYYY-MM-DD）' % e)
        try:
            events = calendar_apple.list_events(cfg['calendar']['name'], f, t)
        except calendar_apple.CalendarError as e:
            _fail(e.code, str(e), e.hint)
        for ev in events:
            ev['source'] = _parse_desc_source(ev.pop('description', ''))
        _out({'range': '%s 至 %s' % (args.from_date, args.to_date),
              'count': len(events), 'events': events})
        return
    _fail('E_ARGS', 'query events 需要 --created-days N 或 --from/--to（YYYY-MM-DD）')


# ---------- main ----------

def main():
    p = argparse.ArgumentParser(prog='never_miss.py', description='never-miss CLI（日程→macOS 日历管道）')
    sub = p.add_subparsers(dest='cmd', required=True)

    sub.add_parser('now').set_defaults(func=cmd_now)
    sub.add_parser('init').set_defaults(func=cmd_init)

    sp = sub.add_parser('secret')
    sp.add_argument('action', choices=['set', 'check', 'delete'])
    sp.add_argument('email')
    sp.set_defaults(func=cmd_secret)

    dp = sub.add_parser('doctor')
    dp.add_argument('--write-test', action='store_true')
    dp.set_defaults(func=cmd_doctor)

    cp = sub.add_parser('create')
    cp.add_argument('--journal', action='store_true',
                    help='自动模式下使用：同步写入运行流水')
    cp.set_defaults(func=cmd_create)

    kp = sub.add_parser('check-conflict')
    kp.add_argument('--start', required=True)
    kp.add_argument('--end', required=True)
    kp.set_defaults(func=cmd_check_conflict)

    mp = sub.add_parser('mail')
    mp.add_argument('action', choices=['list', 'read'])
    mp.add_argument('--account')
    mp.add_argument('--from', dest='from_filter')
    mp.add_argument('--limit', type=int, default=10)
    mp.add_argument('--uid', type=int)
    mp.set_defaults(func=cmd_mail)

    fp = sub.add_parser('scan')
    fp.add_argument('action', choices=['fetch', 'commit'])
    fp.add_argument('--account')
    fp.set_defaults(func=cmd_scan)

    jp = sub.add_parser('journal')
    jp.add_argument('action', choices=['skip', 'error'])
    jp.add_argument('--account', required=True)
    jp.add_argument('--uid', type=int)
    jp.add_argument('--reason')
    jp.add_argument('--detail')
    jp.add_argument('--code')
    jp.add_argument('--message')
    jp.set_defaults(func=cmd_journal)

    qp = sub.add_parser('query')
    qp.add_argument('action', choices=['events', 'status'])
    qp.add_argument('--created-days', type=int, dest='created_days')
    qp.add_argument('--from', dest='from_date')
    qp.add_argument('--to', dest='to_date')
    qp.set_defaults(func=cmd_query)

    args = p.parse_args()
    try:
        args.func(args)
    except KeyboardInterrupt:
        _fail('E_INTERNAL', '用户中断')


if __name__ == '__main__':
    main()
