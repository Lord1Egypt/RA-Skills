#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const os = require('os');

const PROJECTS_DIR = path.join(os.homedir(), '.openclaw', 'projects');
const INDEX_FILE = path.join(PROJECTS_DIR, '_index.json');
const ARCHIVED_DIR = path.join(PROJECTS_DIR, '_archived');

// 确保目录存在
function ensureDir(dir) {
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
}

// 读取项目索引
function readIndex() {
  ensureDir(PROJECTS_DIR);
  if (!fs.existsSync(INDEX_FILE)) {
    return { projects: {}, currentProject: null };
  }
  return JSON.parse(fs.readFileSync(INDEX_FILE, 'utf8'));
}

// 写入项目索引
function writeIndex(index) {
  ensureDir(PROJECTS_DIR);
  fs.writeFileSync(INDEX_FILE, JSON.stringify(index, null, 2));
}

// 列出所有项目
function projectList() {
  const index = readIndex();
  const projects = Object.entries(index.projects).map(([name, info]) => ({
    name,
    description: info.description || '',
    updatedAt: info.updatedAt,
    status: info.status || 'active'
  }));
  
  return {
    success: true,
    currentProject: index.currentProject,
    projects: projects.filter(p => p.status === 'active'),
    archivedCount: projects.filter(p => p.status === 'archived').length
  };
}

// 创建项目
function projectCreate(name, description = '') {
  if (!name || name.trim() === '') {
    return { success: false, error: '项目名称不能为空' };
  }
  
  const index = readIndex();
  
  if (index.projects[name]) {
    return { success: false, error: `项目 "${name}" 已存在` };
  }
  
  const projectDir = path.join(PROJECTS_DIR, name);
  ensureDir(projectDir);
  ensureDir(path.join(projectDir, 'memory'));
  ensureDir(path.join(projectDir, 'context'));
  
  const now = new Date().toISOString();
  const projectConfig = {
    name,
    description,
    createdAt: now,
    updatedAt: now,
    agents: [],
    tags: [],
    status: 'active'
  };
  
  fs.writeFileSync(
    path.join(projectDir, 'project.json'),
    JSON.stringify(projectConfig, null, 2)
  );
  
  fs.writeFileSync(
    path.join(projectDir, 'memory', 'entries.json'),
    JSON.stringify({ entries: [] }, null, 2)
  );
  
  index.projects[name] = {
    description,
    createdAt: now,
    updatedAt: now,
    status: 'active'
  };
  index.currentProject = name;
  writeIndex(index);
  
  return {
    success: true,
    message: `项目 "${name}" 创建成功`,
    project: projectConfig
  };
}

// 切换项目
function projectUse(name) {
  const index = readIndex();
  
  if (!index.projects[name]) {
    return { 
      success: false, 
      error: `项目 "${name}" 不存在`,
      availableProjects: Object.keys(index.projects).filter(
        n => index.projects[n].status === 'active'
      )
    };
  }
  
  if (index.projects[name].status === 'archived') {
    return { success: false, error: `项目 "${name}" 已归档` };
  }
  
  index.currentProject = name;
  index.projects[name].updatedAt = new Date().toISOString();
  writeIndex(index);
  
  return {
    success: true,
    message: `已切换到项目 "${name}"`,
    currentProject: name
  };
}

// 获取项目信息
function projectInfo() {
  const index = readIndex();
  
  if (!index.currentProject) {
    return { 
      success: false, 
      error: '当前没有选择项目',
      availableProjects: Object.keys(index.projects).filter(
        n => index.projects[n].status === 'active'
      )
    };
  }
  
  const projectDir = path.join(PROJECTS_DIR, index.currentProject);
  const configFile = path.join(projectDir, 'project.json');
  
  if (!fs.existsSync(configFile)) {
    return { success: false, error: '项目配置文件不存在' };
  }
  
  const config = JSON.parse(fs.readFileSync(configFile, 'utf8'));
  
  // 统计记忆数量
  const entriesFile = path.join(projectDir, 'memory', 'entries.json');
  let memoryCount = 0;
  if (fs.existsSync(entriesFile)) {
    const entries = JSON.parse(fs.readFileSync(entriesFile, 'utf8'));
    memoryCount = entries.entries.length;
  }
  
  return {
    success: true,
    project: {
      ...config,
      memoryCount
    }
  };
}

