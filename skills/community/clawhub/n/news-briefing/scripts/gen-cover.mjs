#!/usr/bin/env node
/**
 * 生成 news-briefing skill 封面图
 * 输出: /root/.openclaw/workspace/skills/news-briefing/cover.png
 */
import { execSync } from 'child_process';
import { writeFileSync } from 'fs';

const code = `
const { createCanvas, GlobalFonts } = require('@napi-rs/canvas');

// 注册中文字体
GlobalFonts.registerFromPath('/usr/share/fonts/google-noto-cjk/NotoSansCJK-Regular.ttc', 'NotoSansCJK');
GlobalFonts.registerFromPath('/usr/share/fonts/google-noto-cjk/NotoSansCJK-Medium.ttc', 'NotoSansCJKMedium');

const W = 1200, H = 630;
const canvas = createCanvas(W, H);
const ctx = canvas.getContext('2d');

// 背景渐变 - 深海蓝黑
const bg = ctx.createLinearGradient(0, 0, W, H);
bg.addColorStop(0, '#0a0e1a');
bg.addColorStop(0.5, '#0d1525');
bg.addColorStop(1, '#070b14');
ctx.fillStyle = bg;
ctx.fillRect(0, 0, W, H);

// 网格线装饰（情报感）
ctx.strokeStyle = 'rgba(30, 80, 160, 0.15)';
ctx.lineWidth = 1;
for (let x = 0; x < W; x += 60) {
  ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, H); ctx.stroke();
}
for (let y = 0; y < H; y += 60) {
  ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(W, y); ctx.stroke();
}

// 左侧装饰竖线
const lineGrad = ctx.createLinearGradient(0, 0, 0, H);
lineGrad.addColorStop(0, 'rgba(0,180,255,0)');
lineGrad.addColorStop(0.3, 'rgba(0,180,255,0.8)');
lineGrad.addColorStop(0.7, 'rgba(100,220,255,0.8)');
lineGrad.addColorStop(1, 'rgba(0,180,255,0)');
ctx.strokeStyle = lineGrad;
ctx.lineWidth = 3;
ctx.shadowColor = 'rgba(0,180,255,0.6)';
ctx.shadowBlur = 12;
ctx.beginPath(); ctx.moveTo(72, 0); ctx.lineTo(72, H); ctx.stroke();
ctx.shadowBlur = 0;

// 右上角装饰圆
const circleGrad = ctx.createRadialGradient(W-100, 100, 0, W-100, 100, 200);
circleGrad.addColorStop(0, 'rgba(0,120,255,0.15)');
circleGrad.addColorStop(1, 'rgba(0,120,255,0)');
ctx.fillStyle = circleGrad;
ctx.beginPath(); ctx.arc(W-100, 100, 200, 0, Math.PI*2); ctx.fill();

// 顶部标签
ctx.fillStyle = 'rgba(0,180,255,0.15)';
ctx.strokeStyle = 'rgba(0,180,255,0.5)';
ctx.lineWidth = 1;
const tagX = 100, tagY = 60;
roundRect(ctx, tagX, tagY, 160, 34, 6);
ctx.fill();
ctx.stroke();
ctx.fillStyle = '#00b4ff';
ctx.font = '13px NotoSansCJK';
ctx.fillText('OpenClaw Skill', tagX + 14, tagY + 22);

// 主标题 "NEWS"
ctx.shadowColor = 'rgba(0,180,255,0.4)';
ctx.shadowBlur = 30;
ctx.fillStyle = '#ffffff';
ctx.font = 'bold 130px NotoSansCJKMedium';
ctx.fillText('NEWS', 100, 260);

// 副标题 "BRIEFING"
const briefGrad = ctx.createLinearGradient(100, 260, 700, 380);
briefGrad.addColorStop(0, '#00b4ff');
briefGrad.addColorStop(1, '#00e5ff');
ctx.fillStyle = briefGrad;
ctx.font = 'bold 130px NotoSansCJKMedium';
ctx.shadowColor = 'rgba(0,180,255,0.6)';
ctx.shadowBlur = 40;
ctx.fillText('BRIEFING', 100, 380);
ctx.shadowBlur = 0;

// 分隔线
const sepGrad = ctx.createLinearGradient(100, 410, 800, 410);
sepGrad.addColorStop(0, 'rgba(0,180,255,0.8)');
sepGrad.addColorStop(1, 'rgba(0,180,255,0)');
ctx.strokeStyle = sepGrad;
ctx.lineWidth = 2;
ctx.beginPath(); ctx.moveTo(100, 415); ctx.lineTo(800, 415); ctx.stroke();

// 功能标签行
const tags = ['🔍 实时联网搜索', '🧠 AI深度洞察', '📱 飞书卡片推送', '🌏 任意话题'];
let tx = 100;
tags.forEach(tag => {
  ctx.font = '18px NotoSansCJK';
  const tw = ctx.measureText(tag).width;
  ctx.fillStyle = 'rgba(0,100,180,0.3)';
  ctx.strokeStyle = 'rgba(0,180,255,0.4)';
  ctx.lineWidth = 1;
  roundRect(ctx, tx, 435, tw + 24, 34, 8);
  ctx.fill(); ctx.stroke();
  ctx.fillStyle = 'rgba(200,230,255,0.9)';
  ctx.fillText(tag, tx + 12, 457);
  tx += tw + 40;
});

// 底部描述
ctx.fillStyle = 'rgba(140,170,210,0.8)';
ctx.font = '20px NotoSansCJK';
ctx.fillText('让 AI Agent 成为你的私人情报官 · 一句话触发任意话题简报', 100, 520);

// 右侧装饰 — 卡片预览示意
drawMiniCard(ctx, W - 340, 160);

// 右下角作者
ctx.fillStyle = 'rgba(80,120,180,0.6)';
ctx.font = '16px NotoSansCJK';
ctx.fillText('by derekhsu529 · clawhub.com', W - 320, H - 30);

const buf = canvas.toBuffer('image/png');
require('fs').writeFileSync('/root/.openclaw/workspace/skills/news-briefing/cover.png', buf);
console.log('done');

function roundRect(ctx, x, y, w, h, r) {
  ctx.beginPath();
  ctx.moveTo(x+r, y); ctx.lineTo(x+w-r, y);
  ctx.arcTo(x+w, y, x+w, y+r, r);
  ctx.lineTo(x+w, y+h-r);
  ctx.arcTo(x+w, y+h, x+w-r, y+h, r);
  ctx.lineTo(x+r, y+h);
  ctx.arcTo(x, y+h, x, y+h-r, r);
  ctx.lineTo(x, y+r);
  ctx.arcTo(x, y, x+r, y, r);
  ctx.closePath();
}

function drawMiniCard(ctx, x, y) {
  // 卡片背景
  ctx.fillStyle = 'rgba(15,30,60,0.8)';
  ctx.strokeStyle = 'rgba(0,180,255,0.3)';
  ctx.lineWidth = 1;
  roundRect(ctx, x, y, 290, 380, 12);
  ctx.fill(); ctx.stroke();

  // 卡片标题
  ctx.fillStyle = 'rgba(0,180,255,0.8)';
  ctx.font = '14px NotoSansCJK';
  ctx.fillText('📰 AI情报简报', x+16, y+30);

  // 模拟新闻条目
  const items = [
    { emoji: '🧠', title: 'OpenAI发布o3模型...', tag: 'AI' },
    { emoji: '🌍', title: '全人代开幕李强宣布...', tag: 'GEO' },
    { emoji: '⚾', title: '大谷翔平WBC首战...', tag: 'SPORT' },
  ];

  let iy = y + 55;
  items.forEach(item => {
    ctx.fillStyle = 'rgba(30,60,100,0.6)';
    roundRect(ctx, x+12, iy, 266, 80, 8);
    ctx.fill();

    ctx.fillStyle = 'rgba(200,225,255,0.9)';
    ctx.font = '13px NotoSansCJK';
    ctx.fillText(item.emoji + ' ' + item.title, x+20, iy+22);

    ctx.fillStyle = 'rgba(140,170,210,0.7)';
    ctx.font = '11px NotoSansCJK';
    ctx.fillText('摘要：50-60字，中文，手机友好...', x+20, iy+42);

    ctx.fillStyle = 'rgba(0,140,220,0.5)';
    roundRect(ctx, x+20, iy+52, 75, 18, 4);
    ctx.fill();
    ctx.fillStyle = 'rgba(150,210,255,0.9)';
    ctx.font = '10px NotoSansCJK';
    ctx.fillText('📄 查看原文', x+26, iy+64);

    ctx.fillStyle = 'rgba(255,200,50,0.15)';
    roundRect(ctx, x+105, iy+52, 80, 18, 4);
    ctx.fill();
    ctx.fillStyle = 'rgba(255,220,100,0.8)';
    ctx.fillText('💡 AI洞察 ▼', x+111, iy+64);

    iy += 96;
  });
}
`;

const canvasPath = '/root/.local/share/pnpm/global/5/.pnpm/openclaw@2026.2.26_@napi-rs+canvas@0.1.95_@types+express@5.0.6_hono@4.12.3_node-llama-cpp@3.15.1/node_modules/@napi-rs/canvas';

writeFileSync('/tmp/gen-cover.js', code);
execSync(`node -e "const {createCanvas,GlobalFonts}=require('${canvasPath}');${code.replace(/^const.*napi.*\n/, '')}"`, { stdio: 'inherit' });
