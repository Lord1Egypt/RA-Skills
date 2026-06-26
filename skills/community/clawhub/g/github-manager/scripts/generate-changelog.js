#!/usr/bin/env node

/**
 * Changelog Generator
 * 自动生成基于commit历史的changelog
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const chalk = require('chalk');

class ChangelogGenerator {
  constructor(options = {}) {
    this.options = {
      types: ['feat', 'fix', 'docs', 'style', 'refactor', 'perf', 'test', 'chore'],
      excludeScopes: ['deps', 'ci'],
      template: 'keepachangelog',
      outputFile: 'CHANGELOG.md',
      ...options
    };
  }

  /**
   * 获取git commit历史
   */
  getGitLog(sinceTag = null) {
    try {
      let command = 'git log --pretty=format:"%H|%an|%ad|%s" --date=short';
      
      if (sinceTag) {
        command += ` ${sinceTag}..HEAD`;
      }
      
      const output = execSync(command, { encoding: 'utf8' });
      return output.trim().split('\n').map(line => {
        const [hash, author, date, message] = line.split('|');
        return { hash, author, date, message };
      });
    } catch (error) {
      console.error(chalk.red('Error getting git log:'), error.message);
      return [];
    }
  }

  /**
   * 解析commit消息
   */
  parseCommitMessage(message) {
    const patterns = [
      // 常规格式: type(scope): description
      /^(\w+)(?:\(([^)]+)\))?:\s*(.+)$/,
      // 简化格式: type: description
      /^(\w+):\s*(.+)$/,
      // 包含breaking change
      /^(\w+)(?:\(([^)]+)\))?!:\s*(.+)$/
    ];

    for (const pattern of patterns) {
      const match = message.match(pattern);
      if (match) {
        const [, type, scope, description] = match;
        const isBreaking = message.includes('!:'); // 包含breaking change标识
        
        return {
          type: type.toLowerCase(),
          scope: scope || '',
          description: description.trim(),
          isBreaking,
          raw: message
        };
      }
    }

    // 无法解析的commit
    return {
      type: 'other',
      scope: '',
      description: message,
      isBreaking: false,
      raw: message
    };
  }

  /**
   * 分类commits
   */
  categorizeCommits(commits) {
    const categories = {
      feat: { title: '🚀 New Features', items: [] },
      fix: { title: '🐛 Bug Fixes', items: [] },
      docs: { title: '📝 Documentation', items: [] },
      style: { title: '🎨 Code Style', items: [] },
      refactor: { title: '♻️ Refactoring', items: [] },
      perf: { title: '⚡ Performance', items: [] },
      test: { title: '✅ Tests', items: [] },
      chore: { title: '🔧 Chores', items: [] },
      breaking: { title: '⚠️ Breaking Changes', items: [] },
      other: { title: '📦 Other Changes', items: [] }
    };

    commits.forEach(commit => {
      const parsed = this.parseCommitMessage(commit.message);
      
      // 排除特定scope
      if (this.options.excludeScopes.includes(parsed.scope)) {
        return;
      }

      // 处理breaking changes
      if (parsed.isBreaking) {
        categories.breaking.items.push({
          description: parsed.description,
          author: commit.author,
          date: commit.date,
          hash: commit.hash,
          scope: parsed.scope
        });
        return;
      }

      // 分类到对应类型
      if (categories[parsed.type]) {
        categories[parsed.type].items.push({
          description: parsed.description,
          author: commit.author,
          date: commit.date,
          hash: commit.hash,
          scope: parsed.scope
        });
      } else {
        categories.other.items.push({
          description: parsed.description,
          author: commit.author,
          date: commit.date,
          hash: commit.hash,
          scope: parsed.scope
        });
      }
    });

    // 过滤空分类
    return Object.entries(categories)
      .filter(([_, category]) => category.items.length > 0)
      .reduce((acc, [key, category]) => {
        acc[key] = category;
        return acc;
      }, {});
  }

  /**
   * 生成版本号
   */
  generateVersion(currentVersion = '0.0.0', commits) {
    const categorized = this.categorizeCommits(commits);
    
    let [major, minor, patch] = currentVersion.replace(/^v/, '').split('.').map(Number);
    
    if (categorized.breaking) {
      major++;
      minor = 0;
      patch = 0;
    } else if (categorized.feat) {
      minor++;
      patch = 0;
    } else if (categorized.fix || categorized.other) {
      patch++;
    }
    
    return `v${major}.${minor}.${patch}`;
  }

  /**
   * 生成changelog内容
   */
  generateChangelogContent(version, date, categorizedCommits) {
    let content = `# Changelog\n\n`;
    content += `## ${version} (${date})\n\n`;

    // 按特定顺序输出分类
    const order = ['breaking', 'feat', 'fix', 'docs', 'style', 'refactor', 'perf', 'test', 'chore', 'other'];
    
    order.forEach(categoryKey => {
      const category = categorizedCommits[categoryKey];
      if (category) {
        content += `### ${category.title}\n\n`;
        
        category.items.forEach(item => {
          const scope = item.scope ? `**${item.scope}**: ` : '';
          const author = item.author ? ` (@${item.author})` : '';
          content += `- ${scope}${item.description}${author}\n`;
        });
        
        content += '\n';
      }
    });

    return content;
  }

  /**
   * 更新changelog文件
   */
  updateChangelogFile(newContent, prepend = true) {
    const filePath = path.join(process.cwd(), this.options.outputFile);
    let existingContent = '';
    
    try {
      if (fs.existsSync(filePath)) {
        existingContent = fs.readFileSync(filePath, 'utf8');
      }
    } catch (error) {
      console.error(chalk.red('Error reading existing changelog:'), error.message);
    }
    
    const finalContent = prepend 
      ? newContent + '\n' + existingContent
      : existingContent + '\n' + newContent;
    
    try {
      fs.writeFileSync(filePath, finalContent);
      console.log(chalk.green(`✅ Changelog updated: ${filePath}`));
    } catch (error) {
      console.error(chalk.red('Error writing changelog:'), error.message);
    }
  }

  /**
   * 生成changelog
   */
  generate(sinceTag = null, currentVersion = null) {
    console.log(chalk.blue('📋 Generating changelog...'));
    
    // 获取commits
    const commits = this.getGitLog(sinceTag);
    
    if (commits.length === 0) {
      console.log(chalk.yellow('⚠️ No new commits found'));
      return null;
    }
    
    console.log(chalk.blue(`📊 Found ${commits.length} commits`));
    
    // 生成版本号
    const version = currentVersion || this.generateVersion('0.0.0', commits);
    const date = new Date().toISOString().split('T')[0];
    
    // 分类commits
    const categorizedCommits = this.categorizeCommits(commits);
    
    // 生成内容
    const changelogContent = this.generateChangelogContent(version, date, categorizedCommits);
    
    // 输出到控制台
    console.log('\n' + chalk.cyan('='.repeat(50)));
    console.log(chalk.bold(`📦 Version: ${version}`));
    console.log(chalk.cyan('='.repeat(50)));
    console.log(changelogContent);
    
    // 更新文件
    this.updateChangelogFile(changelogContent);
    
    return {
      version,
      date,
      commitCount: commits.length,
      categories: Object.keys(categorizedCommits),
      content: changelogContent
    };
  }

  /**
   * 从package.json获取当前版本
   */
  getCurrentVersion() {
    try {
      const packagePath = path.join(process.cwd(), 'package.json');
      if (fs.existsSync(packagePath)) {
        const pkg = JSON.parse(fs.readFileSync(packagePath, 'utf8'));
        return pkg.version;
      }
    } catch (error) {
      console.error(chalk.yellow('Warning: Could not read package.json'));
    }
    return null;
  }

  /**
   * 获取最新的tag
   */
  getLatestTag() {
    try {
      const tag = execSync('git describe --tags --abbrev=0', { encoding: 'utf8' }).trim();
      return tag;
    } catch (error) {
      console.log(chalk.yellow('No previous tags found'));
      return null;
    }
  }
}

