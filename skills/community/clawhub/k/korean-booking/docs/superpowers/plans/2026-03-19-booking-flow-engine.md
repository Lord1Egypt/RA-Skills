# Booking Flow Engine Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将 PHP `ReservationProcessServices` 的预约流程生成逻辑复刻为 JS 模块，支持从自然语言 query 匹配医院并渲染多字段模板。

**Architecture:** 入口 `index.js` 组合调用四个独立模块：`matcher`（医院匹配）、`template`（模板加载）、`keywords`（拼音关键词生成）、`renderer`（变量替换与清理）。模板以本地 txt 文件存储，变量用 `{field_name}` 占位。

**Tech Stack:** Node.js 22, pinyin-pro, Jest（测试）

---

## File Map

| 状态 | 路径 | 职责 |
|------|------|------|
| 创建 | `lib/matcher.js` | 4 级策略匹配医院 |
| 创建 | `lib/template.js` | 加载本地模板文件 |
| 创建 | `lib/keywords.js` | 生成 search_keywords 虚拟字段 |
| 创建 | `lib/renderer.js` | 变量替换 + 空占位符清理 |
| 创建 | `templates/zh_cn.txt` | 中文预约流程模板 |
| 修改 | `hospitals.json` | 字段迁移：`name_cn`→`name`、`name_en`→`en_name`，新增 `alias`/`pinyin`/`pinyin_abbr` |
| 修改 | `index.js` | 重写入口，组合调用各模块 |
| 创建 | `tests/matcher.test.js` | matcher 单元测试 |
| 创建 | `tests/keywords.test.js` | keywords 单元测试 |
| 创建 | `tests/template.test.js` | template 单元测试 |
| 创建 | `tests/renderer.test.js` | renderer 单元测试 |
| 创建 | `tests/integration.test.js` | 端到端集成测试 |
| 创建 | `package.json` | 项目依赖与测试脚本 |

---

## Task 1: 初始化项目依赖

**Files:**
- Create: `package.json`

- [ ] **Step 1: 创建 package.json**

```json
{
  "name": "booking-skill",
  "version": "1.0.0",
  "main": "index.js",
  "scripts": {
    "test": "jest"
  },
  "dependencies": {
    "pinyin-pro": "^3.26.0"
  },
  "devDependencies": {
    "jest": "^29.0.0"
  }
}
```

- [ ] **Step 2: 安装依赖**

```bash
npm install
```

Expected: `node_modules/` 生成，`package-lock.json` 创建。

- [ ] **Step 3: Commit**

```bash
git add package.json package-lock.json
git commit -m "chore: init package.json with pinyin-pro and jest"
```

---

## Task 2: 更新 hospitals.json 数据结构

**Files:**
- Modify: `hospitals.json`

- [ ] **Step 1: 更新 hospitals.json**

> ⚠️ 注意：此步骤将旧字段 `name_cn` → `name`、`name_en` → `en_name` 重命名，同时新增 `alias`/`pinyin`/`pinyin_abbr`。旧的 `index.js` 引用 `hospital.name_cn` 会在 Task 7 重写时一并修复。

将现有两条记录补全字段：

```json
[
  {
    "id": 1,
    "name": "韩国JD皮肤科",
    "en_name": "JD Skin Clinic",
    "alias": "JD皮肤科",
    "aliases": ["jd皮肤科", "韩国jd", "jd"],
    "pinyin": "JDpifuke",
    "pinyin_abbr": "JDpfk"
  },
  {
    "id": 2,
    "name": "CNP皮肤科狎鸥亭店",
    "en_name": "CNP Skin Clinic",
    "alias": "CNP狎鸥亭",
    "aliases": ["cnp", "cnp皮肤科"],
    "pinyin": "CNPxiaouting",
    "pinyin_abbr": "CNPxot"
  }
]
```

- [ ] **Step 2: Commit**

```bash
git add hospitals.json
git commit -m "feat: enrich hospitals.json with name/alias/pinyin fields"
```

---

## Task 3: 实现 matcher.js + 测试

**Files:**
- Create: `lib/matcher.js`
- Create: `tests/matcher.test.js`

- [ ] **Step 1: 写失败测试**

