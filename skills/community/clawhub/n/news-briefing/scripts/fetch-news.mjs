#!/usr/bin/env node
/**
 * fetch-news.mjs — 通用新闻抓取模块
 *
 * 用 Perplexity sonar 搜索指定主题新闻，
 * 可选用 PPIO Claude 生成 AI 洞察。
 * 支持输出 JSON（供 send-card 合并）或直接发飞书卡片。
 *
 * Usage:
 *   node fetch-news.mjs --topic "全球AI科技" --count 5
 *   node fetch-news.mjs --topic "体育资讯" --count 3 --output json
 */

import { execSync } from 'child_process';
import { writeFileSync } from 'fs';

// ─── helpers ────────────────────────────────────────────────────────────────

function today() {
  return new Date().toLocaleDateString('zh-CN', {
    timeZone: 'Asia/Shanghai',
    year: 'numeric', month: '2-digit', day: '2-digit',
  }).replace(/\//g, '-');
}

function parseArgs(argv) {
  const args = { count: 5, category: 'AI', output: 'feishu', insight: true };
  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    if (arg.startsWith('--')) {
      const key = arg.slice(2);
      const next = argv[i + 1];
      if (key === 'no-insight') { args.insight = false; continue; }
      if (next && !next.startsWith('--')) { args[key] = next; i++; }
      else args[key] = true;
    }
  }
  return args;
}

