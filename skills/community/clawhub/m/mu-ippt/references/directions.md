# 快捷方向包（Direction Presets）

> 当用户风格模糊或说"帮我选一个方向"时，推荐以下 6 个方向包。每个方向包是一组确定性的设计参数——色板+字体+节奏+规则——消除 AI 自由发挥带来的风格漂移。

## 使用方式

1. 用户风格不明确时，策略师展示 7 个方向的**名称+一句话描述+适用场景**
2. 用户选定后，将该方向的色板、字体栈、Posture 规则**原样**注入 `design_spec.md`
3. 如用户要求微调（如"accent 换成绿色"），仅修改指定项，其余保持不变

---

## D1. 商务克制 — "让数据自己说话"

| 属性 | 值 |
|------|-----|
| **一句话** | 咨询级别的安静权威感，如同 McKinsey 报告搬上了屏幕 |
| **绑定哲学** | 01 Pentagram 信息架构 |
| **默认 Token** | stripe |
| **适用场景** | 董事会汇报、战略报告、数据密集型演示、咨询交付物 |

### 色板（OKLch）

| 角色 | 值 | 说明 |
|------|-----|------|
| bg | `oklch(99% 0.005 250)` | 极浅冷白 |
| surface | `oklch(97% 0.008 250)` | 微灰卡片面 |
| fg | `oklch(18% 0.02 250)` | 近黑深蓝 |
| muted | `oklch(50% 0.015 250)` | 中性灰文字 |
| border | `oklch(90% 0.008 250)` | 浅灰线 |
| accent | `oklch(45% 0.12 255)` | 深蓝（权威） |

### 字体栈

- **display**: 'SF Pro Display', -apple-system, 'Microsoft YaHei', sans-serif
- **body**: 'SF Pro Text', -apple-system, 'Microsoft YaHei', sans-serif
- **mono**: 'SF Mono', 'JetBrains Mono', ui-monospace, monospace

### Posture 规则

1. 留白 ≥ 55%，标题与正文字号比 ≥ 2:1
2. 零阴影、零渐变——仅用 1px 细线和间距建立层次
3. 单一 accent 色，每页使用不超过 2 处
4. 数据图表用灰度 + 单色强调，禁止彩虹色
5. 每页一个核心论点，结论放标题位

---

## D2. 科技极简 — "Chrome 消失，内容浮现"

| 属性 | 值 |
|------|-----|
| **一句话** | Linear/Vercel 式的精确与克制，系统字体、近灰色板、一抹饱和强调 |
| **绑定哲学** | 08 Notion 功能性极简 |
| **默认 Token** | linear-app |
| **适用场景** | 产品介绍、技术方案、工程评审、SaaS pitch |

### 色板（OKLch）

| 角色 | 值 | 说明 |
|------|-----|------|
| bg | `oklch(99% 0.002 240)` | 几乎纯白 |
| surface | `oklch(100% 0 0)` | 纯白 |
| fg | `oklch(18% 0.012 250)` | 冷黑 |
| muted | `oklch(54% 0.012 250)` | 中灰 |
| border | `oklch(92% 0.005 250)` | 发丝线 |
| accent | `oklch(58% 0.18 255)` | 钴蓝 |

### 字体栈

- **display**: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', sans-serif
- **body**: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', sans-serif
- **mono**: 'JetBrains Mono', 'IBM Plex Mono', ui-monospace, monospace

### Posture 规则

1. 标题 letter-spacing: -0.02em，正文 0
2. 发丝边框（1px）、无阴影（dropdown/modal 例外）
3. 数字用 tabular-nums，代码/ID 用 mono
4. 一个 accent：仅用于链接 + 主 CTA，绝不用于装饰
5. 内容驱动布局，不用 hero 插图

---

## D3. 温暖人文 — "有温度的专业"

| 属性 | 值 |
|------|-----|
| **一句话** | 奶油底色、衬线标题、柔和圆角——像一本精心设计的杂志 |
| **绑定哲学** | 12 Takram 东方设计思维 |
| **默认 Token** | warm-editorial |
| **适用场景** | 培训材料、文化演示、设计思维工作坊、人文叙事、品牌故事 |

### 色板（OKLch）

| 角色 | 值 | 说明 |
|------|-----|------|
| bg | `oklch(97% 0.018 70)` | 暖奶油 |
| surface | `oklch(99% 0.008 70)` | 浅奶白 |
| fg | `oklch(22% 0.02 50)` | 墨棕 |
| muted | `oklch(50% 0.018 50)` | 暖灰 |
| border | `oklch(90% 0.014 70)` | 米色线 |
| accent | `oklch(58% 0.14 30)` | 赤陶/暖砖红 |

### 字体栈

- **display**: 'Iowan Old Style', 'Charter', 'Noto Serif SC', Georgia, serif
- **body**: -apple-system, 'Microsoft YaHei', system-ui, sans-serif
- **mono**: 'IBM Plex Mono', ui-monospace, monospace

### Posture 规则

1. 衬线标题 + 无衬线正文——温暖又不失可读性
2. 圆角 12-16px，内容卡片无直角
3. Accent 仅用于一处 CTA + 一处编辑点缀（引号、统计数字）
4. 柔和内发光替代阴影
5. 避免图标堆砌——用真实照片/插图代替

---

## D4. 数据密集 — "每平方英寸都是信息"

