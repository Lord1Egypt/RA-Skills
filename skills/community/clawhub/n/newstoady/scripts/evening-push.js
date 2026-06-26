#!/usr/bin/env node
/**
 * NewsToday — 晚间推送 prompt 生成器
 * 由 openclaw cron 驱动，每日 20:00 执行
 * 无文件 I/O：所有个性化参数由 push-toggle.js 在设置 cron 时嵌入命令行。
 *
 * 用法:
 *   node evening-push.js [--lang zh|en] [--topics 科技,财经,国际]
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
const tomorrow = new Date(now);
tomorrow.setDate(tomorrow.getDate() + 1);

const dateISO = `${now.getFullYear()}-${String(now.getMonth()+1).padStart(2,'0')}-${String(now.getDate()).padStart(2,'0')}`;
const tomorrowISO = `${tomorrow.getFullYear()}-${String(tomorrow.getMonth()+1).padStart(2,'0')}-${String(tomorrow.getDate()).padStart(2,'0')}`;

if (lang === 'zh') {
  const WEEKDAYS = ['星期日','星期一','星期二','星期三','星期四','星期五','星期六'];
  const dateStr     = `${now.getFullYear()}年${now.getMonth()+1}月${now.getDate()}日 ${WEEKDAYS[now.getDay()]}`;
  const tomorrowStr = `${tomorrow.getMonth()+1}月${tomorrow.getDate()}日${WEEKDAYS[tomorrow.getDay()]}`;

  const topicHint = topicList.length
    ? `\n用户重点关注：${topicList.join('、')}，收官和预告请侧重这些领域。`
    : '';

  console.log(`请生成今日晚间新闻汇总与明日预告。当前日期：${dateStr}${topicHint}

执行步骤：
1. 搜索「今日晚间重要新闻 ${dateISO}」
2. 搜索「今日热点事件最新进展」
3. 搜索「${tomorrowISO} 重要日程 财经 政治 体育」

输出格式：
🌙 晚间快报 · ${dateStr}
━━━━━━━━━━━━━━━━━━━━━━━

📋 今日收官（3-5条下午/晚间重要新闻，每条附2句摘要及来源）

🔄 今日热点进展（1-2条今天持续发酵事件的最新动态）

📅 明日预告（${tomorrowStr}值得关注）
  · 重要会议 / 政策发布 / 赛事
  · 财经数据公布时间
  · 预计有进展的持续事件

━━━━━━━━━━━━━━━━━━━━━━━
💡 回复序号深读 · 明日早报08:00见`);

} else {
  const WEEKDAYS_EN = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
  const MONTHS_EN = ['January','February','March','April','May','June','July','August','September','October','November','December'];
  const dateStr     = `${WEEKDAYS_EN[now.getDay()]}, ${MONTHS_EN[now.getMonth()]} ${now.getDate()}, ${now.getFullYear()}`;
  const tomorrowStr = `${WEEKDAYS_EN[tomorrow.getDay()]}, ${MONTHS_EN[tomorrow.getMonth()]} ${tomorrow.getDate()}`;

  const topicHint = topicList.length
    ? `\nUser's priority topics: ${topicList.join(', ')} — weight recap and preview toward these.`
    : '';

  console.log(`Please generate the evening news recap and tomorrow's preview. Date: ${dateStr}${topicHint}

Steps:
1. Search "top news this evening ${dateISO}"
2. Search "today's major story latest update"
3. Search "${tomorrowISO} key events schedule finance politics sports"

Output format:
🌙 Evening Recap · ${dateStr}
━━━━━━━━━━━━━━━━━━━━━━━

📋 Today's wrap-up (3–5 significant afternoon/evening stories, each with 2-sentence summary and source)

🔄 Developing stories (1–2 ongoing stories with latest updates)

📅 Tomorrow's preview (${tomorrowStr})
  · Key meetings / policy announcements / sports events
  · Economic data releases
  · Expected developments in ongoing stories

━━━━━━━━━━━━━━━━━━━━━━━
💡 Reply a number to deep-read · Morning briefing tomorrow at 8 AM`);
}
