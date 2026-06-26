#!/usr/bin/env node
// validation/overflow-predict.js
// 文案-容器关联脚本（v1.3.0）
//
// 功能：将 i18n-coverage 检出的硬编码中文文案与 overflow-risk 检出的 CSS 容器信息
// 按 class 名关联，输出结构化 JSON 供 AI agent 做"翻译后溢出预测"
//
// 用法：node overflow-predict.js --project <小程序项目路径>
// 输出：overflow-predict-input.json（写入当前目录）

const fs = require('fs')
const path = require('path')
const overflowRule = require('./rules/overflow-risk')
const i18nRule = require('./rules/i18n-coverage')

// ==================== 配置 ====================

// 各语言文本膨胀参数（相对于中文字符数）
// 来源：W3C 国际化最佳实践 + IBM Globalization Guidelines
const LANGUAGE_PARAMS = {
  en: {
    name: 'English',
    // 中文 N 个字 → 英文约 N * expansionFactor 个字符
    expansionFactor: 3.0,
    // 英文字符平均宽度占中文字符的比例（等宽中文 1em，英文平均约 0.5em）
    charWidthRatio: 0.5,
  },
  es: {
    name: 'Spanish',
    expansionFactor: 3.5,
    charWidthRatio: 0.52,
  },
  it: {
    name: 'Italian',
    expansionFactor: 3.3,
    charWidthRatio: 0.52,
  },
  fr: {
    name: 'French',
    expansionFactor: 3.5,
    charWidthRatio: 0.52,
  },
  de: {
    name: 'German',
    expansionFactor: 4.0,
    charWidthRatio: 0.55,
  },
}

// rpx -> px 换算（标准 375px 设计稿）
const RPX_TO_PX = 0.5

// 默认字体大小（rpx），当 CSS 中没有指定 font-size 时使用
const DEFAULT_FONT_SIZE_RPX = 28

// 容器宽度最小有效值（rpx），低于此值视为噪音（如 LESS 嵌套中的分隔线 width: 2rpx）
const MIN_VALID_CONTAINER_WIDTH_RPX = 20

// ==================== 核心逻辑 ====================

/**
 * 估算中文文案在目标语言下的像素宽度
 * @param {string} chineseText - 中文原文
 * @param {object} langParam - 语言参数
 * @param {number} fontSizeRpx - 字号（rpx）
 * @returns {number} 估算像素宽度
 */
function estimateTranslatedWidth(chineseText, langParam, fontSizeRpx) {
  // 统计中文字符数（每个中文字符约占 1em 宽度）
  const cnCharCount = (chineseText.match(/[\u4e00-\u9fa5]/g) || []).length
  // 非中文字符（数字、英文、符号等）保持原宽度估算
  const nonCnCharCount = chineseText.length - cnCharCount

  // 翻译后的目标语言字符数 = 中文字符数 * 膨胀系数 + 非中文字符数
  const translatedCharCount = cnCharCount * langParam.expansionFactor + nonCnCharCount

  // 翻译后文本像素宽度 = 目标语言字符数 * 字符平均宽度（px）
  // 字符平均宽度 = fontSize(px) * charWidthRatio
  const fontSizePx = fontSizeRpx * RPX_TO_PX
  const estimatedWidth = translatedCharCount * fontSizePx * langParam.charWidthRatio

  return Math.round(estimatedWidth)
}

/**
 * 将容器宽度转为 px
 */
function containerWidthToPx(width, unit) {
  if (unit === 'px') return width
  if (unit === 'rpx') return width * RPX_TO_PX
  return width
}

/**
 * 获取文件所属的"页面/组件目录"路径
 * 例如: /project/pages/home/index.wxml -> /project/pages/home
 *       /project/components/nav/index.wxml -> /project/components/nav
 *       /project/custom-tab-bar/index.wxml -> /project/custom-tab-bar
 */
function getComponentDir(filePath) {
  return path.dirname(filePath)
}

/**
 * 构建 class -> container 的映射（按目录分组）
 * 返回 { dirPath: { className: containerInfo } } 的两层结构
 * 以及一个不区分目录的全局 fallback map
 */
