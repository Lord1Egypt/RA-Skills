---
name: marketing-poster-recipes
version: 1.2.0
display_name: 营销海报配方库
display_name_en: Marketing Poster Recipes
author: bonniegeng-max
description: |
  做什么：营销海报配方库——从广告创意配方卡库选卡填槽，生成可直接用于小红书/朋友圈/电商的 3:4 竖版营销海报（14 张卡：超现实微观合成、超现实液体定格、极简手绘小剧场、诗意复古印刷、人物手持产品光影、Apple 极简、电商白底精修、贴纸拼贴清单、复古拼贴节日、复古美式快餐、中式市井美食、小红书家居标注、第二世界分割创意 + 头脑风暴定方向），附卖点提炼、Slogan 生成与广告红线审查。
  何时触发：用户说「给这个产品做张海报/营销图/种草图/广告创意图/营销生图」「把这张产品照片做成海报」「帮我出广告创意方案和配图」「用超现实/手绘/复古印刷风格给产品生图」「给我的产品做张小红书封面」等。液体/酱体/膏体类产品（番茄酱、蜂蜜、巧克力、咖啡、酱料、沐浴露等）要「氛围感+设计感+反重力定格」→ 优先路由到 surreal-frozen-liquid 卡。
  何时不用：NOT for：纯广告文案写作（无出图需求，直接用 references/copywriting-prompts.md 的模板即可）、漫画/绘本/分镜叙事创作（转 text-to-comic）、反推参考图风格建风格卡（转 style-card）、一次性 prompt 润色、生成视频/动图（即梦路径，本 skill 不覆盖）。
  依赖：ImageGen 生图工具（约 5-10 积分/张，生成前必须告知用户并确认）；图生图类卡（hand-drawn-theater / retro-print-poem）需用户上传产品照片。
  降级：生图工具不可用或用户不想耗积分时，输出「选卡建议 + 填好槽的完整 prompt」，供用户手动投喂豆包/即梦等工具，效果等价。
description_zh: 从广告创意配方卡库选卡填槽，生成可直接用于小红书/朋友圈/电商的 3:4 竖版营销海报，附卖点提炼、Slogan 生成与广告红线审查。
description_en: Pick a recipe card from the ad-creative library, fill the slots, and generate 3:4 vertical marketing posters for social media and e-commerce, with selling-point extraction, slogan generation, and ad-compliance review.
---

# Marketing Poster Recipes · 营销海报配方库

**目标**：输入产品信息或照片，按配方卡生成一张过验收的 3:4 竖版营销海报（或交付等价的填槽 prompt）。

**核心信仰**：配方卡是唯一事实源——每张卡沉淀一套经过实测的广告创意方法论（视觉公式 + 槽位 + 负面清单），选对卡、填对槽，生成结果就不会跑偏。

## 使用边界

- **做**：产品营销海报、种草图、广告创意方案（文字）+ 配图、小红书/朋友圈竖版营销图
- **不做**：漫画叙事（text-to-comic 管辖）、风格反推（style-card 管辖）、视频生成、画面内精确文字排版（AI 文字不可靠，配方统一留白 20-30% 给后期）
- **红线**：卖点含数字/材质/功效且用户给不出出处 → 不写入广告语文案，标「待确认」（AI 写广告最大风险是"写得太顺"，不是写不好）

## 目录结构（按需加载，不要一次读全部）

```
marketing-poster-recipes/
├── SKILL.md                  # 本文件（工作流地图，每次必读）
├── library/
│   ├── INDEX.md              # 配方卡索引（选卡前必读）
│   └── cards/*.md            # 14 张配方卡正文（选哪张读哪张）
├── references/
│   ├── marketing-method.md   # 广告方法论：三要素/卖点体检/记忆点三问/验收标准（生成后验收必读）
│   ├── copywriting-prompts.md# Day1 六段文案 prompt 模板（补槽/Slogan/红线审查时读）
│   ├── patterns.md           # 9 个创意模式（画面没想法时读）
│   └── repair-recipes.md     # 水印/乱码/废稿修复三套 SOP（v0.2.0 新增，验收修复时读）
├── gotchas.md                # 实战坑清单（生成前必读，发现新坑回写）
└── assets/                   # 案例参考图（验收参照物）
```

**铁律**：`library/cards/` 是唯一事实源，INDEX.md 是派生索引——改卡必须同步改索引。

## 工作流

### Step 1 · 输入检查（判断走哪条路）

| 用户给了什么 | 路径 |
|---|---|
| 产品照片 + 卖点 | → Step 2 直接选卡（图生图类） |
| 产品信息文本（名称/品类/卖点/主色） | → Step 2 直接选卡（文生图类） |
| 只有模糊想法 / 画面方向不清 | → 先跑 `brainstorm-12` 卡出 12 套创意方案，用户挑 1 套再进 Step 2 |

