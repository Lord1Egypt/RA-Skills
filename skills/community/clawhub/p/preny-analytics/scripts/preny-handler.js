/**
 * Preny Analytics - Natural Language Handler (Real API)
 * Xử lý câu hỏi tự nhiên và lấy dữ liệu từ Preny API
 */

const PRENY_API_BASE = process.env.PRENY_API_URL || 'https://api-production.prenychatbot.ai/api/v1';
const PRENY_TOKEN = process.env.PRENY_TOKEN;

// Intent patterns
const INTENTS = {
  STATS_TODAY: {
    patterns: [/thống kê hôm nay/i, /số liệu hôm nay/i, /hôm nay thế nào/i, /today stats/i, /stats today/i],
    handler: 'getStatsToday'
  },
  STATS_YESTERDAY: {
    patterns: [/thống kê hôm qua/i, /số liệu hôm qua/i, /hôm qua/i, /yesterday/i],
    handler: 'getStatsYesterday'
  },
  STATS_WEEK: {
    patterns: [/thống kê tuần/i, /tuần này/i, /7 ngày/i, /week stats/i, /tuần qua/i],
    handler: 'getStatsWeek'
  },
  STATS_MONTH: {
    patterns: [/thống kê tháng/i, /tháng này/i, /30 ngày/i, /month stats/i],
    handler: 'getStatsMonth'
  },
  CUSTOMERS: {
    patterns: [/bao nhiêu khách/i, /số khách hàng/i, /khách mới/i, /khách hôm nay/i, /tài khoản mới/i],
    handler: 'getCustomerStats'
  },
  MESSAGES: {
    patterns: [/tin nhắn/i, /message/i, /fanpage/i, /nhắn tin/i],
    handler: 'getMessageStats'
  },
  COMPARE: {
    patterns: [/so sánh/i, /so với/i, /compare/i, /tăng giảm/i, /chênh lệch/i],
    handler: 'getComparison'
  },
  SYSTEM_TAGS: {
    patterns: [/tag màu|tag hệ thống|trạng thái hệ thống|phân loại theo màu|thống kê màu|yellow|red|green|white/i],
    handler: 'getSystemTagStats'
  },
  TAGS: {
    patterns: [/tag khách|tags|phân loại khách|trạng thái khách|gắn tag khách|loại khách|khách đang chat|khách chốt|khách l1|crm/i],
    handler: 'getTagStats'
  }
};

// Date helpers
function getTodayRange() {
  const today = new Date();
  today.setUTCHours(0, 0, 0, 0);
  const from = today.toISOString();
  today.setUTCHours(23, 59, 59, 999);
  const to = today.toISOString();
  return { from, to };
}

function getYesterdayRange() {
  const yesterday = new Date();
  yesterday.setUTCDate(yesterday.getUTCDate() - 1);
  yesterday.setUTCHours(0, 0, 0, 0);
  const from = yesterday.toISOString();
  yesterday.setUTCHours(23, 59, 59, 999);
  const to = yesterday.toISOString();
  return { from, to };
}

function getWeekRange() {
  const to = new Date();
  to.setUTCHours(23, 59, 59, 999);
  const from = new Date();
  from.setUTCDate(from.getUTCDate() - 6);
  from.setUTCHours(0, 0, 0, 0);
  return { from: from.toISOString(), to: to.toISOString() };
}

function getMonthRange() {
  const to = new Date();
  to.setUTCHours(23, 59, 59, 999);
  const from = new Date();
  from.setUTCDate(from.getUTCDate() - 29);
  from.setUTCHours(0, 0, 0, 0);
  return { from: from.toISOString(), to: to.toISOString() };
}

// Format helpers
function formatNumber(num) {
  return num ? num.toLocaleString('vi-VN') : '0';
}

function formatCurrency(num) {
  return num ? num.toLocaleString('vi-VN') + ' VND' : '0 VND';
}

// API Call
async function callAPI(from, to, limit = 30) {
  const url = `${PRENY_API_BASE}/statistics/stats?from=${from}&to=${to}&skip=0&limit=${limit}&sort=-1&type=interact`;
  
  const response = await fetch(url, {
    method: 'GET',
    headers: {
      'Accept': 'application/json',
      'Authorization': `Bearer ${PRENY_TOKEN}`,
      'Content-Type': 'application/json'
    }
  });
  
  return response.json();
}

