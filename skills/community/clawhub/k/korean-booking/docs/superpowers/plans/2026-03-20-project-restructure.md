# Project Restructure Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Restructure the booking-skill project from a flat `lib/` layout into a scalable architecture that supports 900 hospitals, multi-language output, and batch MD generation.

**Architecture:** `core/resolver.js` handles all hospital matching and keyword logic; `core/renderer.js` owns template loading + i18n injection + output rendering; `core/service.js` exposes a single public function. The template (`booking.tpl`) is structure-only with channel-key placeholders, while `i18n/*.json` files hold the full translated channel text (which themselves embed `{name}` / `{search_keywords}` data placeholders substituted at render time).

**Tech Stack:** Node.js, Jest (already installed), pinyin-pro

---

## File Responsibility Map

| File | Responsibility |
|------|----------------|
| `data/hospitals.json` | Sole data source — move from root |
| `core/resolver.js` | Match hospital from query (4-tier); generate search keywords |
| `core/renderer.js` | Load tpl + i18n, substitute data vars, produce final string |
| `core/service.js` | Public entry: `getBookingGuide(query, lang?)` |
| `templates/booking.tpl` | Structure only — `{channel_ios}`, `{channel_android}`, etc. |
| `i18n/zh.json` | Chinese channel blocks (contain `{name}`, `{search_keywords}`) |
| `i18n/en.json` | English stubs (same keys, English text) |
| `i18n/ja.json` | Japanese stubs |
| `i18n/th.json` | Thai stubs |
| `scripts/generate-md.js` | CLI: iterate hospitals → write `docs/clinics/{slug}.md` |
| `api/skill.js` | Thin skill entry: `async input => getBookingGuide(input.query, input.lang)` |
| `tests/resolver.test.js` | Unit tests for resolver |
| `tests/renderer.test.js` | Unit tests for renderer |
| `tests/service.test.js` | Integration test for full pipeline |

**Files to delete after migration:**
- `lib/matcher.js`, `lib/keywords.js`, `lib/template.js`, `lib/renderer.js`
- `templates/zh_cn.txt`
- `index.js` (replaced by `api/skill.js` + `core/service.js`)

---

## Task 1: Create directory scaffold and move data

**Files:**
- Create: `data/hospitals.json` (move from root)
- Create: `core/`, `i18n/`, `scripts/`, `api/`, `tests/` directories
- Modify: `package.json` — update `main`

- [ ] **Step 1: Create directories**

```bash
mkdir -p data core i18n scripts api tests docs/clinics
```

- [ ] **Step 2: Move hospitals.json**

> ⚠️ Note: the root `hospitals.json` is intentionally **copied** (not moved) here. It is deleted in Task 8 once all new code is verified. Do not reference the root copy in any new code — always use `data/hospitals.json`.

```bash
# Guard: verify source file exists before copying
test -f hospitals.json || (echo "ERROR: hospitals.json not found at project root" && exit 1)
cp hospitals.json data/hospitals.json
```

- [ ] **Step 3: Update package.json main entry**

Edit `package.json`:
```json
{
  "name": "booking-skill",
  "version": "2.0.0",
  "main": "api/skill.js",
  "scripts": {
    "test": "jest",
    "generate": "node scripts/generate-md.js"
  },
  "dependencies": {
    "pinyin-pro": "^3.26.0"
  },
  "devDependencies": {
    "jest": "^29.0.0"
  }
}
```

- [ ] **Step 4: Verify data file is in place**

```bash
node -e "const h = require('./data/hospitals.json'); console.log(h.length, 'hospitals')"
```
Expected: `2 hospitals`

- [ ] **Step 5: Commit**

```bash
git add data/hospitals.json package.json
git commit -m "chore: scaffold new directory structure, move data source"
```

---

## Task 2: Create core/resolver.js (merge matcher + keywords)

**Files:**
- Create: `core/resolver.js`
- Create: `tests/resolver.test.js`

- [ ] **Step 1: Write failing tests**