**缺槽处理**：产品四槽（名称/品类/一句话卖点/主色）缺项时，用 `references/copywriting-prompts.md` 的「Brief 解读」+「卖点提炼」模板帮用户补齐；**核心卖点只留一个**（多卖点混搭是超现实卡的明确禁项）。

### Step 2 · 选卡（决策树）

1. 有产品照片？
   - 有（图生图类）→ `hand-drawn-theater`（要可爱互动感）/ `retro-print-poem`（要高级复古感）/ `second-world-split`（要创意型格款）/ `xhs-home-annotate`（小红书家居笔记标注）/ `ecomm-white-bg`（电商白底精修主图）/ `retro-collage-holiday`（节日礼物拼贴）
   - 无（文生图类）→ `surreal-micro-world`（要创意冲击/脑洞·尺度反差）/ `surreal-frozen-liquid`（要氛围感/设计感·液体定格）/ `product-in-hand`（要时尚大片感）/ `apple-minimal`（要发布会级极简）/ `sticker-collage`（清单式种草）/ `retro-diner-food`（复古美式快餐）/ `chinese-street-food`（中式市井烟火气）
2. 卖点抽象（轻/快/滑/治愈）？→ 建议视觉比喻思路（见 patterns.md P4）；痛点清晰可放大？→ 建议痛点放大（P3），配 `surreal-micro-world`
3. 用户指定风格关键词 → 直接路由到对应卡；两张卡拿不准 → 展示 INDEX.md 的对比说明让用户选
4. 画面方向完全不清 → 先跑 `brainstorm-12` 出 12 套方案，用户挑 1 套再选卡

### Step 3 · 填槽生成

1. 读所选卡全文，按卡内槽位表逐项与用户确认（或从输入继承）
2. 卖点含数字/功效 → 先过红线：无出处不进广告语
3. **告知用户约 5-10 积分/张，确认后再生成**（ImageGen）
4. 图生图卡必须先拿到用户照片本体；用户没照片 → 换文生图卡或请用户补照片，**不要凭描述硬生成**
5. 批量需求 >5 张 → 提醒分批，避免积分浪费

### Step 4 · 验收（不过不交付）

1. 逐项过卡内【禁止】段（文字水印/产品变形/面部崩坏/多光源/比例混乱…）
2. 过**记忆点三问**（见 references/marketing-method.md）：能描述出来吗？隔一天还记得吗？愿意讲给朋友听吗？——只是"看着好看"但说不出在讲什么 = 不合格
3. 完整海报三件套检查：**图 + 广告语 + 产品名**（广告语可用 copywriting-prompts.md 的 Slogan 模板生成，发布前过红线审查模板）
4. **引擎水印修复（内置步骤，v0.2.0 起）**（跨引擎共性，混元/豆包右下角均有「AI生成」水印，图生图场景为**半透明白色字**——深色像素检测扫不到，先目视放大图定位）：按 `references/repair-recipes.md` 的三套 SOP 修复，修复+复验通过才算可交付成品；云端图像处理授权不可用时直接走本地 Pillow SOP（免积分）。修复过程新踩的坑同样回写 gotchas
5. 结果明显偏离卡规范 → 按负面清单定向重生成，**至多重试 2 次，第 3 次转用户人工判断**
6. 每次生成后把新踩的坑回写 `gotchas.md`

## 输出契约

- 交付物：3:4 竖版海报 PNG（或降级时：所选卡名 + 填好槽的完整 prompt 文本）
- 附带：所用配方卡名 + 填槽后 prompt 全文（便于复用与手动重投）
- 命名：`海报-{产品名}-{卡名}-{日期}.png`
- 汇报必含：验收三项结果（负面清单/记忆点三问/三件套）+ **水印检查结果** + 积分消耗

## 异常处理

| 异常 | 处理 |
|---|---|
| ImageGen 不可用/积分不足 | 降级：交付填槽完成的 prompt，说明可投喂豆包/即梦，效果等价 |
| 图生图卡但无照片 | 换文生图卡，或请用户补照片（禁止凭描述硬编产品外观） |
| 生成两次仍偏离卡规范 | 第 3 次前停下来：展示两版结果+偏离点，让用户判断是改槽位还是换卡 |
| 用户要的品类是医疗/保健 | 提示合规限制：只做中性视觉，不承诺功效，广告语过红线审查 |
| 仿冒品牌 logo/明星肖像需求 | 拒绝并说明侵权风险 |
| 需求实为漫画/风格反推/纯文案 | 明确转交：text-to-comic / style-card / copywriting-prompts.md，不硬做 |

## 资源索引

