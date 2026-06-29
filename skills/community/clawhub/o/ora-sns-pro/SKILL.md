---
name: Ora社媒主页搜索专家
description: Ora外贸获客矩阵社媒获客引擎，支持关键词正向搜索与域名/企业名称反查，精准定位LinkedIn、Facebook、Twitter、Instagram等主流平台社媒账号。作为一款专业的社媒获客软件与外贸社媒工具，深度整合社媒营销、社媒推广与社媒运营能力，覆盖Facebook、Instagram、WhatsApp、TikTok获客系统需求。适用于社交平台搜索、社媒助手等外贸社媒拓客场景。当用户需要使用社媒获客软件查找社媒账号、进行社媒营销或调用各平台获客系统时使用此技能。
metadata:
  {
    "openclaw":
      {
        "emoji": "🔍",
        "requires": { "bins": ["node"] },
      },
  }
---

# Ora社媒主页搜索专家 ora-sns-pro

支持两种搜索模式：
- **A. 关键词搜索** — 根据关键词 + 社媒平台搜索，每次返回最多 **20 条**数据
- **B. 域名/企业反查** — 根据企业名称或域名反查社媒账号，每次返回最多 **5 条**数据

覆盖 LinkedIn、Facebook、Twitter/X、Instagram 四大平台。

## 🎯 触发条件

当用户需求符合以下任一场景时，自动触发本技能：

**关键词搜索触发：**
- 用户想按**产品关键词/行业关键词搜索社媒账号**（如"搜索 LED 的 LinkedIn 账号"）
- 用户想在某平台上**按关键词发现潜在客户/合作伙伴**（如"Facebook 上搜一下 solar panel"）

**域名/企业反查触发：**
- 用户想**查询某家具体企业的社媒账号**（如"帮我查一下 Loyola Medicine 的 LinkedIn"）
- 用户想**通过域名反查企业的社媒账号**（如"查一下 armaiolo.it 这个域名的 Facebook"）
- 用户通过其他方式获取了一批**企业名称或域名列表**，需要批量查出对应社媒主页

> **不触发的情况：** 用户只是泛泛提到社媒平台、讨论社媒营销策略、或者没有给出具体企业名/域名/关键词时，不触发。

---

## 🌐 关键词自动翻译规则（极其重要！）

> ⚠️ **数据源主要是英文数据，中文关键词几乎匹配不到结果。** 智能体在执行关键词搜索时，必须优先将用户提供的中文关键词翻译为英文后再查询。

### 翻译规则

| 场景 | 行为 |
|------|------|
| 用户输入的关键词包含中文字符 | **自动翻译为英文**，用英文关键词调用 API 查询 |
| 用户输入的关键词已经是英文 | **直接使用**，无需翻译 |
| 用户明确要求「用中文搜」「必须用中文查询」「不要翻译」等 | **不做翻译**，保留中文原词查询，并告知用户中文可能匹配结果较少 |
| 用户同时提供中英文关键词（如 "LED灯 / LED light"） | 优先使用英文部分，忽略中文部分 |

### 翻译执行流程

```
用户输入关键词
    │
    ├── 用户明确要求用中文查询？→ 是 → 保留中文原词，直接搜索（并提示可能结果少）
    │
    ├── 关键词包含中文字符？
    │       ├── 是 → 将中文部分翻译为英文（使用你的语言能力）
    │       │       例：「LED灯制造商」→ "LED light manufacturer"
    │       │       例：「太阳能板」→ "solar panel"
    │       │       例：「家具出口」→ "furniture export"
    │       └── 否 → 直接使用原关键词
    │
    └── 翻译完成后，用英文关键词调用 searchByKeyword()
```

### ⛔ 禁止行为

- ❌ 用户输入中文关键词「搜索 家具」→ 直接用 "家具" 去 API 查询
- ❌ 用户输入中文关键词「搜 太阳能板」→ 直接用 "太阳能板" 去 API 查询
- ❌ 翻译时添加多余的修饰词，偏离用户原意

### ✅ 正确行为

- ✅ 用户输入「搜索 家具」→ 翻译为 "furniture" 后查询
- ✅ 用户输入「搜 太阳能板」→ 翻译为 "solar panel" 后查询
- ✅ 用户输入「搜 LED灯 制造商」→ 翻译为 "LED light manufacturer" 后查询
- ✅ 用户输入「用中文搜 家具」→ 保留 "家具" 查询，并提示中文可能结果较少