// Tags API Call
async function callTagsAPI(from, to) {
  const url = `${PRENY_API_BASE}/statistics/tag-attributes?from=${from}&to=${to}&skip=0&limit=50&sort=-1&type=status`;
  
  const response = await fetch(url, {
    method: 'GET',
    headers: {
      'Accept': 'application/json',
      'Authorization': `Bearer ${PRENY_TOKEN}`,
      'Content-Type': 'application/json'
    }
  });
  
  return response.json();
}

// System Tags API Call
async function callSystemTagsAPI(from, to) {
  const url = `${PRENY_API_BASE}/statistics/tag-default?from=${from}&to=${to}&sort=-1&type=tags`;
  
  const response = await fetch(url, {
    method: 'GET',
    headers: {
      'Accept': 'application/json',
      'Authorization': `Bearer ${PRENY_TOKEN}`,
      'Content-Type': 'application/json'
    }
  });
  
  return response.json();
}

// Detect intent
function detectIntent(message) {
  for (const [name, config] of Object.entries(INTENTS)) {
    for (const pattern of config.patterns) {
      if (pattern.test(message)) {
        return { name, handler: config.handler };
      }
    }
  }
  return null;
}

// Calculate summary
function calculateSummary(listData) {
  return {
    totalAccounts: listData.reduce((sum, d) => sum + (d.countNewAccounts || 0), 0),
    totalPhones: listData.reduce((sum, d) => sum + (d.countNewPhoneNumber || 0), 0),
    totalMessages: listData.reduce((sum, d) => sum + (d.messageByFanpage || 0), 0),
    totalComments: listData.reduce((sum, d) => sum + (d.userCommentPage || 0), 0),
    totalOld: listData.reduce((sum, d) => sum + (d.countOldCustomer || 0), 0),
    totalPageComments: listData.reduce((sum, d) => sum + (d.pageComment || 0), 0)
  };
}

// ===== HANDLERS =====

async function getStatsToday() {
  const { from, to } = getTodayRange();
  const response = await callAPI(from, to, 1);
  
  if (response.systemCode !== 'ACC_0000') {
    return `❌ Lỗi: ${response.message || 'Không thể lấy dữ liệu'}`;
  }
  
  const list = response.data?.listData || [];
  if (list.length === 0) {
    return `📊 Chưa có dữ liệu cho hôm nay`;
  }
  
  const s = calculateSummary(list);
  
  return `📊 THỐNG KÊ HÔM NAY
━━━━━━━━━━━━━━━━━━━━

👥 KHÁCH HÀNG
   Tài khoản mới:     ${formatNumber(s.totalAccounts)}
   SĐT mới:           ${formatNumber(s.totalPhones)}
   Khách quay lại:    ${formatNumber(s.totalOld)}

💬 TƯƠNG TÁC
   Tin nhắn Fanpage:  ${formatNumber(s.totalMessages)}
   Comment khách:     ${formatNumber(s.totalComments)}
   Comment trả lời:   ${formatNumber(s.totalPageComments)}`;
}

async function getStatsYesterday() {
  const { from, to } = getYesterdayRange();
  const response = await callAPI(from, to, 1);
  
  if (response.systemCode !== 'ACC_0000') {
    return `❌ Lỗi: ${response.message || 'Không thể lấy dữ liệu'}`;
  }
  
  const list = response.data?.listData || [];
  if (list.length === 0) {
    return `📊 Chưa có dữ liệu cho hôm qua`;
  }
  
  const s = calculateSummary(list);
  
  return `📊 THỐNG KÊ HÔM QUA
━━━━━━━━━━━━━━━━━━━━

👥 KHÁCH HÀNG
   Tài khoản mới:     ${formatNumber(s.totalAccounts)}
   SĐT mới:           ${formatNumber(s.totalPhones)}
   Khách quay lại:    ${formatNumber(s.totalOld)}

💬 TƯƠNG TÁC
   Tin nhắn Fanpage:  ${formatNumber(s.totalMessages)}
   Comment khách:     ${formatNumber(s.totalComments)}`;
}

