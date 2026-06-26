// Gateway 重启保护钩子（JavaScript 版本）
const fs = require('fs');
const path = require('path');

const BACKUP_DIR = path.join(__dirname, '..', '..', 'backups');
const MAX_BACKUP_AGE_DAYS = 7;

// 配置检查清单
const configChecklist = [
  {
    name: 'Embedding 配置',
    path: path.join(__dirname, '..', '..', 'openclaw.json'),
    key: 'embedding',
    required: true,
    backup: true
  },
  {
    name: '钩子配置',
    path: path.join(__dirname, '..', 'hooks'),
    required: true,
    backup: true
  },
  {
    name: '技能配置',
    path: path.join(__dirname, '..', 'skills'),
    required: true,
    backup: false
  },
  {
    name: '记忆文件',
    path: path.join(__dirname, '..', 'memory'),
    required: true,
    backup: true
  },
  {
    name: '向量数据库',
    path: path.join(__dirname, '..', 'chroma_db'),
    required: false,
    backup: true
  }
];

// 备份配置
function backupConfig(config) {
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  const backupName = `${path.basename(config.path)}-${timestamp}.bak`;
  const backupPath = path.join(BACKUP_DIR, backupName);
  
  if (!fs.existsSync(BACKUP_DIR)) {
    fs.mkdirSync(BACKUP_DIR, { recursive: true });
  }
  
  if (fs.existsSync(config.path)) {
    if (fs.statSync(config.path).isDirectory()) {
      // 目录备份
      const { execSync } = require('child_process');
      execSync(`robocopy "${config.path}" "${backupPath}" /E /COPYALL /R:0`);
    } else {
      // 文件备份
      fs.copyFileSync(config.path, backupPath);
    }
    return backupPath;
  }
  
  return null;
}

// 检查配置
function checkConfig(config) {
  if (!fs.existsSync(config.path)) {
    return {
      name: config.name,
      status: '❌ 不存在',
      required: config.required,
      backup: null
    };
  }
  
  // 检查 Embedding 配置
  if (config.key) {
    const content = JSON.parse(fs.readFileSync(config.path, 'utf-8'));
    const hasKey = content[config.key] !== undefined;
    return {
      name: config.name,
      status: hasKey ? '✅ 已配置' : '⚠️ 未配置',
      required: config.required,
      backup: config.backup ? '待备份' : '不备份'
    };
  }
  
  return {
    name: config.name,
    status: '✅ 存在',
    required: config.required,
    backup: config.backup ? '待备份' : '不备份'
  };
}

// 清理旧备份
function cleanupOldBackups() {
  if (!fs.existsSync(BACKUP_DIR)) return;
  
  const now = Date.now();
  const maxAge = MAX_BACKUP_AGE_DAYS * 24 * 60 * 60 * 1000;
  
  const files = fs.readdirSync(BACKUP_DIR);
  for (const file of files) {
    const filePath = path.join(BACKUP_DIR, file);
    const stat = fs.statSync(filePath);
    if (now - stat.mtimeMs > maxAge) {
      fs.unlinkSync(filePath);
      console.log(`[gateway-restart-protection] Cleaned up old backup: ${file}`);
    }
  }
}

const gatewayRestartProtection = async (event) => {
  // 只处理 Gateway 重启前事件
  if (event.type !== 'gateway' || event.action !== 'restart:before') {
    return;
  }

  console.log('[gateway-restart-protection] Gateway restart requested');
  console.log('[gateway-restart-protection] Blocking automatic restart');

  // 阻止自动重启
  event.preventDefault?.();
  event.blocked = true;

  try {
    // 1. 清理旧备份
    cleanupOldBackups();

    // 2. 检查配置
    const checkResults = configChecklist.map(checkConfig);
    
    // 3. 备份配置
    const backupResults = [];
    for (const config of configChecklist) {
      if (config.backup) {
        const backupPath = backupConfig(config);
        backupResults.push({
          name: config.name,
          status: backupPath ? `✅ 已备份` : '⚠️ 备份失败',
          backup: backupPath
        });
      }
    }

    // 4. 生成保存明细报告
    const timestamp = new Date().toLocaleString('zh-CN');
    const report = `
🛡️ **Gateway 重启保护报告**

**时间：** ${timestamp}
**原因：** ${event.reason || '用户请求重启'}

## 📋 配置检查

${checkResults.map(r => `- ${r.name}: ${r.status}`).join('\n')}

## 💾 备份明细

${backupResults.map(r => `- ${r.name}: ${r.status}${r.backup ? ` (${r.backup})` : ''}`).join('\n')}

## ✅ 安全重启结论

**可以安全重启：** ${checkResults.every(r => !r.required || r.status.includes('✅')) ? '✅ 是' : '❌ 否'}

## ⏳ 等待用户指令

**🚫 禁止擅自重启 Gateway**

请用户确认后执行：
\`\`\`bash
openclaw gateway restart --confirmed
\`\`\`
`.trim();

    // 5. 发送报告给用户
    if (event.messages) {
      event.messages.push(report);
    }

    // 6. 记录日志
    const logFile = path.join(BACKUP_DIR, `restart-report-${timestamp.replace(/[:/]/g, '-')}.md`);
    fs.writeFileSync(logFile, report, 'utf-8');

    console.log('[gateway-restart-protection] Restart blocked, waiting for user confirmation');
    console.log(`[gateway-restart-protection] Report saved to: ${logFile}`);

  } catch (error) {
    console.error(`[gateway-restart-protection] Error: ${error.message}`);
    if (event.messages) {
      event.messages.push(`⚠️ **保护钩子执行失败：** ${error.message}`);
      event.messages.push(`🚫 **Gateway 重启已阻止**`);
    }
  }
};

module.exports = gatewayRestartProtection;
