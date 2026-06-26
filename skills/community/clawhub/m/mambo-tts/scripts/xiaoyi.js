#!/usr/bin/env node
/**
 * 晓伊音色 TTS 快速调用
 * Voice: zh-CN-XiaoyiNeural
 * Rate: +30% (快节奏)
 */

const { spawn } = require('child_process');
const path = require('path');

const args = process.argv.slice(2);
if (args.length === 0) {
  console.error('用法: node xiaoyi.js "你的文本"');
  process.exit(1);
}

const text = args.join(' ');
const edgeTtsScript = path.join(__dirname, '..', '..', 'edge-tts', 'scripts', 'tts-converter.js');

const child = spawn('node', [
  edgeTtsScript,
  text,
  '--voice', 'zh-CN-XiaoyiNeural',
  '--rate', '+30%'
], { stdio: 'inherit' });

child.on('exit', (code) => process.exit(code));