async function getStatsWeek() {
  const { from, to } = getWeekRange();
  const response = await callAPI(from, to, 7);
  
  if (response.systemCode !== 'ACC_0000') {
    return `❌ Lỗi: ${response.message || 'Không thể lấy dữ liệu'}`;
  }
  
  const list = response.data?.listData || [];
  if (list.length === 0) {
    return `📊 Chưa có dữ liệu cho tuần này`;
  }
  
  const s = calculateSummary(list);
  
  let result = `📊 THỐNG KÊ 7 NGÀY QUA
━━━━━━━━━━━━━━━━━━━━

👥 KHÁCH HÀNG
   Tài khoản mới:     ${formatNumber(s.totalAccounts)}
   SĐT mới:           ${formatNumber(s.totalPhones)}
   Khách quay lại:    ${formatNumber(s.totalOld)}

💬 TƯƠNG TÁC
   Tin nhắn Fanpage:  ${formatNumber(s.totalMessages)}
   Comment khách:     ${formatNumber(s.totalComments)}

📅 CHI TIẾT THEO NGÀY
────────────────────────────────
${list.map(d => 
  `   ${d.date} | TK: ${formatNumber(d.countNewAccounts)} | Tin: ${formatNumber(d.messageByFanpage)}`
).join('\n')}`;
  
  return result;
}

async function getStatsMonth() {
  const { from, to } = getMonthRange();
  const response = await callAPI(from, to, 30);
  
  if (response.systemCode !== 'ACC_0000') {
    return `❌ Lỗi: ${response.message || 'Không thể lấy dữ liệu'}`;
  }
  
  const list = response.data?.listData || [];
  if (list.length === 0) {
    return `📊 Chưa có dữ liệu cho tháng này`;
  }
  
  const s = calculateSummary(list);
  
  return `📊 THỐNG KÊ 30 NGÀY QUA
━━━━━━━━━━━━━━━━━━━━

👥 KHÁCH HÀNG
   Tài khoản mới:     ${formatNumber(s.totalAccounts)}
   SĐT mới:           ${formatNumber(s.totalPhones)}
   Khách quay lại:    ${formatNumber(s.totalOld)}

💬 TƯƠNG TÁC
   Tin nhắn Fanpage:  ${formatNumber(s.totalMessages)}
   Comment khách:     ${formatNumber(s.totalComments)}

📊 Trung bình/ngày:
   TK mới: ${formatNumber(Math.round(s.totalAccounts / list.length))}
   Tin nhắn: ${formatNumber(Math.round(s.totalMessages / list.length))}`;
}

async function getCustomerStats() {
  const { from, to } = getTodayRange();
  const response = await callAPI(from, to, 1);
  
  if (response.systemCode !== 'ACC_0000') {
    return `❌ Lỗi: ${response.message || 'Không thể lấy dữ liệu'}`;
  }
  
  const list = response.data?.listData || [];
  const s = calculateSummary(list);
  
  return `👥 THỐNG KÊ KHÁCH HÀNG HÔM NAY
━━━━━━━━━━━━━━━━━━━━

• Tài khoản mới:     ${formatNumber(s.totalAccounts)}
• SĐT mới:           ${formatNumber(s.totalPhones)}
• Khách quay lại:    ${formatNumber(s.totalOld)}
• Tổng khách:        ${formatNumber(s.totalAccounts + s.totalOld)}`;
}

async function getMessageStats() {
  const { from, to } = getTodayRange();
  const response = await callAPI(from, to, 1);
  
  if (response.systemCode !== 'ACC_0000') {
    return `❌ Lỗi: ${response.message || 'Không thể lấy dữ liệu'}`;
  }
  
  const list = response.data?.listData || [];
  const s = calculateSummary(list);
  
  return `💬 THỐNG KÊ TIN NHẮN HÔM NAY
━━━━━━━━━━━━━━━━━━━━

• Tin nhắn Fanpage:  ${formatNumber(s.totalMessages)}
• Comment khách:     ${formatNumber(s.totalComments)}
• Comment trả lời:   ${formatNumber(s.totalPageComments)}`;
}

