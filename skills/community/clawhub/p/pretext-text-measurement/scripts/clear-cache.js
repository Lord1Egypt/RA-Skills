#!/usr/bin/env node
/**
 * Pretext Skill — 缓存清除脚本
 * 基于 @chenglou/pretext（MIT License）
 *
 * 功能：清除 Pretext 内部缓存（切换字体或清理内存时使用）
 * 用法：node clear-cache.js
 */

'use strict';

let Pretext = null;
try {
  Pretext = require('@chenglou/pretext');
} catch (e) {
  console.error(JSON.stringify({
    success: false,
    error: 'PRETEXT_NOT_INSTALLED',
    message: 'Pretext 未安装，请运行：cd ' + __dirname + ' && npm install'
  }, null, 2));
  process.exit(1);
}

try {
  if (typeof Pretext.clearCache === 'function') {
    Pretext.clearCache();
    console.log(JSON.stringify({
      success: true,
      message: 'Pretext 内部缓存已清除',
      tip: '下次 prepare() 将重新测量字符宽度，适用于切换大量不同字体时'
    }, null, 2));
  } else {
    console.log(JSON.stringify({
      success: true,
      message: '当前版本的 Pretext 不需要手动清除缓存',
      note: 'prepare() 会自动管理缓存，无需干预'
    }, null, 2));
  }
} catch (err) {
  console.error(JSON.stringify({
    success: false,
    error: 'CLEAR_CACHE_FAILED',
    message: err.message
  }, null, 2));
  process.exit(1);
}
