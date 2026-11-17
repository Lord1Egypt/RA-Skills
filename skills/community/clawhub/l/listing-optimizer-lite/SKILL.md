---
name: listing-optimizer-lite
display_name: Listing Optimizer Lite
description: 电商Listing优化工具（免费 Lite 版）— 快速生成亚马逊/Shopee/Lazada/独立站的专业标题、卖点、描述和后端关键词，提升搜索排名与转化率。
version: 1.0.0
category: e-commerce
tags:
  - 电商
  - 亚马逊
  - Shopify
  - SEO
  - 产品描述
  - 跨境电商
agent_created: true
language: zh-CN
---

# Listing Optimizer Lite — 电商 Listing 优化 Skill

快速优化亚马逊、Shopee、Lazada、独立站等平台的商品 Listing（标题、卖点、描述、关键词）。**免费 Lite 版**，开箱即用。

---

## 🚀 新手 30 秒入门

**这个 Skill 是干什么的？** 把产品信息丢过来 → AI 帮你写出专业的商品标题、卖点、描述和搜索关键词。

**怎么开始？** 直接复制下面任意一句替换 [ ] 里的内容发送：

```
✅ "优化这个 Listing：无线蓝牙耳机，主动降噪，30小时续航"
✅ "写个美妆刷的产品描述，平台Shopee，市场东南亚"
✅ "帮我生成亚马逊后端关键词：Yoga Mat 183cm x 61cm 防滑"
✅ "优化标题：运动水壶 500ml 不锈钢 保温12小时"
```

**什么也不用学，把你的产品告诉我，我就能帮你优化。**

---

## 适用场景

| 场景 | 说明 |
|------|------|
| 上新品前需要写优质 Listing | 不知道怎么拼标题/卖点/关键词，让 AI 帮你搭框架 |
| 现有 Listing 转化率偏低 | 文案不够吸引人，重新优化提升搜索排名 |
| 跨平台铺货（亚马逊→Shopee） | 不同平台标题长度、关键词策略不一样，一键适配 |
| 广告投放前优化关键词 | 提取高搜索量、高相关度的后端搜索词 |

---

## 能力边界说明

### ✅ 擅长做的事情

1. **产品标题优化** — 按亚马逊/Shopee/Lazada/独立站的平台规则生成 SEO 标题
2. **五点卖点生成** — 利益驱动式卖点，自然融入关键词，按重要度排序
3. **产品描述撰写** — 结构化品牌故事+卖点展开+使用场景
4. **后端搜索词提取** — 覆盖核心词+属性词+场景词+同义词+长尾词
5. **多平台适配** — 自动匹配各平台的标题长度、emoji 规则、关键词策略
6. **竞品高频词分析** — 如提供竞品 ASIN/链接，可提取相关高频词用于优化

### ⚠️ 需要你提供素材才能做

1. **品牌已有文案的页面风格分析** — 需要提供品牌官网或历史 Listing
2. **和竞品做精准差异对比** — 需要提供竞品 ASIN 或链接
3. **多语言翻译** — 基础英文没问题；小语种（印尼语、泰语等）建议专业审校
4. **基于图片的卖点提取** — 需要你描述图片内容或提供文字描述

### ❌ 超出能力范围（附替代方案）

1. **批量处理上百个产品** → Lite 版单次只支持一个产品；建议使用 Pro 版
2. **生成产品图片/A+ 图文内容** → 用 Canva / Photoshop 等设计工具
3. **保证排名/转化率数据** → 用 SellerSprite / Helium10 等工具实测
4. **处理真实的品牌/账户数据** → 本工具不做持久化存储，不登录你的卖家账号
5. **做 VAT / 海关合规咨询** → 找专业跨境税务顾问

---

## 触发方式

在对话中发送以下任一指令即可：

### 主触发词

- "优化这个 Listing：[产品信息]"
- "Optimize this listing：[product info]"
- "帮我写 Listing：[产品信息]"

### 子功能触发

| 功能 | 触发词 | 说明 |
|------|--------|------|
| 标题优化 | "优化标题：[产品信息]" | 只看标题，不生成卖点/描述 |
| 卖点生成 | "写卖点：[产品信息]" | 只看五点卖点 |
| 描述撰写 | "写产品描述：[产品信息]" | 只写产品描述段落 |
| 关键词提取 | "生成关键词：[产品信息]" | 只提取后端搜索词 |
| 跨平台适配 | "从亚马逊转 Shopee：[亚马逊 Listing]" | 平台间格式转换 |

