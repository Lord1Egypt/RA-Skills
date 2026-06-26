/**
 * Agent Skill: HTML 页面转图片
 * 将 HTML 文件中的多个页面元素转换为独立的图片文件
 */

import { convertPagesToImages } from './lib/convert-pages.js';
import { resolve } from 'path';
import { fileURLToPath } from 'url';
import { dirname } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

/**
 * Skill 主入口函数
 * @param {Object} params - 技能参数
 * @param {string} params.htmlFile - HTML 文件路径
 * @param {string} params.outputDir - 输出目录
 * @param {number} params.pageWidth - 页面宽度
 * @param {number} params.pageHeight - 页面高度
 * @param {string} params.selector - 页面元素选择器
 * @returns {Promise<Object>} 执行结果
 */
export async function execute(params = {}) {
  const {
    htmlFile = 'xiaohongshu-articles.html',
    outputDir = 'output',
    pageWidth = 375,
    pageHeight = 667,
    selector = '.page'
  } = params;

  try {
    // 解析路径（支持相对路径和绝对路径）
    const htmlPath = htmlFile.startsWith('/') || htmlFile.match(/^[A-Z]:\\/) 
      ? htmlFile 
      : resolve(__dirname, htmlFile);
    
    const outputPath = outputDir.startsWith('/') || outputDir.match(/^[A-Z]:\\/)
      ? outputDir
      : resolve(__dirname, outputDir);

    console.log('🚀 开始执行 HTML 页面转图片技能...\n');
    console.log(`📖 HTML 文件: ${htmlPath}`);
    console.log(`📁 输出目录: ${outputPath}`);
    console.log(`📐 页面尺寸: ${pageWidth}x${pageHeight}px`);
    console.log(`🎯 选择器: ${selector}\n`);

    // 执行转换
    const result = await convertPagesToImages({
      htmlFile: htmlPath,
      outputDir: outputPath,
      pageWidth,
      pageHeight,
      selector
    });

    return {
      success: true,
      message: `成功转换 ${result.count} 个页面为图片`,
      data: {
        images: result.images,
        count: result.count,
        outputDir: outputPath
      }
    };

  } catch (error) {
    return {
      success: false,
      message: `转换失败: ${error.message}`,
      error: error.stack
    };
  }
}

// 如果直接运行此文件，执行默认转换
const isMainModule = import.meta.url === `file://${resolve(process.argv[1] || '')}` || 
                     process.argv[1]?.includes('index.js');

if (isMainModule) {
  execute().then(result => {
    console.log('\n📊 执行结果:', JSON.stringify(result, null, 2));
    process.exit(result.success ? 0 : 1);
  }).catch(error => {
    console.error('❌ 执行失败:', error);
    process.exit(1);
  });
}
