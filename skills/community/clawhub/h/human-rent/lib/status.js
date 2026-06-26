#!/usr/bin/env node
/**
 * Task Status Module
 * Check status and results of dispatched tasks
 */

const ZhenRentAPIClient = require('./api-client');

class StatusChecker {
  constructor() {
    this.client = new ZhenRentAPIClient();
  }

  /**
   * Check task status
   */
  async checkStatus(taskId) {
    try {
      console.log(`Checking status for task: ${taskId}...\n`);

      const response = await this.client.getTaskStatus(taskId);

      // Display status
      console.log('========================================');
      console.log('TASK STATUS');
      console.log('========================================\n');

      console.log(`Task ID: ${response.id || taskId}`);
      console.log(`Status: ${this.formatStatus(response.status)}`);
      console.log(`Created: ${this.formatDate(response.created_at)}`);

      if (response.assigned_to) {
        console.log(`\nAssigned to: ${response.assigned_to.name || response.assigned_to}`);
        if (response.assigned_at) {
          console.log(`Assigned at: ${this.formatDate(response.assigned_at)}`);
        }
      }

      if (response.status === 'in_progress') {
        console.log(`\nWorker is currently working on this task.`);
        if (response.progress_notes) {
          console.log(`Progress: ${response.progress_notes}`);
        }
      }

      if (response.status === 'completed') {
        console.log(`\nCompleted at: ${this.formatDate(response.completed_at)}`);
        this.displayResults(response.result);
      }

      if (response.status === 'failed' || response.status === 'cancelled') {
        console.log(`\nReason: ${response.failure_reason || response.cancellation_reason || 'Not specified'}`);
      }

      if (response.estimated_completion && response.status !== 'completed') {
        console.log(`\nEstimated completion: ${this.formatDate(response.estimated_completion)}`);
      }

      console.log('\n========================================\n');

      return {
        success: true,
        status: response.status,
        data: response
      };

    } catch (error) {
      console.error('\n✗ Error checking status:', error.message);
      return {
        success: false,
        error: error.message
      };
    }
  }

  /**
   * Display task results
   */
  displayResults(result) {
    if (!result) return;

    console.log('\nResults:');

    if (result.notes) {
      console.log(`  Notes: ${result.notes}`);
    }

    if (result.photos && result.photos.length > 0) {
      console.log(`\n  Photos (${result.photos.length}):`);
      result.photos.forEach((url, i) => {
        console.log(`    ${i + 1}. ${url}`);
      });
    }

    if (result.documents && result.documents.length > 0) {
      console.log(`\n  Documents (${result.documents.length}):`);
      result.documents.forEach((url, i) => {
        console.log(`    ${i + 1}. ${url}`);
      });
    }

    if (result.verification_status) {
      console.log(`\n  Verification: ${result.verification_status}`);
    }

    if (result.data) {
      console.log(`\n  Additional Data:`);
      console.log(`    ${JSON.stringify(result.data, null, 2)}`);
    }
  }

  /**
   * Format status for display
   */
  formatStatus(status) {
    const statusMap = {
      'pending': '⏳ Pending',
      'assigned': '👤 Assigned',
      'in_progress': '🔄 In Progress',
      'completed': '✅ Completed',
      'failed': '❌ Failed',
      'cancelled': '🚫 Cancelled'
    };

    return statusMap[status] || status;
  }

  /**
   * Format date for display
   */
  formatDate(dateStr) {
    if (!dateStr) return 'N/A';
    const date = new Date(dateStr);
    return date.toLocaleString();
  }

  /**
   * Wait for task completion (polling)
   */
  async waitForCompletion(taskId, options = {}) {
    const maxWaitMinutes = options.maxWaitMinutes || 60;
    const pollIntervalSeconds = options.pollIntervalSeconds || 30;
    const maxAttempts = Math.floor((maxWaitMinutes * 60) / pollIntervalSeconds);

    console.log(`Waiting for task completion (max ${maxWaitMinutes} minutes)...`);
    console.log(`Polling every ${pollIntervalSeconds} seconds.\n`);

    for (let attempt = 1; attempt <= maxAttempts; attempt++) {
      const result = await this.checkStatus(taskId);

      if (!result.success) {
        return result;
      }

      const status = result.data.status;

      if (status === 'completed') {
        console.log('\n✓ Task completed!');
        return result;
      }

      if (status === 'failed' || status === 'cancelled') {
        console.log('\n✗ Task did not complete successfully.');
        return result;
      }

      // Still in progress
      console.log(`\n[${attempt}/${maxAttempts}] Status: ${status}. Waiting ${pollIntervalSeconds}s...`);

      // Wait before next poll
      await new Promise(resolve => setTimeout(resolve, pollIntervalSeconds * 1000));
    }

    console.log('\n⏰ Timeout: Task did not complete within max wait time.');
    return {
      success: false,
      error: 'Timeout waiting for task completion'
    };
  }
}

module.exports = StatusChecker;
// tampered
