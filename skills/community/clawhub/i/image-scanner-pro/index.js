const fs = require('fs');
const path = require('path');
const { GoogleGenerativeAI } = require('@google/generative-ai');

const IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.webp', '.heic', '.gif', '.bmp', '.tiff', '.raw', '.cr2', '.nef', '.arw', '.dng'];

const STYLE_KEYWORDS = {
  'portrait': ['人像', 'portrait', '人', 'face', 'head', '肖像'],
  'landscape': ['风景', 'landscape', '山', '海', '湖', '自然', 'nature', '景'],
  'still-life': ['静物', 'still', '产品', 'food', '花', '物品'],
  'architecture': ['建筑', 'architecture', '楼', 'city', 'urban', '建筑'],
  'street': ['街头', 'street', '扫街', '路', '市'],
  'black-white': ['黑白', 'bw', 'monochrome', 'bnw', 'bw'],
  'product': ['产品', 'product', '商品', 'commercial'],
  'event': ['活动', 'event', '婚礼', '会议', '庆典']
};

const PHOTO_ANALYSIS_PROMPT = `你是一位专业摄影指导，请分析这张图片并返回 JSON 格式的分析结果：
{
  "shotType": "景别（特写/近景/中景/全景/远景/大远景）",
  "subject": "主体（人物/动物/建筑/风景/产品/静物/其他）",
  "scene": "场景（室内/室外/工作室/自然/城市/其他）",
  "lighting": "光线（自然光/人造光/混合光/逆光/侧光/顶光/柔光/硬光）",
  "mood": "氛围（温暖/冷静/欢快/忧郁/神秘/戏剧性/宁静/紧张）",
  "tone": "影调（高调/低调/中间调/高对比/低对比）",
  "colorPalette": "主色调（暖色/冷色/中性/黑白/鲜艳/柔和）",
  "objects": ["画面中的主要物件/陈设/产品列表"],
  "composition": "构图方式（三分法/对称/引导线/框架/对角线/其他）",
  "style": "风格分类（人像/风景/商业/纪实/艺术/产品/建筑/街头）",
  "quality": "画质评估（专业/良好/一般/需改进）",
  "suggestions": ["改进建议或亮点说明"]
}
只返回纯 JSON，不要其他文字。`;

async function analyzeImageWithGemini(imagePath, apiKey, proxyUrl) {
  try {
    if (proxyUrl) {
      process.env.HTTP_PROXY = proxyUrl;
      process.env.HTTPS_PROXY = proxyUrl;
    }
    const genAI = new GoogleGenerativeAI(apiKey);
    const model = genAI.getGenerativeModel({ model: "gemini-2.0-flash" });
    const imageBuffer = fs.readFileSync(imagePath);
    const base64Image = imageBuffer.toString('base64');
    const result = await model.generateContent([
      { inlineData: { data: base64Image, mimeType: `image/${path.extname(imagePath).slice(1)}` } },
      PHOTO_ANALYSIS_PROMPT
    ]);
    const response = await result.response;
    const text = response.text();
    const jsonMatch = text.match(/\{[\s\S]*\}/);
    if (jsonMatch) return JSON.parse(jsonMatch[0]);
    return { error: "无法解析分析结果", raw: text };
  } catch (error) {
    return { error: error.message };
  }
}

function detectStyle(filename) {
  const lower = filename.toLowerCase();
  const name = path.basename(filename, path.extname(filename));
  for (const [style, keywords] of Object.entries(STYLE_KEYWORDS)) {
    for (const keyword of keywords) {
      if (lower.includes(keyword) || name.includes(keyword)) return style;
    }
  }
  return 'uncategorized';
}

async function scanAndAnalyze(dirPath, options = {}) {
  const { apiKey, proxyUrl, model = 'gemini', maxFiles = 50 } = options;
  const results = {
    directory: dirPath,
    scanTime: new Date().toISOString(),
    totalFiles: 0,
    analyzedFiles: [],
    summary: { byShotType: {}, bySubject: {}, byScene: {}, byLighting: {}, byMood: {}, byStyle: {} }
  };

  if (!fs.existsSync(dirPath)) {
    console.error(`❌ 错误：目录不存在 - ${dirPath}`);
    return results;
  }

  const files = fs.readdirSync(dirPath)
    .filter(f => IMAGE_EXTENSIONS.includes(path.extname(f).toLowerCase()))
    .slice(0, maxFiles);

  results.totalFiles = files.length;
  console.log(`📸 找到 ${files.length} 张图片，开始分析...\n`);
  console.log(`🤖 模型：${model}`);
  console.log(`🌐 代理：${proxyUrl || '直连'}`);
  console.log('');

  for (let i = 0; i < files.length; i++) {
    const file = files[i];
    const filePath = path.join(dirPath, file);
    const stats = fs.statSync(filePath);
    console.log(`[${i + 1}/${files.length}] 分析：${file}`);

    let analysis = {};
    if (apiKey) {
      analysis = await analyzeImageWithGemini(filePath, apiKey, proxyUrl);
      if (analysis.error) {
        console.log(`   ⚠️ 分析失败：${analysis.error}`);
      }
    } else {
      analysis = {
        shotType: '未知', subject: '未知', scene: '未知', lighting: '未知',
        mood: '未知', tone: '未知', colorPalette: '未知', objects: [],
        composition: '未知', style: detectStyle(file), quality: '未知',
        suggestions: ['需要视觉模型 API 进行深度分析']
      };
    }

    results.analyzedFiles.push({
      name: file, path: filePath, size: stats.size,
      sizeKB: Math.round(stats.size / 1024 * 100) / 100,
      modified: stats.mtime.toISOString(), analysis: analysis
    });

    if (analysis.style && analysis.style !== 'uncategorized') {
      results.summary.byStyle[analysis.style] = (results.summary.byStyle[analysis.style] || 0) + 1;
    }
    if (analysis.subject && analysis.subject !== '未知') {
      results.summary.bySubject[analysis.subject] = (results.summary.bySubject[analysis.subject] || 0) + 1;
    }
  }
  return results;
}