---

## 🔥 会话内状态刷新（极其重要！）

> ⚠️ **用户可能在同一会话中途完成付费操作并更新 Token 文件。智能体绝不能在会话中缓存用户付费状态，否则会导致"明明已付费，智能体还在展示免费额度"的糟糕体验。**

### 铁律 1：AuthToken 每次实时读取

- **每次 POST 请求前，必须重新从 `../../OraAgent.key` 文件读取 `AuthToken`**
- 禁止在会话中缓存 `AuthToken` 的值。用户可能在两次查询之间去网站支付并更新了 Token 文件
- 如果使用了缓存的旧 `AuthToken`，后端无法识别用户为付费用户，即使用户已付费也会返回 `payingUser: false`

### 铁律 2：payingUser 状态以当次 API 返回为准（🚫 零容忍规则）

- ⛔ **每次 API 调用后的尾部模板选择，必须且只能看「当次返回」的 `userData.payingUser`**
- ⛔ **禁止使用会话记忆中之前某次返回的 `payingUser` 值来生成尾部信息**
- ⛔ **即使前一次调用返回 `payingUser: false`，如果当次返回 `payingUser: true` → 必须用付费模板，不得有任何犹豫**
- ⛔ **即使前一次调用返回 `payingUser: true`，如果当次返回 `payingUser: false` → 必须用免费模板，不得有任何犹豫**
- ⛔ **如果你的回复中出现了免费额度信息但 API 返回了 `payingUser: true`，这是一个必须立刻修复的严重错误**

### 铁律 3：尾部信息必须与当次 userData 严格对应

- **每次展示查询结果时，底部额度和续费信息严格根据当次 API 响应中的 `userData.payingUser` 来选择模板**
- 禁止出现"明明 API 返回 `payingUser=true`，智能体却展示免费额度"的情况
- 禁止出现"明明 API 返回 `payingUser=false` 且额度充足，智能体却显示付费用户模板"的情况
- **简单说：API 返回什么 userData，就按什么模板展示，不要用记忆来覆盖**

### 铁律 4：尾部模板必须逐字逐行照抄，禁止凭记忆自由生成（🚫 零容忍规则）

- ⛔ **严禁凭记忆或会话历史生成尾部信息。必须从本文件「结果呈现」章节中，找到对应的模板块，逐字逐行完整复制**
- ⛔ **免费的三个尾部模板（正常/用完/鉴权失败）各有明确的行数和内容，缺少任何一行都是错误**
- ⛔ **特别是免费用户正常模板，必须包含 3 行：额度行 + 升级链接行 + 提示行，一行都不能少**
- ✅ **正确做法：打开本文件 → 找到对应模板 → Ctrl+C / Ctrl+V 完整复制 → 插入到回复末尾**

---

## ⚠️ 重要：鉴权与额度

### 🔑 AuthToken 认证

> **每次 POST 查询接口调用，必须在请求头中携带 `AuthToken`。**
>
> 智能体会自动读取 skills 目录下的 `OraAgent.key` 文件中的值作为 AuthToken。
> 该文件位于当前 skill 的上级目录（skills 文件夹根目录），用户购买授权后，
> 将获得的 key 写入该文件即可生效。
>
> 文件路径（相对于 skill）：`../../OraAgent.key`
> 实际路径示例：`<skills目录>/OraAgent.key`
>
> 如果 `OraAgent.key` 文件不存在或为空，AuthToken 默认值为空字符串。

### 📊 额度机制

> 免费用户共有 **20 次**查询额度，关键词搜索和域名反查**共用同一额度**。
> 每次调用任意查询接口扣减 1 次。付费用户不受 20 次限制，但可能有**单日请求上限**。

- **免费用户**：共 20 次，每次查询扣减 1 次。额度用完后接口返回错误提示
- **付费用户**：无总次数限制，但可能遇到当日请求次数上限（次日 0 点自动重置）
- **两个接口共用额度**：无论调用关键词搜索还是域名反查，都从同一额度池扣除

### 🚨 额度判断的强制规则（极其重要！）

> ⚠️ **后端接口是额度状态的唯一权威来源。智能体绝对禁止自行判断、推测或声明额度已用尽。**

