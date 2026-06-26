#!/usr/bin/env node

/**
 * 核心压缩逻辑
 * 支持单图/批量压缩、格式转换、画质调节、尺寸限制
 * 
 * 改进功能：
 * - 命令行参数解析（commander）
 * - 压缩预设（web/wechat/email/quality）
 * - 进度显示（批量压缩）
 * - 大文件警告（>50MB）
 * - 美观的报告输出
 */

import sharp from 'sharp';
import { readdirSync, statSync, existsSync, mkdirSync, readFileSync } from 'fs';
import { join, extname, basename, dirname, relative } from 'path';
import { homedir } from 'os';
import { program } from 'commander';

const SUPPORTED_FORMATS = ['.jpg', '.jpeg', '.png', '.webp', '.gif', '.bmp', '.heic', '.heif'];

// 压缩预设
const PRESETS = {
  web: { quality: 0.75, description: '网页优化' },
  wechat: { quality: 0.65, description: '微信发送' },
  email: { quality: 0.55, description: '邮件附件' },
  quality: { quality: 0.95, description: '高质量存档' },
  default: { quality: 0.85, description: '默认' }
};

// 大文件阈值（50MB）
const LARGE_FILE_THRESHOLD = 50 * 1024 * 1024;

// 配置命令行参数
function setupCommander() {
  program
    .argument('<input>', '输入文件或文件夹路径')
    .option('-f, --format <format>', '输出格式 (jpg, png, webp, avif)', 'original')
    .option('-q, --quality <quality>', '画质 (0.1-1.0)', '0.85')
    .option('-w, --maxWidth <width>', '最大宽度', '')
    .option('-h, --maxHeight <height>', '最大高度', '')
    .option('-r, --recursive', '递归处理子文件夹', false)
    .option('-o, --outputDir <dir>', '输出目录', '')
    .option('-p, --preset <preset>', '压缩预设 (web, wechat, email, quality)', '')
    .option('--no-confirm', '跳过确认提示', false)
    .action(compress);
  
  program.parse();
}

// 获取唯一输出路径（避免覆盖）
function getUniquePath(outputDir, filename) {
  let targetPath = join(outputDir, filename);
  
  if (!existsSync(targetPath)) {
    return targetPath;
  }
  
  const ext = extname(filename);
  const base = basename(filename, ext);
  let counter = 1;
  
  while (existsSync(targetPath)) {
    const newName = `${base}_${String(counter).padStart(3, '0')}${ext}`;
    targetPath = join(outputDir, newName);
    counter++;
  }
  
  return targetPath;
}

// 获取输出目录（按日期分组）
function getTodayOutputDir(baseDir) {
  const today = new Date().toISOString().split('T')[0];
  const outputDir = join(baseDir, today);
  
  if (!existsSync(outputDir)) {
    mkdirSync(outputDir, { recursive: true });
  }
  
  return outputDir;
}

// 检查大文件
function checkLargeFile(filePath) {
  const stats = statSync(filePath);
  const sizeMB = (stats.size / (1024 * 1024)).toFixed(1);
  
  if (stats.size > LARGE_FILE_THRESHOLD) {
    console.log(`\n⚠️  文件较大 (${sizeMB} MB)`);
    console.log('   压缩可能需要较长时间，确定继续吗？[Y/n]');
    return true;
  }
  return false;
}

