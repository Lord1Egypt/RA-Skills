#!/usr/bin/env node

/**
 * 代码审查工具
 * 自动分析PR代码质量并提供审查建议
 */

const fs = require('fs');
const path = require('path');
const { Octokit } = require('@octokit/rest');
const chalk = require('chalk');

class CodeReviewer {
  constructor(token, username) {
    this.octokit = new Octokit({
      auth: token,
      userAgent: 'GitHub Code Reviewer v1.0.0'
    });
    this.username = username;
  }

  /**
   * 审查单个PR
   */
  async reviewPullRequest(owner, repo, prNumber) {
    console.log(chalk.blue(`\n🔍 开始审查 PR #${prNumber}: ${owner}/${repo}\n`));

    try {
      // 1. 获取PR基本信息
      const pr = await this.octokit.pulls.get({
        owner,
        repo,
        pull_number: prNumber
      });

      console.log(chalk.bold(`📋 PR标题: ${pr.data.title}`));
      console.log(`👤 作者: ${pr.data.user.login}`);
      console.log(`🌿 分支: ${pr.data.head.ref} → ${pr.data.base.ref}`);
      console.log(`📅 创建时间: ${new Date(pr.data.created_at).toLocaleString('zh-CN')}`);
      console.log(`📝 描述: ${pr.data.body || '无描述'}`);
      console.log(chalk.gray('─'.repeat(50)));

      // 2. 获取文件变更
      const files = await this.octokit.pulls.listFiles({
        owner,
        repo,
        pull_number: prNumber,
        per_page: 100
      });

      console.log(chalk.bold(`📄 文件变更 (${files.data.length}个文件):`));
      
      let totalAdditions = 0;
      let totalDeletions = 0;
      const fileAnalysis = [];

      files.data.forEach((file, index) => {
        totalAdditions += file.additions;
        totalDeletions += file.deletions;
        
        const analysis = this.analyzeFile(file);
        fileAnalysis.push(analysis);
        
        console.log(`\n${index + 1}. ${chalk.bold(file.filename)}`);
        console.log(`   📊 +${file.additions} -${file.deletions} (${file.changes}处变更)`);
        console.log(`   📝 状态: ${this.getStatusEmoji(file.status)} ${file.status}`);
        
        if (analysis.suggestions.length > 0) {
          console.log(`   💡 建议:`);
          analysis.suggestions.forEach(suggestion => {
            console.log(`     • ${suggestion}`);
          });
        }
      });

      console.log(chalk.gray('─'.repeat(50)));
      console.log(chalk.bold(`📊 变更统计:`));
      console.log(`   📈 总增加行数: ${chalk.green(`+${totalAdditions}`)}`);
      console.log(`   📉 总删除行数: ${chalk.red(`-${totalDeletions}`)}`);
      console.log(`   📋 总变更行数: ${chalk.blue(totalAdditions + totalDeletions)}`);

      // 3. 提供总体建议
      this.provideOverallSuggestions(pr.data, files.data, fileAnalysis);

      // 4. 检查安全问题
      await this.checkSecurityIssues(files.data);

      // 5. 检查测试覆盖率
      await this.checkTestCoverage(owner, repo, prNumber);

      return {
        pr: pr.data,
        files: files.data,
        analysis: fileAnalysis,
        summary: {
          totalFiles: files.data.length,
          totalAdditions,
          totalDeletions,
          totalChanges: totalAdditions + totalDeletions
        }
      };

    } catch (error) {
      console.error(chalk.red(`❌ 审查失败: ${error.message}`));
      return null;
    }
  }

  /**
   * 分析单个文件
   */
  analyzeFile(file) {
    const suggestions = [];
    const warnings = [];

    // 检查文件大小
    if (file.changes > 500) {
      suggestions.push('文件变更较大，考虑拆分为多个小PR');
    }

    // 检查文件类型
    const ext = path.extname(file.filename).toLowerCase();
    
    if (ext === '.js' || ext === '.ts' || ext === '.jsx' || ext === '.tsx') {
      suggestions.push('JavaScript/TypeScript文件 - 建议运行ESLint检查');
      
      // 检查是否有console.log
      if (file.patch && file.patch.includes('console.log')) {
        warnings.push('发现console.log语句，生产代码中建议移除');
      }
    }

    if (ext === '.json') {
      suggestions.push('JSON配置文件 - 验证格式是否正确');
    }

    if (ext === '.md') {
      suggestions.push('文档文件 - 检查拼写和格式');
    }

    // 检查二进制文件
    if (file.filename.match(/\.(png|jpg|jpeg|gif|pdf|zip)$/i)) {
      warnings.push('二进制文件 - 确保文件大小合理');
    }

    // 检查敏感信息
    if (file.patch) {
      const sensitivePatterns = [
        /password\s*[:=]\s*['"][^'"]+['"]/i,
        /token\s*[:=]\s*['"][^'"]+['"]/i,
        /api[_-]?key\s*[:=]\s*['"][^'"]+['"]/i,
        /secret\s*[:=]\s*['"][^'"]+['"]/i
      ];

      sensitivePatterns.forEach(pattern => {
        if (pattern.test(file.patch)) {
          warnings.push('⚠️ 发现可能的敏感信息，请确认是否需要提交');
        }
      });
    }

    return {
      filename: file.filename,
      additions: file.additions,
      deletions: file.deletions,
      changes: file.changes,
      status: file.status,
      suggestions,
      warnings
    };
  }

