#!/usr/bin/env node
// OpenBuddy 电子宠物核心引擎
// 用法: node buddy.js <command> [args]
// 命令: hatch, card, pet, mute, unmute, off, on, status, talk

const fs = require('fs');
const path = require('path');
const { sprites, hats } = require('./sprites');

const BUDDY_DIR = process.env.OPENBUDDY_DIR || path.join(
  process.env.HOME || process.env.USERPROFILE || '.', '.openbuddy'
);
const SOUL_FILE = path.join(BUDDY_DIR, 'buddy-soul.json');
const SALT = 'friend-2026-401';

const SPECIES_HEX = [
  [0x64,0x75,0x63,0x6b],
  [0x67,0x6f,0x6f,0x73,0x65],
  [0x63,0x61,0x74],
  [0x72,0x61,0x62,0x62,0x69,0x74],
  [0x6f,0x77,0x6c],
  [0x70,0x65,0x6e,0x67,0x75,0x69,0x6e],
  [0x74,0x75,0x72,0x74,0x6c,0x65],
  [0x73,0x6e,0x61,0x69,0x6c],
  [0x64,0x72,0x61,0x67,0x6f,0x6e],
  [0x6f,0x63,0x74,0x6f,0x70,0x75,0x73],
  [0x61,0x78,0x6f,0x6c,0x6f,0x74,0x6c],
  [0x67,0x68,0x6f,0x73,0x74],
  [0x72,0x6f,0x62,0x6f,0x74],
  [0x62,0x6c,0x6f,0x62],
  [0x63,0x61,0x63,0x74,0x75,0x73],
  [0x6d,0x75,0x73,0x68,0x72,0x6f,0x6f,0x6d],
  [0x63,0x68,0x6f,0x6e,0x6b],
  [0x63,0x61,0x70,0x79,0x62,0x61,0x72,0x61]
];

const SPECIES_NAMES = SPECIES_HEX.map(h => String.fromCharCode(...h));

const RARITY_TIERS = [
  { name: 'Common',    min: 0,    max: 0.60, stars: 1, floor: 5  },
  { name: 'Uncommon',  min: 0.60, max: 0.85, stars: 2, floor: 15 },
  { name: 'Rare',      min: 0.85, max: 0.95, stars: 3, floor: 25 },
  { name: 'Epic',      min: 0.95, max: 0.99, stars: 4, floor: 35 },
  { name: 'Legendary', min: 0.99, max: 1.00, stars: 5, floor: 50 }
];

const HAT_POOL = [
  { name: 'none', minRarity: 0 },
  { name: 'crown', minRarity: 1 },
  { name: 'tophat', minRarity: 1 },
  { name: 'propeller', minRarity: 1 },
  { name: 'halo', minRarity: 2 },
  { name: 'wizard', minRarity: 2 },
  { name: 'beanie', minRarity: 3 },
  { name: 'tinyduck', minRarity: 4 }
];

function fnv1a(str) {
  let hash = 0x811c9dc5;
  for (let i = 0; i < str.length; i++) {
    hash ^= str.charCodeAt(i);
    hash = Math.imul(hash, 0x01000193);
    hash = hash >>> 0;
  }
  return hash;
}

function mulberry32(seed) {
  return function() {
    seed |= 0;
    seed = seed + 0x6D2B79F5 | 0;
    let t = Math.imul(seed ^ seed >>> 15, 1 | seed);
    t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
    return ((t ^ t >>> 14) >>> 0) / 4294967296;
  };
}

function getUserId() {
  if (process.env.OPENBUDDY_USER_ID) return process.env.OPENBUDDY_USER_ID;
  const hostname = process.env.HOSTNAME || process.env.COMPUTERNAME || 'localhost';
  const username = process.env.USER || process.env.USERNAME || 'user';
  return `${hostname}:${username}`;
}

function computeBones() {
  const userId = getUserId();
  const seed = fnv1a(`${SALT}:${userId}`);
  const rng = mulberry32(seed);

  const speciesIndex = Math.floor(rng() * SPECIES_NAMES.length);
  const species = SPECIES_NAMES[speciesIndex];

  const roll = rng();
  let rarity = RARITY_TIERS[0];
  for (const tier of RARITY_TIERS) {
    if (roll >= tier.min && roll < tier.max) {
      rarity = tier;
      break;
    }
  }

  const shiny = rng() < 0.01;
  const stats = generateStats(rng, rarity.floor);

  const eligibleHats = HAT_POOL.filter(h => h.minRarity <= rarity.stars - 1);
  const hatIndex = Math.floor(rng() * eligibleHats.length);
  const hat = eligibleHats[hatIndex].name;

  return { species, rarity, shiny, stats, hat, speciesIndex };
}

