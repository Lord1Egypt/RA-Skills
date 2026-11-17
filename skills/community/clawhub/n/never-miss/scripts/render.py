# -*- coding: utf-8 -*-
"""journal → runs/YYYY-MM-DD.md 渲染（需求 §6.6 格式）。"""
import os
from datetime import datetime

from config import account_by_email

SKIP_LABELS = {
    'NO_SCHEDULE': '无日程信息',
    'AMBIGUOUS': '时间表述模糊',
    'MISSING_TIME': '缺开始时间',
    'LOW_CONFIDENCE': '置信度不足',
    'SENDER_FILTERED': '发件人过滤',
}


def _fmt_start(start_iso):
    """'2026-09-12T10:00:00+08:00' → '9/12 10:00'；纯日期 → '9/12'。"""
    try:
        dt = datetime.fromisoformat(str(start_iso))
        if str(start_iso) and len(str(start_iso)) == 10:
            return '%d/%d' % (dt.month, dt.day)
        return '%d/%d %02d:%02d' % (dt.month, dt.day, dt.hour, dt.minute)
    except ValueError:
        return str(start_iso)


def render(cfg, records):
    """把 journal 记录渲染为按账户分段的 markdown。"""
    by_acct = {}
    for r in records:
        by_acct.setdefault(r.get('account') or '未知账户', []).append(r)
    now = datetime.now()
    lines = ['# never-miss 运行报告 %s\n' % now.strftime('%Y-%m-%d')]
    if not by_acct:
        lines.append('- 无任何记录')
        return '\n'.join(lines) + '\n'
    for email, recs in by_acct.items():
        acct = account_by_email(cfg, email)
        label = acct['label'] if acct else '?'
        fetched = [r for r in recs if r.get('action') == 'fetched']
        created = [r for r in recs if r.get('action') == 'create']
        dup = [r for r in recs if r.get('action') == 'duplicate']
        skipped = [r for r in recs if r.get('action') == 'skip']
        errors = [r for r in recs if r.get('action') == 'error']
        processed = len(fetched) + len(skipped)  # 被过滤的邮件不进 fetched，直接记 skip
        lines.append('## 账户：%s（%s）' % (label, email))
        lines.append('- 新邮件 %d 封，处理 %d 封' % (processed, len(created) + len(dup) + len(skipped)))
        if created:
            items = []
            for r in created:
                s = '%s %s' % (_fmt_start(r.get('start')), r.get('title', '?'))
                if r.get('conflicts'):
                    s += '（与 %d 个已有日程冲突）' % r['conflicts']
                items.append(s)
            lines.append('- 新建 %d：%s' % (len(created), '；'.join(items)))
        if dup:
            items = '；'.join('%s %s' % (_fmt_start(r.get('start')), r.get('title', '?')) for r in dup)
            lines.append('- 重复/跨账户重复跳过 %d：%s' % (len(dup), items))
        if skipped:
            groups = {}
            for r in skipped:
                reason = r.get('reason', 'OTHER')
                key = SKIP_LABELS.get(reason, reason)
                if r.get('detail'):
                    key = '%s（%s）' % (key, r['detail'])
                groups[key] = groups.get(key, 0) + 1
            items = '；'.join('%s %d' % (k, v) for k, v in groups.items())
            lines.append('- 跳过 %d：%s' % (len(skipped), items))
        if errors:
            for r in errors:
                lines.append('- 失败：%s %s' % (r.get('code', '?'), r.get('message', '')))
        lines.append('')
    return '\n'.join(lines) + '\n'


def write_report(root, md):
    """写入 runs/YYYY-MM-DD.md；同日多次运行时追加。"""
    runs_dir = os.path.join(root, 'runs')
    os.makedirs(runs_dir, exist_ok=True)
    path = os.path.join(runs_dir, datetime.now().strftime('%Y-%m-%d') + '.md')
    if os.path.exists(path):
        with open(path, 'a', encoding='utf-8') as f:
            f.write('\n---\n\n' + md)
    else:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(md)
    return path
