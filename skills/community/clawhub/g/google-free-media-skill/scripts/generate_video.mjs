#!/usr/bin/env node

/**
 * Google Flow Video Generator
 * สร้างวิดีโอ AI ฟรีผ่าน Google Flow (Veo 3.1) โดยใช้ browser automation
 */

import { execSync } from 'child_process';
import { writeFileSync, mkdirSync, existsSync, readFileSync } from 'fs';
import { dirname, join } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));

// Parse arguments
function parseArgs(args) {
  const result = {
    prompt: null,
    output: null,
    mode: 'text-to-video',
    image: null,
    duration: 8
  };
  
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--prompt' && args[i + 1]) {
      result.prompt = args[++i];
    } else if (args[i] === '--output' && args[i + 1]) {
      result.output = args[++i];
    } else if (args[i] === '--mode' && args[i + 1]) {
      result.mode = args[++i];
    } else if (args[i] === '--image' && args[i + 1]) {
      result.image = args[++i];
    } else if (args[i] === '--duration' && args[i + 1]) {
      result.duration = parseInt(args[++i]);
    }
  }
  
  return result;
}

// ตรวจสอบว่า browser พร้อมหรือไม่
function checkBrowser() {
  try {
    execSync('which google-chrome || which chromium || which chrome', { stdio: 'ignore' });
    console.log('✅ Browser พร้อมใช้งาน');
    return true;
  } catch (e) {
    console.error('❌ ไม่พบ Chrome/Chromium ในระบบ');
    console.error('');
    console.error('ติดตั้งด้วยคำสั่ง:');
    console.error('  Ubuntu/Debian: sudo apt install chromium-browser');
    console.error('  macOS: brew install --cask google-chrome');
    return false;
  }
}

// ตรวจสอบ input image (สำหรับ image-to-video mode)
function validateImage(imagePath) {
  if (!imagePath) {
    return true; // ไม่จำเป็นสำหรับ text-to-video
  }
  
  if (!existsSync(imagePath)) {
    console.error(`❌ ไม่พบไฟล์รูป: ${imagePath}`);
    return false;
  }
  
  const ext = imagePath.split('.').pop().toLowerCase();
  const validExts = ['jpg', 'jpeg', 'png', 'webp'];
  
  if (!validExts.includes(ext)) {
    console.error(`❌ ไฟล์รูปต้องเป็น: ${validExts.join(', ')}`);
    return false;
  }
  
  console.log(`✅ รูปต้นทาง: ${imagePath}`);
  return true;
}

