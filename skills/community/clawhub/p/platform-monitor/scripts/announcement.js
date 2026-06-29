#!/usr/bin/env node
/**
 * announcement.js - 公告监控完整版
 * 
 * 功能:
 *   1. 静态页面：用 axios + cheerio 爬取
 *   2. 动态页面：用 playwright 爬取（JS 渲染后的内容）
 *   3. 智能提取：公告标题、日期、链接
 *   4. 去重：避免重复推送
 * 
 * 用法:
 *   const checkAnnouncements = require('./announcement.js');
 *   await checkAnnouncements(config, lines, alerts);
 */

'use strict';

const fs   = require('fs');
const path = require('path');
const axios = require('axios');
const cheerio = require('cheerio');

// ── 时间戳 ──────────────────────────────────────────────────────────────
function timestamp() {
  return new Date().toISOString().replace('T', ' ').slice(0, 19);
}

// ── 静态页面爬取 ──────────────────────────────────────────────────────────
async function fetchStaticPage(url, timeoutMs = 15000) {
  const res = await axios.get(url, {
    timeout: timeoutMs,
    headers: { 'User-Agent': 'Mozilla/5.0 PlatformMonitor/2.0' }
  });
  return res.data;
}

// ── 动态页面爬取（playwright） ──────────────────────────────────────────
async function fetchDynamicPage(url, timeoutMs = 30000) {
  const { chromium } = require('playwright');
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  await page.goto(url, { timeout: timeoutMs, waitUntil: 'networkidle' });
  const content = await page.content();
  await browser.close();
  return content;
}

// ── 提取公告（通用） ──────────────────────────────────────────────────
function extractAnnouncements(html, config) {
  const $ = cheerio.load(html);
  const results = [];

  // 方法1：按配置的选择器提取
  if (config.selector) {
    $(config.selector).each((i, elem) => {
      const $elem = $(elem);
      const title = $elem.text().trim();
      const link = $elem.attr('href') || '';
      const date = $elem.attr('data-date') || '';
      if (title) results.push({ title, link, date });
    });
  }

  // 方法2：自动提取（找含有"公告"、"更新"等关键词的链接）
  if (results.length === 0) {
    $('a').each((i, elem) => {
      const $elem = $(elem);
      const title = $elem.text().trim();
      const link = $elem.attr('href') || '';
      if (title && /公告|更新|update|announcement|changelog/i.test(title)) {
        results.push({ title, link, date: '' });
      }
    });
  }

  return results;
}

// ── 主函数 ──────────────────────────────────────────────────────────────
async function checkAnnouncements(config, lines, alerts) {
  if (!config.announcements || config.announcements.length === 0) {
    lines.push(`[${timestamp()}] 【公告监控】未配置，跳过`);
    return;
  }

  const historyFile = path.join(process.cwd(), config.announcementHistoryFile || 'platform_monitor_announcements.json');
  let history = [];
  try { if (fs.existsSync(historyFile)) { history = JSON.parse(fs.readFileSync(historyFile, 'utf8')); } } catch { history = []; }

  lines.push(`[${timestamp()}] 【公告监控】检查 ${config.announcements.length} 个页面...`);

  for (const ann of config.announcements) {
    try {
      lines.push(`[${timestamp()}]   检查: ${ann.name} (${ann.url})`);
      
      let html = '';
      try {
        // 先试静态爬取
        html = await fetchStaticPage(ann.url, ann.timeoutMs || 15000);
      } catch (e) {
        // 静态失败，试动态爬取
        lines.push(`[${timestamp()}]     静态爬取失败，尝试动态爬取...`);
        html = await fetchDynamicPage(ann.url, ann.timeoutMs || 30000);
      }

      const items = extractAnnouncements(html, ann);
      if (items.length === 0) {
        lines.push(`[${timestamp()}]     ⚠️  未找到公告（可能需要调整选择器）`);
        continue;
      }

      const newItems = [];
      for (const item of items) {
        const exists = history.find(h => h.title === item.title && h.url === ann.url);
        if (!exists) {
          newItems.push(item);
          history.push({ title: item.title, url: ann.url, firstSeen: timestamp() });
        }
      }

      if (newItems.length > 0) {
        const msg = `📢 【新公告】${ann.name}: ${newItems.length} 条`;
        lines.push(`[${timestamp()}]     ✅ ${msg}`);
        alerts.push(msg);
        for (const item of newItems.slice(0, 5)) {
          lines.push(`[${timestamp()}]       - ${item.title}`);
        }
      } else {
        lines.push(`[${timestamp()}]     ✅ 无新公告`);
      }
    } catch (e) {
      lines.push(`[${timestamp()}]     ❌ 失败: ${e.message}`);
    }
    await new Promise(r => setTimeout(r, 1000));
  }

  try { fs.writeFileSync(historyFile, JSON.stringify(history, null, 2), 'utf8'); } catch (e) {}
  lines.push(`[${timestamp()}] 【公告监控】完成`);
}

module.exports = checkAnnouncements;
