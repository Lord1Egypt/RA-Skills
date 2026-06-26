#!/usr/bin/env node
// OpenClaw Buddy Generator
// Ported from Claude Buddy Checker (by FATCullen)
// Adapted for OpenClaw with bilingual support

// === Constants ===

const RARITIES = ['common', 'uncommon', 'rare', 'epic', 'legendary'];
const RARITY_WEIGHTS = { common: 60, uncommon: 25, rare: 10, epic: 4, legendary: 1 };
const RARITY_STARS = {
  common: '★',
  uncommon: '★★',
  rare: '★★★',
  epic: '★★★★',
  legendary: '★★★★★',
};
const RARITY_FLOOR = { common: 5, uncommon: 15, rare: 25, epic: 35, legendary: 50 };

const RARITY_CN = {
  common: '普通',
  uncommon: '稀有',
  rare: '珍稀',
  epic: '史诗',
  legendary: '传说',
};

const RARITY_EMOJI = {
  common: '⬜',
  uncommon: '🟩',
  rare: '🟦',
  epic: '🟪',
  legendary: '🟨',
};

const SPECIES = [
  'duck', 'goose', 'blob', 'cat', 'dragon', 'octopus', 'owl', 'penguin',
  'turtle', 'snail', 'ghost', 'axolotl', 'capybara', 'cactus', 'robot',
  'rabbit', 'mushroom', 'chonk',
];

const SPECIES_CN = {
  duck: '鸭子', goose: '鹅', blob: '水滴怪', cat: '猫咪',
  dragon: '龙', octopus: '章鱼', owl: '猫头鹰', penguin: '企鹅',
  turtle: '乌龟', snail: '蜗牛', ghost: '幽灵', axolotl: '六角恐龙',
  capybara: '水豚', cactus: '仙人掌', robot: '机器人', rabbit: '兔子',
  mushroom: '蘑菇', chonk: '胖墩',
};

const SPECIES_EMOJI = {
  duck: '🦆', goose: '🪿', blob: '🫧', cat: '🐱',
  dragon: '🐉', octopus: '🐙', owl: '🦉', penguin: '🐧',
  turtle: '🐢', snail: '🐌', ghost: '👻', axolotl: '🦎',
  capybara: '🦫', cactus: '🌵', robot: '🤖', rabbit: '🐰',
  mushroom: '🍄', chonk: '😸',
};

const EYES = ['·', '✦', '×', '◉', '@', '°'];
const EYE_NAMES = { '·': '圆点眼', '✦': '✦ 眼', '×': '× 眼', '◉': '◉ 眼', '@': '@ 眼', '°': '° 眼' };

const HATS = ['none', 'crown', 'tophat', 'propeller', 'halo', 'wizard', 'beanie', 'tinyduck'];
const HAT_CN = {
  none: '无', crown: '皇冠', tophat: '高帽', propeller: '螺旋桨帽',
  halo: '光环帽', wizard: '巫师帽', beanie: '毛线帽', tinyduck: '小鸭帽',
};

const STAT_NAMES = ['DEBUGGING', 'PATIENCE', 'CHAOS', 'WISDOM', 'SNARK'];
const STAT_CN = {
  DEBUGGING: '调试力', PATIENCE: '耐心值', CHAOS: '混乱度',
  WISDOM: '智慧值', SNARK: '毒舌值',
};

// === FNV-1a hash ===

function hashString(s) {
  let h = 2166136261;
  for (let i = 0; i < s.length; i++) {
    h ^= s.charCodeAt(i);
    h = Math.imul(h, 16777619);
  }
  return h >>> 0;
}

// === Mulberry32 PRNG ===

