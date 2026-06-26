#!/usr/bin/env node

/**
 * 项目状态更新工具
 * 用于更新 projects_status.json 和生成 PROJECT_STATUS.md
 */

const fs = require('fs');
const path = require('path');

const PROJECTS_JSON_PATH = path.join(__dirname, '..', 'projects_status.json');
const PROJECTS_MD_PATH = path.join(__dirname, '..', 'PROJECT_STATUS.md');

// 读取当前项目数据
function readProjectsData() {
  try {
    const data = fs.readFileSync(PROJECTS_JSON_PATH, 'utf8');
    return JSON.parse(data);
  } catch (error) {
    console.error('❌ 读取项目数据失败:', error.message);
    process.exit(1);
  }
}

// 写入项目数据
function writeProjectsData(data) {
  try {
    // 更新最后更新时间
    data.last_updated = new Date().toISOString();
    data.updated_by = process.env.AGENT_ID || 'unknown-agent';
    
    fs.writeFileSync(PROJECTS_JSON_PATH, JSON.stringify(data, null, 2), 'utf8');
    console.log('✅ 项目数据已更新');
    
    // 生成Markdown视图
    generateMarkdownView(data);
  } catch (error) {
    console.error('❌ 写入项目数据失败:', error.message);
    process.exit(1);
  }
}

// 生成Markdown视图
function generateMarkdownView(data) {
  const now = new Date();
  const localTime = new Date(now.getTime() + 8 * 60 * 60 * 1000); // UTC+8
  const timeStr = localTime.toISOString().replace('T', ' ').substring(0, 16).replace('-', '年').replace('-', '月') + '日';
  
  let mdContent = `# 📋 项目状态共享系统

**最后更新**: ${timeStr} (北京时间)  
**更新者**: ${data.updated_by}  
**数据文件**: \`projects_status.json\`

---

## 🚀 当前活跃项目

| 项目 | 状态 | 优先级 | 当前任务 | 涉及Agent | 最后更新 |
|------|------|--------|----------|-----------|----------|`;

  // 添加项目行
  data.projects.forEach(project => {
    const statusIcon = project.status === 'completed' ? '✅' : 
                      project.status === 'in_progress' ? '🔄' : '⏸️';
    const priorityText = project.priority === 'high' ? '高' : 
                        project.priority === 'medium' ? '中' : '低';
    
    const lastUpdated = new Date(project.updated_at);
    const lastUpdatedStr = lastUpdated.toISOString().substring(11, 16); // HH:mm
    
    mdContent += `
| [${project.name}](#${project.id}) | ${statusIcon} ${getStatusText(project.status)} | ${priorityText} | ${truncateText(project.current_task, 30)} | ${project.agents_involved.join(', ')} | ${lastUpdatedStr} |`;
  });

  mdContent += `

---

## 📊 项目详情
`;

  // 添加项目详情
  data.projects.forEach(project => {
    const statusIcon = project.status === 'completed' ? '✅' : 
                      project.status === 'in_progress' ? '🔄' : '⏸️';
    const priorityText = project.priority === 'high' ? '高' : 
                        project.priority === 'medium' ? '中' : '低';
    
    const createdTime = new Date(project.created_at).toISOString().substring(0, 16).replace('T', ' ');
    const updatedTime = new Date(project.updated_at).toISOString().substring(0, 16).replace('T', ' ');
    
    mdContent += `
### ${getPriorityIcon(project.priority)} ${project.name} (\`${project.id}\`)

**状态**: ${statusIcon} ${getStatusText(project.status)}  
**优先级**: ${priorityText}  
**创建时间**: ${createdTime}  
**最后更新**: ${updatedTime}

**描述**: ${project.description}

**当前任务**: ${project.current_task}

**涉及Agent**: ${project.agents_involved.join(', ')}

#### 📝 历史记录

| 时间 | Agent | 操作 | 描述 |
|------|-------|------|------|`;

    project.history.forEach(record => {
      const timeStr = new Date(record.timestamp).toISOString().substring(11, 16);
      mdContent += `
| ${timeStr} | ${record.agent} | ${record.action} | ${record.description} |`;
    });

    if (project.errors && project.errors.length > 0) {
      mdContent += `

#### ⚠️ 遇到的问题

| 时间 | 错误 | 详情 | 解决方案 |
|------|------|------|----------|`;

      project.errors.forEach(error => {
        const timeStr = new Date(error.timestamp).toISOString().substring(11, 16);
        mdContent += `
| ${timeStr} | ${error.error} | ${error.details} | ${error.resolution} |`;
      });
    }

    mdContent += `

---`;
  });

  // 添加使用说明
  mdContent += `

## 📌 如何使用

### 查看项目状态
\`\`\`bash
# 查看所有项目概览
cat PROJECT_STATUS.md

# 查看详细数据
cat projects_status.json

# 搜索特定项目
grep -i "关键词" PROJECT_STATUS.md
\`\`\`

### 更新项目状态（主agent）
1. 使用本工具：\`node scripts/update_project_status.js <命令> <参数>\`
2. 直接编辑 \`projects_status.json\`，然后运行本工具重新生成Markdown

### 可用命令
- \`node scripts/update_project_status.js add <项目ID> "<项目名>" "<描述>" [优先级]\`
- \`node scripts/update_project_status.js update <项目ID> <状态> "<当前任务>"\`
- \`node scripts/update_project_status.js history <项目ID> "<操作>" "<描述>"\`
- \`node scripts/update_project_status.js error <项目ID> "<错误>" "<详情>" "<解决方案>"\`
- \`node scripts/update_project_status.js list\`
- \`node scripts/update_project_status.js view <项目ID>\`

---

*本文件由项目共享系统自动生成*  
*最后生成时间: ${new Date().toISOString()}*`;

  try {
    fs.writeFileSync(PROJECTS_MD_PATH, mdContent, 'utf8');
    console.log('✅ Markdown视图已生成');
  } catch (error) {
    console.error('❌ 生成Markdown视图失败:', error.message);
  }
}