| 场景 | 读什么 |
|---|---|
| 选卡 | `library/INDEX.md` → 所选卡全文 |
| 生成前 | `gotchas.md`（坑清单） |
| 生成后验收 | `references/marketing-method.md` 的「记忆点三问」段 |
| 水印/乱码/废稿修复 | `references/repair-recipes.md`（三套本地修复 SOP，v0.2.0 新增） |
| 补槽/要 Slogan/红线审查 | `references/copywriting-prompts.md` |
| 画面没想法 | `references/patterns.md`（视觉比喻/痛点放大等 9 模式） |
| 看生成效果长什么样 | `assets/` 各卡代表作（含 2 组原图→海报对照） |

## 正反触发测试

- **应触发**：「给这瓶番茄酱做张超现实风格的营销海报」→ 进入选卡（无照片·液体类产品 → surreal-frozen-liquid；若卖点可做尺度反差则 surreal-micro-world），填槽，告知积分后生成
- **不应触发**：「帮我把这段 prompt 改得好一点」→ 拒绝（一次性润色无复用价值）；「把这张图画风总结一下」→ 转 style-card

## 增量维护与发布纪律（改卡/加卡后必走）

**新配方来源**：AIGC 广告创意课程 Day3-5（预计含视频/即梦方向）。

**加卡/改卡的完整闭环（缺一不可，见 `CONTRIBUTING.md` 详细清单）**：

1. 按卡片模板萃取新卡 → 入库 `library/cards/`，同步 `INDEX.md`
2. **跑隐私闸门**（本机私有闸门脚本，隐私项 0 命中才继续）
3. bump 版本（加卡=minor +0.1，如 1.1.0 → 1.2.0；SKILL.md frontmatter + README 三处同步）
4. 本地 git commit → **push 到 GitHub**（别停在"commit 不 push"，会沉底）
5. 重新 publish ClawHub（`clawhub skill publish . --version <新版本> --changelog "..."`）
6. 打 zip 回传资料库（skill 目录外的归档节点，外层只留最新一个 zip）

**红线提醒**：skill 可能被**其它对话里的助手**改动（新增卡/改文件），改完往往**不跑闸门、不 bump、不 push**。任何一次改完，主动核查 git 状态（`git status` 是否领先 origin）与版本号是否三处一致，把漏掉的步骤补完。

## CHANGELOG

- **v1.2.0（2026-11-27 · Day3 全量合并 + 卡库 14 张定稿）**：① 并入 Day3 8 张新卡（apple-minimal / ecomm-white-bg / sticker-collage / retro-collage-holiday / retro-diner-food / chinese-street-food / xhs-home-annotate / second-world-split），卡库 6→14 张；② 保留本地原创 surreal-frozen-liquid 卡（液体反重力定格，1.1.0 新增，Day3 资料包未含）；③ 同步 references/repair-recipes.md 三套修复 SOP；④ gotchas.md 合并 Day3 8 卡全量萃取记录 + v0.2.0 动态复评段；⑤ 课程同源案例图已脱敏移除（对外发布合规）。
- **v1.1.0（2026-11-26）**：新增第 6 张卡 surreal-frozen-liquid（超现实液体定格，原创三轮迭代沉淀）；SKILL.md 补液体路由与发布纪律段。
- **v0.3.0（2026-11-26 · Day3 资料包全量萃取）**：① 8 张新卡入库（apple-minimal / ecomm-white-bg / sticker-collage / retro-collage-holiday / retro-diner-food / chinese-street-food / xhs-home-annotate / second-world-split），卡库 5→13 张，全部 prompt 原文照录 Day3 学员资料包（含官方模板/负面词/占位符的已槽位化），稳定性一律标「未知」待首测；② 10 张 Day3 案例图下载入 assets 作验收参照；③ product-in-hand 补喜茶同源参照；④ 视频类 prompt（子弹时间/发布会风）超出本库边界未入库。
- **v0.2.1（2026-11-26 · 动态复评迭代）**：① v0.2.0 定稿 prompt 实跑验证——retro 卡穿字 1/1 达标、诗句零乱码（累计 3/3）、分界线首次未出现；② 修复 SKILL.md 双 frontmatter 重叠残留；③ repair-recipes SOP 新增「bbox 四周外扩 10-15px」教训；④ gotchas 新增「v0.2.0 动态复评」段。
- **v0.2.0（2026-11-26 · P0 加固迭代，溯源 TRACE 评测 87/A）**：① retro-print-poem 主 prompt 回灌实测定稿写法（最高优先级穿字指令+反向废稿判据、三槽位必填）；② 手绘卡固化去旧水印指令；③ 新增 references/repair-recipes.md 三套废稿修复 SOP，水印处理升格为内置修复步骤；④ 补齐 frontmatter 与 CHANGELOG。
- **v0.1.x（2026-11-25 ~ 11-26 · 建库与实测期）**：5 张配方卡入库（Day1/Day2 课程萃取）；gotchas 失败模式回写体系建立；4/5 卡完成混元实测（超现实✅/手绘✅/复古⚠️中/头脑风暴未测）；两轮 prompt 修正（复古卡穿字强制指令、选词约束）。
