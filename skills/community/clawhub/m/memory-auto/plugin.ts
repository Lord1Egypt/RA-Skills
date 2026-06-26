# Minimal OpenClaw Plugin: Memory Auto Archive
# This plugin registers a heartbeat task that runs the PowerShell script

import { Plugin } from 'openclaw';

export default class MemoryAutoPlugin extends Plugin {
  onRegister() {
    this.logger.info('MemoryAutoPlugin registered');

    // Register a startup task (runs when agent starts)
    this.on('agent:startup', async (agent) => {
      this.logger.info('Agent started, triggering memory archive');
      try {
        // Run archive script
        await this.runArchive();
        // Optionally run refinement
        // await this.runRefine();
      } catch (err) {
        this.logger.error('Memory archive failed:', err);
      }
    });
  }

  async runArchive() {
    const script = join(__dirname, 'archive.ps1');
    // Use OpenClaw's exec or spawn
    // For demo: we'll just log
    this.logger.info(`Running ${script}`);
  }
}
