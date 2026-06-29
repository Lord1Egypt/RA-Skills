#!/usr/bin/env node
/**
 * competitor.js - 竞品监控独立模块
 * 
 * 功能:
 *   - 爬取竞品页面（可达性、关键词、排名变化）
 *   - 记录历史，检测变化
 *   - 输出告警
 * 
 * 用法:
 *   const checkCompetitors = require('./competitor.js');
 *   await checkCompetitors(config, lines, alerts);
 */

'use strict';

const https = require('https');
const http  = require('http');
const fs    = require('fs');
const path  = require('path');

// ── HTTP GET ──────────────────────────────────────────────────────────────
function httpGet(urlStr, timeoutMs) {
  return new Promise((resolve, reject) => {
    const url = new URL(urlStr);
    const lib = url.protocol === 'https:' ? https : http;
    const req = lib.get(urlStr, { timeout: timeoutMs, headers: { 'User-Agent': 'Mozilla/5.0 PlatformMonitor/1.1' } }, (res) => {
      const chunks = [];
      res.on('data', d => chunks.push(d));
      res.on('end', () => {
        resolve({ statusCode: res.statusCode, body: Buffer.concat(chunks).toString('utf8') });
      });
    });
    req.on('timeout', () => { req.destroy(); reject(new Error(`timeout after ${timeoutMs}ms`)); });
    req.on('error', reject);
  });
}

// ── 时间戳 ──────────────────────────────────────────────────────────────
function timestamp() {
  const d = new Date();
  const tz = 8;
  const local = new Date(d.getTime() + tz * 3600_000);
  return local.toISOString().replace('T', ' ').slice(0, 19).replace('Z', '');
}

// ── 主函数 ──────────────────────────────────────────────────────────────
async function checkCompetitors(config, lines, alerts) {
  if (!config.competitors || config.competitors.length === 0) {
    lines.push(`[${timestamp()}] 【竞品监控】未配置竞品列表，跳过`);
    return;
  }

  const historyFile = path.join(process.cwd(), 'platform_monitor_competitors.json');
  let history = {};
  try {
    if (fs.existsSync(historyFile)) {
      history = JSON.parse(fs.readFileSync(historyFile, 'utf8'));
    }
  } catch (e) {
    history = {};
  }

  lines.push(`[${timestamp()}] 【竞品监控】开始检查 ${config.competitors.length} 个竞品...`);

  for (const comp of config.competitors) {
    try {
      lines.push(`[${timestamp()}]   检查竞品: ${comp.name} (${comp.url})`);
      const res = await httpGet(comp.url, comp.timeoutMs || 15000);
      
      // 检测关键词
      const keywordFound = comp.expectKeyword ? res.body.includes(comp.expectKeyword) : true;
      const status = res.statusCode >= 200 && res.statusCode < 400 && keywordFound ? 'UP' : 'DEGRADED';
      
      const prev = history[comp.name];
      if (prev && prev.status !== status) {
        const msg = `⚠️ 【竞品状态变化】${comp.name}: ${prev.status} → ${status}`;
        lines.push(`[${timestamp()}]     ${msg}`);
        alerts.push(`[${timestamp()}] ${msg}`);
      }

      history[comp.name] = {
        status,
        lastCheck: timestamp(),
        url: comp.url
      };

      lines.push(`[${timestamp()}]     ✅ ${comp.name}: ${status}`);
    } catch (e) {
      const prev = history[comp.name];
      if (prev && prev.status !== 'DOWN') {
        const msg = `⚠️ 【竞品下线】${comp.name} 无法访问: ${e.message}`;
        lines.push(`[${timestamp()}]     ${msg}`);
        alerts.push(`[${timestamp()}] ${msg}`);
      }
      history[comp.name] = { status: 'DOWN', lastCheck: timestamp(), url: comp.url };
    }
    await new Promise(r => setTimeout(r, 1000));
  }

  // 保存历史
  try {
    fs.writeFileSync(historyFile, JSON.stringify(history, null, 2), 'utf8');
  } catch (e) {
    lines.push(`[${timestamp()}]   ⚠️  保存竞品历史失败: ${e.message}`);
  }

  lines.push(`[${timestamp()}] 【竞品监控】完成`);
}

module.exports = checkCompetitors;
