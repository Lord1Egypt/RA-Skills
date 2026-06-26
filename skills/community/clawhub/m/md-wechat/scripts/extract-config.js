#!/usr/bin/env node
/**
 * 从渲染后的 HTML 文件中提取样式配置
 * 
 * 用法:
 *   node extract-config.js <input.html> [-o config.json]
 */

import fs from 'fs';
import path from 'path';
import { program } from 'commander';
import chalk from 'chalk';

// 默认配置模板
const defaultConfig = {
  version: '1.0.0',
  theme: {
    name: 'extracted'
  },
  style: {
    fontFamily: '',
    fontSize: '16px',
    primaryColor: '#0F4C81',
    textColor: '#3f3f3f',
    bgColor: '#ffffff',
    lineHeight: 1.6
  },
  codeBlock: {
    themeUrl: '',
    themeName: 'atom-one-dark',
    isMacStyle: true,
    showLineNumber: false
  },
  image: {
    legend: 'alt-title',
    borderRadius: '4px'
  },
  link: {
    citeStatus: false,
    color: '#0F4C81'
  },
  content: {
    countStatus: true,
    useIndent: false,
    useJustify: false,
    padding: '20px'
  },
  headingStyles: {
    h1: 'default',
    h2: 'default',
    h3: 'default',
    h4: 'default',
    h5: 'default',
    h6: 'default'
  },
  customCSS: ''
};

/**
 * 从 HTML 中提取样式属性
 */