// 辅助函数
function getStatusText(status) {
  const statusMap = {
    'not_started': '未开始',
    'in_progress': '进行中',
    'completed': '已完成',
    'paused': '已暂停',
    'blocked': '已阻塞'
  };
  return statusMap[status] || status;
}

function getPriorityIcon(priority) {
  const iconMap = {
    'high': '🔴',
    'medium': '🟡',
    'low': '🟢'
  };
  return iconMap[priority] || '⚪';
}

function truncateText(text, maxLength) {
  if (text.length <= maxLength) return text;
  return text.substring(0, maxLength) + '...';
}

// 命令处理
function handleAddCommand(args) {
  const data = readProjectsData();
  const [id, name, description, priority = 'medium'] = args;
  
  // 检查是否已存在
  const existingProject = data.projects.find(p => p.id === id);
  if (existingProject) {
    console.log('❌ 项目ID已存在:', id);
    return;
  }
  
  const now = new Date().toISOString();
  const newProject = {
    id,
    name,
    description,
    status: 'not_started',
    priority,
    current_task: '项目已创建，等待开始',
    agents_involved: [data.updated_by || 'agent:main:main'],
    created_at: now,
    updated_at: now,
    history: [{
      timestamp: now,
      agent: data.updated_by || 'agent:main:main',
      action: '项目创建',
      description: `项目"${name}"已创建`
    }],
    errors: []
  };
  
  data.projects.push(newProject);
  writeProjectsData(data);
  console.log(`✅ 项目"${name}"已创建 (ID: ${id})`);
}

function handleUpdateCommand(args) {
  const data = readProjectsData();
  const [id, status, currentTask] = args;
  
  const project = data.projects.find(p => p.id === id);
  if (!project) {
    console.log('❌ 未找到项目:', id);
    return;
  }
  
  project.status = status;
  project.current_task = currentTask;
  project.updated_at = new Date().toISOString();
  
  // 添加历史记录
  project.history.push({
    timestamp: project.updated_at,
    agent: data.updated_by || 'agent:main:main',
    action: '状态更新',
    description: `状态变更为: ${getStatusText(status)}, 任务: ${currentTask}`
  });
  
  writeProjectsData(data);
  console.log(`✅ 项目"${project.name}"已更新`);
}

function handleHistoryCommand(args) {
  const data = readProjectsData();
  const [id, action, description] = args;
  
  const project = data.projects.find(p => p.id === id);
  if (!project) {
    console.log('❌ 未找到项目:', id);
    return;
  }
  
  const now = new Date().toISOString();
  project.history.push({
    timestamp: now,
    agent: data.updated_by || 'agent:main:main',
    action,
    description
  });
  
  project.updated_at = now;
  writeProjectsData(data);
  console.log(`✅ 已为项目"${project.name}"添加历史记录`);
}

