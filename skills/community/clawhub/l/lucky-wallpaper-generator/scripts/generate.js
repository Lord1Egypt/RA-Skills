/**
 * Lucky Wallpaper Generator - 好运壁纸生成器
 * 自动生成小红书风格的好运壁纸
 */

const fs = require('fs');
const path = require('path');

// 配置
const CONFIG = {
  outputDir: path.join(__dirname, '../output'),
  templates: {
    wealth: {
      name: '招财系列',
      prompts: [
        'A minimalist lucky wallpaper with golden coins and treasure bowl, soft gradient background in red and gold, Chinese prosperity symbols, elegant typography, high quality, 4K',
        'Golden ingots and lucky cat, prosperity wallpaper, red and gold gradient, Chinese style, phone wallpaper, 4K quality',
        'Abundance and wealth wallpaper, gold coins raining, treasure chest, luxurious red gold theme, elegant design'
      ]
    },
    lucky: {
      name: '好运系列',
      prompts: [
        'A beautiful good luck wallpaper with four-leaf clover and rainbow, soft pink and purple gradient background, lucky symbols, dreamy atmosphere, high quality, 4K',
        'Lucky koi fish swimming, good fortune wallpaper, soft blue and pink gradient, Chinese style, phone wallpaper',
        'Good luck symbols, four leaf clover, horseshoe, dreamy clouds, soft pastel colors, minimalist design'
      ]
    },
    healing: {
      name: '治愈系列',
      prompts: [
        'A calming healing wallpaper with soft clouds and stars, blue and green gradient background, peaceful atmosphere, minimalist design, high quality, 4K',
        'Healing nature scene, soft moonlight, gentle waves, calming blue tones, zen atmosphere, phone wallpaper',
        'Peaceful meditation scene, soft lotus flowers, misty background, healing colors, minimalist zen design'
      ]
    },
    career: {
      name: '事业系列',
      prompts: [
        'A professional success wallpaper with golden trophy and stars, deep blue and gold color scheme, motivational atmosphere, high quality, 4K',
        'Career success ladder, reaching the top, golden sunrise, professional theme, elegant design, phone wallpaper',
        'Mountain peak success, golden sunrise, achievement theme, blue and gold colors, inspiring atmosphere'
      ]
    }
  },
  sizes: {
    wallpaper: { width: 1080, height: 1920, name: '手机壁纸' },
    avatar: { width: 500, height: 500, name: '头像' },
    post: { width: 1242, height: 1660, name: '小红书图' }
  }
};

// 确保输出目录存在
function ensureOutputDir() {
  if (!fs.existsSync(CONFIG.outputDir)) {
    fs.mkdirSync(CONFIG.outputDir, { recursive: true });
  }
}

// 随机选择提示词
function getRandomPrompt(type) {
  const template = CONFIG.templates[type];
  if (!template) {
    throw new Error(`未知的类型: ${type}`);
  }
  const prompts = template.prompts;
  return prompts[Math.floor(Math.random() * prompts.length)];
}

// 生成壁纸
async function generateWallpaper(options = {}) {
  const {
    type = 'lucky',
    style = 'minimal',
    size = 'wallpaper',
    count = 1
  } = options;

  ensureOutputDir();
  
  const results = [];
  const sizeConfig = CONFIG.sizes[size];
  const template = CONFIG.templates[type];

  console.log(`\n🎨 开始生成 ${template.name}`);
  console.log(`📐 尺寸: ${sizeConfig.name} (${sizeConfig.width}x${sizeConfig.height})`);
  console.log(`📊 数量: ${count}`);

  for (let i = 0; i < count; i++) {
    const prompt = getRandomPrompt(type);
    const timestamp = Date.now();
    const filename = `${type}_${size}_${timestamp}_${i + 1}.json`;
    const filepath = path.join(CONFIG.outputDir, filename);

    const result = {
      id: `${type}_${timestamp}_${i + 1}`,
      type,
      typeName: template.name,
      size,
      sizeName: sizeConfig.name,
      dimensions: sizeConfig,
      prompt,
      style,
      createdAt: new Date().toISOString(),
      status: 'ready_for_generation',
      apiHint: '请使用通义万相或即梦API生成图片'
    };

    fs.writeFileSync(filepath, JSON.stringify(result, null, 2), 'utf8');
    results.push(result);
    
    console.log(`✅ 已生成配置: ${filename}`);
  }

  console.log(`\n🎉 完成! 共生成 ${results.length} 个配置`);
  console.log(`📁 输出目录: ${CONFIG.outputDir}`);
  
  return results;
}

// 批量生成
async function batchGenerate(batchConfig = {}) {
  const {
    types = ['wealth', 'lucky', 'healing', 'career'],
    countPerType = 3,
    size = 'wallpaper'
  } = batchConfig;

  console.log('\n🚀 批量生成模式');
  console.log('='.repeat(50));

  const allResults = [];

  for (const type of types) {
    const results = await generateWallpaper({
      type,
      size,
      count: countPerType
    });
    allResults.push(...results);
  }

  console.log('\n📊 批量生成统计');
  console.log('='.repeat(50));
  console.log(`总计: ${allResults.length} 张`);
  
  // 按类型统计
  const byType = {};
  allResults.forEach(r => {
    byType[r.typeName] = (byType[r.typeName] || 0) + 1;
  });
  
  Object.entries(byType).forEach(([name, count]) => {
    console.log(`  ${name}: ${count} 张`);
  });

  return allResults;
}

// CLI入口
if (require.main === module) {
  const args = process.argv.slice(2);
  const type = args[0] || 'lucky';
  const count = parseInt(args[1]) || 1;

  if (args.includes('--batch')) {
    batchGenerate({ countPerType: count }).catch(console.error);
  } else {
    generateWallpaper({ type, count }).catch(console.error);
  }
}

module.exports = {
  generateWallpaper,
  batchGenerate,
  CONFIG
};