function mulberry32(seed) {
  let a = seed >>> 0;
  return function () {
    a |= 0;
    a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

// === Roll logic ===

function pick(rng, arr) { return arr[Math.floor(rng() * arr.length)]; }

function rollRarity(rng) {
  const total = Object.values(RARITY_WEIGHTS).reduce((a, b) => a + b, 0);
  let roll = rng() * total;
  for (const rarity of RARITIES) {
    roll -= RARITY_WEIGHTS[rarity];
    if (roll < 0) return rarity;
  }
  return 'common';
}

function rollStats(rng, rarity) {
  const floor = RARITY_FLOOR[rarity];
  const peak = pick(rng, STAT_NAMES);
  let dump = pick(rng, STAT_NAMES);
  while (dump === peak) dump = pick(rng, STAT_NAMES);
  const stats = {};
  for (const name of STAT_NAMES) {
    if (name === peak) stats[name] = Math.min(100, floor + 50 + Math.floor(rng() * 30));
    else if (name === dump) stats[name] = Math.max(1, floor - 10 + Math.floor(rng() * 15));
    else stats[name] = floor + Math.floor(rng() * 40);
  }
  return stats;
}

const SALT = 'openclaw-buddy-2026';

function roll(userId) {
  const rng = mulberry32(hashString(userId + SALT));
  const rarity = rollRarity(rng);
  const species = pick(rng, SPECIES);
  const eye = pick(rng, EYES);
  const hat = rarity === 'common' ? 'none' : pick(rng, HATS);
  const shiny = rng() < 0.01;
  const stats = rollStats(rng, rarity);
  return { rarity, species, eye, hat, shiny, stats };
}

// === Sprite data ===

const BODIES = {
  duck: [
    ['            ', '    __      ', '  <({E} )___  ', '   (  ._>   ', '    `--´    '],
    ['            ', '    __      ', '  <({E} )___  ', '   (  ._>   ', '    `--´~   '],
    ['            ', '    __      ', '  <({E} )___  ', '   (  .__>  ', '    `--´    '],
  ],
  goose: [
    ['            ', '     ({E}>    ', '     ||     ', '   _(__)_   ', '    ^^^^    '],
    ['            ', '    ({E}>     ', '     ||     ', '   _(__)_   ', '    ^^^^    '],
    ['            ', '     ({E}>>   ', '     ||     ', '   _(__)_   ', '    ^^^^    '],
  ],
  blob: [
    ['            ', '   .----.   ', '  ( {E}  {E} )  ', '  (      )  ', '   `----´   '],
    ['            ', '  .------.  ', ' (  {E}  {E}  ) ', ' (        ) ', '  `------´  '],
    ['            ', '    .--.    ', '   ({E}  {E})   ', '   (    )   ', '    `--´    '],
  ],
  cat: [
    ['            ', '   /\\_/\\    ', '  ( {E}   {E})  ', '  (  ω  )   ', '  (")_(")   '],
    ['            ', '   /\\_/\\    ', '  ( {E}   {E})  ', '  (  ω  )   ', '  (")_(")~  '],
    ['            ', '   /\\-/\\    ', '  ( {E}   {E})  ', '  (  ω  )   ', '  (")_(")   '],
  ],
  dragon: [
    ['            ', '  /^\\  /^\\  ', ' <  {E}  {E}  > ', ' (   ~~   ) ', '  `-vvvv-´  '],
    ['            ', '  /^\\  /^\\  ', ' <  {E}  {E}  > ', ' (        ) ', '  `-vvvv-´  '],
    ['   ~    ~   ', '  /^\\  /^\\  ', ' <  {E}  {E}  > ', ' (   ~~   ) ', '  `-vvvv-´  '],
  ],
  octopus: [
    ['            ', '   .----.   ', '  ( {E}  {E} )  ', '  (______)  ', '  /\\/\\/\\/\\  '],
    ['            ', '   .----.   ', '  ( {E}  {E} )  ', '  (______)  ', '  \\/\\/\\/\\/  '],
    ['     o      ', '   .----.   ', '  ( {E}  {E} )  ', '  (______)  ', '  /\\/\\/\\/\\  '],
  ],
  owl: [
    ['            ', '   /\\  /\\   ', '  (({E})({E}))  ', '  (  ><  )  ', '   `----´   '],
    ['            ', '   /\\  /\\   ', '  (({E})({E}))  ', '  (  ><  )  ', '   .----.   '],
    ['            ', '   /\\  /\\   ', '  (({E})(-))  ', '  (  ><  )  ', '   `----´   '],
  ],
  penguin: [
    ['            ', '  .---.     ', '  ({E}>{E})     ', ' /(   )\\    ', '  `---´     '],
    ['            ', '  .---.     ', '  ({E}>{E})     ', ' |(   )|    ', '  `---´     '],
    ['  .---.     ', '  ({E}>{E})     ', ' /(   )\\    ', '  `---´     ', '   ~ ~      '],
  ],
  turtle: [
    ['            ', '   _,--._   ', '  ( {E}  {E} )  ', ' /[______]\\ ', '  ``    ``  '],
    ['            ', '   _,--._   ', '  ( {E}  {E} )  ', ' /[______]\\ ', '   ``  ``   '],
    ['            ', '   _,--._   ', '  ( {E}  {E} )  ', ' /[======]\\ ', '  ``    ``  '],
  ],
  snail: [
    ['            ', ' {E}    .--.  ', '  \\  ( @ )  ', '   \\_`--´   ', '  ~~~~~~~   '],
    ['            ', '  {E}   .--.  ', '  |  ( @ )  ', '   \\_`--´   ', '  ~~~~~~~   '],
    ['            ', ' {E}    .--.  ', '  \\  ( @  ) ', '   \\_`--´   ', '   ~~~~~~   '],
  ],
  ghost: [
    ['            ', '   .----.   ', '  / {E}  {E} \\  ', '  |      |  ', '  ~`~``~`~  '],
    ['            ', '   .----.   ', '  / {E}  {E} \\  ', '  |      |  ', '  `~`~~`~`  '],
    ['    ~  ~    ', '   .----.   ', '  / {E}  {E} \\  ', '  |      |  ', '  ~~`~~`~~  '],
  ],
  axolotl: [
    ['            ', '}~(______)~{', '}~({E} .. {E})~{', '  ( .--. )  ', '  (_/  \\_)  '],
    ['            ', '~}(______){~', '~}({E} .. {E}){~', '  ( .--. )  ', '  (_/  \\_)  '],
    ['            ', '}~(______)~{', '}~({E} .. {E})~{', '  (  --  )  ', '  ~_/  \\_~  '],
  ],
  capybara: [
    ['            ', '  n______n  ', ' ( {E}    {E} ) ', ' (   oo   ) ', '  `------´  '],
    ['            ', '  n______n  ', ' ( {E}    {E} ) ', ' (   Oo   ) ', '  `------´  '],
    ['    ~  ~    ', '  u______n  ', ' ( {E}    {E} ) ', ' (   oo   ) ', '  `------´  '],
  ],
  cactus: [
    ['            ', ' n  ____  n ', ' | |{E}  {E}| | ', ' |_|    |_| ', '   |    |   '],
    ['            ', '    ____    ', ' n |{E}  {E}| n ', ' |_|    |_| ', '   |    |   '],
    [' n        n ', ' |  ____  | ', ' | |{E}  {E}| | ', ' |_|    |_| ', '   |    |   '],
  ],
  robot: [
    ['            ', '   .[||].   ', '  [ {E}  {E} ]  ', '  [ ==== ]  ', '  `------´  '],
    ['            ', '   .[||].   ', '  [ {E}  {E} ]  ', '  [ -==- ]  ', '  `------´  '],
    ['     *      ', '   .[||].   ', '  [ {E}  {E} ]  ', '  [ ==== ]  ', '  `------´  '],
  ],
  rabbit: [
    ['            ', '   (\\__/)   ', '  ( {E}  {E} )  ', ' =(  ..  )= ', '  (")__(")  '],
    ['            ', '   (|__/)   ', '  ( {E}  {E} )  ', ' =(  ..  )= ', '  (")__(")  '],
    ['            ', '   (\\__/)   ', '  ( {E}  {E} )  ', ' =( .  . )= ', '  (")__(")  '],
  ],
  mushroom: [
    ['            ', ' .-o-OO-o-. ', '(__________)', '   |{E}  {E}|   ', '   |____|   '],
    ['            ', ' .-O-oo-O-. ', '(__________)', '   |{E}  {E}|   ', '   |____|   '],
    ['   . o  .   ', ' .-o-OO-o-. ', '(__________)', '   |{E}  {E}|   ', '   |____|   '],
  ],
  chonk: [
    ['            ', '  /\\    /\\  ', ' ( {E}    {E} ) ', ' (   ..   ) ', '  `------´  '],
    ['            ', '  /\\    /|  ', ' ( {E}    {E} ) ', ' (   ..   ) ', '  `------´  '],
    ['            ', '  /\\    /\\  ', ' ( {E}    {E} ) ', ' (   ..   ) ', '  `------´~ '],
  ],
};

const HAT_LINES = {
  none: '',
  crown: '   \\^^^/    ',
  tophat: '   [___]    ',
  propeller: '    -+-     ',
  halo: '   (   )    ',
  wizard: '    /^\\     ',
  beanie: '   (___)    ',
  tinyduck: '    ,>      ',
};

// === Render sprite ===

function renderSprite(bones) {
  const frames = BODIES[bones.species];
  const body = frames[0].map(line => line.replaceAll('{E}', bones.eye));
  const lines = [...body];
  if (bones.hat !== 'none' && !lines[0].trim()) {
    lines[0] = HAT_LINES[bones.hat];
  }
  if (!lines[0].trim() && frames.every(f => !f[0].trim())) {
    lines.shift();
  }
  return lines;
}

// === Stat bar (text) ===

function statBar(value) {
  const filled = Math.round(value / 5); // 0-20 blocks
  const empty = 20 - filled;
  return '█'.repeat(filled) + '░'.repeat(empty);
}

// === Main ===

function main() {
  const userId = process.argv[2];
  if (!userId) {
    console.error('Usage: node buddy.js <user_id>');
    process.exit(1);
  }

  const buddy = roll(userId);
  const sprite = renderSprite(buddy);

  // Build output
  const output = {
    userId,
    ...buddy,
    speciesCn: SPECIES_CN[buddy.species],
    speciesEmoji: SPECIES_EMOJI[buddy.species],
    rarityCn: RARITY_CN[buddy.rarity],
    rarityStars: RARITY_STARS[buddy.rarity],
    rarityEmoji: RARITY_EMOJI[buddy.rarity],
    hatCn: HAT_CN[buddy.hat],
    eyeName: EYE_NAMES[buddy.eye],
    sprite: sprite.join('\n'),
    statsCn: {},
  };

  for (const [k, v] of Object.entries(buddy.stats)) {
    output.statsCn[k] = { name: STAT_CN[k], value: v, bar: statBar(v) };
  }

  // Text card output
  const lines = [];
  lines.push(`${buddy.shiny ? '✨ ' : ''}${SPECIES_EMOJI[buddy.species]} ${SPECIES_CN[buddy.species]} | ${RARITY_CN[buddy.rarity].toUpperCase()} ${RARITY_STARS[buddy.rarity]}${buddy.shiny ? ' ✨' : ''}`);
  lines.push('');
  lines.push(sprite.join('\n'));
  lines.push('');
  lines.push(`🎭 眼睛: ${EYE_NAMES[buddy.eye]}  |  🎩 帽子: ${HAT_CN[buddy.hat]}`);
  if (buddy.shiny) lines.push('✨ 闪光个体！超级稀有！');
  lines.push('');
  lines.push('📊 属性面板');
  for (const name of STAT_NAMES) {
    const val = buddy.stats[name];
    const cn = STAT_CN[name];
    lines.push(`  ${cn.padEnd(4, '　')} ${statBar(val)} ${String(val).padStart(3)}`);
  }

  // Description
  const peakStat = STAT_NAMES.reduce((a, b) => buddy.stats[a] > buddy.stats[b] ? a : b);
  const descriptions = {
    DEBUGGING: `一只擅长找 bug 的${SPECIES_CN[buddy.species]}`,
    PATIENCE: `一只特别有耐心的${SPECIES_CN[buddy.species]}`,
    CHAOS: `一只热爱混乱的${SPECIES_CN[buddy.species]}`,
    WISDOM: `一只充满智慧的${SPECIES_CN[buddy.species]}`,
    SNARK: `一只毒舌但可爱的${SPECIES_CN[buddy.species]}`,
  };
  lines.push('');
  lines.push(`💬 "${descriptions[peakStat]}"`);

  console.log(lines.join('\n'));

  // Also output JSON to stderr for programmatic use
  process.stderr.write(JSON.stringify(output) + '\n');
}

main();
