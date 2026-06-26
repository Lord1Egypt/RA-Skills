#!/usr/bin/env node

/**
 * GitHub Manager CLI
 * 一个全面的GitHub仓库管理工具
 */

const fs = require('fs');
const path = require('path');
const { Octokit } = require('@octokit/rest');
const { execSync } = require('child_process');

class GitHubManager {
  constructor() {
    this.configPath = path.join(process.cwd(), '.github-manager.json');
    this.config = this.loadConfig();
    this.octokit = null;
    
    if (this.config.github && this.config.github.token) {
      this.initializeOctokit();
    }
  }

  loadConfig() {
    try {
      if (fs.existsSync(this.configPath)) {
        return JSON.parse(fs.readFileSync(this.configPath, 'utf8'));
      }
    } catch (error) {
      console.error('Error loading config:', error.message);
    }
    return {};
  }

  saveConfig() {
    try {
      fs.writeFileSync(this.configPath, JSON.stringify(this.config, null, 2));
      console.log('Configuration saved successfully.');
    } catch (error) {
      console.error('Error saving config:', error.message);
    }
  }

  initializeOctokit() {
    try {
      this.octokit = new Octokit({
        auth: this.config.github.token,
        userAgent: 'GitHub Manager CLI v1.0.0',
        timeZone: 'Asia/Shanghai',
        baseUrl: 'https://api.github.com',
        log: {
          debug: () => {},
          info: () => {},
          warn: console.warn,
          error: console.error
        }
      });
    } catch (error) {
      console.error('Failed to initialize GitHub client:', error.message);
    }
  }

  async listRepositories() {
    try {
      const response = await this.octokit.repos.listForAuthenticatedUser({
        sort: 'updated',
        direction: 'desc',
        per_page: 100
      });
      
      console.log('\n📦 Your GitHub Repositories:\n');
      response.data.forEach((repo, index) => {
        console.log(`${index + 1}. ${repo.full_name}`);
        console.log(`   📝 ${repo.description || 'No description'}`);
        console.log(`   ⭐ Stars: ${repo.stargazers_count} | 🍴 Forks: ${repo.forks_count}`);
        console.log(`   🔗 ${repo.html_url}`);
        console.log('');
      });
      
      return response.data;
    } catch (error) {
      console.error('Error listing repositories:', error.message);
      return [];
    }
  }

  async createRepository(name, description = '', isPrivate = false) {
    try {
      const response = await this.octokit.repos.createForAuthenticatedUser({
        name,
        description,
        private: isPrivate,
        auto_init: true,
        gitignore_template: 'Node',
        license_template: 'mit'
      });
      
      console.log(`✅ Repository created successfully: ${response.data.html_url}`);
      return response.data;
    } catch (error) {
      console.error('Error creating repository:', error.message);
      return null;
    }
  }

  async reviewPullRequest(owner, repo, prNumber) {
    try {
      // 获取PR详情
      const pr = await this.octokit.pulls.get({
        owner,
        repo,
        pull_number: prNumber
      });

      // 获取PR文件变更
      const files = await this.octokit.pulls.listFiles({
        owner,
        repo,
        pull_number: prNumber
      });

      console.log(`\n🔍 Reviewing PR #${prNumber}: ${pr.data.title}\n`);
      console.log(`Author: ${pr.data.user.login}`);
      console.log(`Branch: ${pr.data.head.ref} → ${pr.data.base.ref}`);
      console.log(`State: ${pr.data.state}`);
      console.log(`Created: ${new Date(pr.data.created_at).toLocaleString()}`);
      console.log('\n---\n');

      // 分析文件变更
      let totalChanges = 0;
      let additions = 0;
      let deletions = 0;

      files.data.forEach(file => {
        totalChanges++;
        additions += file.additions;
        deletions += file.deletions;
        
        console.log(`📄 ${file.filename}`);
        console.log(`   +${file.additions} -${file.deletions} (${file.changes} changes)`);
        
        // 检查文件类型并提供建议
        if (file.filename.endsWith('.js') || file.filename.endsWith('.ts')) {
          console.log('   💡 JavaScript/TypeScript file detected');
        } else if (file.filename.endsWith('.md')) {
          console.log('   📝 Documentation file');
        } else if (file.filename.endsWith('.json')) {
          console.log('   ⚙️  Configuration file');
        }
        console.log('');
      });

      console.log(`📊 Summary: ${totalChanges} files changed, +${additions} -${deletions}`);

      // 提供审查建议
      this.provideReviewSuggestions(files.data, pr.data);

      return { pr: pr.data, files: files.data, summary: { totalChanges, additions, deletions } };
    } catch (error) {
      console.error('Error reviewing pull request:', error.message);
      return null;
    }
  }

