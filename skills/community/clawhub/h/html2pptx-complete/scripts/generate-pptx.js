#!/usr/bin/env node
/**
 * 步骤 2-3: PPTX 生成脚本
 * 使用 pptxgenjs 解析 HTML 结构，生成可编辑 PPTX
 */

const PptxGenJS = require('pptxgenjs');
const cheerio = require('cheerio');
const fs = require('fs');
const path = require('path');

// 配置
const CONFIG = {
  slideWidth: 10,       // 幻灯片宽度（英寸）
  slideHeight: 5.625,   // 16:9
  margins: {
    x: 0.5,             // 左边距
    y: 0.5,             // 上边距
    w: 9,               // 内容宽度
  },
  fonts: {
    title: { size: 36, bold: true, color: '363636' },
    subtitle: { size: 24, color: '666666' },
    body: { size: 18, color: '363636' },
    small: { size: 14, color: '666666' },
  },
};

/**
 * 解析 CSS 样式
 */
function parseStyle(styleStr) {
  const styles = {};
  if (!styleStr) return styles;
  
  styleStr.split(';').forEach(decl => {
    if (decl.includes(':')) {
      const [key, value] = decl.split(':').map(s => s.trim());
      if (key && value) {
        styles[key] = value;
      }
    }
  });
  
  return styles;
}

/**
 * 解析颜色值
 */
function parseColor(colorStr) {
  if (!colorStr) return '363636';
  
  // 十六进制
  if (colorStr.startsWith('#')) {
    return colorStr.slice(1);
  }
  
  // rgb/rgba
  const rgbMatch = colorStr.match(/rgba?\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)/);
  if (rgbMatch) {
    const r = parseInt(rgbMatch[1]).toString(16).padStart(2, '0');
    const g = parseInt(rgbMatch[2]).toString(16).padStart(2, '0');
    const b = parseInt(rgbMatch[3]).toString(16).padStart(2, '0');
    return `${r}${g}${b}`;
  }
  
  return '363636';
}

/**
 * 解析字体大小 (px → pt)
 */
function parseFontSize(sizeStr) {
  if (!sizeStr) return 18;
  
  const pxMatch = sizeStr.match(/(\d+(?:\.\d+)?)\s*px/);
  if (pxMatch) {
    return Math.round(parseFloat(pxMatch[1]) * 0.75);
  }
  
  const ptMatch = sizeStr.match(/(\d+(?:\.\d+)?)\s*pt/);
  if (ptMatch) {
    return parseFloat(ptMatch[1]);
  }
  
  return 18;
}

/**
 * 添加幻灯片内容
 */
function addSlideContent(slide, element, $) {
  let yPos = CONFIG.margins.y + 1.2;
  const lineHeight = 0.6;
  
  // 遍历子元素
  element.children().each((i, elem) => {
    const $elem = $(elem);
    const tagName = elem.tagName.toLowerCase();
    const styleStr = $elem.attr('style') || '';
    const styles = parseStyle(styleStr);
    
    // 跳过隐藏元素
    if (styles.display === 'none' || styles.visibility === 'hidden') {
      return;
    }
    
    const text = $elem.text().trim();
    if (!text && tagName !== 'img') return;
    
    // 根据标签类型处理
    switch (tagName) {
      case 'h1':
        slide.addText(text, {
          x: CONFIG.margins.x,
          y: yPos,
          w: CONFIG.margins.w,
          h: 1,
          fontSize: parseFontSize(styles['font-size']) || CONFIG.fonts.title.size,
          bold: styles['font-weight'] === 'bold' || parseInt(styles['font-weight']) >= 700,
          color: parseColor(styles['color']),
          align: styles['text-align'] || 'left',
        });
        yPos += 1.2;
        break;
        
      case 'h2':
      case 'h3':
      case 'h4':
      case 'h5':
      case 'h6':
        slide.addText(text, {
          x: CONFIG.margins.x,
          y: yPos,
          w: CONFIG.margins.w,
          h: 0.5,
          fontSize: parseFontSize(styles['font-size']) || (24 - (tagName.charCodeAt(1) - 50) * 2),
          bold: true,
          color: parseColor(styles['color']) || '666666',
          align: styles['text-align'] || 'left',
        });
        yPos += lineHeight;
        break;
        
      case 'p':
      case 'span':
      case 'div':
        slide.addText(text, {
          x: CONFIG.margins.x,
          y: yPos,
          w: CONFIG.margins.w,
          h: 0.5,
          fontSize: parseFontSize(styles['font-size']) || CONFIG.fonts.body.size,
          color: parseColor(styles['color']) || CONFIG.fonts.body.color,
          align: styles['text-align'] || 'left',
        });
        yPos += lineHeight;
        break;
        
      case 'ul':
      case 'ol':
        $elem.find('li').each((j, li) => {
          const itemText = $(li).text().trim();
          if (itemText) {
            slide.addText(itemText, {
              x: CONFIG.margins.x + 0.3,
              y: yPos,
              w: CONFIG.margins.w - 0.3,
              h: 0.4,
              fontSize: CONFIG.fonts.body.size,
              color: CONFIG.fonts.body.color,
              bullet: tagName === 'ul' ? { type: 'bullet' } : { type: 'number' },
            });
            yPos += lineHeight;
          }
        });
        break;
        
      case 'img':
        const src = $elem.attr('src');
        const alt = $elem.attr('alt') || '';
        const width = parseInt($elem.attr('width')) || parseInt(styles['width']) || 6;
        const height = parseInt($elem.attr('height')) || parseInt(styles['height']) || (width * 0.5625);
        
        if (src) {
          try {
            slide.addImage({
              path: src,
              x: CONFIG.margins.x,
              y: yPos,
              w: Math.min(width, CONFIG.margins.w),
              h: height,
            });
            yPos += height + 0.3;
          } catch (err) {
            console.log(`  ⚠️  Image load failed: ${src}`);
            yPos += 0.4;
          }
        }
        break;
        
      case 'table':
        const rows = [];
        $elem.find('tr').each((k, tr) => {
          const row = [];
          $(tr).find('td, th').each((l, td) => {
            row.push($(td).text().trim());
          });
          if (row.length > 0) rows.push(row);
        });
        if (rows.length > 0) {
          slide.addTable(rows, {
            x: CONFIG.margins.x,
            y: yPos,
            w: CONFIG.margins.w,
            fontSize: CONFIG.fonts.small.size,
          });
          yPos += 0.5 * rows.length;
        }
        break;
        
      default:
        // 其他元素：尝试提取文本
        if (text) {
          slide.addText(text, {
            x: CONFIG.margins.x,
            y: yPos,
            w: CONFIG.margins.w,
            h: 0.4,
            fontSize: CONFIG.fonts.small.size,
            color: '666666',
          });
          yPos += 0.5;
        }
    }
  });
  
  return yPos;
}

