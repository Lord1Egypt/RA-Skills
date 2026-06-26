#!/usr/bin/env node
'use strict';
/**
 * Git 项目监控助手 - 支持 GitHub、GitLab、Gitee 等所有 Git 平台
 */

const fs = require('fs');
const path = require('path');
const os = require('os');
const { execSync } = require('child_process');

const CONFIG_PATH = path.join(__dirname, 'config.json');
const SCRIPT_PATH = path.join(__dirname, 'monitor.sh');

// 检查是否为 verbose 模式
const VERBOSE = process.argv.includes('--verbose') || process.argv.includes('-v');

// 日志函数
function log(message) {
  if (VERBOSE) {
    console.log(message);
  }
}

// 读取配置
function loadConfig() {
  if (!fs.existsSync(CONFIG_PATH)) {
    const defaultConfig = {
      repositories: [],
      checkInterval: '6h',
      notifyChannel: 'feishu',
      maxCommitsToShow: 10,
      includeDiffSummary: true
    };
    saveConfig(defaultConfig);
    return defaultConfig;
  }
  return JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf8'));
}

// 级联读取飞书配置（优先级：环境变量 > OpenClaw配置 > 本地config.json）
function getFeishuConfig() {
  // 1. 先检查环境变量
  if (process.env.FEISHU_APP_ID && process.env.FEISHU_APP_SECRET && process.env.FEISHU_CHAT_ID) {
    return {
      appId: process.env.FEISHU_APP_ID,
      appSecret: process.env.FEISHU_APP_SECRET,
      chatId: process.env.FEISHU_CHAT_ID
    };
  }
  
  // 2. 尝试读取 OpenClaw 主配置
  const openclawConfigPath = path.join(os.homedir(), '.openclaw', 'openclaw.json');
  if (fs.existsSync(openclawConfigPath)) {
    try {
      const openclawConfig = JSON.parse(fs.readFileSync(openclawConfigPath, 'utf8'));
      const feishu = openclawConfig.channels?.feishu || openclawConfig.feishu;
      if (feishu?.appId && feishu?.appSecret) {
        // 尝试获取群聊ID（优先使用环境变量或配置的chatId）
        const chatId = process.env.FEISHU_CHAT_ID || feishu.chatId || feishu.groupId;
        if (chatId) {
          return {
            appId: feishu.appId,
            appSecret: feishu.appSecret,
            chatId: chatId
          };
        }
      }
    } catch (e) {
      log(`读取OpenClaw配置失败: ${e.message}`);
    }
  }
  
  // 3. 最后读取本地 config.json
  const config = loadConfig();
  if (config.feishu?.appId && config.feishu?.appSecret && config.feishu?.chatId) {
    // 检查是否是占位符
    if (config.feishu.appId !== 'YOUR_FEISHU_APP_ID' && 
        config.feishu.appSecret !== 'YOUR_FEISHU_APP_SECRET') {
      return config.feishu;
    }
  }
  
  return null;
}

