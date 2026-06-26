#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const TEMPLATES = {
  'session-state': `# SESSION-STATE.md — Active Working Memory

This file is the agent's "RAM" — survives compaction, restarts, distractions.
Chat history is a BUFFER. This file is STORAGE.

## Current Task
[None]

## Key Context
[None yet]

## Pending Actions
- [ ] None

## Recent Decisions
[None yet]

---
*Last updated: ${new Date().toISOString()}*
`,

  'memory-md': `# MEMORY.md — Long-Term Memory

## About the User
[Add user preferences, communication style, etc.]

## Projects
[Active projects and their status]

## Decisions Log
[Important decisions and why they were made]

## Lessons Learned
[Mistakes to avoid, patterns that work]

## Preferences
[Tools, frameworks, workflows the user prefers]

---
*Curated memory — distill insights from daily logs here*
`,

  'daily-template': `# {{DATE}} — Daily Log

## Tasks Completed
- 

## Decisions Made
- 

## Lessons Learned
- 

## Tomorrow
- 
`
};

const commands = {
  init: () => {
    console.log('🧠 Initializing Elite Longterm Memory...\n');
    
    // Create SESSION-STATE.md
    if (!fs.existsSync('SESSION-STATE.md')) {
      fs.writeFileSync('SESSION-STATE.md', TEMPLATES['session-state']);
      console.log('✓ Created SESSION-STATE.md (Hot RAM)');
    } else {
      console.log('• SESSION-STATE.md already exists');
    }
    
    // Create MEMORY.md
    if (!fs.existsSync('MEMORY.md')) {
      fs.writeFileSync('MEMORY.md', TEMPLATES['memory-md']);
      console.log('✓ Created MEMORY.md (Curated Archive)');
    } else {
      console.log('• MEMORY.md already exists');
    }
    
    // Create memory directory
    if (!fs.existsSync('memory')) {
      fs.mkdirSync('memory', { recursive: true });
      console.log('✓ Created memory/ directory');
    } else {
      console.log('• memory/ directory already exists');
    }
    
    // Create today's log
    const today = new Date().toISOString().split('T')[0];
    const todayFile = `memory/${today}.md`;
    if (!fs.existsSync(todayFile)) {
      const content = TEMPLATES['daily-template'].replace('{{DATE}}', today);
      fs.writeFileSync(todayFile, content);
      console.log(`✓ Created ${todayFile}`);
    }
    
    console.log('\n🎉 Elite Longterm Memory initialized!');
    console.log('\nNext steps:');
    console.log('1. Add SESSION-STATE.md to your agent context');
    console.log('2. (Optional) Configure embedding provider — see SKILL.md');
    console.log('3. Review SKILL.md for full setup guide');
  },
  
  today: () => {
    const today = new Date().toISOString().split('T')[0];
    const todayFile = `memory/${today}.md`;
    
    if (!fs.existsSync('memory')) {
      fs.mkdirSync('memory', { recursive: true });
    }
    
    if (!fs.existsSync(todayFile)) {
      const content = TEMPLATES['daily-template'].replace('{{DATE}}', today);
      fs.writeFileSync(todayFile, content);
      console.log(`✓ Created ${todayFile}`);
    } else {
      console.log(`• ${todayFile} already exists`);
    }
  },
  
  status: () => {
    console.log('🧠 Elite Longterm Memory Status\n');
    
    // Check SESSION-STATE.md
    if (fs.existsSync('SESSION-STATE.md')) {
      const stat = fs.statSync('SESSION-STATE.md');
      console.log(`✓ SESSION-STATE.md (${(stat.size / 1024).toFixed(1)}KB, modified ${stat.mtime.toLocaleString()})`);
    } else {
      console.log('✗ SESSION-STATE.md missing');
    }
    
    // Check MEMORY.md
    if (fs.existsSync('MEMORY.md')) {
      const stat = fs.statSync('MEMORY.md');
      const lines = fs.readFileSync('MEMORY.md', 'utf8').split('\n').length;
      console.log(`✓ MEMORY.md (${lines} lines, ${(stat.size / 1024).toFixed(1)}KB)`);
    } else {
      console.log('✗ MEMORY.md missing');
    }
    
    // Check memory directory
    if (fs.existsSync('memory')) {
      const files = fs.readdirSync('memory').filter(f => f.endsWith('.md'));
      console.log(`✓ memory/ (${files.length} daily logs)`);
    } else {
      console.log('✗ memory/ directory missing');
    }
    
    // Check LanceDB (supports both openclaw and clawdbot paths)
    const lancedbPaths = [
      path.join(process.env.HOME, '.openclaw/memory/lancedb'),
      path.join(process.env.HOME, '.clawdbot/memory/lancedb')
    ];
    const lancedbExists = lancedbPaths.some(p => fs.existsSync(p));
    if (lancedbExists) {
      console.log('✓ LanceDB vectors initialized');
    } else {
      console.log('• LanceDB not initialized (optional)');
    }
  },
  
  backup: () => {
    const isGit = process.argv.includes('--git');
    
    const memoryFiles = [];
    if (fs.existsSync('SESSION-STATE.md')) memoryFiles.push('SESSION-STATE.md');
    if (fs.existsSync('MEMORY.md')) memoryFiles.push('MEMORY.md');
    if (fs.existsSync('memory') && fs.statSync('memory').isDirectory()) memoryFiles.push('memory/');
    
    if (memoryFiles.length === 0) {
      console.log('✗ No memory files found. Run "init" first.');
      return;
    }
    
    if (isGit) {
      console.log('🧠 Backing up memory via Git...\n');
      
      try {
        execSync('git rev-parse --git-dir', { stdio: 'pipe' });
      } catch {
        console.log('✗ Not a Git repository. Initialize with "git init" first.');
        return;
      }
      
      let hasRemote = false;
      try {
        const remotes = execSync('git remote', { encoding: 'utf8' }).trim();
        hasRemote = remotes.length > 0;
      } catch {
        hasRemote = false;
      }
      
      try {
        const filesToAdd = memoryFiles.map(f => f.replace(/\/$/, '')).join(' ');
        execSync(`git add ${filesToAdd}`, { stdio: 'pipe' });
        
        const date = new Date().toISOString().replace('T', ' ').slice(0, 19);
        try {
          execSync(`git commit -m "memory backup ${date}"`, { stdio: 'pipe' });
          console.log(`✓ Committed memory files (${date})`);
        } catch (e) {
          if (e.stdout && e.stdout.toString().includes('nothing to commit')) {
            console.log('• No changes to commit (memory files unchanged)');
          } else {
            throw e;
          }
        }
        
        if (hasRemote) {
          try {
            execSync('git push', { stdio: 'pipe', timeout: 30000 });
            console.log('✓ Pushed to remote');
          } catch {
            console.log('⚠ Committed locally but push failed. Try "git push" manually.');
          }
        } else {
          console.log('• No remote configured. Add one with "git remote add origin <url>"');
        }
        
        console.log(`\n📦 Backed up: ${memoryFiles.join(', ')}`);
      } catch (e) {
        console.log(`✗ Git backup failed: ${e.message}`);
      }
      return;
    }
    
    console.log('🧠 Creating zip backup...\n');
    
    const now = new Date();
    const timestamp = now.toISOString().replace(/[-:T.]/g, '').slice(0, 14);
    const zipName = `memory-backup-${timestamp}.zip`;
    const tarName = `memory-backup-${timestamp}.tar.gz`;
    const files = memoryFiles.join(' ');
    
    try {
      execSync(`zip -r "${zipName}" ${files}`, { stdio: 'pipe' });
      const stat = fs.statSync(zipName);
      const sizeKB = (stat.size / 1024).toFixed(1);
      console.log(`✓ Created ${zipName} (${memoryFiles.length} items, ${sizeKB}KB)`);
      console.log(`\n  Restore with: npx liu-longterm-memory restore ${zipName}`);
    } catch {
      try {
        execSync(`tar -czf "${tarName}" ${files}`, { stdio: 'pipe' });
        const stat = fs.statSync(tarName);
        const sizeKB = (stat.size / 1024).toFixed(1);
        console.log(`✓ Created ${tarName} (${memoryFiles.length} items, ${sizeKB}KB)`);
        console.log(`  (zip not available, used tar.gz instead)`);
        console.log(`\n  Restore with: npx liu-longterm-memory restore ${tarName}`);
      } catch (e2) {
        console.log(`✗ Backup failed: neither zip nor tar available.`);
        console.log(`  Try manually: zip -r backup.zip ${files}`);
      }
    }
  },
  
  restore: () => {
    const file = process.argv[3];
    
    if (!file) {
      console.log('Usage: npx liu-longterm-memory restore <backup-file>');
      console.log('\nExample:');
      console.log('  npx liu-longterm-memory restore memory-backup-20260404.zip');
      console.log('  npx liu-longterm-memory restore memory-backup-20260404.tar.gz');
      return;
    }
    
    if (!fs.existsSync(file)) {
      console.log(`✗ File not found: ${file}`);
      return;
    }
    
    console.log(`🧠 Restoring memory from ${file}...\n`);
    
    try {
      if (file.endsWith('.tar.gz') || file.endsWith('.tgz')) {
        execSync(`tar -xzf "${file}"`, { stdio: 'pipe' });
      } else if (file.endsWith('.zip')) {
        execSync(`unzip -o "${file}"`, { stdio: 'pipe' });
      } else {
        console.log('✗ Unsupported format. Use .zip or .tar.gz files.');
        return;
      }
      
      console.log('✓ Memory restored successfully!');
      console.log('\nRestored files:');
      if (fs.existsSync('SESSION-STATE.md')) console.log('  • SESSION-STATE.md');
      if (fs.existsSync('MEMORY.md')) console.log('  • MEMORY.md');
      if (fs.existsSync('memory')) {
        const logs = fs.readdirSync('memory').filter(f => f.endsWith('.md'));
        console.log(`  • memory/ (${logs.length} daily logs)`);
      }
    } catch (e) {
      console.log(`✗ Restore failed: ${e.message}`);
    }
  },
  
  help: () => {
    console.log(`
🧠 Elite Longterm Memory CLI

Commands:
  init          Initialize memory system in current directory
  today         Create today's daily log file
  status        Check memory system health
  backup        Create a zip backup of memory files
  backup --git  Commit and push memory files via Git
  restore <f>   Restore memory from a backup file
  help          Show this help

Usage:
  npx liu-longterm-memory init
  npx liu-longterm-memory status
  npx liu-longterm-memory backup
  npx liu-longterm-memory backup --git
  npx liu-longterm-memory restore memory-backup-20260404.zip
`);
  }
};

const command = process.argv[2] || 'help';

if (commands[command]) {
  commands[command]();
} else {
  console.log(`Unknown command: ${command}`);
  commands.help();
}