  provideReviewSuggestions(files, pr) {
    console.log('\n💡 Review Suggestions:\n');
    
    const suggestions = [];
    
    // 检查是否有测试文件
    const hasTestFiles = files.some(f => 
      f.filename.includes('test') || 
      f.filename.includes('spec') ||
      f.filename.includes('__tests__')
    );
    
    if (!hasTestFiles && pr.additions > 50) {
      suggestions.push('• Consider adding tests for the new functionality');
    }
    
    // 检查文档更新
    const hasDocUpdates = files.some(f => 
      f.filename.endsWith('.md') || 
      f.filename.includes('README') ||
      f.filename.includes('docs/')
    );
    
    if (!hasDocUpdates && pr.additions > 30) {
      suggestions.push('• Update documentation to reflect the changes');
    }
    
    // 检查大文件
    const largeFiles = files.filter(f => f.changes > 200);
    if (largeFiles.length > 0) {
      suggestions.push('• Large files detected - consider breaking them into smaller modules');
    }
    
    // 检查配置变更
    const configFiles = files.filter(f => 
      f.filename.includes('package.json') ||
      f.filename.includes('config') ||
      f.filename.endsWith('.yml') ||
      f.filename.endsWith('.yaml')
    );
    
    if (configFiles.length > 0) {
      suggestions.push('• Configuration changes detected - verify they work in all environments');
    }
    
    if (suggestions.length === 0) {
      console.log('✅ No specific suggestions. PR looks good!');
    } else {
      suggestions.forEach(suggestion => console.log(suggestion));
    }
  }

  async generateChangelog(owner, repo, sinceTag = null) {
    try {
      // 获取所有tags
      const tags = await this.octokit.repos.listTags({
        owner,
        repo,
        per_page: 50
      });

      // 获取commits
      const commits = await this.octokit.repos.listCommits({
        owner,
        repo,
        per_page: 100
      });

      console.log(`\n📋 Generating Changelog for ${owner}/${repo}\n`);
      
      const changelog = {
        version: 'Unreleased',
        date: new Date().toISOString().split('T')[0],
        features: [],
        fixes: [],
        breaking: [],
        other: []
      };

      // 分析commit消息
      commits.data.forEach(commit => {
        const message = commit.commit.message;
        const author = commit.commit.author.name;
        
        // 分类commit类型
        if (message.toLowerCase().includes('feat') || message.toLowerCase().includes('add')) {
          changelog.features.push(`- ${message.split('\n')[0]} (by ${author})`);
        } else if (message.toLowerCase().includes('fix') || message.toLowerCase().includes('bug')) {
          changelog.fixes.push(`- ${message.split('\n')[0]} (by ${author})`);
        } else if (message.toLowerCase().includes('break')) {
          changelog.breaking.push(`- ${message.split('\n')[0]} (by ${author})`);
        } else {
          changelog.other.push(`- ${message.split('\n')[0]} (by ${author})`);
        }
      });

      // 输出changelog
      console.log(`# Changelog\n`);
      console.log(`## ${changelog.version} (${changelog.date})\n`);
      
      if (changelog.features.length > 0) {
        console.log('### 🚀 New Features\n');
        changelog.features.forEach(f => console.log(f));
        console.log('');
      }
      
      if (changelog.fixes.length > 0) {
        console.log('### 🐛 Bug Fixes\n');
        changelog.fixes.forEach(f => console.log(f));
        console.log('');
      }
      
      if (changelog.breaking.length > 0) {
        console.log('### ⚠️ Breaking Changes\n');
        changelog.breaking.forEach(f => console.log(f));
        console.log('');
      }
      
      if (changelog.other.length > 0) {
        console.log('### 📝 Other Changes\n');
        changelog.other.forEach(f => console.log(f));
        console.log('');
      }

      return changelog;
    } catch (error) {
      console.error('Error generating changelog:', error.message);
      return null;
    }
  }

  async manageIssues(owner, repo, action, options = {}) {
    try {
      switch (action) {
        case 'list':
          const issues = await this.octokit.issues.listForRepo({
            owner,
            repo,
            state: 'open',
            sort: 'created',
            direction: 'desc',
            per_page: 50
          });
          
          console.log(`\n🐛 Open Issues for ${owner}/${repo}:\n`);
          issues.data.forEach(issue => {
            console.log(`#${issue.number}: ${issue.title}`);
            console.log(`   👤 ${issue.user.login} | 🏷️ ${issue.labels.map(l => l.name).join(', ') || 'No labels'}`);
            console.log(`   📅 Created: ${new Date(issue.created_at).toLocaleDateString()}`);
            console.log(`   🔗 ${issue.html_url}\n`);
          });
          break;

        case 'create':
          const newIssue = await this.octokit.issues.create({
            owner,
            repo,
            title: options.title,
            body: options.body || '',
            labels: options.labels ? options.labels.split(',') : ['bug']
          });
          console.log(`✅ Issue created: ${newIssue.data.html_url}`);
          break;

        case 'close':
          await this.octokit.issues.update({
            owner,
            repo,
            issue_number: options.number,
            state: 'closed'
          });
          console.log(`✅ Issue #${options.number} closed`);
          break;
      }
    } catch (error) {
      console.error(`Error managing issues:`, error.message);
    }
  }

