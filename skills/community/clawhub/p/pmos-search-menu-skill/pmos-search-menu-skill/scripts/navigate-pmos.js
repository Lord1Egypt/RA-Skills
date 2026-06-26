#!/usr/bin/env node
/**
 * PMOS 菜单导航自动化脚本
 * 使用 OpenClaw browser 工具自动导航 PMOS 网站菜单
 */

const { execSync } = require('child_process');
const readline = require('readline');

// 配置
const CONFIG = {
  baseUrl: 'https://pmos.gs.sgcc.com.cn/',
  targetTabPattern: 'pxf-settlement',
  defaultTimeout: 2000,
};

// 默认菜单路径
const DEFAULT_MENU_PATH = [
  { name: '信息披露', ref: null, opensNewTab: false },
  { name: '综合查询', ref: null, opensNewTab: true },
  { name: '市场运营', ref: null, opensNewTab: false },
  { name: '交易组织及出清', ref: null, opensNewTab: false },
  { name: '现货市场申报、出清信息', ref: null, opensNewTab: false },
  { name: '实时各节点出清类信息', ref: null, opensNewTab: false },
  { name: '实时市场出清节点电价', ref: null, opensNewTab: false },
];

// 执行 OpenClaw 命令
function runCommand(cmd, silent = false) {
  try {
    const output = execSync(cmd, { encoding: 'utf-8', stdio: silent ? 'pipe' : 'inherit' });
    return output;
  } catch (error) {
    if (!silent) {
      console.error(`命令执行失败：${cmd}`);
      console.error(error.message);
    }
    throw error;
  }
}

// 打开浏览器
function openBrowser() {
  console.log(`🌐 打开 PMOS 网站：${CONFIG.baseUrl}`);
  runCommand(`openclaw browser open "${CONFIG.baseUrl}"`);
}

// 获取页面快照
function getSnapshot(targetId) {
  console.log('📸 获取页面快照...');
  const cmd = targetId
    ? `openclaw browser snapshot --refs aria --targetId ${targetId} --compact`
    : 'openclaw browser snapshot --refs aria --compact';
  return runCommand(cmd, true);
}

// 点击菜单项
function clickMenuItem(ref, targetId) {
  console.log(`👆 点击菜单项 (ref: ${ref})...`);
  const cmd = targetId
    ? `openclaw browser act click --ref ${ref} --targetId ${targetId}`
    : `openclaw browser act click --ref ${ref}`;
  runCommand(cmd);
}

// 获取标签页列表
function getTabs() {
  console.log('📑 获取标签页列表...');
  const output = runCommand('openclaw browser tabs', true);
  try {
    return JSON.parse(output);
  } catch {
    return output;
  }
}

// 切换到指定标签页
function focusTab(targetId) {
  console.log(`🔄 切换到标签页：${targetId}`);
  runCommand(`openclaw browser focus --targetId ${targetId}`);
}

// 查找目标标签页
function findTargetTab() {
  const tabs = getTabs();
  if (Array.isArray(tabs)) {
    const targetTab = tabs.find(tab => 
      tab.url && tab.url.includes(CONFIG.targetTabPattern)
    );
    return targetTab ? targetTab.targetId : null;
  }
  return null;
}

// 等待用户确认
async function waitForUser(message) {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });
  
  return new Promise(resolve => {
    rl.question(message, () => {
      rl.close();
      resolve();
    });
  });
}

// 延迟
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// 主流程
async function navigate(menuPath = DEFAULT_MENU_PATH) {
  console.log('');
  console.log('🦞 PMOS 菜单导航工具');
  console.log('==================');
  console.log(`目标网站：${CONFIG.baseUrl}`);
  console.log(`导航路径：${menuPath.map(m => m.name).join(' → ')}`);
  console.log('');
  
  // 步骤 1: 打开浏览器
  openBrowser();
  
  // 步骤 2: 等待用户登录
  console.log('\n⚠️  请先手动登录网站');
  await waitForUser('登录完成后按回车继续...');
  
  let currentTabId = null;
  
  // 步骤 3: 遍历菜单路径
  for (let i = 0; i < menuPath.length; i++) {
    const menuItem = menuPath[i];
    const stepNum = i + 1;
    
    console.log('');
    console.log('━'.repeat(40));
    console.log(`步骤 ${stepNum}/${menuPath.length}: 点击 "${menuItem.name}"`);
    
    // 获取快照
    const snapshot = getSnapshot(currentTabId);
    
    // 提示用户查找引用
    console.log('🔍 请在快照中查找菜单项引用...');
    console.log(`⚠️  搜索文本：${menuItem.name}`);
    console.log('💡 提示：查看 treeitem 元素');
    
    const rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout,
    });
    
    const ref = await new Promise(resolve => {
      rl.question('  输入元素引用 (例如 e78，留空跳过): ', resolve);
    });
    rl.close();
    
    if (ref) {
      // 点击菜单项
      clickMenuItem(ref, currentTabId);
      await sleep(CONFIG.defaultTimeout);
      
      // 检查是否需要切换标签页
      if (menuItem.opensNewTab) {
        console.log('🔄 等待新标签页打开...');
        await sleep(CONFIG.defaultTimeout);
        
        const newTabId = findTargetTab();
        if (newTabId) {
          currentTabId = newTabId;
          focusTab(currentTabId);
          console.log(`✓ 已切换到新标签页：${currentTabId}`);
        }
      }
    } else {
      console.log('⚠️  跳过此步骤');
    }
  }
  
  console.log('');
  console.log('━'.repeat(40));
  console.log('✅ 导航完成！');
  console.log('');
  console.log('当前页面内容预览：');
  runCommand(`openclaw browser snapshot --refs aria --compact${currentTabId ? ` --targetId ${currentTabId}` : ''}`);
  
  console.log('');
  console.log('💡 提示：如需导出数据，请继续操作页面内的查询和导出功能');
  console.log('');
}

// 执行
navigate().catch(console.error);
