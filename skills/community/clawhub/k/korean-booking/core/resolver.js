const { pinyin } = require('pinyin-pro')

// ── Stop words for keyword filtering ─────────────────────────────────────────

const STOP_WORDS = [
  '整形外科&皮肤科', '&皮肤科', '抗老化医学美容中心',
  '皮肤科医院', '皮肤医院', '整形医院', '整形外科',
  '韩国', '牙科', '皮肤科', '眼科', '妇科',
  '总店', '国际店', '分店', '分馆', '诊所', '本院', '医院', '国际', '店'
]

const PINYIN_STOP = ['pifuke', 'pfk']

// Words that appear as sub-tokens in many pinyin_abbr values and must not drive a match alone
const ABBR_STOP = new Set(['pfk', 'pifuke', 'yy', 'yyuan', 'zx', 'zxwk'])

function filterName(name) {
  let result = name.replace(/[（(][^）)]*[）)]/g, '')
  const sorted = [...STOP_WORDS].sort((a, b) => b.length - a.length)
  sorted.forEach(w => { result = result.split(w).join('') })
  return result.trim()
}

function filterPinyin(str) {
  return PINYIN_STOP.reduce(
    (acc, kw) => acc.replace(new RegExp(kw, 'gi'), ''),
    str
  )
}

// ── Search keyword generation ─────────────────────────────────────────────────

function generateSearchKeywords(hospital) {
  const cnName = filterName(hospital.name || '')
  const enName = (hospital.en_name || '')
    .replace(/\bclinic\b/gi, '')
    .replace(/\bhospital\b/gi, '')
    .trim()

  // 优先使用数据库带来的 pinyin / pinyin_abbr 字段（原始值，不做 stop word 过滤）
  // 降级：实时用 pinyin-pro 计算（仅对纯中文字符，需过滤通用词）
  let py, abbr
  if (hospital.pinyin) {
    py   = hospital.pinyin.trim()
    abbr = hospital.pinyin_abbr ? hospital.pinyin_abbr.trim() : ''
  } else {
    const chineseForPinyin = cnName ? extractChineseOnly(cnName) : ''
    py = chineseForPinyin
      ? filterPinyin(pinyin(chineseForPinyin, { toneType: 'none', separator: '', type: 'string' }))
      : ''
    abbr = chineseForPinyin
      ? filterPinyin(pinyin(chineseForPinyin, { toneType: 'none', separator: '', type: 'string', pattern: 'first' }))
      : ''
  }

  const parts = [['中文名', cnName], ['英文名', enName], ['拼音', py], ['首字母', abbr]]
  const seen = new Set()
  const keywords = []

  for (const [label, value] of parts) {
    if (!value) continue
    const key = value.toLowerCase()
    if (seen.has(key)) continue
    seen.add(key)
    keywords.push(`${label}"${value}"`)
  }

  return keywords.join('、')
}

// ── Dynamic pinyin generation for matching ────────────────────────────────────

/**
 * Extract only the Chinese characters from a string for pinyin generation.
 * e.g. "CNP狎鸥亭" → "狎鸥亭", "JD皮肤科" → "皮肤科"
 */
function extractChineseOnly(str) {
  return str.replace(/[^\u4e00-\u9fff]/g, '')
}

function getDynamicPinyin(hospital) {
  const cnName = filterName(hospital.name || '')
  if (!cnName) return { py: '', abbr: '' }
  // Only run pinyin over Chinese characters to avoid mixing in Latin prefixes
  const chineseOnly = extractChineseOnly(cnName)
  if (!chineseOnly) return { py: '', abbr: '' }
  const py = filterPinyin(pinyin(chineseOnly, { toneType: 'none', separator: '', type: 'string' }))
  const abbr = filterPinyin(pinyin(chineseOnly, { toneType: 'none', separator: '', type: 'string', pattern: 'first' }))
  return { py, abbr }
}

// ── Hospital matching (4-tier strategy) ──────────────────────────────────────

// Minimum token length for bidirectional alias matching to avoid false positives
const MIN_ALIAS_MATCH_LEN = 2

function matchHospital(query, hospitals) {
  const q = query.toLowerCase()

  // Strategy 1: exact match on name / en_name / alias / aliases
  let found = hospitals.find(h => {
    if ([h.name, h.en_name, h.alias].some(v => v && v.toLowerCase() === q)) return true
    if (h.aliases && h.aliases.some(a => a && a.toLowerCase() === q)) return true
    return false
  })
  if (found) return found

  // Strategy 2: exact pinyin / pinyin_abbr (prefer DB field, fall back to dynamic)
  found = hospitals.find(h => {
    const dbPy   = h.pinyin   ? h.pinyin.trim().toLowerCase()   : ''
    const dbAbbr = h.pinyin_abbr ? h.pinyin_abbr.trim().toLowerCase() : ''
    if ((dbPy && dbPy === q) || (dbAbbr && dbAbbr === q)) return true
    const { py, abbr } = getDynamicPinyin(h)
    return (py && py.toLowerCase() === q) || (abbr && abbr.toLowerCase() === q)
  })
  if (found) return found

  // Strategy 3: fuzzy name contains query (require query length >= 2 to avoid single-char false positives)
  if (q.length >= MIN_ALIAS_MATCH_LEN) {
    found = hospitals.find(h => h.name && h.name.toLowerCase().includes(q))
    if (found) return found
  }

  // Strategy 3b: token split match — split query into [a-z0-9]+ and CJK chars, require all tokens
  // appear in the hospital name. Handles inputs like "cnp狎鸥亭" → ["cnp","狎","鸥","亭"]
  if (q.length >= MIN_ALIAS_MATCH_LEN) {
    const tokens = q.match(/[a-z0-9]+|[\u4e00-\u9fff]/g) || []
    if (tokens.length >= 2) {
      found = hospitals.find(h => {
        const nameLow = (h.name || '').toLowerCase()
        return tokens.every(t => nameLow.includes(t))
      })
      if (found) return found
    }
  }

  // Strategy 4: other fields fuzzy + aliases bidirectional
  if (q.length >= MIN_ALIAS_MATCH_LEN) {
    found = hospitals.find(h => {
      const { py, abbr } = getDynamicPinyin(h)
      const dbPy   = h.pinyin   ? h.pinyin.trim().toLowerCase()   : ''
      const dbAbbr = h.pinyin_abbr ? h.pinyin_abbr.trim().toLowerCase() : ''
      // en_name / alias: substring match
      const enName = h.en_name ? h.en_name.toLowerCase() : ''
      const alias  = h.alias   ? h.alias.toLowerCase()   : ''
      if (enName && enName.includes(q)) return true
      if (alias  && alias.includes(q))  return true
      // pinyin full: substring match
      if ((py && py.includes(q)) || (dbPy && dbPy.includes(q))) return true
      // pinyin_abbr: includes match, but skip if query is a generic stop token
      if (!ABBR_STOP.has(q)) {
        if ((abbr && abbr.includes(q)) || (dbAbbr && dbAbbr.includes(q))) return true
      }
      if (h.aliases && h.aliases.some(a => {
        const al = a.toLowerCase()
        if (al.length < MIN_ALIAS_MATCH_LEN || q.length < MIN_ALIAS_MATCH_LEN) return false
        return q.includes(al) || al.includes(q)
      })) return true
      return false
    })
  }

  return found || null
}

module.exports = { matchHospital, generateSearchKeywords }
