#!/usr/bin/env node
/**
 * html2pptx-complete — 一键转换脚本
 * 
 * 步骤 1: CSS 内嵌 (Python)
 * 步骤 2: PPTX 生成 (Node.js)
 * 步骤 3: 导出文件
 * 
 * 用法:
 *   node convert.js <input.html> [output.pptx]
 */

const { execSync } = require('child_process');
const path = require('path');
const fs = require('fs');

async function convert(htmlPath, outputPath) {
  console.log('🎨 html2pptx-complete — HTML 转 PPTX 完整工作流\n');
  
  const scriptDir = __dirname;
  const tempHtml = path.join(
    path.dirname(htmlPath),
    `_${path.basename(htmlPath, '.html')}_embedded.html`
  );
  
  // 步骤 1: CSS 内嵌
  console.log('📌 步骤 1: CSS 内嵌');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  try {
    execSync(`python3 "${path.join(scriptDir, 'embed-css.py')}" "${htmlPath}" "${tempHtml}"`, {
      stdio: 'inherit',
      cwd: scriptDir
    });
    console.log('✅ 步骤 1 完成\n');
  } catch (err) {
    console.log('⚠️  CSS 内嵌跳过或失败，继续处理...\n');
  }
  
  // 步骤 2-3: PPTX 生成
  console.log('📌 步骤 2-3: PPTX 生成');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  try {
    const inputFile = fs.existsSync(tempHtml) ? tempHtml : htmlPath;
    execSync(`node "${path.join(scriptDir, 'generate-pptx.js')}" "${inputFile}" "${outputPath || ''}"`, {
      stdio: 'inherit',
      cwd: scriptDir
    });
    console.log('✅ 步骤 2-3 完成\n');
  } catch (err) {
    console.error('❌ PPTX 生成失败:', err.message);
    process.exit(1);
  }
  
  // 清理临时文件
  if (fs.existsSync(tempHtml)) {
    try {
      fs.unlinkSync(tempHtml);
      console.log(`🧹 清理临时文件：${path.basename(tempHtml)}`);
    } catch (err) {
      console.log(`⚠️  清理临时文件失败：${err.message}`);
    }
  }
  
  console.log('\n🎉 转换完成!');
  if (outputPath) {
    console.log(`📁 输出文件：${outputPath}`);
  }
}

// 主入口
if (require.main === module) {
  const args = process.argv.slice(2);
  
  if (args.length < 1) {
    console.log('🎨 html2pptx-complete — HTML 转 PPTX 完整工作流\n');
    console.log('用法: node convert.js <input.html> [output.pptx]\n');
    console.log('示例:');
    console.log('  node convert.js presentation.html');
    console.log('  node convert.js presentation.html output.pptx\n');
    process.exit(1);
  }
  
  const inputPath = args[0];
  const outputPath = args[1] || null;
  
  convert(inputPath, outputPath).catch(err => {
    console.error('\n❌ 转换失败:', err.message);
    process.exit(1);
  });
}

module.exports = { convert };
