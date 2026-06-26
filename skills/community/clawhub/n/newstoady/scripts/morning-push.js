#!/usr/bin/env node
/**
 * NewsToday — 早报 prompt 生成器
 * 由 openclaw cron 驱动，每日 08:00 执行
 * 无文件 I/O：所有个性化参数由 push-toggle.js 在设置 cron 时嵌入命令行。
 *
 * 用法:
 *   node morning-push.js [--lang zh|en] [--topics 科技,财经,国际]
 */

// 允许的话题白名单
const ALLOWED_TOPICS = new Set(['科技','财经','国际','社会','娱乐','体育','tech','finance','international','society','entertainment','sports']);

const args = process.argv.slice(2);

const langIdx = args.indexOf('--lang');
const rawLang = langIdx !== -1 ? args[langIdx + 1] : null;
const lang = rawLang === 'en' ? 'en' : 'zh';

const topicsIdx = args.indexOf('--topics');
const rawTopics = topicsIdx !== -1 ? args[topicsIdx + 1] : null;
// 仅保留白名单内的话题，过滤任意外部输入
const topicList = rawTopics
  ? rawTopics.split(',').map(t => t.trim()).filter(t => ALLOWED_TOPICS.has(t))
  : [];

const now = new Date();
const dateISO = `${now.getFullYear()}-${String(now.getMonth()+1).padStart(2,'0')}-${String(now.getDate()).padStart(2,'0')}`;

if (lang === 'zh') {
  const WEEKDAYS = ['星期日','星期一','星期二','星期三','星期四','星期五','星期六'];
  const dateStr = `${now.getFullYear()}年${now.getMonth()+1}月${now.getDate()}日 ${WEEKDAYS[now.getDay()]}`;

  const topicHint = topicList.length
    ? `\n用户重点关注：${topicList.join('、')}（优先多选这些领域的新闻）。`
    : '';

  console.log(`请生成今日个性化早报。当前日期：${dateStr}${topicHint}

信息来源（按优先级）：
1. 【WebSearch 主源】
   - 搜索「今日重要新闻 ${dateISO}」
   - 搜索「今日国际新闻 ${dateISO}」
   - 搜索「今日财经新闻 ${dateISO}」
2. 【RSS 补充】可运行 node scripts/rss-fetch.js --lang zh 获取 RSS 源列表

处理要求：
- 去重后选取 10 条，覆盖不同领域（重要/财经/国际/科技/社会各至少 1 条）
- 第1条为【头条】：重要性最高的单条新闻，含标题、来源、时间、3-4句详细摘要、影响分析
- 其余9条为常规条目：标题、来源媒体、发布时间、2句摘要
- 财经类每条额外标注影响评级：📈 利好 / 📉 利空 / ➡️ 中性
- 按领域分组，每条标注话题标签
- 有争议内容保持中立，标注多方视角
- 统计总条数和预估阅读时长（每条约30秒）

输出格式：
📰 今日早报 · ${dateStr} | 10条 · 阅读约5分钟
━━━━━━━━━━━━━━━━━━━━━━━

🔥 头条
[头条新闻 — 标题加粗，3-4句详细摘要，含影响分析]

━━━━━━━━━━━━━━━━━━━━━━━

🔴 重要
[新闻条目]

💰 财经  （每条含 📈/📉/➡️ 评级）
[新闻条目]

🌍 国际
[新闻条目]

💻 科技
[新闻条目]

🏙️ 社会
[新闻条目]

━━━━━━━━━━━━━━━━━━━━━━━
💡 回复序号深读 · 回复"热榜"查看实时热搜 · 晚报20:00见`);

} else {
  const WEEKDAYS_EN = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
  const MONTHS_EN = ['January','February','March','April','May','June','July','August','September','October','November','December'];
  const dateStr = `${WEEKDAYS_EN[now.getDay()]}, ${MONTHS_EN[now.getMonth()]} ${now.getDate()}, ${now.getFullYear()}`;

  const topicHint = topicList.length
    ? `\nUser's priority topics: ${topicList.join(', ')} — prefer these categories.`
    : '';

  console.log(`Please generate today's personalized morning news briefing. Date: ${dateStr}${topicHint}

Sources (in priority order):
1. [WebSearch main]
   - Search "top news today ${dateISO}"
   - Search "international news today ${dateISO}"
   - Search "financial news today ${dateISO}"
2. [RSS supplement] Run node scripts/rss-fetch.js --lang en for RSS feed list

Requirements:
- After deduplication, select 10 stories covering different categories
- Story #1 is the [Lead Story]: highest-importance single item, with headline, source, time, 3-4 sentence detailed summary, and impact analysis
- Remaining 9 are standard entries: headline, source, publish time, 2-sentence summary
- Finance entries must include an impact tag: 📈 bullish / 📉 bearish / ➡️ neutral
- Group by category, tag each story
- Present disputed topics neutrally with multiple perspectives
- Count total stories and estimate reading time (~30 sec per story)

Output format:
📰 Morning Briefing · ${dateStr} | 10 stories · ~5 min read
━━━━━━━━━━━━━━━━━━━━━━━

🔥 Lead Story
[Top story — bold headline, 3-4 sentence detailed summary with impact analysis]

━━━━━━━━━━━━━━━━━━━━━━━

🔴 Top Stories
[entries]

💰 Finance  (each with 📈/📉/➡️ rating)
[entries]

🌍 International
[entries]

💻 Tech
[entries]

🏙️ Society
[entries]

━━━━━━━━━━━━━━━━━━━━━━━
💡 Reply a number to deep-read · Reply "trending" for hot topics · Evening recap at 8 PM`);
}