function buildScopedClassContainerMap(containers) {
  const scopedMap = {} // dirPath -> { className -> container }
  const globalMap = {} // className -> container (fallback)

  for (const c of containers) {
    const dir = getComponentDir(c.file)

    if (!scopedMap[dir]) scopedMap[dir] = {}

    // 如果容器宽度低于最小有效值，忽略其宽度（可能是 LESS 嵌套中的分隔线/图标等）
    const effectiveWidth = (c.containerWidth && c.containerWidth >= MIN_VALID_CONTAINER_WIDTH_RPX)
      ? c.containerWidth : null
    const effectiveContainer = effectiveWidth ? c : { ...c, containerWidth: null }

    for (const cls of c.classNames) {
      // 跳过无意义的 class（如 less/wxss 等因选择器解析引入的噪音）
      if (['less', 'wxss', 'css'].includes(cls)) continue

      // 分目录映射：如果同目录已有，取宽度更小的（更严格的约束）
      if (scopedMap[dir][cls]) {
        if (effectiveContainer.containerWidth && (!scopedMap[dir][cls].containerWidth || effectiveContainer.containerWidth < scopedMap[dir][cls].containerWidth)) {
          scopedMap[dir][cls] = effectiveContainer
        }
      } else {
        scopedMap[dir][cls] = effectiveContainer
      }

      // 全局映射
      if (globalMap[cls]) {
        if (effectiveContainer.containerWidth && (!globalMap[cls].containerWidth || effectiveContainer.containerWidth < globalMap[cls].containerWidth)) {
          globalMap[cls] = effectiveContainer
        }
      } else {
        globalMap[cls] = effectiveContainer
      }
    }
  }
  return { scopedMap, globalMap }
}

/**
 * 在指定的 classMap 中查找匹配的容器
 * 支持精确匹配和 BEM 子串匹配
 */
function findContainerInMap(elementClasses, classMap) {
  if (!classMap) return { container: null, matchedClass: '' }

  for (const cls of elementClasses) {
    // 精确匹配优先
    if (classMap[cls]) {
      return { container: classMap[cls], matchedClass: cls }
    }
  }

  // BEM 子串匹配（仅在精确匹配全部失败后尝试）
  for (const cls of elementClasses) {
    for (const [key, val] of Object.entries(classMap)) {
      // 要求子串匹配有一定长度门槛，避免 "my" 之类的短 class 误匹配
      if (cls.length >= 3 && key.length >= 3) {
        if (key.includes(cls) || cls.includes(key)) {
          return { container: val, matchedClass: key }
        }
      }
    }
  }

  return { container: null, matchedClass: '' }
}

/**
 * 关联文案与容器（同目录优先匹配）
 */
function correlate(i18nFindings, containers) {
  const { scopedMap, globalMap } = buildScopedClassContainerMap(containers)
  const results = []

  for (const finding of i18nFindings) {
    if (!finding.chineseText) continue

    const chineseText = finding.chineseText
    const elementClasses = (finding.elementClass || '').split(/\s+/).filter(Boolean)
    const wxmlDir = getComponentDir(finding.file)

    // 策略 1: 优先在同目录的 CSS 中查找
    let matchedContainer = null
    let matchedClass = ''
    let matchScope = ''

    const sameDir = findContainerInMap(elementClasses, scopedMap[wxmlDir])
    if (sameDir.container) {
      matchedContainer = sameDir.container
      matchedClass = sameDir.matchedClass
      matchScope = 'same-dir'
    }

    // 策略 2: 同目录没找到，尝试全局映射（降级，标记为 global）
    if (!matchedContainer) {
      const global = findContainerInMap(elementClasses, globalMap)
      if (global.container) {
        matchedContainer = global.container
        matchedClass = global.matchedClass
        matchScope = 'global-fallback'
      }
    }

    // 容器信息
    const containerWidthRpx = matchedContainer ? matchedContainer.containerWidth : null
    const containerWidthPx = containerWidthRpx 
      ? containerWidthToPx(containerWidthRpx, matchedContainer.widthUnit || 'rpx')
      : null
    const fontSizeRpx = (matchedContainer && matchedContainer.fontSize) || DEFAULT_FONT_SIZE_RPX

    // 估算各语言的溢出风险
    const langEstimates = {}
    for (const [lang, params] of Object.entries(LANGUAGE_PARAMS)) {
      const estimatedWidth = estimateTranslatedWidth(chineseText, params, fontSizeRpx)
      let riskLevel = 'unknown'
      let ratio = null

      if (containerWidthPx) {
        ratio = estimatedWidth / containerWidthPx
        if (ratio > 1.0) riskLevel = 'high'
        else if (ratio > 0.8) riskLevel = 'medium'
        else riskLevel = 'low'
      }

      langEstimates[lang] = {
        language: params.name,
        estimatedWidthPx: estimatedWidth,
        ratio: ratio ? Math.round(ratio * 100) / 100 : null,
        riskLevel,
      }
    }

    results.push({
      // 文案信息
      chineseText,
      chineseCharCount: (chineseText.match(/[\u4e00-\u9fa5]/g) || []).length,
      file: finding.file,
      line: finding.line,
      tagName: finding.tagName || '',
      attrName: finding.attrName || '',

      // 容器信息
      matchedClass: matchedClass || null,
      matchScope: matchScope || null,
      containerSelector: matchedContainer ? matchedContainer.selector : null,
      containerFile: matchedContainer ? matchedContainer.file : null,
      containerWidthRpx: containerWidthRpx || null,
      containerWidthPx: containerWidthPx || null,
      fontSizeRpx,
      fontSizePx: Math.round(fontSizeRpx * RPX_TO_PX),
      hasContainerConstraint: !!containerWidthPx,

      // 各语言估算
      langEstimates,
    })
  }

  return results
}