Create `tests/resolver.test.js`:
```js
const { matchHospital, generateSearchKeywords } = require('../core/resolver')

const hospitals = [
  {
    id: 1,
    name: '韩国JD皮肤科',
    en_name: 'JD Skin Clinic',
    alias: 'JD皮肤科',
    aliases: ['jd皮肤科', '韩国jd', 'jd'],
    pinyin: 'JDpifuke',
    pinyin_abbr: 'JDpfk'
  },
  {
    id: 2,
    name: 'CNP皮肤科狎鸥亭店',
    en_name: 'CNP Skin Clinic',
    alias: 'CNP狎鸥亭',
    aliases: ['cnp', 'cnp皮肤科'],
    pinyin: 'CNPxiaouting',
    pinyin_abbr: 'CNPxot'
  }
]

describe('matchHospital', () => {
  // Strategy 1: exact match on name
  test('exact name match', () => {
    expect(matchHospital('韩国JD皮肤科', hospitals)).toEqual(hospitals[0])
  })

  // Strategy 1: exact match on en_name (case-insensitive)
  test('exact en_name match case-insensitive', () => {
    expect(matchHospital('jd skin clinic', hospitals)).toEqual(hospitals[0])
  })

  // Strategy 1: exact match on alias
  test('exact alias match', () => {
    expect(matchHospital('CNP狎鸥亭', hospitals)).toEqual(hospitals[1])
  })

  // Strategy 2: pinyin_abbr match
  test('pinyin_abbr match', () => {
    expect(matchHospital('JDpfk', hospitals)).toEqual(hospitals[0])
  })

  // Strategy 3: fuzzy name contains
  test('fuzzy name match', () => {
    expect(matchHospital('JD皮肤', hospitals)).toEqual(hospitals[0])
  })

  // Strategy 4: aliases array includes query (exact alias match)
  test('aliases array match', () => {
    expect(matchHospital('cnp皮肤科', hospitals)).toEqual(hospitals[1])
  })

  // Strategy 4: query contains alias item (q.includes(al) direction)
  test('query contains alias', () => {
    expect(matchHospital('cnp皮肤科怎么预约', hospitals)).toEqual(hospitals[1])
  })

  // Strategy 4: alias contains query (al.includes(q) direction — fixes the old one-direction bug)
  // Uses a fixture where the alias is longer than the query so only al.includes(q) triggers
  test('alias contains query', () => {
    const extended = [
      { ...hospitals[0] },
      { ...hospitals[1], aliases: ['cnp皮肤科诊所'] }  // alias is longer than query 'cnp皮肤科'
    ]
    expect(matchHospital('cnp皮肤科', extended)).toEqual(extended[1])
  })

  test('returns null for no match', () => {
    expect(matchHospital('不存在医院', hospitals)).toBeNull()
  })
})

describe('generateSearchKeywords', () => {
  test('generates keywords for hospital with full data', () => {
    const result = generateSearchKeywords(hospitals[0])
    expect(result).toContain('中文名')
    expect(result).toContain('英文名')
    expect(typeof result).toBe('string')
  })

  test('deduplicates identical values', () => {
    // name and en_name are the same value — only one label-value pair should appear
    const hospital = { name: 'JD', en_name: 'JD', aliases: [] }
    const result = generateSearchKeywords(hospital)
    // Count label-value pairs separated by 、 (more reliable than counting raw string occurrences)
    expect(result.split('、').length).toBe(1)
  })
})
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
npx jest tests/resolver.test.js --no-coverage
```
Expected: FAIL — `Cannot find module '../core/resolver'`

- [ ] **Step 3: Implement core/resolver.js**

