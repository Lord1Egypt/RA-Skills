/**
 * 坐标映射器 - Pixel → EMU转换
 * 基于Images2Slides论文的归一化坐标映射算法
 * EMU: English Metric Units, 914400 EMU = 1 inch
 *
 * v1.1 更新: 增强JSON解析容错性 + 全角/半角符号校正
 */

// 标准PPT尺寸 (16:9)
const SLIDE_WIDTH_EMU = 9144000;   // 10英寸
const SLIDE_HEIGHT_EMU = 5143500;  // 5.625英寸
const DPI = 96;

/**
 * 像素转EMU
 * @param {number} pixel - 像素值
 * @param {number} dpi - DPI，默认96
 * @returns {number} EMU值
 */
function pixelToEmu(pixel, dpi = DPI) {
  return Math.round(pixel * 914400 / dpi);
}

/**
 * 归一化坐标映射（论文核心算法）
 * @param {Object} region - 区域对象
 * @param {number} imageWidth - 原始图像宽度
 * @param {number} imageHeight - 原始图像高度
 * @param {number} slideWidth - 幻灯片宽度(EMU)
 * @param {number} slideHeight - 幻灯片高度(EMU)
 * @returns {Object} 映射后的坐标
 */
function normalizeAndMap(region, imageWidth, imageHeight, slideWidth = SLIDE_WIDTH_EMU, slideHeight = SLIDE_HEIGHT_EMU) {
  const scaleX = slideWidth / imageWidth;
  const scaleY = slideHeight / imageHeight;

  return {
    x: Math.round(region.bounds.x * scaleX),
    y: Math.round(region.bounds.y * scaleY),
    w: Math.round(region.bounds.width * scaleX),
    h: Math.round(region.bounds.height * scaleY)
  };
}

/**
 * 批量映射区域数组
 * @param {Array} regions - 区域数组
 * @param {number} imageWidth - 图像宽度
 * @param {number} imageHeight - 图像高度
 * @returns {Array} 映射后的区域数组
 */
function mapAllRegions(regions, imageWidth, imageHeight) {
  return regions.map(region => ({
    ...region,
    mapped: normalizeAndMap(region, imageWidth, imageHeight)
  }));
}

/**
 * 【短期优化】全角/半角符号校正
 * 将VLM误输出的全角括号、标点还原为原版中文排版常用形式
 * 规则: 分析报告 P0 - 括号全角/半角一致性
 * @param {string} text - 待校正的文本
 * @param {string} mode - 'keep_cn'保留中文全角 / 'ascii'转ASCII
 * @returns {string} 校正后文本
 */
function normalizeSymbols(text, mode = 'keep_cn') {
  if (!text || typeof text !== 'string') return text;

  if (mode === 'ascii') {
    // 将全角符号转为半角
    return text
      .replace(/（/g, '(').replace(/）/g, ')')
      .replace(/【/g, '[').replace(/】/g, ']')
      .replace(/「/g, '"').replace(/」/g, '"')
      .replace(/『/g, "'").replace(/』/g, "'")
      .replace(/，/g, ',').replace(/。/g, '.')
      .replace(/：/g, ':').replace(/；/g, ';')
      .replace(/！/g, '!').replace(/？/g, '?');
  }

  // mode === 'keep_cn': 仅修正明显错误（半角括号在中文语境中应为全角）
  // 此为保守模式，保持原样（由分析prompt确保精度）
  return text;
}

/**
 * 【短期优化】识别bullet符号类型并统一
 * @param {string} text - 文本内容
 * @returns {{ bulletChar: string|null, cleanText: string }} bullet类型和去除bullet后的文本
 */
function detectBullet(text) {
  if (!text) return { bulletChar: null, cleanText: text };

  // 匹配常见 bullet 符号
  const bulletPatterns = [
    { pattern: /^[■□▪▫•·]\s*/, char: '■' },
    { pattern: /^[✓✔]\s*/, char: '✓' },
    { pattern: /^[-–—]\s*/, char: '-' },
    { pattern: /^(\d+)[、.．。]\s*/, char: null }, // 数字编号，保留原样
  ];

  for (const { pattern, char } of bulletPatterns) {
    if (pattern.test(text)) {
      return {
        bulletChar: char,
        cleanText: text.replace(pattern, '').trim()
      };
    }
  }

  return { bulletChar: null, cleanText: text };
}

/**
 * 【短期优化】从MiniMax分析结果提取区域（增强版）
 * 增加：多策略JSON提取、字段校验、符号校正、bullet识别
 * @param {string} analysisText - MiniMax返回的分析文本
 * @returns {Array} 结构化区域数组
 */
function parseAnalysisToRegions(analysisText) {
  let parsed = null;

  // 策略1: 直接尝试完整JSON解析
  try {
    parsed = JSON.parse(analysisText.trim());
  } catch (_) {}

  // 策略2: 提取 JSON 数组
  if (!parsed) {
    try {
      const arrMatch = analysisText.match(/\[[\s\S]*\]/);
      if (arrMatch) parsed = JSON.parse(arrMatch[0]);
    } catch (_) {}
  }

  // 策略3: 提取 JSON 对象（包含regions字段）
  if (!parsed) {
    try {
      const objMatch = analysisText.match(/\{[\s\S]*\}/);
      if (objMatch) {
        const obj = JSON.parse(objMatch[0]);
        parsed = obj.regions || obj.elements || obj.items || obj;
      }
    } catch (_) {}
  }

  // 策略4: 提取代码块内的JSON
  if (!parsed) {
    try {
      const codeBlockMatch = analysisText.match(/```(?:json)?\s*([\s\S]*?)```/);
      if (codeBlockMatch) {
        const inner = codeBlockMatch[1].trim();
        parsed = JSON.parse(inner);
        if (!Array.isArray(parsed) && parsed.regions) parsed = parsed.regions;
      }
    } catch (_) {}
  }

  if (!parsed) {
    console.warn('[coordinate_mapper] JSON解析全部策略失败，返回空数组');
    return [];
  }

  const regions = Array.isArray(parsed) ? parsed : [parsed];

  // 后处理：字段校验 + 符号/bullet校正
  return regions.map((r, idx) => {
    // 确保bounds字段存在
    if (!r.bounds) {
      r.bounds = {
        x: r.x || 0,
        y: r.y || 0,
        width: r.width || r.w || 100,
        height: r.height || r.h || 30
      };
    }

    // 【短期优化P0】文字内容符号校正
    if (r.content) {
      r.content = normalizeSymbols(r.content, 'keep_cn');
    }

    // 【短期优化P0】bullet符号识别
    if (r.content && !r.bulletType) {
      const { bulletChar } = detectBullet(r.content);
      if (bulletChar) r.bulletType = bulletChar;
    }

    // 确保zIndex有值
    if (r.zIndex === undefined) r.zIndex = idx;

    return r;
  });
}

module.exports = {
  SLIDE_WIDTH_EMU,
  SLIDE_HEIGHT_EMU,
  DPI,
  pixelToEmu,
  normalizeAndMap,
  mapAllRegions,
  parseAnalysisToRegions,
  normalizeSymbols,
  detectBullet
};