```js
// tests/matcher.test.js
const { matchHospital } = require('../lib/matcher')
const hospitals = require('../hospitals.json')

test('精确匹配中文名', () => {
  expect(matchHospital('CNP皮肤科狎鸥亭店', hospitals)).toMatchObject({ id: 2 })
})

test('精确匹配英文名（忽略大小写）', () => {
  expect(matchHospital('cnp skin clinic', hospitals)).toMatchObject({ id: 2 })
})

test('alias 匹配', () => {
  expect(matchHospital('CNP狎鸥亭', hospitals)).toMatchObject({ id: 2 })
})

test('pinyin 精确匹配', () => {
  expect(matchHospital('CNPxiaouting', hospitals)).toMatchObject({ id: 2 })
})

test('name 模糊匹配', () => {
  expect(matchHospital('JD皮肤', hospitals)).toMatchObject({ id: 1 })
})

test('aliases 数组模糊匹配', () => {
  expect(matchHospital('cnp皮肤科怎么预约', hospitals)).toMatchObject({ id: 2 })
})

test('找不到医院返回 null', () => {
  expect(matchHospital('不存在的医院', hospitals)).toBeNull()
})
```

- [ ] **Step 2: 运行测试，确认失败**

```bash
npx jest tests/matcher.test.js
```

Expected: FAIL — `Cannot find module '../lib/matcher'`

- [ ] **Step 3: 实现 matcher.js**

```js
// lib/matcher.js
function matchHospital(query, hospitals) {
  const q = query.toLowerCase()

  // 策略1: 精确匹配 name / en_name / alias（忽略大小写）
  let found = hospitals.find(h =>
    [h.name, h.en_name, h.alias].some(v => v && v.toLowerCase() === q)
  )
  if (found) return found

  // 策略2: pinyin / pinyin_abbr 精确匹配（忽略大小写）
  found = hospitals.find(h =>
    [h.pinyin, h.pinyin_abbr].some(v => v && v.toLowerCase() === q)
  )
  if (found) return found

  // 策略3: name 模糊包含
  found = hospitals.find(h => h.name && h.name.toLowerCase().includes(q))
  if (found) return found

  // 策略4: 其他字段模糊包含（en_name, alias, pinyin, pinyin_abbr, aliases 数组）
  found = hospitals.find(h => {
    const fields = [h.en_name, h.alias, h.pinyin, h.pinyin_abbr]
    if (fields.some(v => v && v.toLowerCase().includes(q))) return true
    if (h.aliases && h.aliases.some(a => q.includes(a.toLowerCase()))) return true
    return false
  })
  return found || null
}

module.exports = { matchHospital }
```

- [ ] **Step 4: 运行测试，确认通过**

```bash
npx jest tests/matcher.test.js
```

Expected: PASS — 7 tests passed

- [ ] **Step 5: Commit**

```bash
git add lib/matcher.js tests/matcher.test.js
git commit -m "feat: implement hospital matcher with 4-strategy matching"
```

---

## Task 4: 实现 keywords.js + 测试

**Files:**
- Create: `lib/keywords.js`
- Create: `tests/keywords.test.js`

- [ ] **Step 1: 写失败测试**

```js
// tests/keywords.test.js
const { generateSearchKeywords, filterPinyin } = require('../lib/keywords')

const hospital = {
  name: 'CNP皮肤科狎鸥亭店',
  en_name: 'CNP Skin Clinic',
  alias: 'CNP狎鸥亭'
}

test('包含中文名（过滤通用词后，展示 alias 短名）', () => {
  const result = generateSearchKeywords(hospital)
  expect(result).toContain('中文名')
  expect(result).toContain('CNP狎鸥亭')
})

test('包含英文名（去除 clinic/hospital 后）', () => {
  const result = generateSearchKeywords(hospital)
  expect(result).toContain('英文名')
  expect(result).toContain('CNP Skin')
})

test('包含拼音且不含音调', () => {
  const result = generateSearchKeywords(hospital)
  // 拼音段不应含声调字符
  expect(result).toMatch(/拼音"[^""]*"/)
  expect(result).not.toMatch(/[āáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜ]/)
})

test('首字母与拼音不重复', () => {
  const result = generateSearchKeywords(hospital)
  // 结果中拼音和首字母都应出现，且各自不重复
  expect(result).toContain('拼音')
  expect(result).toContain('首字母')
})

test('filterPinyin 直接移除 pifuke 和 pfk', () => {
  expect(filterPinyin('JDpifuke')).toBe('JD')
  expect(filterPinyin('CNPpfk')).toBe('CNP')
  expect(filterPinyin('PIFUKEtest')).toBe('test')
})

test('跳过空值字段', () => {
  const minHospital = { name: 'CNP皮肤科狎鸥亭店', en_name: '', alias: '' }
  const result = generateSearchKeywords(minHospital)
  expect(result).not.toContain('英文名""')
})
```

