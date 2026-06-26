#!/usr/bin/env node
/**
 * scripts/import-hospitals.js
 *
 * 从数据库导出的 CSV 生成 data/hospitals.json
 *
 * CSV 列顺序（无表头）：
 *   id, name, alias, en_name, pinyin, pinyin_abbr
 *
 * 用法：
 *   node scripts/import-hospitals.js /path/to/export.csv
 *   node scripts/import-hospitals.js ~/Desktop/无标题.csv
 */

const fs   = require('fs')
const path = require('path')

// ── formatSlug (与前端 updateSemanticUrl 逻辑一致) ────────────────────────────
function formatSlug(enName) {
  if (!enName) return ''
  return enName
    .toLowerCase()
    .replace(/\s+/g, '-')
    .replace(/[^a-z0-9-]/g, '')
    .replace(/-+/g, '-')       // 合并连续连字符
    .replace(/^-|-$/g, '')     // 去掉首尾连字符
}

// ── CSV 解析（支持带引号字段） ─────────────────────────────────────────────────
function parseCSVLine(line) {
  const result = []
  let current = ''
  let inQuotes = false

  for (let i = 0; i < line.length; i++) {
    const ch = line[i]
    if (ch === '"') {
      if (inQuotes && line[i + 1] === '"') {
        // 转义的双引号
        current += '"'
        i++
      } else {
        inQuotes = !inQuotes
      }
    } else if (ch === ',' && !inQuotes) {
      result.push(current.trim())
      current = ''
    } else {
      current += ch
    }
  }
  result.push(current.trim())
  return result
}

// ── 主逻辑 ────────────────────────────────────────────────────────────────────
function main() {
  const csvPath = process.argv[2]
  if (!csvPath) {
    console.error('用法: node scripts/import-hospitals.js <csv文件路径>')
    process.exit(1)
  }

  const absPath = path.resolve(csvPath.replace(/^~/, process.env.HOME))
  if (!fs.existsSync(absPath)) {
    console.error(`文件不存在: ${absPath}`)
    process.exit(1)
  }

  const content = fs.readFileSync(absPath, 'utf-8')
  const lines   = content.split(/\r?\n/).filter(l => l.trim())

  const hospitals = []
  let skipped = 0

  for (const line of lines) {
    const cols = parseCSVLine(line)
    // 至少需要 id 和 name
    if (cols.length < 2) { skipped++; continue }

    const [id, name, alias, en_name, pinyin, pinyin_abbr] = cols

    // id 必须是数字
    const numId = parseInt(id, 10)
    if (isNaN(numId) || !name) { skipped++; continue }

    const cleanName    = name.trim()
    const cleanAlias   = alias ? alias.trim() : ''
    const cleanEnName  = en_name ? en_name.trim() : ''
    const cleanPinyin  = pinyin ? pinyin.trim() : ''
    const cleanAbbr    = pinyin_abbr ? pinyin_abbr.trim() : ''

    // 生成 slug 和 URL
    const slug = formatSlug(cleanEnName)
    const url         = slug ? `https://i.beautsgo.com/cn/hospital/${slug}?from=skill` : ''
    const booking_url = slug ? `https://i.beautsgo.com/cn/hospital/${slug}/skill` : ''

    const entry = {
      id: numId,
      name: cleanName,
      alias: cleanAlias || cleanName,  // alias 为空时降级为 name
      en_name: cleanEnName,
      pinyin: cleanPinyin,
      pinyin_abbr: cleanAbbr,
      url,
      booking_url
    }

    hospitals.push(entry)
  }

  // 按 id 排序
  hospitals.sort((a, b) => a.id - b.id)

  const outPath = path.join(__dirname, '..', 'data', 'hospitals.json')
  fs.writeFileSync(outPath, JSON.stringify(hospitals, null, 2), 'utf-8')

  console.log(`✅ 导入完成：${hospitals.length} 条医院数据 → ${outPath}`)
  if (skipped > 0) console.log(`⚠️  跳过 ${skipped} 行（格式不合法）`)
}

main()
