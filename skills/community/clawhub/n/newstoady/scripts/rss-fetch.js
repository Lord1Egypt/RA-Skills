#!/usr/bin/env node
/**
 * NewsToday — RSS 聚合 prompt 生成器
 * 纯 CLI 参数输入 → stdout 输出，无任何文件 I/O 或网络调用。
 * 所有 URL 均为硬编码公开地址，不受外部输入影响。
 *
 * 用法:
 *   node rss-fetch.js [--lang zh|en] [--topics 科技,财经,国际]
 *
 * 示例:
 *   node rss-fetch.js --lang zh --topics 科技,财经
 *   node rss-fetch.js --lang en --topics tech,finance
 *   node rss-fetch.js                      # 使用默认值（中文，全部话题）
 */

// 全部 RSS 源均为硬编码公开地址，不受任何外部输入影响
const RSS_SOURCES_ZH = {
  综合: [
    { name: '新浪新闻头条', url: 'https://rss.sina.com.cn/news/china/focus15.xml' },
    { name: '澎湃新闻',     url: 'https://www.thepaper.cn/rss_promotion.jsp' },
  ],
  科技: [
    { name: '36氪',   url: 'https://36kr.com/feed' },
    { name: '少数派', url: 'https://sspai.com/feed' },
  ],
  财经: [
    { name: '华尔街见闻', url: 'https://wallstreetcn.com/rss' },
  ],
  国际: [
    { name: 'BBC中文',     url: 'https://feeds.bbci.co.uk/zhongwen/simp/rss.xml' },
    { name: 'Reuters中文', url: 'https://cn.reuters.com/rssFeed/CNTopNews' },
  ],
};

const RSS_SOURCES_EN = {
  general: [
    { name: 'Reuters',    url: 'https://feeds.reuters.com/reuters/topNews' },
    { name: 'BBC News',   url: 'http://feeds.bbci.co.uk/news/rss.xml' },
    { name: 'AP News',    url: 'https://rsshub.app/apnews/topics/apf-topnews' },
  ],
  tech: [
    { name: 'Hacker News', url: 'https://news.ycombinator.com/rss' },
    { name: 'TechCrunch',  url: 'https://techcrunch.com/feed/' },
  ],
  finance: [
    { name: 'Financial Times', url: 'https://www.ft.com/rss/home' },
    { name: 'Bloomberg',       url: 'https://feeds.bloomberg.com/markets/news.rss' },
  ],
};

// 允许的话题白名单（防止任意字符串进入输出）
const ALLOWED_ZH = new Set(['综合', '科技', '财经', '国际', '社会', '娱乐', '体育']);
const ALLOWED_EN = new Set(['general', 'tech', 'finance', 'international', 'society', 'entertainment', 'sports']);
const EN_TO_ZH_KEY = { tech: '科技', finance: '财经', international: '国际', general: '综合' };

// --- 解析 CLI 参数（仅接受 --lang 和 --topics）---
const args = process.argv.slice(2);

const langIdx = args.indexOf('--lang');
const rawLang = langIdx !== -1 ? args[langIdx + 1] : null;
const lang = rawLang === 'en' ? 'en' : 'zh'; // 仅允许 zh/en，其余默认 zh

const topicsIdx = args.indexOf('--topics');
const rawTopics = topicsIdx !== -1 ? args[topicsIdx + 1] : null;

// 将 --topics 参数解析为白名单内的话题集合
const allowedSet = lang === 'en' ? ALLOWED_EN : ALLOWED_ZH;
let requestedTopics = null; // null = 全部
if (rawTopics) {
  requestedTopics = new Set(
    rawTopics.split(',')
      .map(t => t.trim())
      .filter(t => allowedSet.has(t))
  );
}

// --- 从硬编码常量中选取 RSS 源 ---
const sources = lang === 'en' ? RSS_SOURCES_EN : RSS_SOURCES_ZH;
const generalKey = lang === 'en' ? 'general' : '综合';
const selected = [];

for (const [key, feeds] of Object.entries(sources)) {
  if (key === generalKey) {
    selected.push(...feeds); // 综合/general 始终包含
    continue;
  }
  // 无过滤要求，或该话题在请求列表中
  if (!requestedTopics) {
    selected.push(...feeds);
  } else {
    const zhKey = lang === 'en' ? (EN_TO_ZH_KEY[key] ?? key) : key;
    if (requestedTopics.has(key) || requestedTopics.has(zhKey)) {
      selected.push(...feeds);
    }
  }
}

// --- 输出 prompt ---
const now = new Date();
const dateISO = `${now.getFullYear()}-${String(now.getMonth()+1).padStart(2,'0')}-${String(now.getDate()).padStart(2,'0')}`;

if (lang === 'zh') {
  const sourceList = selected.map(s => `  - ${s.name}：${s.url}`).join('\n');
  console.log(`请通过 WebFetch 获取以下 RSS 源的最新内容，汇总今日（${dateISO}）重要新闻。

RSS 源列表：
${sourceList}

处理步骤：
1. 依次 WebFetch 以上每个 URL，获取 XML 内容
2. 从每个源提取最新 3-5 条标题和摘要（优先今日内容）
3. 全部去重合并，按新闻价值排序，选取 10 条
4. 每条输出：标题、来源、发布时间、2 句中文摘要

注意：
- 若某 RSS URL 无法访问，跳过并继续其他源
- 去除广告、软文、纯娱乐八卦内容
- 有争议内容保持中立，不做立场判断`);
} else {
  const sourceList = selected.map(s => `  - ${s.name}: ${s.url}`).join('\n');
  console.log(`Please WebFetch the following RSS feeds and compile today's (${dateISO}) top news.

RSS sources:
${sourceList}

Steps:
1. WebFetch each URL above to get the XML content
2. Extract the latest 3–5 headlines and summaries from each (prefer today's content)
3. Deduplicate and merge all results, rank by news value, pick top 10
4. For each item output: headline, source, publish time, 2-sentence English summary

Notes:
- If a URL is unreachable, skip and continue with others
- Filter out ads, sponsored content, and pure celebrity gossip
- Present disputed topics neutrally without taking sides`);
}
