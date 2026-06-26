#!/usr/bin/env node
/**
 * 自定义模板配置初始化脚本
 *
 * 用法：node init-custom-config.js
 *
 * 此脚本在用户项目中创建自定义模板配置文件，
 * 允许用户覆盖或扩展默认的templates-config
 */

const fs = require('fs');
const path = require('path');
const readline = require('readline');

function createRL() {
  return readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });
}

function ask(rl, question) {
  return new Promise((resolve) => {
    rl.question(question, (answer) => {
      resolve(answer.trim());
    });
  });
}

async function main() {
  const rl = createRL();
  const projectDir = process.cwd();

  console.log('╔════════════════════════════════════════════════╗');
  console.log('║      ⚙️  自定义模板配置向导                     ║');
  console.log('╚════════════════════════════════════════════════╝');
  console.log('');
  console.log('此向导将帮助您创建自定义的产品类型配置。');
  console.log('');

  try {
    // 检查是否已有配置文件
    const configDir = path.join(projectDir, 'templates-config');
    if (!fs.existsSync(configDir)) {
      fs.mkdirSync(configDir, { recursive: true });
    }

    // 选择操作
    console.log('请选择操作：');
    console.log('  1. 创建新的产品类型配置');
    console.log('  2. 复制默认配置并修改');
    console.log('  3. 查看当前配置');

    const choice = await ask(rl, '\n请输入数字（1-3）：');

    if (choice === '1') {
      await createNewConfig(rl, configDir);
    } else if (choice === '2') {
      await copyDefaultConfig(rl, configDir);
    } else if (choice === '3') {
      await showCurrentConfig(configDir);
    } else {
      console.log('❌ 无效的选择');
    }

    rl.close();

  } catch (error) {
    console.error('❌ 发生错误:', error.message);
    rl.close();
    process.exit(1);
  }
}

async function createNewConfig(rl, configDir) {
  console.log('\n--- 创建新的产品类型配置 ---');

  const typeId = await ask(rl, '请输入产品类型ID（如：health）：');
  const typeName = await ask(rl, '请输入产品类型名称（如：健康医疗）：');

  const config = {
    id: typeId,
    name: typeName,
    keywords: [],
    focusAreas: [],
    commonFeatures: [],
    userRoles: [],
    specialEvents: [],
    commonFlows: []
  };

  // 关键词
  console.log('\n请输入识别关键词（用于自动匹配此类型，回车结束）：');
  while (true) {
    const keyword = await ask(rl, `  关键词 ${config.keywords.length + 1}（回车结束）：`);
    if (!keyword) break;
    config.keywords.push(keyword);
  }

  // 关注焦点
  console.log('\n请输入此类型产品的关注焦点（回车结束）：');
  while (true) {
    const focus = await ask(rl, `  焦点 ${config.focusAreas.length + 1}（回车结束）：`);
    if (!focus) break;
    config.focusAreas.push(focus);
  }

  // 常用功能
  console.log('\n请输入此类型产品的常用功能（回车结束）：');
  while (true) {
    const feature = await ask(rl, `  功能 ${config.commonFeatures.length + 1}（回车结束）：`);
    if (!feature) break;
    config.commonFeatures.push(feature);
  }

  // 用户角色
  console.log('\n请输入此类型产品的典型用户角色（回车结束）：');
  while (true) {
    const role = await ask(rl, `  角色 ${config.userRoles.length + 1}（回车结束）：`);
    if (!role) break;
    config.userRoles.push(role);
  }

  // 特殊埋点事件
  console.log('\n请输入此类型产品的特殊埋点事件（回车结束）：');
  while (true) {
    const event = await ask(rl, `  事件 ${config.specialEvents.length + 1}（回车结束）：`);
    if (!event) break;
    config.specialEvents.push(event);
  }

  // 常见流程图
  console.log('\n请输入此类型产品的常见流程图名称（回车结束）：');
  while (true) {
    const flow = await ask(rl, `  流程 ${config.commonFlows.length + 1}（回车结束）：`);
    if (!flow) break;
    config.commonFlows.push(flow);
  }

  // 保存配置
  const configFile = path.join(configDir, `${typeId}.json`);
  fs.writeFileSync(configFile, JSON.stringify(config, null, 2) + '\n');

  console.log(`\n✅ 配置已保存: ${configFile}`);
  console.log('\n使用此配置：');
  console.log(`  在 SKILL.md 中将此项目标记为 "${typeName}" 类型`);
}

