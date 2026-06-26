#!/usr/bin/env node

/**
 * OpenClaw Security Audit
 * 自动检查 OpenClaw 配置文件中的安全风险
 * 只检查并提示，不自动修复
 * 执行官方安全审计
 */

const fs = require('fs');
const path = require('path');
const os = require('os');
const { execSync } = require('child_process');

// 跨平台获取用户主目录
function getConfigPath() {
  return path.join(os.homedir(), '.openclaw', 'openclaw.json');
}

// 读取配置文件
function readConfig(configPath) {
  if (!fs.existsSync(configPath)) {
    console.error('配置文件不存在:', configPath);
    console.log('请先运行 openclaw gateway start 初始化配置');
    process.exit(1);
  }

  const content = fs.readFileSync(configPath, 'utf8');
  try {
    return JSON.parse(content);
  } catch (e) {
    console.error('配置文件格式错误:', e.message);
    process.exit(1);
  }
}

// 检查配置，仅提示，不修复
function checkConfig(config) {
  const findings = [];

  // 1. gateway.bind: 0.0.0.0 -> 建议 127.0.0.1
  if (config.gateway && config.gateway.bind === '0.0.0.0') {
    findings.push({
      key: 'gateway.bind',
      current: '0.0.0.0',
      suggested: '127.0.0.1',
      reason: '绑定到 0.0.0.0 允许外部访问，存在安全风险',
      action: '请将 gateway.bind 修改为 127.0.0.1'
    });
  }

  // 2. gateway.auth.token: 短或默认 -> 建议使用至少 32 位强随机字符串
  if (config.gateway && config.gateway.auth && typeof config.gateway.auth.token === 'string') {
    const token = config.gateway.auth.token;
    const isDefault =
      token === 'your-secure-token-here' ||
      token === '' ||
      token === 'default';

    if (token.length < 32 || isDefault) {
      const masked = token.length > 8 ? token.slice(0, 8) + '...' : token || '(空)';
      findings.push({
        key: 'gateway.auth.token',
        current: masked,
        suggested: '至少 32 位强随机字符串',
        reason: 'Token 过短或为默认值，存在认证风险',
        action: '请手动生成并替换为至少 32 位的强随机 token'
      });
    }
  }

  // 3. controlUi.allowInsecureAuth: true -> 建议 false
  if (config.controlUi && config.controlUi.allowInsecureAuth === true) {
    findings.push({
      key: 'controlUi.allowInsecureAuth',
      current: 'true',
      suggested: 'false',
      reason: '允许不安全认证可能导致未授权访问',
      action: '请将 controlUi.allowInsecureAuth 修改为 false'
    });
  }

  // 4. tools.exec.security: full -> 建议 allowlist
  if (config.tools && config.tools.exec && config.tools.exec.security === 'full') {
    findings.push({
      key: 'tools.exec.security',
      current: 'full',
      suggested: 'allowlist',
      reason: 'security=full 允许执行任意命令，存在安全风险',
      action: '请将 tools.exec.security 修改为 allowlist'
    });
  }

  // 5. tools.exec.ask: off -> 建议 on-miss
  if (config.tools && config.tools.exec && config.tools.exec.ask === 'off') {
    findings.push({
      key: 'tools.exec.ask',
      current: 'off',
      suggested: 'on-miss',
      reason: 'ask=off 可能导致未经确认执行危险操作',
      action: '请将 tools.exec.ask 修改为 on-miss'
    });
  }

  return findings;
}

// 打印检查结果
function printFindings(findings) {
  console.log('\n' + '='.repeat(60));
  console.log('配置检查报告');
  console.log('='.repeat(60));

  if (findings.length === 0) {
    console.log('所有配置项均为安全值，未发现需要调整的项目');
    return false;
  }

  console.log(`\n发现 ${findings.length} 项配置存在风险，请手动处理:\n`);

  findings.forEach((item, i) => {
    console.log(`  ${i + 1}. ${item.key}`);
    console.log(`     当前值: ${item.current}`);
    console.log(`     建议值: ${item.suggested}`);
    console.log(`     原因: ${item.reason}`);
    console.log(`     建议操作: ${item.action}`);
    console.log('');
  });

  console.log('当前为只读检查模式，不会自动修改配置文件\n');
  return true;
}

// 执行官方深度审计
function runSecurityAudit(hasFindings) {
  if (hasFindings) {
    console.log('\n已输出风险项，继续执行官方深度审计进行补充检查...\n');
  } else {
    console.log('\n配置已确认安全，执行官方深度审计进行全面检查...\n');
  }

  console.log('='.repeat(60));
  console.log('🔍 OpenClaw 官方深度安全审计');
  console.log('='.repeat(60) + '\n');

  try {
    // 检查 openclaw 命令是否可用
    execSync('openclaw --version', { stdio: 'pipe' });
  } catch (e) {
    console.error('未找到 openclaw 命令，请确保已安装 OpenClaw');
    return;
  }

  try {
    const output = execSync('openclaw security audit --deep', {
      encoding: 'utf8',
      timeout: 120000
    });
    console.log(output);
  } catch (e) {
    if (e.stdout) {
      console.log(e.stdout);
    }
    if (e.stderr) {
      console.error('审计错误:', e.stderr);
    }
  }
}

// 主函数
function main() {
  console.log('\nOpenClaw 安全检查工具');
  console.log('========================================\n');

  const configPath = getConfigPath();
  console.log('配置文件:', configPath);

  // 读取配置
  const config = readConfig(configPath);
  console.log('配置文件读取成功\n');

  // 检查配置
  const findings = checkConfig(config);

  // 打印检查结果
  const hasFindings = printFindings(findings);

  // 执行官方深度审计
  runSecurityAudit(hasFindings);

  console.log('\n' + '='.repeat(60));
  console.log('安全检查完成');
  console.log('='.repeat(60) + '\n');
}

// 运行
main();