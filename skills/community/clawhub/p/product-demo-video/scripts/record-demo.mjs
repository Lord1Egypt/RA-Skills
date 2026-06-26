#!/usr/bin/env node
/**
 * Product Demo Video Recorder
 * 
 * Records browser interactions with voiceover and text overlays.
 * Customize SCENES array for your app.
 * 
 * Usage: node record-demo.mjs
 * 
 * Prerequisites: Run install-deps.sh first
 */

import { createRequire } from 'module';
const require = createRequire(import.meta.url);

// Try global puppeteer, fallback to local
let puppeteer;
try { puppeteer = require('puppeteer'); } catch(e) {
  try { puppeteer = require('/usr/lib/node_modules/puppeteer'); } catch(e2) {
    console.error('❌ Puppeteer not found. Run: npm i -g puppeteer');
    process.exit(1);
  }
}

import { execSync } from 'child_process';
import fs from 'fs';
import path from 'path';

// ==================== CONFIGURATION ====================

const CONFIG = {
  width: 1280,
  height: 720,
  captureFps: 6,         // Frames per second during capture
  outputFps: 24,         // Output video frame rate
  crf: 20,               // Video quality (lower = better, 18-23 recommended)
  voice: 'en-US-AndrewNeural',  // edge-tts voice
  voiceRate: '+5%',      // Speech rate adjustment
  chromePath: '/usr/bin/chromium-browser',  // Adjust for your system
  workDir: '/tmp/demo-video-work',
  output: './demo-video.mp4',
  fontBold: '/usr/share/fonts/google-noto/NotoSans-Bold.ttf',
  fontReg: '/usr/share/fonts/google-noto/NotoSans-Regular.ttf',
};

// ==================== SCENES ====================
// Customize this array for YOUR app

const SCENES = [
  {
    id: 'intro',
    title: 'YourApp.dev',
    subtitle: 'Your tagline here',
    badge: 'Your data never leaves your device',
    narration: 'Welcome to YourApp. A brief description of what your product does.',
    url: 'https://yourapp.dev/',
    type: 'intro',  // 'intro' | 'tool' | 'outro'
    actions: async (page) => {
      await page.waitForSelector('h1', { timeout: 10000 });
    }
  },
  {
    id: 'feature1',
    title: 'Feature Name',
    subtitle: 'What this feature does in one line',
    narration: 'Describe this feature and why it matters.',
    url: 'https://yourapp.dev/feature1/',
    type: 'tool',
    actions: async (page) => {
      // Example: type into a React input and click a button
      await reactSetValue(page, 'textarea', 'sample input data');
      await wait(1000);
      await clickButton(page, ['Submit', 'Run', 'Generate']);
      await wait(2500);
    }
  },
  {
    id: 'outro',
    title: 'Try YourApp Today',
    subtitle: 'yourapp.dev  |  Free  |  No Sign-up',
    narration: 'Visit yourapp.dev and try it yourself. Its free and always will be.',
    url: 'https://yourapp.dev/',
    type: 'outro',
    actions: async (page) => {
      for (let i = 0; i < 4; i++) {
        await page.evaluate(() => window.scrollBy(0, 300));
        await wait(400);
      }
      await page.evaluate(() => window.scrollTo({ top: 0, behavior: 'smooth' }));
      await wait(500);
    }
  }
];

// ==================== HELPERS ====================

async function wait(ms) { return new Promise(r => setTimeout(r, ms)); }

// React-compatible value setter — triggers React's internal onChange
async function reactSetValue(page, selector, value) {
  await page.evaluate((sel, val) => {
    const el = document.querySelector(sel);
    if (!el) return;
    const setter = Object.getOwnPropertyDescriptor(
      el.tagName === 'TEXTAREA'
        ? window.HTMLTextAreaElement.prototype
        : window.HTMLInputElement.prototype,
      'value'
    )?.set;
    if (setter) setter.call(el, val);
    else el.value = val;
    el.dispatchEvent(new Event('input', { bubbles: true }));
    el.dispatchEvent(new Event('change', { bubbles: true }));
  }, selector, value);
}

async function clickButton(page, texts) {
  const buttons = await page.$$('button');
  for (const btn of buttons) {
    const text = await btn.evaluate(el => el.textContent?.trim());
    if (text && texts.some(t => text.includes(t))) {
      await btn.click();
      return true;
    }
  }
  return false;
}

// ==================== MAIN ====================

