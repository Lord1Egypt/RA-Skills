/**
 * 热点雷达 - 话题监控配置管理
 */

const fs = require('fs');
const path = require('path');

const CONFIG = {
  configDir: path.join(__dirname, '../config'),
};

// 确保配置目录存在
function ensureConfigDir() {
  if (!fs.existsSync(CONFIG.configDir)) {
    fs.mkdirSync(CONFIG.configDir, { recursive: true });
  }
}

// 默认监控配置
const DEFAULT_MONITOR = {
  keywords: [],
  enabled: true,
  notifyOnNew: true,
  notifyOnTop10: true
};

// 读取监控配置
function loadConfig() {
  ensureConfigDir();
  const configPath = path.join(CONFIG.configDir, 'monitor.json');

  try {
    if (fs.existsSync(configPath)) {
      return JSON.parse(fs.readFileSync(configPath, 'utf-8'));
    }
  } catch (e) {
    console.error('读取监控配置失败:', e.message);
  }

  return { ...DEFAULT_MONITOR };
}

// 保存监控配置
function saveConfig(config) {
  ensureConfigDir();
  const configPath = path.join(CONFIG.configDir, 'monitor.json');
  fs.writeFileSync(configPath, JSON.stringify(config, null, 2), 'utf-8');
  console.log('监控配置已保存:', configPath);
}

// 添加关键词
function addKeyword(keyword) {
  const config = loadConfig();
  const normalizedKeyword = keyword.trim();

  if (!normalizedKeyword) {
    console.error('关键词不能为空');
    return false;
  }

  if (config.keywords.includes(normalizedKeyword)) {
    console.log(`关键词 "${normalizedKeyword}" 已存在`);
    return false;
  }

  config.keywords.push(normalizedKeyword);
  saveConfig(config);
  console.log(`已添加监控关键词: ${normalizedKeyword}`);
  return true;
}

// 移除关键词
function removeKeyword(keyword) {
  const config = loadConfig();
  const normalizedKeyword = keyword.trim();
  const index = config.keywords.indexOf(normalizedKeyword);

  if (index === -1) {
    console.log(`关键词 "${normalizedKeyword}" 不存在`);
    return false;
  }

  config.keywords.splice(index, 1);
  saveConfig(config);
  console.log(`已移除监控关键词: ${normalizedKeyword}`);
  return true;
}

// 列出所有关键词
function listKeywords() {
  const config = loadConfig();
  console.log('\n📋 当前监控关键词:');
  if (config.keywords.length === 0) {
    console.log('  (暂无监控关键词)');
  } else {
    config.keywords.forEach((kw, idx) => {
      console.log(`  ${idx + 1}. ${kw}`);
    });
  }
  console.log('');
  return config.keywords;
}

// 启用/禁用监控
function setEnabled(enabled) {
  const config = loadConfig();
  config.enabled = enabled;
  saveConfig(config);
  console.log(`监控已${enabled ? '启用' : '禁用'}`);
  return config;
}

// 显示帮助
function showHelp() {
  console.log(`
🔔 热点雷达 - 话题监控管理

用法:
  node monitor.js add <关键词>    添加监控关键词
  node monitor.js remove <关键词> 移除监控关键词
  node monitor.js list           列出所有监控关键词
  node monitor.js enable         启用监控
  node monitor.js disable        禁用监控
  node monitor.js status         查看监控状态

示例:
  node monitor.js add "人工智能"
  node monitor.js add "考研"
  node monitor.js remove "人工智能"
  node monitor.js list
`);
}

// 主函数
function main() {
  const args = process.argv.slice(2);
  const command = args[0];

  switch (command) {
    case 'add':
      if (!args[1]) {
        console.error('请提供要添加的关键词');
        process.exit(1);
      }
      addKeyword(args.slice(1).join(' '));
      break;

    case 'remove':
      if (!args[1]) {
        console.error('请提供要移除的关键词');
        process.exit(1);
      }
      removeKeyword(args.slice(1).join(' '));
      break;

    case 'list':
      listKeywords();
      break;

    case 'enable':
      setEnabled(true);
      break;

    case 'disable':
      setEnabled(false);
      break;

    case 'status':
      const config = loadConfig();
      console.log('\n🔔 监控状态:', config.enabled ? '已启用' : '已禁用');
      console.log('📋 监控关键词:');
      if (config.keywords.length === 0) {
        console.log('  (暂无)');
      } else {
        config.keywords.forEach(kw => console.log(`  - ${kw}`));
      }
      console.log('');
      break;

    default:
      showHelp();
  }
}

module.exports = { addKeyword, removeKeyword, listKeywords, setEnabled, loadConfig, saveConfig };

// 直接运行时执行
if (require.main === module) {
  main();
}
