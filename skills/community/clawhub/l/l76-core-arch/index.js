/**
 * L76 Core Architecture - Main Entry Point
 * 
 * This script demonstrates the main logic flow for a production-ready skill.
 * It's optional for simple skills (which can be SKILL.md only), but useful
 * for complex skills with reusable logic.
 * 
 * Usage: node index.js [options]
 */

const fs = require('fs');
const path = require('path');

// Configuration
const CONFIG = {
  skillName: 'l76-core-arch',
  version: '1.0.0',
  workspaceRoot: path.join(__dirname, '..', '..'),
  stateFile: path.join(__dirname, 'state.json')
};

/**
 * State Management
 * Tracks skill execution state across runs
 */
class StateManager {
  constructor(stateFile) {
    this.stateFile = stateFile;
    this.state = this.load();
  }

  load() {
    try {
      if (fs.existsSync(this.stateFile)) {
        return JSON.parse(fs.readFileSync(this.stateFile, 'utf8'));
      }
    } catch (error) {
      console.warn(`Failed to load state: ${error.message}`);
    }
    return {
      lastRun: null,
      runCount: 0,
      errors: [],
      config: {}
    };
  }

  save() {
    try {
      fs.writeFileSync(this.stateFile, JSON.stringify(this.state, null, 2));
    } catch (error) {
      console.warn(`Failed to save state: ${error.message}`);
    }
  }

  update(updates) {
    Object.assign(this.state, updates);
    this.state.lastRun = new Date().toISOString();
    this.state.runCount++;
    this.save();
  }

  logError(error) {
    this.state.errors.push({
      timestamp: new Date().toISOString(),
      message: error.message,
      stack: error.stack
    });
    // Keep only last 10 errors
    if (this.state.errors.length > 10) {
      this.state.errors = this.state.errors.slice(-10);
    }
    this.save();
  }
}

/**
 * Main Skill Logic
 * Demonstrates core architecture patterns
 */
class SkillExecutor {
  constructor(config) {
    this.config = config;
    this.state = new StateManager(path.join(__dirname, 'state.json'));
  }

  /**
   * Preflight Checks
   * Verify prerequisites before execution
   */
  async preflight() {
    console.log('🔍 Running preflight checks...');
    
    const checks = [
      { name: 'Workspace exists', pass: fs.existsSync(this.config.workspaceRoot) },
      { name: 'SKILL.md exists', pass: fs.existsSync(path.join(__dirname, 'SKILL.md')) },
      { name: 'Node.js available', pass: typeof process.versions.node === 'string' }
    ];

    const failed = checks.filter(c => !c.pass);
    if (failed.length > 0) {
      throw new Error(`Preflight failed: ${failed.map(f => f.name).join(', ')}`);
    }

    console.log('✅ All preflight checks passed');
    return { success: true, checks };
  }

  /**
   * Main Execution
   * Core skill functionality
   */
  async execute(options = {}) {
    console.log('🚀 Executing skill logic...');
    
    try {
      // Step 1: Initialize
      await this.initialize(options);
      
      // Step 2: Process
      const result = await this.process(options);
      
      // Step 3: Finalize
      await this.finalize(result);
      
      return {
        status: 'success',
        result,
        timestamp: new Date().toISOString()
      };
    } catch (error) {
      this.state.logError(error);
      return {
        status: 'error',
        error: error.message,
        recovery: 'Check logs and retry with --verbose flag',
        timestamp: new Date().toISOString()
      };
    }
  }

  async initialize(options) {
    console.log('📦 Initializing...');
    // Initialize resources, load config, etc.
    this.state.update({ config: options });
  }

  async process(options) {
    console.log('⚙️ Processing...');
    // Core business logic here
    return {
      itemsProcessed: 0,
      duration: '0ms'
    };
  }

  async finalize(result) {
    console.log('✅ Finalizing...');
    // Cleanup, save state, report results
    console.log(`Result: ${JSON.stringify(result, null, 2)}`);
  }
}

/**
 * CLI Interface
 */
async function main() {
  const args = process.argv.slice(2);
  const executor = new SkillExecutor(CONFIG);

  try {
    // Parse arguments
    const options = {
      verbose: args.includes('--verbose') || args.includes('-v'),
      dryRun: args.includes('--dry-run') || args.includes('-n'),
      force: args.includes('--force') || args.includes('-f')
    };

    console.log(`🏗️  ${CONFIG.skillName} v${CONFIG.version}`);
    console.log('');

    // Run preflight
    if (!options.dryRun) {
      await executor.preflight();
    }

    // Execute main logic
    const result = await executor.execute(options);

    // Report outcome
    if (result.status === 'success') {
      console.log('✅ Skill completed successfully');
      process.exit(0);
    } else {
      console.error('❌ Skill failed:', result.error);
      console.log('💡 Recovery:', result.recovery);
      process.exit(1);
    }
  } catch (error) {
    console.error('💥 Unexpected error:', error.message);
    process.exit(1);
  }
}

// Export for use as module
module.exports = { SkillExecutor, StateManager, CONFIG };

// Run if called directly
if (require.main === module) {
  main();
}