function handleErrorCommand(args) {
  const data = readProjectsData();
  const [id, error, details, resolution] = args;
  
  const project = data.projects.find(p => p.id === id);
  if (!project) {
    console.log('❌ 未找到项目:', id);
    return;
  }
  
  const now = new Date().toISOString();
  project.errors.push({
    timestamp: now,
    error,
    details,
    resolution
  });
  
  // 同时添加历史记录
  project.history.push({
    timestamp: now,
    agent: data.updated_by || 'agent:main:main',
    action: '记录错误',
    description: `记录错误: ${error}`
  });
  
  project.updated_at = now;
  writeProjectsData(data);
  console.log(`✅ 已为项目"${project.name}"记录错误`);
}

function handleListCommand() {
  const data = readProjectsData();
  console.log('\n📋 项目列表:');
  console.log('='.repeat(60));
  
  data.projects.forEach((project, index) => {
    const statusIcon = project.status === 'completed' ? '✅' : 
                      project.status === 'in_progress' ? '🔄' : '⏸️';
    console.log(`${index + 1}. ${statusIcon} ${project.name} (${project.id})`);
    console.log(`   状态: ${getStatusText(project.status)} | 优先级: ${project.priority}`);
    console.log(`   当前任务: ${project.current_task}`);
    console.log(`   最后更新: ${new Date(project.updated_at).toISOString().substring(0, 16)}`);
    console.log();
  });
}

function handleViewCommand(args) {
  const data = readProjectsData();
  const [id] = args;
  
  const project = data.projects.find(p => p.id === id);
  if (!project) {
    console.log('❌ 未找到项目:', id);
    return;
  }
  
  console.log(`\n📊 项目详情: ${project.name} (${project.id})`);
  console.log('='.repeat(60));
  console.log(`描述: ${project.description}`);
  console.log(`状态: ${getStatusText(project.status)} (${project.priority} 优先级)`);
  console.log(`当前任务: ${project.current_task}`);
  console.log(`涉及Agent: ${project.agents_involved.join(', ')}`);
  console.log(`创建时间: ${project.created_at}`);
  console.log(`最后更新: ${project.updated_at}`);
  
  console.log(`\n📝 历史记录 (${project.history.length} 条):`);
  project.history.forEach((record, index) => {
    const timeStr = new Date(record.timestamp).toISOString().substring(11, 16);
    console.log(`  ${index + 1}. [${timeStr}] ${record.agent}: ${record.action} - ${record.description}`);
  });
  
  if (project.errors && project.errors.length > 0) {
    console.log(`\n⚠️  遇到的问题 (${project.errors.length} 个):`);
    project.errors.forEach((error, index) => {
      const timeStr = new Date(error.timestamp).toISOString().substring(11, 16);
      console.log(`  ${index + 1}. [${timeStr}] ${error.error}`);
      console.log(`     详情: ${error.details}`);
      console.log(`     解决方案: ${error.resolution}`);
    });
  }
}

// 主函数
function main() {
  const command = process.argv[2];
  const args = process.argv.slice(3);
  
  switch (command) {
    case 'add':
      handleAddCommand(args);
      break;
    case 'update':
      handleUpdateCommand(args);
      break;
    case 'history':
      handleHistoryCommand(args);
      break;
    case 'error':
      handleErrorCommand(args);
      break;
    case 'list':
      handleListCommand();
      break;
    case 'view':
      handleViewCommand(args);
      break;
    case 'help':
    case '--help':
    case '-h':
      console.log(`
📋 项目状态管理工具

用法: node scripts/update_project_status.js <命令> <参数>

命令:
  add <ID> "<名称>" "<描述>" [优先级]  添加新项目
  update <ID> <状态> "<任务>"          更新项目状态和任务
  history <ID> "<操作>" "<描述>"        添加历史记录
  error <ID> "<错误>" "<详情>" "<解决方案>" 记录错误
  list                                列出所有项目
  view <ID>                           查看项目详情
  help                                显示此帮助

状态值: not_started, in_progress, completed, paused, blocked
优先级: high, medium, low (默认: medium)

示例:
  node scripts/update_project_status.js add feature_123 "新功能" "实现XXX功能" high
  node scripts/update_project_status.js update feature_123 in_progress "正在开发核心逻辑"
  node scripts/update_project_status.js history feature_123 "设计完成" "API设计已完成"
      `);
      break;
    default:
      // 如果没有命令，只重新生成Markdown
      const data = readProjectsData();
      generateMarkdownView(data);
      console.log('✅ Markdown视图已重新生成');
  }
}

// 执行主函数
if (require.main === module) {
  main();
}

// 导出函数供其他模块使用
module.exports = {
  readProjectsData,
  writeProjectsData,
  generateMarkdownView
};