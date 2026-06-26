#!/usr/bin/env node
/**
 * 免 Key 网络搜索（嫁接层）
 * 用 DuckDuckGo Instant Answer API，无需注册。
 * OpenClaw agent 在 web_search 不可用时，可 exec 本脚本获取检索结果。
 *
 * 用法: node free_search.js "你的搜索词"
 * 或:   node free_search.js "搜索词" --json
 */

const query = process.argv[2];
if (!query || query.startsWith('-')) {
  console.error('用法: node free_search.js "搜索词" [--json]');
  process.exit(1);
}
const wantJson = process.argv.includes('--json');

const url = `https://api.duckduckgo.com/?q=${encodeURIComponent(query)}&format=json&no_html=1`;

async function main() {
  let data;
  try {
    const res = await fetch(url, {
      headers: { 'User-Agent': 'Mozilla/5.0 (compatible; OpenClaw/1.0)' },
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    data = await res.json();
  } catch (fetchErr) {
    // 国内可能无法直连 DuckDuckGo，尝试用 curl（会走系统代理若有）
    try {
      const { execFileSync } = require('child_process');
      const out = execFileSync('curl', ['-s', '-L', '--max-time', '15', url], {
        encoding: 'utf-8',
        maxBuffer: 1024 * 1024,
      });
      data = JSON.parse(out);
    } catch (curlErr) {
      console.error('搜索失败: 无法访问 DuckDuckGo（若在国内需代理或 VPN）', fetchErr?.message || fetchErr);
      process.exit(2);
    }
  }
  try {
    const out = {
      query: data.Heading || query,
      abstract: data.Abstract ? { text: data.Abstract, url: data.AbstractURL } : null,
      related: (data.RelatedTopics || [])
        .filter((r) => r.Text)
        .slice(0, 10)
        .map((r) => ({ text: r.Text, url: r.FirstURL || null })),
    };

    if (wantJson) {
      console.log(JSON.stringify(out, null, 2));
      return;
    }

    // 纯文本，方便 agent 直接读
    const lines = [];
    if (out.abstract) {
      lines.push('[摘要] ' + out.abstract.text);
      if (out.abstract.url) lines.push('链接: ' + out.abstract.url);
      lines.push('');
    }
    out.related.forEach((r, i) => {
      lines.push(`${i + 1}. ${r.text}`);
      if (r.url) lines.push('   ' + r.url);
    });
    console.log(lines.join('\n') || '未找到相关结果，可换关键词再试。');
  } catch (e) {
    console.error('解析失败:', e.message);
    process.exit(2);
  }
}

main();