// 发送飞书通知
async function sendFeishuNotification(message, chatId) {
  const config = getFeishuConfig();
  if (!config) {
    console.log('⚠️ 未配置飞书通知，跳过推送');
    return false;
  }
  
  const { appId, appSecret, chatId: configChatId } = config;
  const targetChatId = chatId || configChatId;
  
  if (!targetChatId) {
    console.log('⚠️ 未配置飞书群聊ID，跳过推送');
    return false;
  }
  
  try {
    // 获取 tenant_access_token
    const tokenResponse = await fetch('https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ app_id: appId, app_secret: appSecret })
    });
    const tokenData = await tokenResponse.json();
    
    if (!tokenData.tenant_access_token) {
      console.log('❌ 获取飞书token失败:', tokenData);
      return false;
    }
    
    // 发送消息
    const msgResponse = await fetch('https://open.feishu.cn/open-apis/im/v1/messages', {
      method: 'POST',
      headers: { 
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${tokenData.tenant_access_token}`
      },
      body: JSON.stringify({
        receive_id: targetChatId,
        msg_type: 'text',
        content: JSON.stringify({ text: message })
      })
    });
    const msgData = await msgResponse.json();
    
    if (msgData.code === 0) {
      console.log('✅ 飞书通知发送成功');
      return true;
    } else {
      console.log('❌ 飞书通知发送失败:', msgData);
      return false;
    }
  } catch (e) {
    console.log('❌ 飞书通知发送异常:', e.message);
    return false;
  }
}

// 保存配置
function saveConfig(config) {
  fs.writeFileSync(CONFIG_PATH, JSON.stringify(config, null, 2));
}

// 解析仓库 URL 或简写
function parseRepoInput(input) {
  // 完整 URL
  if (input.startsWith('http://') || input.startsWith('https://')) {
    const url = new URL(input);
    const pathParts = url.pathname.replace(/\.git$/, '').split('/').filter(Boolean);
    
    if (pathParts.length < 2) {
      throw new Error('无效的仓库 URL');
    }
    
    const owner = pathParts[0];
    const repo = pathParts[1];
    const platform = url.hostname.includes('gitlab') ? 'gitlab' : 
                     url.hostname.includes('gitee') ? 'gitee' : 'github';
    
    return {
      url: input.endsWith('.git') ? input : input + '.git',
      name: `${owner}-${repo}`,
      platform,
      owner,
      repo
    };
  }
  
  // 简写格式: owner/repo 或 platform:owner/repo
  let platform = 'github';
  let repoPath = input;
  
  if (input.includes(':')) {
    [platform, repoPath] = input.split(':');
  }
  
  const [owner, repo] = repoPath.split('/');
  if (!owner || !repo) {
    throw new Error('无效的仓库格式，应为 owner/repo 或 platform:owner/repo');
  }
  
  // 构建 URL
  const platformUrls = {
    github: 'https://github.com',
    gitlab: 'https://gitlab.com',
    gitee: 'https://gitee.com'
  };
  
  const baseUrl = platformUrls[platform.toLowerCase()] || platformUrls.github;
  const url = `${baseUrl}/${owner}/${repo}.git`;
  
  return {
    url,
    name: `${owner}-${repo}`,
    platform: platform.toLowerCase(),
    owner,
    repo
  };
}

// 添加仓库
function addRepository(input, branch = 'main') {
  const config = loadConfig();
  
  try {
    const repoInfo = parseRepoInput(input);
    
    // 检查是否已存在
    const existing = config.repositories.find(r => r.url === repoInfo.url);
    if (existing) {
      console.log(`⚠️  仓库已存在: ${existing.name}`);
      return existing;
    }
    
    const localPath = path.join(
      os.homedir(),
      '.openclaw/workspace/repos',
      repoInfo.name
    );
    
    const repo = {
      url: repoInfo.url,
      name: repoInfo.name,
      platform: repoInfo.platform,
      owner: repoInfo.owner,
      repo: repoInfo.repo,
      localPath,
      branch,
      lastChecked: null,
      lastCommit: null,
      addedAt: new Date().toISOString()
    };
    
    config.repositories.push(repo);
    saveConfig(config);
    
    console.log(`✅ 已添加仓库: ${repo.name}`);
    console.log(`   平台: ${repo.platform}`);
    console.log(`   URL: ${repo.url}`);
    console.log(`   本地路径: ${repo.localPath}`);
    
    return repo;
  } catch (error) {
    console.error(`❌ 添加失败: ${error.message}`);
    throw error;
  }
}

// 删除仓库
function removeRepository(nameOrUrl) {
  const config = loadConfig();
  
  const index = config.repositories.findIndex(r => 
    r.name === nameOrUrl || r.url === nameOrUrl || 
    `${r.owner}/${r.repo}` === nameOrUrl
  );
  
  if (index === -1) {
    console.log(`⚠️  未找到仓库: ${nameOrUrl}`);
    return false;
  }
  
  const repo = config.repositories[index];
  config.repositories.splice(index, 1);
  saveConfig(config);
  
  console.log(`✅ 已删除仓库: ${repo.name}`);
  console.log(`   提示: 本地文件未删除，位于 ${repo.localPath}`);
  
  return true;
}

// 列出所有仓库
function listRepositories() {
  const config = loadConfig();
  
  if (config.repositories.length === 0) {
    console.log('📋 当前没有监控任何仓库');
    console.log('');
    console.log('使用以下命令添加仓库:');
    console.log('  node helper.js add owner/repo');
    console.log('  node helper.js add https://github.com/owner/repo');
    console.log('  node helper.js add gitlab:owner/repo');
    return;
  }
  
  console.log(`📋 监控列表 (共 ${config.repositories.length} 个仓库):\n`);
  
  config.repositories.forEach((repo, index) => {
    const lastCheckTime = repo.lastChecked 
      ? new Date(repo.lastChecked).toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai', hour: '2-digit', minute: '2-digit' })
      : '从未检查';
    const lastCommit = repo.lastCommit ? repo.lastCommit.substring(0, 7) : '未知';
    
    console.log(`${index + 1}. ${repo.name}`);
    console.log(`   平台: ${repo.platform} · 分支: ${repo.branch}`);
    console.log(`   最后检查: ${lastCheckTime} · 最新: ${lastCommit}`);
    console.log('');
  });
}

// 执行监控脚本（跨平台版本，不再依赖 bash）
function checkRepository(repo) {
  const { url, name, localPath, branch = 'main' } = repo;
  
  log(`\n🔍 检查仓库: ${name}`);
  log(`   本地路径: ${localPath}`);
  
  try {
    const git = (...args) => {
      try {
        return execSync(`git ${args.join(' ')}`, { 
          encoding: 'utf8', 
          maxBuffer: 10 * 1024 * 1024,
          cwd: localPath,
          stdio: ['ignore', 'pipe', 'pipe']
        });
      } catch (e) {
        return e.stdout || e.message;
      }
    };
    
    // 1. 判断本地仓库是否存在
    const repoExists = fs.existsSync(path.join(localPath, '.git'));
    
    if (!repoExists) {
      // 首次克隆
      log('   首次克隆仓库...');
      execSync(`git clone "${url}" "${localPath}" --depth=100`, {
        encoding: 'utf8',
        maxBuffer: 50 * 1024 * 1024,
        stdio: ['ignore', 'pipe', 'pipe']
      });
      
      const commit = execSync(`git rev-parse HEAD`, {
        encoding: 'utf8',
        cwd: localPath
      }).trim();
      
      return {
        isInitial: true,
        repo: repo.name,
        commit
      };
    }
    
    // 2. 更新到最新
    log('   拉取最新代码...');
    
    // 保存当前 HEAD commit（用于对比）
    let oldCommit = '';
    try {
      oldCommit = execSync('git rev-parse HEAD', { cwd: localPath }).trim();
    } catch (e) {
      oldCommit = '';
    }
    
    // fetch + reset --hard origin/branch
    try {
      execSync(`git fetch origin`, { cwd: localPath, stdio: ['ignore', 'pipe', 'pipe'] });
      execSync(`git reset --hard origin/${branch}`, { cwd: localPath, stdio: ['ignore', 'pipe', 'pipe'] });
    } catch (e) {
      // 分支可能不存在，尝试 master
      try {
        execSync(`git fetch origin`, { cwd: localPath, stdio: ['ignore', 'pipe', 'pipe'] });
        execSync(`git reset --hard origin/master`, { cwd: localPath, stdio: ['ignore', 'pipe', 'pipe'] });
      } catch (e2) {
        return { hasUpdates: false, error: `拉取失败: ${e2.message}`, repo: repo.name };
      }
    }
    
    // 获取新 commit
    const newCommit = execSync('git rev-parse HEAD', { cwd: localPath }).trim();
    
    // 如果没有变化
    if (oldCommit === newCommit) {
      return { hasUpdates: false, repo: repo.name };
    }
    
    // 有更新，获取 commits 和 files
    log('   获取变更详情...');
    
    const diffOutput = execSync(
      `git log ${oldCommit}..${newCommit} --oneline --format="%H|%an|%ai|%s" -20`,
      { cwd: localPath }
    ).trim();
    
    const commits = diffOutput.split('\n').filter(Boolean).map(line => {
      const [hash, author, time, ...msgParts] = line.split('|');
      return {
        hash: hash?.substring(0, 7),
        fullHash: hash,
        author,
        time: time?.replace('+0800', '').trim(),
        message: msgParts.join('|')
      };
    });
    
    // 获取文件变更
    const filesOutput = execSync(
      `git diff ${oldCommit}..${newCommit} --stat --format=""`,
      { cwd: localPath }
    ).trim();
    
    const files = filesOutput.split('\n').filter(Boolean).map(line => {
      const match = line.match(/^\s*(\S+)\s*\|\s*(\d+)/);
      if (match) {
        return { status: 'M', path: match[1], lines: match[2] };
      }
      // 新文件或删除
      const parts = line.trim().split(/\s+/);
      return { status: 'M', path: parts[parts.length - 1] };
    });
    
    return {
      hasUpdates: true,
      repo: repo.name,
      url: repo.url,
      platform: repo.platform,
      owner: repo.owner,
      repoName: repo.repo,
      oldCommit,
      newCommit,
      commits,
      files,
      stats: filesOutput
    };
    
  } catch (error) {
    console.error(`❌ 检查失败: ${error.message}`);
    return { hasUpdates: false, error: error.message, repo: repo.name };
  }
}

// 解析脚本输出
function parseOutput(output, repo) {
  if (output.includes('NO_UPDATES')) {
    return { hasUpdates: false, repo: repo.name };
  }
  
  if (output.includes('INITIAL_COMMIT=')) {
    const match = output.match(/INITIAL_COMMIT=([a-f0-9]+)/);
    return {
      isInitial: true,
      repo: repo.name,
      commit: match ? match[1] : null
    };
  }
  
  // 提取 commits
  const commitsMatch = output.match(/=== COMMITS_START ===\n([\s\S]*?)\n=== COMMITS_END ===/);
  const commits = commitsMatch ? parseCommits(commitsMatch[1]) : [];
  
  // 提取统计信息
  const statsMatch = output.match(/=== STATS_START ===\n([\s\S]*?)\n=== STATS_END ===/);
  const stats = statsMatch ? statsMatch[1].trim() : '';
  
  // 提取文件变更
  const filesMatch = output.match(/=== FILES_START ===\n([\s\S]*?)\n=== FILES_END ===/);
  const files = filesMatch ? parseFiles(filesMatch[1]) : [];
  
  // 提取 commit hash
  const oldCommitMatch = output.match(/OLD_COMMIT=([a-f0-9]+)/);
  const newCommitMatch = output.match(/NEW_COMMIT=([a-f0-9]+)/);
  
  return {
    hasUpdates: true,
    repo: repo.name,
    url: repo.url,
    platform: repo.platform,
    owner: repo.owner,
    repoName: repo.repo,
    oldCommit: oldCommitMatch ? oldCommitMatch[1] : null,
    newCommit: newCommitMatch ? newCommitMatch[1] : null,
    commits,
    stats,
    files
  };
}

// 解析 commit 列表
function parseCommits(text) {
  return text.trim().split('\n').filter(Boolean).map(line => {
    const [hash, author, time, ...messageParts] = line.split('|');
    return {
      hash: hash?.substring(0, 7),
      fullHash: hash,
      author,
      time,
      message: messageParts.join('|')
    };
  });
}

// 解析文件变更
function parseFiles(text) {
  return text.trim().split('\n').filter(Boolean).map(line => {
    const [status, ...pathParts] = line.split('\t');
    return {
      status: status.trim(),
      path: pathParts.join('\t').trim()
    };
  });
}

// 生成摘要
function generateSummary(result) {
  if (!result.hasUpdates) {
    return `[${result.repo}] 已是最新`;
  }
  
  if (result.isInitial) {
    return `[${result.repo}] 已克隆 (commit: ${result.commit?.substring(0, 7)})`;
  }
  
  const { repo, url, platform, owner, repoName, commits, stats, files, oldCommit, newCommit } = result;
  
  // 生成简洁的摘要（适合飞书推送，纯文本）
  // 显示完整仓库地址
  const repoUrl = url.replace('.git', '');
  let summary = `${repoUrl}\n`;
  summary += `${commits.length} 个提交, ${files.length} 个文件变更\n\n`;
  
  // 最新的提交
  if (commits.length > 0) {
    const latest = commits[0];
    summary += `最新: ${latest.message}\n`;
    summary += `${latest.author} · ${latest.time}\n`;
  }
  
  // 文件变更预览
  if (files.length > 0) {
    const added = files.filter(f => f.status === 'A').length;
    const modified = files.filter(f => f.status === 'M').length;
    const deleted = files.filter(f => f.status === 'D').length;
    
    summary += `\n${added} 新增, ${modified} 修改, ${deleted} 删除\n`;
    
    // 显示前3个文件
    const previewFiles = files.slice(0, 3).map(f => {
      const prefix = f.status === 'A' ? '+' : f.status === 'M' ? '*' : '-';
      return `${prefix} ${f.path}`;
    }).join('\n');
    
    if (previewFiles) {
      summary += `\n${previewFiles}`;
    }
  }
  
  // 链接
  const compareUrl = `https://${platform === 'gitee' ? 'gitee.com' : platform === 'gitlab' ? 'gitlab.com' : 'github.com'}/${owner}/${repoName}/compare/${oldCommit?.substring(0, 7)}...${newCommit?.substring(0, 7)}`;
  summary += `\n\n查看: ${compareUrl}`;
  
  return summary;
}

// 主函数
async function main() {
  const args = process.argv.slice(2);
  const command = args[0];
  
  if (command === 'add') {
    const input = args[1];
    const branch = args[2] || 'main';
    
    if (!input) {
      console.error('❌ 请指定仓库');
      console.log('用法: node helper.js add <repo>');
      console.log('示例:');
      console.log('  node helper.js add owner/repo');
      console.log('  node helper.js add https://github.com/owner/repo');
      console.log('  node helper.js add gitlab:owner/repo');
      console.log('  node helper.js add https://gitee.com/owner/repo');
      process.exit(1);
    }
    
    addRepository(input, branch);
    
  } else if (command === 'remove' || command === 'delete') {
    const nameOrUrl = args[1];
    
    if (!nameOrUrl) {
      console.error('❌ 请指定要删除的仓库');
      console.log('用法: node helper.js remove <name|url>');
      process.exit(1);
    }
    
    removeRepository(nameOrUrl);
    
  } else if (command === 'list') {
    listRepositories();
    
  } else if (command === 'check') {
    const config = loadConfig();
    const repoName = args[1];
    
    let repos = config.repositories;
    if (repoName) {
      repos = repos.filter(r => 
        r.name === repoName || 
        `${r.owner}/${r.repo}` === repoName
      );
      
      if (repos.length === 0) {
        console.error(`❌ 未找到仓库: ${repoName}`);
        process.exit(1);
      }
    }
    
    if (repos.length === 0) {
      console.log('📋 当前没有监控任何仓库');
      console.log('使用 node helper.js add <repo> 添加仓库');
      process.exit(0);
    }
    
    const results = repos.map(repo => {
      const result = checkRepository(repo);
      
      // 更新配置（无论是否有更新都记录检查时间）
      repo.lastChecked = new Date().toISOString();
      if (result.hasUpdates || result.isInitial) {
        if (result.newCommit) {
          repo.lastCommit = result.newCommit;
        } else if (result.commit) {
          repo.lastCommit = result.commit;
        }
      }
      
      return result;
    });
    
    saveConfig(config);
    
    // 输出结果
    console.log('\n' + '='.repeat(60));
    results.forEach(result => {
      console.log('\n' + generateSummary(result));
    });
    console.log('='.repeat(60) + '\n');
    
    // 返回 JSON 供 OpenClaw 使用
    console.log('\n=== JSON_RESULT ===');
    console.log(JSON.stringify(results, null, 2));
    
    // 检查是否有更新，发送飞书通知
    const updates = results.filter(r => r.hasUpdates);
    if (updates.length > 0) {
      const notifyMessage = updates.map(r => generateSummary(r)).join('\n\n');
      const feishuConfig = getFeishuConfig();
      if (feishuConfig?.chatId) {
        console.log('\n📤 正在发送飞书通知...');
        await sendFeishuNotification(notifyMessage, feishuConfig.chatId);
      } else {
        console.log('\n⚠️ 未配置飞书通知，跳过推送');
        console.log('提示: 可通过以下方式配置飞书:');
        console.log('  1. 设置环境变量: FEISHU_APP_ID, FEISHU_APP_SECRET, FEISHU_CHAT_ID');
        console.log('  2. 或在 OpenClaw 配置中设置飞书凭证');
        console.log('  3. 或编辑 config.json 配置 feishu');
      }
    }
    
  } else if (command === 'status') {
    listRepositories();
    
  } else {
    console.log('Git 项目监控工具 - 支持 GitHub、GitLab、Gitee 等所有 Git 平台\n');
    console.log('用法:');
    console.log('  node helper.js add <repo> [branch]     - 添加监控仓库');
    console.log('  node helper.js remove <name>           - 删除监控仓库');
    console.log('  node helper.js list                    - 列出所有仓库');
    console.log('  node helper.js check [repo-name]       - 检查更新');
    console.log('  node helper.js status                  - 查看监控状态');
    console.log('');
    console.log('示例:');
    console.log('  node helper.js add anthropics/skills');
    console.log('  node helper.js add https://github.com/openai/openai-python');
    console.log('  node helper.js add gitlab:gitlab-org/gitlab');
    console.log('  node helper.js add https://gitee.com/mindspore/mindspore');
    console.log('  node helper.js check anthropics-skills');
    console.log('  node helper.js remove anthropics-skills');
  }
}

if (require.main === module) {
  main().catch(console.error);
}

module.exports = { addRepository, removeRepository, checkRepository, generateSummary, listRepositories };
