#!/usr/bin/env node
/**
 * NewsToday — 突发新闻检测 prompt 生成器
 * 由 openclaw cron 每 2 小时执行（08:00-22:00）
 * 无文件 I/O：所有参数由 push-toggle.js 在设置 cron 时嵌入命令行。
 * 只有检测到重大突发新闻时，Claude 才发送提醒（否则静默）。
 *
 * 用法:
 *   node breaking-alert.js [--lang zh|en] [--topics 科技,财经,国际]
 */

const ALLOWED_TOPICS = new Set(['科技','财经','国际','社会','娱乐','体育','tech','finance','international','society','entertainment','sports']);

const args = process.argv.slice(2);

const langIdx = args.indexOf('--lang');
const rawLang = langIdx !== -1 ? args[langIdx + 1] : null;
const lang = rawLang === 'en' ? 'en' : 'zh';

const topicsIdx = args.indexOf('--topics');
const rawTopics = topicsIdx !== -1 ? args[topicsIdx + 1] : null;
const topicList = rawTopics
  ? rawTopics.split(',').map(t => t.trim()).filter(t => ALLOWED_TOPICS.has(t))
  : [];

const now = new Date();
const dateISO = `${now.getFullYear()}-${String(now.getMonth()+1).padStart(2,'0')}-${String(now.getDate()).padStart(2,'0')}`;
const timeStr = `${String(now.getHours()).padStart(2,'0')}:${String(now.getMinutes()).padStart(2,'0')}`;

if (lang === 'zh') {
  const topicHint = topicList.length
    ? `用户重点关注领域：${topicList.join('、')}，优先检测这些领域的突发事件。`
    : '';

  console.log(`请检测当前是否有重大突发新闻，仅在有真正重要的突发事件时才发送提醒。

当前时间：${dateISO} ${timeStr}
${topicHint}

检测步骤：
1. 搜索「突发新闻 ${dateISO}」
2. 搜索「今日重大事件 最新」
3. 如话题包含财经，额外搜索「市场暴跌 OR 股市熔断 ${dateISO}」
4. 如话题包含国际，额外搜索「国际突发 ${dateISO}」

判断标准（满足以下任一条才发送提醒）：
- 自然灾害：7级以上地震、大型台风、洪灾
- 重大事故：重大交通/安全事故，伤亡较大
- 金融市场：主要指数单日跌幅 >5%，或熔断
- 政治外交：重大政策发布、外交冲突升级
- 公共卫生：疫情爆发、重大食品安全事件
- 科技事件：重大数据泄露、主流平台大规模宕机

如果没有符合标准的突发事件：输出一个空行，不发送任何内容。

如果有符合标准的突发事件，按以下格式输出：
🚨 突发 · ${timeStr}
━━━━━━━━━━━━━━━━━━━━━━━
[事件标题]

[3-4句描述：什么事、哪里、影响范围、最新进展]

📌 来源：[媒体名称]
💡 回复"追踪"获取持续更新`);

} else {
  const topicHint = topicList.length
    ? `User's priority topics: ${topicList.join(', ')}. Focus detection on these areas.`
    : '';

  console.log(`Check for major breaking news right now. Only send an alert if there is a genuinely significant breaking event.

Current time: ${dateISO} ${timeStr}
${topicHint}

Detection steps:
1. Search "breaking news ${dateISO}"
2. Search "major event today latest"
3. If topics include finance, also search "market crash OR circuit breaker ${dateISO}"
4. If topics include international, also search "international breaking news ${dateISO}"

Alert criteria (send only if at least one applies):
- Natural disaster: magnitude 7+ earthquake, major hurricane/typhoon, severe flooding
- Major accident: significant casualties in transport or industrial accident
- Financial markets: major index drops >5% in a day, or trading halt triggered
- Politics/diplomacy: major policy announcement, significant escalation
- Public health: disease outbreak, major food safety incident
- Tech: large-scale data breach, major platform outage

If no qualifying breaking event found: output a single blank line. Send nothing.

If a qualifying breaking event is found:
🚨 Breaking · ${timeStr}
━━━━━━━━━━━━━━━━━━━━━━━
[Event headline]

[3–4 sentences: what happened, where, scale, latest update]

📌 Source: [media name]
💡 Reply "track" for continuous updates`);
}
