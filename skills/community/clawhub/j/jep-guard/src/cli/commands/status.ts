import { Command } from 'commander';
import fs from 'fs';
import path from 'path';
import os from 'os';

export const statusCommand = new Command('status')
  .description('Show JEP Guard status')
  .action(async () => {
    const configDir = path.join(os.homedir(), '.jep-guard');
    const socketPath = path.join(os.tmpdir(), 'jep-guard.sock');

    console.log('\n🛡️  JEP Guard v2.0.4 Status\n');

    // Config
    const configPath = path.join(configDir, 'config.json');
    if (fs.existsSync(configPath)) {
      const config = JSON.parse(fs.readFileSync(configPath, 'utf-8'));
      console.log(`Mode:      ${config.mode}`);
      console.log(`Version:   ${config.version}`);
      console.log(`Daemon:    ${fs.existsSync(socketPath) ? '✅ Running' : '⏹️  Stopped'}`);
    } else {
      console.log('❌ Not initialized. Run: claw run jep-guard init');
      return;
    }

    // Stats
    const auditPath = path.join(configDir, 'audit-stream.jep');
    if (fs.existsSync(auditPath)) {
      const stats = fs.statSync(auditPath);
      console.log(`Audit Log: ${(stats.size / 1024).toFixed(1)} KB`);
    }

    console.log('\nQuick commands:');
    console.log('  claw run jep-guard daemon          Start daemon');
    console.log('  claw run jep-guard log --last     View recent events');
    console.log('  claw run jep-guard dashboard      Interactive dashboard');
  });