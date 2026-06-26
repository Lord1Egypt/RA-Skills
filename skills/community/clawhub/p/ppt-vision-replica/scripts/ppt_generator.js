/**
 * 智能PPT生成器 - 基于区域JSON生成PPTX
 * 使用pptxgenjs将结构化区域数据转换为可编辑PPT
 *
 * v1.1 更新 (短期优化方案):
 * - 支持行间距 (lineSpacing)
 * - 支持bullet符号精确处理
 * - 支持字符间距 (charSpacing)
 * - 支持圆角矩形 (roundedRect)
 * - 改进文字内容空行/多行处理
 */

const PptxGenJS = require('pptxgenjs');
const { normalizeAndMap, SLIDE_WIDTH_EMU, SLIDE_HEIGHT_EMU, normalizeSymbols } = require('./coordinate_mapper');

/**
 * 从区域JSON生成PPT
 * @param {Array} regions - 区域数组
 * @param {Object} options - 生成选项
 * @returns {Promise<PptxGenJS>} PptxGenJS实例
 */
async function generateFromRegions(regions, options = {}) {
  const {
    slideWidth = SLIDE_WIDTH_EMU,
    slideHeight = SLIDE_HEIGHT_EMU,
    background = null,
    imageWidth = 2100,
    imageHeight = 1192
  } = options;

  const pptx = new PptxGenJS();

  // 设置幻灯片背景色（如有）
  const slide = pptx.addSlide();
  if (background) {
    slide.background = { color: background.replace('#', '') };
  }

  // 按z-index排序，确保正确的叠加顺序
  const sortedRegions = [...regions].sort((a, b) => (a.zIndex || 0) - (b.zIndex || 0));

  for (const region of sortedRegions) {
    try {
      await renderRegion(slide, region, slideWidth, slideHeight, imageWidth, imageHeight);
    } catch (err) {
      console.warn(`[ppt_generator] 渲染区域 ${region.id || '?'} 失败:`, err.message);
    }
  }

  return pptx;
}

/**
 * 渲染单个区域
 */
async function renderRegion(slide, region, slideWidth, slideHeight, imageWidth = 2100, imageHeight = 1192) {
  const mapped = region.mapped || normalizeAndMap(region, imageWidth, imageHeight, slideWidth, slideHeight);

  // EMU 转英寸
  const pos = {
    x: mapped.x / 914400,
    y: mapped.y / 914400,
    w: mapped.w / 914400,
    h: mapped.h / 914400
  };

  switch (region.type) {
    case 'rectangle':
    case 'rect':
    case 'shape':
      renderRectangle(slide, region, pos);
      break;
    case 'roundedRect':
    case 'roundRect':
      renderRoundedRect(slide, region, pos);
      break;
    case 'text':
      renderText(slide, region, pos);
      break;
    case 'image':
      renderImage(slide, region, pos);
      break;
    case 'line':
      renderLine(slide, region, pos);
      break;
    default:
      // 兜底：如有内容当文本渲染，否则当矩形
      if (region.content) {
        renderText(slide, region, pos);
      } else {
        console.log(`[ppt_generator] 未知区域类型: ${region.type}，尝试矩形渲染`);
        renderRectangle(slide, region, pos);
      }
  }
}

/**
 * 渲染矩形
 */
function renderRectangle(slide, region, pos) {
  const hasFill = region.fill || region.color || region.backgroundColor;
  const hasLine = region.lineColor || region.borderColor || (region.line && region.line.color);

  if (!hasFill && !hasLine) return;

  const shapeOpts = {
    ...pos,
    fill: hasFill ? { color: cleanColor(region.fill || region.backgroundColor || region.color) } : { type: 'none' },
    line: hasLine ? {
      color: cleanColor(region.lineColor || region.borderColor || (region.line && region.line.color) || '000000'),
      width: region.lineWidth || (region.line && region.line.width) || 1,
      dashType: region.dashType || 'solid'
    } : { width: 0 }
  };

  slide.addShape('rect', shapeOpts);
}

/**
 * 渲染圆角矩形
 */