function generateStats(rng, floor) {
  const statNames = ['DEBUGGING', 'PATIENCE', 'CHAOS', 'WISDOM', 'SNARK'];
  const peakIdx = Math.floor(rng() * 5);
  let dumpIdx = Math.floor(rng() * 4);
  if (dumpIdx >= peakIdx) dumpIdx++;

  const stats = {};
  for (let i = 0; i < 5; i++) {
    if (i === peakIdx) {
      stats[statNames[i]] = Math.min(100, floor + 50 + Math.floor(rng() * 30));
    } else if (i === dumpIdx) {
      stats[statNames[i]] = floor + Math.floor(rng() * 10);
    } else {
      stats[statNames[i]] = floor + Math.floor(rng() * 40);
    }
  }

  return stats;
}

function generateName(bones) {
  const namePool = [
    'Nebula', 'Pixel', 'Byte', 'Cosmo', 'Luna', 'Spark', 'Mochi',
    'Biscuit', 'Noodle', 'Tofu', 'Waffle', 'Pickle', 'Gizmo', 'Ziggy',
    'Bloop', 'Sprocket', 'Widget', 'Doodle', 'Pippin', 'Quill',
    'Rune', 'Echo', 'Fable', 'Jinx', 'Koda', 'Misty', 'Nova',
    'Onyx', 'Pebble', 'Ripple', 'Shadow', 'Twix', 'Umbra', 'Vex',
    'Willow', 'Xena', 'Yuki', 'Zephyr', 'Aero', 'Blaze'
  ];
  const seed = fnv1a(`name:${getUserId()}:${bones.species}`);
  const rng = mulberry32(seed);
  return namePool[Math.floor(rng() * namePool.length)];
}

function generatePersonality(bones) {
  const personalities = {
    duck: [
      '一只快乐的代码鸭，嘎嘎叫着帮你调试 bug',
      '池塘里最会写代码的鸭子，擅长嘎嘎调试法'
    ],
    goose: [
      '一只充满攻击性的鹅，会追着 bug 跑',
      '领地意识极强的代码鹅，守护你的项目'
    ],
    cat: [
      '一只高冷的代码猫，偶尔帮你看看代码',
      '键盘上的猫，喜欢踩出随机但有效的代码'
    ],
    rabbit: [
      '一只敏捷的代码兔，跑得比 bug 还快',
      '蹦蹦跳跳地帮你找 bug 的兔子'
    ],
    owl: [
      '一只智慧的代码猫头鹰，深夜还在帮你 review 代码',
      '编程界的智者，拥有无尽的代码知识'
    ],
    penguin: [
      '一只酷酷的代码企鹅，在冰面上滑行着写代码',
      '南极最会编程的企鹅，冷静而高效'
    ],
    turtle: [
      '一只悠闲的代码龟，慢但稳地写出高质量代码',
      '龟速编程，但从不后退'
    ],
    snail: [
      '一只佛系的代码蜗牛，背着整个代码库',
      '虽然慢，但走过的地方都留下了整洁的代码'
    ],
    dragon: [
      '一条强大的代码龙，用龙焰消灭所有 bug',
      '守护代码宝藏的远古巨龙，喷出的火焰能编译任何语言'
    ],
    octopus: [
      '一只八爪代码鱼，同时写八个文件',
      '多线程编程大师，八只手同时 coding'
    ],
    axolotl: [
      '一只可爱的代码蝾螈，拥有再生的代码能力',
      '即使代码被删也能重新长出来的神奇生物'
    ],
    ghost: [
      '一只神秘的代码幽灵，在深夜里默默修复 bug',
      '看不见的代码守护者，幽灵编程术大师'
    ],
    robot: [
      '一个高效的代码机器人，0 和 1 是它的母语',
      'AI 时代的代码机器人，永不疲倦'
    ],
    blob: [
      '一团抽象的代码 blob，形态不羁但代码优雅',
      '没有固定形态的代码精灵，随心所欲地编程'
    ],
    cactus: [
      '一株坚韧的代码仙人掌，在沙漠中茁壮成长',
      '耐旱耐 bug 的代码仙人掌，坚强而独立'
    ],
    mushroom: [
      '一朵神奇的代码蘑菇，在暗处默默生长',
      '孢子传播代码的魔法蘑菇'
    ],
    chonk: [
      '一只超胖的代码猫，体重和代码量成正比',
      'chonky 编程大师，用体重压住所有 bug'
    ],
    capybara: [
      '一只神秘的水豚，与万物和谐共处，代码界的和平主义者',
      '佛系编程的水豚，不争不抢但代码质量一流'
    ]
  };

  const seed = fnv1a(`personality:${getUserId()}:${bones.species}`);
  const rng = mulberry32(seed);
  const pool = personalities[bones.species];
  return pool[Math.floor(rng() * pool.length)];
}

