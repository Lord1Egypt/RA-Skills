// validation/rules/i18n-coverage.js
// 扫描小程序项目的 i18n 覆盖度：
// 1. 检查 app.json 的 navigationBarTitleText / tabBar text 是否纯中文
// 2. 检查 project.config.json 的 projectname 是否为无意义默认值
// 3. 扫描 WXML 中的硬编码中文文案（title/label/placeholder/button 文字等）
// 4. 检查 JS 中的硬编码中文字符串（toast/modal/dialog 等用户可见文案）
const fs = require('fs')
const path = require('path')
const fg = require('fast-glob')

// 中文字符检测
const CN_CHAR_RE = /[\u4e00-\u9fa5]/

// 无意义的默认 projectname
const DEFAULT_PROJECT_NAMES = [
  'miniprogram',
  'miniprogram-starter',
  'miniprogram-demo',
  'my-miniprogram',
  'wechat-miniprogram',
  'weixin',
]

// 无意义的默认 navigationBarTitleText
const DEFAULT_NAV_TITLES = [
  'weixin',
  'wechat',
  '微信',
]

function checkProjectConfig(root) {
  const findings = []
  const configPath = path.join(root, 'project.config.json')
  if (!fs.existsSync(configPath)) return findings

  try {
    const config = JSON.parse(fs.readFileSync(configPath, 'utf8'))
    const name = (config.projectname || '').toLowerCase().trim()

    if (!name) {
      findings.push({
        severity: 'warn',
        ruleId: 'I18N_PROJECT_NAME',
        file: configPath,
        message: 'project.config.json 的 projectname 为空，建议设置为包含英文业务名称的值'
      })
    } else if (DEFAULT_PROJECT_NAMES.some((d) => name === d || name.startsWith(d + '-'))) {
      findings.push({
        severity: 'warn',
        ruleId: 'I18N_PROJECT_NAME',
        file: configPath,
        message: `projectname "${config.projectname}" 为脚手架默认名称，境外用户搜索时无法通过英文关键词找到此小程序。建议改为"品牌名-英文描述"格式`
      })
    }
  } catch (e) {
    // JSON 解析失败由其他规则处理
  }

  return findings
}

function checkAppJson(root) {
  const findings = []
  const appJsonPath = path.join(root, 'app.json')
  if (!fs.existsSync(appJsonPath)) return findings

  try {
    const appJson = JSON.parse(fs.readFileSync(appJsonPath, 'utf8'))

    // 检查全局 navigationBarTitleText
    const navTitle = (appJson.window && appJson.window.navigationBarTitleText) || ''
    if (navTitle) {
      const lower = navTitle.toLowerCase().trim()
      if (DEFAULT_NAV_TITLES.includes(lower)) {
        findings.push({
          severity: 'warn',
          ruleId: 'I18N_NAV_TITLE',
          file: appJsonPath,
          message: `window.navigationBarTitleText "${navTitle}" 为平台默认值，建议设置为有意义的业务名称并支持多语言`
        })
      } else if (CN_CHAR_RE.test(navTitle) && !/[A-Za-z]/.test(navTitle)) {
        findings.push({
          severity: 'info',
          ruleId: 'I18N_NAV_TITLE',
          file: appJsonPath,
          message: `window.navigationBarTitleText "${navTitle}" 为纯中文，建议通过 i18n 在运行时动态设置（wx.setNavigationBarTitle）`
        })
      }
    }

    // 检查 tabBar 文本
    if (appJson.tabBar && Array.isArray(appJson.tabBar.list)) {
      for (const item of appJson.tabBar.list) {
        if (item.text && CN_CHAR_RE.test(item.text) && !/[A-Za-z]/.test(item.text)) {
          findings.push({
            severity: 'warn',
            ruleId: 'I18N_TABBAR_TEXT',
            file: appJsonPath,
            message: `tabBar 项 "${item.text}" (${item.pagePath}) 为纯中文，境外用户无法理解导航含义。建议通过 custom-tab-bar + i18n 动态设置`
          })
        }
      }
    }
  } catch (e) {
    // JSON 解析失败由其他规则处理
  }

  return findings
}

// 从 WXML 行中提取最近的 class 属性值
function extractClassFromLine(line) {
  const classMatch = line.match(/class="([^"]*)"/)
  return classMatch ? classMatch[1].trim() : ''
}

// 从 WXML 行中提取标签名
function extractTagFromLine(line) {
  const tagMatch = line.match(/<([a-zA-Z][\w-]*)[\s>\/]/)
  return tagMatch ? tagMatch[1] : ''
}

// 向上搜索最近的包含 class 的父元素（在同一文件 lines 数组中）
function findNearestClass(lines, lineIndex) {
  // 先检查当前行
  const currentClass = extractClassFromLine(lines[lineIndex])
  if (currentClass) return currentClass

  // 向上搜索最近的 class（最多 20 行）
  for (let j = lineIndex - 1; j >= Math.max(0, lineIndex - 20); j--) {
    const cls = extractClassFromLine(lines[j])
    if (cls) return cls
  }
  return ''
}

