#!/usr/bin/env node
// validation/scan-project.js
// 小程序境外适配扫描工具
//
// 核心目标：扫描小程序中所有中文文案，预测经过平台翻译后是否会在 CSS 容器中溢出/错乱
// 同时检测账号体系、表单等会导致境外用户无法使用的硬性问题
//
// 用法：node scan-project.js --project <小程序项目路径>
// 输出：reports/scan-report.md + reports/scan-result.json

const fs = require('fs')
const path = require('path')
const fg = require('fast-glob')

const overflowRiskRule = require('./rules/overflow-risk')
const i18nCoverageRule = require('./rules/i18n-coverage')

// ==================== 配置 ====================

const LANGUAGE_PARAMS = {
  en: { name: 'English', expansionFactor: 3.0, charWidthRatio: 0.5 },
  es: { name: 'Spanish', expansionFactor: 3.5, charWidthRatio: 0.52 },
  fr: { name: 'French', expansionFactor: 3.5, charWidthRatio: 0.52 },
  de: { name: 'German', expansionFactor: 4.0, charWidthRatio: 0.55 },
}

const RPX_TO_PX = 0.5
const DEFAULT_FONT_SIZE_RPX = 28
// 容器宽度低于此值视为噪音（icon/分隔线/padding 等，不会是文案容器）
const MIN_TEXT_CONTAINER_WIDTH_RPX = 40

// ==================== 工具函数 ====================

function detectMiniProgramRoot(inputPath) {
  if (fs.existsSync(path.join(inputPath, 'app.json'))) return inputPath
  const mpDir = path.join(inputPath, 'miniprogram')
  if (fs.existsSync(mpDir) && fs.existsSync(path.join(mpDir, 'app.json'))) return mpDir
  const projConfig = path.join(inputPath, 'project.config.json')
  if (fs.existsSync(projConfig)) {
    try {
      const config = JSON.parse(fs.readFileSync(projConfig, 'utf8'))
      if (config.miniprogramRoot) {
        const mpRoot = path.join(inputPath, config.miniprogramRoot)
        if (fs.existsSync(mpRoot)) return mpRoot
      }
    } catch (e) { /* ignore */ }
  }
  return inputPath
}

function estimateTranslatedWidth(chineseText, langParam, fontSizeRpx) {
  const cnCharCount = (chineseText.match(/[\u4e00-\u9fa5]/g) || []).length
  const nonCnCharCount = chineseText.length - cnCharCount
  const translatedCharCount = cnCharCount * langParam.expansionFactor + nonCnCharCount
  const fontSizePx = fontSizeRpx * RPX_TO_PX
  return Math.round(translatedCharCount * fontSizePx * langParam.charWidthRatio)
}

// ==================== 增强版容器匹配 ====================

function buildScopedContainerMap(containers) {
  const scopedMap = {}
  const globalMap = {}

  for (const c of containers) {
    const dir = path.dirname(c.file)
    if (!scopedMap[dir]) scopedMap[dir] = {}

    const effectiveWidth = (c.containerWidth && c.containerWidth >= 20) ? c.containerWidth : null
    const effectiveContainer = effectiveWidth ? c : { ...c, containerWidth: null }

    for (const cls of c.classNames) {
      if (['less', 'wxss', 'css'].includes(cls)) continue

      if (!scopedMap[dir][cls] || (effectiveContainer.containerWidth &&
          (!scopedMap[dir][cls].containerWidth || effectiveContainer.containerWidth > scopedMap[dir][cls].containerWidth))) {
        scopedMap[dir][cls] = effectiveContainer
      }

      if (!globalMap[cls] || (effectiveContainer.containerWidth &&
          (!globalMap[cls].containerWidth || effectiveContainer.containerWidth > globalMap[cls].containerWidth))) {
        globalMap[cls] = effectiveContainer
      }
    }
  }
  return { scopedMap, globalMap }
}

