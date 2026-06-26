/**
 * 使用示例：演示如何调用 HTML 页面转图片 Agent Skill
 */

import { execute } from './index.js';

async function examples() {
  console.log('='.repeat(60));
  console.log('HTML 页面转图片 Agent Skill - 使用示例');
  console.log('='.repeat(60));
  console.log();

  // 示例 1: 使用默认配置
  console.log('📌 示例 1: 使用默认配置');
  console.log('-'.repeat(60));
  const result1 = await execute();
  console.log('结果:', result1);
  console.log();

  // 示例 2: 自定义 HTML 文件
  console.log('📌 示例 2: 自定义 HTML 文件');
  console.log('-'.repeat(60));
  const result2 = await execute({
    htmlFile: 'xiaohongshu-articles.html',
    outputDir: 'output-custom'
  });
  console.log('结果:', result2);
  console.log();

  // 示例 3: 完全自定义配置
  console.log('📌 示例 3: 完全自定义配置');
  console.log('-'.repeat(60));
  const result3 = await execute({
    htmlFile: 'xiaohongshu-articles.html',
    outputDir: 'output-large',
    pageWidth: 800,
    pageHeight: 1200,
    selector: '.page'
  });
  console.log('结果:', result3);
  console.log();
}

// 运行示例（注释掉以避免自动执行）
// examples().catch(console.error);
