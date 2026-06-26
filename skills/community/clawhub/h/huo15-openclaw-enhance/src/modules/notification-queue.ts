/**
 * 通知中心 — 内部事件队列，供仪表盘消费展示
 * 纯内部模块，不注册任何工具。
 */
import type Database from "better-sqlite3";
import type { NotificationQueue, NotificationLevel, NotificationSource, NotificationConfig } from "../types.js";
import {
  emitNotification,
  getRecentNotifications,
  getUnreadNotificationCount,
  markNotificationRead,
  pruneNotifications,
} from "../utils/sqlite-store.js";

export function createNotificationQueue(
  db: Database.Database,
  config?: NotificationConfig,
): NotificationQueue {
  const maxRetained = config?.maxRetained ?? 100;

  return {
    emit(agentId, level, source, title, detail) {
      emitNotification(db, agentId, level, source, title, detail);
      pruneNotifications(db, maxRetained);
    },
    getRecent(agentId?, limit?) {
      return getRecentNotifications(db, agentId, limit).map((row: any) => ({
        ...row,
        read: !!row.read,
      }));
    },
    getUnreadCount(agentId?) {
      return getUnreadNotificationCount(db, agentId);
    },
    markRead(id) {
      markNotificationRead(db, id);
    },
    prune(max) {
      pruneNotifications(db, max);
    },
  };
}