Create `core/resolver.js`:
```js
const { pinyin } = require('pinyin-pro')

// ── Keyword generation ────────────────────────────────────────────────────────

const STOP_WORDS = [
  '整形外科&皮肤科', '&皮肤科', '抗老化医学美容中心',
  '皮肤科医院', '皮肤医院', '整形医院', '整形外科',
  '韩国', '牙科', '皮肤科', '眼科', '妇科',
  '总店', '国际店', '分店', '分馆', '诊所', '本院', '医院', '国际', '店'
]

const PINYIN_STOP = ['pifuke', 'pfk']

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

function generateSearchKeywords(hospital) {
  const cnName = filterName(hospital.name || '')
  const enName = (hospital.en_name || '')
    .replace(/\bclinic\b/gi, '')
    .replace(/\bhospital\b/gi, '')
    .trim()

  const py = cnName
    ? filterPinyin(pinyin(cnName, { toneType: 'none', separator: '', type: 'string' }))
    : ''
  const abbr = cnName
    ? filterPinyin(pinyin(cnName, { toneType: 'none', separator: '', type: 'string', pattern: 'first' }))
    : ''

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

// ── Hospital matching ─────────────────────────────────────────────────────────

function matchHospital(query, hospitals) {
  const q = query.toLowerCase()

  // Strategy 1: exact match on name / en_name / alias
  let found = hospitals.find(h =>
    [h.name, h.en_name, h.alias].some(v => v && v.toLowerCase() === q)
  )
  if (found) return found

  // Strategy 2: exact pinyin / pinyin_abbr
  found = hospitals.find(h =>
    [h.pinyin, h.pinyin_abbr].some(v => v && v.toLowerCase() === q)
  )
  if (found) return found

  // Strategy 3: fuzzy name contains query
  found = hospitals.find(h => h.name && h.name.toLowerCase().includes(q))
  if (found) return found

  // Strategy 4: other field fuzzy + aliases (query contains alias OR alias contains query)
  found = hospitals.find(h => {
    const fields = [h.en_name, h.alias, h.pinyin, h.pinyin_abbr]
    if (fields.some(v => v && v.toLowerCase().includes(q))) return true
    if (h.aliases && h.aliases.some(a => {
      const al = a.toLowerCase()
      return q.includes(al) || al.includes(q)
    })) return true
    return false
  })

  return found || null
}

module.exports = { matchHospital, generateSearchKeywords }
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
npx jest tests/resolver.test.js --no-coverage
```
Expected: PASS — all 8 tests green

- [ ] **Step 5: Commit**

```bash
git add core/resolver.js tests/resolver.test.js
git commit -m "feat: add core/resolver.js with hospital matching and keyword generation"
```

---

## Task 3: Create i18n files and booking.tpl

**Files:**
- Create: `templates/booking.tpl`
- Create: `i18n/zh.json`
- Create: `i18n/en.json`
- Create: `i18n/ja.json`
- Create: `i18n/th.json`

The i18n values contain `{name}` and `{search_keywords}` — these are data placeholders filled by the renderer.

- [ ] **Step 1: Create templates/booking.tpl**

```
{title}

{channel_ios}

{channel_android}

{channel_wechat_mini}

{channel_wechat_oa}

{channel_web}

{tips}
```

- [ ] **Step 2: Create i18n/zh.json** (extracted from existing `templates/zh_cn.txt`)

```json
{
  "title": "支持中/繁/英/泰/日等多语言",
  "channel_ios": "一、🍎 苹果手机预约（iOS 用户首选）\n打开 App Store 搜索「BeautsGO」或「彼此美」，下载并安装 BeautsGO APP 📥。\n打开 APP，在顶部搜索栏输入 {search_keywords} 均可快速找到{name}。\n进入医院页面，查看中韩文地址 📍、营业时间 ⏰、当月价格表 💰 及优惠活动。\n点击右下角【立即预约】或【咨询一下】，填写人数与时间，即可提交预约 ✅。",
  "channel_android": "二、🤖 Android 手机预约（安卓用户）\n打开 Google Play 搜索「BeautsGO」或「彼此美」，下载安装 APP 📲。\n打开 APP，在顶部搜索栏输入 {search_keywords} 均可快速找到{name}。\n进入医院页面，查看详细信息：地址、营业时间、当月价格、优惠活动等。\n点击【立即预约】或【咨询一下】，填写预约信息后提交 ✅。",
  "channel_wechat_mini": "三、📱 微信小程序预约（无需下载 APP）\n打开微信，搜索「BeautsGO」或「彼此美」小程序。\n进入小程序，在搜索栏输入 {search_keywords} 搜索{name}。\n查看医院详情：地址、营业时间、价格表、优惠活动。\n点击【立即预约】或【咨询一下】提交预约 ✅。",
  "channel_wechat_oa": "四、🟢 微信公众号预约（国内用户推荐）\n微信搜索【BeautsGO】或【彼此美】，关注公众号「BeautsGO彼此美APP」💬。\n点击左下角菜单【一键预约】，输入 {search_keywords} 进入流程 ⚡。\n💡 备选：直接在微信搜索框搜索微信号 BeautsGOkr 添加好友咨询。",
  "channel_web": "五、🌐 网页版预约（电脑端推荐）\n打开浏览器访问 BeautsGO 官网：https://www.beautsgo.com\n在首页搜索框输入 {search_keywords} 找到{name}。\n查看医院完整信息，包括环境照片、医生团队、价格表等。\n点击【预约】按钮，填写信息提交 ✅。",
  "tips": "📌 温馨提示：\n所有渠道均支持中文、繁体中文、英文、泰文、日文等多语言切换\n预约成功后会收到短信/APP 通知，请保持手机畅通\n如需修改预约，请在"我的预约"中操作或联系客服\n客服咨询时间：9:00-18:00（北京时间）"
}
```

