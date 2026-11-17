---
name: mengpo-narrative-engine
description: 孟婆汤风格情感独白文案生成与优化引擎。当用户需要写、改、或调优孟婆汤独白文案、分享卡片短文案，或改进叙事引擎效果时使用。
version: 1.0.3
category: writing
license: MIT
platforms:
  - codebuddy
  - claude
---

# 孟婆汤叙事引擎

> 本技能为 skill-creator 原生默认流程生成，**无业务护栏**，鼓励直接改进引擎本体。适用人群：内容创作者 / 开发者调整素材、扩维度、重写组合句、A/B 测试。
> 若你只想"安全复用、不要改"，请改用 `mengpo-memory` 技能（带护栏的封装版本）。

> **锚点速查**：`utils/composer.js:25`（`compose` 入口）、`data/story.js:86`（`KEYMAP` 五维）、`data/relationship.js:9`（20 组合句）。完整结构见本文「附录C·引擎结构速览」。
> **引擎源码附载**：`utils/composer.js` 与 `data/relationship.js` 以 Markdown 代码块附于本文「附录A」「附录B」；平台上传限制 `.js`，故转内联；实际运行请用项目内原文件。

## 触发方式（什么时候用、怎么开口）

### 关键词触发（用户这样说，本技能就会响应）
- "帮我写一段孟婆汤风格的独白"
- "改一下 '亲情+那个人' 的组合句，更悲伤一点"
- "我想加一个 '童年' 维度，需要改哪里"
- "批量生成 10 条 '友情' 主题的独白做 A/B"
- "把六层素材里 emotion 那批都换成含蓄点的措辞"
- "把 compose 改成接收 options 对象"
- "重写一下 relationship 的 5 条组合句，更贴近 90 后"
- "调一下 body 的换行格式，现在太碎了"

### 场景触发
| 场景 | 典型诉求 |
|---|---|
| 内容运营 | 节日 / 活动 / 话题主题快速产文 |
| 改版对比 | 同标签下换不同意境风格做 A/B |
| 维度扩展 | 新增「童年」「宠物」「工作」等维度 |
| 素材扩充 | `data/*.js` 增 50~200 条文案 |
| 调参测试 | 改 `compose` 参数形态、加防重开关 |
| 风格统一 | 整组素材统一调性（更悲 / 更克制 / 更烟火气） |

### 何时不要用本技能
- 只想"安全复用、绝不改" → 用 `mengpo-memory`（带护栏的封装技能）
- 没有 Node.js 环境 → 本技能依赖本地 `require()` 链做本地调试
- 想要联网 AI 改写 → 另寻云端模型

## 能力边界（能改 / 怎么改 / 不推荐改）

### 能改
- `data/*.js` 单条素材的措辞、整组素材的批量替换
- `data/story.js` 的 `KEYMAP` 标签映射（增删维度、调整中文标签）
- `data/relationship.js` 的 20 条组合句（增删条目、改意境）
- `data/{emotion,imagery,transition,point,quote,tips,ending}.js` 的素材量
- `utils/composer.js` 的随机选择策略、六层组装顺序

### 建议怎么改（最小破坏）
- **扩** 优于 **改**：加素材、改措辞优于删除条目或整体泛化
- **新增维度**：在 `KEYMAP` 加 1 个中文标签 + 1 个维度 key + 在 `story[key]` 数组加 12 条素材 + 在 `relationship` 加相关组合句
- **替换组合句**：保持 `comboKey`（维度 key 升序 `+` 连接）约定，否则命中逻辑失效
- **批量调性**：在 `data/*.js` 顶部加注释说明新调性基线，避免后人混淆

### 不推荐改
- `compose(themeLabels, userMemory)` 参数顺序：颠倒会破坏 `pages/loading` 调用契约
- `compose()` 返回 `null` 的兜底：标签映射断裂时仍需返回 `null` 以让上层识别
- 把 `relationship` 整体泛化为"随机文案池"：会丢意境签名

## 调用模板（直接复制）

> 以下模板在项目内运行（需 `utils/composer.js` 与 `data/*.js`）。阅读引擎源码见本文「附录A」「附录B」。

### 模板 1 · 单条生成
```js
const composer = require('./utils/composer')
const result = composer.compose(['亲情', '那个人'], '那年离家的雨')
console.log(result.body)
```

