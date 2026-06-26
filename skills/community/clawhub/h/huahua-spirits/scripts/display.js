#!/usr/bin/env node
/**
 * OpenClaw Spirits — Full display card rendering
 * Generates the complete spirit card in Chinese or English
 */

const { renderSprite, renderFace } = require('./render.js');

// Species names (ZH / EN)
const SPECIES_NAMES = {
  // Living
  mosscat: { zh: '苔猫', en: 'Mosscat', emoji: '🐱' },
  inkoi: { zh: '墨鲤', en: 'Inkoi', emoji: '🐟' },
  embermoth: { zh: '烬蛾', en: 'Embermoth', emoji: '🦋' },
  frostpaw: { zh: '霜兔', en: 'Frostpaw', emoji: '🐰' },
  bellhop: { zh: '铃蛙', en: 'Bellhop', emoji: '🐸' },
  astortoise: { zh: '星龟', en: 'Astortoise', emoji: '🐢' },
  foldwing: { zh: '纸鸢', en: 'Foldwing', emoji: '🐦' },
  cogmouse: { zh: '齿鼠', en: 'Cogmouse', emoji: '🐭' },
  umbracrow: { zh: '影鸦', en: 'Umbracrow', emoji: '🦅' },
  crackviper: { zh: '裂晶蛇', en: 'Crackviper', emoji: '🐍' },
  glowshroom: { zh: '萤菇', en: 'Glowshroom', emoji: '🍄' },
  bubbloom: { zh: '泡水母', en: 'Bubbloom', emoji: '🪼' },
  // Elemental
  inkling: { zh: '墨灵', en: 'Inkling', emoji: '💧' },
  rustbell: { zh: '锈铃', en: 'Rustbell', emoji: '🔔' },
  mossrock: { zh: '苔石', en: 'Mossrock', emoji: '🪨' },
  frostfang: { zh: '霜齿', en: 'Frostfang', emoji: '❄️' },
  loopwyrm: { zh: '迴纹', en: 'Loopwyrm', emoji: '🐉' },
  bubbell: { zh: '泡铃', en: 'Bubbell', emoji: '🫧' },
  cogbeast: { zh: '齿轮兽', en: 'Cogbeast', emoji: '⚙️' },
  umbra: { zh: '影子', en: 'Umbra', emoji: '👤' },
  stardust: { zh: '星沙', en: 'Stardust', emoji: '✨' },
  crackle: { zh: '裂纹', en: 'Crackle', emoji: '💎' },
  wickling: { zh: '烛芯', en: 'Wickling', emoji: '🕯️' },
  echochord: { zh: '弦音', en: 'Echochord', emoji: '🎵' }
};

// Rarity names and symbols
const RARITY_INFO = {
  mundane: { zh: '凡', en: 'MUNDANE', symbol: '·' },
  peculiar: { zh: '异', en: 'PECULIAR', symbol: '··' },
  spirited: { zh: '灵', en: 'SPIRITED', symbol: '···' },
  phantom: { zh: '幻', en: 'PHANTOM', symbol: '····' },
  mythic: { zh: '神', en: 'MYTHIC', symbol: '·····' }
};

// Stat names
const STAT_INFO = {
  intuition: { zh: '直觉', en: 'INTUITION' },
  grit: { zh: '韧性', en: 'GRIT' },
  spark: { zh: '灵动', en: 'SPARK' },
  anchor: { zh: '沉稳', en: 'ANCHOR' },
  edge: { zh: '锋芒', en: 'EDGE' }
};

/**
 * Generate a stat bar (10 chars wide)
 * @param {number} value - 0-100
 * @returns {string}
 */
function statBar(value) {
  const filled = Math.floor(value / 10);
  const empty = 10 - filled;
  return '█'.repeat(filled) + '░'.repeat(empty);
}

/**
 * Render full display card
 * @param {object} companion - full companion data
 * @param {string} lang - 'zh' or 'en'
 * @returns {string}
 */
function displayCard(companion, lang = 'zh') {
  const { species, rarity, name, personality, stats } = companion;
  const speciesInfo = SPECIES_NAMES[species];
  const rarityInfo = RARITY_INFO[rarity];

  // Sprite (frame 0)
  const spriteLines = renderSprite(companion, 0);

  // Header
  const header = lang === 'zh' ? '🥚 灵兽降世！' : '🥚 A Spirit emerges!';

  // Name line
  const nameDisplay = lang === 'zh'
    ? `${speciesInfo.emoji} ${name || speciesInfo.zh} — ${speciesInfo.zh} ${speciesInfo.en}`
    : `${speciesInfo.emoji} ${name || speciesInfo.en} — ${speciesInfo.en}`;

  // Rarity line
  const rarityDisplay = lang === 'zh'
    ? `${rarityInfo.symbol} ${rarityInfo.zh} ${rarityInfo.en}`
    : `${rarityInfo.symbol} ${rarityInfo.en}`;

  // Personality
  const personalityLine = `"${personality}"`;

  // Stats box
  const statLines = [];
  const statOrder = ['intuition', 'grit', 'spark', 'anchor', 'edge'];
  
  statLines.push('┌──────────────────────────────┐');
  for (const stat of statOrder) {
    const value = stats[stat];
    const bar = statBar(value);
    const label = lang === 'zh'
      ? `${STAT_INFO[stat].zh} ${STAT_INFO[stat].en}`
      : STAT_INFO[stat].en;
    const padding = lang === 'zh' ? '' : '  ';
    statLines.push(`│ ${label.padEnd(14)} ${bar}  ${String(value).padStart(2)} ${padding}│`);
  }
  statLines.push('└──────────────────────────────┘');

  // Footer
  const footer = lang === 'zh'
    ? '🔮 灵兽与主人的灵魂绑定，不可选择，不可交易。'
    : '🔮 Spirits are soul-bound. No choosing. No trading.';

  // Assemble
  const lines = [
    header,
    '',
    ...spriteLines,
    '',
    `${nameDisplay}  ${rarityDisplay}`,
    '',
    personalityLine,
    '',
    ...statLines,
    '',
    footer
  ];

  return lines.join('\n');
}

// === CLI ===
if (require.main === module) {
  const args = process.argv.slice(2);
  if (args.length === 0) {
    console.error('Usage: node display.js <companion-json> [zh|en]');
    console.error('Example: node display.js companion.json zh');
    process.exit(1);
  }

  const fs = require('fs');
  const input = args[0];
  const lang = args[1] || 'zh';

  // Accept either a file path or inline JSON
  let companion;
  try {
    companion = JSON.parse(input);
  } catch {
    companion = JSON.parse(fs.readFileSync(input, 'utf8'));
  }
  console.log(displayCard(companion, lang));
}

module.exports = { displayCard, SPECIES_NAMES, RARITY_INFO };