function curlPost(url, headers, body, proxy, timeoutMs = 30000) {
  const headerArgs = Object.entries(headers).map(([k, v]) => `-H "${k}: ${v}"`).join(' ');
  const proxyArg = proxy ? `--proxy ${proxy}` : '';
  const escaped = JSON.stringify(body).replace(/'/g, "'\\''");
  const cmd = `curl -s --max-time ${Math.floor(timeoutMs / 1000)} ${proxyArg} -X POST "${url}" ${headerArgs} -d '${escaped}'`;
  return JSON.parse(execSync(cmd, { timeout: timeoutMs + 2000 }).toString());
}

// ─── Perplexity 搜索 ─────────────────────────────────────────────────────────

function fetchNewsRaw(apiKey, proxy, topic, count, dateStr) {
  const prompt = `${dateStr} ${topic} 最新${count}条重要新闻。

严格按此格式输出，每条用---分隔，禁止任何解释或前言：
TITLE: 新闻标题（必须是中文，简洁，不超过25字）
URL: 来源链接（真实可访问）
SUMMARY: 摘要（必须是中文，50-60字，含关键数字/人名，一句话说清核心事实，禁止废话）
---

重要：标题和摘要必须全部用中文表达，即使原始来源是英文或日文，也要翻译成中文输出。`;

  for (let attempt = 1; attempt <= 2; attempt++) {
    try {
      const data = curlPost(
        'https://api.perplexity.ai/chat/completions',
        { 'Content-Type': 'application/json', 'Authorization': `Bearer ${apiKey}` },
        { model: 'sonar', messages: [{ role: 'user', content: prompt }], max_tokens: 1500 },
        proxy,
        28000
      );
      const content = data.choices?.[0]?.message?.content;
      if (content && content.length > 50) {
        return content.replace(/\[\d+\]/g, '').replace(/\*\*/g, '').trim();
      }
    } catch (e) {
      console.warn(`  ⚠️ Perplexity 第${attempt}次失败: ${e.message.slice(0, 60)}`);
    }
  }
  return '';
}

// ─── 解析新闻条目 ────────────────────────────────────────────────────────────

function parseNewsItems(text, category) {
  const items = [];
  const blocks = text.split(/\n---+\n?/).map(b => b.trim()).filter(Boolean);
  for (const block of blocks) {
    const title = (block.match(/TITLE[：:]\s*(.+)/)?.[1] || '').trim();
    const url = (block.match(/URL[：:]\s*(https?:\/\/[^\s]+)/)?.[1] || '').trim();
    const summary = (block.match(/SUMMARY[：:]\s*([\s\S]+?)(?=\n[A-Z]|$)/)?.[1] || '')
      .replace(/\s+/g, ' ').trim();
    if (title && summary.length > 10) {
      items.push({ title, url, summary, category, insight: '' });
    }
  }
  return items;
}

// ─── AI 洞察生成 ─────────────────────────────────────────────────────────────

function generateInsight(ppioKey, proxy, title, summary) {
  if (!ppioKey) return '';
  try {
    const prompt = `你是资深分析师，对以下新闻做深度洞察（150字以内，格式严格如下）：

📌 背景：[为何发生]
🔍 深层逻辑：[核心驱动力]
💥 影响：[行业/市场影响]
👁 关注点：[值得追踪的信号]

禁止重复摘要内容，直接输出洞察。

标题：${title}
摘要：${summary}`;

    const escaped = JSON.stringify({
      model: 'pa/claude-haiku-4-5-20251001',
      messages: [{ role: 'user', content: prompt }],
      max_tokens: 400,
    }).replace(/'/g, "'\\''");
    const proxyArg = proxy ? `--proxy ${proxy}` : '';
    const cmd = `curl -s --max-time 20 ${proxyArg} -X POST "https://api.ppinfra.com/v3/openai/chat/completions" -H "Content-Type: application/json" -H "Authorization: Bearer ${ppioKey}" -d '${escaped}'`;
    const data = JSON.parse(execSync(cmd, { timeout: 22000 }).toString());
    return data.choices?.[0]?.message?.content?.trim() || '';
  } catch (e) {
    console.warn(`  ⚠️ 洞察生成失败: ${e.message.slice(0, 50)}`);
    return '';
  }
}

// ─── 主流程 ──────────────────────────────────────────────────────────────────

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const {
    topic, count, category, output,
    'output-file': outputFile,
    date: dateStr = today(),
    insight: genInsight,
  } = args;

  if (!topic) {
    console.error('❌ 缺少 --topic 参数');
    process.exit(1);
  }

  const apiKey = process.env.PERPLEXITY_API_KEY;
  const ppioKey = process.env.PPIO_API_KEY;
  const proxy = process.env.HTTPS_PROXY || process.env.https_proxy || '';

  if (!apiKey) { console.error('❌ 缺少 PERPLEXITY_API_KEY'); process.exit(1); }

  process.stderr.write(`🔍 搜索「${topic}」最新 ${count} 条新闻...\n`);
  const rawText = fetchNewsRaw(apiKey, proxy, topic, count, dateStr);

  if (!rawText) {
    process.stderr.write('❌ 新闻获取失败\n');
    process.exit(1);
  }

  const items = parseNewsItems(rawText, category.toUpperCase());
  process.stderr.write(`📋 解析到 ${items.length} 条新闻\n`);

  if (items.length === 0) {
    process.stderr.write('❌ 未解析到新闻条目\n原始输出: ' + rawText.slice(0, 300) + '\n');
    process.exit(1);
  }

  // 生成洞察
  if (genInsight && ppioKey) {
    process.stderr.write('🧠 生成 AI 洞察...\n');
    await Promise.all(items.map(async (item, i) => {
      item.insight = generateInsight(ppioKey, proxy, item.title, item.summary);
      if (item.insight) process.stderr.write(`  ✓ [${i+1}] ${item.title.slice(0, 25)}…\n`);
    }));
  }

  // 输出
  if (output === 'json') {
    const result = JSON.stringify({ topic, category, dateStr, items }, null, 2);
    if (outputFile) {
      writeFileSync(outputFile, result);
      console.log(`💾 已写入 ${outputFile}`);
    } else {
      process.stdout.write(result);
    }
  } else {
    // 直接输出到 stdout 供 send-card 读取
    process.stdout.write(JSON.stringify({ topic, category, dateStr, items }));
  }
}

main().catch(e => { console.error('❌', e.message); process.exit(1); });