**判断逻辑：** 如果用户没有指定子功能，默认输出完整优化（标题+卖点+描述+关键词）。

---

## 输入格式

输入越详细，优化质量越高。以下为最佳输入模板：

| 字段 | 必填 | 说明 | 示例 |
|------|------|------|------|
| 产品名称 | ✅ | 品名（中英文均可） | 无线蓝牙耳机 |
| 核心卖点 | ❌ | 3-5 个特点 | 主动降噪、30h续航、IPX5防水 |
| 目标平台 | ❌ | 默认亚马逊 | Amazon / Shopee / Lazada / 独立站 |
| 目标市场 | ❌ | 默认美国 | 美国/欧洲/东南亚/日本/国内 |
| 竞品参考 | ❌ | 1-3 个 ASIN 或链接 | B0XXXXXXXX |
| 价格区间 | ❌ | 定价 | $29.99 |
| 品牌名称 | ❌ | 品牌名 | Anker / 小米 |

---

## 输出格式

每次输出按以下统一格式呈现：

━━━ 📋 Listing 优化结果 ━━━

📌 优化标题
[按平台公式优化后的标题]

📌 五点卖点
• [卖点1 — 以核心利益开头的短句]
• [卖点2]
• [卖点3]
• [卖点4]
• [卖点5]

📌 产品描述
[段落化描述，首段品牌→中段优势→尾段保障]

📌 后端搜索词
[空格分隔的关键词列表，按搜索量/相关性排序]

📌 优化说明
• 改动要点：[本次改动概述]
• 建议：[额外优化建议或注意事项]
━━━━━━━━━━━━━━━━━━━━━━━━

---

## 优化规则（系统指令）

### 标题优化规则

**亚马逊公式：** 品牌 + 核心关键词 + 特性词 + 尺寸/颜色/型号 + 包装数量
- 严格 ≤ 200 字符，首字母大写（介词/连词小写）
- ❌ 禁止：价格、促销语、emoji、HTML 标签、全大写单词
- 核心搜索词务必放在标题前 80 字符内
- 每个标题包含至少 2-3 个高搜索量关键词

**Shopee 公式：** 核心关键词 + 卖点词 + 属性词 + 场景词
- 严格 ≤ 60 字符（移动端截断点约 60）
- ✅ 可含 1-2 个 emoji（建议放在开头或末尾）
- ❌ 禁止：价格、促销语在标题中

**Lazada 公式：** 品牌（如有）+ 核心关键词 + 属性词 + 卖点
- 严格 ≤ 80 字符
- ❌ 避免重复词和关键词堆砌
- ✅ 品牌词可出现在开头

### 五点卖点规则

1. **每条 80-150 字符**，按对用户重要的程度降序排列
2. **每句以核心利益/价值开头**，后跟特性支撑
   - ✅ "Enjoy crystal-clear calls with advanced noise cancellation technology"
   - ❌ "This product has noise cancellation"
3. **使用主动语态、动词开头**（Experience / Enjoy / Get / Feel）
4. **自然融入 1-2 个目标关键词**，不堆砌
5. **覆盖逻辑链：**
   - 卖点1：核心功能 → 解决什么痛点
   - 卖点2：关键参数 → 比竞品好在哪里
   - 卖点3：使用场景 → 什么时候用
   - 卖点4：差异化 → 别人没有你有的
   - 卖点5：售后/保障 → 买了放心

### 产品描述规则

- **首段（品牌故事）：** 2-3 句，定位产品在品类的价值
- **中段（优势展开）：** 3-5 条，每条 1-2 句，展开核心卖点
- **尾段（场景+人群+保障）：** 2-3 句，谁说适合什么时候用，售后政策
- **语气：** 专业、热情但不过度夸张
- ✅ 自然融入 3-5 个 LSI 关键词（相关但不重复的变体）
- ❌ 禁止：虚假承诺（"销量第一"无数据支撑）、过度夸张用语

### 后端搜索词规则

- **提取来源：** 核心词 + 属性词 + 场景词 + 用途词 + 同义词 + 长尾词
- **排序：** 按搜索量推测 → 找高频词优先，长尾词次之
- ❌ 排除：品牌无关词、不准确描述、已被标题覆盖的重复词根
- ❌ 不重复词根（亚马逊系统忽略重复，浪费字符）
- **亚马逊美国站限制：** ≤ 250 字节（约 250 个英文字符）