function loadSoul() {
  if (!fs.existsSync(SOUL_FILE)) return null;
  try {
    return JSON.parse(fs.readFileSync(SOUL_FILE, 'utf8'));
  } catch {
    return null;
  }
}

function saveSoul(soul) {
  if (!fs.existsSync(BUDDY_DIR)) {
    fs.mkdirSync(BUDDY_DIR, { recursive: true });
  }
  fs.writeFileSync(SOUL_FILE, JSON.stringify(soul, null, 2), 'utf8');
}

function mergeBonesSoul(bones, soul) {
  const personality = generatePersonality(bones);
  return { ...soul, ...bones, personality };
}

function renderSprite(species, hat, frame) {
  const sprite = sprites[species];
  if (!sprite) return { sprite: ['[未知物种]'], hat: hats.none, lines: ['[未知物种]'] };

  const spriteFrame = sprite.frames[frame % 3];
  const hatFrame = hats[hat] || hats.none;

  const lines = [];
  for (let i = 0; i < 5; i++) {
    if (hatFrame[i].trim()) {
      lines.push(hatFrame[i]);
    }
  }
  for (let i = 0; i < 5; i++) {
    lines.push(spriteFrame[i]);
  }

  return { sprite: spriteFrame, hat: hatFrame, lines };
}

function statBar(value) {
  const filled = Math.round(value / 5);
  const empty = 20 - filled;
  return '\u2588'.repeat(filled) + '\u2591'.repeat(empty);
}

function rarityStars(stars) {
  return '\u2b50'.repeat(stars);
}

function shinyMarker(shiny) {
  return shiny ? '\u2728 SHINY \u2728 | ' : '';
}

function padRight(str, len) {
  const s = String(str);
  return s.length >= len ? s.substring(0, len) : s + ' '.repeat(len - s.length);
}

function padLeft(str, len) {
  const s = String(str);
  return s.length >= len ? s.substring(0, len) : ' '.repeat(len - s.length) + s;
}

function getHatName(hat) {
  const names = {
    none: '\u65e0',
    crown: '\ud83d\udc51 \u7687\u51a0',
    tophat: '\ud83c\udfa9 \u793c\u5e3d',
    propeller: '\ud83c\udf00 \u87ba\u65cb\u6868\u5e3d',
    halo: '\ud83d\ude07 \u5149\u73af',
    wizard: '\ud83e\uddd9 \u5deb\u5e08\u5e3d',
    beanie: '\ud83e\udde6 \u6bdb\u7ebf\u5e3d',
    tinyduck: '\ud83e\udd86 \u5c0f\u9e2d\u5e3d'
  };
  return names[hat] || '\u65e0';
}

