#!/usr/bin/env node
/**
 * 曼波音色 TTS 快速调用
 * Voice: zh-CN-XiaoyiNeural
 * Pitch: +8%
 */

const { spawn } = require('child_process');
const path = require('path');

const args = process.argv.slice(2);
if (args.length === 0) {
  console.error('用法: node mambo.js "你的文本"');
  process.exit(1);
}

const text = args.join(' ');
const edgeTtsScript = path.join(__dirname, '..', '..', 'edge-tts', 'scripts', 'tts-converter.js');

const child = spawn('node', [
  edgeTtsScript,
  text,
  '--voice', 'zh-CN-XiaoyiNeural',
  '--pitch', '+8%'
], { stdio: 'inherit' });

child.on('exit', (code) => process.exit(code));