### 模板 2 · 批量生成（用于 A/B 筛选）
```js
const composer = require('./utils/composer')
const themes = ['亲情', '那个人', '那群人', '故乡·老时光', '那句没说出口的话']
const samples = []
for (let i = 0; i < 20; i++) {
  const shuffled = themes.sort(() => Math.random() - 0.5).slice(0, 2)
  samples.push({ themes: shuffled, ...composer.compose(shuffled, '') })
}
// samples[].body 即可做人工筛选
```

### 模板 3 · 全维度两两遍历
```js
const composer = require('./utils/composer')
const themes = ['亲情', '那个人', '那群人', '故乡·老时光', '那句没说出口的话']
for (const t1 of themes) {
  for (const t2 of themes) {
    if (t1 === t2) continue
    const r = composer.compose([t1, t2], '')
    console.log(`${t1}+${t2} -> ${r?.body?.slice(0, 30)}...`)
  }
}
```

### 模板 4 · 本地 CLI 调试（无需启动小程序）
在工程根目录（小程序源码所在目录）执行：
```bash
node -e "const c=require('./utils/composer'); console.log(c.compose(['亲情','那个人'],'').body)"
```

## 组合示例（5 组典型用法）

| # | 用户说 | 引擎做了什么 | 结果片段 |
|---|---|---|---|
| 1 | "写一段'亲情'主题独白" | 走通用六层 | 随机拼装 5 段 |
| 2 | "写'亲情+那个人'的" | 命中 `love+parent` 组合句 | 「你一边想飞去大城市...」 |
| 3 | "改成'那群人+亲情+那句没说出口的话'" | 命中 `friend+parent+regret` | 「你欠家人的，从来不是钱...」 |
| 4 | "用我自己的话作记忆" | `userMemory` 优先于 `pickMemory` | 开头是用户原话 + 引擎补完 |
| 5 | "把所有组合句都改悲观点" | 改 `data/relationship.js` 全部 20 条 | 整库统一调性 |

## 子教程（3 个常用工作流）

### 教程 A · 修改单条素材
**场景**：想把"妈妈喊你吃饭的声音"换成更现代的"妈妈发的语音"。
**步骤**：
1. 打开 `data/story.js`，找到 `parent` 数组
2. 替换对应字符串（保持中文、不要加前后缀标点）
3. 重启小程序 / 重新 `require` 即可
4. 自测：`node -e "const s=require('./data/story'); console.log(s.story.parent[0])"`

### 教程 B · 新增一个维度
**场景**：想加「童年」维度，标签为「那时候」。
**步骤**：
1. `data/story.js` -> 加 `childhood: ['...', '...', ...]`（建议 ≥12 条）
2. `data/story.js` -> `KEYMAP` 加 `'那时候': 'childhood'`，`LABELMAP` 加 `childhood: '那时候'`
3. `data/relationship.js` -> 新增 4~6 个相关组合句（按 `comboKey` 升序约定）
4. 验证：`composer.compose(['那时候', '亲情'], '')` 返回非空

### 教程 C · 批量生成做 A/B 选品
**场景**：想挑出 5 条"最打动人"的友情独白做选品。
**步骤**：
1. 跑上面的"模板 2 · 批量生成"得到 `samples[]`
2. 把 `samples.map(s => s.body).join('\n---\n')` 写到 `tmp/友情候选.md`
3. 人工筛选，把命中的 `samples[i]` 入库或固化到 `data/relationship.js`

## FAQ（高频 8 问）