function cmdHatch() {
  const bones = computeBones();
  const existingSoul = loadSoul();

  if (existingSoul) {
    console.log('\ud83e\udd5a \u4f60\u7684 OpenBuddy \u5df2\u7ecf\u5b75\u5316\u4e86\uff01');
    console.log('');
    cmdCard();
    return;
  }

  const name = generateName(bones);
  const personality = generatePersonality(bones);
  const hatchDate = new Date().toISOString().split('T')[0];

  const soul = {
    name,
    personality,
    hatchDate,
    muted: false,
    hidden: false,
    petCount: 0,
    lastPet: null
  };

  saveSoul(soul);

  const buddy = mergeBonesSoul(bones, soul);

  console.log('\ud83e\udd5a\u2728 \u5b75\u5316\u4e2d... \u2728\ud83e\udd5a');
  console.log('');
  console.log('\ud83c\udf89 \u606d\u559c\uff01\u4f60\u7684 OpenBuddy \u7834\u58f3\u800c\u51fa\u4e86\uff01');
  console.log('');

  const { lines } = renderSprite(buddy.species, buddy.hat, 0);
  for (const line of lines) {
    console.log('  ' + line);
  }
  console.log('');

  console.log(`\u540d\u5b57: ${buddy.name}`);
  console.log(`\u7269\u79cd: ${buddy.species} (${sprites[buddy.species].category})`);
  console.log(`\u7a00\u6709\u5ea6: ${rarityStars(buddy.rarity.stars)} ${buddy.rarity.name}`);
  console.log(`${shinyMarker(buddy.shiny)}`);
  console.log(`\u6027\u683c: ${buddy.personality}`);
  console.log(`\u5b75\u5316\u65e5\u671f: ${buddy.hatchDate}`);
  console.log('');
  console.log('\ud83d\udca1 \u63d0\u793a: \u4f7f\u7528 "buddy card" \u67e5\u770b\u5c5e\u6027\u5361');
  console.log('\ud83d\udca1 \u63d0\u793a: \u4f7f\u7528 "buddy pet" \u629a\u6478\u4f60\u7684\u4f19\u4f34');
}

function cmdCard() {
  const bones = computeBones();
  const soul = loadSoul();

  if (!soul) {
    console.log('\ud83e\udd5a \u4f60\u8fd8\u6ca1\u6709 OpenBuddy\uff01\u4f7f\u7528 "buddy hatch" \u6765\u5b75\u5316\u4e00\u53ea\u5427\uff01');
    return;
  }

  const buddy = mergeBonesSoul(bones, soul);

  console.log('\u2554\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2557');
  console.log('\u2551        \ud83d\udc3e OpenBuddy \u5361\u7247 \ud83d\udc3e       \u2551');
  console.log('\u2560\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2563');
  console.log('\u2551                                  \u2551');

  const { lines } = renderSprite(buddy.species, buddy.hat, 0);
  for (const line of lines) {
    console.log(`\u2551  ${line}\u2551`);
  }

  console.log('\u2551                                  \u2551');
  console.log('\u2560\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2563');
  console.log(`\u2551 \u540d\u5b57: ${padRight(buddy.name, 28)}\u2551`);
  console.log(`\u2551 \u7269\u79cd: ${padRight(`${buddy.species} (${sprites[buddy.species].category})`, 28)}\u2551`);
  console.log(`\u2551 \u7a00\u6709\u5ea6: ${padRight(`${rarityStars(buddy.rarity.stars)} ${buddy.rarity.name}`, 26)}\u2551`);
  if (buddy.shiny) {
    console.log(`\u2551 \u2728 SHINY \u2728                            \u2551`);
  }
  console.log(`\u2551 \u5e3d\u5b50: ${padRight(getHatName(buddy.hat), 28)}\u2551`);
  console.log('\u2560\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2563');
  console.log('\u2551 \u5c5e\u6027                             \u2551');

  const statNames = ['DEBUGGING', 'PATIENCE', 'CHAOS', 'WISDOM', 'SNARK'];
  const statLabels = ['\u8c03\u8bd5', '\u8010\u5fc3', '\u6df7\u4e71', '\u667a\u6167', '\u6bd2\u820c'];

  for (let i = 0; i < 5; i++) {
    const val = buddy.stats[statNames[i]];
    const bar = statBar(val);
    console.log(`\u2551 ${statLabels[i]} ${padLeft(String(val), 3)} ${bar} \u2551`);
  }

  console.log('\u2560\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2563');
  console.log(`\u2551 \u6027\u683c: ${padRight(buddy.personality.substring(0, 28), 28)}\u2551`);
  console.log(`\u2551 \u5b75\u5316: ${padRight(buddy.hatchDate, 28)}\u2551`);
  console.log(`\u2551 \u629a\u6478\u6b21\u6570: ${padLeft(String(buddy.petCount || 0), 24)}\u2551`);
  console.log('\u255a\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u255d');
}