function findInMap(elementClasses, classMap) {
  if (!classMap) return null
  // 精确匹配
  for (const cls of elementClasses) {
    if (classMap[cls] && classMap[cls].containerWidth >= MIN_TEXT_CONTAINER_WIDTH_RPX) return classMap[cls]
  }
  // BEM 子串匹配
  for (const cls of elementClasses) {
    for (const [key, val] of Object.entries(classMap)) {
      if (cls.length >= 3 && key.length >= 3 && val.containerWidth >= MIN_TEXT_CONTAINER_WIDTH_RPX) {
        if (key.includes(cls) || cls.includes(key)) return val
      }
    }
  }
  return null
}

function findContainerForText(elementClasses, scopedMap, globalMap, wxmlDir) {
  // 策略1：同目录匹配
  const c1 = findInMap(elementClasses, scopedMap[wxmlDir])
  if (c1) return { container: c1, scope: 'same-dir' }

  // 策略2：全局匹配
  const c2 = findInMap(elementClasses, globalMap)
  if (c2) return { container: c2, scope: 'global-fallback' }

  return { container: null, scope: null }
}

// ==================== 翻译后溢出预测（核心功能）====================

function predictOverflow(projectRoot) {
  const findings = []

  // 1. 获取所有 CSS 容器
  const containers = overflowRiskRule.getAllContainers(projectRoot)

  // 2. 获取所有中文文案
  const i18nFindings = i18nCoverageRule.run({ projectRoot })
  const wxmlTexts = i18nFindings.filter(f => f.ruleId === 'I18N_HARDCODED_CN')

  // 3. 构建容器映射
  const { scopedMap, globalMap } = buildScopedContainerMap(containers)

  // 4. CSS 有固定宽度但无溢出保护的选择器
  const overflowFindings = overflowRiskRule.run({ projectRoot })
  const unguardedSelectors = new Set(overflowFindings.map(f => f.selector).filter(Boolean))

  // 5. 对每个文案做溢出预测
  let skippedLow = 0
  for (const text of wxmlTexts) {
    if (!text.chineseText) continue

    const elementClasses = (text.elementClass || '').split(/\s+/).filter(Boolean)
    const wxmlDir = path.dirname(text.file)
    const { container, scope } = findContainerForText(elementClasses, scopedMap, globalMap, wxmlDir)

    if (!container || !container.containerWidth) continue // 无容器约束 = 不报

    const containerWidthPx = container.containerWidth * RPX_TO_PX
    const fontSizeRpx = container.fontSize || DEFAULT_FONT_SIZE_RPX

    // 各语言溢出估算
    const langResults = {}
    let worstRatio = 0
    let worstLang = ''

    for (const [lang, params] of Object.entries(LANGUAGE_PARAMS)) {
      const estWidth = estimateTranslatedWidth(text.chineseText, params, fontSizeRpx)
      const ratio = Math.round((estWidth / containerWidthPx) * 100) / 100
      langResults[lang] = { ratio, estWidth, riskLevel: ratio > 1.0 ? 'HIGH' : ratio > 0.8 ? 'MEDIUM' : 'LOW' }
      if (ratio > worstRatio) {
        worstRatio = ratio
        worstLang = lang
      }
    }

    // 只报告 HIGH 和 MEDIUM
    if (worstRatio <= 0.8) {
      skippedLow++
      continue
    }

    const priority = worstRatio > 1.0 ? 'P0' : 'P1'
    const isUnguarded = container.selector && unguardedSelectors.has(container.selector)

    findings.push({
      priority,
      category: 'overflow-predict',
      ruleId: worstRatio > 1.0 ? 'OVERFLOW_HIGH' : 'OVERFLOW_MEDIUM',
      file: text.file,
      line: text.line,
      chineseText: text.chineseText,
      tagName: text.tagName,
      attrName: text.attrName,
      containerSelector: container.selector,
      containerFile: container.file,
      containerWidthRpx: container.containerWidth,
      containerWidthPx,
      fontSizeRpx,
      matchedClass: scope,
      hasOverflowGuard: !isUnguarded,
      langResults,
      worstLang,
      worstRatio,
      message: `"${text.chineseText}" 翻译后预计溢出 ${worstRatio}x（${LANGUAGE_PARAMS[worstLang].name}），容器 ${container.containerWidth}rpx`,
      suggestion: isUnguarded
        ? `容器 "${container.selector}" 无溢出保护，建议添加 overflow:hidden; text-overflow:ellipsis; 或改为 min-width+padding 弹性布局`
        : `容器 "${container.selector}" 宽度不足，建议放宽 width 或改为 flex 弹性布局`
    })
  }

  findings._skippedLow = skippedLow
  return findings
}

