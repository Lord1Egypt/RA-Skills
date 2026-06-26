#!/usr/bin/env node

/**
 * 进度报告脚本
 * 生成项目进度报告
 */

const { execSync } = require('child_process');

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

// 导出
module.exports = { generateProgressReport };
