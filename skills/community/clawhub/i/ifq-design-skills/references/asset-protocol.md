# 核心资产协议（Asset Protocol）

> **触发条件**：任务涉及具体品牌——用户提了产品名 / 公司名 / 明确客户（Stripe、Linear、Anthropic、Notion、Lovart、DJI、自家公司等），不论用户是否主动提供了品牌资料。
>
> **前置硬条件**：先执行本文件的事实验证与官方来源核对，确认品牌 / 产品存在且状态已知，再走资产采集流程。

这是 v1 最核心的约束，也是稳定性的生命线。Agent 是否走通这个协议，直接决定输出质量是 40 分还是 90 分。不要跳过任何一步。

## 核心理念：资产 > 规范

**品牌的本质是「它被认出来」**。识别度按以下顺序贡献：

| 资产 | 识别度 | 必需性 |
|---|---|---|
| **Logo** | 最高 | 任何品牌必须有 |
| **产品图 / 渲染图** | 极高 | 实体产品必须有 |
| **UI 截图 / 界面素材** | 极高 | 数字产品必须有 |
| **色值** | 中 | 辅助 |
| **字体** | 低 | 辅助 |
| **气质关键词** | 低 | agent 自检用 |

**翻译成执行规则**：
- 只抽色值 + 字体、不找 logo / 产品图 / UI → **违反本协议**
- 用 CSS 剪影 / SVG 手画替代真实产品图 → **违反本协议**（生成的就是「通用科技动画」，任何品牌都长一样）
- 找不到资产不告诉用户、也不 AI 生成，硬做 → **违反本协议**

宁可停下问用户要素材，也不要用 generic 填充。

## 5 步硬流程

### Step 1 · 问（资产清单一次问全）

```
关于 <brand/product>，你手上有以下哪些资料？我按优先级列：
1. Logo（SVG / 高清 PNG）—— 任何品牌必备
2. 产品图 / 官方渲染图 —— 实体产品必备
3. UI 截图 / 界面素材 —— 数字产品必备
4. 色值清单（HEX / RGB / 品牌色盘）
5. 字体清单（Display / Body）
6. Brand guidelines PDF / Figma design system / 品牌官网链接

有的直接发我，没有的我去搜 / 抓 / 生成。
```

### Step 2 · 搜官方渠道

| 资产 | 搜索路径 |
|---|---|
| **Logo** | `<brand>.com/brand` · `/press` · `/press-kit` · `brand.<brand>.com` · 官网 header inline SVG |
| **产品图** | `<brand>.com/<product>` 详情页 hero + gallery · 官方 YouTube launch film 截帧 · 新闻稿附图 |
| **UI 截图** | App Store / Google Play 截图 · 官网 screenshots section · 演示视频截帧 |
| **色值** | 官网 inline CSS / Tailwind config / brand guidelines PDF |
| **字体** | 官网 `<link rel="stylesheet">` 引用 · Google Fonts 追踪 · brand guidelines |

兜底搜索关键词：
- `<brand> logo download SVG`、`<brand> press kit`
- `<brand> <product> official renders`、`<brand> <product> product photography`
- `<brand> app screenshots`、`<brand> dashboard UI`

### Step 3 · 下载资产

**3.1 Logo**

1. 独立 SVG/PNG 文件：`curl -o assets/<brand>-brand/logo.svg https://<brand>.com/logo.svg`
2. 官网 HTML 全文提取 inline SVG（80% 场景必用）：`curl -A "Mozilla/5.0" -L https://<brand>.com -o assets/<brand>-brand/homepage.html` 然后 grep `<svg>...</svg>`
3. 官方社交媒体 avatar（最后手段）

**3.2 产品图（实体产品必需）**

1. 官方产品页 hero image（最高优先级，2000px+）
2. 官方 press kit
3. 官方 launch video 截帧（`yt-dlp` + `ffmpeg`）
4. Wikimedia Commons
5. AI 生成兜底（nano-banana-pro，以真实产品图为参考）。**不要用 CSS/SVG 手画代替**

**3.3 UI 截图（数字产品必需）**

App Store / Google Play 截图（注意：可能是 mockup） · 官网 screenshots · 演示视频截帧 · 用户账号截屏。

### Step 3.4 · 素材质量门槛「5-10-2-8」原则（铁律）

> **Logo 例外**：Logo 有就必须用，没有就停下问用户。其他素材（产品图 / UI / 参考图 / 配图）走「5-10-2-8」。

| 维度 | 标准 | 反模式 |
|---|---|---|
| 5 轮搜索 | 多渠道交叉搜 | 第一页结果直接用 |
| 10 个候选 | 至少凑 10 个备选才开始筛 | 只抓 2 个，没得选 |
| 选 2 个好的 | 从 10 个里精选 2 个 | 全都用 = 视觉过载 |
| 每个 8/10 分以上 | 不够 8 分宁可不用，用诚实 placeholder 或 nano-banana-pro 生成 | 凑数 7 分素材进 brand-spec.md |

