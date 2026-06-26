/**
 * 格式化模块
 */

export function checkRelevance(title, content, keywords) {
  const text = `${title} ${content}`.toLowerCase();
  for (const keyword of keywords) {
    if (text.includes(keyword.toLowerCase())) return true;
  }
  return false;
}

export function assessPriority(title, content) {
  const text = `${title} ${content}`.toLowerCase();
  const highKeywords = ["发布", "推出", "融资", "收购", "重大突破", "上市", "合作"];
  for (const kw of highKeywords) {
    if (text.includes(kw)) return "高";
  }
  const mediumKeywords = ["更新", "升级", "应用", "案例", "报告", "分析"];
  for (const kw of mediumKeywords) {
    if (text.includes(kw)) return "中";
  }
  return "低";
}

export function parseResults(results, keywords) {
  const articles = [];
  const today = new Date().toISOString().split('T')[0];
  const seen = new Set();
  
  for (const item of results) {
    if (seen.has(item.url) || item.title.length < 10) continue;
    seen.add(item.url);
    
    if (!checkRelevance(item.title, item.snippet, keywords)) continue;
    
    let source = "";
    try {
      source = new URL(item.url).hostname.replace(/^www\./, '');
    } catch (e) {
      source = "未知来源";
    }
    
    articles.push({
      title: item.title,
      source,
      url: item.url,
      date: item.date || today,
      summary: truncate(item.snippet, 50) || "待验证",
      priority: assessPriority(item.title, item.snippet)
    });
  }
  
  return articles;
}

export function formatMessage(items, outputConfig) {
  const today = new Date().toLocaleDateString('zh-CN');
  const title = outputConfig?.title || "🌅 晨间资讯简报";
  
  let msg = `${title} - ${today}\n`;
  msg += `━━━━━━━━━━━━━━━━━━━━━━\n\n`;
  
  if (items.length === 0) {
    msg += `⚠️ 今日暂无匹配资讯\n\n`;
  } else {
    items.forEach((item, i) => {
      const priority = item.priority === "高" ? "🔴高" : item.priority === "中" ? "🟡中" : "🟢低";
      msg += `${i + 1}. 【${item.source}】\n`;
      msg += `标题：${item.title}\n`;
      msg += `链接：${item.url}\n`;
      msg += `日期：${item.date}\n`;
      msg += `摘要：${item.summary}\n`;
      msg += `优先级：${priority}\n\n`;
    });
  }
  
  msg += `━━━━━━━━━━━━━━━━━━━━━━\n`;
  msg += `💡 共 ${items.length} 条资讯\n`;
  msg += `⏰ 每日早7点自动推送\n`;
  
  return msg;
}

function truncate(str, maxLen) {
  if (!str) return "";
  if (str.length <= maxLen) return str;
  return str.substring(0, maxLen - 2) + "..";
}
