#!/usr/bin/env node
/**
 * scripts/merge-address.js
 *
 * 将地址 CSV 合并进 data/hospitals.json（只追加地址字段，原有字段保留）
 *
 * CSV 列顺序（无表头）：
 *   id, zh_cn_address, en_address, ko_kr_address, ja_address, th_address
 *
 * 用法：
 *   node scripts/merge-address.js /path/to/无标题.csv
 */

const fs   = require('fs')
const path = require('path')

// ── CSV 解析（支持带引号字段） ─────────────────────────────────────────────────
function parseCSVLine(line) {
  const result = []
  let current = ''
  let inQuotes = false

  for (let i = 0; i < line.length; i++) {
    const ch = line[i]
    if (ch === '"') {
      if (inQuotes && line[i + 1] === '"') {
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

function main() {
  const csvPath = process.argv[2]
  if (!csvPath) {
    console.error('用法: node scripts/merge-address.js <csv文件路径>')
    process.exit(1)
  }

  const absPath = path.resolve(csvPath.replace(/^~/, process.env.HOME))
  if (!fs.existsSync(absPath)) {
    console.error(`文件不存在: ${absPath}`)
    process.exit(1)
  }

  // 读取现有 hospitals.json
  const jsonPath  = path.join(__dirname, '..', 'data', 'hospitals.json')
  const hospitals = JSON.parse(fs.readFileSync(jsonPath, 'utf-8'))

  // 建立 id → index 映射，方便快速定位
  const idMap = {}
  hospitals.forEach((h, i) => { idMap[h.id] = i })

  // 解析 CSV，按 id 合并地址字段
  const content = fs.readFileSync(absPath, 'utf-8')
  const lines   = content.split(/\r?\n/).filter(l => l.trim())

  let merged = 0
  let skipped = 0
  let notFound = 0

  for (const line of lines) {
    const cols = parseCSVLine(line)
    if (cols.length < 1) { skipped++; continue }

    const numId = parseInt(cols[0], 10)
    if (isNaN(numId)) { skipped++; continue }

    const idx = idMap[numId]
    if (idx === undefined) {
      // CSV 里有但 json 里没有（已下架等），跳过
      notFound++
      continue
    }

    // 只追加地址字段，原有字段保留
    if (cols[1] !== undefined) hospitals[idx].zh_cn_address = cols[1]
    if (cols[2] !== undefined) hospitals[idx].en_address     = cols[2]
    if (cols[3] !== undefined) hospitals[idx].ko_kr_address  = cols[3]
    if (cols[4] !== undefined) hospitals[idx].ja_address     = cols[4]
    if (cols[5] !== undefined) hospitals[idx].th_address     = cols[5]

    merged++
  }

  fs.writeFileSync(jsonPath, JSON.stringify(hospitals, null, 2), 'utf-8')

  console.log(`✅ 合并完成：${merged} 条地址已写入 hospitals.json`)
  if (notFound > 0) console.log(`⚠️  ${notFound} 条 id 在 hospitals.json 中不存在（已跳过）`)
  if (skipped  > 0) console.log(`⚠️  ${skipped} 行格式不合法（已跳过）`)
}

main()