function scanWxmlHardcodedChinese(root) {
  const findings = []
  const wxmlFiles = fg.sync(['**/*.wxml'], {
    cwd: root,
    absolute: true,
    ignore: ['node_modules/**', 'miniprogram_npm/**']
  })

  for (const filePath of wxmlFiles) {
    const content = fs.readFileSync(filePath, 'utf8')
    const lines = content.split('\n')

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i]
      // 跳过 WXML 注释行
      if (line.includes('<!--')) continue

      // 检测常见属性中的中文
      const attrPatterns = [
        { re: /title="([^"]*[\u4e00-\u9fa5]+[^"]*)"/g, attr: 'title' },
        { re: /label="([^"]*[\u4e00-\u9fa5]+[^"]*)"/g, attr: 'label' },
        { re: /placeholder="([^"]*[\u4e00-\u9fa5]+[^"]*)"/g, attr: 'placeholder' },
        { re: /content="([^"]*[\u4e00-\u9fa5]+[^"]*)"/g, attr: 'content' },
        { re: /confirm-btn="([^"]*[\u4e00-\u9fa5]+[^"]*)"/g, attr: 'confirm-btn' },
        { re: /cancel-btn="([^"]*[\u4e00-\u9fa5]+[^"]*)"/g, attr: 'cancel-btn' },
        { re: /action="([^"]*[\u4e00-\u9fa5]+[^"]*)"/g, attr: 'action' },
      ]

      for (const { re, attr } of attrPatterns) {
        let m
        while ((m = re.exec(line)) !== null) {
          // 跳过 {{}} 数据绑定表达式
          if (/^\{\{.*\}\}$/.test(m[1].trim())) continue
          const elementClass = findNearestClass(lines, i)
          const tagName = extractTagFromLine(line)
          findings.push({
            severity: 'info',
            ruleId: 'I18N_HARDCODED_CN',
            file: filePath,
            line: i + 1,
            message: `${attr}="${m[1]}" 为硬编码中文，建议通过 i18n 的 t() 函数动态获取`,
            chineseText: m[1],
            elementClass,
            tagName,
            attrName: attr
          })
        }
      }

      // 检测标签内的纯中文文本（非 {{}} 绑定）
      const textContentRe = />([^<]*[\u4e00-\u9fa5]{2,}[^<]*)</g
      let tm
      while ((tm = textContentRe.exec(line)) !== null) {
        const text = tm[1].trim()
        // 跳过纯数据绑定
        if (/^\{\{.*\}\}$/.test(text)) continue
        // 跳过已被 {{}} 包裹的部分
        if (text.startsWith('{{') && text.endsWith('}}')) continue
        const elementClass = findNearestClass(lines, i)
        const tagName = extractTagFromLine(line)
        findings.push({
          severity: 'info',
          ruleId: 'I18N_HARDCODED_CN',
          file: filePath,
          line: i + 1,
          message: `标签内文本 "${text.slice(0, 40)}" 为硬编码中文`,
          chineseText: text,
          elementClass,
          tagName,
          attrName: '_textContent'
        })
      }
    }
  }

  return findings
}

function scanJsHardcodedChinese(root) {
  const findings = []
  const jsFiles = fg.sync(['**/*.js'], {
    cwd: root,
    absolute: true,
    ignore: ['node_modules/**', 'miniprogram_npm/**', 'locales/**', 'mock/**']
  })

  for (const filePath of jsFiles) {
    const content = fs.readFileSync(filePath, 'utf8')
    const lines = content.split('\n')

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i]
      // 跳过注释
      if (line.trim().startsWith('//') || line.trim().startsWith('*')) continue

      // 检测 title/content/label 等字段值中的中文字符串
      const cnStringInCode = /(title|content|label|message|text|placeholder|desc)\s*[:=]\s*['"]([^'"]*[\u4e00-\u9fa5]{2,}[^'"]*)['"]/g
      let m
      while ((m = cnStringInCode.exec(line)) !== null) {
        findings.push({
          severity: 'info',
          ruleId: 'I18N_HARDCODED_CN_JS',
          file: filePath,
          line: i + 1,
          message: `JS 中硬编码中文: "${m[2].slice(0, 40)}"，建议使用 i18n.t() 替代`,
          chineseText: m[2],
          fieldName: m[1]
        })
      }
    }
  }

  return findings
}

function run(ctx) {
  const root = ctx.projectRoot
  if (!root || !fs.existsSync(root)) return []

  const findings = [
    ...checkProjectConfig(root),
    ...checkAppJson(root),
    ...scanWxmlHardcodedChinese(root),
    ...scanJsHardcodedChinese(root),
  ]

  return findings
}

module.exports = { id: 'I18N_COVERAGE', run }
