const fs = require('fs');
const path = require('path');

// 图片扩展名映射
const IMAGE_EXTENSIONS = {
  '.jpg': 'JPEG',
  '.jpeg': 'JPEG',
  '.png': 'PNG',
  '.gif': 'GIF',
  '.bmp': 'BMP',
  '.webp': 'WebP',
  '.heic': 'HEIC',
  '.heif': 'HEIF',
  '.raw': 'RAW',
  '.cr2': 'Canon RAW',
  '.nef': 'Nikon RAW',
  '.arw': 'Sony RAW',
  '.dng': 'Adobe RAW',
  '.tiff': 'TIFF',
  '.tif': 'TIFF'
};

// 风格分类关键词（基于文件名猜测）
const STYLE_KEYWORDS = {
  'portrait': ['人像', 'portrait', '人', 'face', 'head'],
  'landscape': ['风景', 'landscape', '山', '海', '湖', '自然', 'nature'],
  'still-life': ['静物', 'still', '产品', 'food', '花'],
  'architecture': ['建筑', 'architecture', '楼', 'city', 'urban'],
  'street': ['街头', 'street', '扫街'],
  'black-white': ['黑白', 'bw', 'monochrome', 'bnw']
};

async function scanDirectory(dirPath) {
  const results = {
    directory: dirPath,
    scanTime: new Date().toISOString(),
    totalFiles: 0,
    imageFiles: [],
    byFormat: {},
    byStyle: {},
    byColor: {}
  };

  if (!fs.existsSync(dirPath)) {
    console.error(`错误：目录不存在 - ${dirPath}`);
    return results;
  }

  const files = fs.readdirSync(dirPath);
  
  for (const file of files) {
    const ext = path.extname(file).toLowerCase();
    const filePath = path.join(dirPath, file);
    const stats = fs.statSync(filePath);

    if (stats.isFile() && IMAGE_EXTENSIONS[ext]) {
      results.totalFiles++;
      
      const fileInfo = {
        name: file,
        format: IMAGE_EXTENSIONS[ext],
        extension: ext,
        size: stats.size,
        sizeKB: Math.round(stats.size / 1024 * 100) / 100,
        modified: stats.mtime.toISOString(),
        style: detectStyle(file),
        color: 'unknown' // 需要图片分析库
      };

      results.imageFiles.push(fileInfo);

      // 按格式统计
      if (!results.byFormat[fileInfo.format]) {
        results.byFormat[fileInfo.format] = 0;
      }
      results.byFormat[fileInfo.format]++;

      // 按风格统计
      if (!results.byStyle[fileInfo.style]) {
        results.byStyle[fileInfo.style] = 0;
      }
      results.byStyle[fileInfo.style]++;
    }
  }

  return results;
}

function detectStyle(filename) {
  const lower = filename.toLowerCase();
  
  for (const [style, keywords] of Object.entries(STYLE_KEYWORDS)) {
    for (const keyword of keywords) {
      if (lower.includes(keyword)) {
        return style;
      }
    }
  }
  
  return 'uncategorized';
}

function printReport(results) {
  console.log('\n📸 图片扫描报告');
  console.log('═'.repeat(50));
  console.log(`目录：${results.directory}`);
  console.log(`扫描时间：${results.scanTime}`);
  console.log(`总图片数：${results.totalFiles}`);
  
  console.log('\n📁 按格式分类:');
  for (const [format, count] of Object.entries(results.byFormat)) {
    console.log(`  ${format}: ${count} 张`);
  }

  console.log('\n🎨 按风格分类:');
  for (const [style, count] of Object.entries(results.byStyle)) {
    console.log(`  ${style}: ${count} 张`);
  }

  console.log('\n📋 文件列表:');
  results.imageFiles.forEach((file, index) => {
    console.log(`  ${index + 1}. ${file.name}`);
    console.log(`     格式：${file.format} | 大小：${file.sizeKB} KB | 风格：${file.style}`);
  });

  console.log('\n' + '═'.repeat(50));
}

// 主函数
async function main() {
  const args = process.argv.slice(2);
  const pathIndex = args.indexOf('--path');
  const actionIndex = args.indexOf('--action');
  
  const dirPath = pathIndex !== -1 ? args[pathIndex + 1] : '.';
  const action = actionIndex !== -1 ? args[actionIndex + 1] : 'scan';

  console.log(`🔍 开始${action === 'classify' ? '分类整理' : '扫描'}: ${dirPath}`);

  const results = await scanDirectory(dirPath);
  printReport(results);

  // 如果需要自动分类
  if (action === 'classify') {
    const outputIndex = args.indexOf('--output');
    const outputDir = outputIndex !== -1 ? args[outputIndex + 1] : null;
    
    if (outputDir) {
      console.log(`\n📁 将文件分类移动到：${outputDir}`);
      // 这里可以实现自动创建文件夹并移动文件的逻辑
      console.log('⚠️  自动分类功能需要确认，请先查看报告');
    }
  }
}

main().catch(console.error);