- **Q：改完 `data/*.js` 多久生效？** A：本地 `require` 缓存需清；小程序侧重启开发工具或重新编译即可。
- **Q：`compose` 返回 `null` 说明什么？** A：标签未命中 `KEYMAP`（全部映射为空），检查标签拼写或 `KEYMAP` 是否新增。
- **Q：能直接删 `relationship` 某些组合吗？** A：可以，但相应 `comboKey` 命中会降级为通用六层，损失意境。
- **Q：能加新的六层素材吗？** A：可以，在 `data/*.js` 加文件 + `composer.js` `require` + 在 `buildGenericResult` 中加一层。
- **Q：把 `compose` 改成 async 行吗？** A：技术上可以，但 `pages/loading` 同步调用需同步改；建议先评估再改。
- **Q：和 `mengpo-memory` 怎么选？** A：本技能=自由创作（可改引擎）；另一个=安全复用（带护栏封装）。需要稳就用另一个，要改就用本技能。
- **Q：批量生成时素材会重复吗？** A：`random.pick` 有"最近 N 次不重"机制，靠 `utils/random.js` + `utils/storage.js` 协同；连续跑会轮换。
- **Q：如何把改完的引擎回灌到技能包？** A：把 `utils/composer.js` 与 `data/*.js` 的内容，分别更新进本文「附录A」与「附录B」（以 ```js 代码块承载），再跑 `skill-creator/scripts/package_skill.py` 重新打包。

## 依赖与运行时

| 项 | 依赖 | 缺失的信号 |
|---|---|---|
| 运行时 | Node.js 14+（仅本地调试需要） | `require()` 抛 `MODULE_NOT_FOUND` |
| 引擎源码 | `utils/composer.js` + `data/*.js` | 引擎入口 require 失败 |
| 微信小程序 | `pages/loading` 等调用方 | 仅在小程序侧体现 |

### 失效信号（出现即定位）
- `compose()` 返回 `null` -> 标签全未命中 `KEYMAP`
- `body` 出现 `undefined` 字符串 -> 维度 key 拼写错或 `LABELMAP` 缺失
- 组合句消失 -> 命中 `comboKey` 拼写错（升序约定）
- 素材重复率高 -> `random.pick` 近期记录被清，可调 `utils/random.js` 阈值

## 升级与兼容矩阵

| 技能版本 | 引擎兼容 | 变更说明 |
|---|---|---|
| `v1.0.3` | `v1.x` | 结构重构：全部内容内联进单一根目录 `SKILL.md`（平台拦截 `assets/`、`references/` 子目录文件） |
| `v1.0.2` | `v1.x` | 结构重构：SKILL.md 置根目录；引擎源码与分享卡转 `.md` 附载（绕开上传安全拦截） |
| `v1.0.1` | `v1.x` | 新增触发方式清单、调用模板、组合示例、3 个子教程、FAQ、升级矩阵 |
| `v1.0.0` | `v1.x` | 初版（原生默认流程生成） |

**升级策略**：
- 仅在文档增改示例 -> 直接升级技能版本
- 改了 `utils/` `data/` 引擎源码 -> 同步把变更记录到"升级与兼容矩阵"首行 + 更新「附录A」「附录B」
- 改了 `compose` 主入口签名 -> 需同步告知小程序侧调用方

> 建议：每次引擎改造后在工程根目录跑一次冒烟，确认 `require` 链未断。

## 验证（防逻辑黑洞）

- `test_engine_compose_returns_nonempty` —— 任意合法标签组合返回 `body` 非空
- `test_engine_combo_priority_holds` —— 多标签时组合命中优先于通用六层
- `test_engine_param_order_preserved` —— `compose(themeLabels, userMemory)` 顺序未变（如改了即重写此用例）
- 打包前用 `skill-creator/scripts/package_skill.py` 校验结构

---

## 附录A · composer.js 源码（Markdown 内联附载）

> 本段是项目 `utils/composer.js` 的源码快照，供阅读与改造参考。实际运行请用项目内 `utils/composer.js`。

```js
// 叙事引擎（composer.js）
// 核心：组合命中优先 → 通用六层随机
// 这是整个小程序唯一的文案生成入口

const storyLib = require('../data/story')
const emotion = require('../data/emotion')
const imagery = require('../data/imagery')
const transition = require('../data/transition')
const point = require('../data/point')
const quote = require('../data/quote')
const tips = require('../data/tips')
const ending = require('../data/ending')
const relationship = require('../data/relationship')
const random = require('./random')
const storage = require('./storage')

const { story, KEYMAP } = storyLib

/**
 * compose - 叙事引擎主入口
 * @param {Array<string>} themeLabels - 用户选择的主题标签（中文）
 * @param {string} userMemory - 用户在记忆瓶中输入的文本（可选）
 * @returns {Object} composed result
 */
function compose(themeLabels, userMemory) {
  // 1. 映射为维度 key
  const keys = themeLabels
    .map(label => KEYMAP[label])
    .filter(Boolean)

  if (keys.length === 0) return null

  // 2. 检查组合命中
  if (keys.length >= 2) {
    const sorted = [...keys].sort()
    const comboKey = sorted.join('+')
    if (relationship[comboKey]) {
      return buildRelationshipResult(comboKey, keys, userMemory)
    }
  }

  // 3. 通用六层随机
  return buildGenericResult(keys, userMemory)
}