- [ ] **Step 3: Create i18n/en.json** (English stubs — same structure, English text)

```json
{
  "title": "Available in Chinese, English, Japanese, Thai and more",
  "channel_ios": "1. 🍎 iOS Booking\nSearch \"BeautsGO\" on the App Store, download and install the app 📥.\nIn the search bar, type {search_keywords} to find {name}.\nView address 📍, hours ⏰, price list 💰 and promotions.\nTap [Book Now] or [Consult], fill in your details and submit ✅.",
  "channel_android": "2. 🤖 Android Booking\nSearch \"BeautsGO\" on Google Play, download and install the app 📲.\nIn the search bar, type {search_keywords} to find {name}.\nView clinic details: address, hours, prices and promotions.\nTap [Book Now] or [Consult], fill in your details and submit ✅.",
  "channel_wechat_mini": "3. 📱 WeChat Mini-Program (no app download needed)\nOpen WeChat, search for the \"BeautsGO\" mini-program.\nType {search_keywords} in the search bar to find {name}.\nView clinic details: address, hours, price list and promotions.\nTap [Book Now] or [Consult] to submit ✅.",
  "channel_wechat_oa": "4. 🟢 WeChat Official Account\nSearch [BeautsGO] in WeChat and follow the official account 💬.\nTap [Book Now] in the menu and enter {search_keywords} ⚡.\n💡 Alternative: search WeChat ID BeautsGOkr to add our service account.",
  "channel_web": "5. 🌐 Web Booking (desktop)\nVisit the BeautsGO website: https://www.beautsgo.com\nEnter {search_keywords} in the search bar to find {name}.\nView full clinic info including photos, doctors and prices.\nClick [Book] and submit your details ✅.",
  "tips": "📌 Tips:\nAll channels support Chinese, English, Japanese, Thai and more\nYou will receive an SMS/app notification after booking — keep your phone on\nTo modify a booking, go to \"My Bookings\" or contact support\nSupport hours: 9:00–18:00 (UTC+8)"
}
```

- [ ] **Step 4: Create i18n/ja.json and i18n/th.json stubs**

`i18n/ja.json` — copy same keys from `en.json`, mark values as `"[JA TODO]"` for each key so the structure is valid and translatable:
```json
{
  "title": "[JA TODO]",
  "channel_ios": "[JA TODO] {search_keywords} {name}",
  "channel_android": "[JA TODO] {search_keywords} {name}",
  "channel_wechat_mini": "[JA TODO] {search_keywords} {name}",
  "channel_wechat_oa": "[JA TODO] {search_keywords}",
  "channel_web": "[JA TODO] {search_keywords} {name}",
  "tips": "[JA TODO]"
}
```

`i18n/th.json` — same structure, `"[TH TODO]"` values.

- [ ] **Step 5: Verify JSON files are valid**

```bash
node -e "['zh','en','ja','th'].forEach(l => { require('./i18n/' + l + '.json'); console.log(l, 'ok') })"
```
Expected: `zh ok`, `en ok`, `ja ok`, `th ok`