// ==================== CSS 溢出风险（无保护的固定宽度容器）====================

function checkCssOverflowRisk(projectRoot) {
  const findings = []
  const overflowFindings = overflowRiskRule.run({ projectRoot })

  for (const item of overflowFindings) {
    findings.push({
      priority: 'P1',
      category: 'css-risk',
      ruleId: 'CSS_OVERFLOW_NO_GUARD',
      file: item.file,
      line: item.line,
      message: item.message,
      suggestion: '添加 overflow:hidden; text-overflow:ellipsis; 或将固定 width 改为 min-width + padding',
      selector: item.selector,
      containerWidth: item.containerWidth
    })
  }

  return findings
}

// ==================== 账号体系检测（仅检测硬性问题）====================

function checkAccountSystem(projectRoot) {
  const findings = []

  const jsFiles = fg.sync(['**/*.js', '**/*.ts'], {
    cwd: projectRoot, absolute: true,
    ignore: ['node_modules/**', 'miniprogram_npm/**']
  })
  const wxmlFiles = fg.sync(['**/*.wxml'], {
    cwd: projectRoot, absolute: true,
    ignore: ['node_modules/**', 'miniprogram_npm/**']
  })

  for (const f of jsFiles) {
    const code = fs.readFileSync(f, 'utf8')
    const lines = code.split('\n')

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i]

      // 手机号硬编码 +86
      if (/areaCode\s*[:=]\s*['"]?\+86['"]?/.test(line)) {
        findings.push({
          priority: 'P0',
          category: 'account',
          ruleId: 'PHONE_86_HARDCODED',
          file: f,
          line: i + 1,
          message: '手机号区号硬编码为 +86，境外用户无法使用',
          suggestion: '增加国际区号选择器',
          evidence: line.trim()
        })
      }

      // 手机号 11 位硬编码校验
      if (/\.length\s*[!=]==?\s*11\b/.test(line) && /phone|mobile|tel/i.test(line)) {
        findings.push({
          priority: 'P0',
          category: 'account',
          ruleId: 'PHONE_LENGTH_11',
          file: f,
          line: i + 1,
          message: '手机号校验硬编码为 11 位，境外手机号位数不同（8-15 位）',
          suggestion: '根据区号动态校验位数',
          evidence: line.trim()
        })
      }
    }
  }

  for (const f of wxmlFiles) {
    const content = fs.readFileSync(f, 'utf8')
    const lines = content.split('\n')

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i]
      if (/maxlength\s*=\s*["']11["']/i.test(line) && /phone|tel|mobile/i.test(line)) {
        findings.push({
          priority: 'P0',
          category: 'account',
          ruleId: 'PHONE_MAXLENGTH_11',
          file: f,
          line: i + 1,
          message: '手机号输入框 maxlength=11，境外手机号会被截断',
          suggestion: '将 maxlength 改为 20',
          evidence: line.trim()
        })
      }
    }
  }

  return findings
}

// ==================== 表单国际化检测 ====================

