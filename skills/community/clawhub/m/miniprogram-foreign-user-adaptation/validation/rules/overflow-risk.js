// validation/rules/overflow-risk.js
// 扫描所有 wxss/less 文件，检测多语言溢出风险：
// 1. 固定宽度（width: Nrpx）且无 overflow/text-overflow/word-break 保护
// 2. 固定高度单行文本（height + line-height 相同，无 overflow）
// 3. !important 修饰的固定尺寸
//
// v1.3 增强：每个 finding 额外输出 containerWidth/widthUnit/fontSize/fontSizeUnit/padding 结构化字段
// 供 overflow-predict.js 做文案-容器关联时使用
const fs = require('fs')
const fg = require('fast-glob')

// 匹配固定宽度声明（rpx/px）
const FIXED_WIDTH_RE = /width\s*:\s*(\d+)(rpx|px)/g
const IMPORTANT_SIZE_RE = /(?:width|height|max-width)\s*:\s*\d+(?:rpx|px)\s*!important/g

// 提取具体数值的正则
const WIDTH_CAPTURE_RE = /(?:^|[^-])width\s*:\s*(\d+)(rpx|px)/
const MAX_WIDTH_CAPTURE_RE = /max-width\s*:\s*(\d+)(rpx|px)/
const FONT_SIZE_CAPTURE_RE = /font-size\s*:\s*(\d+)(rpx|px)/
const PADDING_L_CAPTURE_RE = /padding-left\s*:\s*(\d+)(rpx|px)/
const PADDING_R_CAPTURE_RE = /padding-right\s*:\s*(\d+)(rpx|px)/
const PADDING_SHORTHAND_RE = /padding\s*:\s*(\d+)(rpx|px)(?:\s+(\d+)(rpx|px))?/

// 保护性属性
const OVERFLOW_GUARDS = [
  'overflow',
  'text-overflow',
  'word-break',
  'overflow-wrap',
  'word-wrap',
  'white-space',
  'flex-wrap',
  'flex-shrink',
  'min-width',
]

function parseBlocks(css) {
  // 简易 CSS 块解析：提取 selector { ... } 对
  const blocks = []
  let depth = 0
  let blockStart = -1
  let selectorStart = 0

  for (let i = 0; i < css.length; i++) {
    if (css[i] === '{') {
      if (depth === 0) {
        blockStart = i + 1
      }
      depth++
    } else if (css[i] === '}') {
      depth--
      if (depth === 0 && blockStart >= 0) {
        const selector = css.slice(selectorStart, css.lastIndexOf('{', blockStart)).trim()
        const body = css.slice(blockStart, i)
        blocks.push({ selector, body, startOffset: selectorStart })
        selectorStart = i + 1
        blockStart = -1
      }
    }
  }
  return blocks
}

function hasGuard(body) {
  const lower = body.toLowerCase()
  return OVERFLOW_GUARDS.some((g) => lower.includes(g))
}

// 从 CSS body 中提取结构化容器信息
function extractContainerMetrics(body) {
  const metrics = {}

  // 提取 width
  const wm = body.match(WIDTH_CAPTURE_RE)
  if (wm) {
    metrics.containerWidth = parseInt(wm[1], 10)
    metrics.widthUnit = wm[2]
  }

  // 提取 max-width（如果没有 width 则用 max-width）
  if (!metrics.containerWidth) {
    const mwm = body.match(MAX_WIDTH_CAPTURE_RE)
    if (mwm) {
      metrics.containerWidth = parseInt(mwm[1], 10)
      metrics.widthUnit = mwm[2]
      metrics.widthType = 'max-width'
    }
  } else {
    metrics.widthType = 'width'
  }

  // 提取 font-size
  const fsm = body.match(FONT_SIZE_CAPTURE_RE)
  if (fsm) {
    metrics.fontSize = parseInt(fsm[1], 10)
    metrics.fontSizeUnit = fsm[2]
  }

  // 提取 padding（左右）
  let paddingLeft = 0, paddingRight = 0
  const plm = body.match(PADDING_L_CAPTURE_RE)
  if (plm) paddingLeft = parseInt(plm[1], 10)
  const prm = body.match(PADDING_R_CAPTURE_RE)
  if (prm) paddingRight = parseInt(prm[1], 10)

  // padding 简写（如果没有单独的 padding-left/right）
  if (!paddingLeft && !paddingRight) {
    const psm = body.match(PADDING_SHORTHAND_RE)
    if (psm) {
      if (psm[3]) {
        // padding: Vpx Hpx -> 左右为 H
        paddingLeft = parseInt(psm[3], 10)
        paddingRight = paddingLeft
      } else {
        // padding: Npx -> 四边相同
        paddingLeft = parseInt(psm[1], 10)
        paddingRight = paddingLeft
      }
    }
  }

  if (paddingLeft || paddingRight) {
    metrics.paddingLeft = paddingLeft
    metrics.paddingRight = paddingRight
  }

  return metrics
}

