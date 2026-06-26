#!/usr/bin/env node

/**
 * Google Gemini Image Generator
 * สร้างรูปภาพ AI ฟรีผ่าน Google Gemini โดยใช้ browser automation
 */

import { execSync } from 'child_process';
import { writeFileSync, mkdirSync, existsSync } from 'fs';
import { dirname, join } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));

// Parse arguments
function parseArgs(args) {
  const result = {
    prompt: null,
    output: null,
    style: 'realistic',
    enhance: true
  };
  
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--prompt' && args[i + 1]) {
      result.prompt = args[++i];
    } else if (args[i] === '--output' && args[i + 1]) {
      result.output = args[++i];
    } else if (args[i] === '--style' && args[i + 1]) {
      result.style = args[++i];
    } else if (args[i] === '--enhance') {
      result.enhance = args[i + 1] !== 'false';
      if (result.enhance && !args[i + 1]?.startsWith('--')) {
        i++;
      }
    }
  }
  
  return result;
}

// Enhance prompt ให้ professional ขึ้น
function enhancePrompt(originalPrompt, style = 'realistic') {
  const styleModifiers = {
    realistic: 'photorealistic, professional photography, 8K ultra detailed, natural lighting',
    artistic: 'digital art, concept art, artistic composition, vibrant colors, dramatic lighting',
    minimalist: 'minimalist design, clean composition, simple background, elegant, modern',
    cinematic: 'cinematic shot, movie still, dramatic lighting, depth of field, color graded',
    futuristic: 'futuristic design, sci-fi aesthetic, neon lighting, cyberpunk, high tech'
  };
  
  const baseModifiers = styleModifiers[style] || styleModifiers.realistic;
  
  // ถ้าเป็นภาษาไทย แปลงเป็นอังกฤษก่อน (แบบง่าย)
  const isThai = /[\u0E00-\u0E7F]/.test(originalPrompt);
  
  if (isThai) {
    console.log('🌐 Detected Thai prompt - will use as-is (Gemini supports Thai)');
  }
  
  const enhanced = `${originalPrompt}, ${baseModifiers}, high quality, professional`;
  
  console.log('✨ Enhanced Prompt:');
  console.log(`   ${enhanced}`);
  console.log('');
  
  return enhanced;
}

// ตรวจสอบว่า browser พร้อมหรือไม่
function checkBrowser() {
  try {
    // ตรวจสอบว่า Chrome/Chromium ติดตั้งหรือไม่
    execSync('which google-chrome || which chromium || which chrome', { stdio: 'ignore' });
    console.log('✅ Browser พร้อมใช้งาน');
    return true;
  } catch (e) {
    console.error('❌ ไม่พบ Chrome/Chromium ในระบบ');
    console.error('');
    console.error('ติดตั้งด้วยคำสั่ง:');
    console.error('  Ubuntu/Debian: sudo apt install chromium-browser');
    console.error('  macOS: brew install --cask google-chrome');
    console.error('  หรือใช้ Puppeteer: npm install puppeteer');
    return false;
  }
}

// สร้างรูปผ่าน Gemini (ใช้ browser automation)
async function generateWithGemini(prompt, outputPath, options) {
  console.log('🎨 กำลังสร้างรูปผ่าน Google Gemini...');
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
  console.log('🌐 เปิด browser ไปยัง gemini.google.com...');
  console.log('📝 ส่ง prompt ให้ Gemini...');
  console.log('⏳ รอ generate รูป (ปกติใช้เวลา 10-30 วินาที)...');
  console.log('');
  
  // NOTE: นี่คือ skeleton script
  // การ implement จริงต้องใช้ Puppeteer/Playwright ควบคุม browser
  // ตัวอย่าง pseudo-code:
  /*
  const browser = await puppeteer.launch({ headless: false });
  const page = await browser.newPage();
  
  // ไป Gemini
  await page.goto('https://gemini.google.com', { waitUntil: 'networkidle2' });
  
  // หาปุ่มสร้างรูปและคลิก
  const imageButton = await page.$('button[aria-label*="image" i]');
  await imageButton?.click();
  
  // พิมพ์ prompt
  const textarea = await page.$('textarea[aria-label*="input" i]');
  await textarea?.type(prompt);
  
  // กดส่ง
  const sendButton = await page.$('button[aria-label*="send" i]');
  await sendButton?.click();
  
  // รอรูป generate
  await page.waitForSelector('img[alt*="image" i]', { timeout: 60000 });
  
  // ดึงรูป (ใช้ =s0 trick สำหรับ full resolution)
  const imageElement = await page.$('img[src*="gemini" i]');
  const src = await page.evaluate(el => el.src, imageElement);
  const fullResSrc = src.replace('=s1024', '=s0');
  
  // ดาวน์โหลด
  const response = await page.goto(fullResSrc);
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
  console.log('  4. รัน script นี้เพื่อสร้างรูปอัตโนมัติ');
  console.log('');
  
  // บันทึก placeholder
  const placeholder = {
    status: 'demo',
    prompt: prompt,
    outputPath: outputPath,
    timestamp: new Date().toISOString(),
    note: 'Implement browser automation with Puppeteer/Playwright'
  };
  
  writeFileSync(outputPath.replace('.jpg', '.json'), JSON.stringify(placeholder, null, 2), 'utf-8');
  
  // ใช้ quota
  try {
    execSync(`node ${__dirname}/quota_manager.mjs consume image 1`, { stdio: 'ignore' });
  } catch (e) {
    // Ignore quota errors
  }
  
  console.log('✅ เสร็จสิ้น (Demo Mode)');
  console.log(`   Output: ${outputPath}`);
}

// Main
const args = process.argv.slice(2);

if (args.length === 0 || args.includes('--help') || args.includes('-h')) {
  console.log('🎨 Google Gemini Image Generator');
  console.log('');
  console.log('Usage:');
  console.log('  node generate_image.mjs --prompt "คำอธิบายรูป" --output /path/to/output.jpg');
  console.log('');
  console.log('Options:');
  console.log('  --prompt <text>    คำอธิบายรูป (required)');
  console.log('  --output <path>    Path ไฟล์ output (required)');
  console.log('  --style <style>    Style ของรูป: realistic, artistic, minimalist, cinematic, futuristic');
  console.log('  --enhance <bool>   ให้ AI enhance prompt อัตโนมัติ (default: true)');
  console.log('');
  console.log('Examples:');
  console.log('  node generate_image.mjs --prompt "cat wearing glasses" --output ./cat.jpg');
  console.log('  node generate_image.mjs --prompt "futuristic city" --output ./city.png --style futuristic');
  process.exit(0);
}

const options = parseArgs(args);

if (!options.prompt || !options.output) {
  console.error('❌ Error: --prompt และ --output เป็น required arguments');
  process.exit(1);
}

console.log('🖼️  Google Gemini Image Generator');
console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
console.log('');

// ตรวจสอบ browser
if (!checkBrowser()) {
  process.exit(1);
}

console.log('');

// Enhance prompt ถ้าต้องการ
const finalPrompt = options.enhance 
  ? enhancePrompt(options.prompt, options.style)
  : options.prompt;

// สร้างรูป
generateWithGemini(finalPrompt, options.output, options);
