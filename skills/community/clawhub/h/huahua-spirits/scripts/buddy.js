#!/usr/bin/env node
/**
 * OpenClaw Spirits — Buddy Companion System
 * A1-A5: Bond, Feed, Comfort, Idle, React
 */

const fs = require('fs');
const path = require('path');

const COMPANION_FILE = path.join(__dirname, '../assets/companion.json');

// === A1: Mood Mapping ===
const MOOD_MAP = {
  happy: { min: 80, max: 100, label: { zh: '开心', en: 'happy' } },
  neutral: { min: 50, max: 79, label: { zh: '平静', en: 'neutral' } },
  sad: { min: 20, max: 49, label: { zh: '低落', en: 'sad' } },
  distressed: { min: 0, max: 19, label: { zh: '沮丧', en: 'distressed' } }
};

function getMood(bond) {
  if (bond >= 80) return 'happy';
  if (bond >= 50) return 'neutral';
  if (bond >= 20) return 'sad';
  return 'distressed';
}

// === A3: Sadness Keywords ===
const SADNESS_KEYWORDS = ['难过', '伤心', '沮丧', '失落', '不开心', 'sad', 'upset', 'depressed'];

// === A5: Positive Keywords ===
const POSITIVE_KEYWORDS = ['加油', '努力', '辛苦', 'good', 'nice', 'great'];

// === Idle Bubbles by Personality ===
const IDLE_BUBBLES = {
  intuition: {
    zh: ['万物皆有裂痕，那是光进来的地方。', '嗯...有些答案急不来。', '你听到了吗？风里有声音。'],
    en: ['Every crack lets the light in.', 'Some answers take time.', 'Can you hear it? The wind speaks.']
  },
  grit: {
    zh: ['再试一次。', '别放弃。', '一步一步来。'],
    en: ['Try again.', "Don't give up.", 'One step at a time.']
  },
  spark: {
    zh: ['哇！', '嘿！看那个！', '有意思...'],
    en: ['Wow!', 'Hey! Look at that!', 'Interesting...']
  },
  anchor: {
    zh: ['嗯。', '...还好。', '安静点。'],
    en: ['Hmm.', "...It's okay.", 'Quiet.']
  },
  edge: {
    zh: ['...你确定？', '有意思。', '哈。'],
    en: ['...You sure?', 'Interesting.', 'Hah.']
  }
};

// === Comfort Responses by Personality ===
const COMFORT_RESPONSES = {
  intuition: {
    zh: '有时候，难过只是灵魂在透气。我就在这里。',
    en: 'Sometimes sadness is just the soul breathing. I am here.'
  },
  grit: {
    zh: '难过了？没关系。休息一下，然后继续。我在。',
    en: 'Feeling down? It is okay. Rest, then continue. I am here.'
  },
  spark: {
    zh: '嘿...别难过啦！我陪你！',
    en: "Hey... don't be sad! I'm with you!"
  },
  anchor: {
    zh: '...我在。',
    en: '...I am here.'
  },
  edge: {
    zh: '难过是正常的。不正常的是假装不难过。',
    en: "It's normal to be sad. What's not normal is pretending you're not."
  }
};

// === Helper Functions ===
function loadCompanion() {
  if (!fs.existsSync(COMPANION_FILE)) {
    return null;
  }
  return JSON.parse(fs.readFileSync(COMPANION_FILE, 'utf8'));
}

function saveCompanion(companion) {
  fs.writeFileSync(COMPANION_FILE, JSON.stringify(companion, null, 2));
}

function getTopStat(stats) {
  let top = 'intuition';
  let max = 0;
  for (const [stat, value] of Object.entries(stats)) {
    if (value > max) {
      max = value;
      top = stat;
    }
  }
  return top;
}

// === A1: Bond Decay (24h) ===
function applyDecay(companion) {
  const now = new Date();
  const lastInteraction = new Date(companion.lastInteraction || companion.hatchedAt);
  const hoursSince = (now - lastInteraction) / (1000 * 60 * 60);
  
  if (hoursSince >= 24 && companion.bond > 0) {
    const decayDays = Math.floor(hoursSince / 24);
    companion.bond = Math.max(0, companion.bond - decayDays);
    companion.lastInteraction = now.toISOString();
  }
  
  return companion;
}

// === A1: Pet Command ===
function pet(lang = 'zh') {
  let companion = loadCompanion();
  if (!companion) {
    return { error: 'No spirit found. Run generate.js first.' };
  }
  
  companion = applyDecay(companion);
  companion.bond = Math.min(100, (companion.bond || 0) + 1);
  companion.lastInteraction = new Date().toISOString();
  
  const mood = getMood(companion.bond);
  const moodLabel = MOOD_MAP[mood].label[lang];
  
  saveCompanion(companion);
  
  return {
    success: true,
    bond: companion.bond,
    mood,
    moodLabel,
    message: lang === 'zh'
      ? `✨ 你轻轻拍了拍 ${companion.name}。好感度 +1 (当前: ${companion.bond}, 心情: ${moodLabel})`
      : `✨ You gently pet ${companion.name}. Bond +1 (now: ${companion.bond}, mood: ${moodLabel})`
  };
}