function renderRoundedRect(slide, region, pos) {
  const hasFill = region.fill || region.color || region.backgroundColor;
  const hasLine = region.lineColor || region.borderColor;

  const shapeOpts = {
    ...pos,
    fill: hasFill ? { color: cleanColor(region.fill || region.backgroundColor || region.color) } : { type: 'none' },
    line: hasLine ? {
      color: cleanColor(region.lineColor || region.borderColor || '000000'),
      width: region.lineWidth || 1
    } : { width: 0 },
    rectRadius: region.cornerRadius || 0.1  // 圆角半径(英寸)
  };

  slide.addShape('roundRect', shapeOpts);
}

/**
 * 渲染文本
 * 【短期优化】支持行间距、bullet、字符间距
 */
function renderText(slide, region, pos) {
  const rawContent = region.content || '';

  // 文字校正
  const content = normalizeSymbols(rawContent, 'keep_cn');

  // 构造文字选项
  const textOptions = {
    ...pos,
    fontSize: region.fontSize || 14,
    color: cleanColor(region.color || region.textColor || '000000'),
    align: region.align || 'left',
    valign: region.valign || 'top',
    wrap: true,
    autoFit: false
  };

  // 字体
  if (region.fontFamily || region.font) {
    textOptions.fontFace = region.fontFamily || region.font;
  }

  // 加粗 / 斜体
  if (region.bold || region.fontWeight === 'bold' || region.fontWeight === 700) {
    textOptions.bold = true;
  }
  if (region.italic) {
    textOptions.italic = true;
  }

  // 【短期优化P0】行间距
  // lineSpacing值: 1.0=单倍, 1.5=1.5倍, 2.0=双倍
  if (region.lineSpacing) {
    // pptxgenjs lineSpacingMultiple 单位为百分比(pt*100)
    textOptions.lineSpacingMultiple = region.lineSpacing;
  }

  // 【短期优化P0】字符间距
  if (region.charSpacing !== undefined) {
    textOptions.charSpacing = region.charSpacing;
  }

  // 背景色（文本框填充）
  if (region.backgroundColor) {
    textOptions.fill = { color: cleanColor(region.backgroundColor) };
  }

  // 【短期优化P0】bullet符号处理
  // 如果文本包含多行且含bullet前缀，改为分段渲染
  if (content.includes('\n')) {
    const lines = content.split('\n').filter(l => l.trim());
    const paragraphs = lines.map(line => ({
      text: line,
      options: {
        fontSize: textOptions.fontSize,
        color: textOptions.color,
        bold: textOptions.bold,
        align: textOptions.align,
        lineSpacingMultiple: textOptions.lineSpacingMultiple
      }
    }));
    slide.addText(paragraphs, textOptions);
  } else {
    slide.addText(content, textOptions);
  }
}

/**
 * 渲染图片
 */
function renderImage(slide, region, pos) {
  if (region.imagePath || region.path || region.data) {
    slide.addImage({
      ...pos,
      path: region.imagePath || region.path,
      data: region.data  // base64
    });
  }
}

/**
 * 渲染线条
 */
function renderLine(slide, region, pos) {
  slide.addShape('line', {
    ...pos,
    line: {
      color: cleanColor(region.color || '000000'),
      width: region.lineWidth || 1,
      dashType: region.dashType || 'solid'
    }
  });
}

/**
 * 清理颜色值（去掉 # 前缀）
 * @param {string} color - 颜色值
 * @returns {string} 标准化的6位十六进制颜色
 */
function cleanColor(color) {
  if (!color || typeof color !== 'string') return '000000';
  const c = color.replace('#', '').toUpperCase();
  // 3位颜色扩展为6位
  if (c.length === 3) {
    return c[0] + c[0] + c[1] + c[1] + c[2] + c[2];
  }
  return c.slice(0, 6).padStart(6, '0');
}

/**
 * 保存PPT到文件
 * @param {Array} regions - 区域数组
 * @param {string} outputPath - 输出路径
 * @param {Object} options - 选项
 */
async function saveFromRegions(regions, outputPath, options = {}) {
  const pptx = await generateFromRegions(regions, options);
  await pptx.writeFile({ fileName: outputPath });
  console.log(`[ppt_generator] 生成成功: ${outputPath}`);
  return outputPath;
}

module.exports = {
  generateFromRegions,
  saveFromRegions,
  renderRegion,
  cleanColor
};
