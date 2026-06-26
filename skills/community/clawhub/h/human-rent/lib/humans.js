#!/usr/bin/env node
/**
 * Human Workers Module
 * List and search for available human workers
 */

const ZhenRentAPIClient = require('./api-client');

class HumanManager {
  constructor() {
    this.client = new ZhenRentAPIClient();
  }

  /**
   * List available human workers
   */
  async listHumans(options = {}) {
    try {
      console.log('Fetching available human workers...\n');

      const location = options.location || null;
      const radius = options.radius || 5000; // 5km default

      const response = await this.client.listWorkers(location, radius);

      console.log('========================================');
      console.log('AVAILABLE HUMAN WORKERS');
      console.log('========================================\n');

      if (response.statistics) {
        console.log('Statistics:');
        console.log(`  Total workers: ${response.statistics.total || 0}`);
        console.log(`  Available now: ${response.statistics.available || 0}`);
        console.log(`  Average rating: ${response.statistics.average_rating || 'N/A'}`);
        console.log('');
      }

      if (response.workers && response.workers.length > 0) {
        console.log(`Found ${response.workers.length} available workers:\n`);

        response.workers.forEach((worker, index) => {
          console.log(`${index + 1}. ${worker.name || 'Worker ' + worker.id}`);
          console.log(`   ID: ${worker.id}`);
          console.log(`   Rating: ${this.formatRating(worker.rating)}`);

          if (worker.skills && worker.skills.length > 0) {
            console.log(`   Skills: ${worker.skills.join(', ')}`);
          }

          if (worker.location) {
            console.log(`   Location: ${worker.location.city || 'Unknown'}`);
          }

          if (worker.hourly_rate) {
            console.log(`   Hourly rate: $${worker.hourly_rate}`);
          }

          if (worker.completed_tasks) {
            console.log(`   Completed tasks: ${worker.completed_tasks}`);
          }

          console.log('');
        });
      } else {
        console.log('No workers available at the moment.');
        console.log('Try expanding the search radius or checking back later.\n');
      }

      console.log('========================================\n');

      return {
        success: true,
        workers: response.workers || [],
        statistics: response.statistics || {}
      };

    } catch (error) {
      console.error('\n✗ Error listing workers:', error.message);
      return {
        success: false,
        error: error.message
      };
    }
  }

  /**
   * Search for workers with specific skills
   */
  async searchBySkills(skills, options = {}) {
    try {
      const result = await this.listHumans(options);

      if (!result.success) {
        return result;
      }

      // Filter by skills
      const filtered = result.workers.filter(worker => {
        if (!worker.skills) return false;
        return skills.every(skill =>
          worker.skills.some(s => s.toLowerCase().includes(skill.toLowerCase()))
        );
      });

      console.log(`\nFiltered to ${filtered.length} workers with required skills: ${skills.join(', ')}\n`);

      return {
        success: true,
        workers: filtered,
        statistics: result.statistics
      };

    } catch (error) {
      console.error('\n✗ Error searching workers:', error.message);
      return {
        success: false,
        error: error.message
      };
    }
  }

  /**
   * Get worker details by ID
   */
  async getWorkerDetails(workerId) {
    try {
      console.log(`Fetching details for worker: ${workerId}...\n`);

      // Note: This would require a dedicated endpoint
      // For now, we'll list all and filter
      const result = await this.listHumans();

      if (!result.success) {
        return result;
      }

      const worker = result.workers.find(w => w.id === workerId);

      if (!worker) {
        throw new Error(`Worker ${workerId} not found`);
      }

      console.log('========================================');
      console.log('WORKER DETAILS');
      console.log('========================================\n');

      console.log(`Name: ${worker.name}`);
      console.log(`ID: ${worker.id}`);
      console.log(`Rating: ${this.formatRating(worker.rating)}`);

      if (worker.bio) {
        console.log(`\nBio: ${worker.bio}`);
      }

      if (worker.skills && worker.skills.length > 0) {
        console.log(`\nSkills: ${worker.skills.join(', ')}`);
      }

      if (worker.certifications && worker.certifications.length > 0) {
        console.log(`\nCertifications: ${worker.certifications.join(', ')}`);
      }

      if (worker.completed_tasks) {
        console.log(`\nCompleted tasks: ${worker.completed_tasks}`);
      }

      if (worker.hourly_rate) {
        console.log(`Hourly rate: $${worker.hourly_rate}`);
      }

      console.log('\n========================================\n');

      return {
        success: true,
        worker: worker
      };

    } catch (error) {
      console.error('\n✗ Error fetching worker details:', error.message);
      return {
        success: false,
        error: error.message
      };
    }
  }

  /**
   * Format rating for display
   */
  formatRating(rating) {
    if (!rating) return 'N/A';

    const stars = '⭐'.repeat(Math.floor(rating));
    return `${stars} (${rating.toFixed(1)}/5.0)`;
  }
}

module.exports = HumanManager;