function extractStyles(html) {
  const config = JSON.parse(JSON.stringify(defaultConfig));
  
  // 提取内联样式
  const styleMatch = html.match(/<style[^>]*>([\s\S]*?)<\/style>/gi);
  const inlineStyles = styleMatch ? styleMatch.join('\n') : '';
  
  // 提取字体
  const fontMatch = html.match(/font-family:\s*([^;}"']+)/i);
  if (fontMatch) {
    config.style.fontFamily = fontMatch[1].trim();
  }
  
  // 提取字号
  const fontSizeMatch = html.match(/font-size:\s*(\d+px)/i);
  if (fontSizeMatch) {
    config.style.fontSize = fontSizeMatch[1];
  }
  
  // 提取主色调（从链接、标题等元素）
  const colorPatterns = [
    /color:\s*(#[0-9a-fA-F]{3,6})/gi,
    /background(-color)?:\s*(#[0-9a-fA-F]{3,6})/gi
  ];
  
  const colors = new Set();
  for (const pattern of colorPatterns) {
    let match;
    while ((match = pattern.exec(html)) !== null) {
      if (match[1] && match[1].startsWith('#')) {
        colors.add(match[1].toUpperCase());
      } else if (match[2] && match[2].startsWith('#')) {
        colors.add(match[2].toUpperCase());
      }
    }
  }
  
  // 智能识别主色调（出现次数最多或用于关键元素的）
  if (colors.size > 0) {
    const colorArray = Array.from(colors);
    // 过滤掉黑色、白色和灰色
    const mainColors = colorArray.filter(c => {
      const r = parseInt(c.slice(1, 3), 16);
      const g = parseInt(c.slice(3, 5), 16);
      const b = parseInt(c.slice(5, 7), 16);
      const brightness = (r * 299 + g * 587 + b * 114) / 1000;
      return brightness > 50 && brightness < 200;
    });
    if (mainColors.length > 0) {
      config.style.primaryColor = mainColors[0];
      config.link.color = mainColors[0];
    }
  }
  
  // 提取文本颜色
  const textColorMatch = html.match(/color:\s*(#[0-9a-fA-F]{3,6})[^;]*;/i);
  if (textColorMatch) {
    const color = textColorMatch[1];
    // 检查是否不是链接颜色（链接通常有下划线或特殊样式）
    if (!isLikelyLinkColor(html, color)) {
      config.style.textColor = color;
    }
  }
  
  // 提取背景色
  const bgMatch = html.match(/background(-color)?:\s*(#[0-9a-fA-F]{3,6})/i);
  if (bgMatch) {
    config.style.bgColor = bgMatch[2];
  }
  
  // 提取行高
  const lineHeightMatch = html.match(/line-height:\s*([\d.]+|\d+px)/i);
  if (lineHeightMatch) {
    config.style.lineHeight = parseFloat(lineHeightMatch[1]) || 1.6;
  }
  
  // 检测代码块样式
  const codeBlockMatch = html.match(/hljs|highlight\.js|highlightjs/i);
  if (codeBlockMatch) {
    // 提取代码块主题
    const themeMatch = html.match(/\/([^\/]+)\.min\.css/);
    if (themeMatch) {
      config.codeBlock.themeName = themeMatch[1].replace('.min', '');
    }
    
    // 检测是否有 Mac 风格装饰（三个圆点）
    const macStyleMatch = html.match(/ellipse.*rgb\(220,60,54\).*ellipse.*rgb\(218,151,33\).*ellipse.*rgb\(27,161,37\)/is);
    config.codeBlock.isMacStyle = !!macStyleMatch;
  }
  
  // 检测代码块背景色
  const codeBgMatch = html.match(/<pre[^>]*style="[^"]*background:\s*(#[0-9a-fA-F]{3,6})/i);
  if (codeBgMatch) {
    config.codeBlock.bgColor = codeBgMatch[1];
  }
  
  // 检测图片样式
  const imgStyleMatch = html.match(/<img[^>]*style="[^"]*border-radius:\s*(\d+px)/i);
  if (imgStyleMatch) {
    config.image.borderRadius = imgStyleMatch[1];
  }
  
  // 检测图片标题样式
  const figcaptionMatch = html.match(/figcaption/i);
  if (figcaptionMatch) {
    config.image.legend = 'alt-title';
  }
  
  // 检测链接引用
  const citeMatch = html.match(/<cite[^>]*class="[^"]*footnote/i);
  config.link.citeStatus = !!citeMatch;
  
  // 检测段落缩进
  const indentMatch = html.match(/text-indent:\s*2em/i);
  config.content.useIndent = !!indentMatch;
  
  // 检测两端对齐
  const justifyMatch = html.match(/text-align:\s*justify/i);
  config.content.useJustify = !!justifyMatch;
  
  // 检测内容区域 padding
  const paddingMatch = html.match(/padding:\s*(\d+px)/i);
  if (paddingMatch) {
    config.content.padding = paddingMatch[1];
  }
  
  // 分析标题样式
  const headingPatterns = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6'];
  for (const h of headingPatterns) {
    const hMatch = html.match(new RegExp(`<${h}[^>]*style="[^"]*"`, 'i'));
    if (hMatch) {
      config.headingStyles[h] = 'custom';
    }
  }
  
  // 提取自定义 CSS（排除标准样式）
  config.customCSS = extractCustomCSS(inlineStyles);
  
  return config;
}

/**
 * 判断颜色是否是链接颜色
 */
function isLikelyLinkColor(html, color) {
  // 检查颜色是否出现在 a 标签附近
  const linkPattern = new RegExp(`<a[^>]*style="[^"]*color:\\s*${color}`, 'i');
  return linkPattern.test(html);
}

/**
 * 提取自定义 CSS
 */
function extractCustomCSS(css) {
  // 排除标准样式，保留自定义部分
  const standardPatterns = [
    /^\.hljs/,
    /^\.katex/,
    /^\.mermaid/,
    /^pre\s*\{/,
    /^code\s*\{/,
    /^blockquote\s*\{/,
    /^table\s*\{/,
    /^@keyframes/
  ];
  
  const lines = css.split('\n');
  const customLines = [];
  let inBlock = false;
  let blockDepth = 0;
  let currentBlock = '';
  
  for (const line of lines) {
    // 跳过空行
    if (!line.trim()) continue;
    
    // 检查是否是标准样式
    const isStandard = standardPatterns.some(p => p.test(line.trim()));
    
    if (!isStandard && line.includes('{')) {
      inBlock = true;
      currentBlock = line;
      blockDepth = (line.match(/{/g) || []).length - (line.match(/}/g) || []).length;
    } else if (inBlock) {
      currentBlock += '\n' + line;
      blockDepth += (line.match(/{/g) || []).length - (line.match(/}/g) || []).length;
      
      if (blockDepth <= 0) {
        inBlock = false;
        // 再次检查整个块是否是标准样式
        const isBlockStandard = standardPatterns.some(p => p.test(currentBlock));
        if (!isBlockStandard && currentBlock.trim()) {
          customLines.push(currentBlock);
        }
        currentBlock = '';
      }
    }
  }
  
  return customLines.join('\n\n').trim();
}

/**
 * 从 Markdown 文件和渲染后的 HTML 对比提取配置
 */
function extractFromPair(markdown, html) {
  const config = extractStyles(html);
  
  // 分析 Markdown 结构特征
  const lines = markdown.split('\n');
  
  // 检测是否使用数学公式
  const hasMath = /\$\$[\s\S]+?\$\$|\$[^\$\n]+?\$/.test(markdown);
  config.features = config.features || {};
  config.features.math = hasMath;
  
  // 检测是否使用代码块
  const hasCodeBlock = /```[\w]*\n/.test(markdown);
  config.features.codeBlock = hasCodeBlock;
  
  // 检测是否使用表格
  const hasTable = /^\|.+?\|$/.test(markdown);
  config.features.table = hasTable;
  
  // 检测是否使用 Mermaid
  const hasMermaid = /```mermaid/i.test(markdown);
  config.features.mermaid = hasMermaid;
  
  // 检测是否使用 PlantUML
  const hasPlantUML = /```plantuml/i.test(markdown);
  config.features.plantUML = hasPlantUML;
  
  return config;
}

/**
 * 主函数
 */
async function main() {
  program
    .name('extract-config')
    .description('从渲染后的 HTML 文件中提取样式配置')
    .argument('<input>', '渲染后的 HTML 文件路径')
    .option('-o, --output <path>', '输出配置文件路径')
    .option('-m, --markdown <path>', '对应的 Markdown 文件（用于增强分析）')
    .option('--name <name>', '配置名称', 'extracted')
    .parse();
  
  const options = program.opts();
  const inputPath = program.args[0];
  
  // 读取 HTML 文件
  if (!fs.existsSync(inputPath)) {
    console.error(chalk.red(`错误: 文件不存在: ${inputPath}`));
    process.exit(1);
  }
  
  const html = fs.readFileSync(inputPath, 'utf-8');
  
  let config;
  
  if (options.markdown && fs.existsSync(options.markdown)) {
    // 从 Markdown 和 HTML 对比提取
    const md = fs.readFileSync(options.markdown, 'utf-8');
    config = extractFromPair(md, html);
  } else {
    // 仅从 HTML 提取
    config = extractStyles(html);
  }
  
  // 设置配置名称
  config.theme.name = options.name;
  
  // 确定输出路径
  const outputPath = options.output || inputPath.replace(/\.html?$/i, '-config.json');
  
  // 写入配置文件
  fs.writeFileSync(outputPath, JSON.stringify(config, null, 2), 'utf-8');
  
  console.log(chalk.green('✓ 配置提取完成！'));
  console.log(chalk.gray(`  输出文件: ${outputPath}`));
  console.log('');
  console.log(chalk.cyan('提取的配置:'));
  console.log(chalk.gray(`  主色调: ${config.style.primaryColor}`));
  console.log(chalk.gray(`  字体: ${config.style.fontFamily || '(未检测到)'}`));
  console.log(chalk.gray(`  字号: ${config.style.fontSize}`));
  console.log(chalk.gray(`  代码块主题: ${config.codeBlock.themeName}`));
  console.log(chalk.gray(`  Mac 风格代码块: ${config.codeBlock.isMacStyle ? '是' : '否'}`));
}

main().catch(console.error);