  /**
   * 提供总体建议
   */
  provideOverallSuggestions(pr, files, fileAnalysis) {
    console.log(chalk.gray('─'.repeat(50)));
    console.log(chalk.bold(`💡 总体审查建议:`));

    const suggestions = [];

    // 检查PR大小
    const totalChanges = fileAnalysis.reduce((sum, file) => sum + file.changes, 0);
    if (totalChanges > 1000) {
      suggestions.push('PR变更较大，建议拆分为多个小PR以便审查');
    }

    // 检查测试文件
    const hasTestFiles = files.some(file => 
      file.filename.includes('test') || 
      file.filename.includes('spec') ||
      file.filename.includes('__tests__')
    );

    if (!hasTestFiles && totalChanges > 100) {
      suggestions.push('未发现测试文件，建议添加相关测试');
    }

    // 检查文档更新
    const hasDocUpdates = files.some(file => 
      file.filename.endsWith('.md') || 
      file.filename.includes('README') ||
      file.filename.includes('docs/')
    );

    if (!hasDocUpdates && totalChanges > 50) {
      suggestions.push('建议更新相关文档以反映代码变更');
    }

    // 检查大文件
    const largeFiles = files.filter(file => file.changes > 200);
    if (largeFiles.length > 0) {
      suggestions.push(`发现${largeFiles.length}个大文件，建议优化代码结构`);
    }

    // 输出建议
    if (suggestions.length === 0) {
      console.log(chalk.green('✅ PR结构良好，无特殊建议'));
    } else {
      suggestions.forEach((suggestion, index) => {
        console.log(`${index + 1}. ${suggestion}`);
      });
    }

    // 检查警告
    const allWarnings = fileAnalysis.flatMap(file => file.warnings);
    if (allWarnings.length > 0) {
      console.log(chalk.yellow('\n⚠️ 警告:'));
      [...new Set(allWarnings)].forEach((warning, index) => {
        console.log(`${index + 1}. ${warning}`);
      });
    }
  }