### 错误/异常处理规则

1. **用户输入信息不足时：**
   - 先基于已有信息生成一个"假设版本"给用户看
   - 再问："如果你想调整，可以告诉我产品卖点/目标市场等信息"
   - ❌ 禁止：直接回复"信息不足，请补充"
2. **用户请求超出范围时：**
   - 先告诉用户这个做不到
   - 再推荐替代工具或方法
3. **不确定的领域：**
   - ❌ 禁止编造数据、政策解读
   - ✅ 注明"这是基于通用规则的优化建议，建议核对平台最新政策"

---

## 平台规范速查表

| 项目 | 亚马逊 | Shopee | Lazada | 独立站 |
|------|--------|--------|--------|--------|
| 标题最大长度 | 200 字符 | 60 字符 | 80 字符 | 不限 |
| 允许 emoji | ❌ 禁止 | ✅ 1-2 个 | ❌ 不建议 | ✅ 根据品牌调性 |
| 价格/促销语 | ❌ 禁止 | ❌ 不建议标题 | ❌ 不建议标题 | ✅ 可含 |
| Bullet Points 限制 | ≤ 500 字符/条 | 自然分布 | 自然分布 | 不限 |
| Description 限制 | ≤ 2000 字符 | 不限 | 建议 300-500 字 | 不限 |
| 后端关键词 | ≤ 250 字节 | 标题中自然分布 | 标题中自然分布 | SEO 插件配置 |

---

## 工作流程（AI 执行）

1. **接收信息** → 确认产品名称、平台、市场、产品类型
2. **分析竞品**（如提供）→ 提取标题高频词、卖点模式
3. **生成标题** → 按目标平台公式 + SEO 规则
4. **生成卖点** → 利益驱动 + 关键词自然融入
5. **生成描述** → 结构化品牌故事 + 卖点展开
6. **提取关键词** → 覆盖核心 + 长尾 + 场景词，排除重复词根
7. **输出结果** → 按标准格式呈现 + 优化说明

---

## 受众说明

| 用户类型 | 如何使用 |
|---------|---------|
| **跨境电商卖家（个人/小团队）** | 直接丢产品信息，30 秒拿到优化版 Listing |
| **运营/文案专员** | 作为初稿生成器，拿到后再做二次润色 |
| **创业者（刚起步）** | 不用学任何规则，把产品描述给我即可 |
| **已有大卖家账号的资深运营** | 用高级输入（竞品 ASIN+价格区间）获取更精准优化 |

---

## 定制化使用指南

可以在指令中附加以下参数：

- **语气偏好：** "专业风格" / "活泼一点" / "简洁版"
- **关键词倾向：** "重点突出 waterproof"
- **长度控制：** "标题要短一点" / "卖点写细一点"
- **竞品参考：** "参考 A 品牌的写法" → 需提供 ASIN/链接

示例：
```
"优化标题：运动水壶，要活泼一点的语气，突出便携"
"写个蓝牙音箱的描述，简洁版，重点放在音质和续航"
```

---

## 常见问题 FAQ

**Q1：这个工具免费吗？能用多久？**
完全免费，Lite 版无使用次数限制。每次只优化一个产品。

**Q2：生成的内容直接上架到平台会被封号吗？**
优化建议符合行业通用规则，但建议你核对目标平台的最新政策。尤其注意亚马逊的重复内容政策，不同卖家的同款产品建议差异化措辞。

**Q3：Lite 版和 Pro 版有什么区别？**
Pro 版（规划中）支持批量优化、图片/A+ 内容生成、多语言翻译、关键词搜索量数据接入。

**Q4：支持中文产品优化吗？**
支持。中文输入 → 生成中文 Listing；中文输入 + 目标市场 US → 自动翻译为英文，按美国站规则优化。

**Q5：输入了竞品 ASIN 后，数据安全吗？**
所有信息仅在本次对话中处理，不会存储到数据库，也不会用于训练其他模型。

**Q6：如果我给的卖点不够详细怎么办？**
AI 会先基于产品名称推断 3-5 个合理的卖点方向生成假设版本给你看，然后问你是否需要调整。不会盲目等你补充。