async function copyDefaultConfig(rl, configDir) {
  // 获取默认配置目录
  const skillDir = path.dirname(__dirname); // 假设脚本在 scripts/ 目录
  const defaultConfigDir = path.join(skillDir, 'templates-config');

  if (!fs.existsSync(defaultConfigDir)) {
    console.log('❌ 找不到默认配置目录');
    return;
  }

  // 列出可用配置
  const configs = fs.readdirSync(defaultConfigDir).filter(f => f.endsWith('.json'));

  console.log('\n可用的默认配置：');
  configs.forEach((cfg, i) => {
    const name = cfg.replace('.json', '');
    console.log(`  ${i + 1}. ${name}`);
  });

  const choice = await ask(rl, '\n请选择要复制的配置（输入数字）：');
  const selected = configs[parseInt(choice) - 1];

  if (!selected) {
    console.log('❌ 无效的选择');
    return;
  }

  // 复制并允许修改
  const sourcePath = path.join(defaultConfigDir, selected);
  const config = JSON.parse(fs.readFileSync(sourcePath, 'utf-8'));

  console.log(`\n--- 修改配置: ${config.name} ---`);
  console.log('(直接回车保持原值)');

  const newName = await ask(rl, `名称 [${config.name}]：`);
  if (newName) config.name = newName;

  // 可以添加更多修改选项...

  const destPath = path.join(configDir, selected);
  fs.writeFileSync(destPath, JSON.stringify(config, null, 2) + '\n');

  console.log(`\n✅ 配置已复制到: ${destPath}`);
  console.log('您可以直接编辑此文件来自定义配置。');
}

async function showCurrentConfig(configDir) {
  if (!fs.existsSync(configDir)) {
    console.log('❌ 项目中暂无自定义配置');
    return;
  }

  const configs = fs.readdirSync(configDir).filter(f => f.endsWith('.json'));

  if (configs.length === 0) {
    console.log('❌ 项目中暂无自定义配置');
    return;
  }

  console.log('\n当前自定义配置：');
  configs.forEach(cfg => {
    const config = JSON.parse(fs.readFileSync(path.join(configDir, cfg), 'utf-8'));
    console.log(`\n  📄 ${cfg}`);
    console.log(`     名称: ${config.name}`);
    console.log(`     关键词: ${config.keywords?.join(', ') || '无'}`);
    console.log(`     功能: ${config.commonFeatures?.join(', ') || '无'}`);
  });
}

// 导出函数供其他脚本使用
module.exports = {
  loadCustomConfig(projectDir, typeId) {
    const customConfigPath = path.join(projectDir, 'templates-config', `${typeId}.json`);
    if (fs.existsSync(customConfigPath)) {
      return JSON.parse(fs.readFileSync(customConfigPath, 'utf-8'));
    }
    return null;
  },

  mergeWithDefault(defaultConfig, customConfig) {
    return {
      ...defaultConfig,
      ...customConfig,
      keywords: [...(defaultConfig.keywords || []), ...(customConfig.keywords || [])],
      commonFeatures: [...(defaultConfig.commonFeatures || []), ...(customConfig.commonFeatures || [])],
      userRoles: [...(defaultConfig.userRoles || []), ...(customConfig.userRoles || [])],
      specialEvents: [...(defaultConfig.specialEvents || []), ...(customConfig.specialEvents || [])],
      commonFlows: [...(defaultConfig.commonFlows || []), ...(customConfig.commonFlows || [])]
    };
  }
};

// 如果直接运行此脚本
if (require.main === module) {
  main();
}