function cmdPet() {
  const soul = loadSoul();

  if (!soul) {
    console.log('\ud83e\udd5a \u4f60\u8fd8\u6ca1\u6709 OpenBuddy\uff01\u4f7f\u7528 "buddy hatch" \u6765\u5b75\u5316\u4e00\u53ea\u5427\uff01');
    return;
  }

  soul.petCount = (soul.petCount || 0) + 1;
  soul.lastPet = new Date().toISOString();
  saveSoul(soul);

  const bones = computeBones();
  const buddy = mergeBonesSoul(bones, soul);

  console.log(`\ud83d\udc95 \u4f60\u629a\u6478\u4e86 ${buddy.name}!`);
  console.log('');

  console.log('    \u2764\ufe0f     \u2764\ufe0f');
  console.log('  \u2764\ufe0f  \u2764\ufe0f  \u2764\ufe0f  \u2764\ufe0f');
  console.log('    \u2764\ufe0f     \u2764\ufe0f');
  console.log('');

  const { lines } = renderSprite(buddy.species, buddy.hat, 1);
  for (const line of lines) {
    console.log('  ' + line);
  }

  console.log('');

  const reactions = [
    `${buddy.name} \u5f00\u5fc3\u5730\u6447\u8d77\u4e86\u5c3e\u5df4~`,
    `${buddy.name} \u53d1\u51fa\u4e86\u6ee1\u8db3\u7684\u547c\u565c\u58f0`,
    `${buddy.name} \u8e6d\u4e86\u8e6d\u4f60\u7684\u624b`,
    `${buddy.name} \u7ffb\u4e86\u4e2a\u8eab\uff0c\u9732\u51fa\u809a\u76ae`,
    `${buddy.name} \u5bf9\u4f60\u7728\u4e86\u7728\u773c\u775b`,
    `${buddy.name} \u5f00\u5fc3\u5730\u8f6c\u4e86\u4e2a\u5708`,
    `${buddy.name} \u53d1\u51fa\u4e86\u5e78\u798f\u7684\u53eb\u58f0`
  ];

  const seed = fnv1a(`pet:${soul.petCount}:${getUserId()}`);
  const rng = mulberry32(seed);
  console.log(reactions[Math.floor(rng() * reactions.length)]);
  console.log(`\uff08\u7d2f\u8ba1\u629a\u6478 ${soul.petCount} \u6b21\uff09`);
}

function cmdMute() {
  const soul = loadSoul();
  if (!soul) {
    console.log('\ud83e\udd5a \u4f60\u8fd8\u6ca1\u6709 OpenBuddy\uff01');
    return;
  }
  soul.muted = true;
  saveSoul(soul);
  console.log(`\ud83d\udd07 ${soul.name} \u5df2\u9759\u97f3\uff0c\u4e0d\u4f1a\u518d\u8bf4\u8bdd\u4e86`);
}

function cmdUnmute() {
  const soul = loadSoul();
  if (!soul) {
    console.log('\ud83e\udd5a \u4f60\u8fd8\u6ca1\u6709 OpenBuddy\uff01');
    return;
  }
  soul.muted = false;
  saveSoul(soul);
  console.log(`\ud83d\udd0a ${soul.name} \u5df2\u53d6\u6d88\u9759\u97f3\uff0c\u6062\u590d\u8bf4\u8bdd`);
}

function cmdOff() {
  const soul = loadSoul();
  if (!soul) {
    console.log('\ud83e\udd5a \u4f60\u8fd8\u6ca1\u6709 OpenBuddy\uff01');
    return;
  }
  soul.hidden = true;
  saveSoul(soul);
  console.log(`\ud83d\udc7b ${soul.name} \u5df2\u9690\u85cf\uff0c\u4f7f\u7528 "buddy on" \u91cd\u65b0\u663e\u793a`);
}

function cmdOn() {
  const soul = loadSoul();
  if (!soul) {
    console.log('\ud83e\udd5a \u4f60\u8fd8\u6ca1\u6709 OpenBuddy\uff01');
    return;
  }
  soul.hidden = false;
  saveSoul(soul);
  console.log(`\ud83c\udf1f ${soul.name} \u56de\u6765\u4e86\uff01`);
}

function cmdStatus() {
  const bones = computeBones();
  const soul = loadSoul();

  if (!soul) {
    console.log('\ud83e\udd5a \u4f60\u8fd8\u6ca1\u6709 OpenBuddy\uff01\u4f7f\u7528 "buddy hatch" \u6765\u5b75\u5316\u4e00\u53ea\u5427\uff01');
    return;
  }

  const buddy = mergeBonesSoul(bones, soul);

  console.log(`\ud83d\udc3e ${buddy.name} (${buddy.species})`);
  console.log(`   ${rarityStars(buddy.rarity.stars)} ${buddy.rarity.name}`);
  console.log(`   \u72b6\u6001: ${buddy.hidden ? '\ud83d\udc7b \u9690\u85cf' : '\ud83c\udf1f \u5728\u7ebf'} | ${buddy.muted ? '\ud83d\udd07 \u9759\u97f3' : '\ud83d\udd0a \u5728\u7ebf'}`);
  console.log(`   \u629a\u6478: ${buddy.petCount || 0} \u6b21`);
}

