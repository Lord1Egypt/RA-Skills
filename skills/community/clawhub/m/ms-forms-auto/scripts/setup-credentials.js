#!/usr/bin/env node
/**
 * Interactive M365 credential setup.
 * Saves email and password to config/credentials.json (gitignored).
 */

const fs = require('fs');
const path = require('path');
const readline = require('readline');

const CONFIG_DIR = path.join(__dirname, '..', 'config');
const CREDENTIALS_PATH = path.join(CONFIG_DIR, 'credentials.json');

function prompt(question, hidden = false) {
  return new Promise((resolve) => {
    const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
    
    if (hidden) {
      // Hide password input
      const stdin = process.stdin;
      process.stdout.write(question);
      stdin.setRawMode(true);
      stdin.resume();
      
      let password = '';
      stdin.on('data', (char) => {
        char = char.toString();
        if (char === '\r' || char === '\n') {
          stdin.setRawMode(false);
          stdin.pause();
          rl.close();
          process.stdout.write('\n');
          resolve(password);
        } else if (char === '\u0003') {
          // Ctrl+C
          process.exit();
        } else if (char === '\u007f') {
          // Backspace
          password = password.slice(0, -1);
        } else {
          password += char;
        }
      });
    } else {
      rl.question(question, (answer) => {
        rl.close();
        resolve(answer.trim());
      });
    }
  });
}

async function main() {
  console.log('🔐 M365 Credential Setup\n');
  console.log('This saves your Microsoft 365 email and password for automated form submission.');
  console.log('Credentials are stored locally in config/credentials.json and NEVER sent anywhere else.\n');
  
  if (fs.existsSync(CREDENTIALS_PATH)) {
    const overwrite = await prompt('⚠️  credentials.json already exists. Overwrite? (y/N): ');
    if (overwrite.toLowerCase() !== 'y') {
      console.log('Aborted.');
      process.exit(0);
    }
  }
  
  const email = await prompt('M365 Email: ');
  if (!email || !email.includes('@')) {
    console.error('❌ Invalid email address.');
    process.exit(1);
  }
  
  const password = await prompt('Password: ', true);
  if (!password) {
    console.error('❌ Password cannot be empty.');
    process.exit(1);
  }
  
  // Ensure config directory exists
  if (!fs.existsSync(CONFIG_DIR)) {
    fs.mkdirSync(CONFIG_DIR, { recursive: true });
  }
  
  // Save credentials
  const credentials = {
    email,
    password,
    createdAt: new Date().toISOString(),
  };
  
  fs.writeFileSync(CREDENTIALS_PATH, JSON.stringify(credentials, null, 2), { mode: 0o600 });
  
  console.log(`\n✅ Credentials saved to ${CREDENTIALS_PATH}`);
  console.log('   File permissions: 600 (owner read/write only)');
  console.log('\nNext steps:');
  console.log('1. Edit config/form-values.json with your daily answers');
  console.log('2. Run: node scripts/submit.js --dry-run (to test)');
  console.log('3. Run: node scripts/submit.js --headed (first real run, for MFA if needed)');
}

main();
