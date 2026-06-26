/**
 * Odoo SyncUpdate → NotificationEnvelope 转换
 *
 * 把 poller 产出的判别联合事件标准化成跨渠道统一的信封格式，
 * 让下游渠道（企微、钉钉 …）只针对 NotificationEnvelope 编程。
 */

import type {
  SyncUpdate,
  NotificationEnvelope,
  NotificationPriority,
} from '../types/index.js';

function priorityFromOdoo(raw: unknown): NotificationPriority {
  const s = String(raw ?? '0');
  if (s === '3') return 'urgent';
  if (s === '2') return 'high';
  if (s === '1') return 'normal';
  return 'low';
}

function stripHtml(html: unknown): string {
  return String(html ?? '').replace(/<[^>]+>/g, '').replace(/\s+/g, ' ').trim();
}

function truncate(s: string, n: number): string {
  return s.length <= n ? s : s.substring(0, n - 1) + '…';
}

function odooLink(odooUrl: string | undefined, model: string, id: number): { url: string; label?: string } | undefined {
  if (!odooUrl) return undefined;
  return { url: `${odooUrl.replace(/\/$/, '')}/odoo/action-base.action_open_view?model=${encodeURIComponent(model)}&id=${id}`, label: '在辉火云中打开' };
}

/**
 * 把 SyncUpdate 转成 NotificationEnvelope
 *
 * @param update  poller 产出的事件
 * @param agentId 所属 OpenClaw agent
 * @param odooUrl Odoo 实例 URL（用于构造 deep-link）
 */
export function toEnvelope(
  update: SyncUpdate,
  agentId: string,
  odooUrl?: string,
): NotificationEnvelope {
  const d = update.data as Record<string, unknown>;
  const id = `odoo:${agentId}:${update.type}:${update.id}`;
  const createdAt = Date.now();

  switch (update.type) {
    case 'todo': {
      const name = String(d['name'] ?? '(未命名待办)');
      const deadline = typeof d['date_deadline'] === 'string' ? d['date_deadline'] : '';
      const priority = priorityFromOdoo(d['priority']);
      const title = update.action === 'create' ? `新待办：${name}` : `待办更新：${name}`;
      const summary = deadline ? `${name}（截止 ${deadline}）` : name;
      return {
        id,
        source: 'odoo',
        agentId,
        kind: 'todo',
        action: update.action,
        priority,
        title,
        summary,
        body: deadline ? `${name}\n截止：${deadline}` : name,
        link: odooLink(odooUrl, 'project.task', update.id),
        tags: ['odoo', 'todo', update.action],
        createdAt,
        origin: { url: odooUrl, model: 'project.task', resId: update.id },
        raw: d,
      };
    }

    case 'activity': {
      const summaryText = String(d['summary'] ?? '活动');
      const deadline = String(d['date_deadline'] ?? '');
      const resModel = String(d['res_model'] ?? '');
      const resId = Number(d['res_id'] ?? 0);
      return {
        id,
        source: 'odoo',
        agentId,
        kind: 'activity',
        action: update.action,
        priority: 'high',
        title: `活动到期：${summaryText}`,
        summary: deadline ? `${summaryText}（${deadline}）` : summaryText,
        body: [
          summaryText,
          deadline ? `截止：${deadline}` : '',
          resModel ? `关联：${resModel}#${resId}` : '',
        ].filter(Boolean).join('\n'),
        link: resModel && resId ? odooLink(odooUrl, resModel, resId) : undefined,
        tags: ['odoo', 'activity', 'due'],
        createdAt,
        origin: { url: odooUrl, model: resModel, resId },
        raw: d,
      };
    }

    case 'message': {
      const subject = String(d['subject'] ?? '(无主题)');
      const bodyText = truncate(stripHtml(d['body']), 500);
      const authorArr = d['author_id'];
      const authorName = Array.isArray(authorArr) ? String(authorArr[1] ?? '系统') : '系统';
      const model = String(d['model'] ?? '');
      const resId = Number(d['res_id'] ?? 0);
      return {
        id,
        source: 'odoo',
        agentId,
        kind: 'message',
        action: update.action,
        priority: 'normal',
        title: `新消息：${subject}`,
        summary: `${authorName}：${truncate(bodyText || subject, 80)}`,
        body: bodyText,
        link: model && resId ? odooLink(odooUrl, model, resId) : undefined,
        tags: ['odoo', 'message'],
        createdAt,
        origin: { url: odooUrl, model, resId },
        raw: d,
      };
    }

    case 'email': {
      return {
        id,
        source: 'odoo',
        agentId,
        kind: 'email',
        action: update.action,
        priority: 'normal',
        title: '新邮件通知',
        summary: `您有一条新的辉火云邮件通知（id=${update.id}）`,
        body: `辉火云邮件通知\nnotification_id: ${update.id}`,
        tags: ['odoo', 'email'],
        createdAt,
        origin: { url: odooUrl, model: 'mail.notification', resId: update.id },
        raw: d,
      };
    }

    case 'calendar': {
      const name = String(d['name'] ?? '日历事件');
      const start = String(d['start'] ?? '');
      const stop = String(d['stop'] ?? '');
      return {
        id,
        source: 'odoo',
        agentId,
        kind: 'calendar',
        action: update.action,
        priority: 'normal',
        title: update.action === 'create' ? `新日历事件：${name}` : `日历更新：${name}`,
        summary: start ? `${name}（${start}）` : name,
        body: [name, start ? `开始：${start}` : '', stop ? `结束：${stop}` : ''].filter(Boolean).join('\n'),
        link: odooLink(odooUrl, 'calendar.event', update.id),
        tags: ['odoo', 'calendar', update.action],
        createdAt,
        origin: { url: odooUrl, model: 'calendar.event', resId: update.id },
        raw: d,
      };
    }
  }
}
