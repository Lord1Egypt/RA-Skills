#!/usr/bin/env node

/**
 * 项目管理工具
 * - 列出用户/组织/仓库项目
 * - 创建项目并初始化默认列
 * - 管理项目看板卡片
 * - 管理里程碑
 * - 生成周报
 */

const fs = require('fs');
const path = require('path');
const { Octokit } = require('@octokit/rest');
const chalk = require('chalk');

class ProjectManager {
  constructor(token, username) {
    this.octokit = new Octokit({
      auth: token,
      userAgent: 'GitHub Project Manager v1.0.0'
    });
    this.username = username;
  }

  /** Projects v2 API 请求头（必须指定版本） */
  _projectsV2Headers() {
    return { 'X-GitHub-Api-Version': '2022-11-28' };
  }

  /**
   * 列出项目（Projects v2 API）
   * - 指定 repo 时：先校验仓库存在，再列出该 owner 下的所有 v2 项目
   * - 仅指定 target 时：列出该用户或组织下的所有 v2 项目
   * - 当前用户的项目优先用 GET /user/projectsV2（避免 404）
   */
  async listProjects(target, repo) {
    console.log(chalk.blue('\n📋 列出项目 (Projects v2)\n'));

    try {
      let owner = target;

      if (repo) {
        const parts = repo.split('/');
        owner = parts[0];
        const repoName = parts[1];
        try {
          await this.octokit.repos.get({ owner, repo: repoName });
        } catch (err) {
          if (err.status === 404) {
            console.error(chalk.red(`❌ 仓库 ${repo} 不存在或无权访问，请检查 owner/repo 是否正确`));
            return;
          }
          throw err;
        }
        console.log(chalk.gray(`仓库 ${repo} 存在，正在列出 ${owner} 下的项目…\n`));
      }

      const h = this._projectsV2Headers();
      let list = [];

      // 当前用户：使用 /users/{username}/projectsV2（需 Token 具 project/read:project 权限）
      if (owner === this.username) {
        try {
          const res = await this.octokit.request('GET /users/{username}/projectsV2', {
            username: owner,
            per_page: 100,
            headers: h
          });
          list = res.data || [];
        } catch (err) {
          if (err.status === 404 || err.status === 403) {
            console.log(chalk.yellow('无法列出当前用户的 Projects v2。'));
            console.log(chalk.gray('请确认 Token 具有 project 或 read:project 权限：'));
            console.log(chalk.gray('  https://github.com/settings/tokens → 编辑 Token → 勾选 project'));
            return;
          }
          throw err;
        }
      } else {
        // 先尝试组织，再尝试其他用户
        try {
          const orgRes = await this.octokit.request('GET /orgs/{org}/projectsV2', {
            org: owner,
            per_page: 100,
            headers: h
          });
          list = orgRes.data || [];
        } catch (err) {
          if (err.status === 404) {
            try {
              const userRes = await this.octokit.request('GET /users/{username}/projectsV2', {
                username: owner,
                per_page: 100,
                headers: h
              });
              list = userRes.data || [];
            } catch (err2) {
              if (err2.status === 404 || err2.status === 403) {
                console.log(chalk.yellow(`${owner} 下暂无可见的 Projects v2，或 Token 无 project/read:project 权限。`));
                console.log(chalk.gray('请确认 Token 权限：https://github.com/settings/tokens'));
                return;
              }
              throw err2;
            }
          } else {
            throw err;
          }
        }
      }

      if (list.length === 0) {
        console.log(chalk.yellow(`${owner} 下暂无 Projects v2 项目`));
        console.log(chalk.gray('可在 GitHub 网页端创建：https://github.com/' + (repo || owner)));
        return;
      }

      list.forEach((p, idx) => {
        const title = p.title || p.name || '(无标题)';
        const num = p.number != null ? p.number : p.id;
        const url = p.html_url || '';
        const desc = p.short_description || p.description || '';
        console.log(`${idx + 1}. ${chalk.bold(title)} #${num}`);
        if (desc) console.log(`   ${desc}`);
        if (url) console.log(`   ${chalk.cyan(url)}`);
        console.log('');
      });
    } catch (error) {
      console.error(chalk.red(`❌ 列出项目失败: ${error.message}`));
    }
  }

