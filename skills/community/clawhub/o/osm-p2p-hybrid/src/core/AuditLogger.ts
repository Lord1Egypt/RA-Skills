/**
 * AuditLogger - 审计日志
 * 记录所有进出消息，便于调试和追溯
 */

import { appendFile, mkdir } from 'fs/promises';
import { existsSync } from 'fs';
import { join } from 'path';
import type { AuditLogEntry, Envelope } from '../types.js';

export class AuditLogger {
  private enabled: boolean;
  private logPath: string;
  private buffer: AuditLogEntry[] = [];
  private flushTimer: NodeJS.Timeout | null = null;
  private bufferSize: number = 100;

  constructor(logPath: string, enabled: boolean = true) {
    this.logPath = logPath;
    this.enabled = enabled;

    if (enabled) {
      this.ensureDir();
      this.startFlushTimer();
    }
  }

  /**
   * 确保日志目录存在
   */
  private async ensureDir(): Promise<void> {
    const dir = this.logPath.substring(0, this.logPath.lastIndexOf('/')) || '.';
    if (!existsSync(dir)) {
      await mkdir(dir, { recursive: true });
    }
  }

  /**
   * 记录入站消息
   */
  logIncoming(envelope: Envelope, size: number): void {
    if (!this.enabled) return;

    const entry: AuditLogEntry = {
      ts: Date.now(),
      dir: 'in',
      peer: envelope.from.nodeId,
      room: envelope.to.type === 'room' ? envelope.to.target : undefined,
      type: envelope.payload.type,
      content: this.truncateContent(JSON.stringify(envelope.payload.data)),
      transport: envelope._transport || 'unknown',
      size,
    };

    this.buffer.push(entry);
    this.checkFlush();
  }

  /**
   * 记录出站消息
   */
  logOutgoing(envelope: Envelope, target: string, size: number): void {
    if (!this.enabled) return;

    const entry: AuditLogEntry = {
      ts: Date.now(),
      dir: 'out',
      peer: target,
      room: envelope.to.type === 'room' ? envelope.to.target : undefined,
      type: envelope.payload.type,
      content: this.truncateContent(JSON.stringify(envelope.payload.data)),
      transport: envelope._transport || 'unknown',
      size,
    };

    this.buffer.push(entry);
    this.checkFlush();
  }

  /**
   * 记录系统事件
   */
  logSystem(event: string, details?: Record<string, unknown>): void {
    if (!this.enabled) return;

    const entry: AuditLogEntry = {
      ts: Date.now(),
      dir: 'out',
      peer: 'system',
      type: 'system',
      content: details ? `${event}: ${JSON.stringify(details)}` : event,
      transport: 'local',
      size: 0,
    };

    this.buffer.push(entry);
    this.checkFlush();
  }

  /**
   * 检查是否需要刷新
   */
  private checkFlush(): void {
    if (this.buffer.length >= this.bufferSize) {
      this.flush();
    }
  }

  /**
   * 启动定时刷新
   */
  private startFlushTimer(): void {
    this.flushTimer = setInterval(() => {
      this.flush();
    }, 5000); // 每5秒刷新一次
  }

  /**
   * 刷新缓冲区到文件
   */
  private async flush(): Promise<void> {
    if (this.buffer.length === 0) return;

    const lines = this.buffer.map(entry => 
      JSON.stringify(entry)
    ).join('\n') + '\n';

    try {
      await appendFile(this.logPath, lines);
      this.buffer = [];
    } catch (e) {
      console.error('审计日志写入失败:', e);
    }
  }

  /**
   * 截断过长的内容
   */
  private truncateContent(content: string, maxLen: number = 500): string {
    if (content.length <= maxLen) return content;
    return content.substring(0, maxLen) + '... [truncated]';
  }

  /**
   * 停止日志服务
   */
  async stop(): Promise<void> {
    if (this.flushTimer) {
      clearInterval(this.flushTimer);
      this.flushTimer = null;
    }
    await this.flush();
  }
}
