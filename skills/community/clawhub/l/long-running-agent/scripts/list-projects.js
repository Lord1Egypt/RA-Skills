#!/usr/bin/env node
/**
 * list-projects.js - 列出所有项目
 * 
 * 用法：
 *   node list-projects.js [工作区路径]
 */

const fs = require('fs');
const path = require('path');

function listProjects(workspacePath) {
  const tasksDir = path.join(workspacePath, 'tasks');
  
  if (!fs.existsSync(tasksDir)) {
    return [];
  }
  
  const projects = [];
  const dirs = fs.readdirSync(tasksDir, { withFileTypes: true });
  
  for (const dir of dirs) {
    if (!dir.isDirectory()) continue;
    
    const projectPath = path.join(tasksDir, dir.name);
    const projectMd = path.join(projectPath, 'PROJECT.md');
    const changelogMd = path.join(projectPath, 'CHANGELOG.md');
    
    const project = {
      name: dir.name,
      path: projectPath,
      hasProject: fs.existsSync(projectMd),
      hasChangelog: fs.existsSync(changelogMd)
    };
    
    // 读取进度
    if (project.hasChangelog) {
      const content = fs.readFileSync(changelogMd, 'utf-8');
      const progressMatch = content.match(/\*\*进度\*\*:\s*(\d+)\/(\d+)\s*任务完成/);
      if (progressMatch) {
        project.completed = parseInt(progressMatch[1]);
        project.total = parseInt(progressMatch[2]);
        project.percent = Math.round((project.completed / project.total) * 100);
      }
      
      const statusMatch = content.match(/## 当前状态:\s*(.+)/);
      if (statusMatch) {
        project.status = statusMatch[1].trim();
      }
    }
    
    projects.push(project);
  }
  
  return projects;
}

// CLI 入口
if (require.main === module) {
  const workspacePath = process.argv[2] || process.cwd();
  
  const projects = listProjects(workspacePath);
  
  if (projects.length === 0) {
    console.log('📭 没有找到项目');
    process.exit(0);
  }
  
  console.log(`📋 项目列表 (共 ${projects.length} 个)\n`);
  console.log('名称                    | 状态           | 进度    | 文件');
  console.log('-'.repeat(60));
  
  for (const p of projects) {
    const name = p.name.padEnd(23);
    const status = (p.status || '-').substring(0, 14).padEnd(15);
    const progress = p.percent ? `${p.percent}%`.padEnd(7) : '-'.padEnd(7);
    const files = `${p.hasProject ? '📄' : '❌'} ${p.hasChangelog ? '📝' : '❌'}`;
    
    console.log(`${name} | ${status} | ${progress} | ${files}`);
  }
}

module.exports = { listProjects };
