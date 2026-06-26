#!/usr/bin/env node
/**
 * Task Dispatch Module
 * Core logic for dispatching human workers
 */

const ZhenRentAPIClient = require('./api-client');
const ConfirmationManager = require('./confirmation');

class TaskDispatcher {
  constructor() {
    this.client = new ZhenRentAPIClient();
    this.confirmationManager = new ConfirmationManager();
  }

  /**
   * Parse location string to coordinates
   */
  parseLocation(locationStr) {
    if (!locationStr) return null;

    // Check if it's lat,lng format
    const coords = locationStr.split(',').map(s => parseFloat(s.trim()));
    if (coords.length === 2 && !isNaN(coords[0]) && !isNaN(coords[1])) {
      return {
        latitude: coords[0],
        longitude: coords[1]
      };
    }

    // Otherwise treat as address
    return {
      address: locationStr
    };
  }

  /**
   * Parse budget string
   */
  parseBudget(budgetStr) {
    if (!budgetStr) {
      return { min: 15, max: 25 };
    }

    // Extract numbers from string like "$15-25" or "$20"
    const numbers = budgetStr.match(/\d+/g);
    if (!numbers) {
      return { min: 15, max: 25 };
    }

    if (numbers.length === 1) {
      const amount = parseInt(numbers[0]);
      return { min: amount, max: amount };
    }

    return {
      min: parseInt(numbers[0]),
      max: parseInt(numbers[1])
    };
  }

  /**
   * Estimate task cost based on type and requirements
   */
  estimateCost(taskType, budget) {
    const costMap = {
      'photo_verification': { min: 10, max: 20 },
      'address_verification': { min: 15, max: 25 },
      'document_scan': { min: 15, max: 25 },
      'visual_inspection': { min: 20, max: 40 },
      'voice_verification': { min: 10, max: 20 },
      'purchase_verification': { min: 20, max: 40 }
    };

    const estimate = costMap[taskType] || budget || { min: 15, max: 25 };
    return `$${estimate.min}-${estimate.max}`;
  }

  /**
   * Dispatch a human task with user confirmation
   */
  async dispatch(instruction, options = {}) {
    try {
      // Parse options
      const location = this.parseLocation(options.location);
      const budget = this.parseBudget(options.budget);
      const taskType = options.taskType || this.inferTaskType(instruction);
      const priority = options.priority || 'normal';
      const timeoutMinutes = options.timeout || 30;

      // Build task data
      const taskData = {
        title: this.generateTitle(instruction),
        description: instruction,
        task_type: taskType,
        location: location,
        budget_min: budget.min,
        budget_max: budget.max,
        priority: priority,
        deadline: new Date(Date.now() + timeoutMinutes * 60 * 1000).toISOString(),
        requirements: options.requirements || {}
      };

      // Prepare confirmation details
      const confirmationDetails = {
        instruction: instruction,
        location: location,
        estimatedCost: this.estimateCost(taskType, budget),
        estimatedTime: `${timeoutMinutes} minutes`
      };

      // Show cost warning if needed
      this.confirmationManager.showCostWarning(budget.max);

      // Check for sensitive tasks
      const sensitiveConfirmed = await this.confirmationManager.confirmSensitiveTask(taskType);
      if (!sensitiveConfirmed) {
        return {
          success: false,
          error: 'Sensitive task authorization required but not granted'
        };
      }

      // Request user confirmation
      const confirmed = await this.confirmationManager.promptForDispatch(confirmationDetails);
      if (!confirmed) {
        return {
          success: false,
          error: 'Task cancelled by user'
        };
      }

      // Create task via API
      console.log('Creating task on ZhenRent platform...');
      const response = await this.client.createTask(taskData);

      console.log('\n✓ Task dispatched successfully!\n');
      console.log('Task Details:');
      console.log(`  Task ID: ${response.id || response.task_id}`);
      console.log(`  Status: ${response.status}`);
      console.log(`  Estimated completion: ${response.estimated_completion || 'TBD'}`);
      console.log(`\nCheck status with: human-rent status ${response.id || response.task_id}`);

      return {
        success: true,
        taskId: response.id || response.task_id,
        status: response.status,
        data: response
      };

    } catch (error) {
      console.error('\n✗ Error dispatching task:', error.message);
      return {
        success: false,
        error: error.message
      };
    }
  }

  /**
   * Infer task type from instruction
   */
  inferTaskType(instruction) {
    const lower = instruction.toLowerCase();

    if (lower.includes('photo') || lower.includes('picture') || lower.includes('image')) {
      return 'photo_verification';
    }
    if (lower.includes('address') || lower.includes('location') || lower.includes('verify')) {
      return 'address_verification';
    }
    if (lower.includes('call') || lower.includes('phone') || lower.includes('voice')) {
      return 'voice_verification';
    }
    if (lower.includes('inspect') || lower.includes('check condition')) {
      return 'visual_inspection';
    }
    if (lower.includes('document') || lower.includes('scan') || lower.includes('paper')) {
      return 'document_scan';
    }
    if (lower.includes('purchase') || lower.includes('buy') || lower.includes('availability')) {
      return 'purchase_verification';
    }

    return 'photo_verification'; // Default
  }

  /**
   * Generate task title from instruction
   */
  generateTitle(instruction) {
    // Take first 50 chars
    const title = instruction.substring(0, 50);
    return instruction.length > 50 ? title + '...' : title;
  }
}

module.exports = TaskDispatcher;