  /**
   * 检查安全问题
   */
  async checkSecurityIssues(files) {
    console.log(chalk.gray('─'.repeat(50)));
    console.log(chalk.bold(`🔒 安全检查:`));

    const securityIssues = [];

    files.forEach(file => {
      if (file.patch) {
        // 检查硬编码的凭证
        if (file.patch.match(/['"](?:[A-Za-z0-9+/]{40,}|gh[ops]_[A-Za-z0-9_]{36,})['"]/)) {
          securityIssues.push(`文件 ${file.filename} 中可能包含硬编码的API token`);
        }

        // 检查SQL注入风险
        if (file.patch.match(/SELECT|INSERT|UPDATE|DELETE.*['"][^'"]+\+[^'"]+['"]/i)) {
          securityIssues.push(`文件 ${file.filename} 中可能存在SQL注入风险`);
        }

        // 检查eval使用
        if (file.patch.includes('eval(')) {
          securityIssues.push(`文件 ${file.filename} 中使用eval，存在安全风险`);
        }
      }
    });

    if (securityIssues.length === 0) {
      console.log(chalk.green('✅ 未发现明显安全问题'));
    } else {
      console.log(chalk.red('❌ 发现安全问题:'));
      securityIssues.forEach((issue, index) => {
        console.log(`${index + 1}. ${issue}`);
      });
    }
  }

  /**
   * 检查测试覆盖率
   */
  async checkTestCoverage(owner, repo, prNumber) {
    console.log(chalk.gray('─'.repeat(50)));
    console.log(chalk.bold(`🧪 测试检查:`));

    try {
      // 获取检查运行状态
      const checks = await this.octokit.checks.listForRef({
        owner,
        repo,
        ref: `pull/${prNumber}/head`
      });

      const testChecks = checks.data.check_runs.filter(check => 
        check.name.toLowerCase().includes('test') ||
        check.name.toLowerCase().includes('coverage')
      );

      if (testChecks.length === 0) {
        console.log(chalk.yellow('⚠️ 未发现测试检查运行'));
        return;
      }

      testChecks.forEach(check => {
        const status = check.status;
        const conclusion = check.conclusion;
        const emoji = this.getCheckEmoji(status, conclusion);
        
        console.log(`${emoji} ${check.name}: ${status} (${conclusion || '运行中'})`);
        
        if (check.output && check.output.title) {
          console.log(`   ${check.output.title}`);
        }
      });

    } catch (error) {
      console.log(chalk.yellow('⚠️ 无法获取测试检查状态'));
    }
  }

  /**
   * 获取状态表情
   */
  getStatusEmoji(status) {
    const emojis = {
      added: '🆕',
      modified: '📝',
      removed: '🗑️',
      renamed: '📛',
      copied: '📋'
    };
    return emojis[status] || '📄';
  }

  /**
   * 获取检查表情
   */
  getCheckEmoji(status, conclusion) {
    if (status !== 'completed') return '⏳';
    
    switch (conclusion) {
      case 'success': return '✅';
      case 'failure': return '❌';
      case 'cancelled': return '🚫';
      case 'skipped': return '⏭️';
      default: return '❓';
    }
  }

  /**
   * 批量审查PR
   */
  async reviewAllOpenPRs(owner, repo) {
    console.log(chalk.blue(`\n📋 开始审查 ${owner}/${repo} 的所有打开PR\n`));

    try {
      const prs = await this.octokit.pulls.list({
        owner,
        repo,
        state: 'open',
        sort: 'created',
        direction: 'desc',
        per_page: 20
      });

      if (prs.data.length === 0) {
        console.log(chalk.yellow('📭 没有打开的PR需要审查'));
        return [];
      }

      console.log(chalk.bold(`找到 ${prs.data.length} 个打开的PR:\n`));

      const reviews = [];
      for (const pr of prs.data) {
        console.log(chalk.cyan(`\n${'═'.repeat(50)}`));
        console.log(chalk.bold(`PR #${pr.number}: ${pr.title}`));
        console.log(chalk.cyan(`${'═'.repeat(50)}`));
        
        const review = await this.reviewPullRequest(owner, repo, pr.number);
        if (review) {
          reviews.push(review);
        }
        
        // 添加间隔
        if (pr !== prs.data[prs.data.length - 1]) {
          console.log('\n');
        }
      }

      console.log(chalk.green(`\n✅ 完成审查 ${reviews.length} 个PR`));
      return reviews;

    } catch (error) {
      console.error(chalk.red(`❌ 批量审查失败: ${error.message}`));
      return [];
    }
  }
}

// CLI接口
if (require.main === module) {
  const args = process.argv.slice(2);
  
  // 读取配置文件
  const configPath = path.join(__dirname, '..', '.github-manager.json');
  let config = {};
  
  try {
    if (fs.existsSync(configPath)) {
      config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
    }
  } catch (error) {
    console.error(chalk.red('❌ 无法读取配置文件'));
    process.exit(1);
  }

  if (!config.github || !config.github.token || !config.github.username) {
    console.error(chalk.red('❌ 请先配置GitHub认证信息'));
    console.log(chalk.yellow('运行: github config --token <token> --username <username>'));
    process.exit(1);
  }

  const reviewer = new CodeReviewer(config.github.token, config.github.username);

  if (args[0] === 'pr' && args[1]) {
    const prNumber = parseInt(args[1]);
    const repo = args[2] || config.github.defaultRepo;
    
    if (!repo) {
      console.error(chalk.red('❌ 请指定仓库或设置默认仓库'));
      process.exit(1);
    }
    
    const [owner, repoName] = repo.split('/');
    reviewer.reviewPullRequest(owner, repoName, prNumber);
    
  } else if (args[0] === 'all') {
    const repo = args[1] || config.github.defaultRepo;
    
    if (!repo) {
      console.error(chalk.red('❌ 请指定仓库或设置默认仓库'));
      process.exit(1);
    }
    
    const [owner, repoName] = repo.split('/');
    reviewer.reviewAllOpenPRs(owner, repoName);
    
  } else {
    console.log(`
代码审查工具

用法:
  node code-review.js pr <pr-number> [owner/repo]  审查单个PR
  node code-review.js all [owner/repo]            审查所有打开的PR

  owner/repo 可为任意 GitHub 用户或组织的仓库（需 token 有读权限）。

示例:
  node code-review.js pr 123 VeyraDev/my-repo
  node code-review.js pr 456 facebook/react
  node code-review.js all owner/repo
    `);
  }
}

module.exports = CodeReviewer;