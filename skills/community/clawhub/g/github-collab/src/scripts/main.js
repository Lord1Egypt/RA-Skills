#!/usr/bin/env node

/**
 * GitHub 协同开发技能 - 主入口脚本
 * 负责任务分析、仓库创建、Agent 分配和进度跟踪
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

// 配置
const CONFIG = {
  defaultRepoName: 'collab-project',
  defaultVisibility: 'private',
  agents: {
    coder: 'coder',
    checker: 'checker',
    writer: 'memowriter'
  }
};

/**
 * 检查 GitHub CLI 是否可用
 */
function checkGitHubCLI() {
  try {
    const version = execSync('gh --version', { encoding: 'utf8' });
    console.log('✅ GitHub CLI 已安装:', version.split('\n')[0]);
    return true;
  } catch (error) {
    console.error('❌ GitHub CLI 未安装或未配置');
    throw new Error('GH_NOT_CONFIGURED: 请运行 `gh auth login` 配置 GitHub token');
  }
}

/**
 * 检查 GitHub token 是否配置
 */
function checkGitHubToken() {
  try {
    const token = execSync('gh auth status', { encoding: 'utf8' });
    console.log('✅ GitHub token 已配置');
    return true;
  } catch (error) {
    console.error('❌ GitHub token 未配置');
    throw new Error('TOKEN_INVALID: 请运行 `gh auth login` 配置 GitHub token');
  }
}

/**
 * 创建 GitHub 仓库
 */
function createRepository(repoName, description, visibility = 'private') {
  try {
    console.log(`📦 创建仓库：${repoName}`);
    const visibilityFlag = visibility === 'public' ? '--public' : visibility === 'private' ? '--private' : '';
    const cmd = `gh repo create ${repoName} --description "${description}" ${visibilityFlag}`;
    execSync(cmd, { encoding: 'utf8' });
    console.log(`✅ 仓库创建成功：https://github.com/${repoName}`);
    return repoName;
  } catch (error) {
    if (error.message.includes('already exists')) {
      console.warn(`⚠️ 仓库 ${repoName} 已存在`);
      return repoName;
    }
    throw new Error(`REPO_CREATE_FAILED: ${error.message}`);
  }
}

/**
 * 初始化项目结构
 */
function initProjectStructure(repoName) {
  const projectDir = path.join(process.cwd(), repoName);
  
  // 创建目录结构
  const dirs = ['docs', 'src', 'tests', 'scripts', '.github/workflows'];
  dirs.forEach(dir => {
    const fullPath = path.join(projectDir, dir);
    if (!fs.existsSync(fullPath)) {
      fs.mkdirSync(fullPath, { recursive: true });
    }
  });

  // 创建 README.md
  const readme = `# ${repoName}

## 项目说明

这是一个通过 GitHub 协同开发的项目。

## 项目结构

\`\`\`
${repoName}/
├── README.md
├── docs/           # 文档目录
├── src/            # 源代码
├── tests/          # 测试代码
├── scripts/        # 构建脚本
└── .github/        # GitHub 配置
    └── workflows/  # CI/CD 工作流
\`\`\`

## 环境搭建

请查看 docs/setup.md

## 开发流程

1. 从 main 分支创建 feature 分支
2. 开发功能并编写测试
3. 提交代码并创建 Pull Request
4. 代码审查后合并

## 参与开发

- **Coder**: 负责编码实现
- **Checker**: 负责测试验证
- **Memowriter**: 负责文档编写

---
*本项目由 GitHub 协同开发技能自动生成*
`;

  fs.writeFileSync(path.join(projectDir, 'README.md'), readme);
  console.log('✅ 项目结构初始化完成');
}

/**
 * 创建任务 Issues
 */
function createIssues(repoName, tasks) {
  tasks.forEach(task => {
    try {
      const labels = task.type === 'code' ? 'coding' : task.type === 'test' ? 'testing' : 'documentation';
      const cmd = `gh issue create --repo ${repoName} --title "[${task.type.toUpperCase()}] ${task.title}" --body "${task.description}" --label ${labels}`;
      execSync(cmd, { encoding: 'utf8' });
      console.log(`✅ Issue 创建：${task.title}`);
    } catch (error) {
      console.error(`❌ Issue 创建失败：${task.title}`, error.message);
    }
  });
}

/**
 * 分配任务给 Agent
 */
function assignAgents(repoName, tasks) {
  const agentTasks = {
    coder: tasks.filter(t => t.type === 'code'),
    checker: tasks.filter(t => t.type === 'test'),
    writer: tasks.filter(t => t.type === 'doc')
  };

  console.log('📋 任务分配结果:');
  Object.entries(agentTasks).forEach(([agent, tasks]) => {
    if (tasks.length > 0) {
      console.log(`  - ${agent}: ${tasks.length} 个任务`);
      tasks.forEach(t => {
        console.log(`    * [${t.type.toUpperCase()}] ${t.title}`);
      });
    }
  });

  return agentTasks;
}

/**
 * 生成进度报告
 */
function generateProgressReport(repoName) {
  try {
    const issues = execSync(`gh issue list --repo ${repoName} --limit 50`, { encoding: 'utf8' });
    const commits = execSync(`gh pr list --repo ${repoName} --limit 20`, { encoding: 'utf8' });
    
    const report = `
## 📊 项目进度报告 - ${repoName}

### Issues 状态
${issues}

### Pull Requests
${commits}

---
*报告生成时间：${new Date().toISOString()}*
    `;
    
    console.log(report);
    return report;
  } catch (error) {
    console.error('❌ 进度报告生成失败:', error.message);
    return null;
  }
}

/**
 * 主函数
 */
async function main() {
  const args = process.argv.slice(2);
  
  // 解析参数
  const params = {
    task: '',
    repoName: CONFIG.defaultRepoName,
    description: 'Collaborative development project',
    visibility: CONFIG.defaultVisibility,
    assignCoder: CONFIG.agents.coder,
    assignChecker: CONFIG.agents.checker,
    assignWriter: CONFIG.agents.writer
  };

  // 检查环境
  console.log('🔍 检查 GitHub 环境...');
  checkGitHubCLI();
  checkGitHubToken();

  // 创建仓库
  const repoName = createRepository(params.repoName, params.description, params.visibility);

  // 初始化项目结构
  initProjectStructure(repoName);

  // 示例任务列表
  const tasks = [
    { type: 'code', title: '实现核心功能模块', description: '开发项目核心功能' },
    { type: 'test', title: '编写单元测试', description: '为核心功能编写测试用例' },
    { type: 'doc', title: '编写操作手册', description: '编写项目使用文档' }
  ];

  // 创建 Issues
  createIssues(repoName, tasks);

  // 分配 Agent
  const assignmentResults = assignAgents(repoName, tasks);

  // 生成进度报告
  generateProgressReport(repoName);

  console.log('\n🎉 项目初始化完成!');
  console.log(`📍 仓库地址：https://github.com/${repoName}`);
}

// 运行
main().catch(error => {
  console.error('💥 错误:', error.message);
  process.exit(1);
});