// สร้างวิดีโอผ่าน Google Flow
async function generateWithFlow(prompt, outputPath, options) {
  console.log('🎬 กำลังสร้างวิดีโอผ่าน Google Flow (Veo 3.1)...');
  console.log('');
  
  // ตรวจสอบ quota ก่อน
  try {
    const quotaCheck = execSync(`node ${__dirname}/quota_manager.mjs check`, { encoding: 'utf-8' });
    console.log(quotaCheck);
  } catch (e) {
    console.log('⚠️  ไม่สามารถตรวจสอบ quota ได้ (ดำเนินการต่อ)');
  }
  
  // สร้าง output directory ถ้ายังไม่มี
  const outputDir = dirname(outputPath);
  if (!existsSync(outputDir)) {
    mkdirSync(outputDir, { recursive: true });
    console.log(`📁 สร้างโฟลเดอร์: ${outputDir}`);
  }
  
  console.log('');
  console.log(`🎯 Mode: ${options.mode}`);
  console.log(`⏱️  Duration: ${options.duration} วินาที`);
  console.log('');
  console.log('🌐 เปิด browser ไปยัง labs.google/flow...');
  console.log('📝 ส่ง prompt ให้ Veo 3.1...');
  console.log('⏳ รอ generate วิดีโอ (ปกติใช้เวลา 1-5 นาที)...');
  console.log('');
  
  // NOTE: นี่คือ skeleton script
  // การ implement จริงต้องใช้ Puppeteer/Playwright ควบคุม browser
  // ตัวอย่าง pseudo-code:
  /*
  const browser = await puppeteer.launch({ headless: false });
  const page = await browser.newPage();
  
  // ไป Google Flow
  await page.goto('https://labs.google/flow', { waitUntil: 'networkidle2' });
  
  // เลือก mode
  if (options.mode === 'image-to-video' && options.image) {
    // อัพโหลดรูป
    const uploadInput = await page.$('input[type="file"]');
    await uploadInput?.uploadFile(options.image);
    
    // รอรูปโหลด
    await page.waitForSelector('img[alt*="uploaded" i]', { timeout: 30000 });
  }
  
  // พิมพ์ prompt
  const textarea = await page.$('textarea[aria-label*="prompt" i]');
  await textarea?.type(prompt);
  
  // ตั้ง duration (ถ้ามี option)
  // ...
  
  // กด generate
  const generateButton = await page.$('button[aria-label*="generate" i]');
  await generateButton?.click();
  
  // รอวิดีโอ generate
  await page.waitForSelector('video[src]', { timeout: 300000 }); // 5 นาที
  
  // ดาวน์โหลดวิดีโอ
  const videoElement = await page.$('video');
  const src = await page.evaluate(el => el.src, videoElement);
  
  const response = await page.goto(src);
  const buffer = await response.buffer();
  writeFileSync(outputPath, buffer);
  
  await browser.close();
  */
  
  // Simulate success (สำหรับ demo)
  console.log('⚠️  SCRIPT DEMO MODE');
  console.log('');
  console.log('นี่คือ skeleton script สำหรับ demonstration');
  console.log('การ implement จริงต้อง:');
  console.log('  1. ติดตั้ง Puppeteer: npm install puppeteer');
  console.log('  2. Uncomment code ด้านบนและปรับ selector ให้ตรงกับ UI ปัจจุบัน');
  console.log('  3. Login Google ครั้งแรกผ่าน browser ปกติ');
  console.log('  4. รัน script นี้เพื่อสร้างวิดีโออัตโนมัติ');
  console.log('');
  console.log('📋 Google Flow (Veo 3.1) รองรับ:');
  console.log('   • Text to Video - สร้างวิดีโอจากข้อความ');
  console.log('   • Image to Video - animate รูปให้เป็นวิดีโอ');
  console.log('   • Video Extension - ต่อวิดีโอให้ยาวขึ้น');
  console.log('');
  
  // บันทึก placeholder
  const placeholder = {
    status: 'demo',
    prompt: prompt,
    outputPath: outputPath,
    mode: options.mode,
    duration: options.duration,
    timestamp: new Date().toISOString(),
    note: 'Implement browser automation with Puppeteer/Playwright'
  };
  
  writeFileSync(outputPath.replace('.mp4', '.json'), JSON.stringify(placeholder, null, 2), 'utf-8');
  
  // ใช้ quota
  try {
    execSync(`node ${__dirname}/quota_manager.mjs consume video 1`, { stdio: 'ignore' });
  } catch (e) {
    // Ignore quota errors
  }
  
  console.log('✅ เสร็จสิ้น (Demo Mode)');
  console.log(`   Output: ${outputPath}`);
}

// Main
const args = process.argv.slice(2);

if (args.length === 0 || args.includes('--help') || args.includes('-h')) {
  console.log('🎬 Google Flow Video Generator (Veo 3.1)');
  console.log('');
  console.log('Usage:');
  console.log('  node generate_video.mjs --prompt "คำอธิบายวิดีโอ" --output /path/to/output.mp4');
  console.log('');
  console.log('Options:');
  console.log('  --prompt <text>     คำอธิบายวิดีโอ (required)');
  console.log('  --output <path>     Path ไฟล์ output (required)');
  console.log('  --mode <mode>       โหมดการสร้าง: text-to-video, image-to-video (default: text-to-video)');
  console.log('  --image <path>      Path รูปต้นทาง (สำหรับ image-to-video)');
  console.log('  --duration <sec>    ระยะเวลาวิดีโอ 5-10 วินาที (default: 8)');
  console.log('');
  console.log('Examples:');
  console.log('  node generate_video.mjs --prompt "ocean waves at sunset" --output ./ocean.mp4');
  console.log('  node generate_video.mjs --prompt "cat running" --output ./cat.mp4 --mode image-to-video --image ./cat.jpg');
  console.log('  node generate_video.mjs --prompt "fireworks" --output ./fire.mp4 --duration 10');
  process.exit(0);
}

const options = parseArgs(args);

if (!options.prompt || !options.output) {
  console.error('❌ Error: --prompt และ --output เป็น required arguments');
  process.exit(1);
}

// Validate duration
if (options.duration < 5 || options.duration > 10) {
  console.log('⚠️  Duration ควรอยู่ระหว่าง 5-10 วินาที (ปรับเป็นค่าที่ใกล้เคียงที่สุด)');
  options.duration = Math.max(5, Math.min(10, options.duration));
}

// Validate mode
const validModes = ['text-to-video', 'image-to-video'];
if (!validModes.includes(options.mode)) {
  console.error(`❌ Mode ต้องเป็น: ${validModes.join(', ')}`);
  process.exit(1);
}

// Validate image (ถ้าเป็น image-to-video)
if (options.mode === 'image-to-video' && !validateImage(options.image)) {
  process.exit(1);
}

console.log('🎬 Google Flow Video Generator');
console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
console.log('');

// ตรวจสอบ browser
if (!checkBrowser()) {
  process.exit(1);
}

console.log('');

// สร้างวิดีโอ
generateWithFlow(options.prompt, options.output, options);