// 单图压缩
async function compressImage(inputPath, options) {
  const {
    outputDir,
    quality = 0.85,
    format = 'original',
    maxWidth = null,
    maxHeight = null
  } = options;
  
  // 验证输入文件
  if (!existsSync(inputPath)) {
    throw new Error(`文件不存在：${inputPath}`);
  }
  
  const ext = extname(inputPath).toLowerCase();
  if (!SUPPORTED_FORMATS.includes(ext)) {
    throw new Error(`不支持的文件格式：${ext}`);
  }
  
  // 大文件检查
  const stats = statSync(inputPath);
  const sizeMB = (stats.size / (1024 * 1024)).toFixed(1);
  
  if (stats.size > LARGE_FILE_THRESHOLD && !options.noConfirm) {
    console.log(`\n⚠️  文件较大 (${sizeMB} MB)`);
    console.log('   压缩可能需要较长时间，确定继续吗？[Y/n]');
    
    // 简单处理：继续执行（实际可以用 readline 等待用户输入）
  }
  
  const originalSize = stats.size;
  
  // 确定输出格式
  let outputFormat = format === 'original' ? ext.replace('.', '') : format;
  if (outputFormat === 'jpg') outputFormat = 'jpeg';
  
  // 确定输出文件名
  const filename = basename(inputPath);
  const outputFilename = format === 'original' ? filename : `${basename(filename, ext)}.${outputFormat === 'jpeg' ? 'jpg' : outputFormat}`;
  
  // 获取唯一输出路径
  const todayDir = getTodayOutputDir(outputDir);
  const outputPath = getUniquePath(todayDir, outputFilename);
  
  // 构建 sharp 处理链
  let processor = sharp(inputPath);
  
  // 处理 PNG→JPG 的透明通道（白色背景）
  if (ext === '.png' && outputFormat === 'jpeg') {
    processor = processor.flatten({ background: { r: 255, g: 255, b: 255, alpha: 1 } });
  }
  
  // 尺寸限制
  if (maxWidth || maxHeight) {
    processor = processor.resize({
      width: maxWidth || undefined,
      height: maxHeight || undefined,
      fit: 'inside',
      withoutEnlargement: true
    });
  }
  
  // 格式转换和压缩
  const formatOptions = { quality: Math.round(quality * 100) };
  
  if (outputFormat === 'jpeg') {
    processor = processor.jpeg({
      quality: formatOptions.quality,
      progressive: true,      // 渐进式加载
      mozjpeg: false,         // 使用 mozjpeg（更好压缩）
      strip: true             // 移除元数据
    });
  } else if (outputFormat === 'png') {
    // 优化 PNG 压缩（类似 TinyPNG 的智能压缩）
    processor = processor.png({
      compressionLevel: 9,    // 最大压缩级别
      palette: true,          // 启用颜色量化（关键！）
      colors: 256,            // 减少到 256 色
      dither: 1,              // 抖动处理，减少色带
      strip: true,            // 移除元数据
      progressive: false
    });
  } else if (outputFormat === 'webp') {
    processor = processor.webp({
      quality: formatOptions.quality,
      alphaQuality: formatOptions.quality,
      lossless: false,
      nearLossless: false,
      smartSubsample: true,   // 智能子采样
      mixed: true             // 混合压缩模式
    });
  } else if (outputFormat === 'avif') {
    processor = processor.avif({
      quality: formatOptions.quality,
      alphaQuality: formatOptions.quality,
      lossless: false,
      speed: 4                // 平衡速度和质量
    });
  }
  
  // 执行压缩
  await processor.toFile(outputPath);
  
  // 获取压缩后文件大小
  const compressedSize = statSync(outputPath).size;
  const savings = ((1 - compressedSize / originalSize) * 100).toFixed(1);
  
  return {
    success: true,
    inputPath,
    outputPath,
    originalSize: formatSize(originalSize),
    compressedSize: formatSize(compressedSize),
    savings: `${savings}%`,
    format: outputFormat === 'jpeg' ? 'jpg' : outputFormat
  };
}

// 格式化文件大小
function formatSize(bytes) {
  if (bytes >= 1024 * 1024) {
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  } else if (bytes >= 1024) {
    return `${(bytes / 1024).toFixed(1)} KB`;
  } else {
    return `${bytes} B`;
  }
}

