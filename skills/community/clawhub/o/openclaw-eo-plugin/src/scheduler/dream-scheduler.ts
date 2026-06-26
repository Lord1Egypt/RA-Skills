/**
 * Dream Scheduler - Automates Dream Module triggers via cron
 * 
 * Part of the self-optimization loop:
 * Decision → Execute → Track → Score → Optimize → Evolve (Dream)
 * 
 * Provides:
 * - Daily Dream trigger (00:30)
 * - Idle-based Dream trigger (30min idle)
 * - Manual trigger interface
 */

import { cronManager, type CronJob } from './cron-manager.js';
import { logger } from '../utils/logger.js';

const DREAM_JOB_NAME = 'EO Dream Module - Daily Evolution';
const DREAM_SCHEDULE = '30 0 * * *'; // 00:30 daily
const DREAM_TIMEZONE = 'Asia/Shanghai';

export interface DreamSchedulerConfig {
  enabled: boolean;
  dailyTime?: string;       // HH:MM format, e.g., "00:30"
  idleTrigger?: boolean;    // Enable idle-based Dream trigger
  idleTimeoutMs?: number;  // Idle timeout in ms (default: 30 min)
  feishuChatId?: string;   // Feishu chat ID for Dream reports
}

export interface DreamResult {
  success: boolean;
  jobId?: string;
  message: string;
  error?: string;
}

const DEFAULT_CONFIG: DreamSchedulerConfig = {
  enabled: true,
  dailyTime: '00:30',
  idleTrigger: false,
  idleTimeoutMs: 1800000, // 30 minutes
};

/**
 * Dream Scheduler class
 */
export class DreamScheduler {
  private config: DreamSchedulerConfig;
  private dreamJobId: string | null = null;

  constructor(config: Partial<DreamSchedulerConfig> = {}) {
    this.config = { ...DEFAULT_CONFIG, ...config };
  }

  /**
   * Initialize the dream scheduler
   * Creates/updates the cron job for daily Dream trigger
   */
  async initialize(): Promise<DreamResult> {
    try {
      // Check if Dream job already exists
      const existingJobs = await cronManager.listJobs({ nameContains: 'Dream' });
      const existingDreamJob = existingJobs.find(j => j.name.includes('Dream Module'));

      if (existingDreamJob) {
        // Re-enable if it was disabled
        if (!existingDreamJob.enabled) {
          await cronManager.enableJob(existingDreamJob.id);
        }
        this.dreamJobId = existingDreamJob.id;
        return {
          success: true,
          jobId: existingDreamJob.id,
          message: `Found existing Dream job: ${existingDreamJob.id}`,
        };
      }

      // Create new Dream job
      const job = await cronManager.createJob({
        name: DREAM_JOB_NAME,
        description: 'Daily Dream Module evolution - analyzes sessions, extracts patterns, updates memory',
        enabled: true,
        schedule: {
          kind: 'cron',
          expr: DREAM_SCHEDULE,
          tz: DREAM_TIMEZONE,
        },
        sessionTarget: 'isolated',
        wakeMode: 'now',
        payload: {
          kind: 'agentTurn',
          message: this.buildDreamMessage(),
          timeoutSeconds: 300, // 5 min timeout
        },
        delivery: {
          mode: 'silent', // Don't announce Dream results
        },
      });

      this.dreamJobId = job.id;
      return {
        success: true,
        jobId: job.id,
        message: `Created Dream scheduler job: ${job.id}`,
      };
    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : String(error);
      console.error('[DreamScheduler] Initialization failed:', errorMsg);
      return {
        success: false,
        message: 'Failed to initialize Dream scheduler',
        error: errorMsg,
      };
    }
  }

  /**
   * Build the Dream Module trigger message
   */
  private buildDreamMessage(): string {
    return `🌙 Dream Module - Daily Evolution

请执行Dream Module的自我进化流程：

1. 分析今天的所有会话记录
2. 提取跨会话的pattern
3. 更新MEMORY.md（如果有重要发现）
4. 生成进化报告

使用 /eo_dream 触发。

完成后输出简短的进化报告。`;
  }