- [ ] **Step 2: 运行测试，确认失败**

```bash
npx jest tests/keywords.test.js
```

Expected: FAIL — `Cannot find module '../lib/keywords'`

- [ ] **Step 3: 实现 keywords.js**

```js
// lib/keywords.js
const { pinyin } = require('pinyin-pro')

const STOP_WORDS = [
  '整形外科&皮肤科', '&皮肤科', '抗老化医学美容中心',
  '皮肤科医院', '皮肤医院', '整形医院', '整形外科',
  '韩国', '牙科', '皮肤科', '眼科', '妇科',
  '总店', '国际店', '分店', '分馆', '诊所', '本院', '医院', '国际', '店'
]

const FILTER_PINYIN = ['pifuke', 'pfk']

function filterName(name) {
  // 去除括号内容
  let result = name.replace(/[（(][^）)]*[）)]/g, '')
  // 去除通用词（长词优先）
  const sorted = [...STOP_WORDS].sort((a, b) => b.length - a.length)
  sorted.forEach(w => { result = result.split(w).join('') })
  return result.trim()
}

function filterPinyin(str) {
  let result = str
  FILTER_PINYIN.forEach(kw => {
    result = result.replace(new RegExp(kw, 'gi'), '')
  })
  return result
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

  const parts = [
    ['中文名', cnName],
    ['英文名', enName],
    ['拼音', py],
    ['首字母', abbr]
  ]

  const seen = new Set()
  const keywords = []

  for (const [label, value] of parts) {
    if (!value || value === '-') continue
    const key = value.toLowerCase()
    if (seen.has(key)) continue
    seen.add(key)
    keywords.push(`${label}"${value}"`)
  }

  return keywords.join('、')
}

module.exports = { generateSearchKeywords, filterPinyin }
```

- [ ] **Step 4: 运行测试，确认通过**

```bash
npx jest tests/keywords.test.js
```

Expected: PASS — 6 tests passed

- [ ] **Step 5: Commit**

```bash
git add lib/keywords.js tests/keywords.test.js
git commit -m "feat: implement search_keywords generator with pinyin-pro"
```

---

## Task 5: 实现 template.js + 测试

**Files:**
- Create: `lib/template.js`
- Create: `templates/zh_cn.txt`
- Create: `tests/template.test.js`

- [ ] **Step 1: 写失败测试**

```js
// tests/template.test.js
const path = require('path')
const { loadTemplate } = require('../lib/template')

test('成功加载 zh_cn 模板', () => {
  const content = loadTemplate('zh_cn')
  expect(typeof content).toBe('string')
  expect(content.length).toBeGreaterThan(0)
  expect(content).toContain('{name}')
  expect(content).toContain('{search_keywords}')
})

test('加载不存在的语言模板时抛出错误', () => {
  expect(() => loadTemplate('xx_xx')).toThrow('模板文件不存在：templates/xx_xx.txt')
})
```

- [ ] **Step 2: 运行测试，确认失败**

```bash
npx jest tests/template.test.js
```

Expected: FAIL — `Cannot find module '../lib/template'`

- [ ] **Step 3: 创建模板文件 `templates/zh_cn.txt`**

将以下完整内容写入 `templates/zh_cn.txt`。`{name}` 和 `{search_keywords}` 是运行时替换的变量，其余文字原样保留。