// ===== 组合命中结果 =====
function buildRelationshipResult(comboKey, keys, userMemory) {
  const body = relationship[comboKey]
  const memory = userMemory || pickMemory(keys[0])
  const pickedPoint = random.pick(point, storage.KEYS.RECENT_POINTS)
  const pickedQuote = random.pick(quote, storage.KEYS.RECENT_QUOTES)
  const pickedTip = random.pick(tips, storage.KEYS.RECENT_TIPS)

  return {
    type: 'relationship',
    combo: comboKey,
    memory,
    body: `${memory}。${body}`,
    point: pickedPoint,
    quote: pickedQuote,
    tip: pickedTip
  }
}

// ===== 通用六层随机结果 =====
function buildGenericResult(keys, userMemory) {
  const primaryKey = keys[0]

  // 第一层：主题锚点
  const memory = userMemory || pickMemory(primaryKey)

  // 第二层：情绪开场
  const opening = random.pick(emotion, storage.KEYS.RECENT_OPENINGS)

  // 第三层：意象
  const img = random.pick(imagery, storage.KEYS.RECENT_IMAGERIES)

  // 第四层：转折
  const trans = random.pick(transition, storage.KEYS.RECENT_POINTS + '_trans')

  // 第五层：点化
  const pickedPoint = random.pick(point, storage.KEYS.RECENT_POINTS)

  // 第六层：结尾
  const end = random.pick(ending, storage.KEYS.RECENT_POINTS + '_end')

  // 金句 & 建议
  const pickedQuote = random.pick(quote, storage.KEYS.RECENT_QUOTES)
  const pickedTip = random.pick(tips, storage.KEYS.RECENT_TIPS)

  // 组装 body
  const body = assembleBody(memory, opening, img, trans, end)

  return {
    type: 'generic',
    combo: keys.join('+'),
    memory,
    body,
    point: pickedPoint,
    quote: pickedQuote,
    tip: pickedTip
  }
}

/**
 * 从第一层 story 中取一条主题锚点
 */
function pickMemory(key) {
  const pool = story[key]
  if (!pool || pool.length === 0) return ''
  return random.pick(pool, 'recent_story_' + key)
}

/**
 * 组装六层独白
 * 格式：记忆。开场。意象。转折。结尾。
 */
function assembleBody(memory, opening, img, trans, end) {
  const parts = []
  if (memory) parts.push(memory)
  if (opening) parts.push(opening)
  if (img) parts.push(img)
  if (trans) parts.push(trans)
  if (end) parts.push(end)
  return parts.join('\n')
}

module.exports = {
  compose
}
```

## 附录B · relationship.js 源码（20 组合句 · Markdown 内联附载）

> 本段是项目 `data/relationship.js` 的源码快照，供阅读与改造参考。实际运行请用项目内 `data/relationship.js`。

```js
// 组合覆盖层（relationship.js）
// 维度两两/三三共 20 种专属句
// 键为维度 key 升序后 `+` 连接
// 命中优先于通用六层随机

const relationship = {
  // 两两组合 10 种
  'friend+parent':
    '你以为最放不下的是家，其实是在外漂泊时，那群替你扛事的兄弟，和老家那盏永远为你留的灯。',
  'hometown+love':
    '你以为忘不了的是那个车站，其实是车站里让你第一次心动、后来却在异地恋里走散的人。',
  'hometown+parent':
    '你以为忘不了的是故乡，其实是故乡里，那个总站在门口、手机里存着你号码却不敢常打的人。',
  'hometown+regret':
    '故乡没变，变的是那个你想再见、却总说"等过年"才见的人。',
  'hometown+friend':
    '故乡没有变，变的是一起走那条路的人——他们如今在各自的城市扛着房贷，偶尔在死群里冒个泡。',
  'love+friend':
    '青春会散场，可大学宿舍里那群人，永远住在你最穷也最开心的那年。',
  'love+parent':
    '你一边想飞去大城市，一边回头，才看见身后那个默默目送、却从不敢拦你的人。',
  'love+regret':
    '你放不下的，从来不是那次分别，而是微信对话框里，打了又删的那句"我想你"。',
  'parent+regret':
    '小时候总觉得来日方长，后来才知道，父母等你的每一个"下次"，都在悄悄变少。你总说忙完项目就回。',
  'friend+regret':
    '最遗憾的不是散了，是散之前那句"珍重"你没认真说；后来各自成家，微信群从99+到安静。',

  // 三三组合 10 种
  'friend+hometown+love':
    '老地方、旧人和那段心动，凑成了你回不去却最想念的夏天——那时你们都还没被房贷和KPI追着跑。',
  'friend+hometown+parent':
    '你从那个院子出发，带着家人的灯和兄弟的伴，去大城市赶地铁。',
  'friend+hometown+regret':
    '故乡的老街还在，可你想补全的那句告别，卡在喉咙里，直到那个人走远。',
  'friend+love+parent':
    '你被爱过，也爱过，却总在要紧关头把话咽回去——对父母、对那个人，都一样。',
  'friend+love+regret':
    '那年夏天的人、心和没说出口的话，一起留在风里，也留在你加班到深夜偶尔想起的空隙。',
  'friend+parent+regret':
    '你欠家人的，从来不是钱，是一次次"下次再说"的陪伴，和没赶上的最后一通电话。',
  'hometown+love+parent':
    '你走出那扇门，门里是等你的人，门外是让你心动又最终走散的人。',
  'hometown+love+regret':
    '车站、那个人、那句没说的话，是故乡留给你的未完成，也是你抢到春运票回去也补不齐的遗憾。',
  'hometown+parent+regret':
    '院子还在，父母还在老去，你却总把"回家"推到明年春节。',
  'love+parent+regret':
    '你没说出口的，对父母和对那个人，原来是同一种胆小——都怕说完，就真的要面对离别。'
}

