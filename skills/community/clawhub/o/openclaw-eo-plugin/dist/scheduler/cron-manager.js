/**
 * Cron Manager - Manages OpenClaw cron jobs
 *
 * Provides programmatic cron job management for EO scheduling
 */
import { exec } from 'child_process';
import { promisify } from 'util';
import fs from 'fs/promises';
import path from 'path';
import { logger } from '../utils/logger.js';
const execAsync = promisify(exec);
const CRON_JOBS_PATH = path.join(process.env.HOME || '/home/zzy', '.openclaw/cron/jobs.json');
/**
 * CronManager class for managing OpenClaw cron jobs
 */
export class CronManager {
    jobsPath;
    constructor(jobsPath) {
        this.jobsPath = jobsPath || CRON_JOBS_PATH;
    }
    /**
     * Load all cron jobs from the config file
     */
    async loadJobs() {
        try {
            const content = await fs.readFile(this.jobsPath, 'utf-8');
            const data = JSON.parse(content);
            return data.jobs || [];
        }
        catch (error) {
            console.error('[CronManager] Failed to load jobs:', error);
            return [];
        }
    }
    /**
     * Save jobs back to the config file
     */
    async saveJobs(jobs) {
        const data = { version: 1, jobs };
        await fs.writeFile(this.jobsPath, JSON.stringify(data, null, 2), 'utf-8');
    }
    /**
     * Get a specific job by ID
     */
    async getJob(id) {
        const jobs = await this.loadJobs();
        return jobs.find(j => j.id === id);
    }
    /**
     * Create a new cron job
     */
    async createJob(job) {
        const jobs = await this.loadJobs();
        const now = Date.now();
        const newJob = {
            ...job,
            id: this.generateId(),
            createdAtMs: now,
            updatedAtMs: now,
        };
        jobs.push(newJob);
        await this.saveJobs(jobs);
        logger.debug(`Created job: ${newJob.name} (${newJob.id})`);
        return newJob;
    }
    /**
     * Update an existing job
     */
    async updateJob(id, updates) {
        const jobs = await this.loadJobs();
        const index = jobs.findIndex(j => j.id === id);
        if (index === -1) {
            console.warn(`[CronManager] Job not found: ${id}`);
            return undefined;
        }
        jobs[index] = { ...jobs[index], ...updates, updatedAtMs: Date.now() };
        await this.saveJobs(jobs);
        logger.debug(`Updated job: ${jobs[index].name} (${id})`);
        return jobs[index];
    }
    /**
     * Delete a job by ID
     */
    async deleteJob(id) {
        const jobs = await this.loadJobs();
        const index = jobs.findIndex(j => j.id === id);
        if (index === -1) {
            console.warn(`[CronManager] Job not found: ${id}`);
            return false;
        }
        const deleted = jobs.splice(index, 1)[0];
        await this.saveJobs(jobs);
        logger.debug(`Deleted job: ${deleted.name} (${id})`);
        return true;
    }
    /**
     * Enable a job
     */
    async enableJob(id) {
        const job = await this.updateJob(id, { enabled: true });
        return job !== undefined;
    }
    /**
     * Disable a job
     */
    async disableJob(id) {
        const job = await this.updateJob(id, { enabled: false });
        return job !== undefined;
    }
    /**
     * Get statistics about all jobs
     */
    async getStats() {
        const jobs = await this.loadJobs();
        const stats = {
            totalJobs: jobs.length,
            enabledJobs: jobs.filter(j => j.enabled).length,
            disabledJobs: jobs.filter(j => !j.enabled).length,
            jobsByStatus: {},
        };
        for (const job of jobs) {
            const status = job.state?.lastRunStatus || 'never';
            stats.jobsByStatus[status] = (stats.jobsByStatus[status] || 0) + 1;
        }
        return stats;
    }
    /**
     * List all jobs with optional filter
     */
    async listJobs(filter) {
        let jobs = await this.loadJobs();
        if (filter?.enabled !== undefined) {
            jobs = jobs.filter(j => j.enabled === filter.enabled);
        }
        if (filter?.nameContains) {
            const search = filter.nameContains.toLowerCase();
            jobs = jobs.filter(j => j.name.toLowerCase().includes(search));
        }
        return jobs;
    }
    /**
     * Validate a cron expression
     */
    validateCronExpr(expr) {
        // Basic validation: 5 fields (minute, hour, day, month, weekday)
        const parts = expr.trim().split(/\s+/);
        if (parts.length !== 5)
            return false;
        // Each part should be a valid cron component or * or valid range
        const validPattern = /^(\*|\d+(-\d+)?(,\d+(-\d+)?)*|\*\/\d+)$/;
        return parts.every(p => validPattern.test(p));
    }
    /**
     * Generate a unique job ID
     */
    generateId() {
        return `${Date.now()}-${Math.random().toString(36).slice(2, 11)}`;
    }
}
// Export singleton instance
export const cronManager = new CronManager();
//# sourceMappingURL=cron-manager.js.map