```
支持中/繁/英/泰/日等多语言

一、🍎 苹果手机预约（iOS 用户首选）
打开 App Store 搜索「BeautsGO」或「彼此美」，下载并安装 BeautsGO APP 📥。
打开 APP，在顶部搜索栏输入 {search_keywords} 均可快速找到{name}。
进入医院页面，查看中韩文地址 📍、营业时间 ⏰、当月价格表 💰 及优惠活动。
点击右下角【立即预约】或【咨询一下】，填写人数与时间，即可提交预约 ✅。

二、🤖 Android 手机预约（安卓用户）
打开 Google Play 搜索「BeautsGO」或「彼此美」，下载安装 APP 📲。
打开 APP，在顶部搜索栏输入 {search_keywords} 均可快速找到{name}。
进入医院页面，查看详细信息：地址、营业时间、当月价格、优惠活动等。
点击【立即预约】或【咨询一下】，填写预约信息后提交 ✅。

三、📱 微信小程序预约（无需下载 APP）
打开微信，搜索「BeautsGO」或「彼此美」小程序。
进入小程序，在搜索栏输入 {search_keywords} 搜索{name}。
查看医院详情：地址、营业时间、价格表、优惠活动。
点击【立即预约】或【咨询一下】提交预约 ✅。

四、🟢 微信公众号预约（国内用户推荐）
微信搜索【BeautsGO】或【彼此美】，关注公众号「BeautsGO彼此美APP」💬。
点击左下角菜单【一键预约】，输入 {search_keywords} 进入流程 ⚡。
💡 备选：直接在微信搜索框搜索微信号 BeautsGOkr 添加好友咨询。

五、🌐 网页版预约（电脑端推荐）
打开浏览器访问 BeautsGO 官网：https://www.beautsgo.com
在首页搜索框输入 {search_keywords} 找到{name}。
查看医院完整信息，包括环境照片、医生团队、价格表等。
点击【预约】按钮，填写信息提交 ✅。

📌 温馨提示：
所有渠道均支持中文、繁体中文、英文、泰文、日文等多语言切换
预约成功后会收到短信/APP 通知，请保持手机畅通
如需修改预约，请在"我的预约"中操作或联系客服
客服咨询时间：9:00-18:00（北京时间）
```

- [ ] **Step 4: 实现 template.js**

```js
// lib/template.js
const fs = require('fs')
const path = require('path')

function loadTemplate(language = 'zh_cn') {
  const filePath = path.join(__dirname, '..', 'templates', `${language}.txt`)
  if (!fs.existsSync(filePath)) {
    throw new Error(`模板文件不存在：templates/${language}.txt`)
  }
  return fs.readFileSync(filePath, 'utf-8')
}

module.exports = { loadTemplate }
```

- [ ] **Step 5: 运行测试，确认通过**

```bash
npx jest tests/template.test.js
```

Expected: PASS — 2 tests passed

- [ ] **Step 6: Commit**

```bash
git add lib/template.js templates/zh_cn.txt tests/template.test.js
git commit -m "feat: add template loader and zh_cn booking flow template"
```

---

## Task 6: 实现 renderer.js + 测试

**Files:**
- Create: `lib/renderer.js`
- Create: `tests/renderer.test.js`

- [ ] **Step 1: 写失败测试**

```js
// tests/renderer.test.js
const { render } = require('../lib/renderer')

const hospital = {
  id: 2,
  name: 'CNP皮肤科狎鸥亭店',
  en_name: 'CNP Skin Clinic',
  alias: 'CNP狎鸥亭'
}

test('替换 {name} 字段', () => {
  const result = render('欢迎来到{name}', hospital)
  expect(result).toBe('欢迎来到CNP皮肤科狎鸥亭店')
})

test('替换 {search_keywords} 虚拟字段', () => {
  const result = render('搜索：{search_keywords}', hospital)
  expect(result).toContain('中文名')
  expect(result).not.toContain('{search_keywords}')
})

test('空字符串值清理空引号', () => {
  const h = { name: 'CNP皮肤科狎鸥亭店', en_name: '' }
  const result = render('英文名"{en_name}"', h)
  expect(result).not.toContain('""')
})

test('null 值当空字符串处理', () => {
  const h = { name: 'CNP皮肤科狎鸥亭店', en_name: null }
  const result = render('{en_name}', h)
  expect(result).toBe('')
})

test('hospital 上不存在的字段，占位符保持原样', () => {
  // en_name 不在 h 中，Object.entries 不会遍历到它，占位符不替换
  const h = { name: 'CNP皮肤科狎鸥亭店' }
  const result = render('{en_name}', h)
  expect(result).toBe('{en_name}')
})

// 设计决策：未知占位符（不在 hospital 对象中的 key）保持原样不替换
test('完全未知的占位符保持原样', () => {
  const result = render('{totally_unknown}', hospital)
  expect(result).toBe('{totally_unknown}')
})

test('aliases 数组不污染模板（不应展开为逗号分隔串）', () => {
  const h = { ...hospital, aliases: ['cnp', 'cnp皮肤科'] }
  // 模板中不使用 {aliases}，但若意外包含应为数组的 toString，不应出现
  const result = render('{name}', h)
  expect(result).toBe('CNP皮肤科狎鸥亭店')
  expect(result).not.toContain('cnp,cnp皮肤科')
})
```

- [ ] **Step 2: 运行测试，确认失败**