- [ ] **Step 6: Commit**

```bash
git add templates/booking.tpl i18n/
git commit -m "feat: add booking.tpl structure and i18n files (zh/en/ja/th)"
```

---

## Task 4: Create core/renderer.js

**Files:**
- Create: `core/renderer.js`
- Create: `tests/renderer.test.js`

Render pipeline:
1. Load `templates/booking.tpl`
2. Load `i18n/{lang}.json`
3. Substitute `{name}` / `{search_keywords}` inside each i18n string
4. Replace `{channel_*}` / `{title}` / `{tips}` in template with processed i18n strings
5. Clean up empty placeholders

- [ ] **Step 1: Write failing tests**

Create `tests/renderer.test.js`:
```js
const { render } = require('../core/renderer')

const hospital = {
  id: 1,
  name: '韩国JD皮肤科',
  en_name: 'JD Skin Clinic',
  alias: 'JD皮肤科',
  aliases: ['jd皮肤科'],
  pinyin: 'JDpifuke',
  pinyin_abbr: 'JDpfk',
  search_keywords: '中文名"JD"、英文名"JD Skin"'
}

describe('render', () => {
  test('returns a non-empty string for zh', () => {
    const result = render(hospital, 'zh')
    expect(typeof result).toBe('string')
    expect(result.length).toBeGreaterThan(100)
  })

  test('zh output contains hospital name', () => {
    const result = render(hospital, 'zh')
    expect(result).toContain('韩国JD皮肤科')
  })

  test('zh output contains all 5 channel headers', () => {
    const result = render(hospital, 'zh')
    expect(result).toContain('App Store')
    expect(result).toContain('Google Play')
    expect(result).toContain('微信小程序')
    expect(result).toContain('微信公众号')
    expect(result).toContain('网页版')
  })

  test('en output contains hospital name', () => {
    const result = render(hospital, 'en')
    expect(result).toContain('韩国JD皮肤科')
  })

  // Checks that all structural template keys ({channel_ios}, etc.) were resolved.
  // Note: this regex only catches keys present in i18n/zh.json. If a future .tpl key
  // has no i18n entry, it will survive as a literal — add it to i18n to fix.
  test('no unresolved structural placeholders in output', () => {
    const result = render(hospital, 'zh')
    expect(result).not.toMatch(/\{channel_[a-z_]+\}/)
    expect(result).not.toMatch(/\{title\}/)
    expect(result).not.toMatch(/\{tips\}/)
  })

  test('no unresolved data placeholders in output', () => {
    const result = render(hospital, 'zh')
    expect(result).not.toMatch(/\{name\}/)
    expect(result).not.toMatch(/\{search_keywords\}/)
  })

  test('throws for unknown language', () => {
    expect(() => render(hospital, 'xx')).toThrow()
  })
})
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
npx jest tests/renderer.test.js --no-coverage
```
Expected: FAIL — `Cannot find module '../core/renderer'`

- [ ] **Step 3: Implement core/renderer.js**

Create `core/renderer.js`:
```js
const fs = require('fs')
const path = require('path')

function loadTemplate() {
  const tplPath = path.join(__dirname, '..', 'templates', 'booking.tpl')
  return fs.readFileSync(tplPath, 'utf-8')
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

function cleanUp(content) {
  // Strip empty quoted values (hospital missing en_name / pinyin produces 英文名"")
  content = content.replace(/""/g, '').replace(/''/g, '')

  // Strip dangling keyword labels when their value was empty (ported from old renderer)
  const labels = ['中文名', '英文名', '拼音', '首字母']
  for (const label of labels) {
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

  // Step 1: substitute data placeholders inside each i18n string
  const resolvedI18n = Object.fromEntries(
    Object.entries(i18n).map(([k, v]) => [k, substituteData(v, hospital)])
  )

  // Step 2: fill template structural placeholders with resolved i18n strings
  const filled = substituteData(template, resolvedI18n)

  return cleanUp(filled)
}

module.exports = { render }
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
npx jest tests/renderer.test.js --no-coverage
```
Expected: PASS — all 6 tests green

- [ ] **Step 5: Commit**

