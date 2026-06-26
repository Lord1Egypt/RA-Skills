/**
 * Odoo 通知轮询服务
 *
 * 定期轮询 Odoo，检测待办/活动/消息/邮件/日历的变化，
 * 将更新通知 OpenClaw 用户。
 *
 * 改进点（相比 dev 版）：
 * - 消息去重使用 highWaterMessageId（高水位线 id），不依赖 write_date 时间戳
 * - 每轮 poll 前调用 ensureAuthenticated()，应对 Odoo 服务重启
 * - 支持可选的 email / calendar 通道
 */

import type { OdooClient } from './odoo-client.js';
import type { SyncUpdate } from '../types/index.js';
import { today, daysFromNow } from '../utils/date-utils.js';

type DomainItem = string | [string, string, unknown];
type Domain = DomainItem[];

export type NotificationCallback = (updates: SyncUpdate[]) => void;

export class NotificationPoller {
  private client: OdooClient;
  private intervalId: ReturnType<typeof setInterval> | null = null;
  private callback: NotificationCallback | null = null;
  private intervalSeconds: number = 30;
  private channels: string[] = ['todo', 'activity', 'message'];
  private lastCheck: Date = new Date();

  // 去重状态
  private seenTaskIds: Set<number> = new Set();
  private highWaterMessageId: number = 0;       // mail.message 高水位线
  private highWaterEmailId: number = 0;         // mail.notification 高水位线
  private seenCalendarIds: Set<number> = new Set();

  constructor(client: OdooClient) {
    this.client = client;
  }

  /** 启动轮询 */
  start(
    callback: NotificationCallback,
    options: { intervalSeconds?: number; channels?: string[] } = {},
  ): void {
    this.callback = callback;
    this.intervalSeconds = options.intervalSeconds ?? 30;
    this.channels = options.channels ?? ['todo', 'activity', 'message'];

    // 立即执行一次初始同步（静默，不推送，仅建立基准水位）
    this.initBaseline().catch(() => void 0);

    this.intervalId = setInterval(() => {
      this.poll().catch(() => void 0);
    }, this.intervalSeconds * 1000);
  }

  /** 停止轮询 */
  stop(): void {
    if (this.intervalId) {
      clearInterval(this.intervalId);
      this.intervalId = null;
    }
    this.callback = null;
  }

  /** 手动触发一次同步（返回发现的更新） */
  async poll(): Promise<SyncUpdate[]> {
    try {
      await this.client.ensureAuthenticated();
    } catch {
      return [];
    }

    const updates: SyncUpdate[] = [];

    for (const channel of this.channels) {
      try {
        switch (channel) {
          case 'todo':
            updates.push(...await this.checkTodos());
            break;
          case 'activity':
            updates.push(...await this.checkActivities());
            break;
          case 'message':
            updates.push(...await this.checkMessages());
            break;
          case 'email':
            updates.push(...await this.checkEmails());
            break;
          case 'calendar':
            updates.push(...await this.checkCalendar());
            break;
        }
      } catch {
        // 单个通道失败不影响其他通道
      }
    }

    this.lastCheck = new Date();

    if (updates.length > 0 && this.callback) {
      this.callback(updates);
    }

    return updates;
  }

  /** 获取轮询状态 */
  getStatus(): { running: boolean; lastCheck: Date; channels: string[] } {
    return {
      running: this.intervalId !== null,
      lastCheck: this.lastCheck,
      channels: this.channels,
    };
  }

  // ==================== 私有方法 ====================

  /**
   * 初始化基准水位线（首次启动时静默读取当前状态，后续只推送新增内容）
   */
  private async initBaseline(): Promise<void> {
    try {
      await this.client.ensureAuthenticated();
    } catch {
      return;
    }

    // 建立 task 基准
    try {
      const uid = this.client.getUid() ?? 0;
      const tasks = await this.client.searchRead(
        'project.task',
        [['user_ids', 'in', [uid]], ['active', '=', true]],
        ['id'],
        { limit: 200 },
      );
      for (const t of tasks.records) {
        this.seenTaskIds.add(t['id'] as number);
      }
    } catch { /* ignore */ }

    // 建立 message 高水位
    try {
      const msgs = await this.client.searchRead(
        'mail.message',
        [['message_type', '!=', 'notification']],
        ['id'],
        { limit: 1, order: 'id desc' },
      );
      if (msgs.records.length > 0) {
        this.highWaterMessageId = msgs.records[0]!['id'] as number;
      }
    } catch { /* ignore */ }

    // 建立 email 高水位
    try {
      const emails = await this.client.searchRead(
        'mail.notification',
        [['notification_type', '=', 'inbox']],
        ['id'],
        { limit: 1, order: 'id desc' },
      );
      if (emails.records.length > 0) {
        this.highWaterEmailId = emails.records[0]!['id'] as number;
      }
    } catch { /* ignore */ }

    // 建立 calendar 基准
    try {
      const events = await this.client.searchRead(
        'calendar.event',
        [['start', '>=', today()]],
        ['id'],
        { limit: 100 },
      );
      for (const e of events.records) {
        this.seenCalendarIds.add(e['id'] as number);
      }
    } catch { /* ignore */ }

    this.lastCheck = new Date();
  }