// 归档项目
function projectArchive(name) {
  const index = readIndex();
  
  if (!index.projects[name]) {
    return { success: false, error: `项目 "${name}" 不存在` };
  }
  
  index.projects[name].status = 'archived';
  index.projects[name].archivedAt = new Date().toISOString();
  
  if (index.currentProject === name) {
    index.currentProject = null;
  }
  
  writeIndex(index);
  
  // 移动到归档目录
  ensureDir(ARCHIVED_DIR);
  const srcDir = path.join(PROJECTS_DIR, name);
  const destDir = path.join(ARCHIVED_DIR, name);
  
  if (fs.existsSync(srcDir)) {
    fs.renameSync(srcDir, destDir);
  }
  
  return {
    success: true,
    message: `项目 "${name}" 已归档`
  };
}

// 删除项目
function projectDelete(name, confirm) {
  if (!confirm) {
    return { 
      success: false, 
      error: '删除操作需要确认，请设置 confirm: true' 
    };
  }
  
  const index = readIndex();
  
  if (!index.projects[name]) {
    return { success: false, error: `项目 "${name}" 不存在` };
  }
  
  // 删除目录
  const projectDir = path.join(PROJECTS_DIR, name);
  const archivedDir = path.join(ARCHIVED_DIR, name);
  
  if (fs.existsSync(projectDir)) {
    fs.rmSync(projectDir, { recursive: true });
  }
  if (fs.existsSync(archivedDir)) {
    fs.rmSync(archivedDir, { recursive: true });
  }
  
  delete index.projects[name];
  
  if (index.currentProject === name) {
    index.currentProject = null;
  }
  
  writeIndex(index);
  
  return {
    success: true,
    message: `项目 "${name}" 已永久删除`
  };
}

// 保存记忆
function memorySave(title, content, tags = []) {
  const index = readIndex();
  
  if (!index.currentProject) {
    return { 
      success: false, 
      error: '请先选择一个项目',
      hint: '使用 /project use <项目名> 或 /project create <项目名>'
    };
  }
  
  const projectDir = path.join(PROJECTS_DIR, index.currentProject);
  const entriesFile = path.join(projectDir, 'memory', 'entries.json');
  
  ensureDir(path.join(projectDir, 'memory'));
  
  let entries = { entries: [] };
  if (fs.existsSync(entriesFile)) {
    entries = JSON.parse(fs.readFileSync(entriesFile, 'utf8'));
  }
  
  const entryId = `mem_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  const now = new Date().toISOString();
  
  const entry = {
    id: entryId,
    title,
    tags,
    createdAt: now,
    updatedAt: now,
    agent: process.env.OPENCLAW_AGENT_ID || 'unknown'
  };
  
  entries.entries.unshift(entry);
  fs.writeFileSync(entriesFile, JSON.stringify(entries, null, 2));
  
  // 保存详细内容
  const contentFile = path.join(projectDir, 'memory', `${entryId}.md`);
  fs.writeFileSync(contentFile, `# ${title}\n\n${content}\n\n---\n创建时间: ${now}\n标签: ${tags.join(', ')}`);
  
  // 更新项目时间
  index.projects[index.currentProject].updatedAt = now;
  writeIndex(index);
  
  return {
    success: true,
    message: `记忆已保存到项目 "${index.currentProject}"`,
    entryId,
    title
  };
}