/**
 * 生成 PPTX
 */
async function generatePptx(htmlPath, outputPath) {
  console.log(`📄 Reading: ${htmlPath}`);
  
  // 读取 HTML
  const html = fs.readFileSync(htmlPath, 'utf-8');
  const $ = cheerio.load(html);
  
  // 创建 PPTX
  const pptx = new PptxGenJS();
  pptx.layout = 'LAYOUT_16x9';
  
  // 查找幻灯片结构
  let slides = $('section.slide');
  
  // 如果没有 section.slide，尝试按 h1 分页
  if (slides.length === 0) {
    const h1Elements = $('h1');
    if (h1Elements.length > 0) {
      console.log(`⚠️  No section.slide found, using ${h1Elements.length} h1 tag(s) for pagination`);
      
      h1Elements.each((i, elem) => {
        const slide = pptx.addSlide();
        const $elem = $(elem);
        const title = $elem.text().trim();
        
        console.log(`  📌 Slide ${i + 1}: ${title.substring(0, 50)}${title.length > 50 ? '...' : ''}`);
        
        // 添加标题
        slide.addText(title, {
          x: CONFIG.margins.x,
          y: CONFIG.margins.y,
          w: CONFIG.margins.w,
          h: 1,
          fontSize: CONFIG.fonts.title.size,
          bold: true,
          color: CONFIG.fonts.title.color,
        });
        
        // 添加 h1 之后的内容
        const content = $elem.nextUntil('h1');
        addSlideContent(slide, content, $);
      });
    } else {
      // 整个文档作为单页
      console.log('⚠️  No section.slide or h1 found, creating single slide from body');
      const slide = pptx.addSlide();
      addSlideContent(slide, $('body'), $);
    }
  } else {
    // 按 section.slide 分页
    console.log(`✅ Found ${slides.length} section.slide element(s)`);
    
    slides.each((i, elem) => {
      const slide = pptx.addSlide();
      const $elem = $(elem);
      
      console.log(`  📌 Slide ${i + 1}`);
      
      // 查找标题
      const title = $elem.find('h1, h2, .title, .xw-title').first().text().trim();
      if (title) {
        slide.addText(title, {
          x: CONFIG.margins.x,
          y: CONFIG.margins.y,
          w: CONFIG.margins.w,
          h: 1,
          fontSize: CONFIG.fonts.title.size,
          bold: true,
          color: CONFIG.fonts.title.color,
        });
      }
      
      // 添加内容
      addSlideContent(slide, $elem, $);
    });
  }
  
  // 保存文件
  if (!outputPath) {
    outputPath = path.join(
      path.dirname(htmlPath),
      path.basename(htmlPath, '.html') + '_converted.pptx'
    );
  }
  
  console.log(`💾 Saving: ${outputPath}`);
  await pptx.writeFile({ fileName: outputPath });
  console.log(`✅ Done!`);
  
  return { outputPath, slides: slides.length || 1 };
}

// 主入口
if (require.main === module) {
  const args = process.argv.slice(2);
  
  if (args.length < 1) {
    console.log('Usage: node generate-pptx.js <input.html> [output.pptx]');
    process.exit(1);
  }
  
  const inputPath = args[0];
  const outputPath = args[1] || null;
  
  generatePptx(inputPath, outputPath).catch(err => {
    console.error('❌ Error:', err.message);
    process.exit(1);
  });
}

module.exports = { generatePptx };