// CLI接口
if (require.main === module) {
  const args = process.argv.slice(2);
  const options = {};
  
  // 解析参数
  args.forEach((arg, index) => {
    if (arg === '--since' && args[index + 1]) {
      options.sinceTag = args[index + 1];
    } else if (arg === '--version' && args[index + 1]) {
      options.currentVersion = args[index + 1];
    } else if (arg === '--output' && args[index + 1]) {
      options.outputFile = args[index + 1];
    } else if (arg === '--template' && args[index + 1]) {
      options.template = args[index + 1];
    }
  });
  
  const generator = new ChangelogGenerator(options);
  
  // 获取最新tag作为since参数
  const sinceTag = options.sinceTag || generator.getLatestTag();
  
  // 获取当前版本
  const currentVersion = options.currentVersion || generator.getCurrentVersion();
  
  // 生成changelog
  const result = generator.generate(sinceTag, currentVersion);
  
  if (result) {
    console.log(chalk.green(`\n✅ Changelog generated successfully!`));
    console.log(chalk.blue(`Version: ${result.version}`));
    console.log(chalk.blue(`Commits: ${result.commitCount}`));
    console.log(chalk.blue(`Output: ${options.outputFile || 'CHANGELOG.md'}`));
  }
}

module.exports = ChangelogGenerator;