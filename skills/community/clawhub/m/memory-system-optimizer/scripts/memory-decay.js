#!/usr/bin/env node
/**
 * memory-decay.js - 记忆温度分档
 * Hot: 7天内访问
 * Warm: 8-30天访问
 * Cold: 30+天未访问
 */

const fs = require('fs');
const path = require('path');

const WORKSPACE = process.env.HOME + '/.openclaw/workspace';
const LIFE_DIR = path.join(WORKSPACE, 'life');

function categorize(items) {
  const now = new Date();
  const hot = [], warm = [], cold = [];
  
  items.forEach(item => {
    const days = Math.floor((now - new Date(item.lastAccessed || item.timestamp)) / (1000*60*60*24));
    if (days <= 7) hot.push(item);
    else if (days <= 30) warm.push(item);
    else cold.push(item);
  });
  
  return { hot, warm, cold };
}

console.log('=== Memory Decay ===');
console.log('Hot: ≤7天 | Warm: 8-30天 | Cold: >30天');
console.log('=== Done ===');