  async setupCICD(owner, repo) {
    try {
      const workflows = {
        'ci.yml': `name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    strategy:
      matrix:
        node-version: [18.x, 20.x]
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Use Node.js \${{ matrix.node-version }}
      uses: actions/setup-node@v3
      with:
        node-version: \${{ matrix.node-version }}
        cache: 'npm'
    
    - name: Install dependencies
      run: npm ci
    
    - name: Run tests
      run: npm test
    
    - name: Run linting
      run: npm run lint || true
    
  build:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Use Node.js 20.x
      uses: actions/setup-node@v3
      with:
        node-version: 20.x
        cache: 'npm'
    
    - name: Install dependencies
      run: npm ci
    
    - name: Build
      run: npm run build
    
    - name: Upload build artifacts
      uses: actions/upload-artifact@v3
      with:
        name: build
        path: dist/`,

        'deploy.yml': `name: Deploy

on:
  push:
    tags:
      - 'v*'

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: 20.x
    
    - name: Install dependencies
      run: npm ci
    
    - name: Build
      run: npm run build
    
    - name: Deploy to Production
      run: |
        echo "Deploying version \${{ github.ref_name }}"
        # Add your deployment commands here
        # For example:
        # npm run deploy -- --env production`
      };

      console.log(`\n⚙️ Setting up CI/CD for ${owner}/${repo}\n`);

      // 创建.github/workflows目录
      const workflowsDir = path.join(process.cwd(), '.github', 'workflows');
      if (!fs.existsSync(workflowsDir)) {
        fs.mkdirSync(workflowsDir, { recursive: true });
      }

      // 写入工作流文件
      for (const [filename, content] of Object.entries(workflows)) {
        const filepath = path.join(workflowsDir, filename);
        fs.writeFileSync(filepath, content);
        console.log(`✅ Created workflow: ${filename}`);
      }

      console.log('\n📋 CI/CD setup complete!');
      console.log('Workflows have been created in .github/workflows/');
      console.log('You may need to commit and push these files to activate them.');

    } catch (error) {
      console.error('Error setting up CI/CD:', error.message);
    }
  }
}

// CLI处理
function parseArgs() {
  const args = process.argv.slice(2);
  const result = {};
  
  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg.startsWith('--')) {
      const key = arg.slice(2);
      const nextArg = args[i + 1];
      if (nextArg && !nextArg.startsWith('--')) {
        result[key] = nextArg;
        i++;
      } else {
        result[key] = true;
      }
    }
  }
  
  return result;
}

async function main() {
  const args = parseArgs();
  const manager = new GitHubManager();
  
  if (args.config) {
    if (args.token && args.username) {
      manager.config.github = {
        token: args.token,
        username: args.username,
        defaultRepo: args['default-repo'] || null
      };
      manager.saveConfig();
      manager.initializeOctokit();
      console.log('✅ Configuration saved successfully.');
    } else {
      console.log('Usage: github config --token <token> --username <username> [--default-repo <repo>]');
    }
    return;
  }

  if (!manager.octokit) {
    console.log('❌ GitHub not configured. Please run:');
    console.log('github config --token <your-token> --username <your-username>');
    return;
  }

  // 命令路由
  const getRepo = () => {
    const repo = args.repo || (manager.config.github.defaultRepo);
    if (!repo || !repo.includes('/')) {
      console.log('❌ 需要指定仓库。请使用 --repo owner/repo 或设置 defaultRepo。');
      return null;
    }
    return repo.split('/');
  };

  if (args.command === 'repos' && args.action === 'list') {
    await manager.listRepositories();
  } else if (args.command === 'repos' && args.action === 'create') {
    await manager.createRepository(args.name, args.description, args.private === 'true');
  } else if (args.command === 'review' && args.pr) {
    const repoParts = getRepo();
    if (repoParts) await manager.reviewPullRequest(repoParts[0], repoParts[1], parseInt(args.pr));
  } else if (args.command === 'changelog' && args.generate) {
    const repoParts = getRepo();
    if (repoParts) await manager.generateChangelog(repoParts[0], repoParts[1], args.since);
  } else if (args.command === 'issues') {
    const repoParts = getRepo();
    if (repoParts) await manager.manageIssues(repoParts[0], repoParts[1], args.action, args);
  } else if (args.command === 'ci' && args.setup) {
    const repoParts = getRepo();
    if (repoParts) await manager.setupCICD(repoParts[0], repoParts[1]);
  } else {
    console.log(`
GitHub Manager CLI - 全面的GitHub仓库管理工具

常用命令:
  github config --token <token> --username <username>  配置GitHub认证
  github repos list                                    列出所有仓库
  github repos create --name <name> [--description]    创建新仓库
  github review pr --repo <owner/repo> --pr <number>   审查PR
  github changelog generate --repo <owner/repo>        生成changelog
  github issues list --repo <owner/repo>               列出issue
  github ci setup --repo <owner/repo>                  设置CI/CD

示例:
  github config --token ghp_abc123 --username yourname
  github repos list
  github review pr --repo owner/repo --pr 123
  github changelog generate --repo owner/repo
  github issues list --repo owner/repo
  github ci setup --repo owner/repo
    `);
  }
}

main().catch((error) => {
  console.error('Error:', error.message || error);
  process.exit(1);
});