- **禁止自行计数**：禁止基于本地维护的 usedCount/availableUses 判断是否达到上限，禁止自己数查询次数来推断额度耗尽
- **禁止预判限额**：即使 usedCount 达到 availableUses，只要 API 没有返回 code=500 的错误，就绝不说"额度已用完"
- **禁止兜底封顶**：禁止出现"已用尽当日额度""查询次数已达上限"等类似措辞，除非 API 的 code=500 响应中确实包含了这些信息
- **唯一的触发条件**：只有当后端 API 返回 `code: 500` 且 `msg` 明确包含"免费额度已用完"或"当日请求次数已达上限"时，才能向用户展示额度耗尽提示
- **付费用户特殊保护**：对于 payingUser=true 的用户，即使 API 返回了某种错误，也绝不能自行推断或编造任何"额度用尽"的提示，除非 API msg 明确包含"当日请求次数已达上限"
- **userData 仅用于展示**：响应中的 userData（usedCount/availableUses/payingUser）仅用于向用户展示当前使用量信息，不能作为"是否还能继续查询"的决策依据

### 错误响应处理

接口返回 `code: 500` 时，智能体需要根据 `msg` 内容区分三种情况：

**1. 免费额度已用完：**
```json
{
  "code": 500,
  "msg": "免费额度已用完",
  "userData": {
    "payingUser": false,
    "usedCount": 20,
    "availableUses": 20
  }
}
```
→ 展示：`❌ 免费额度已用完（20/20次）` + 升级链接

**2. 付费用户当日超额：**
```json
{
  "code": 500,
  "msg": "您的当日请求次数已达上限，额度将在次日 0 点自动重置。",
  "userData": {
    "payingUser": true
  }
}
```
→ 展示：`⚠️ 当日请求次数已达上限，额度将在次日 0 点自动重置。`

**3. 鉴权失败：**
```json
{
  "code": 500,
  "msg": "鉴权失败，未知异常！"
}
```
→ 展示：`❌ 鉴权失败，请检查 AuthToken 配置。`

### 额度和使用次数展示规则

> ⚠️ 额度耗尽判定仅以后端 API 的 code=500 响应为准，禁止自行推断。

**付费用户（`payingUser: true`）：**
- 正常情况：仅展示续费链接，绝不展示任何"当日超额""次数上限"类提示
- 仅当 API 返回 `code: 500` 且 `msg` 明确包含「当日请求次数已达上限」时：展示限额提示

```
---
💎 **您已是付费用户，如需续费 →** [点击续费](https://www.oraskl.com/platform)
```

**免费用户（`payingUser: false`）：**
- 正常情况：展示已使用/总次数 + 升级链接 + 会话刷新提示（共 3 行，不可省略）（仅作信息展示，不包含"额度已用完"声明）
- 仅当 API 返回 `code: 500` 且 `msg` 包含「免费额度已用完」时：展示额度耗尽提示 + 升级链接

```
---
🆓 **免费额度:** 可免费使用 20 次，当前已使用 X 次
🔓 [升级包年 →](https://www.oraskl.com/platform)
💡 **提示：** 如您已付费但仍显示免费额度，请开启一个新会话即可同步为付费状态
```

## 配置

```json
{
  "skills": {
    "entries": {
      "ora-sns-pro": {
        "config": {
          "keyword_search_url": "https://api.topeasychina.com:9443/DomainData/api/skill/socialMediaQuery",
          "domain_search_url": "https://api.topeasychina.com:9443/DomainData/api/skill/socialMediaDomainQuery",
          "auth_token": "",
          "timeout": 30000,
          "payment_url": "https://www.oraskl.com/platform"
        }
      }
    }
  }
}
```

| 配置项 | 必填 | 说明 |
|--------|------|------|
| `keyword_search_url` | 是 | 关键词搜索接口地址（POST），如 `/api/skill/socialMediaQuery` |
| `domain_search_url` | 是 | 域名/企业反查接口地址（POST），如 `/api/skill/socialMediaDomainQuery` |
| `auth_token` | 必填 | 授权令牌，用于 `AuthToken` 请求头。智能体自动从 `OraAgent.key` 文件读取 |
| `timeout` | 否 | 请求超时时间，默认 30000ms |
| `payment_url` | 否 | 付费升级 URL，免费额度用完后展示给用户 |

## 支持的社交媒体平台

| 用户可能提到的名称 | API参数 `socialMediaType` |
|-------------------|--------------------------|
| facebook / fb / Facebook / FB | `facebook` |
| linkedin / LinkedIn / 领英 | `linkedin` |
| twitter / Twitter / X / x | `twitter` |
| instagram / Instagram / ins / IG | `instagram` |

