#!/usr/bin/env node

/**
 * Quota Manager สำหรับ Google Free Media Skill
 * จัดการและติดตาม quota การใช้งาน Gemini และ Google Flow
 */

import { readFileSync, writeFileSync, existsSync, mkdirSync, appendFileSync } from 'fs';
import { dirname, join } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const CONFIG_PATH = join(__dirname, '../configs/quota.json');
const LOG_PATH = join(__dirname, '../configs/quota_log.jsonl');

// Default config
const DEFAULT_CONFIG = {
  dailyLimits: {
    images: 100,
    videoCredits: 50
  },
  currentUsage: {
    images: 0,
    videoCredits: 0
  },
  lastReset: new Date().toISOString()
};

// อ่าน config
function loadConfig() {
  if (!existsSync(CONFIG_PATH)) {
    const configDir = dirname(CONFIG_PATH);
    if (!existsSync(configDir)) {
      mkdirSync(configDir, { recursive: true });
    }
    saveConfig(DEFAULT_CONFIG);
    return DEFAULT_CONFIG;
  }
  
  const content = readFileSync(CONFIG_PATH, 'utf-8');
  return JSON.parse(content);
}

// บันทึก config
function saveConfig(config) {
  writeFileSync(CONFIG_PATH, JSON.stringify(config, null, 2), 'utf-8');
}

// บันทึก log
function appendLog(entry) {
  const logEntry = {
    timestamp: new Date().toISOString(),
    ...entry
  };
  
  const logLine = JSON.stringify(logEntry) + '\n';
  
  if (!existsSync(LOG_PATH)) {
    const logDir = dirname(LOG_PATH);
    if (!existsSync(logDir)) {
      mkdirSync(logDir, { recursive: true });
    }
  }
  
  appendFileSync(LOG_PATH, logLine, 'utf-8');
}

// ตรวจสอบว่าต้อง reset หรือยัง (วันใหม่)
function shouldReset(config) {
  const lastReset = new Date(config.lastReset);
  const now = new Date();
  
  const lastResetDate = lastReset.toLocaleDateString('th-TH', { timeZone: 'Asia/Bangkok' });
  const nowDate = now.toLocaleDateString('th-TH', { timeZone: 'Asia/Bangkok' });
  
  return lastResetDate !== nowDate;
}

// Reset quota สำหรับวันใหม่
function resetQuota() {
  let config = loadConfig();
  
  config.currentUsage = {
    images: 0,
    videoCredits: 0
  };
  config.lastReset = new Date().toISOString();
  
  saveConfig(config);
  
  appendLog({ action: 'reset', usage: config.currentUsage });
  
  console.log('✅ Reset quota สำหรับวันใหม่แล้ว');
  console.log(`   รูป: 0 / ${config.dailyLimits.images}`);
  console.log(`   วิดีโอ credits: 0 / ${config.dailyLimits.videoCredits}`);
}

// ตรวจสอบ quota
function checkQuota() {
  let config = loadConfig();
  
  if (shouldReset(config)) {
    console.log('📅 ตรวจพบวันใหม่ กำลัง reset quota...');
    resetQuota();
    config = loadConfig();
  }
  
  const imagesRemaining = config.dailyLimits.images - config.currentUsage.images;
  const videoRemaining = config.dailyLimits.videoCredits - config.currentUsage.videoCredits;
  
  console.log('📊 Quota วันนี้ (Google Free Tier)');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log(`🖼️  รูปภาพ: ${imagesRemaining} / ${config.dailyLimits.images} เหลือ`);
  console.log(`   ใช้ไปแล้ว: ${config.currentUsage.images} รูป`);
  console.log('');
  console.log(`🎬 วิดีโอ: ${videoRemaining} / ${config.dailyLimits.videoCredits} credits เหลือ`);
  console.log(`   ใช้ไปแล้ว: ${config.currentUsage.videoCredits} credits`);
  console.log('');
  
  if (imagesRemaining < 20) {
    console.log('⚠️  WARNING: รูปเหลือไม่ถึง 20 รูป!');
  }
  if (videoRemaining < 10) {
    console.log('⚠️  WARNING: วิดีโอ credits เหลือไม่ถึง 10!');
  }
  
  return {
    images: {
      used: config.currentUsage.images,
      remaining: imagesRemaining,
      limit: config.dailyLimits.images
    },
    videos: {
      used: config.currentUsage.videoCredits,
      remaining: videoRemaining,
      limit: config.dailyLimits.videoCredits
    }
  };
}

// ใช้ quota
function consumeQuota(type, amount = 1) {
  let config = loadConfig();
  
  if (shouldReset(config)) {
    resetQuota();
    config = loadConfig();
  }
  
  if (type === 'image') {
    config.currentUsage.images += amount;
  } else if (type === 'video') {
    config.currentUsage.videoCredits += amount;
  }
  
  saveConfig(config);
  
  appendLog({ 
    action: 'consume', 
    type, 
    amount, 
    usage: config.currentUsage 
  });
  
  const remaining = type === 'image' 
    ? config.dailyLimits.images - config.currentUsage.images
    : config.dailyLimits.videoCredits - config.currentUsage.videoCredits;
  
  console.log(`✅ ใช้ ${type} quota ${amount} หน่วย`);
  console.log(`   เหลือ: ${remaining}`);
  
  return remaining;
}

// ดู log
function showLog(limit = 10) {
  if (!existsSync(LOG_PATH)) {
    console.log('📭 ยังไม่มี log การใช้งาน');
    return;
  }
  
  const content = readFileSync(LOG_PATH, 'utf-8');
  const lines = content.trim().split('\n').slice(-limit);
  
  console.log(`📜 Log การใช้งาน (${lines.length} รายการล่าสุด)`);
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  
  lines.forEach(line => {
    const entry = JSON.parse(line);
    const time = new Date(entry.timestamp).toLocaleString('th-TH');
    const action = entry.action === 'consume' 
      ? `ใช้ ${entry.type} ${entry.amount}` 
      : entry.action;
    console.log(`${time} - ${action}`);
  });
}

// Main
const args = process.argv.slice(2);
const command = args[0];

switch (command) {
  case 'check':
    checkQuota();
    break;
  case 'reset':
    resetQuota();
    break;
  case 'consume':
    const type = args[1];
    const amount = parseInt(args[2]) || 1;
    consumeQuota(type, amount);
    break;
  case 'log':
    const limit = parseInt(args[1]) || 10;
    showLog(limit);
    break;
  default:
    console.log('📦 Quota Manager - Google Free Media');
    console.log('');
    console.log('Usage:');
    console.log('  node quota_manager.mjs check   - ตรวจสอบ quota ที่เหลือ');
    console.log('  node quota_manager.mjs reset   - Reset quota ด้วยตนเอง');
    console.log('  node quota_manager.mjs consume <type> [amount] - ใช้ quota');
    console.log('  node quota_manager.mjs log [limit] - ดู log การใช้งาน');
    console.log('');
    console.log('Types: image, video');
}