async function getComparison() {
  const todayRange = getTodayRange();
  const yesterdayRange = getYesterdayRange();
  
  const [todayRes, yesterdayRes] = await Promise.all([
    callAPI(todayRange.from, todayRange.to, 1),
    callAPI(yesterdayRange.from, yesterdayRange.to, 1)
  ]);
  
  if (todayRes.systemCode !== 'ACC_0000' || yesterdayRes.systemCode !== 'ACC_0000') {
    return `❌ Lỗi khi lấy dữ liệu`;
  }
  
  const todayList = todayRes.data?.listData || [];
  const yesterdayList = yesterdayRes.data?.listData || [];
  
  const t = calculateSummary(todayList);
  const y = calculateSummary(yesterdayList);
  
  const formatChange = (curr, prev) => {
    const change = curr - prev;
    const percent = prev > 0 ? ((change / prev) * 100).toFixed(1) : 0;
    const arrow = change >= 0 ? '↑' : '↓';
    return `${arrow} ${change >= 0 ? '+' : ''}${formatNumber(change)} (${percent}%)`;
  };
  
  return `📊 SO SÁNH HÔM NAY VS HÔM QUA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Chỉ số            Hôm nay      Hôm qua      Thay đổi
───────────────────────────────────────────────────
👥 TK mới         ${formatNumber(t.totalAccounts).padEnd(11)} ${formatNumber(y.totalAccounts).padEnd(11)} ${formatChange(t.totalAccounts, y.totalAccounts)}
📱 SĐT mới        ${formatNumber(t.totalPhones).padEnd(11)} ${formatNumber(y.totalPhones).padEnd(11)} ${formatChange(t.totalPhones, y.totalPhones)}
💬 Tin nhắn       ${formatNumber(t.totalMessages).padEnd(11)} ${formatNumber(y.totalMessages).padEnd(11)} ${formatChange(t.totalMessages, y.totalMessages)}
💬 Comments       ${formatNumber(t.totalComments).padEnd(11)} ${formatNumber(y.totalComments).padEnd(11)} ${formatChange(t.totalComments, y.totalComments)}`;
}

async function getTagStats() {
  const { from, to } = getWeekRange();
  const response = await callTagsAPI(from, to);
  
  if (response.systemCode !== 'ACC_0000') {
    return `❌ Lỗi: ${response.message || 'Không thể lấy dữ liệu'}`;
  }
  
  const list = response.data?.listData || [];
  if (list.length === 0) {
    return `📊 Chưa có dữ liệu tag`;
  }
  
  // Sort by totalConversation descending
  const sorted = list.sort((a, b) => (b.totalConversation || 0) - (a.totalConversation || 0));
  const total = response.data?.total || sorted.length;
  
  let result = `🏷️ THỐNG KÊ TAG KHÁCH HÀNG (7 NGÀY QUA)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

`;
  
  // Top tags
  const topTags = sorted.slice(0, 10);
  for (const tag of topTags) {
    const bar = '█'.repeat(Math.min(Math.floor(tag.totalConversation / 20), 20));
    result += `   ${(tag.name || 'N/A').padEnd(20)} ${formatNumber(tag.totalConversation).padStart(6)}  ${bar}\n`;
  }
  
  result += `
   ─────────────────────────────────
   Tổng: ${total} tags

💡 Phân tích:
`;
  
  // Find specific tags
  const activeChat = sorted.find(t => t.name?.toLowerCase().includes('đang chat'));
  const stopCare = sorted.find(t => t.name?.toLowerCase().includes('dừng'));
  const l1 = sorted.find(t => t.name?.toLowerCase() === 'l1');
  const spam = sorted.find(t => t.name?.toLowerCase().includes('spam'));
  
  if (activeChat) result += `   • ${activeChat.totalConversation} khách đang chat\n`;
  if (l1) result += `   • ${l1.totalConversation} khách L1 (quan tâm cao)\n`;
  if (stopCare) result += `   • ${stopCare.totalConversation} khách đã dừng chăm sóc\n`;
  if (spam) result += `   • ${spam.totalConversation} khách spam\n`;
  
  return result;
}