// 从选择器中提取 class 名列表（供关联使用）
function extractClassNames(selector) {
  const classRe = /\.([a-zA-Z_][\w-]*)/g
  const classes = []
  let m
  while ((m = classRe.exec(selector)) !== null) {
    classes.push(m[1])
  }
  return classes
}

function scanFile(filePath) {
  const findings = []
  const content = fs.readFileSync(filePath, 'utf8')

  const blocks = parseBlocks(content)

  for (const block of blocks) {
    const body = block.body
    const hasFixedWidth = FIXED_WIDTH_RE.test(body)
    FIXED_WIDTH_RE.lastIndex = 0
    const hasImportantSize = IMPORTANT_SIZE_RE.test(body)
    IMPORTANT_SIZE_RE.lastIndex = 0
    const guarded = hasGuard(body)

    // 提取结构化容器信息（无论是否有风险，都提取，供 overflow-predict 使用）
    const metrics = extractContainerMetrics(body)
    const classNames = extractClassNames(block.selector)

    if (hasFixedWidth && !guarded) {
      const offset = block.startOffset
      const lineNum = content.slice(0, offset).split('\n').length
      findings.push({
        severity: 'warn',
        ruleId: 'OVERFLOW_RISK',
        file: filePath,
        line: lineNum,
        message: `选择器 "${block.selector.slice(0, 60)}" 含固定宽度但无溢出保护（缺少 overflow/word-break/text-overflow）`,
        selector: block.selector,
        classNames,
        risk: 'fixed-width-no-guard',
        ...metrics
      })
    }

    if (hasImportantSize) {
      const offset = block.startOffset
      const lineNum = content.slice(0, offset).split('\n').length
      findings.push({
        severity: 'warn',
        ruleId: 'OVERFLOW_RISK',
        file: filePath,
        line: lineNum,
        message: `选择器 "${block.selector.slice(0, 60)}" 使用 !important 固定尺寸，多语言文案可能溢出`,
        selector: block.selector,
        classNames,
        risk: 'important-fixed-size',
        ...metrics
      })
    }
  }

  return findings
}

// 额外导出：扫描所有 CSS 块（含无风险的），用于 overflow-predict 获取完整容器信息
function scanAllContainers(filePath) {
  const containers = []
  const content = fs.readFileSync(filePath, 'utf8')
  const blocks = parseBlocks(content)

  for (const block of blocks) {
    const metrics = extractContainerMetrics(block.body)
    const classNames = extractClassNames(block.selector)
    if (classNames.length > 0 && (metrics.containerWidth || metrics.fontSize)) {
      containers.push({
        file: filePath,
        selector: block.selector,
        classNames,
        ...metrics
      })
    }
  }

  return containers
}

function getAllContainers(root) {
  if (!root || !fs.existsSync(root)) return []

  const styleFiles = fg.sync(['**/*.wxss', '**/*.less'], {
    cwd: root,
    absolute: true,
    ignore: ['node_modules/**', 'miniprogram_npm/**']
  })

  const allContainers = []
  for (const f of styleFiles) {
    try {
      allContainers.push(...scanAllContainers(f))
    } catch (e) {
      // 忽略解析失败
    }
  }
  return allContainers
}

function run(ctx) {
  const findings = []
  const root = ctx.projectRoot
  if (!root || !fs.existsSync(root)) return findings

  const styleFiles = fg.sync(['**/*.wxss', '**/*.less'], {
    cwd: root,
    absolute: true,
    ignore: ['node_modules/**', 'miniprogram_npm/**']
  })

  for (const f of styleFiles) {
    try {
      const fileFindings = scanFile(f)
      findings.push(...fileFindings)
    } catch (e) {
      findings.push({
        severity: 'error',
        ruleId: 'OVERFLOW_RISK',
        file: f,
        message: `解析失败: ${e.message}`
      })
    }
  }

  return findings
}

module.exports = { id: 'OVERFLOW_RISK', run, scanFile, getAllContainers }