  /** 检查待办任务新增/更新 */
  private async checkTodos(): Promise<SyncUpdate[]> {
    const updates: SyncUpdate[] = [];
    const uid = this.client.getUid() ?? 0;

    const lastCheckStr = this.lastCheck.toISOString().replace('T', ' ').substring(0, 19);
    const domain: Domain = [
      ['user_ids', 'in', [uid]],
      ['active', '=', true],
      ['write_date', '>', lastCheckStr],
    ];

    const tasks = await this.client.searchRead(
      'project.task',
      domain,
      ['id', 'name', 'stage_id', 'date_deadline', 'priority'],
      { limit: 30 },
    );

    for (const task of tasks.records) {
      const taskId = task['id'] as number;
      const action = this.seenTaskIds.has(taskId) ? 'update' : 'create';
      this.seenTaskIds.add(taskId);
      updates.push({ type: 'todo', action, id: taskId, data: task, timestamp: Date.now() });
    }

    return updates;
  }

  /** 检查今日及逾期活动提醒 */
  private async checkActivities(): Promise<SyncUpdate[]> {
    const updates: SyncUpdate[] = [];
    const uid = this.client.getUid() ?? 0;

    const activities = await this.client.searchRead(
      'mail.activity',
      [
        ['user_id', '=', uid],
        ['date_deadline', '<=', today()],
        ['date_deadline', '>=', daysFromNow(-1)],
      ],
      ['id', 'summary', 'date_deadline', 'activity_type_id', 'res_model', 'res_id'],
      { limit: 20 },
    );

    for (const activity of activities.records) {
      updates.push({
        type: 'activity',
        action: 'due',
        id: activity['id'] as number,
        data: activity,
        timestamp: Date.now(),
      });
    }

    return updates;
  }

  /** 检查新消息（使用 id 高水位线去重） */
  private async checkMessages(): Promise<SyncUpdate[]> {
    const updates: SyncUpdate[] = [];

    const messages = await this.client.searchRead(
      'mail.message',
      [
        ['message_type', '!=', 'notification'],
        ['id', '>', this.highWaterMessageId],
      ],
      ['id', 'subject', 'body', 'author_id', 'date', 'model', 'res_id'],
      { limit: 20, order: 'id asc' },
    );

    for (const message of messages.records) {
      const msgId = message['id'] as number;
      updates.push({ type: 'message', action: 'create', id: msgId, data: message, timestamp: Date.now() });
      if (msgId > this.highWaterMessageId) {
        this.highWaterMessageId = msgId;
      }
    }

    return updates;
  }

  /** 检查新邮件通知（使用 id 高水位线去重） */
  private async checkEmails(): Promise<SyncUpdate[]> {
    const updates: SyncUpdate[] = [];

    const emails = await this.client.searchRead(
      'mail.notification',
      [
        ['notification_type', '=', 'inbox'],
        ['is_read', '=', false],
        ['id', '>', this.highWaterEmailId],
      ],
      ['id', 'mail_message_id', 'notification_status', 'is_read'],
      { limit: 20, order: 'id asc' },
    );

    for (const email of emails.records) {
      const emailId = email['id'] as number;
      updates.push({ type: 'email', action: 'create', id: emailId, data: email, timestamp: Date.now() });
      if (emailId > this.highWaterEmailId) {
        this.highWaterEmailId = emailId;
      }
    }

    return updates;
  }

  /** 检查日历事件（今明两天范围内的新事件） */
  private async checkCalendar(): Promise<SyncUpdate[]> {
    const updates: SyncUpdate[] = [];

    const events = await this.client.searchRead(
      'calendar.event',
      [
        ['start', '>=', today()],
        ['start', '<=', daysFromNow(1)],
      ],
      ['id', 'name', 'start', 'stop', 'partner_ids'],
      { limit: 20 },
    );

    for (const event of events.records) {
      const eventId = event['id'] as number;
      const action = this.seenCalendarIds.has(eventId) ? 'update' : 'create';
      this.seenCalendarIds.add(eventId);
      updates.push({ type: 'calendar', action, id: eventId, data: event, timestamp: Date.now() });
    }

    return updates;
  }
}