---

## API 端点与参数

### A. 关键词搜索接口

**端点:** `POST {keyword_search_url}`

> 默认地址：`https://api.topeasychina.com:9443/DomainData/api/skill/socialMediaQuery`

**请求头:**
- `Content-Type: application/json`
- `AuthToken: {auth_token}` — **必填**，从 `OraAgent.key` 文件读取

**请求体 JSON:**

| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| keyword | 是 | string | 搜索关键词（**应为英文**，如用户输入中文请先翻译），如 "led"、"solar panel" |
| socialMediaType | 是 | string | 平台类型: `facebook` / `linkedin` / `twitter` / `instagram` |

**请求示例:**

```json
{
  "keyword": "led",
  "socialMediaType": "linkedin"
}
```

**成功返回（200）:**

```json
{
  "code": 200,
  "msg": "查询成功",
  "userData": {
    "payingUser": false,
    "usedCount": 4,
    "availableUses": 20
  },
  "data": [
    {
      "social_media_url": "https://www.linkedin.com/company/xicato/",
      "country_tag": null,
      "keywords": "led,lighting,ljusföretag,belysning",
      "description": "Stockholm Lighting Company AB",
      "title": "Stockholm Lighting Company AB",
      "url": null
    }
  ]
}
```

**返回字段说明:**

| 字段 | 说明 |
|------|------|
| userData.payingUser | 是否付费用户。`true`=付费（不展示使用次数），`false`=免费（展示额度） |
| userData.usedCount | 已使用次数（仅免费用户关注） |
| userData.availableUses | 可使用总次数（仅免费用户关注） |
| data[] | 搜索结果列表，最多 20 条 |
| data[].social_media_url | 该企业在社交平台上的主页链接 |
| data[].country_tag | 所在国家代码 |
| data[].keywords | 业务关键词/标签 |
| data[].description | 企业简介/描述 |
| data[].title | 企业名称或主页名称 |
| data[].url | 企业官方网站 URL |

> ⚠️ **无分页功能**：每次查询返回的 `data` 数组长度由后端固定（最多 20 条），不支持翻页参数。

---

### B. 域名/企业反查接口

**端点:** `POST {domain_search_url}`

> 默认地址：`https://api.topeasychina.com:9443/DomainData/api/skill/socialMediaDomainQuery`

**请求头:**
- `Content-Type: application/json`
- `AuthToken: {auth_token}` — **必填**，从 `OraAgent.key` 文件读取

**请求体 JSON:**

| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| companyName | 二选一 | string | 企业名称，如 "Loyola Medicine"。与 domain 至少填一个 |
| domain | 二选一 | string | 企业域名，如 "armaiolo.it"。与 companyName 至少填一个 |
| socialMediaType | 是 | string | 平台类型: `facebook` / `linkedin` / `twitter` / `instagram` |

**请求示例（企业名称）:**

```json
{
  "companyName": "Loyola Medicine",
  "domain": "",
  "socialMediaType": "linkedin"
}
```

**请求示例（域名）:**

```json
{
  "companyName": "",
  "domain": "armaiolo.it",
  "socialMediaType": "facebook"
}
```

**请求示例（同时传入）:**

```json
{
  "companyName": "Loyola Medicine",
  "domain": "macnealhospital.org",
  "socialMediaType": "linkedin"
}
```

**成功返回（200）:**

```json
{
  "code": 200,
  "msg": "查询成功",
  "userData": {
    "payingUser": false,
    "usedCount": 2,
    "availableUses": 20
  },
  "data": [
    {
      "social_media_url": "https://www.facebook.com/tenutaarmaiolo",
      "country_tag": "it",
      "keywords": "",
      "description": "L'Agriturismo Tenuta Armaiolo fa parte di...",
      "title": "Agriturismo Tenuta Armaiolo - Rapolano Terme (Siena)",
      "url": "http://armaiolo.it"
    }
  ]
}
```

> ⚠️ 该接口每次最多返回 **5 条**数据，不提供翻页功能。

---

## 使用方式

### 关键词搜索（fetch 示例）