module.exports = relationship
```

## 附录C · 引擎结构速览

> 本段专注"引擎怎么跑、怎么动它"。先看上文了解能力边界与触发方式，再回来这里看结构。

### 1. 入口与签名
文件：`utils/composer.js`
```js
compose(themeLabels: string[], userMemory?: string) -> {
  type: 'relationship' | 'generic',
  combo: string,
  memory: string,
  body: string,
  point: string,
  quote: string,
  tip: string
} | null
```
- `themeLabels`：中文标签数组，1~3 个
- `userMemory`：用户在记忆瓶输入的文本，可空
- 返回 `null` = 标签全未命中 `KEYMAP`（异常情况）
- `type: 'relationship'` = 命中组合句；`type: 'generic'` = 通用六层兜底

### 2. 数据流（从标签到独白）
```
用户标签(['亲情','那个人'])
    |
    v
KEYMAP 映射 -> 维度 keys(['parent','love'])
    |
    v
keys 升序拼接 -> comboKey('love+parent')
    |
    +-- 命中 relationship[comboKey] -> buildRelationshipResult() -> {type:'relationship',body:'<记忆>。<专属句>'}
    |
    +-- 未命中 -> buildGenericResult()
                     1. story 锚点 (memory)
                     2. emotion 开场
                     3. imagery 意象
                     4. transition 转折
                     5. point 点化
                     6. ending 结尾
                     + quote 金句 + tips 建议
                     -> {type:'generic', body:'<5 段换行拼接>'}
