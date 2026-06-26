/**
 * MiniMax PDF OCR Skill
 * 使用 MiniMax Vision API 识别 PDF/图片中的文字
 * 
 * 使用方法:
 *   export MINIMAX_API_KEY="your-api-key"
 *   node pdf-ocr-minimax.js <pdf文件路径> [输出目录]
 */

const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');

const OUTPUT_DIR = process.env.OUTPUT_DIR || './';

// 获取 API Key（仅从环境变量）
function getApiKey() {
  if (process.env.MINIMAX_API_KEY) {
    return process.env.MINIMAX_API_KEY;
  }
  return null;
}

// PDF 转图片
async function pdfToImages(pdfPath, outputDir) {
  const filename = path.basename(pdfPath, '.pdf');
  const imageDir = path.join(outputDir, `${filename}_images`);
  
  if (!fs.existsSync(imageDir)) {
    fs.mkdirSync(imageDir, { recursive: true });
  }
  
  console.log('📄 正在将 PDF 转换为图片...');
  
  return new Promise((resolve, reject) => {
    const proc = spawn('pdftoppm', [
      '-png',
      '-r', '200',
      '-singlefile',
      pdfPath,
      path.join(imageDir, 'page')
    ], { shell: true });
    
    proc.on('close', (code) => {
      const files = fs.readdirSync(imageDir)
        .filter(f => f.endsWith('.png'))
        .sort();
      
      resolve(files.map(f => path.join(imageDir, f)));
    });
    
    proc.on('error', reject);
  });
}

// 调用 MiniMax Vision API
async function recognizeImage(imagePath, apiKey) {
  const imageData = fs.readFileSync(imagePath);
  const base64Image = imageData.toString('base64');
  
  const response = await fetch('https://api.minimax.chat/v1/text/chatcompletion_v2', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${apiKey}`
    },
    body: JSON.stringify({
      model: 'MiniMax-M2.5',
      messages: [{
        role: 'user',
        content: [
          { type: 'text', text: '请仔细识别这张图片中的所有文字内容，包括中文和英文。保持原有格式输出。如果是表格，请用表格格式。' },
          { type: 'image_url', image_url: { url: `data:image/png;base64,${base64Image}` } }
        ]
      }],
      max_tokens: 8192
    })
  });
  
  const data = await response.json();
  
  if (data.base_resp && data.base_resp.status_code !== 0) {
    throw new Error(data.base_resp.status_msg || 'API Error');
  }
  
  return data.choices?.[0]?.message?.content || '';
}

// 主函数
async function main() {
  const args = process.argv.slice(2);
  
  if (args.length === 0 || args[0] === '--help') {
    console.log(`
MiniMax PDF OCR Tool
====================

使用方法:
  node pdf-ocr-minimax.js <pdf文件> [输出目录]   识别 PDF
  node pdf-ocr-minimax.js --help                显示帮助

环境变量:
  MINIMAX_API_KEY     MiniMax API Key (必填)
  OUTPUT_DIR          输出目录 (可选, 默认当前目录)

首次使用:
  1. 获取 API Key: https://platform.minimaxi.com/user-center/basic-information/interface-key
  2. 运行: export MINIMAX_API_KEY="your-key"
  3. 运行: node pdf-ocr-minimax.js your.pdf
`);
    process.exit(1);
  }
  
  const pdfPath = args[0];
  const outputDir = args[1] || OUTPUT_DIR;
  
  if (!fs.existsSync(pdfPath)) {
    console.error('错误: 文件不存在:', pdfPath);
    process.exit(1);
  }
  
  const filename = path.basename(pdfPath, '.pdf');
  console.log(`\n🔍 开始处理: ${filename}\n`);
  
  // 获取 API Key
  const apiKey = getApiKey();
  
  if (!apiKey) {
    console.log('❌ 未找到 API Key');
    console.log('请先设置环境变量: export MINIMAX_API_KEY="your-key"');
    console.log('获取 API Key: https://platform.minimaxi.com/user-center/basic-information/interface-key');
    process.exit(1);
  }
  
  console.log('✅ MiniMax API Key 已加载');
  
  // PDF 转图片
  const imageFiles = await pdfToImages(pdfPath, outputDir);
  
  if (imageFiles.length === 0) {
    console.error('错误: 无法将 PDF 转换为图片');
    process.exit(1);
  }
  
  console.log(`📑 共 ${imageFiles.length} 页\n`);
  
  // 识别
  let fullText = `# ${filename}\n\n`;
  
  for (let i = 0; i < imageFiles.length; i++) {
    console.log(`  正在识别第 ${i + 1}/${imageFiles.length} 页...`);
    
    try {
      const text = await recognizeImage(imageFiles[i], apiKey);
      fullText += `## 第 ${i + 1} 页\n\n${text}\n\n`;
      console.log(`    ✓ 完成 (${text.length} 字符)`);
    } catch(e) {
      console.error(`    ✗ 失败: ${e.message}`);
      fullText += `## 第 ${i + 1} 页\n\n[识别失败]\n\n`;
    }
  }
  
  // 保存
  const outputPath = path.join(outputDir, `${filename}.md`);
  fs.writeFileSync(outputPath, fullText, 'utf8');
  
  console.log(`\n✅ 完成! 结果已保存到: ${outputPath}`);
  console.log(`📊 总计 ${fullText.length} 字符`);
  
  // 清理临时图片
  const imageDir = path.join(outputDir, `${filename}_images`);
  if (fs.existsSync(imageDir)) {
    fs.rmSync(imageDir, { recursive: true });
  }
}

main().catch(console.error);