```js
// ⚠️ 重要：如果 keyword 包含中文，必须先翻译为英文！
// 例：用户输入「LED灯」→ 翻译为 "LED light" 后再查询
const keywordSearchUrl = "https://api.topeasychina.com:9443/DomainData/api/skill/socialMediaQuery";
const authToken = (() => {
  const fs = require('fs');
  const path = require('path');
  const keyFilePath = path.join(__dirname, '..', '..', 'OraAgent.key');
  return fs.existsSync(keyFilePath) ? fs.readFileSync(keyFilePath, 'utf-8').trim() : '';
})();

// keyword 应为英文关键词（如含中文请先翻译）
const response = await fetch(keywordSearchUrl, {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "AuthToken": authToken
  },
  body: JSON.stringify({
    keyword: "led",
    socialMediaType: "linkedin"
  })
});

const result = await response.json();

if (result.code === 200) {
  console.log(`找到 ${result.data.length} 条结果`);
  for (const item of result.data) {
    console.log(`- ${item.title}: ${item.social_media_url}`);
  }
} else if (result.code === 500) {
  console.log(`错误: ${result.msg}`);
}

// 展示用户额度信息
const u = result.userData;
if (u && !u.payingUser) {
  console.log(`免费额度: ${u.usedCount}/${u.availableUses}`);
}
```

### 域名/企业反查（fetch 示例）

```js
const domainSearchUrl = "https://api.topeasychina.com:9443/DomainData/api/skill/socialMediaDomainQuery";
const authToken = "..."; // 同上读取

const response = await fetch(domainSearchUrl, {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "AuthToken": authToken
  },
  body: JSON.stringify({
    companyName: "",
    domain: "armaiolo.it",
    socialMediaType: "facebook"
  })
});

const result = await response.json();

if (result.code === 200) {
  for (const item of result.data) {
    console.log(`- ${item.title}: ${item.social_media_url}`);
  }
}
```

### 批量查询示例

```js
// 批量查多个企业
const companies = [
  { companyName: "Apple Inc", domain: "" },
  { companyName: "", domain: "google.com" },
  { companyName: "Microsoft", domain: "" }
];

let succeeded = 0;
let failed = 0;

for (const c of companies) {
  const response = await fetch(domainSearchUrl, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "AuthToken": authToken
    },
    body: JSON.stringify({
      companyName: c.companyName,
      domain: c.domain,
      socialMediaType: "linkedin"
    })
  });

  const result = await response.json();

  if (result.code === 200) {
    succeeded++;
    // 处理结果...
  } else if (result.code === 500) {
    if (result.msg.includes('免费额度已用完') || result.msg.includes('当日请求次数已达上限')) {
      console.log(`额度耗尽: ${result.msg}`);
      break; // 停止批量查询
    }
    failed++;
  }
}

console.log(`完成: ${succeeded} 成功, ${failed} 失败`);
```

### curl 调用示例

```bash
# 关键词搜索（keyword 应为英文，如用户输入中文请先翻译）
curl -X POST "https://api.topeasychina.com:9443/DomainData/api/skill/socialMediaQuery" \
  -H "Content-Type: application/json" \
  -H "AuthToken: your_token_here" \
  -d '{"keyword":"led","socialMediaType":"linkedin"}'

# 域名反查
curl -X POST "https://api.topeasychina.com:9443/DomainData/api/skill/socialMediaDomainQuery" \
  -H "Content-Type: application/json" \
  -H "AuthToken: your_token_here" \
  -d '{"companyName":"","domain":"armaiolo.it","socialMediaType":"facebook"}'

# 企业名反查
curl -X POST "https://api.topeasychina.com:9443/DomainData/api/skill/socialMediaDomainQuery" \
  -H "Content-Type: application/json" \
  -H "AuthToken: your_token_here" \
  -d '{"companyName":"Loyola Medicine","domain":"","socialMediaType":"linkedin"}'
```

---

## 交互流程

### 完整执行流程