**Q7：优化结果是百分百正确的吗？**
AI 生成的内容基于通用规则，建议你在各平台上传前人工核对一遍，尤其注意：
- 定价/促销信息是否准确
- 品牌名称、型号等事实性信息
- 各平台最新标题字符上限变化

**Q8：同一款产品在不同平台应该用不同的关键词吗？**
是的。亚马逊更关注标题+后端搜索词的覆盖率，Shopee 受限于短标题建议在描述中补关键词，Lazada 同 Shopee 逻辑。

---

## 注意事项

- **数据安全：** 所有输入信息只在当前对话上下文处理，不会持久化存储到数据库或用于模型训练
- **合规性：** 生成内容需用户自行核对各平台最新政策；本工具不构成法律或合规建议
- **Lite 版限制：** 单次优化一个产品；不支持批量；不支持图片/A+ 内容；不支持搜索量数据回填
- **版权声明：** 生成的文案如有版权纠纷，归用户自行修改后使用；AI 输出不享有版权

---

## 使用示例

### 示例 1：亚马逊美国站

**用户输入：**
```
产品：Wireless Bluetooth Earbuds
卖点：Active Noise Cancellation, 30hr battery, IPX5 waterproof, ergonomic fit
平台：Amazon
市场：US
```

**AI 输出：**
```
━━━ 📋 Listing 优化结果 ━━━

📌 优化标题
[Brand] Wireless Bluetooth Earbuds, Active Noise Cancelling 30Hr Playtime IPX5 Waterproof Ergonomic In-Ear Headphones with Mic

📌 五点卖点
• Immerse in Pure Sound — Advanced active noise cancellation technology blocks out background noise for crystal-clear audio in any environment
• All-Day Power — Enjoy up to 30 hours of non-stop playback on a single charge, with quick USB-C charging for when you're on the go
• Built for Any Adventure — IPX5 waterproof rating protects against sweat, rain, and splashes, making these the perfect workout companion
• Custom Comfort Fit — Ergonomic in-ear design with 3 sizes of silicone ear tips ensures a secure and comfortable fit for all-day wear
• Stay Connected — Built-in high-sensitivity microphone delivers clear hands-free calls, with one-touch control for music and calls

📌 产品描述
Experience audio freedom like never before with our Wireless Bluetooth Earbuds. Designed for those who demand both performance and comfort, these earbuds deliver premium sound quality in a compact, stylish form factor that fits your active lifestyle. Whether you're commuting, working out, or simply relaxing at home, every note comes through with stunning clarity.

Equipped with industry-leading active noise cancellation, these earbuds create your personal sound sanctuary wherever you go. The powerful 30-hour battery life means less charging and more listening, while IPX5 waterproof construction ensures they can handle whatever your day throws at them. The ergonomic design, paired with multiple ear tip sizes, provides a custom fit that stays secure during even the most intense workouts.

Perfect for travelers, fitness enthusiasts, and music lovers alike, these wireless earbuds are your ideal audio companion. Backed by our satisfaction guarantee and responsive customer support, you can buy with confidence knowing we stand behind our product.

📌 后端搜索词
wireless earphones bluetooth 5.3 noise isolating earbuds sport headphones running gym workout waterproof earbuds long battery life true wireless earbuds hands-free earbuds with microphone compact earbuds travel earphones sweatproof earbuds

📌 优化说明
• 改动要点：标题加入品牌位和型号空间；卖点转为利益驱动句式；描述三段式结构；关键词覆盖同义词和场景词
• 建议：请将 [Brand] 替换为实际品牌名；上传前确认平台 bullet point 字数是否超标（长版建议控制在 150 字符内）
```

### 示例 2：Shopee 东南亚站

**用户输入：**
```
产品：瑜伽垫 183cm x 61cm
卖点：防滑 TPE 材质、环保无毒、附捆绑带
平台：Shopee
市场：东南亚
```

**AI 输出**（略，参照输出格式）。

---

## 版本与许可

- **当前版本：** v1.0.0（免费 Lite 版）
- **许可协议：** MIT — 可自由使用、修改、分发
- **Pro 版路线图：** 批量优化 / A+ 内容生成 / 多语言翻译 / 关键词搜索量数据
- **反馈渠道：** GitHub Issues 或 ClawHub 评论区

---

*Listing Optimizer Lite — 免费开源，让每个卖家都能写出专业 Listing。*
