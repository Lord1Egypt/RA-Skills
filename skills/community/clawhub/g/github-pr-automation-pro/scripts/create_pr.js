#!/usr/bin/env node

/**
 * GitHub PR Creator
 * Creates pull requests with templates and automation
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

function createPR(options) {
  const { branch, title, template, body, draft, labels } = options;
  
  // Check if gh CLI is available
  try {
    execSync('gh --version', { stdio: 'ignore' });
  } catch (e) {
    console.error('❌ GitHub CLI (gh) not found. Install: brew install gh');
    process.exit(1);
  }
  
  // Load template if specified
  let prBody = body || '';
  if (template) {
    const templatePath = path.join(__dirname, '../references/pr_templates', `${template}.md`);
    if (fs.existsSync(templatePath)) {
      prBody = fs.readFileSync(templatePath, 'utf8');
      console.log(`📝 Using template: ${template}`);
    } else {
      console.warn(`⚠️  Template not found: ${template}, using default body`);
    }
  }
  
  // Build gh pr create command
  let cmd = `gh pr create --title "${title}" --body "${prBody}"`;
  
  if (branch) {
    cmd += ` --head ${branch}`;
  }
  
  if (draft) {
    cmd += ' --draft';
  }
  
  if (labels) {
    cmd += ` --label "${labels}"`;
  }
  
  console.log(`\n🚀 Creating PR: ${title}`);
  console.log(`Branch: ${branch || 'current'}\n`);
  
  try {
    const output = execSync(cmd, { encoding: 'utf8' });
    console.log('✅ PR created successfully!\n');
    console.log(output);
    
    // Extract PR number from output
    const match = output.match(/\/pull\/(\d+)/);
    if (match) {
      const prNumber = match[1];
      console.log(`\n📊 PR #${prNumber}`);
      
      // Auto-label based on branch name
      autoLabel(prNumber, branch || getCurrentBranch());
    }
  } catch (e) {
    console.error('❌ Failed to create PR:', e.message);
    process.exit(1);
  }
}

function getCurrentBranch() {
  try {
    return execSync('git branch --show-current', { encoding: 'utf8' }).trim();
  } catch (e) {
    return '';
  }
}

function autoLabel(prNumber, branch) {
  const rules = {
    'fix': 'bug',
    'feat': 'feature',
    'docs': 'documentation',
    'refactor': 'refactor',
    'test': 'testing'
  };
  
  for (const [keyword, label] of Object.entries(rules)) {
    if (branch.toLowerCase().includes(keyword)) {
      try {
        execSync(`gh pr edit ${prNumber} --add-label "${label}"`, { stdio: 'ignore' });
        console.log(`🏷️  Auto-labeled: ${label}`);
      } catch (e) {
        // Ignore labeling errors
      }
      break;
    }
  }
}

// Parse command line arguments
const args = process.argv.slice(2);
const options = {};

for (let i = 0; i < args.length; i++) {
  switch (args[i]) {
    case '--branch':
      options.branch = args[++i];
      break;
    case '--title':
      options.title = args[++i];
      break;
    case '--template':
      options.template = args[++i];
      break;
    case '--body':
      options.body = args[++i];
      break;
    case '--draft':
      options.draft = true;
      break;
    case '--labels':
      options.labels = args[++i];
      break;
  }
}

if (!options.title) {
  console.error('Usage: node create_pr.js --title "PR Title" [--branch branch-name] [--template feature] [--draft] [--labels "bug,feature"]');
  process.exit(1);
}

createPR(options);