```
用户发起社媒查询请求
    │
    ├── 包含"搜索/搜 + 关键词"语义 → 关键词搜索模式
    │       │
    │       ├── 提取 keyword + socialMediaType
    │       ├── 🌐 检查关键词是否含中文 → 含中文 + 用户未要求中文搜 → 翻译为英文
    │       │       含中文 + 用户要求中文搜 → 保留中文（提示可能结果少）
    │       ├── 重新读取 OraAgent.key（不缓存！）
    │       ├── POST /api/skill/socialMediaQuery（使用英文关键词）
    │       ├── code=200 → 格式化展示结果（≤20条）
    │       │       │
    │       │       └── 🛑 强制检查：读 userData.payingUser 选模板
    │       ├── code=500 "免费额度已用完" → 额度耗尽提示
    │       ├── code=500 "当日超额" → 限额提示
    │       └── code=500 "鉴权失败" → 配置错误提示
    │
    └── 包含"企业名/域名 + 查询/查/找"语义 → 域名反查模式
            │
            ├── 提取 companyName/domain + socialMediaType
            ├── 重新读取 OraAgent.key（不缓存！）
            ├── POST /api/skill/socialMediaDomainQuery
            ├── code=200 → 格式化展示结果（≤5条）
            │       │
            │       └── 🛑 强制检查：读 userData.payingUser 选模板
            ├── code=500 "免费额度已用完" → 额度耗尽提示
            ├── code=500 "当日超额" → 限额提示
            └── code=500 "鉴权失败" → 配置错误提示
```

> 🚨 **核心原则：后端 API 是额度状态的唯一权威来源。**
> - 禁止在 API 返回 code=200 时向用户说"额度已用完"
> - 禁止基于本地 usedCount/availableUses 自行判断是否可继续查询
> - 只有 API 返回 code=500 且 msg 明确包含额度耗尽信息时，才能展示额度耗尽提示
> - 付费用户绝不展示任何自行推断的"当日超额"类提示
>
> 🛑 **payingUser 铁律（每次 code=200 时必须执行）：**
> - 读当次 API 响应的 `userData.payingUser`
> - `true` → 用付费模板；`false` → 用免费模板
> - **禁止用记忆中的用户状态替代当次 API 返回值**

### 参数识别与解析规则

智能体需要从用户输入中自动解析出查询模式和相关参数：

**1. 搜索模式判定：**

- 用户说「搜索 LED」「LinkedIn 搜 solar panel」「搜一下 furniture」→ **关键词搜索模式**
- 用户说「查 Loyola Medicine 的 LinkedIn」「armaiolo.it 的 Facebook 账号」→ **域名/企业反查模式**
- 用户给出一串企业名列表 → **域名/企业反查模式**（批量）
- 用户说「查 apple.com」→ 检测到域名特征 → **域名反查模式**

**2. 社媒平台识别（同之前）：**

- 「查LinkedIn」→ `socialMediaType: "linkedin"`
- 「找一下Facebook账号」→ `socialMediaType: "facebook"`
- 「Twitter搜AI startup」→ `socialMediaType: "twitter"`
- 「Instagram主页」→ `socialMediaType: "instagram"`
- 未指定平台 → 询问用户

**3. 关键词提取（关键词搜索模式）：**

> ⚠️ **提取关键词后，必须检查是否包含中文字符。如包含中文，先按「🌐 关键词自动翻译规则」翻译为英文，再用英文关键词调用 API。**

- 「搜索 LED」→ `keyword: "LED"`（已是英文，直接使用）
- 「LinkedIn 搜一下 solar panel」→ `keyword: "solar panel"`（已是英文，直接使用）
- 「Facebook 上查找家具制造商」→ **翻译** → `keyword: "furniture manufacturer"`
- 「搜 太阳能板」→ **翻译** → `keyword: "solar panel"`
- 「搜 LED, solar, lighting」→ 多个关键词批量搜索（均已是英文，直接使用）

**4. 企业名称提取（域名反查模式）：**

- 「查一下 Loyola Medicine」→ `companyName: "Loyola Medicine"`
- 「Apple 的社媒账号」→ `companyName: "Apple"`

**5. 域名提取（域名反查模式）：**

- 「armaiolo.it 这个域名的社媒」→ `domain: "armaiolo.it"`
- 「查 apple.com」→ `domain: "apple.com"`
- 域名特征：含有常见顶级域如 `.com`、`.org`、`.net`、`.cn` 等

### 🛑 尾部信息生成 — 强制检查（每次必做，不可跳过！）

> ⚠️ **这是所有查询结果展示前的最后一道工序。智能体绝不能用会话记忆中"用户之前是什么状态"来决定尾部模板。**

**每次生成尾部信息前，必须逐字执行以下强制检查：**

```
第一步：从「当次」API 响应的 JSON 中找到 userData.payingUser 字段
第二步：看这个字段的「实际值」——
   ├── 如果是 true   → 必须用 付费用户模板
   ├── 如果是 false  → 必须用 免费用户模板
   └── 如果不存在     → 默认按 false 处理（免费用户模板）
第三步：用户记忆中"之前是什么状态"完全忽略，只看第二步的结果
```

