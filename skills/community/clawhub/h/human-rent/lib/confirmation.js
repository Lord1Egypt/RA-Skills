#!/usr/bin/env node
/**
 * User Confirmation Module
 * Ensures explicit user consent before dispatching human workers
 */

const readline = require('readline');

class ConfirmationManager {
  /**
   * Prompt user for confirmation before dispatching task
   */
  async promptForDispatch(taskDetails) {
    // If running in non-interactive mode, require explicit flag
    if (!process.stdin.isTTY) {
      if (process.env.HUMAN_RENT_AUTO_CONFIRM === 'true') {
        console.log('[Auto-confirmed via HUMAN_RENT_AUTO_CONFIRM]');
        return true;
      }
      throw new Error(
        'Cannot prompt for confirmation in non-interactive mode.\n' +
        'Set HUMAN_RENT_AUTO_CONFIRM=true environment variable to auto-confirm, or run in interactive terminal.'
      );
    }

    // Display task details
    console.log('\n========================================');
    console.log('DISPATCH CONFIRMATION REQUIRED');
    console.log('========================================\n');

    console.log('Task Details:');
    console.log(`  Description: ${taskDetails.description || taskDetails.instruction}`);

    if (taskDetails.location) {
      console.log(`  Location: ${taskDetails.location.address || `${taskDetails.location.latitude},${taskDetails.location.longitude}`}`);
    }

    if (taskDetails.estimatedCost) {
      console.log(`  Estimated Cost: ${taskDetails.estimatedCost}`);
    }

    if (taskDetails.estimatedTime) {
      console.log(`  Estimated Time: ${taskDetails.estimatedTime}`);
    }

    console.log('\nThis will dispatch a real human worker to perform a physical task.');
    console.log('You will be charged for this service.');

    // Prompt for confirmation
    const rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout
    });

    return new Promise((resolve) => {
      rl.question('\nDispatch human worker? [y/N]: ', (answer) => {
        rl.close();
        const confirmed = answer.toLowerCase() === 'y' || answer.toLowerCase() === 'yes';

        if (confirmed) {
          console.log('\n✓ Task confirmed. Dispatching...\n');
        } else {
          console.log('\n✗ Task cancelled by user.\n');
        }

        resolve(confirmed);
      });
    });
  }

  /**
   * Show cost warning for expensive tasks
   */
  showCostWarning(cost) {
    if (typeof cost === 'string') {
      cost = parseFloat(cost.replace(/[^0-9.]/g, ''));
    }

    if (cost > 50) {
      console.log('\n⚠️  WARNING: This is a high-cost task (>${cost})');
      console.log('Please ensure you have sufficient budget allocated.\n');
    }
  }

  /**
   * Confirm dangerous or sensitive operations
   */
  async confirmSensitiveTask(taskType) {
    const sensitiveTasks = [
      'legal_consultation',
      'medical_consultation',
      'financial_advice',
      'property_access'
    ];

    if (sensitiveTasks.includes(taskType)) {
      console.log('\n⚠️  SENSITIVE TASK DETECTED');
      console.log('This task type requires additional verification.');
      console.log('Please ensure you have proper authorization.\n');

      if (process.stdin.isTTY) {
        const rl = readline.createInterface({
          input: process.stdin,
          output: process.stdout
        });

        return new Promise((resolve) => {
          rl.question('I confirm I have proper authorization [yes/NO]: ', (answer) => {
            rl.close();
            resolve(answer.toLowerCase() === 'yes');
          });
        });
      }

      return false;
    }

    return true;
  }
}

module.exports = ConfirmationManager;