function printReport(results) {
  console.log('\n🎬 摄影作品分析报告');
  console.log('═'.repeat(60));
  console.log(`📁 目录：${results.directory}`);
  console.log(`🕐 扫描时间：${results.scanTime}`);
  console.log(`📸 总图片数：${results.totalFiles}`);
  console.log(`✅ 已分析：${results.analyzedFiles.length}`);

  const validStyles = Object.entries(results.summary.byStyle).filter(([_, v]) => v > 0);
  if (validStyles.length > 0) {
    console.log('\n📊 风格分类统计:');
    for (const [style, count] of validStyles) {
      const bar = '█'.repeat(Math.min(count, 30));
      console.log(`  ${style.padEnd(15)} ${count.toString().padStart(3)} ${bar}`);
    }
  }

  const validSubjects = Object.entries(results.summary.bySubject).filter(([_, v]) => v > 0);
  if (validSubjects.length > 0) {
    console.log('\n🎯 主体分类统计:');
    for (const [subject, count] of validSubjects) {
      console.log(`  ${subject.padEnd(15)} ${count} 张`);
    }
  }

  console.log('\n📋 详细分析:');
  results.analyzedFiles.forEach((file, index) => {
    console.log(`\n  ${index + 1}. ${file.name}`);
    console.log(`     大小：${file.sizeKB} KB`);
    if (file.analysis.style && file.analysis.style !== 'uncategorized') {
      console.log(`     风格：${file.analysis.style}`);
    }
    if (file.analysis.subject && file.analysis.subject !== '未知') {
      console.log(`     主体：${file.analysis.subject}`);
    }
    if (file.analysis.shotType && file.analysis.shotType !== '未知') {
      console.log(`     景别：${file.analysis.shotType}`);
    }
    if (file.analysis.lighting && file.analysis.lighting !== '未知') {
      console.log(`     光线：${file.analysis.lighting}`);
    }
    if (file.analysis.mood && file.analysis.mood !== '未知') {
      console.log(`     氛围：${file.analysis.mood}`);
    }
    if (file.analysis.colorPalette && file.analysis.colorPalette !== '未知') {
      console.log(`     色调：${file.analysis.colorPalette}`);
    }
    if (file.analysis.objects?.length > 0) {
      console.log(`     物件：${file.analysis.objects.join(', ')}`);
    }
  });
  console.log('\n' + '═'.repeat(60));
}

async function main() {
  const args = process.argv.slice(2);
  const pathIndex = args.indexOf('--path');
  const apiKeyIndex = args.indexOf('--api-key');
  const proxyIndex = args.indexOf('--proxy');
  const modelIndex = args.indexOf('--model');
  const outputIndex = args.indexOf('--output');
  
  const dirPath = pathIndex !== -1 ? args[pathIndex + 1] : '.';
  const apiKey = apiKeyIndex !== -1 ? args[apiKeyIndex + 1] : process.env.GEMINI_API_KEY;
  const proxyUrl = proxyIndex !== -1 ? args[proxyIndex + 1] : process.env.HTTPS_PROXY;
  const model = modelIndex !== -1 ? args[modelIndex + 1] : 'gemini-2.0-flash';
  const outputPath = outputIndex !== -1 ? args[outputIndex + 1] : null;

  console.log(`🔍 开始分析：${dirPath}`);
  console.log(`🤖 模型：${model}`);
  if (apiKey) {
    console.log(`✅ API Key: 已配置`);
  } else {
    console.log(`⚠️  未提供 API Key，将使用基础分析模式`);
  }
  if (proxyUrl) {
    console.log(`🌐 代理：${proxyUrl}`);
  }

  const results = await scanAndAnalyze(dirPath, { apiKey, proxyUrl, model });
  printReport(results);

  if (outputPath) {
    fs.writeFileSync(outputPath, JSON.stringify(results, null, 2));
    console.log(`\n💾 报告已保存：${outputPath}`);
  }
}

main().catch(console.error);