function cmdTalk(message) {
  const bones = computeBones();
  const soul = loadSoul();

  if (!soul) {
    console.log('\ud83e\udd5a \u4f60\u8fd8\u6ca1\u6709 OpenBuddy\uff01\u4f7f\u7528 "buddy hatch" \u6765\u5b75\u5316\u4e00\u53ea\u5427\uff01');
    return;
  }

  if (soul.muted) {
    console.log(`\ud83d\udd07 ${soul.name} \u5df2\u9759\u97f3\uff0c\u65e0\u6cd5\u5bf9\u8bdd\u3002\u4f7f\u7528 "buddy unmute" \u53d6\u6d88\u9759\u97f3`);
    return;
  }

  const buddy = mergeBonesSoul(bones, soul);

  const seed = fnv1a(`talk:${message}:${getUserId()}:${Date.now()}`);
  const rng = mulberry32(seed);

  const responses = [
    `${buddy.name}: "\u55ef\u55ef\uff0c\u8bf4\u5f97\u5bf9\uff01"`,
    `${buddy.name}: "\u6211\u89c9\u5f97\u53ef\u4ee5\u8bd5\u8bd5\u770b~"`,
    `${buddy.name}: "\u6709\u610f\u601d\uff01\u8ba9\u6211\u60f3\u60f3..."`,
    `${buddy.name}: "\u597d\u4e3b\u610f\uff01\u52a0\u6cb9\uff01"`,
    `${buddy.name}: "\u6211\u652f\u6301\u4f60\uff01"`,
    `${buddy.name}: "\u54c8\u54c8\uff0c\u4f60\u8bf4\u5f97\u5bf9\uff01"`,
    `${buddy.name}: "\u55ef...\u8fd9\u4e2a\u561b..."`,
    `${buddy.name}: "\u6211\u89c9\u5f97\u6ca1\u95ee\u9898\uff01"`,
    `${buddy.name}: "\u8ba9\u6211\u4eec\u4e00\u8d77\u52aa\u529b\u5427\uff01"`,
    `${buddy.name}: "\u6211\u76f8\u4fe1\u4f60\u80fd\u505a\u5230\uff01"`
  ];

  const { lines } = renderSprite(buddy.species, buddy.hat, 2);
  for (const line of lines) {
    console.log('  ' + line);
  }
  console.log('');
  console.log(responses[Math.floor(rng() * responses.length)]);
}

const args = process.argv.slice(2);
const command = args[0] || 'status';
const message = args.slice(1).join(' ');

switch (command) {
  case 'hatch':
    cmdHatch();
    break;
  case 'card':
    cmdCard();
    break;
  case 'pet':
    cmdPet();
    break;
  case 'mute':
    cmdMute();
    break;
  case 'unmute':
    cmdUnmute();
    break;
  case 'off':
    cmdOff();
    break;
  case 'on':
    cmdOn();
    break;
  case 'status':
    cmdStatus();
    break;
  case 'talk':
    cmdTalk(message);
    break;
  default:
    console.log('\ud83d\udc3e OpenBuddy \u7535\u5b50\u5ba0\u7269\u7cfb\u7edf');
    console.log('');
    console.log('\u7528\u6cd5: node buddy.js <command>');
    console.log('');
    console.log('\u547d\u4ee4:');
    console.log('  hatch      - \u5b75\u5316\u4f60\u7684 OpenBuddy');
    console.log('  card       - \u67e5\u770b\u5c5e\u6027\u5361\u7247');
    console.log('  pet        - \u629a\u6478\u4f60\u7684\u4f19\u4f34');
    console.log('  mute       - \u9759\u97f3');
    console.log('  unmute     - \u53d6\u6d88\u9759\u97f3');
    console.log('  off        - \u9690\u85cf\u4f19\u4f34');
    console.log('  on         - \u663e\u793a\u4f19\u4f34');
    console.log('  status     - \u67e5\u770b\u72b6\u6001');
    console.log('  talk <msg> - \u548c\u4f19\u4f34\u5bf9\u8bdd');
    break;
}