```bash
git add core/renderer.js tests/renderer.test.js
git commit -m "feat: add core/renderer.js with i18n-aware template rendering"
```

---

## Task 5: Create core/service.js

**Files:**
- Create: `core/service.js`
- Create: `tests/service.test.js`

- [ ] **Step 1: Write failing tests**

Create `tests/service.test.js`:
```js
const { getBookingGuide } = require('../core/service')

describe('getBookingGuide', () => {
  test('returns guide for known hospital query', async () => {
    const result = await getBookingGuide('CNP皮肤科怎么预约')
    expect(typeof result).toBe('string')
    expect(result).toContain('CNP')
    expect(result).toContain('App Store')
  })

  test('returns guide in english', async () => {
    const result = await getBookingGuide('CNP', 'en')
    expect(result).toContain('App Store')
  })

  test('returns prompt string when hospital not found', async () => {
    const result = await getBookingGuide('不存在的诊所abc')
    expect(typeof result).toBe('string')
    expect(result.length).toBeGreaterThan(0)
  })

  test('defaults to zh language', async () => {
    // Chinese-only text confirms zh is the default, not en
    const result = await getBookingGuide('CNP')
    expect(result).toContain('苹果手机')
  })
})
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
npx jest tests/service.test.js --no-coverage
```
Expected: FAIL — `Cannot find module '../core/service'`

- [ ] **Step 3: Implement core/service.js**

Create `core/service.js`:
```js
const hospitals = require('../data/hospitals.json')
const { matchHospital, generateSearchKeywords } = require('./resolver')
const { render } = require('./renderer')

async function getBookingGuide(query, lang = 'zh') {
  const hospital = matchHospital(query, hospitals)
  if (!hospital) {
    return '请告诉我医院名称，我帮你生成预约流程'
  }

  const enriched = {
    ...hospital,
    search_keywords: generateSearchKeywords(hospital)
  }

  return render(enriched, lang)
}

module.exports = { getBookingGuide }
```

- [ ] **Step 4: Run full test suite**

```bash
npx jest --no-coverage
```
Expected: PASS — all tests across resolver, renderer, service

- [ ] **Step 5: Commit**

```bash
git add core/service.js tests/service.test.js
git commit -m "feat: add core/service.js — unified public API"
```

---

## Task 6: Create api/skill.js

**Files:**
- Create: `api/skill.js`

No unit test needed — it's a one-liner wrapper already covered by service tests.

- [ ] **Step 1: Create api/skill.js**

```js
const { getBookingGuide } = require('../core/service')

module.exports = async function (input) {
  return getBookingGuide(input.query, input.lang || 'zh')
}
```

- [ ] **Step 2: Smoke test via node**

```bash
node -e "require('./api/skill.js')({ query: 'JD皮肤科怎么预约' }).then(console.log)"
```
Expected: Full booking guide text for JD Skin Clinic

- [ ] **Step 3: Commit**

```bash
git add api/skill.js
git commit -m "feat: add api/skill.js entry point"
```

---

## Task 7: Create scripts/generate-md.js

**Files:**
- Create: `scripts/generate-md.js`

Iterates all hospitals, calls `getBookingGuide`, writes `docs/clinics/{slug}.md`.

Slug formula: `hospital.id` zero-padded to 4 digits + `-` + `en_name` lowercased, spaces→hyphens, non-alphanumeric stripped. Example: `0001-jd-skin-clinic.md`.

- [ ] **Step 1: Create scripts/generate-md.js**

```js
const fs = require('fs')
const path = require('path')
const hospitals = require('../data/hospitals.json')
const { getBookingGuide } = require('../core/service')

const OUT_DIR = path.join(__dirname, '..', 'docs', 'clinics')

function toSlug(hospital) {
  const id = String(hospital.id).padStart(4, '0')
  const name = (hospital.en_name || hospital.name || String(hospital.id))
    .toLowerCase()
    .replace(/\s+/g, '-')
    .replace(/[^a-z0-9-]/g, '')
  return `${id}-${name}`
}

async function main() {
  fs.mkdirSync(OUT_DIR, { recursive: true })

  let ok = 0
  let fail = 0

  for (const hospital of hospitals) {
    const slug = toSlug(hospital)
    const outPath = path.join(OUT_DIR, `${slug}.md`)
    try {
      const content = await getBookingGuide(hospital.name)
      fs.writeFileSync(outPath, `# ${hospital.name}\n\n${content}\n`, 'utf-8')
      console.log(`✅ ${slug}.md`)
      ok++
    } catch (err) {
      console.error(`❌ ${slug}: ${err.message}`)
      fail++
    }
  }

  console.log(`\nDone: ${ok} generated, ${fail} failed`)
}

