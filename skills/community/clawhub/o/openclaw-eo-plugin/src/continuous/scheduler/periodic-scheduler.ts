/**
 * Periodic Scheduler
 * Schedules and manages periodic tasks for the continuous learning loop
 */

import { logger } from '../../utils/logger.js'

export interface ScheduledTask {
  id: string
  name: string
  intervalMs: number
  lastRun: number | null
  nextRun: number
  enabled: boolean
  callback: () => Promise<void> | void
}

export interface SchedulerConfig {
  enabled: boolean
  defaultIntervalMs: number
  maxConcurrentTasks: number
}

export class PeriodicScheduler {
  private config: SchedulerConfig
  private tasks: Map<string, ScheduledTask> = new Map()
  private running: boolean = false
  private intervalHandle: ReturnType<typeof setInterval> | null = null

  constructor(defaultIntervalMs: number = 3600000) {
    this.config = {
      enabled: true,
      defaultIntervalMs,
      maxConcurrentTasks: 5,
    }
  }

  /**
   * Schedule a periodic task
   */
  schedule(
    id: string,
    name: string,
    callback: () => Promise<void> | void,
    intervalMs?: number
  ): ScheduledTask {
    const interval = intervalMs || this.config.defaultIntervalMs
    const now = Date.now()

    const task: ScheduledTask = {
      id,
      name,
      intervalMs: interval,
      lastRun: null,
      nextRun: now + interval,
      enabled: true,
      callback,
    }

    this.tasks.set(id, task)
    return task
  }

  /**
   * Unschedule a task
   */
  unschedule(id: string): boolean {
    return this.tasks.delete(id)
  }

  /**
   * Enable a task
   */
  enable(id: string): boolean {
    const task = this.tasks.get(id)
    if (task) {
      task.enabled = true
      return true
    }
    return false
  }

  /**
   * Disable a task
   */
  disable(id: string): boolean {
    const task = this.tasks.get(id)
    if (task) {
      task.enabled = false
      return true
    }
    return false
  }

  /**
   * Start the scheduler
   */
  start(): void {
    if (this.running) {
      logger.warn('PeriodicScheduler already running')
      return
    }

    this.running = true
    logger.info('PeriodicScheduler started')

    // Run check every 10 seconds
    this.intervalHandle = setInterval(() => {
      this.checkAndRunTasks()
    }, 10000)
  }

  /**
   * Stop the scheduler
   */
  stop(): void {
    if (this.intervalHandle) {
      clearInterval(this.intervalHandle)
      this.intervalHandle = null
    }
    this.running = false
    logger.info('PeriodicScheduler stopped')
  }

  /**
   * Check and run due tasks
   */
  private async checkAndRunTasks(): Promise<void> {
    if (!this.running) return

    const now = Date.now()

    for (const task of this.tasks.values()) {
      if (!task.enabled) continue
      if (task.nextRun > now) continue

      logger.debug(`Running task: ${task.name}`)

      try {
        await task.callback()
        task.lastRun = now
        task.nextRun = now + task.intervalMs
      } catch (error) {
        console.error(`[PeriodicScheduler] Task ${task.name} failed:`, error)
        // Still update next run to prevent tight looping
        task.nextRun = now + task.intervalMs
      }
    }
  }

  /**
   * Run a specific task immediately
   */
  async runNow(id: string): Promise<boolean> {
    const task = this.tasks.get(id)
    if (!task) return false

    logger.debug(`Running task immediately: ${task.name}`)

    try {
      await task.callback()
      task.lastRun = Date.now()
      return true
    } catch (error) {
      console.error(`[PeriodicScheduler] Task ${task.name} failed:`, error)
      return false
    }
  }

  /**
   * Check if scheduler is running
   */
  isActive(): boolean {
    return this.running
  }

  /**
   * Get task status
   */
  getTaskStatus(id: string): ScheduledTask | null {
    return this.tasks.get(id) || null
  }

  /**
   * Get all tasks
   */
  getAllTasks(): ScheduledTask[] {
    return Array.from(this.tasks.values())
  }

  /**
   * Get scheduler status
   */
  getStatus(): {
    running: boolean
    taskCount: number
    enabledTasks: number
    tasks: Array<{
      id: string
      name: string
      enabled: boolean
      lastRun: number | null
      nextRun: number
      overdue: boolean
    }>
  } {
    const now = Date.now()

    return {
      running: this.running,
      taskCount: this.tasks.size,
      enabledTasks: Array.from(this.tasks.values()).filter(t => t.enabled).length,
      tasks: Array.from(this.tasks.values()).map(t => ({
        id: t.id,
        name: t.name,
        enabled: t.enabled,
        lastRun: t.lastRun,
        nextRun: t.nextRun,
        overdue: t.enabled && t.nextRun < now,
      })),
    }
  }

  /**
   * Update configuration
   */
  updateConfig(config: Partial<SchedulerConfig>): void {
    this.config = { ...this.config, ...config }
  }

  /**
   * Clear all tasks
   */
  clear(): void {
    this.tasks.clear()
  }
}
