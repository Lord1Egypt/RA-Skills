#!/usr/bin/env node
/**
 * news-digest.mjs — 一键入口：抓取多主题新闻 + 发飞书卡片
 *
 * Usage:
 *   node news-digest.mjs \
 *     --topics "全球AI科技,时政要闻" \
 *     --counts "5,5" \
 *     --categories "AI,GEO" \
 *     --title "🗞️ AI新闻日报" \
 *     --target-user ou_xxx
 *
 * 单主题：
 *   node news-digest.mjs \
 *     --topics "MLB道奇最新战报" \
 *     --categories "SPORT" \
 *     --title "⚾ 道奇战报"
 */

import { execSync } from 'child_process';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __dir = dirname(fileURLToPath(import.meta.url));

function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    if (arg.startsWith('--')) {
      const key = arg.slice(2);
      const next = argv[i + 1];
      if (next && !next.startsWith('--')) { args[key] = next; i++; }
      else args[key] = true;
    }
  }
  return args;
}

function today() {
  return new Date().toLocaleDateString('zh-CN', {
    timeZone: 'Asia/Shanghai',
    year: 'numeric', month: '2-digit', day: '2-digit',
  }).replace(/\//g, '-');
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const {
    topics: topicsStr,
    counts: countsStr = '5',
    categories: catsStr = 'AI',
    title,
    'target-user': targetUser,
    'no-insight': noInsight,
    'dry-run': dryRun,
    date: dateStr = today(),
  } = args;

  if (!topicsStr) {
    console.error('❌ 缺少 --topics 参数\n示例: --topics "全球AI科技,时政要闻"');
    process.exit(1);
  }

  const topics = topicsStr.split(',').map(s => s.trim());
  const counts = countsStr.split(',').map(s => parseInt(s.trim()) || 5);
  const cats = catsStr.split(',').map(s => s.trim().toUpperCase());

  const sections = [];
  const fetchScript = join(__dir, 'fetch-news.mjs');

  for (let i = 0; i < topics.length; i++) {
    const topic = topics[i];
    const count = counts[i] || counts[0] || 5;
    const category = cats[i] || cats[0] || 'AI';

    console.log(`\n[${i+1}/${topics.length}] 处理「${topic}」...`);

    try {
      const envStr = [
        process.env.PERPLEXITY_API_KEY ? `PERPLEXITY_API_KEY=${process.env.PERPLEXITY_API_KEY}` : '',
        process.env.PPIO_API_KEY ? `PPIO_API_KEY=${process.env.PPIO_API_KEY}` : '',
        process.env.HTTPS_PROXY ? `HTTPS_PROXY=${process.env.HTTPS_PROXY}` : '',
      ].filter(Boolean).join(' ');

      const insightFlag = noInsight ? '--no-insight' : '';
      const cmd = `${envStr} node "${fetchScript}" --topic "${topic}" --count ${count} --category ${category} --date "${dateStr}" --output json ${insightFlag}`;
      const raw = execSync(cmd, { timeout: 120000, env: process.env }).toString().trim();

      // fetch-news 输出 JSON
      const data = JSON.parse(raw);
      sections.push({
        topic: `${getCategoryLabel(category)} ${topic}`,
        items: data.items || [],
      });
      console.log(`  ✓ ${data.items?.length || 0} 条`);
    } catch (e) {
      console.warn(`  ⚠️ 「${topic}」获取失败: ${e.message.slice(0, 80)}`);
      // 失败不中断，继续下一个主题
    }
  }

  if (sections.length === 0 || sections.every(s => s.items.length === 0)) {
    console.error('❌ 所有主题均获取失败');
    process.exit(1);
  }

  const totalItems = sections.reduce((s, sec) => s + sec.items.length, 0);
  const cardTitle = title || `🗞️ 新闻日报 | ${dateStr}`;
  const subtitle = `共 **${totalItems}** 条精选，${dateStr} 联网实时搜索`;

  console.log(`\n📤 构建卡片（${sections.length} 个主题，${totalItems} 条新闻）...`);

  const sendScript = join(__dir, 'send-card.mjs');
  const sectionsJson = JSON.stringify(sections).replace(/'/g, "'\\''");
  const userFlag = targetUser ? `--target-user "${targetUser}"` : '';
  const dryFlag = dryRun ? '--dry-run' : '';

  const sendCmd = `FEISHU_APP_ID=${process.env.FEISHU_APP_ID} FEISHU_APP_SECRET=${process.env.FEISHU_APP_SECRET} TARGET_USER_ID=${process.env.TARGET_USER_ID || ''} node "${sendScript}" --title "${cardTitle}" --subtitle "${subtitle}" --json '${sectionsJson}' ${userFlag} ${dryFlag}`;

  const result = execSync(sendCmd, { timeout: 30000, env: process.env }).toString();
  console.log(result);
}

function getCategoryLabel(cat) {
  const map = { AI: '🤖', GEO: '🌍', SPORT: '🏆', BIZ: '💼', CUSTOM: '📌' };
  return map[cat] || '📰';
}

main().catch(e => { console.error('❌', e.message); process.exit(1); });