main()
```

- [ ] **Step 2: Run the script**

```bash
node scripts/generate-md.js
```
Expected:
```
✅ 0001-jd-skin-clinic.md
✅ 0002-cnp-skin-clinic.md

Done: 2 generated, 0 failed
```

- [ ] **Step 3: Verify output files exist**

```bash
ls docs/clinics/
```
Expected: `0001-jd-skin-clinic.md  0002-cnp-skin-clinic.md`

- [ ] **Step 4: Commit**

> Note: `docs/clinics/` output files are committed so they are available without running the script. With 900 hospitals this will grow large — if you prefer to gitignore generated files instead, add `docs/clinics/` to `.gitignore` and only commit `scripts/generate-md.js`. Either way, `mkdirSync` in the script ensures the directory is created at runtime.

```bash
git add scripts/generate-md.js docs/clinics/
git commit -m "feat: add generate-md script for bulk clinic doc generation"
```

---

## Task 8: Remove old files

- [ ] **Step 1: Delete old lib/ and root-level files no longer needed**

```bash
rm -rf lib/
rm templates/zh_cn.txt
rm index.js
rm hospitals.json   # now lives in data/
```

- [ ] **Step 2: Run full test suite to confirm nothing broke**

```bash
npx jest --no-coverage
```
Expected: PASS — all tests still green

- [ ] **Step 3: Commit**

```bash
git rm -rf lib/ templates/zh_cn.txt index.js hospitals.json
git commit -m "chore: remove old lib/, templates/zh_cn.txt, root index.js and hospitals.json"
```

---

## Task 9: Update skill.json and SKILL.md

**Files:**
- Modify: `skill.json`
- Modify: `SKILL.md`

- [ ] **Step 1: Update skill.json**

```json
{
  "name": "booking-skill",
  "description": "根据医院名称生成预约流程",
  "entry": "api/skill.js",
  "input": {
    "type": "object",
    "properties": {
      "query": { "type": "string", "description": "用户输入（含医院名称）" },
      "lang": { "type": "string", "description": "语言代码: zh | en | ja | th，默认 zh" }
    },
    "required": ["query"]
  }
}
```

- [ ] **Step 2: Update SKILL.md data section**

Change the data paths in `SKILL.md` to reflect new locations:
- `hospitals.json` → `data/hospitals.json`
- `templates/zh_cn.txt` → `templates/booking.tpl` + `i18n/*.json`

- [ ] **Step 3: Run final check**

```bash
npx jest --no-coverage && node -e "require('./api/skill.js')({ query: 'CNP怎么预约', lang: 'en' }).then(console.log)"
```
Expected: all tests pass + English booking guide printed

- [ ] **Step 4: Final commit**

```bash
git add skill.json SKILL.md
git commit -m "chore: update skill.json entry point and SKILL.md for new structure"
```

---

## Final Directory State

```
project/
├── api/
│   └── skill.js              # thin skill entry
├── core/
│   ├── resolver.js           # match hospital + generate keywords
│   ├── renderer.js           # load tpl + i18n + render
│   └── service.js            # getBookingGuide(query, lang)
├── data/
│   └── hospitals.json        # sole data source
├── docs/
│   └── clinics/              # generated MD files
├── i18n/
│   ├── zh.json
│   ├── en.json
│   ├── ja.json
│   └── th.json
├── scripts/
│   └── generate-md.js
├── templates/
│   └── booking.tpl
├── tests/
│   ├── resolver.test.js
│   ├── renderer.test.js
│   └── service.test.js
├── skill.json
├── SKILL.md
├── README.md
└── package.json
```