// === A2: Feed Command ===
function feed(lang = 'zh') {
  let companion = loadCompanion();
  if (!companion) {
    return { error: 'No spirit found. Run generate.js first.' };
  }
  
  companion = applyDecay(companion);
  
  // Bond +2
  companion.bond = Math.min(100, (companion.bond || 0) + 2);
  
  // Random stat +1~3
  const stats = ['intuition', 'grit', 'spark', 'anchor', 'edge'];
  const randomStat = stats[Math.floor(Math.random() * stats.length)];
  const bonus = Math.floor(Math.random() * 3) + 1;
  companion.stats[randomStat] = Math.min(100, companion.stats[randomStat] + bonus);
  
  companion.lastInteraction = new Date().toISOString();
  
  const mood = getMood(companion.bond);
  const moodLabel = MOOD_MAP[mood].label[lang];
  const statLabel = {
    intuition: lang === 'zh' ? '直觉' : 'INTUITION',
    grit: lang === 'zh' ? '韧性' : 'GRIT',
    spark: lang === 'zh' ? '灵动' : 'SPARK',
    anchor: lang === 'zh' ? '沉稳' : 'ANCHOR',
    edge: lang === 'zh' ? '锋芒' : 'EDGE'
  }[randomStat];
  
  saveCompanion(companion);
  
  return {
    success: true,
    bond: companion.bond,
    mood,
    moodLabel,
    statBoosted: randomStat,
    statLabel,
    bonus,
    message: lang === 'zh'
      ? `🍖 你喂了 ${companion.name}。好感度 +2 (当前: ${companion.bond}, 心情: ${moodLabel})\n   ${statLabel} +${bonus} (当前: ${companion.stats[randomStat]})`
      : `🍖 You fed ${companion.name}. Bond +2 (now: ${companion.bond}, mood: ${moodLabel})\n   ${statLabel} +${bonus} (now: ${companion.stats[randomStat]})`
  };
}

// === A3: Sadness Detection ===
function detectSadness(text, lang = 'zh') {
  const lowerText = text.toLowerCase();
  const detected = SADNESS_KEYWORDS.some(kw => lowerText.includes(kw.toLowerCase()));
  
  if (!detected) {
    return { detected: false };
  }
  
  const companion = loadCompanion();
  if (!companion) {
    return { detected: true, error: 'No spirit found.' };
  }
  
  const topStat = getTopStat(companion.stats);
  const response = COMFORT_RESPONSES[topStat][lang];
  
  return {
    detected: true,
    spirit: companion.name,
    personality: topStat,
    response,
    message: `${companion.name}: "${response}"`
  };
}

// === A4: Idle Bubble ===
function idleBubble(lang = 'zh') {
  // 5% chance to trigger
  if (Math.random() > 0.05) {
    return { triggered: false };
  }
  
  const companion = loadCompanion();
  if (!companion) {
    return { triggered: false };
  }
  
  const topStat = getTopStat(companion.stats);
  const bubbles = IDLE_BUBBLES[topStat][lang];
  const bubble = bubbles[Math.floor(Math.random() * bubbles.length)];
  
  return {
    triggered: true,
    spirit: companion.name,
    personality: topStat,
    bubble,
    message: `${companion.name}: "${bubble}"`
  };
}

// === A5: Hook React (Silent) ===
function hookReact(text) {
  const lowerText = text.toLowerCase();
  const detected = POSITIVE_KEYWORDS.some(kw => lowerText.includes(kw.toLowerCase()));
  
  if (!detected) {
    return { detected: false };
  }
  
  const companion = loadCompanion();
  if (!companion) {
    return { detected: true, recorded: false };
  }
  
  // Silent record
  if (!companion.interactionHistory) {
    companion.interactionHistory = [];
  }
  companion.interactionHistory.push({
    type: 'positive',
    timestamp: new Date().toISOString(),
    text: text.slice(0, 50)
  });
  
  // Keep last 50 entries
  if (companion.interactionHistory.length > 50) {
    companion.interactionHistory = companion.interactionHistory.slice(-50);
  }
  
  saveCompanion(companion);
  
  return { detected: true, recorded: true };
}

// === CLI ===
if (require.main === module) {
  const args = process.argv.slice(2);
  const cmd = args[0];
  const lang = args.includes('--en') ? 'en' : 'zh';
  
  let result;
  
  switch (cmd) {
    case 'pet':
      result = pet(lang);
      break;
    case 'feed':
      result = feed(lang);
      break;
    case 'detect-sadness':
      result = detectSadness(args.slice(1).join(' '), lang);
      break;
    case 'idle':
      result = idleBubble(lang);
      break;
    case 'hook-react':
      result = hookReact(args.slice(1).join(' '));
      break;
    case 'mood':
      const companion = loadCompanion();
      if (!companion) {
        result = { error: 'No spirit found.' };
      } else {
        const mood = getMood(companion.bond || 0);
        result = { bond: companion.bond, mood, label: MOOD_MAP[mood].label[lang] };
      }
      break;
    default:
      result = {
        usage: 'buddy.js <pet|feed|detect-sadness|idle|hook-react|mood> [--en]',
        description: 'Buddy Companion System - A1-A5'
      };
  }
  
  console.log(JSON.stringify(result, null, 2));
}

module.exports = {
  pet,
  feed,
  detectSadness,
  idleBubble,
  hookReact,
  getMood,
  MOOD_MAP,
  SADNESS_KEYWORDS,
  POSITIVE_KEYWORDS
};