async function main() {
  const { workDir, output, voice, voiceRate, captureFps, outputFps, crf,
          width, height, chromePath, fontBold, fontReg } = CONFIG;
  const audioDir = `${workDir}/audio`;
  
  fs.mkdirSync(audioDir, { recursive: true });

  // ===== STEP 1: Generate voiceover =====
  console.log('🎙️  Generating voiceover...');
  for (const s of SCENES) {
    const audioPath = `${audioDir}/${s.id}.mp3`;
    execSync(`edge-tts --voice ${voice} --rate=${voiceRate} --text "${s.narration.replace(/"/g, '\\"')}" --write-media ${audioPath}`);
    const dur = parseFloat(execSync(`ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 ${audioPath}`).toString().trim());
    s.audioDuration = dur;
    s.duration = Math.max(8, Math.ceil(dur) + 2);
    console.log(`  ${s.id}: audio=${dur.toFixed(1)}s, scene=${s.duration}s`);
  }

  // ===== STEP 2: Record browser scenes =====
  console.log('\n📹 Recording scenes...');
  const browser = await puppeteer.launch({
    headless: true,
    executablePath: chromePath,
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu', '--disable-dev-shm-usage'],
  });
  const page = await browser.newPage();
  await page.setViewport({ width, height });

  for (const s of SCENES) {
    console.log(`  Recording: ${s.id} (${s.duration}s)...`);
    const dir = `${workDir}/frames_${s.id}`;
    fs.mkdirSync(dir, { recursive: true });
    try { fs.readdirSync(dir).forEach(f => fs.unlinkSync(`${dir}/${f}`)); } catch(e) {}

    await page.goto(s.url, { waitUntil: 'networkidle2', timeout: 30000 });
    await wait(600);
    await s.actions(page);
    await wait(300);

    const totalFrames = s.duration * captureFps;
    for (let f = 0; f < totalFrames; f++) {
      await page.screenshot({ path: `${dir}/frame_${String(f).padStart(5, '0')}.png` });
    }
  }
  await browser.close();

  // ===== STEP 3: Add text overlays with PIL =====
  console.log('\n✍️  Adding text overlays...');
  const pyScript = generateOverlayScript(SCENES, workDir, captureFps, fontBold, fontReg);
  fs.writeFileSync(`${workDir}/overlay.py`, pyScript);
  execSync(`python3 ${workDir}/overlay.py`, { stdio: 'inherit' });

  // ===== STEP 4: Compile each scene with audio =====
  console.log('\n🎬 Compiling scenes...');
  for (const s of SCENES) {
    execSync(`ffmpeg -y -framerate ${captureFps} -i ${workDir}/overlay_${s.id}/frame_%05d.png -c:v libx264 -preset slow -crf ${crf} -pix_fmt yuv420p -r ${outputFps} ${workDir}/${s.id}_video.mp4 2>/dev/null`);
    execSync(`ffmpeg -y -i ${workDir}/${s.id}_video.mp4 -i ${audioDir}/${s.id}.mp3 -c:v copy -c:a aac -b:a 128k -shortest ${workDir}/${s.id}_final.mp4 2>/dev/null`);
    execSync(`ffmpeg -y -i ${workDir}/${s.id}_final.mp4 -c:v libx264 -preset slow -crf ${crf} -pix_fmt yuv420p -r ${outputFps} -c:a aac -b:a 128k -ar 44100 -ac 2 ${workDir}/${s.id}_norm.mp4 2>/dev/null`);
    console.log(`  ${s.id} ✓`);
  }

  // ===== STEP 5: Concatenate =====
  console.log('\n📼 Concatenating...');
  const concatList = SCENES.map(s => `file '${workDir}/${s.id}_norm.mp4'`).join('\n');
  fs.writeFileSync(`${workDir}/concat.txt`, concatList);
  
  const outputPath = path.resolve(output);
  fs.mkdirSync(path.dirname(outputPath), { recursive: true });
  execSync(`ffmpeg -y -f concat -safe 0 -i ${workDir}/concat.txt -c copy ${outputPath} 2>/dev/null`);

  const stat = fs.statSync(outputPath);
  const totalDur = parseFloat(execSync(`ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 ${outputPath}`).toString().trim());
  
  console.log(`\n✅ Demo video complete!`);
  console.log(`   File: ${outputPath}`);
  console.log(`   Size: ${(stat.size / 1024 / 1024).toFixed(1)} MB`);
  console.log(`   Duration: ${totalDur.toFixed(1)}s`);
  console.log(`   Scenes: ${SCENES.length}`);
  console.log(`   Voice: ${voice}`);
}

// ==================== OVERLAY GENERATOR ====================