**8/10 评分维度**：
1. **分辨率** ≥ 2000px（印刷 / 大屏 ≥ 3000px）
2. **版权清晰度** — 官方 > 公共领域 > 免费素材 > 疑似盗图（疑似盗图直接 0 分）
3. **品牌气质契合度** — 与 brand-spec.md 的「气质关键词」一致
4. **光线 / 构图 / 风格一致性** — 2 个素材放一起不打架
5. **独立叙事能力** — 能单独表达一个叙事角色（不是装饰）

**为什么是铁律**：滥竽充数比没有更糟——污染视觉品味、传递「不专业」信号。每一个视觉元素都在积分或扣分。7 分素材 = 扣分项，不如留空。

### Step 4 · 验证 + 提取

| 资产 | 验证动作 |
|---|---|
| Logo | 文件存在 + 可打开 + 至少深底/浅底两个版本 + 透明背景 |
| 产品图 | 至少一张 2000px+ + 去背或干净背景 + 多角度 |
| UI 截图 | 真实分辨率 + 最新版本 + 无用户数据污染 |
| 色值 | `grep -hoE '#[0-9A-Fa-f]{6}' assets/<brand>-brand/*.{svg,html,css} \| sort \| uniq -c \| sort -rn \| head -20`，过滤黑白灰 |

**警惕示范品牌污染**：产品截图常有用户 demo 的品牌色（如某工具截图演示喜茶红），那不是该工具的色。同时出现两种强色时必须区分。

**品牌多切面**：同一品牌的官网营销色和产品 UI 色经常不同（Lovart 官网暖米+橙，产品 UI 是 Charcoal + Lime）。两套都是真的——根据交付场景选合适的切面。

### Step 5 · 固化为 `brand-spec.md`

```markdown
# <Brand> · Brand Spec
> 采集日期：YYYY-MM-DD
> 资产来源：<列出下载来源>
> 资产完整度：<完整 / 部分 / 推断>

## 🎯 核心资产（一等公民）

### Logo
- 主版本：`assets/<brand>-brand/logo.svg`
- 浅底反色版：`assets/<brand>-brand/logo-white.svg`
- 使用场景：<片头/片尾/角落水印/全局>
- 禁用变形：<不能拉伸/改色/加描边>

### 产品图（实体产品必填）
- 主视角：`assets/<brand>-brand/product-hero.png`（2000×1500）
- 细节图：`assets/<brand>-brand/product-detail-{1,2}.png`
- 场景图：`assets/<brand>-brand/product-scene.png`

### UI 截图（数字产品必填）
- 主页：`assets/<brand>-brand/ui-home.png`
- 核心功能：`assets/<brand>-brand/ui-feature-<name>.png`

## 🎨 辅助资产

### 色板
- Primary: #XXXXXX  <来源标注>
- Background / Ink / Accent / 禁用色

### 字型
- Display / Body / Mono

### 签名细节 / 禁区 / 气质关键词（3-5 个）
```

**写完 spec 后的执行纪律**：
- 所有 HTML 必须**引用** spec 里的资产文件路径，不允许 CSS 剪影 / SVG 手画代替
- Logo 用 `<img>` 引用真实文件，不重画
- CSS 变量从 spec 注入：`:root { --brand-primary: ...; }`，HTML 只用 `var(--brand-*)`
- 让品牌一致性从「靠自觉」变成「靠结构」

## 全流程失败的兜底

| 缺失 | 处理 |
|---|---|
| Logo 完全找不到 | **停下问用户**，不要硬做 |
| 产品图（实体）找不到 | nano-banana-pro 以官方参考为基底生成 → 向用户索取 → 诚实 placeholder（标注"产品图待补"） |
| UI 截图（数字）找不到 | 向用户索取自己账号截屏 → 官方演示视频截帧。**不用 mockup 生成器凑** |
| 色值找不到 | 进设计方向顾问模式，推荐 3 方向并标注 assumption |

**禁止**：找不到资产就静默用 CSS 剪影 / 通用渐变硬做。宁可停下问，也不要凑。

## 反例（真实踩过的坑）

- **Kimi 动画**：凭记忆猜「应该是橙色」，实际 Kimi 是 `#1783FF` 蓝色——返工
- **Lovart 设计**：把产品截图里演示品牌的喜茶红当成 Lovart 的色——差点毁整个设计
- **DJI Pocket 4 发布动画**（2026-04-20，本协议升级触发案例）：旧版只抽色值，没下载 logo 没找产品图，用 CSS 剪影代替——做出「通用黑底+橙 accent 的科技动画」，没有大疆识别度。IFQ 原话：「否则，我们在表达什么呢？」

## 成本对比

| 场景 | 时间 |
|---|---|
| 正确走完协议 | 下载 logo 5 min + 产品图 / UI 10 min + grep 色值 5 min + 写 spec 10 min = **30 分钟** |
| 不做协议的代价 | 通用动画 → 用户返工 1-2 小时甚至重做 |

**这是稳定性最便宜的投资**。