  /**
   * Manually trigger a Dream cycle
   */
  async triggerNow(feishuChatId?: string): Promise<DreamResult> {
    const chatId = feishuChatId || this.config.feishuChatId
    try {
      // Import dynamically to avoid circular deps
      const { DreamEngine } = await import('../dream/dream-engine.js');
      const dreamEngine = new DreamEngine(process.cwd());

      logger.info('Manual Dream trigger started');
      const result = await dreamEngine.executeDream({ type: 'manual' });

      if (result.success) {
        // Send Feishu notification if chat_id is configured
        if (chatId) {
          await this.sendDreamReport(result, chatId)
        }
        return {
          success: true,
          message: `Dream completed in ${result.durationMs}ms. Sessions analyzed: ${result.report?.sessionsAnalyzed || 0}`,
        };
      } else {
        return {
          success: false,
          message: 'Dream failed',
          error: result.error,
        };
      }
    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : String(error);
      console.error('[DreamScheduler] Manual trigger failed:', errorMsg);
      return {
        success: false,
        message: 'Failed to trigger Dream',
        error: errorMsg,
      };
    }
  }

  /**
   * Send Dream evolution report to Feishu
   */
  private async sendDreamReport(result: any, chatId: string): Promise<void> {
    try {
      // Dynamically import to avoid circular deps
      const { proactiveNotifier } = await import('../continuous/proactive-notifier.js')
      const report = result.report || {}
      const lines = [
        `🌙 Dream Module 进化报告`,
        ``,
        `• 分析会话：${report.sessionsAnalyzed || 0}个`,
        `• Pattern提取：${report.patternsExtracted || 0}个`,
        `• 记忆更新：${report.memoryUpdated ? '✅' : '❌'}`,
        `• 专家权重调整：${report.weightsAdjusted ? '✅' : '❌'}`,
        `• 进化耗时：${result.durationMs || 0}ms`,
        ``,
        `⏰ ${new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' })}`,
      ]
      await proactiveNotifier.notify(
        'success',
        '🌙 Dream 进化完成',
        lines.join('\n'),
        ['feishu'],
        { feishuChatId: chatId }
      )
    } catch (e) {
      console.error('[DreamScheduler] Feishu report send failed:', e)
    }
  }

  /**
   * Get the status of the Dream scheduler
   */
  async getStatus(): Promise<{
    configured: boolean;
    jobId: string | null;
    nextRun: string | null;
    lastRun: string | null;
    enabled: boolean;
  }> {
    const job = this.dreamJobId
      ? await cronManager.getJob(this.dreamJobId)
      : (await cronManager.listJobs({ nameContains: 'Dream' }))[0];

    if (!job) {
      return {
        configured: false,
        jobId: null,
        nextRun: null,
        lastRun: null,
        enabled: false,
      };
    }

    // Calculate next run time from cron expression
    const nextRun = this.calculateNextRun(job.schedule.expr || DREAM_SCHEDULE);

    return {
      configured: true,
      jobId: job.id,
      nextRun,
      lastRun: job.state?.lastRunAtMs
        ? new Date(job.state.lastRunAtMs).toISOString()
        : null,
      enabled: job.enabled,
    };
  }

  /**
   * Calculate approximate next run time from cron expression
   * Simplified - doesn't handle all cron cases
   */
  private calculateNextRun(expr: string): string | null {
    try {
      const parts = expr.trim().split(/\s+/);
      if (parts.length !== 5) return null;

      const [minute, hour] = parts;
      const now = new Date();
      const next = new Date();

      // Set to specified hour/minute
      if (minute !== '*') {
        next.setMinutes(parseInt(minute, 10));
      } else {
        next.setMinutes(0);
      }

      if (hour !== '*') {
        next.setHours(parseInt(hour, 10));
      } else {
        next.setHours(0);
      }

      // If time has passed today, move to tomorrow
      if (next.getTime() <= now.getTime()) {
        next.setDate(next.getDate() + 1);
      }

      return next.toISOString();
    } catch {
      return null;
    }
  }

  /**
   * Disable the Dream scheduler
   */
  async disable(): Promise<boolean> {
    if (!this.dreamJobId) return false;
    return cronManager.disableJob(this.dreamJobId);
  }

  /**
   * Enable the Dream scheduler
   */
  async enable(): Promise<boolean> {
    if (!this.dreamJobId) return false;
    return cronManager.enableJob(this.dreamJobId);
  }

  /**
   * Remove the Dream scheduler
   */
  async remove(): Promise<boolean> {
    if (!this.dreamJobId) return false;
    const result = await cronManager.deleteJob(this.dreamJobId);
    if (result) this.dreamJobId = null;
    return result;
  }

  /**
   * Update configuration
   */
  updateConfig(config: Partial<DreamSchedulerConfig>): void {
    this.config = { ...this.config, ...config };
  }

  /**
   * Get current configuration
   */
  getConfig(): DreamSchedulerConfig {
    return { ...this.config };
  }
}

// Export singleton instance
export const dreamScheduler = new DreamScheduler();
