/**
 * JD皮肤科预约技能 — 渲染层
 * 将医院数据 + i18n 文案渲染为最终 Markdown 输出
 */

const fs = require('fs')
const path = require('path')

// 预约指南模板（同 beautsgo-booking）
const BOOKING_TEMPLATE = [
  '{title}',
  '',
  '{direct_link}',
  '',
  '{channel_ios}',
  '',
  '{channel_android}',
  '',
  '{channel_wechat_mini}',
  '',
  '{channel_wechat_oa}',
  '',
  '{channel_web}',
  '',
  '{tips}',
  ''
].join('\n')

const DEFAULT_KEYWORD_LABELS = ['中文名', '英文名', '拼音', '首字母']

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

function cleanUp(content, keywordLabels = DEFAULT_KEYWORD_LABELS) {
  content = content.replace(/""/g, '').replace(/''/g, '')
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
  const i18n = loadI18n(lang)

  // Pass 1: inject hospital data into each i18n string
  const resolvedI18n = Object.fromEntries(
    Object.entries(i18n).map(([k, v]) => [k, typeof v === 'string' ? substituteData(v, hospital) : v])
  )

  // Pass 2: fill template structural placeholders
  const filled = substituteData(BOOKING_TEMPLATE, resolvedI18n)

  const keywordLabels = Array.isArray(i18n.keyword_labels)
    ? i18n.keyword_labels
    : DEFAULT_KEYWORD_LABELS

  return cleanUp(filled, keywordLabels)
}

module.exports = { render, loadI18n }
