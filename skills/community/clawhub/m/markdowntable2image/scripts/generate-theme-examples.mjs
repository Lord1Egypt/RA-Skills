#!/usr/bin/env node
/**
 * 生成所有主题的图片示例（内置主题 + 自定义主题）
 */

import { renderTable } from './index.js';
import { writeFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __dirname = dirname(fileURLToPath(import.meta.url));

// 统一的表格数据
const tableData = [
  { scheme: 'A. 渐进优化', tech: '保持 Sharp+SVG，优化字体和配置', pros: '风险低、兼容好', effort: '⭐⭐' },
  { scheme: 'B. Satori 升级', tech: 'Vercel Satori + Resvg', pros: '现代化、CSS支持好', effort: '⭐⭐⭐⭐' },
  { scheme: 'C. 混合架构', tech: '简单表格→Sharp，复杂→Puppeteer', pros: '灵活、兼顾性能和功能', effort: '⭐⭐⭐⭐⭐' }
];

const columns = [
  { key: 'scheme', header: '方案', width: 120 },
  { key: 'tech', header: '技术栈', width: 280 },
  { key: 'pros', header: '优点', width: 150 },
  { key: 'effort', header: '工作量', width: 80, align: 'center' }
];

const builtInThemes = [
  'discord-light', 'discord-dark', 'finance', 'minimal',
  'sweet-pink', 'deep-sea', 'wisteria', 'pond-blue', 'camellia'
];

const customThemes = [
  {
    name: 'custom-primary-secondary',
    theme: { primary: '#FF6B6B', secondary: '#2C3E50' },
    subtitle: 'Custom: primary=#FF6B6B, secondary=#2C3E50'
  },
  {
    name: 'custom-full',
    theme: {
      background: '#0f172a',
      headerBg: '#38bdf8',
      headerText: '#0f172a',
      rowBg: '#0f172a',
      rowAltBg: '#1e293b',
      text: '#38bdf8',
      border: '#38bdf8'
    },
    subtitle: 'Custom: full object theme'
  }
];

async function generateExamples() {
  console.log('生成内置主题图片示例...\n');

  for (const theme of builtInThemes) {
    console.log(`生成 ${theme} 主题...`);
    try {
      const result = await renderTable({
        data: tableData,
        columns,
        title: '技术方案对比',
        subtitle: `Theme: ${theme}`,
        theme,
        maxWidth: 700
      });

      const outputPath = join(__dirname, '..', 'assets', `theme-${theme}.png`);
      writeFileSync(outputPath, result.buffer);
      console.log(`  ✅ assets/theme-${theme}.png (${result.width}x${result.height}px)`);
    } catch (error) {
      console.error(`  ❌ ${theme} 失败:`, error.message);
    }
  }

  console.log('\n生成自定义主题图片示例...\n');

  for (const { name, theme, subtitle } of customThemes) {
    console.log(`生成 ${name} 主题...`);
    try {
      const result = await renderTable({
        data: tableData,
        columns,
        title: '技术方案对比',
        subtitle,
        theme,
        maxWidth: 700
      });

      const outputPath = join(__dirname, '..', 'assets', `${name}.png`);
      writeFileSync(outputPath, result.buffer);
      console.log(`  ✅ assets/${name}.png (${result.width}x${result.height}px)`);
    } catch (error) {
      console.error(`  ❌ ${name} 失败:`, error.message);
    }
  }

  console.log('\n全部完成！');
}

generateExamples().catch(console.error);