  /**
   * 创建项目（Projects v2）
   * REST 无创建 v2 项目的接口，需使用网页或 GraphQL。本命令仅给出说明。
   */
  async createProject(target, repo, name, description = '', template = 'basic') {
    console.log(chalk.blue('\n🆕 创建项目 (Projects v2)\n'));
    console.log(chalk.yellow('Projects v2 暂不支持通过 REST 创建。'));
    console.log(chalk.gray('请使用以下方式之一：'));
    console.log(chalk.gray('  • 网页：https://github.com/' + (target || this.username) + '?tab=projects → New project'));
    console.log(chalk.gray('  • GraphQL：createProjectV2 mutation'));
    if (name) console.log(chalk.gray('  建议项目名称：' + name));
  }

  /**
   * Projects v2 无「列」概念，使用视图与字段。本方法保留为空实现。
   */
  async createDefaultColumns(projectId, template = 'basic') {
    // no-op for v2
  }

  /**
   * 管理项目项（Projects v2 Items API）
   * owner: 组织名或用户名；projectNumber: 项目编号（list 输出中的 #数字）
   */
  async manageCards(owner, projectNumber, action, options = {}) {
    console.log(chalk.blue('\n🗂️ 项目项 (Projects v2)\n'));

    const h = this._projectsV2Headers();

    const tryOrg = async () => {
      return this.octokit.request('GET /orgs/{org}/projectsV2/{project_number}/items', {
        org: owner,
        project_number: projectNumber,
        per_page: 100,
        headers: h
      });
    };
    const tryUser = async () => {
      return this.octokit.request('GET /users/{username}/projectsV2/{project_number}/items', {
        username: owner,
        project_number: projectNumber,
        per_page: 100,
        headers: h
      });
    };

    try {
      let itemsRes;
      try {
        itemsRes = await tryOrg();
      } catch (err) {
        if (err.status === 404) {
          itemsRes = await tryUser();
        } else {
          throw err;
        }
      }

      const items = Array.isArray(itemsRes.data)
        ? itemsRes.data
        : (itemsRes.data?.items || []);

      if (action === 'list') {
        if (items.length === 0) {
          console.log(chalk.yellow('该项目暂无项'));
          return;
        }
        items.forEach((item, idx) => {
          const content = item.content;
          const title = content?.title || item.title || '(无标题)';
          const type = content ? (content.pull_request ? 'PR' : 'Issue') : 'Draft';
          const num = content?.number ? `#${content.number}` : '';
          console.log(`  ${idx + 1}. [${type}] ${title} ${num}`);
        });
        return;
      }

      if (action === 'add') {
        const { note, issue } = options;
        const isOrg = await this._isOrg(owner);

        if (issue) {
          const match = issue.match(/^([^/]+)\/([^#]+)#(\d+)$/);
          if (!match) {
            console.error(chalk.red('❌ issue 格式应为 owner/repo#number'));
            return;
          }
          const [, o, repoName, numStr] = match;
          const issueNum = parseInt(numStr, 10);
          const issueData = await this.octokit.issues.get({
            owner: o,
            repo: repoName,
            issue_number: issueNum
          });
          const contentId = issueData.data.node_id;
          const contentType = issueData.data.pull_request ? 'PullRequest' : 'Issue';

          const path = isOrg
            ? 'POST /orgs/{org}/projectsV2/{project_number}/items'
            : 'POST /users/{username}/projectsV2/{project_number}/items';
          const params = isOrg
            ? { org: owner, project_number: projectNumber, data: { content_id: contentId, content_type: contentType }, headers: h }
            : { username: owner, project_number: projectNumber, data: { content_id: contentId, content_type: contentType }, headers: h };
          await this.octokit.request(path, params);
          console.log(chalk.green(`✅ 已添加 ${contentType} #${issueNum} 到项目`));
          return;
        }

        if (note) {
          const path = isOrg
            ? 'POST /orgs/{org}/projectsV2/{project_number}/items'
            : 'POST /users/{username}/projectsV2/{project_number}/items';
          const params = isOrg
            ? { org: owner, project_number: projectNumber, data: { body: note }, headers: h }
            : { username: owner, project_number: projectNumber, data: { body: note }, headers: h };
          await this.octokit.request(path, params);
          console.log(chalk.green('✅ 已添加备注项到项目'));
          return;
        }

        console.error(chalk.red('❌ 请提供 --note <内容> 或 --issue owner/repo#number'));
      }
    } catch (error) {
      console.error(chalk.red(`❌ 管理项目项失败: ${error.message}`));
    }
  }

  async _isOrg(owner) {
    try {
      await this.octokit.orgs.get({ org: owner });
      return true;
    } catch {
      return false;
    }
  }

  /**
   * 管理里程碑（列出 / 报告）
   */
  async manageMilestones(owner, repo, action, options = {}) {
    console.log(chalk.blue('\n🎯 里程碑\n'));

    try {
      if (action === 'list') {
        const res = await this.octokit.issues.listMilestones({
          owner,
          repo,
          state: 'all',
          per_page: 50
        });

        if (res.data.length === 0) {
          console.log(chalk.yellow('暂无里程碑'));
          return;
        }

        res.data.forEach((m, idx) => {
          console.log(`${idx + 1}. ${chalk.bold(m.title)} (编号: ${m.number})`);
          console.log(`   状态: ${m.state} | 截止: ${m.due_on || '未设置'}`);
          console.log(`   进度: 打开 ${m.open_issues} / 关闭 ${m.closed_issues}`);
          console.log('');
        });
        return;
      }

      if (action === 'report') {
        const { number } = options;
        if (!number) {
          console.error(chalk.red('❌ 请通过 --number 指定里程碑编号'));
          return;
        }

        const milestone = await this.octokit.issues.getMilestone({
          owner,
          repo,
          milestone_number: number
        });

        console.log(chalk.bold(`\n📊 里程碑报告: ${milestone.data.title}`));
        console.log(`状态: ${milestone.data.state}`);
        console.log(`截止日期: ${milestone.data.due_on || '未设置'}`);
        console.log(`打开 issues: ${milestone.data.open_issues}`);
        console.log(`关闭 issues: ${milestone.data.closed_issues}`);

        const issues = await this.octokit.issues.listForRepo({
          owner,
          repo,
          milestone: number,
          state: 'all',
          per_page: 100
        });

        console.log('\nIssues:');
        issues.data.forEach((issue) => {
          console.log(`- #${issue.number} [${issue.state}] ${issue.title}`);
        });
      }
    } catch (error) {
      console.error(chalk.red(`❌ 里程碑操作失败: ${error.message}`));
    }
  }

  /**
   * 生成周报
   */
  async generateWeeklyReport(owner, repo) {
    console.log(chalk.blue('\n🗓️ 生成周报\n'));

    try {
      const now = new Date();
      const since = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);
      const sinceISO = since.toISOString();

      console.log(chalk.gray(`时间范围: ${since.toISOString()} ~ ${now.toISOString()}`));

      const [issues, pulls] = await Promise.all([
        this.octokit.issues.listForRepo({
          owner,
          repo,
          state: 'all',
          since: sinceISO,
          per_page: 100
        }),
        this.octokit.pulls.list({
          owner,
          repo,
          state: 'all',
          per_page: 100
        })
      ]);

      console.log(chalk.bold('\n📌 Issues（最近一周更新）'));
      const recentIssues = issues.data.filter((i) => new Date(i.updated_at) >= since);
      if (recentIssues.length === 0) {
        console.log('  无');
      } else {
        recentIssues.forEach((issue) => {
          console.log(`- #${issue.number} [${issue.state}] ${issue.title}`);
        });
      }

      console.log(chalk.bold('\n📌 Pull Requests（最近一周更新）'));
      const recentPRs = pulls.data.filter((pr) => new Date(pr.updated_at) >= since);
      if (recentPRs.length === 0) {
        console.log('  无');
      } else {
        recentPRs.forEach((pr) => {
          console.log(`- #${pr.number} [${pr.state}] ${pr.title}`);
        });
      }
    } catch (error) {
      console.error(chalk.red(`❌ 生成周报失败: ${error.message}`));
    }
  }
}

// CLI接口
if (require.main === module) {
  const args = process.argv.slice(2);

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

  const manager = new ProjectManager(config.github.token, config.github.username);

  const cmd = args[0];

  if (cmd === 'list') {
    const arg1 = args[1];
    const arg2 = args[2];

    let target = config.github.username;
    let repo = undefined;

    if (arg2) {
      // 形如: list owner repoName  或 list owner owner/repo
      if (arg2.includes('/')) {
        target = arg1 || config.github.username;
        repo = arg2;
      } else {
        target = arg1 || config.github.username;
        repo = `${target}/${arg2}`;
      }
    } else if (arg1) {
      // 形如: list owner  或 list owner/repo
      if (arg1.includes('/')) {
        repo = arg1;
      } else {
        target = arg1;
      }
    }

    manager.listProjects(target, repo);
  } else if (cmd === 'create') {
    const target = args[1] || config.github.username;
    const repo = args[2];
    const name = args[3];
    const description = args[4] || '';
    const template = args[5] || 'basic';

    if (!name) {
      console.error(chalk.red('❌ 请指定项目名称'));
      process.exit(1);
    }

    manager.createProject(target, repo, name, description, template);
  } else if (cmd === 'cards') {
    const sub = args[1];
    const owner = args[2];
    const projectNumber = parseInt(args[3], 10);

    if (!owner || !projectNumber || isNaN(projectNumber)) {
      console.error(chalk.red('❌ 用法: cards list <owner> <project_number>  或  cards add <owner> <project_number> [--note "内容" | <owner/repo#number>]'));
      process.exit(1);
    }

    if (sub === 'list') {
      manager.manageCards(owner, projectNumber, 'list');
    } else if (sub === 'add') {
      let note = null;
      let issue = null;
      for (let i = 4; i < args.length; i++) {
        if (args[i] === '--note' && args[i + 1]) {
          note = args[i + 1];
          break;
        }
        if (args[i] === '--issue' && args[i + 1]) {
          issue = args[i + 1];
          break;
        }
        if (args[i].includes('#')) {
          issue = args[i];
          break;
        }
      }
      manager.manageCards(owner, projectNumber, 'add', { note, issue });
    } else {
      console.error(chalk.red('❌ 请使用 cards list 或 cards add'));
      process.exit(1);
    }
  } else if (cmd === 'milestones') {
    const repo = args[2] || config.github.defaultRepo;

    if (!repo) {
      console.error(chalk.red('❌ 请指定仓库'));
      process.exit(1);
    }

    const [owner, repoName] = repo.split('/');

    if (args[1] === 'list') {
      manager.manageMilestones(owner, repoName, 'list');
    } else if (args[1] === 'report') {
      const number = parseInt(args[3], 10);
      manager.manageMilestones(owner, repoName, 'report', { number });
    }
  } else if (cmd === 'weekly') {
    const repo = args[1] || config.github.defaultRepo;

    if (!repo) {
      console.error(chalk.red('❌ 请指定仓库'));
      process.exit(1);
    }

    const [owner, repoName] = repo.split('/');
    manager.generateWeeklyReport(owner, repoName);
  } else {
    console.log(`
项目管理工具 (Projects v2)

用法:
  node project-manager.js list [owner] [repo]                    列出项目
  node project-manager.js create [owner] [repo] <name>           创建项目（提示用网页/GraphQL）
  node project-manager.js cards list <owner> <project_number>   列出项目项
  node project-manager.js cards add <owner> <project_number> --issue owner/repo#number
  node project-manager.js milestones list <owner/repo>          列出里程碑
  node project-manager.js milestones report <owner/repo> --number <id>
  node project-manager.js weekly <owner/repo>                   生成周报

示例:
  node project-manager.js list VeyraDev
  node project-manager.js list VeyraDev AI-Intel
  node project-manager.js cards list VeyraDev 1
  node project-manager.js cards add VeyraDev 1 --issue VeyraDev/AI-Intel#3
  node project-manager.js weekly VeyraDev/AI-Intel
    `);
  }
}

module.exports = ProjectManager;