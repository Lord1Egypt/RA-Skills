#!/usr/bin/env node
/**
 * init-project.js - 初始化新项目
 * 
 * 用法：
 *   node init-project.js <项目名> [选项]
 * 
 * 选项：
 *   --desc "描述"    项目描述
 *   --path "路径"    项目路径（默认 workspace/tasks/）
 */

const fs = require('fs');
const path = require('path');

// 项目模板
const PROJECT_TEMPLATE = `# PROJECT.md - {PROJECT_NAME}

> 创建时间: {DATE}
> 最后更新: {DATE}

## 项目概述

**一句话描述**: {DESCRIPTION}

**预期时间**: 待评估

---

## 交付物

- [ ] 待定义

---

## 成功标准

项目完成的定义：

1. **功能完整**: 待定义
2. **质量标准**: 测试通过

**可量化指标**:
- 测试: 全部通过

---

## 定向协议

**每个会话开始时，执行以下步骤**：

\`\`\`
1. 读取 CHANGELOG.md 的"当前状态"和"下一步"
2. 确认没有回归
3. 从优先列表中选择任务
4. 开始工作
\`\`\`

**不要做的事**：
- ❌ 不要跳过定向协议
- ❌ 不要重新尝试已记录为"失败"的方法

---

## 任务分解

### Phase 1: 初始化

- [ ] 定义详细需求
- [ ] 创建测试用例

---

## 版本历史

- {DATE}: 项目创建
`;

const CHANGELOG_TEMPLATE = `# CHANGELOG.md - {PROJECT_NAME} 开发进度

> 创建时间: {DATE}
> 最后更新: {DATE}

---

## 当前状态: 项目初始化

**进度**: 0/N 任务完成，0%

**当前里程碑**: Phase 1

**阻塞问题**: 无

**下一步行动**: 
1. 定义详细需求
2. 创建第一个测试

**Ralph Loop 状态**:
\`\`\`
迭代: 1/20
成功标准: 待定义
\`\`\`

---

## 测试状态

| 模块 | 通过 | 失败 | 跳过 | 最后运行 |
|------|------|------|------|----------|
| - | - | - | - | 未运行 |

**快速测试**: ⏳ 待运行

---

## 完成的任务

(尚无完成任务)

---

## 进行中的任务

### 项目初始化

**当前进度**: 项目文件创建中

**已完成**:
- [x] 创建 PROJECT.md
- [x] 创建 CHANGELOG.md

**待完成**:
- [ ] 定义需求
- [ ] 创建测试

**阻塞**: 无

---

## 失败的方法

> ⚠️ 尚无失败方法记录

---

## 会话日志

### Session 1 - {DATE}

**时长**: 初始化

**完成**:
- 创建项目框架

**下次继续**:
- 定义详细需求

---

## 版本历史

- {DATE}: 项目初始化
`;

function initProject(projectName, options = {}) {
  const date = new Date().toISOString().split('T')[0];
  const projectPath = options.path || path.join(process.cwd(), 'tasks', projectName);
  
  // 创建目录
  if (!fs.existsSync(projectPath)) {
    fs.mkdirSync(projectPath, { recursive: true });
  }
  
  // 生成 PROJECT.md
  const projectMd = PROJECT_TEMPLATE
    .replace(/{PROJECT_NAME}/g, projectName)
    .replace(/{DATE}/g, date)
    .replace(/{DESCRIPTION}/g, options.desc || '待定义');
  
  fs.writeFileSync(path.join(projectPath, 'PROJECT.md'), projectMd);
  
  // 生成 CHANGELOG.md
  const changelogMd = CHANGELOG_TEMPLATE
    .replace(/{PROJECT_NAME}/g, projectName)
    .replace(/{DATE}/g, date);
  
  fs.writeFileSync(path.join(projectPath, 'CHANGELOG.md'), changelogMd);
  
  // 创建 tests 目录
  const testsDir = path.join(projectPath, 'tests');
  if (!fs.existsSync(testsDir)) {
    fs.mkdirSync(testsDir);
  }
  
  return {
    path: projectPath,
    files: ['PROJECT.md', 'CHANGELOG.md', 'tests/']
  };
}

// CLI 入口
if (require.main === module) {
  const args = process.argv.slice(2);
  let projectName = null;
  const options = {};
  
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--desc') {
      options.desc = args[++i];
    } else if (args[i] === '--path') {
      options.path = args[++i];
    } else if (!args[i].startsWith('--')) {
      projectName = args[i];
    }
  }
  
  if (!projectName) {
    console.error('用法: node init-project.js <项目名> [--desc "描述"] [--path "路径"]');
    process.exit(1);
  }
  
  try {
    const result = initProject(projectName, options);
    console.log(`✅ 项目已创建: ${projectName}`);
    console.log(`📁 位置: ${result.path}`);
    console.log(`📄 文件: ${result.files.join(', ')}`);
  } catch (error) {
    console.error(`❌ 创建失败: ${error.message}`);
    process.exit(1);
  }
}

module.exports = { initProject };
