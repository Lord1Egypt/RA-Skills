#!/usr/bin/env node
import fs from 'node:fs';

/**
 * Build sales-friendly summary markdown from capture manifest.
 */
export function buildSummaryMarkdown(manifest) {
  const date = manifest.date;
  const lines = [];
  lines.push(`# OpenRouter 模型排名日报（${date}）`);
  lines.push('');
  lines.push(
    '> 数据来源：[OpenRouter Rankings](https://openrouter.ai/rankings)。以下为各使用场景下**过去一周** token 使用占比排名（Top 5），便于销售同学快速了解客户可能关心的模型趋势。',
  );
  lines.push('');

  lines.push('## 一、给销售同学的 3 句话摘要');
  lines.push('');
  const cats = (manifest.categoryScenarios || []).filter((c) => c.ok && c.rankings?.length);
  if (cats.length > 0) {
    const prog = cats.find((c) => c.scenario === 'Programming') || cats[0];
    const top = prog.rankings[0];
    lines.push(`1. **编程场景**当前第一名是 **${top.model}**（${top.share || '份额见下图'}），适合向有代码/开发需求的客户推荐。`);
    const role = cats.find((c) => c.scenario === 'Roleplay');
    if (role?.rankings?.[0]) {
      lines.push(`2. **角色扮演场景**领先模型为 **${role.rankings[0].model}**（${role.rankings[0].share || ''}）。`);
    }
    lines.push(`3. 本文档含 **${cats.length} 个业务场景**的完整截图与排名，可直接转发客户或用于内部晨会。`);
  } else {
    lines.push('1. 今日已抓取 OpenRouter 排名页各板块截图，详见下方。');
    lines.push('2. Categories 场景数据解析失败时请重新运行截图脚本。');
    lines.push('3. 图表反映的是 OpenRouter 平台真实 token 使用占比，非主观评测。');
  }
  lines.push('');

  lines.push('## 二、各业务场景 Top 5（Categories）');
  lines.push('');
  for (const cat of cats) {
    lines.push(`### ${cat.scenario}`);
    lines.push('');
    lines.push('| 排名 | 模型 | 提供商 | 用量 | 占比 |');
    lines.push('| --- | --- | --- | --- | --- |');
    for (const r of cat.rankings.slice(0, 5)) {
      lines.push(`| ${r.rank} | ${r.model} | ${r.provider || '-'} | ${r.volume || '-'} | ${r.share || '-'} |`);
    }
    lines.push('');
  }

  lines.push('## 三、页面其他板块说明');
  lines.push('');
  const others = (manifest.sections || []).filter((s) => s.ok && !s.scenario);
  for (const s of others) {
    lines.push(`- **${s.heading}**：见文档内对应截图。`);
  }
  lines.push('');
  lines.push('---');
  lines.push(`*生成时间：${manifest.capturedAt}*`);

  return lines.join('\n');
}

/** Short text for Feishu chat (no file paths). */
export function buildChatSummary(manifest) {
  const cats = (manifest.categoryScenarios || []).filter((c) => c.ok && c.rankings?.length);
  const prog = cats.find((c) => c.scenario === 'Programming');
  const lines = [
    `📊 OpenRouter 排名日报（${manifest.date}）已生成，详见飞书文档链接。`,
    '',
    '**今日要点（给销售）：**',
  ];
  const highlights = ['Programming', 'Roleplay', 'Marketing', 'Legal']
    .map((s) => cats.find((c) => c.scenario === s))
    .filter(Boolean);
  for (const cat of highlights.slice(0, 3)) {
    const t = cat.rankings[0];
    if (t) lines.push(`• **${cat.scenario}** 场景第 1 名：**${t.model}**（${t.share || '见文档'}）`);
  }
  lines.push(`• 共收录 **${cats.length}** 个业务场景截图 + 页面其他排名板块`);
  lines.push('');
  lines.push('👇 点击下方文档查看全部截图与详细表格。');
  return lines.join('\n');
}

export function writeSummary(manifest, summaryPath) {
  const md = buildSummaryMarkdown(manifest);
  fs.writeFileSync(summaryPath, md, 'utf8');
  const chatPath = summaryPath.replace(/\.md$/, '-chat.txt');
  fs.writeFileSync(chatPath, buildChatSummary(manifest), 'utf8');
  return { summaryPath, chatPath };
}

if (process.argv[1]?.endsWith('generate-summary.mjs')) {
  const manifestPath = process.argv[2];
  if (!manifestPath) {
    console.error('Usage: node generate-summary.mjs <manifest.json>');
    process.exit(1);
  }
  const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
  const out = manifestPath.replace(/manifest\.json$/, 'summary.md');
  writeSummary(manifest, out);
  console.log('Wrote', out);
}
