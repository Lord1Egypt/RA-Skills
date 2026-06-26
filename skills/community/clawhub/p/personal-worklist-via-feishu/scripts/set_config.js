/**
 * 动态更新飞书 API 凭证配置
 * 用法:
 *   node set_config.js --app-id "cli_xxx" --app-secret "xxx" --app-token "xxx" --table-id "xxx"
 *   node set_config.js --app-token "NEW_TOKEN" --table-id "NEW_TABLE_ID"
 *   node set_config.js --list
 * 
 * 说明：
 *   - 不带参数时显示当前配置
 *   - 支持部分更新，只提供想修改的字段即可
 *   - 修改前会显示旧值和新值供确认
 */

const fs = require('fs');
const path = require('path');

// 当前配置（从 config.js 读取）
const CONFIG_PATH = path.join(__dirname, 'config.js');

function readConfig() {
  const content = fs.readFileSync(CONFIG_PATH, 'utf8');
  const match = content.match(/const CONFIG = \{([^}]+)\}/s);
  if (!match) return null;
  
  const config = {};
  const pairs = match[1].split(',');
  pairs.forEach(pair => {
    const [key, value] = pair.split(':').map(s => s.trim());
    if (key && value) {
      const cleanValue = value.replace(/['"]/g, '').trim();
      config[key] = cleanValue;
    }
  });
  return config;
}

function parseArgs() {
  const args = process.argv.slice(2);
  const config = {};
  for (let i = 0; i < args.length; i += 2) {
    const key = args[i].replace('--', '');
    const value = args[i + 1];
    config[key] = value;
  }
  return config;
}

function updateConfig(updates) {
  let content = fs.readFileSync(CONFIG_PATH, 'utf8');
  
  for (const [key, value] of Object.entries(updates)) {
    // 匹配类似 APP_ID: 'xxx' 的模式
    const regex = new RegExp(`(${key}\\s*:\\s*)'[^']*'`, 'g');
    if (regex.test(content)) {
      content = content.replace(regex, `$1'${value}'`);
    } else {
      // 如果没找到，尝试匹配多行配置块
      console.log(`⚠️  ${key} 在配置中未找到，跳过`);
    }
  }
  
  fs.writeFileSync(CONFIG_PATH, content, 'utf8');
  return true;
}

function showCurrentConfig() {
  const config = readConfig();
  if (!config) {
    console.error('❌ 无法读取当前配置');
    return;
  }
  
  console.log('\n📋 当前飞书 API 凭证配置：\n');
  console.log(`   APP_ID:    ${config.APP_ID || '(未设置)'}`);
  console.log(`   APP_SECRET: ${config.APP_SECRET ? '******' : '(未设置)'}`);
  console.log(`   APP_TOKEN: ${config.APP_TOKEN || '(未设置)'}`);
  console.log(`   TABLE_ID:  ${config.TABLE_ID || '(未设置)'}`);
  console.log();
}

async function main() {
  const args = parseArgs();
  
  // --list 显示当前配置
  if (args.list) {
    showCurrentConfig();
    return;
  }
  
  // 不带参数时显示帮助
  if (Object.keys(args).length === 0) {
    console.log('\n📝 set_config.js - 动态更新飞书 API 凭证');
    console.log('\n用法:');
    console.log('   node set_config.js --list                              # 显示当前配置');
    console.log('   node set_config.js --app-token "NEW_TOKEN"             # 更新 APP_TOKEN');
    console.log('   node set_config.js --table-id "NEW_TABLE_ID"           # 更新 TABLE_ID');
    console.log('   node set_config.js --app-id "cli_xxx" --app-secret "xxx"  # 同时更新多个字段');
    console.log('\n示例:');
    console.log('   node set_config.js --app-token "YOUR_APP_TOKEN" --table-id "YOUR_TABLE_ID"');
    showCurrentConfig();
    return;
  }
  
  // 读取当前配置
  const currentConfig = readConfig();
  if (!currentConfig) {
    console.error('❌ 无法读取当前配置，请检查 config.js 是否存在');
    process.exit(1);
  }
  
  // 过滤掉无效参数
  const validKeys = ['app-id', 'app-secret', 'app-token', 'table-id'];
  const updates = {};
  
  for (const [key, value] of Object.entries(args)) {
    if (validKeys.includes(key)) {
      // 转换为 CONFIG 中的键名（APP_ID, APP_SECRET 等）
      const configKey = key.toUpperCase().replace('-', '_');
      updates[configKey] = value;
    }
  }
  
  if (Object.keys(updates).length === 0) {
    console.error('❌ 未提供有效的配置参数');
    console.log('   有效参数: --app-id, --app-secret, --app-token, --table-id');
    process.exit(1);
  }
  
  // 显示变更预览
  console.log('\n📝 配置变更预览：\n');
  for (const [key, newValue] of Object.entries(updates)) {
    const oldValue = currentConfig[key] || '(未设置)';
    if (key === 'APP_SECRET' && oldValue !== '(未设置)') {
      console.log(`   ${key}: ${'******'} → ${newValue ? '******' : '(未设置)'}`);
    } else {
      console.log(`   ${key}: ${oldValue} → ${newValue || '(未设置)'}`);
    }
  }
  console.log();
  
  // 执行更新
  updateConfig(updates);
  
  console.log('✅ 配置文件已更新！\n');
  showCurrentConfig();
}

main();