/**
 * 生成摘要统计
 */
function generateSummary(results) {
  const summary = {
    totalTexts: results.length,
    withContainerConstraint: results.filter(r => r.hasContainerConstraint).length,
    withoutContainerConstraint: results.filter(r => !r.hasContainerConstraint).length,
    riskByLanguage: {},
  }

  for (const lang of Object.keys(LANGUAGE_PARAMS)) {
    const counts = { high: 0, medium: 0, low: 0, unknown: 0 }
    for (const r of results) {
      const risk = r.langEstimates[lang].riskLevel
      counts[risk]++
    }
    summary.riskByLanguage[lang] = counts
  }

  return summary
}

// ==================== CLI 入口 ====================

function main() {
  // 解析命令行参数
  const args = process.argv.slice(2)
  let projectRoot = null

  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--project' && args[i + 1]) {
      projectRoot = path.resolve(args[i + 1])
      i++
    }
  }

  if (!projectRoot) {
    console.error('Usage: node overflow-predict.js --project <path-to-miniprogram>')
    process.exit(1)
  }

  if (!fs.existsSync(projectRoot)) {
    console.error(`Project root not found: ${projectRoot}`)
    process.exit(1)
  }

  console.log(`Scanning project: ${projectRoot}`)
  console.log()

  // Step 1: 获取所有 CSS 容器（包含无风险的）
  const containers = overflowRule.getAllContainers(projectRoot)
  console.log(`Found ${containers.length} CSS containers with width/font-size constraints`)

  // Step 2: 获取所有硬编码中文文案
  const i18nFindings = i18nRule.run({ projectRoot })
  const wxmlFindings = i18nFindings.filter(f => f.ruleId === 'I18N_HARDCODED_CN')
  const jsFindings = i18nFindings.filter(f => f.ruleId === 'I18N_HARDCODED_CN_JS')
  console.log(`Found ${wxmlFindings.length} WXML hardcoded Chinese texts`)
  console.log(`Found ${jsFindings.length} JS hardcoded Chinese texts`)

  // Step 3: 关联文案与容器（只处理 WXML，JS 文案无法直接关联 CSS）
  const results = correlate(wxmlFindings, containers)

  // Step 4: 生成摘要
  const summary = generateSummary(results)

  // Step 5: 输出 JSON
  const output = {
    meta: {
      generatedAt: new Date().toISOString(),
      projectRoot,
      languageParams: LANGUAGE_PARAMS,
      rpxToPx: RPX_TO_PX,
      defaultFontSizeRpx: DEFAULT_FONT_SIZE_RPX,
    },
    summary,
    items: results,
    jsTexts: jsFindings.map(f => ({
      chineseText: f.chineseText,
      file: f.file,
      line: f.line,
      fieldName: f.fieldName,
      note: 'JS 文案无法自动关联 CSS 容器，需 agent 根据上下文判断是否有溢出风险（如 toast/modal 通常由框架控制宽度，button 文案需关注）'
    })),
  }

  const outputPath = path.join(__dirname, 'overflow-predict-input.json')
  fs.writeFileSync(outputPath, JSON.stringify(output, null, 2), 'utf8')
  console.log(`\nOutput written to: ${outputPath}`)

  // 打印摘要
  console.log('\n=== Overflow Prediction Summary ===')
  console.log(`Total WXML texts analyzed: ${summary.totalTexts}`)
  console.log(`  With container constraint: ${summary.withContainerConstraint}`)
  console.log(`  Without (uses screen width): ${summary.withoutContainerConstraint}`)
  console.log()
  console.log('Risk by language:')
  for (const [lang, counts] of Object.entries(summary.riskByLanguage)) {
    const langName = LANGUAGE_PARAMS[lang].name
    console.log(`  ${langName}: HIGH=${counts.high} MEDIUM=${counts.medium} LOW=${counts.low} UNKNOWN=${counts.unknown}`)
  }

  // 打印高风险项
  const highRiskItems = results.filter(r => 
    Object.values(r.langEstimates).some(e => e.riskLevel === 'high')
  )
  if (highRiskItems.length > 0) {
    console.log(`\n=== High Risk Items (${highRiskItems.length}) ===`)
    for (const item of highRiskItems) {
      const relFile = path.relative(projectRoot, item.file)
      const highLangs = Object.entries(item.langEstimates)
        .filter(([, e]) => e.riskLevel === 'high')
        .map(([lang, e]) => `${lang}(${e.ratio}x)`)
        .join(', ')
      console.log(`  "${item.chineseText}" [${relFile}:${item.line}] -> container ${item.containerWidthRpx}rpx -> ${highLangs}`)
    }
  }

  console.log('\nDone. Feed overflow-predict-input.json to AI agent for translation + final overflow judgment.')
}

// 导出供测试用
module.exports = { correlate, estimateTranslatedWidth, buildScopedClassContainerMap, LANGUAGE_PARAMS }

// CLI 运行
if (require.main === module) {
  main()
}