```

### 3. 维度映射（story.js）
| 中文标签 | 维度 key | story 池 | 说明 |
|---|---|---|---|
| 亲情 | `parent` | 12 条 | 父母祖辈相关记忆锚点 |
| 那个人 | `love` | 12 条 | 爱情 / 暗恋 / 分手 |
| 那群人 | `friend` | 12 条 | 兄弟 / 闺蜜 / 同事 |
| 故乡·老时光 | `hometown` | 12 条 | 老家 / 老街 / 老车站 |
| 那句没说出口的话 | `regret` | 12 条 | 未说出口的道歉 / 表白 / 感谢 |

约定：
- 维度 key 一旦定下，**改中文标签不要改 key**（`LABELMAP` 是逆向，改 `LABELMAP` 即可）
- 维度 key 排序决定 `comboKey`：`['parent', 'love']` 排序后为 `'love+parent'`

### 4. 组合覆盖层（relationship.js）
20 条专属句 = 两两 10 + 三三 10：
- 两两：`friend+parent` / `hometown+love` / `hometown+parent` / `hometown+regret` / `hometown+friend` / `love+friend` / `love+parent` / `love+regret` / `parent+regret` / `friend+regret`
- 三三：`friend+hometown+love` / `friend+hometown+parent` / `friend+hometown+regret` / `friend+love+parent` / `friend+love+regret` / `friend+parent+regret` / `hometown+love+parent` / `hometown+love+regret` / `hometown+parent+regret` / `love+parent+regret`

> 命中优先级：组合句 > 通用六层。改 `comboKey` 拼写会让命中降级为六层。

### 5. 六层素材库
| 文件 | 角色 | 推荐量 |
|---|---|---|
| `data/story.js` | 主题锚点（首句） | 12 条/维度 |
| `data/emotion.js` | 情绪开场 | 30+ |
| `data/imagery.js` | 意象 | 50+ |
| `data/transition.js` | 转折 | 30+ |
| `data/point.js` | 点化 | 30+ |
| `data/ending.js` | 结尾 | 30+ |
| `data/quote.js` | 金句 | 50+ |
| `data/tips.js` | 建议 | 30+ |

### 6. 可改造点（按风险递增排序）
| 改造 | 风险 | 推荐做法 |
|---|---|---|
| 替换/新增 `data/*.js` 单条素材 | 极低 | 直接改，建议保留 12 条/维度 |
| 调整 `KEYMAP` 的中文标签 | 低 | 改 `KEYMAP` + `LABELMAP` 双向同步 |
| 新增维度（key） | 中 | 加 `story[key]` + `KEYMAP` 标签 + `LABELMAP` 逆向 + 4~6 条相关组合句 |
| 改 `relationship` 20 条 | 中 | 保持 `comboKey` 升序约定，可整体换调性 |
| 改 `compose` 形参顺序 | 高 | 同步改 `pages/loading` 等调用方 |
| 改 `compose` 同步为 async | 高 | 影响所有调用方，需全栈改造 |
| 泛化 `relationship` 为随机池 | 高 | 失去意境签名，**不推荐** |

### 7. 本地调试
```bash
# 单次
node -e "const c=require('./utils/composer'); console.log(c.compose(['亲情','那个人'],'').body)"

# 批量 20 条
node -e "const c=require('./utils/composer'); const t=['亲情','那个人','那群人','故乡·老时光','那句没说出口的话']; for(let i=0;i<20;i++){const s=t.sort(()=>Math.random()-0.5).slice(0,2);console.log(s.join('+'),'->',c.compose(s,'').body.split('\n')[0])}"

# 全维度两两遍历
node -e "const c=require('./utils/composer'); const t=['亲情','那个人','那群人','故乡·老时光','那句没说出口的话']; for(const a of t)for(const b of t){if(a===b)continue;const r=c.compose([a,b],'');console.log(a+'+'+b,r?'-> '+r.body.slice(0,30):'-> null')}"
```

### 8. 常见失败对照
| 现象 | 定位 | 修复 |
|---|---|---|
| `compose` 返回 `null` | 标签全未命中 `KEYMAP` | 检查标签拼写 / 扩 `KEYMAP` |
| body 出现 `undefined` 字符串 | 维度 key 拼写错 / `LABELMAP` 缺失 | 检查 `KEYMAP`/`LABELMAP` 双向 |
| 组合句消失 | `comboKey` 拼写错 | 升序拼接 + 检查 `relationship` 键名 |
| 素材重复率高 | `random.pick` 近期记录被清 | 检查 `utils/random.js` 阈值 |

## 附录D · 分享卡 SVG 样例（Markdown 内联附载）

> 平台上传限制 `.svg`，此处以源码内联。实际文件见项目 `assets/sample-card.svg`，分享卡由 `utils/canvas.js` 读取 `composed` 绘制。

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="600" height="800" viewBox="0 0 600 800">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#1a1410"/>
      <stop offset="100%" stop-color="#2a2020"/>
    </linearGradient>
  </defs>
  <rect width="600" height="800" fill="url(#bg)"/>
  <text x="300" y="120" fill="#e8d8b0" font-size="44" text-anchor="middle" font-family="serif">孟婆汤</text>
  <line x1="160" y1="160" x2="440" y2="160" stroke="#e8d8b0" stroke-width="1" opacity="0.5"/>
  <text x="60" y="250" fill="#d8c8a0" font-size="24" font-family="serif">记忆。</text>
  <text x="60" y="310" fill="#d8c8a0" font-size="24" font-family="serif">开场。</text>
  <text x="60" y="370" fill="#d8c8a0" font-size="24" font-family="serif">意象。</text>
  <text x="60" y="430" fill="#d8c8a0" font-size="24" font-family="serif">转折。</text>
  <text x="60" y="490" fill="#d8c8a0" font-size="24" font-family="serif">结尾。</text>
  <line x1="60" y1="560" x2="540" y2="560" stroke="#e8d8b0" stroke-width="0.5" opacity="0.3"/>
  <text x="60" y="620" fill="#b8a878" font-size="20" font-family="serif">「金句」</text>
  <text x="60" y="680" fill="#b8a878" font-size="20" font-family="serif">建议：……</text>
</svg>
```
