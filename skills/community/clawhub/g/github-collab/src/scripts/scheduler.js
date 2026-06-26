#!/usr/bin/env node

/**
 * 定时任务调度器
 * 支持每日进度报告、项目自动处理
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const CONFIG = {
  dataDir: path.join(__dirname, '..', 'data'),
  scheduleFile: path.join(__dirname, '..', 'data', 'schedule.json'),
  projectsFile: path.join(__dirname, '..', 'data', 'projects.json')
};

function initDataDir() {
  if (!fs.existsSync(CONFIG.dataDir)) {
    fs.mkdirSync(CONFIG.dataDir, { recursive: true });
  }
}

function readJSON(file) {
  try {
    if (fs.existsSync(file)) {
      return JSON.parse(fs.readFileSync(file, 'utf8'));
    }
  } catch (error) {
    console.error(`读取文件失败：${file}`, error.message);
  }
  return null;
}

function writeJSON(file, data) {
  try {
    fs.writeFileSync(file, JSON.stringify(data, null, 2), 'utf8');
  } catch (error) {
    console.error(`写入文件失败：${file}`, error.message);
  }
}

function getCurrentUser() {
  try {
    const user = JSON.parse(execSync('gh api user', { encoding: 'utf8' }));
    return user.login;
  } catch (error) {
    return 'wljmmx';
  }
}

function dailyProgressReport() {
  console.log('📊 生成每日进度报告...');
  const projects = readJSON(CONFIG.projectsFile) || {};
  const report = [];
  
  Object.entries(projects).forEach(([name, project]) => {
    const fullRepoName = `${getCurrentUser()}/${name}`;
    try {
      const issues = execSync(`gh issue list --repo ${fullRepoName} --limit 10`, { encoding: 'utf8' });
      const commits = execSync(`gh pr list --repo ${fullRepoName} --limit 5`, { encoding: 'utf8' });
      
      report.push({
        repo: name,
        issues: issues,
        prs: commits,
        lastUpdate: project.lastUpdate || new Date().toISOString()
      });
    } catch (error) {
      console.error(`❌ 获取项目 ${name} 进度失败`, error.message);
    }
  });
  
  const summary = `
## 📊 每日进度报告 - ${new Date().toLocaleDateString()}

${report.map(r => `
### ${r.repo}
**Issues:**
${r.issues}
**PRs:**
${r.prs}
`).join('\n')}

---
*报告生成时间：${new Date().toISOString()}*
`;
  
  console.log(summary);
  return summary;
}

function setSchedule(type, time) {
  initDataDir();
  const schedule = readJSON(CONFIG.scheduleFile) || {};
  
  schedule[type] = {
    enabled: true,
    time: time || '09:00',
    lastRun: null,
    createdAt: new Date().toISOString()
  };
  
  writeJSON(CONFIG.scheduleFile, schedule);
  console.log(`✅ 定时任务已设置：${type} - ${time || '09:00'}`);
}

function clearSchedule(type) {
  initDataDir();
  const schedule = readJSON(CONFIG.scheduleFile) || {};
  
  if (schedule[type]) {
    delete schedule[type];
    writeJSON(CONFIG.scheduleFile, schedule);
    console.log(`✅ 定时任务已取消：${type}`);
  } else {
    console.log(`⚠️ 定时任务 ${type} 不存在`);
  }
}

function showSchedule() {
  const schedule = readJSON(CONFIG.scheduleFile) || {};
  
  console.log('📅 定时任务列表:');
  if (Object.keys(schedule).length === 0) {
    console.log('  无定时任务');
  } else {
    Object.entries(schedule).forEach(([type, config]) => {
      console.log(`  - ${type}: ${config.time} (启用：${config.enabled})`);
      console.log(`    上次运行：${config.lastRun || '从未'}`);
    });
  }
}

function runScheduledTasks() {
  initDataDir();
  const schedule = readJSON(CONFIG.scheduleFile) || {};
  const now = new Date();
  const currentTime = `${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}`;
  
  console.log(`🕐 当前时间：${currentTime}`);
  
  Object.entries(schedule).forEach(([type, config]) => {
    if (!config.enabled) return;
    
    if (config.time === currentTime) {
      console.log(`⏰ 执行定时任务：${type}`);
      
      switch (type) {
        case 'daily-report':
          dailyProgressReport();
          break;
      }
      
      config.lastRun = new Date().toISOString();
      writeJSON(CONFIG.scheduleFile, schedule);
    }
  });
}

function main() {
  const args = process.argv.slice(2);
  const command = args[0];
  
  initDataDir();
  
  switch (command) {
    case 'set':
      setSchedule(args[1], args[2]);
      break;
      
    case 'clear':
      clearSchedule(args[1]);
      break;
      
    case 'show':
      showSchedule();
      break;
      
    case 'run':
      runScheduledTasks();
      break;
      
    case 'report':
    default:
      dailyProgressReport();
      break;
  }
}

main();