function checkFormIssues(projectRoot) {
  const findings = []

  const jsFiles = fg.sync(['**/*.js', '**/*.ts'], {
    cwd: projectRoot, absolute: true,
    ignore: ['node_modules/**', 'miniprogram_npm/**']
  })

  for (const f of jsFiles) {
    const code = fs.readFileSync(f, 'utf8')
    const lines = code.split('\n')

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i]

      // 姓名仅限中文
      if (/[\u4e00-\u9fa5]\{2,10\}/.test(line) && !/A-Za-z/.test(line)) {
        findings.push({
          priority: 'P0',
          category: 'form',
          ruleId: 'NAME_CN_ONLY',
          file: f,
          line: i + 1,
          message: '姓名校验仅允许中文字符，境外用户英文姓名无法输入',
          suggestion: '放宽正则，允许英文+空格+连字符，长度上限改为 50',
          evidence: line.trim()
        })
      }
    }
  }

  return findings
}

// ==================== 报告生成 ====================

function generateReport(projectRoot, inputRoot, allFindings) {
  const lines = []

  const p0 = allFindings.filter(f => f.priority === 'P0')
  const p1 = allFindings.filter(f => f.priority === 'P1')

  const overflowItems = allFindings.filter(f => f.category === 'overflow-predict')
  const cssRiskItems = allFindings.filter(f => f.category === 'css-risk')
  const accountItems = allFindings.filter(f => f.category === 'account')
  const formItems = allFindings.filter(f => f.category === 'form')

  lines.push('# 小程序境外适配扫描报告')
  lines.push('')
  lines.push(`**项目路径**: \`${inputRoot}\``)
  lines.push(`**小程序根目录**: \`${projectRoot}\``)
  lines.push(`**扫描时间**: ${new Date().toISOString()}`)
  lines.push('')

  // 总览
  lines.push('## 总览')
  lines.push('')
  lines.push('| 优先级 | 数量 | 说明 |')
  lines.push('|--------|------|------|')
  lines.push(`| P0 (必须修复) | ${p0.length} | 翻译后确定溢出 / 账号表单硬性阻塞 |`)
  lines.push(`| P1 (建议修复) | ${p1.length} | 翻译后可能溢出 / CSS 缺少溢出保护 |`)
  lines.push(`| 合计 | ${allFindings.length} | |`)
  lines.push('')

  if (overflowItems.length > 0 || cssRiskItems.length > 0) {
    lines.push(`**翻译后溢出**: ${overflowItems.filter(f => f.ruleId === 'OVERFLOW_HIGH').length} 处高风险, ${overflowItems.filter(f => f.ruleId === 'OVERFLOW_MEDIUM').length} 处中风险`)
    lines.push(`**CSS 无保护容器**: ${cssRiskItems.length} 处固定宽度无 overflow 保护`)
  }
  if (accountItems.length > 0 || formItems.length > 0) {
    lines.push(`**账号/表单问题**: ${accountItems.length + formItems.length} 处`)
  }
  lines.push('')

  // 翻译后溢出详情
  const highOverflow = overflowItems.filter(f => f.ruleId === 'OVERFLOW_HIGH')
  const medOverflow = overflowItems.filter(f => f.ruleId === 'OVERFLOW_MEDIUM')

  if (highOverflow.length > 0) {
    lines.push('## P0 -- 翻译后确定溢出')
    lines.push('')
    lines.push('以下中文文案翻译为其他语言后，估算宽度超出所在 CSS 容器，会导致文字溢出/截断/重叠。')
    lines.push('')
    lines.push('| # | 中文文案 | 文件:行 | 容器宽度 | 容器选择器 | 最严重语言 | 溢出倍数 | 有保护 | 建议 |')
    lines.push('|---|---------|---------|---------|-----------|-----------|---------|--------|------|')
    highOverflow.forEach((f, idx) => {
      const relFile = f.file ? path.relative(inputRoot, f.file) : '-'
      const langName = LANGUAGE_PARAMS[f.worstLang] ? LANGUAGE_PARAMS[f.worstLang].name : f.worstLang
      const guard = f.hasOverflowGuard ? 'Yes' : '**No**'
      lines.push(`| ${idx + 1} | ${esc(f.chineseText)} | ${esc(relFile)}:${f.line} | ${f.containerWidthRpx}rpx | ${esc((f.containerSelector || '').slice(0, 40))} | ${langName} | ${f.worstRatio}x | ${guard} | ${esc(f.suggestion)} |`)
    })
    lines.push('')
  }

  if (medOverflow.length > 0) {
    lines.push('## P1 -- 翻译后可能溢出')
    lines.push('')
    lines.push('以下文案翻译后宽度接近容器边界（80%-100%），特定语言下可能溢出。')
    lines.push('')
    lines.push('| # | 中文文案 | 文件:行 | 容器宽度 | 最严重语言 | 溢出比率 | 建议 |')
    lines.push('|---|---------|---------|---------|-----------|---------|------|')
    medOverflow.forEach((f, idx) => {
      const relFile = f.file ? path.relative(inputRoot, f.file) : '-'
      const langName = LANGUAGE_PARAMS[f.worstLang] ? LANGUAGE_PARAMS[f.worstLang].name : f.worstLang
      lines.push(`| ${idx + 1} | ${esc(f.chineseText)} | ${esc(relFile)}:${f.line} | ${f.containerWidthRpx}rpx | ${langName} | ${f.worstRatio}x | ${esc(f.suggestion)} |`)
    })
    lines.push('')
  }

  // CSS 溢出风险
  if (cssRiskItems.length > 0) {
    lines.push('## P1 -- CSS 固定宽度无溢出保护')
    lines.push('')
    lines.push('以下 CSS 选择器使用固定宽度但缺少 overflow/word-break/text-overflow 保护，翻译后文案可能溢出。')
    lines.push('')
    lines.push('| # | 文件:行 | 选择器 | 建议 |')
    lines.push('|---|---------|--------|------|')
    cssRiskItems.forEach((f, idx) => {
      const relFile = f.file ? path.relative(inputRoot, f.file) : '-'
      lines.push(`| ${idx + 1} | ${esc(relFile)}:${f.line} | ${esc((f.selector || '').slice(0, 50))} | ${esc(f.suggestion)} |`)
    })
    lines.push('')
  }

  // 账号/表单
  if (accountItems.length > 0 || formItems.length > 0) {
    lines.push('## 账号体系 / 表单问题')
    lines.push('')
    lines.push('| # | 类别 | 文件:行 | 问题 | 建议 |')
    lines.push('|---|------|---------|------|------|')
    ;[...accountItems, ...formItems].forEach((f, idx) => {
      const relFile = f.file ? path.relative(inputRoot, f.file) : '-'
      lines.push(`| ${idx + 1} | ${f.priority} | ${esc(relFile)}:${f.line || '-'} | ${esc(f.message)} | ${esc(f.suggestion)} |`)
    })
    lines.push('')
  }

  // 扫描范围说明
  lines.push('## 扫描说明')
  lines.push('')
  const totalTexts = allFindings._totalTexts || 0
  const withContainer = allFindings._withContainer || 0
  const withoutContainer = allFindings._withoutContainer || 0
  lines.push(`- WXML 中文文案总数: ${totalTexts}`)
  lines.push(`- 匹配到 CSS 容器约束: ${withContainer}（已完成溢出预测）`)
  lines.push(`- 未匹配到容器约束: ${withoutContainer}（通常在 flex 布局或全屏宽度中，溢出风险较低）`)
  lines.push(`- 溢出预测使用 4 种目标语言: English(3.0x), Spanish(3.5x), French(3.5x), German(4.0x)`)
  lines.push('')

  return lines.join('\n')
}

