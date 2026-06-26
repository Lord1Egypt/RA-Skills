const fs = require('fs')
const path = require('path')

function loadTemplate() {
  return fs.readFileSync(path.join(__dirname, '..', 'templates', 'booking.tpl'), 'utf-8')
}

function loadI18n(lang) {
  const i18nPath = path.join(__dirname, '..', 'i18n', `${lang}.json`)
  if (!fs.existsSync(i18nPath)) {
    throw new Error(`Unsupported language: ${lang}. Add i18n/${lang}.json to enable it.`)
  }
  return JSON.parse(fs.readFileSync(i18nPath, 'utf-8'))
}

function substituteData(str, data) {
  return Object.entries(data).reduce((acc, [key, value]) => {
    if (Array.isArray(value)) return acc
    const v = (value == null || value === '-' || value === '- ') ? '' : String(value)
    return acc.split(`{${key}}`).join(v)
  }, str)
}

// Default keyword labels used in cleanUp — overridden by i18n.keyword_labels when present
const DEFAULT_KEYWORD_LABELS = ['中文名', '英文名', '拼音', '首字母']

function cleanUp(content, keywordLabels = DEFAULT_KEYWORD_LABELS) {
  // Strip empty quoted values
  content = content.replace(/""/g, '').replace(/''/g, '')

  // Strip dangling keyword labels when their value was empty
  for (const label of keywordLabels) {
    const esc = label.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
    content = content.replace(new RegExp(esc + '\\s*[,，、·]\\s*', 'gu'), '')
    content = content.replace(new RegExp('[,，、·]\\s*' + esc + '\\s*$', 'gmu'), '')
    content = content.replace(new RegExp(esc + '\\s*$', 'gmu'), '')
  }

  return content
    .replace(/或或者/g, '或').replace(/或者或/g, '或').replace(/或或/g, '或')
    .replace(/,+/g, ',')
    .replace(/,([。.!？\n])/g, '$1')
    .replace(/ +/g, ' ')
    .trim()
}

function render(hospital, lang = 'zh') {
  const template = loadTemplate()
  const i18n = loadI18n(lang)

  // Pass 1: inject hospital data into each i18n string (skip non-string values like keyword_labels)
  const resolvedI18n = Object.fromEntries(
    Object.entries(i18n).map(([k, v]) => [k, typeof v === 'string' ? substituteData(v, hospital) : v])
  )

  // Pass 2: fill template structural placeholders with resolved i18n strings
  const filled = substituteData(template, resolvedI18n)

  // Use keyword_labels from i18n if provided, otherwise fall back to default (Chinese)
  const keywordLabels = Array.isArray(i18n.keyword_labels)
    ? i18n.keyword_labels
    : DEFAULT_KEYWORD_LABELS

  return cleanUp(filled, keywordLabels)
}

module.exports = { render, loadI18n }
