import { Command } from 'commander';
import inquirer from 'inquirer';
import fs from 'fs';
import path from 'path';
import os from 'os';

export const initCommand = new Command('init')
  .description('Initialize JEP Guard v2.0.4')
  .action(async () => {
    console.log('\n🛡️  JEP Guard v2.0.4 Setup\n');

    const answers = await inquirer.prompt([
      { 
        type: 'list', 
        name: 'mode', 
        message: 'Select operating mode:', 
        choices: [
          { name: 'Personal (single user, silent)', value: 'personal' },
          { name: 'Team (shared audit, more visible)', value: 'team' },
          { name: 'Enterprise (strict, full logging)', value: 'enterprise' }
        ],
        default: 'personal'
      },
      { 
        type: 'checkbox', 
        name: 'extensions', 
        message: 'Enable extensions:', 
        choices: [
          { name: 'Cross-Agent Delegation (recommended)', value: 'cross_agent', checked: true },
          { name: 'AEGIS Runtime Integration', value: 'aegis', checked: false },
          { name: 'Cognitive Attestation (LLM features)', value: 'cognitive', checked: false },
          { name: 'TEE Hardware Trust', value: 'tee', checked: false }
        ]
      },
      {
        type: 'list',
        name: 'notifications',
        message: 'Notification style:',
        choices: [
          { name: 'Silent (only blocks)', value: 'silent' },
          { name: 'Minimal (weekly summary)', value: 'minimal' },
          { name: 'Normal (per-session)', value: 'normal' }
        ],
        default: 'minimal'
      }
    ]);

    const configDir = path.join(os.homedir(), '.jep-guard');
    if (!fs.existsSync(configDir)) fs.mkdirSync(configDir, { recursive: true, mode: 0o700 });

    const config = {
      version: '2.0.4',
      mode: answers.mode,
      core: { default_deny: true, auto_start: false },
      extensions: Object.fromEntries(answers.extensions.map((e: string) => [e, { enabled: true }])),
      audit: { stream: answers.mode === 'personal' ? 'local' : 'remote', retention_days: 30 },
      ui: { notifications: answers.notifications, confirmation: 'adaptive' }
    };

    fs.writeFileSync(path.join(configDir, 'config.json'), JSON.stringify(config, null, 2), { mode: 0o600 });

    console.log('\n✅ JEP Guard v2.0.4 initialized');
    console.log(`   Mode: ${answers.mode}`);
    console.log(`   Notifications: ${answers.notifications}`);
    console.log(`   Config: ${configDir}/config.json`);
    console.log('\n💡 Your skills are now protected. Run `claw run jep-guard daemon` to start.');
  });