// 搜索记忆
function memorySearch(query, limit = 10) {
  const index = readIndex();
  
  if (!index.currentProject) {
    return { 
      success: false, 
      error: '请先选择一个项目' 
    };
  }
  
  const projectDir = path.join(PROJECTS_DIR, index.currentProject);
  const entriesFile = path.join(projectDir, 'memory', 'entries.json');
  
  if (!fs.existsSync(entriesFile)) {
    return { success: true, results: [], message: '暂无记忆' };
  }
  
  const entries = JSON.parse(fs.readFileSync(entriesFile, 'utf8'));
  const queryLower = query.toLowerCase();
  
  const results = [];
  
  for (const entry of entries.entries) {
    // 搜索标题和标签
    const titleMatch = entry.title.toLowerCase().includes(queryLower);
    const tagMatch = entry.tags.some(t => t.toLowerCase().includes(queryLower));
    
    // 搜索内容
    const contentFile = path.join(projectDir, 'memory', `${entry.id}.md`);
    let contentMatch = false;
    let snippet = '';
    
    if (fs.existsSync(contentFile)) {
      const content = fs.readFileSync(contentFile, 'utf8');
      contentMatch = content.toLowerCase().includes(queryLower);
      
      if (titleMatch || tagMatch || contentMatch) {
        // 提取匹配片段
        const idx = content.toLowerCase().indexOf(queryLower);
        if (idx !== -1) {
          const start = Math.max(0, idx - 50);
          const end = Math.min(content.length, idx + query.length + 50);
          snippet = '...' + content.substring(start, end) + '...';
        }
      }
    }
    
    if (titleMatch || tagMatch || contentMatch) {
      results.push({
        ...entry,
        snippet,
        relevance: (titleMatch ? 3 : 0) + (tagMatch ? 2 : 0) + (contentMatch ? 1 : 0)
      });
    }
    
    if (results.length >= limit) break;
  }
  
  // 按相关度排序
  results.sort((a, b) => b.relevance - a.relevance);
  
  return {
    success: true,
    project: index.currentProject,
    query,
    results: results.slice(0, limit)
  };
}

// 列出记忆
function memoryList(limit = 20, offset = 0) {
  const index = readIndex();
  
  if (!index.currentProject) {
    return { 
      success: false, 
      error: '请先选择一个项目' 
    };
  }
  
  const projectDir = path.join(PROJECTS_DIR, index.currentProject);
  const entriesFile = path.join(projectDir, 'memory', 'entries.json');
  
  if (!fs.existsSync(entriesFile)) {
    return { success: true, entries: [], total: 0 };
  }
  
  const data = JSON.parse(fs.readFileSync(entriesFile, 'utf8'));
  const total = data.entries.length;
  const entries = data.entries.slice(offset, offset + limit);
  
  return {
    success: true,
    project: index.currentProject,
    entries,
    total,
    offset,
    limit,
    hasMore: offset + limit < total
  };
}

// 主函数 - 处理命令行参数
function main() {
  const args = process.argv.slice(2);
  const command = args[0];
  
  let result;
  
  switch (command) {
    case 'project_list':
      result = projectList();
      break;
    case 'project_create':
      result = projectCreate(args[1], args[2]);
      break;
    case 'project_use':
      result = projectUse(args[1]);
      break;
    case 'project_info':
      result = projectInfo();
      break;
    case 'project_archive':
      result = projectArchive(args[1]);
      break;
    case 'project_delete':
      result = projectDelete(args[1], args[2] === 'true');
      break;
    case 'memory_save':
      result = memorySave(args[1], args[2], args[3] ? JSON.parse(args[3]) : []);
      break;
    case 'memory_search':
      result = memorySearch(args[1], parseInt(args[2]) || 10);
      break;
    case 'memory_list':
      result = memoryList(parseInt(args[1]) || 20, parseInt(args[2]) || 0);
      break;
    default:
      result = { error: `未知命令: ${command}` };
  }
  
  console.log(JSON.stringify(result, null, 2));
}

main();
