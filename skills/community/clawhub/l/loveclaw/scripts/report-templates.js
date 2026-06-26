/**
 * LoveClaw 匹配报告文案（写死模版，晚间推送与本地 cron 共用）
 * 修改文案只改本文件即可。
 */

/**
 * 匹配成功 — 晚间推送 / 「今日缘分已到」
 * @param {string} partnerName
 * @param {string} partnerCity
 * @param {string} partnerPhone
 * @param {number|string} scorePct 总匹配度，显示为数字（可加小数）
 * @param {string} interpretation 八字解读（建议由 bazi.generateMatchReport 生成）
 */
function formatEveningMatchSuccess(partnerName, partnerCity, partnerPhone, scorePct, interpretation) {
  const name = partnerName || '有缘人';
  const city = partnerCity || '未知';
  const phone = partnerPhone || '未知';
  const pct = scorePct == null ? '--' : scorePct;
  const text = buildConciseCompatibilityText(pct, interpretation);

  return `🌟 今日缘分已到！

【匹配对象】
📛 ${name}
📍 ${city}
☎️ ${phone}

【匹配信息】
🔮 总匹配度：${pct}%
💬 ${text}

💡 快去联系你的有缘人吧！`;
}

function buildConciseCompatibilityText(scorePct, interpretation) {
  const n = Number(scorePct);
  let levelText = '你们的八字契合度中等，适合先从日常交流开始。';
  if (!Number.isNaN(n)) {
    if (n >= 85) levelText = '你们的八字契合度很高，价值观与相处节奏较容易同频。';
    else if (n >= 75) levelText = '你们的八字契合度较高，互动通常更容易建立默契。';
    else if (n >= 65) levelText = '你们的八字契合度不错，给彼此一点时间会更容易进入状态。';
  }

  // 兼容旧参数：若传入了简短解读，则优先用首句；多段长文自动忽略
  const raw = String(interpretation || '').trim();
  const firstLine = raw.split('\n').map(s => s.trim()).find(Boolean) || '';
  if (firstLine && firstLine.length <= 36 && !firstLine.includes('【')) {
    return firstLine;
  }
  return levelText;
}

/**
 * 匹配失败 / 今日无合适对象 — 晚间推送（与 README 示例一致）
 * @param {string} [userName] 用户昵称，缺省为「你」
 */
function formatEveningMatchFail(userName) {
  return '🦞 爱情龙虾今日匹配失败，但是命运的齿轮依然转动，期待明日月老的大驾光临！（用户无需重复报名，明日继续自动匹配）';
}

/**
 * 本地 cron.js 曾使用的龙虾口号版（可选）
 */
function formatEveningMatchFailLobster() {
  return '🦞 爱情龙虾今日匹配失败，但是命运的齿轮依然转动，期待明日月老的大驾光临！（用户无需重复报名，明日继续自动匹配）';
}

module.exports = {
  formatEveningMatchSuccess,
  formatEveningMatchFail,
  formatEveningMatchFailLobster,
};