function generateOverlayScript(scenes, workDir, fps, fontBold, fontReg) {
  const scenesJson = JSON.stringify(scenes.map(s => ({
    id: s.id, title: s.title, subtitle: s.subtitle, 
    badge: s.badge || '', type: s.type, duration: s.duration
  })));
  
  return `
import os, glob
from PIL import Image, ImageDraw, ImageFont

FONT_BOLD = '${fontBold}'
FONT_REG = '${fontReg}'
WORK = '${workDir}'
FPS = ${fps}
GREEN = (74, 222, 128)

scenes = ${scenesJson}

def add_overlay(img, scene, frame_idx):
    draw = ImageDraw.Draw(img, 'RGBA')
    w, h = img.size
    
    try:
        font_title = ImageFont.truetype(FONT_BOLD, 44 if scene['type'] == 'intro' else 36)
        font_sub = ImageFont.truetype(FONT_REG, 20 if scene['type'] == 'intro' else 18)
        font_badge = ImageFont.truetype(FONT_REG, 16)
    except:
        font_title = ImageFont.load_default()
        font_sub = font_title
        font_badge = font_title
    
    if frame_idx < int(0.3 * FPS):
        return img
    
    if scene['type'] == 'intro':
        bar_h = 170
        draw.rectangle([(0, h-bar_h), (w, h)], fill=(10,10,10,235))
        draw.rectangle([(0, h-bar_h-2), (w, h-bar_h)], fill=(*GREEN, 200))
        bbox = draw.textbbox((0,0), scene['title'], font=font_title)
        tw = bbox[2] - bbox[0]
        draw.text(((w-tw)//2, h-bar_h+18), scene['title'], fill='white', font=font_title)
        bbox2 = draw.textbbox((0,0), scene['subtitle'], font=font_sub)
        tw2 = bbox2[2] - bbox2[0]
        draw.text(((w-tw2)//2, h-bar_h+72), scene['subtitle'], fill=(255,255,255,220), font=font_sub)
        badge = scene.get('badge', '')
        if badge and frame_idx > int(1.0 * FPS):
            bbox3 = draw.textbbox((0,0), badge, font=font_badge)
            tw3 = bbox3[2] - bbox3[0]
            draw.text(((w-tw3)//2, h-bar_h+108), badge, fill=(*GREEN, 255), font=font_badge)
    
    elif scene['type'] == 'outro':
        bar_h = 150
        draw.rectangle([(0, h-bar_h), (w, h)], fill=(10,10,10,240))
        draw.rectangle([(0, h-bar_h-2), (w, h-bar_h)], fill=(*GREEN, 200))
        bbox = draw.textbbox((0,0), scene['title'], font=font_title)
        tw = bbox[2] - bbox[0]
        draw.text(((w-tw)//2, h-bar_h+20), scene['title'], fill='white', font=font_title)
        bbox2 = draw.textbbox((0,0), scene['subtitle'], font=font_sub)
        tw2 = bbox2[2] - bbox2[0]
        draw.text(((w-tw2)//2, h-bar_h+72), scene['subtitle'], fill=(*GREEN, 255), font=font_sub)
    
    else:
        bar_h = 75
        draw.rectangle([(0, h-bar_h), (w, h)], fill=(10,10,10,235))
        draw.rectangle([(0, h-bar_h-2), (w, h-bar_h)], fill=(*GREEN, 180))
        draw.text((18, h-bar_h+10), scene['title'], fill='white', font=font_title)
        draw.text((18, h-bar_h+46), scene['subtitle'], fill=(255,255,255,210), font=font_sub)
        privacy_text = '100% Client-Side'
        bbox_p = draw.textbbox((0,0), privacy_text, font=font_badge)
        pw = bbox_p[2] - bbox_p[0]
        draw.text((w-pw-18, h-bar_h+14), privacy_text, fill=(*GREEN, 230), font=font_badge)
    
    return img

for scene in scenes:
    sid = scene['id']
    frame_dir = f'{WORK}/frames_{sid}'
    out_dir = f'{WORK}/overlay_{sid}'
    os.makedirs(out_dir, exist_ok=True)
    frames = sorted(glob.glob(f'{frame_dir}/frame_*.png'))
    for i, fp in enumerate(frames):
        img = Image.open(fp).convert('RGBA')
        img = add_overlay(img, scene, i)
        img.convert('RGB').save(f'{out_dir}/frame_{i:05d}.png')
    print(f'  {sid}: {len(frames)} frames overlaid')
print('Done')
`;
}

main().catch(console.error);
