/**
 * Scheduler Module - Cron-based task scheduling for EO
 * 
 * Provides:
 * - CronManager: Generic cron job management
 * - DreamScheduler: Dream Module automation
 */

export { CronManager, cronManager, type CronJob, type CronManagerStats } from './cron-manager.js';
export { DreamScheduler, dreamScheduler, type DreamSchedulerConfig, type DreamResult } from './dream-scheduler.js';