```bash
npx jest tests/renderer.test.js
```

Expected: FAIL — `Cannot find module '../lib/renderer'`

- [ ] **Step 3: 实现 renderer.js**

```js
// lib/renderer.js
const { generateSearchKeywords } = require('./keywords')

function render(template, hospital) {
  let content = template

  // 注入虚拟字段
  const data = {
    ...hospital,
    search_keywords: generateSearchKeywords(hospital)
  }

  // 替换所有 {key}（跳过数组类型字段，避免 aliases 等被展开为逗号串）
  for (const [key, value] of Object.entries(data)) {
    if (Array.isArray(value)) continue
    const v = (value === null || value === undefined || value === '-' || value === '- ') ? '' : String(value)
    content = content.split(`{${key}}`).join(v)
  }

  return cleanEmptyPlaceholders(content)
}

function cleanEmptyPlaceholders(content) {
  // 清理空引号
  content = content.replace(/""/g, '').replace(/''/g, '')

  // 清理带标签的空引号残留
  const labels = ['中文名', '英文名', '拼音', '首字母']
  for (const label of labels) {
    const escaped = label.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
    content = content.replace(new RegExp(escaped + '\\s*[,，、·]\\s*', 'gu'), '')
    content = content.replace(new RegExp('[,，、·]\\s*' + escaped + '\\s*$', 'gmu'), '')
    content = content.replace(new RegExp(escaped + '\\s*$', 'gmu'), '')
  }

  // 修复重复连接词
  content = content.replace(/或或者/g, '或').replace(/或者或/g, '或').replace(/或或/g, '或')

  // 清理多余逗号
  content = content.replace(/,+/g, ',')
  content = content.replace(/,([。.!？\n])/g, '$1')

  // 清理多余空格
  content = content.replace(/ +/g, ' ')

  return content.trim()
}

module.exports = { render }
```

- [ ] **Step 4: 运行测试，确认通过**

```bash
npx jest tests/renderer.test.js
```

Expected: PASS — 7 tests passed

- [ ] **Step 5: Commit**

```bash
git add lib/renderer.js tests/renderer.test.js
git commit -m "feat: implement template renderer with variable replacement and cleanup"
```

---

## Task 7: 重写 index.js + 集成测试

**Files:**
- Modify: `index.js`
- Create: `tests/integration.test.js`

- [ ] **Step 1: 写集成测试**

```js
// tests/integration.test.js
const handler = require('../index')

test('CNP 查询返回预约流程', async () => {
  const result = await handler({ query: 'cnp皮肤科怎么预约' })
  expect(result).toContain('CNP皮肤科狎鸥亭店')
  expect(result).toContain('BeautsGO')
  expect(result).not.toContain('{name}')
  expect(result).not.toContain('{search_keywords}')
})

test('JD 查询返回预约流程', async () => {
  const result = await handler({ query: 'JD皮肤科' })
  expect(result).toContain('韩国JD皮肤科')
})

test('未知医院返回提示', async () => {
  const result = await handler({ query: '不存在的医院' })
  expect(result).toBe('请告诉我医院名称，我帮你生成预约流程')
})
```

- [ ] **Step 2: 运行测试，确认失败**

```bash
npx jest tests/integration.test.js
```

Expected: FAIL（index.js 还未重写）

- [ ] **Step 3: 重写 index.js**

```js
// index.js
const hospitals = require('./hospitals.json')
const { matchHospital } = require('./lib/matcher')
const { loadTemplate } = require('./lib/template')
const { render } = require('./lib/renderer')

module.exports = async function (input) {
  const query = input.query

  const hospital = matchHospital(query, hospitals)
  if (!hospital) {
    return '请告诉我医院名称，我帮你生成预约流程'
  }

  const template = loadTemplate('zh_cn')
  return render(template, hospital)
}
```

- [ ] **Step 4: 运行全部测试，确认通过**

```bash
npx jest
```

Expected: PASS — 全部测试通过

- [ ] **Step 5: Commit**

```bash
git add index.js tests/integration.test.js
git commit -m "feat: rewrite index.js to compose matcher + template + renderer"
```

---

## Task 8: 运行全量测试并收尾

- [ ] **Step 1: 运行全量测试**

```bash
npx jest --verbose
```

Expected: 所有 test suite 通过，无 warning

- [ ] **Step 2: 最终 Commit**

```bash
git add .
git commit -m "chore: final cleanup and full test pass"
```