async function getSystemTagStats() {
  const { from, to } = getWeekRange();
  const response = await callSystemTagsAPI(from, to);
  
  if (response.systemCode !== 'ACC_0000') {
    return `❌ Lỗi: ${response.message || 'Không thể lấy dữ liệu'}`;
  }
  
  const list = response.data || [];
  if (list.length === 0) {
    return `📊 Chưa có dữ liệu tag hệ thống`;
  }
  
  // Tag colors mapping
  const colorMeaning = {
    'WHITE': 'Mới - Chưa phân loại',
    'YELLOW': 'Đang quan tâm - Cần chăm sóc',
    'GREEN': 'Đã chốt - Khách hàng tiềm năng',
    'RED': 'Khó - Cần chú ý đặc biệt'
  };
  
  const colorEmoji = {
    'WHITE': '⚪',
    'YELLOW': '🟡',
    'GREEN': '🟢',
    'RED': '🔴'
  };
  
  let result = `🎨 THỐNG KÊ TAG HỆ THỐNG (7 NGÀY QUA)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

`;
  
  // Sort by total descending
  const sorted = list.sort((a, b) => (b.total || 0) - (a.total || 0));
  
  for (const tag of sorted) {
    const emoji = colorEmoji[tag.name] || '🏷️';
    const meaning = colorMeaning[tag.name] || 'Khác';
    const bar = '█'.repeat(Math.min(Math.floor(tag.total / 10), 20));
    result += `   ${emoji} ${tag.name.padEnd(8)} ${formatNumber(tag.total).padStart(6)}  ${bar}\n`;
    result += `      ${meaning}\n\n`;
  }
  
  const total = sorted.reduce((sum, t) => sum + (t.total || 0), 0);
  result += `   ─────────────────────────────────\n`;
  result += `   Tổng: ${formatNumber(total)} khách\n\n`;
  
  result += `💡 Ý nghĩa:\n`;
  result += `   ⚪ WHITE  = Mới, chưa phân loại\n`;
  result += `   🟡 YELLOW = Đang quan tâm, cần chăm sóc\n`;
  result += `   🟢 GREEN  = Đã chốt, khách tiềm năng\n`;
  result += `   🔴 RED    = Khó, cần chú ý đặc biệt\n`;
  
  return result;
}

// ===== MAIN =====

async function handleQuery(message) {
  // Check token
  if (!PRENY_TOKEN) {
    return `❌ Chưa cấu hình PRENY_TOKEN

Cách lấy token:
1. Đăng nhập https://app.preny.ai
2. Mở DevTools (F12) → Tab Network
3. Thao tác bất kỳ trên dashboard
4. Tìm request có header Authorization: Bearer xxx
5. Copy token và chạy:
   export PRENY_TOKEN="your-token"`;
  }
  
  // Detect intent
  const intent = detectIntent(message);
  
  if (!intent) {
    return `❓ Tôi không hiểu câu hỏi.

Bạn có thể hỏi về:
• "Thống kê hôm nay"
• "Thống kê hôm qua"
• "Thống kê tuần này"
• "Thống kê tháng này"
• "Bao nhiêu khách hôm nay"
• "Tin nhắn hôm nay"
• "So sánh hôm nay và hôm qua"
• "Thống kê tag khách hàng"
• "Phân loại khách hàng"
• "Thống kê tag màu"
• "Trạng thái hệ thống"`;
  }
  
  // Call handler
  const handlers = {
    getStatsToday,
    getStatsYesterday,
    getStatsWeek,
    getStatsMonth,
    getCustomerStats,
    getMessageStats,
    getComparison,
    getTagStats,
    getSystemTagStats
  };
  
  return await handlers[intent.handler]();
}

// CLI usage
if (require.main === module) {
  const message = process.argv.slice(2).join(' ');
  if (!message) {
    console.log('Usage: node preny-handler.js "câu hỏi"');
    console.log('Example: node preny-handler.js "thống kê hôm nay"');
    process.exit(1);
  }
  
  handleQuery(message).then(console.log).catch(console.error);
}

module.exports = { handleQuery, detectIntent, callAPI };
