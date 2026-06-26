#!/usr/bin/env node
/**
 * jiajiaoy-morning — 晚间明日运势 prompt 生成器
 *
 * 读取用户的八字档案，生成明日运势的分析指令
 *
 * 用法：
 *   node evening-push.js <userId>
 */

'use strict';

const fs   = require('fs');
const path = require('path');

const USERS_DIR       = path.join(__dirname, '../data/users');
const YUNSHI_PROFILES = path.join(__dirname, '../../yunshi/data/profiles');

function sanitizeId(v) {
  if (typeof v !== 'string' || !/^[a-zA-Z0-9_@-]{1,128}$/.test(v)) {
    console.error('❌ 无效的 userId'); process.exit(1);
  }
  return v;
}

function safeUserPath(dir, userId) {
  const resolved = path.resolve(dir, `${userId}.json`);
  if (!resolved.startsWith(path.resolve(dir) + path.sep)) {
    console.error('❌ 非法路径'); process.exit(1);
  }
  return resolved;
}

const args = process.argv.slice(2);
if (!args[0]) {
  console.error('用法: node evening-push.js <userId>');
  process.exit(1);
}

const userId = sanitizeId(args[0]);

// 读取用户配置
const userConfigPath = safeUserPath(USERS_DIR, userId);
if (!fs.existsSync(userConfigPath)) {
  console.error(`❌ 用户 ${userId} 未注册。请先运行: node setup.js`);
  process.exit(1);
}
const config = JSON.parse(fs.readFileSync(userConfigPath, 'utf8'));

if (!config.modules?.evening?.yunshi_tomorrow) {
  console.error(`ℹ️ 用户 ${userId} 未开启晚间运势推送`);
  process.exit(0);
}

// 读取用户八字档案（来自 yunshi skill）
let bazi = null;
const yunshiProfilePath = safeUserPath(YUNSHI_PROFILES, userId);
if (fs.existsSync(yunshiProfilePath)) {
  const profile = JSON.parse(fs.readFileSync(yunshiProfilePath, 'utf8'));
  bazi = profile.bazi || null;
}

// 计算明日日期
const now = new Date();
const tomorrow = new Date(now);
tomorrow.setDate(tomorrow.getDate() + 1);
const year  = tomorrow.getFullYear();
const month = tomorrow.getMonth() + 1;
const day   = tomorrow.getDate();
const WEEKDAYS = ['星期日','星期一','星期二','星期三','星期四','星期五','星期六'];
const weekday = WEEKDAYS[tomorrow.getDay()];
const dateStr = `${year}年${month}月${day}日 ${weekday}`;

const name = config.name || userId;

// 生成 prompt
if (bazi && bazi.year && bazi.month && bazi.day && bazi.hour) {
  console.log(`请为 ${name} 推算明天（${dateStr}）的详细运势。

用户八字：
- 年柱：${bazi.year}　月柱：${bazi.month}　日柱：${bazi.day}　时柱：${bazi.hour}
- 日主：${bazi.dayStem || '乙'}　生肖：${bazi.zodiac || '虎'}

请结合八字、紫微斗数和奇门遁甲，给出明日完整运程：

🔮 **明日运势 · ${dateStr}**

**综合运势**：[★★★★☆ 整体评分和一句话概括]

**四大运势**：
- 💼 事业：[分析+建议]
- 💰 财运：[分析+建议]
- 💕 感情：[分析+建议]
- 🏥 健康：[分析+建议]

**时辰吉凶**：[最佳行事时间2-3个]

**宜忌**：
- 宜：[3项]
- 忌：[3项]

**幸运元素**：颜色 [X] · 数字 [X] · 方位 [X]

**明日提醒**：[一句最重要的个性化建议]`);
} else {
  // 没有八字档案，输出通用提示
  console.log(`请根据今天（${new Date().toLocaleDateString('zh-CN')}）的干支历法，推算明天（${dateStr}）的通用运势。

🔮 **明日运势 · ${dateStr}**

请结合明日的天干地支、奇门遁甲等，给出：
- 综合运势评分（★）
- 事业、财运、感情、健康各方面简析
- 今日宜忌
- 幸运颜色/数字/方位
- 最佳行事时辰

直接输出运势内容，格式简洁清晰。`);
}