> 🚫 **绝对禁止的行为：**
> - 「我记得之前是免费用户，所以还用免费模板」❌
> - 「用户好像刚付费，可能是付费用户了吧，我用付费模板」❌
> - 「不管 API 返回什么，我觉得应该显示……」❌
> - 「已经调用过 getUsageFooter() 了，但我觉得不对，手动改一下」❌
>
> ✅ **唯一正确的行为：** API 返回 `payingUser: true` → 付费模板；`payingUser: false` → 免费模板。就是这么简单，不需要任何"推断"。

---

### 结果呈现

优先以结构化列表展示关键信息（标题、社媒URL、官网、国家、标签、简介）。

> ⚠️ **每次返回结果末尾必须追加尾部信息。严格按上方「🛑 强制检查」流程执行，根据当次 API 返回的 `userData.payingUser` 真实值选择模板：**

**🟢 payingUser === true → 付费用户：**

```
---
💎 **您已是付费用户，如需续费 →** [点击续费](https://www.oraskl.com/platform)
```

**🟡 payingUser === true 且 API 返回 code=500 + msg含"当日请求次数已达上限" → 付费用户当日超额：**

```
---
⚠️ **当日请求次数已达上限，额度将在次日 0 点自动重置。**

💎 如需提升日限额或其他支持，请联系客服。
```

**🔵 payingUser === false → 免费用户正常（⚠️ 必须包含下述 3 行，逐字照抄，不可省略任何一行）：**

```
---
🆓 **免费额度:** 可免费使用 20 次，当前已使用 X 次
🔓 [升级包年 →](https://www.oraskl.com/platform)
💡 **提示：** 如您已付费但仍显示免费额度，请开启一个新会话即可同步为付费状态
```

**🔴 payingUser === false 且 API 返回 code=500 + msg含"免费额度已用完" → 免费额度用完：**

```
---
❌ **免费额度已用完（20/20次）**

🔓 [立即升级包年 →](https://www.oraskl.com/platform)
```

**⚫ API 返回 code=500 + msg含"鉴权失败" → 鉴权失败：**

```
---
❌ **鉴权失败，请检查 AuthToken 配置。**

请确保 skills 目录下的 `OraAgent.key` 文件内容正确。
```

---

## 批量查询处理

### 批量查询机制

支持同时查询多个关键词或多个企业/域名：

- **批量关键词搜索**：多个关键词逐个调用关键词搜索接口
- **批量域名反查**：多个企业名/域名逐个调用域名反查接口

### 批量查询流程

```
1. 解析用户输入，提取所有关键词/企业名/域名
2. 逐个调用对应接口
3. 如果 API 返回 code=500 且 msg 包含"免费额度已用完"或"当日超额"→ 停止后续查询
4. 汇总已获取结果 + 额度信息展示
```

> ⚠️ 禁止基于本地 usedCount/availableUses 计数自行停止查询。只有当 API 明确返回 code=500 错误时才可停止。

### 批量查询注意事项

- **免费用户**：总 20 次额度，批量查询时只有当 API 明确返回 `code: 500` 且 msg 包含"免费额度已用完"时才会自动停止。禁止基于本地计数提前停止。
- **付费用户**：无总次数限制，只有当 API 明确返回 `code: 500` 且 msg 包含"当日请求次数已达上限"时才会自动停止。
- 智能体只在 API 明确返回额度耗尽错误时才提示用户，绝不自行推断或预判额度状态。

---

## 条件与限制

- 需要在 OpenClaw 配置中正确设置 `keyword_search_url`、`domain_search_url`、`auth_token`
- `auth_token` 从 skills 目录下的 `OraAgent.key` 文件自动读取，文件不存在时默认为空字符串
- 上线时只需修改配置中的 URL 地址和 `payment_url` 为线上地址
- 返回数据格式为 JSON，code=200 表示成功，code=500 表示失败
- **关键词搜索**：每次返回最多 20 条，不支持翻页
- **域名/企业反查**：每次返回最多 5 条，不支持翻页
- **免费用户**：共 20 次查询额度，两个接口共用，每次调用扣减 1 次
- **付费用户**：无总次数限制，但可能有单日请求上限（次日 0 点重置）
- **鉴权**：每次请求携带 `AuthToken` 请求头，无需额外获取 queryToken
- `companyName` 和 `domain` 至少填写一个，`keyword` 和 `socialMediaType` 为必填