| 属性 | 值 |
|------|-----|
| **一句话** | Datadog/GitHub 式的工程师友好界面，等宽字体、网格、信号色 |
| **绑定哲学** | 02 Fathom 数据叙事 + 04 Tufte 数据真实 |
| **默认 Token** | posthog |
| **适用场景** | 数据分析报告、运营仪表板、技术监控、财务复盘 |

### 色板（OKLch）

| 角色 | 值 | 说明 |
|------|-----|------|
| bg | `oklch(98% 0.005 250)` | 冷白 |
| surface | `oklch(100% 0 0)` | 纯白 |
| fg | `oklch(22% 0.02 240)` | 深墨 |
| muted | `oklch(50% 0.018 240)` | 中灰 |
| border | `oklch(90% 0.008 240)` | 结构线 |
| accent | `oklch(58% 0.16 145)` | 信号绿 |

### 字体栈

- **display**: 'Inter', -apple-system, 'Segoe UI', sans-serif
- **body**: 'Inter', -apple-system, 'Segoe UI', sans-serif
- **mono**: 'JetBrains Mono', 'IBM Plex Mono', ui-monospace, Menlo, monospace

### Posture 规则

1. sans 统一（一个字体家族贯穿），mono 用于数字/代码/ID
2. tabular-nums 无处不在
3. 密集表格用 1px 线、无行条纹
4. 状态胶囊（绿/黄/红）用低饱和背景色
5. 禁止：hero 图片、大标题、营销文案——展示产品/数据本身

---

## D5. 实验先锋 — "规则存在是为了被打破"

| 属性 | 值 |
|------|-----|
| **一句话** | Are.na/Yale 式的粗犷美学——大字体、可见网格、蓄意的不完美即自信 |
| **绑定哲学** | 06 Sagmeister 表现性字体 + 11 Atelier Olschinsky 数字拼贴 |
| **默认 Token** | wired |
| **适用场景** | 创意机构提案、艺术/文化活动、品牌探索、设计宣言 |

### 色板（OKLch）

| 角色 | 值 | 说明 |
|------|-----|------|
| bg | `oklch(96% 0.004 100)` | 打印纸白 |
| surface | `oklch(100% 0 0)` | 纯白 |
| fg | `oklch(15% 0.02 100)` | 浓墨 |
| muted | `oklch(40% 0.02 100)` | 深灰 |
| border | `oklch(15% 0.02 100)` | 与 fg 同色（满强度） |
| accent | `oklch(60% 0.22 25)` | 热红 |

### 字体栈

- **display**: 'Times New Roman', 'Iowan Old Style', Georgia, serif
- **body**: ui-monospace, 'IBM Plex Mono', Menlo, monospace
- **mono**: ui-monospace, 'IBM Plex Mono', Menlo, monospace

### Posture 规则

1. 标题 = 衬线超大号（clamp(60px, 10vw, 160px)），故意占据
2. 正文 = 等宽体——是的，等宽作为正文，刻意如此
3. 边框用满强度 fg（1.5-2px），不是柔和灰
4. 非对称布局：70%:30% 分栏
5. 近乎零圆角（0-2px）、无阴影、无渐变

---

## D6. 东方意韵 — "空非虚无，是蓄势的容器"

| 属性 | 值 |
|------|-----|
| **一句话** | Kenya Hara 无印良品哲学——极致留白、最少文字、每页如一幅水墨 |
| **绑定哲学** | 13 Kenya Hara 虚空即充盈 |
| **默认 Token** | default |
| **适用场景** | 哲学/思想领导力、奢侈品叙事、年度总结、冥想型演示、跨文化场景 |

### 色板（OKLch）

| 角色 | 值 | 说明 |
|------|-----|------|
| bg | `oklch(100% 0 0)` | 纯白（白即画布） |
| surface | `oklch(98% 0.006 80)` | 微暖白 |
| fg | `oklch(28% 0.015 60)` | 暖深灰（非纯黑） |
| muted | `oklch(55% 0.01 60)` | 淡墨 |
| border | `oklch(92% 0.008 80)` | 若有若无 |
| accent | `oklch(48% 0.08 160)` | 苔藓绿 |

### 字体栈

- **display**: 'Noto Serif SC', 'Source Han Serif', 'STSong', serif
- **body**: 'Microsoft YaHei', -apple-system, sans-serif
- **mono**: 'IBM Plex Mono', ui-monospace, monospace

### Posture 规则

1. 留白 ≥ 70%，每页最多 15-20 个词
2. 巨大边距（120px+ 四边）
3. 每页最多一个视觉元素——"颜色是事件，不是常态"
4. 仅通过字重差异（300 vs 700）建立层次，不用颜色区分
5. 禁止：图标、装饰、渐变、任何"吸引注意力"的元素

---


---

## 快速选择矩阵

| 如果用户说… | 推荐方向 |
|-------------|---------|
| "高端/商务/严肃/给老板看" | D1 商务克制 |
| "科技/极简/干净/产品" | D2 科技极简 |
| "温暖/有温度/文化/人文" | D3 温暖人文 |
| "数据/图表/密集/分析" | D4 数据密集 |
| "大胆/创意/先锋/不一样" | D5 实验先锋 |
| "留白/禅意/东方/哲学" | D6 东方意韵 |
| 无明确偏好 | 默认 D2 科技极简 |