// 批量压缩
async function compressBatch(inputDir, options) {
  const results = [];
  const files = [];
  
  // 递归扫描图片
  function scanDir(dir, relativePath = '') {
    const entries = readdirSync(dir, { withFileTypes: true });
    
    for (const entry of entries) {
      const fullPath = join(dir, entry.name);
      const relPath = join(relativePath, entry.name);
      
      if (entry.isDirectory() && options.recursive) {
        scanDir(fullPath, relPath);
      } else if (entry.isFile()) {
        const ext = extname(entry.name).toLowerCase();
        if (SUPPORTED_FORMATS.includes(ext)) {
          files.push(fullPath);
        }
      }
    }
  }
  
  scanDir(inputDir);
  
  if (files.length === 0) {
    throw new Error(`在 ${inputDir} 中未找到图片文件`);
  }
  
  console.log(`\n🔄 正在压缩 ${files.length} 张图片...\n`);
  
  let totalOriginal = 0;
  let totalCompressed = 0;
  
  for (let i = 0; i < files.length; i++) {
    const file = files[i];
    const progress = `[${String(i + 1).padStart(files.length.toString().length, '0')}/${files.length}]`;
    
    try {
      console.log(`  ${progress} 正在处理：${basename(file)}...`);
      const result = await compressImage(file, { ...options, noConfirm: true });
      results.push(result);
      totalOriginal += parseSize(result.originalSize);
      totalCompressed += parseSize(result.compressedSize);
      
      console.log(`        ✅ ${result.originalSize} → ${result.compressedSize} (${result.savings})`);
    } catch (error) {
      console.log(`        ❌ 失败：${error.message}`);
    }
  }
  
  const totalSavings = ((1 - totalCompressed / totalOriginal) * 100).toFixed(1);
  
  return {
    success: true,
    total: results.length,
    results,
    totalOriginal: formatSize(totalOriginal),
    totalCompressed: formatSize(totalCompressed),
    totalSavings: `${totalSavings}%`,
    outputDir: getTodayOutputDir(options.outputDir)
  };
}

// 解析文件大小为字节
function parseSize(sizeStr) {
  const match = sizeStr.match(/([\d.]+)\s*(KB|MB|B)?/);
  if (!match) return 0;
  
  const value = parseFloat(match[1]);
  const unit = match[2] || 'B';
  
  if (unit === 'MB') return value * 1024 * 1024;
  if (unit === 'KB') return value * 1024;
  return value;
}

// 加载配置
function loadConfig() {
  const configPath = join(homedir(), '.openclaw', 'workspace', 'skills', 'image-compress', 'config.json');
  
  if (existsSync(configPath)) {
    return JSON.parse(readFileSync(configPath, 'utf8'));
  }
  
  return {
    outputDir: join(homedir(), 'Downloads', 'compressed-images'),
    defaultQuality: 0.85,
    defaultFormat: 'original'
  };
}

// 打印报告
function printReport(result) {
  console.log('\n✅ 压缩完成！\n');
  console.log('📊 压缩报告');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━');
  
  if (result.total) {
    // 批量压缩报告
    console.log(`共处理：   ${result.total} 张`);
    console.log(`原图总计： ${result.totalOriginal}`);
    console.log(`压缩后：   ${result.totalCompressed}`);
    console.log(`总计节省： ${result.totalSavings}`);
    console.log('━━━━━━━━━━━━━━━━━━━━━━━');
    console.log(`📁 输出目录：${result.outputDir}`);
  } else {
    // 单图压缩报告
    console.log(`原图：     ${result.originalSize}`);
    console.log(`压缩后：   ${result.compressedSize}`);
    console.log(`节省：     ${result.savings}`);
    console.log('━━━━━━━━━━━━━━━━━━━━━━━');
    console.log(`📁 输出：${result.outputPath}`);
  }
  console.log('');
}

// 主函数
async function compress(input, options) {
  const config = loadConfig();
  
  // 处理预设
  let quality = options.quality;
  if (options.preset && PRESETS[options.preset]) {
    quality = PRESETS[options.preset].quality.toString();
    console.log(`📌 使用预设：${options.preset} (${PRESETS[options.preset].description}, 画质 ${quality})`);
  }
  
  const compressOptions = {
    outputDir: options.outputDir || config.outputDir,
    quality: parseFloat(quality),
    format: options.format,
    maxWidth: options.maxWidth ? parseInt(options.maxWidth) : null,
    maxHeight: options.maxHeight ? parseInt(options.maxHeight) : null,
    recursive: options.recursive,
    noConfirm: options.noConfirm
  };
  
  const stats = statSync(input);
  
  let result;
  
  if (stats.isFile()) {
    result = await compressImage(input, compressOptions);
  } else if (stats.isDirectory()) {
    result = await compressBatch(input, compressOptions);
  } else {
    throw new Error('输入路径必须是文件或目录');
  }
  
  printReport(result);
  return result;
}

// 如果直接运行
if (import.meta.url === `file://${process.argv[1]}`) {
  setupCommander();
}

// 导出函数
export { compress, compressImage, compressBatch, PRESETS };