function esc(s) {
  return (s || '').replace(/\|/g, '\\|').replace(/\n/g, ' ')
}

// ==================== 去重 ====================

function dedup(findings) {
  const seen = new Set()
  return findings.filter(f => {
    const key = `${f.ruleId}:${f.file}:${f.line}:${(f.chineseText || f.message || '').slice(0, 30)}`
    if (seen.has(key)) return false
    seen.add(key)
    return true
  })
}

// ==================== CLI 入口 ====================

function main() {
  const args = process.argv.slice(2)
  let inputRoot = null

  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--project' && args[i + 1]) {
      inputRoot = path.resolve(args[i + 1])
      i++
    }
  }

  if (!inputRoot) {
    console.error('Usage: node scan-project.js --project <path-to-miniprogram>')
    process.exit(1)
  }

  if (!fs.existsSync(inputRoot)) {
    console.error(`Project root not found: ${inputRoot}`)
    process.exit(1)
  }

  const projectRoot = detectMiniProgramRoot(inputRoot)
  console.log(`Input path: ${inputRoot}`)
  console.log(`Detected miniprogram root: ${projectRoot}`)
  console.log('')

  // 1. 翻译后溢出预测
  console.log('== 1. 翻译后溢出预测 ==')
  const overflowFindings = predictOverflow(projectRoot)
  const highCount = overflowFindings.filter(f => f.ruleId === 'OVERFLOW_HIGH').length
  const medCount = overflowFindings.filter(f => f.ruleId === 'OVERFLOW_MEDIUM').length
  console.log(`  HIGH: ${highCount}, MEDIUM: ${medCount}`)

  // 2. CSS 溢出风险
  console.log('== 2. CSS 无保护容器 ==')
  const cssFindings = checkCssOverflowRisk(projectRoot)
  console.log(`  发现 ${cssFindings.length} 处`)

  // 3. 账号体系
  console.log('== 3. 账号体系检测 ==')
  const accountFindings = checkAccountSystem(projectRoot)
  console.log(`  发现 ${accountFindings.length} 处`)

  // 4. 表单问题
  console.log('== 4. 表单问题检测 ==')
  const formFindings = checkFormIssues(projectRoot)
  console.log(`  发现 ${formFindings.length} 处`)

  // 汇总
  let allFindings = dedup([
    ...overflowFindings,
    ...cssFindings,
    ...accountFindings,
    ...formFindings
  ])

  const priorityOrder = { P0: 0, P1: 1, P2: 2 }
  allFindings.sort((a, b) => (priorityOrder[a.priority] || 9) - (priorityOrder[b.priority] || 9))

  // 获取文案统计（用于报告）
  const i18nFindings = i18nCoverageRule.run({ projectRoot })
  const wxmlTexts = i18nFindings.filter(f => f.ruleId === 'I18N_HARDCODED_CN')
  allFindings._totalTexts = wxmlTexts.length
  allFindings._withContainer = overflowFindings.length + overflowFindings._skippedLow
  allFindings._withoutContainer = wxmlTexts.length - (overflowFindings.length + (overflowFindings._skippedLow || 0))

  const p0 = allFindings.filter(f => f.priority === 'P0').length
  const p1 = allFindings.filter(f => f.priority === 'P1').length

  console.log(`\n== 扫描完成 ==`)
  console.log(`P0 (必须修复): ${p0}`)
  console.log(`P1 (建议修复): ${p1}`)
  console.log(`合计: ${allFindings.length}`)

  // 生成报告
  const report = generateReport(projectRoot, inputRoot, allFindings)

  const reportsDir = path.join(__dirname, 'reports')
  fs.mkdirSync(reportsDir, { recursive: true })

  const reportPath = path.join(reportsDir, 'scan-report.md')
  fs.writeFileSync(reportPath, report)
  console.log(`\nReport: ${reportPath}`)

  const resultPath = path.join(reportsDir, 'scan-result.json')
  fs.writeFileSync(resultPath, JSON.stringify({
    generatedAt: new Date().toISOString(),
    inputRoot,
    projectRoot,
    summary: {
      total: allFindings.length, p0, p1,
      overflowHigh: highCount, overflowMedium: medCount,
      cssRisk: cssFindings.length,
      account: accountFindings.length, form: formFindings.length,
      totalTexts: wxmlTexts.length
    },
    findings: allFindings
  }, null, 2))
  console.log(`Result: ${resultPath}`)

  process.exit(p0 > 0 ? 1 : 0)
}

if (require.main === module) {
  main()
}

module.exports = { main, predictOverflow, checkCssOverflowRisk, checkAccountSystem, checkFormIssues }
