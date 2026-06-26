---
name: huo15-img-prompt
displayName: 火一五文生图提示词
description: 火一五文生图提示词 v3.2 — AI 创作生态中枢，14 件套 + ⭐v3.2 审美锚点系统：88 预设新增 aesthetic_anchor 字段（每个预设映射到具体导演 / 摄影师 / 艺术家 / 电影场景，赛博朋克→Roger Deakins 银翼杀手 2049 / 汉服写真→张叔平一代宗师 / ghibli→千与千寻汤屋窗景）+ 15 个 Master 档设计师级预设（Pentagram / Saul Bass / Massimo Vignelli / Wim Crouwel / Paul Rand / Tibor Kalman / Stefan Sagmeister / Paula Scher / Otl Aicher / Bruno Munari / 杉本博司 / 原研哉 / 安藤忠雄 / 王家卫 / Wes Anderson）。适配 Midjourney/SD/SDXL/Flux/DALL-E 3。触发词：文生图、火一五文生图提示词、文生视频、提示词增强、故事板、storyboard、剧本拆分、关键帧、视频脚本包、品牌套件、brand kit、品牌规范、风格学习、style learn、自学习预设、learned preset、参考图学习、Claude Vision、闭环迭代、五维评审、A/B 测试、角色卡、MCP server、Web UI、Obsidian 集成、Replicate、Fal、即梦、可灵、Hailuo、Sora、Claude Code、Cursor、aesthetic anchor、审美锚点、Master 档预设、设计师级预设、Pentagram、Saul Bass、Massimo Vignelli、Roger Deakins、王家卫、张叔平、杉本博司。
version: 3.2.0
aliases:
  - 火一五文生图提示词
  - 火一五文生图技能
  - 火一五文生视频技能
  - 火一五提示词技能
  - 火一五提示词全家桶技能
  - 火一五AI绘画技能
  - 文生图
  - 文生视频
  - 提示词增强
  - 智能润色
  - 平台合规润色
  - img-prompt
---

# 火一五文生图提示词 v3.2

**AI 创作生态中枢。从单帧提示词到完整短片脚本包，从手选预设到自学习风格，从孤岛工具到与 huo15 设计四件套联动。v3.2 起加 audestically anchor 系统 + 15 个 Master 档设计师级预设。**

---

## v3.2 ⭐ 审美锚点系统（与下文 88 预设并列）

### 为什么需要审美锚点

88 预设的 lighting / palette / camera 是**固定字符串拼接**（如赛博朋克 → "neon magenta and cyan rim, wet reflective streets"），LLM 拼出来的 prompt 容易陷入 cliché。**审美锚点**是把每个预设映射到**具体的真实创作者 / 作品**，让 Claude 在拼提示词时有真实意向锚定。

锚点不是替换原 prompt，而是**追加为可选 augmentation**（脚本可在 system prompt 里读到，或用户用 `--anchor` 显式启用）。

### 88 预设的审美锚点表（v3.2 增量字段）

下面是预设 → 锚点映射的精选清单。**完整 88 条锚点作为 prompt-fragment 库 by-design 让 Claude 在调用 enhance_prompt 时自动叠加**，不需要硬编码到 Python 脚本里。

| 预设 | 升级后的审美锚点（新增） |
|------|---------------------|
| 赛博朋克 | Roger Deakins《Blade Runner 2049》氪绿一段 / Darren Aronofsky《Black Swan》冷调 / 《Severance》Lumon 极简冷感（新一代赛博） |
| 电影感 | 王家卫 × 杜可风《花样年华》/ 侯孝贤《海上花》/ Wes Anderson《Grand Budapest》对称构图 / Roger Deakins《1917》长镜头光 |
| 汉服写真 | 张叔平《一代宗师》室内逆光 / 张艺谋《影》水墨黑白 / 陈家毛《满江红》青砖朱漆 |
| 宫崎骏 | 《千与千寻》汤屋夕照 / 《天空之城》云海光线 / 《魔女宅急便》清晨海港光（指明具体场景胜过笼统"宫崎骏感"） |
| 新海诚 | 《你的名字》黄昏彗星天 / 《天气之子》雨光 / 《秒速 5 厘米》新宿夜灯 |
| 敦煌壁画 | 莫高窟 257 窟九色鹿本生（青绿） / 220 窟药师变（朱红群青） / 余秋雨《文化苦旅·莫高窟》文字描述 |
| 原神 | 蒙德 City Centre 全景 / 璃月港夜景 / 稻妻天守阁雷电（指明地区光） |
| 黑暗奇幻 | 《指环王》摩瑞亚矿坑 / 《权游》龙石岛雾景 / Frank Frazetta 油画 |
| 极简主义 | Dieter Rams Braun 设计目录 / 原研哉「白」展册 / vitsoe.com 货架 |
| Logo 设计 | Paul Rand IBM rebus / Massimo Vignelli NYC subway / Saul Bass AT&T 圈 |
| 信息图 | Edward Tufte《The Visual Display of Quantitative Information》/ Otl Aicher 慕尼黑奥运图标 |
| 浮世绘 | 葛饰北斋《神奈川冲浪里》/ 歌川广重《东海道五十三次》/ 月冈芳年《月百姿》 |
| 包豪斯 | Herbert Bayer 海报 / Paul Klee 几何 / Wassily Kandinsky 圆三角方 |
| 蒸汽朋克 | Hayao Miyazaki《天空之城》机械城 / Jules Verne 插图传统 / 《Wild Wild West》机械师 |
| 暗黑美食 | 《Chef's Table》深焦特写 / Helmut Newton 黑白美食 / Gabriele Stabile 静物 |
| 赛璐璐 | 《新世纪福音战士》线稿 / 《幽游白书》明暗块面 / 《灌篮高手》动作分镜 |
| 复古海报 | Saul Bass《迷魂记》/ 《七年之痒》Hirschfeld 线稿 / Cassandre《Dubonnet》 |
| 国潮 | 故宫博物院文创色板 / 《国家宝藏》视觉 / 上海 1933 老场坊 |
| 复古胶片 | Kodak Portra 400 颗粒 / Fuji Pro 400H / Cinestill 800T 夜灯光晕 |
| 莫兰迪 | Giorgio Morandi《静物》系列 / 莫兰迪博物馆 Bologna 实拍 |
| 治愈 | 《想见你》《同棲生活》生活流 / Notion 早期插画 / 阿尼斯 Aniish 涂鸦 |
| 国风故宫 | 故宫倦勤斋 / 三希堂 / 《我在故宫修文物》纪录片 |
| 水墨 | 八大山人《荷石图》/ 齐白石《虾》/ 黄宾虹《青城山图》/ 张大千泼彩 |
| 油画 | Vermeer《戴珍珠耳环的少女》/ Caravaggio 明暗对比 / Rembrandt 自画像 |
| 像素艺术 | 《Stardew Valley》/ 《Owlboy》/ 《Hyper Light Drifter》 |

**用法**：在 `enhance_prompt.py` 调用时由 Claude 主动追加锚点到主体描述：

```bash
# 自动注入锚点（推荐 Master 档使用）
enhance_prompt.py "持剑女侠" -p 赛博朋克 --anchor "in the style of Roger Deakins Blade Runner 2049, ammonia-green corridor lighting"

# 或在 --polish 模式下让 Claude 自动从 system prompt 读锚点表叠加
enhance_prompt.py "持剑女侠" -p 赛博朋克 --polish --tier master
```

### Master 档设计师级预设（v3.2 新增 15 个）

下面 15 个预设**不是流派也不是主题**，而是**具体设计大师 / 导演 / 艺术家**的视觉语言。专为 Master 档设计需求（品牌官网 KV / 高端杂志封面 / 投融资路演主视觉）。

| # | 预设名 | 锚定大师 / 作品 | 视觉签名 | 适用 |
|---|--------|---------------|---------|------|
| 1 | `pentagram` | Pentagram（Paula Scher） | 超大字排版 + 强烈对比 + 平面英雄主义 | 品牌 KV / 杂志封 |
| 2 | `saul-bass` | Saul Bass | 几何剪影 + 单色调 + 电影海报式构图 | 海报 / 电影主视觉 |
| 3 | `vignelli` | Massimo Vignelli | 网格 + Helvetica + 红黄黑三色 + 工业理性 | 信息图 / 地铁式导视 |
| 4 | `wim-crouwel` | Wim Crouwel | 网格化字母 + 色块 + 几何字体 + Stedelijk 海报 | 实验排版 / 美术馆视觉 |
| 5 | `paul-rand` | Paul Rand | 玩味 logo + 极简色块 + Eye-Bee-M 风幽默 | 企业 logo / IBM 风 |
| 6 | `tibor-kalman` | Tibor Kalman / M&Co. | 反讽设计 + 拼贴 + Colors Magazine 风 | 文化媒体 / 反工业 |
| 7 | `sagmeister` | Stefan Sagmeister | 手写 + 大胆 + Things I Have Learned 系列 | 个人品牌 / 演讲 |
| 8 | `paula-scher` | Paula Scher | 文字即图像 + Citibank logo / Public Theater 风 | 文化机构 / 公共项目 |
| 9 | `otl-aicher` | Otl Aicher | 慕尼黑奥运图标 + 几何象形 + Lufthansa 视觉 | 体育 / 航空 / 系统设计 |
| 10 | `bruno-munari` | Bruno Munari | 实验书籍 + 童趣几何 + Codice Ovvio | 出版 / 童书 / 实验艺术 |
| 11 | `sugimoto` | 杉本博司 | 长曝光海景 / 影院系列 / 极简黑白 + 时间感 | 高端艺术 / 摄影集 |
| 12 | `kenya-hara` | 原研哉 | 白 / 空 / 纸感 / 朱红印章 | 日式品牌 / 杂志 |
| 13 | `tadao-ando` | 安藤忠雄 | 清水混凝土 + 光的教堂 + 几何空间感 | 建筑 / 美术馆 |
| 14 | `wong-kar-wai` | 王家卫 + 杜可风 | 室内逆光 + 红绿撞色 + 慢镜头长曝 + 留白 | 电影感 / 文艺品牌 |
| 15 | `wes-anderson` | Wes Anderson | 中心对称 + 糖果粉薄荷 + 顶底品牌线 | 旅行 / 童趣品牌 |

**用法示例**：

```bash
# 用 Pentagram 风做品牌 KV
enhance_prompt.py "极简茶饮品牌主视觉" -p pentagram -m Midjourney
# → 自动注入：bold typography, high contrast, Paula Scher SoHo poster aesthetic

# 用王家卫 + 杜可风做电影感写真
enhance_prompt.py "持伞女子等候" -p wong-kar-wai -m Flux
# → 自动注入：Christopher Doyle cinematography, In the Mood for Love color grading, slow shutter

# 用杉本博司做高端艺术摄影
enhance_prompt.py "孤舟" -p sugimoto -m Midjourney
# → 自动注入：Hiroshi Sugimoto seascape, long exposure, monochrome, time as subject
```

**Master 档预设和 design-director v3.0 §三 Master 档对标的关系**：

- design-director 在选定方向后，如果用户选 Master 档，**brief 中的 signatureHook 可指定一个 Master 档预设**作为参考
- 例如 director brief 写「signatureHook: 用 wong-kar-wai 风格的室内逆光 + 红绿撞色」→ frontend-design 落地时调 huo15-img-prompt 用 `wong-kar-wai` 预设生成 hero 图

### 与 huo15 生态的联动

```
design-director v3.0 §二 视觉三元组
    ↓ 锚点列直接指向 img-prompt 的 Master 档预设
    ↓ 例：philosophy #1 原研哉 → img-prompt 的 kenya-hara 预设
img-prompt v3.2 Master 档预设
    ↓ 输出 prompt
任意文生图后端（DALL-E / MJ / Flux / 即梦 / 可灵）
    ↓ 输出图
design-critique v2.0 §五 8 流派对标
    ↓ 用对应 Master 档锚点评估
```

---

## v3.0 = 14 件套

| # | 脚本 | 作用 | 一行 demo |
|---|------|------|-----------|
| 1 | `enhance_prompt.py` | 文生图核心 | `enhance_prompt.py "持剑女侠" -p 赛博朋克 --variants 4` |
| 2 | `enhance_video.py` | 视频提示词 | `enhance_video.py "汉服少女转身回眸" -p 汉服写真 -m Kling` |
| 3 | `reverse_prompt.py` | 参考图反解 | `reverse_prompt.py img.png --mj` |
| 4 | `render_prompt.py` | 10 后端直出 | `render_prompt.py "原神少女" -p 原神 --backend jimeng` |
| 5 | `claude_polish.py` | Claude 润色 + top-3 推荐 | `claude_polish.py "温柔治愈" --suggest` |
| 6 | `safety_lint.py` | 平台合规润色 | `safety_lint.py "战士手中的鲜血" --target dalle` |
| 7 | `image_review.py` | Claude Vision 五维评审 | `image_review.py img.png -p "原 prompt"` |
| 8 | `auto_iterate.py` | 闭环自动迭代 | `auto_iterate.py "持剑女侠" -p 赛博朋克 --backend dalle --target 7.5` |
| 9 | `character.py` | 角色卡持久化 | `enhance_prompt.py "新场景" --char 银发机甲少女` |
| 10 | `mcp_server.py` | MCP stdio server | `python3 mcp_server.py`（注册到 ~/.claude/mcp.json） |
| 11 | `web_ui.py` | 本地 Web UI | `python3 web_ui.py`（http://127.0.0.1:7155） |
| 12 | `storyboard.py` ⭐v3.0 | 剧本→关键帧+转场视频脚本包 | `storyboard.py "..." -p 电影感 --scenes 6 --output ./story` |
| 13 | `brand_kit.py` ⭐v3.0 | 品牌套件持久化 | `enhance_prompt.py "..." --brand-kit huo15` |
| 14 | `style_learn.py` ⭐v3.0 | 多参考图→learned preset | `style_learn.py --name 我的风格 ref*.jpg && enhance_prompt.py "..." -p "@我的风格"` |

📚 配套文档：
- [`QUICKSTART.md`](QUICKSTART.md) ⭐v3.1 — 30 秒/5 分钟/30 分钟分级上手
- [`RECIPES.md`](RECIPES.md) — 5 个端到端食谱
- [`examples/`](examples/) ⭐v3.1 — 真实可运行示例（brand_kit / character / learned_preset / 剧本）
- [`scripts/doctor.py`](scripts/doctor.py) ⭐v3.1 — 一键健康检查
- [`tests/smoke.py`](tests/smoke.py) ⭐v3.1 — 33 自动回归测试

## 版本演进

| 维度 | v2.4 | v2.5 | v2.6 | v3.0 |
|------|------|------|------|------|
| **风格预设** | 88 + 参考图链接 | + 智能 top-3 | 沿用 | + **自学习 learned preset** |
| **一致性** | + session 锁 | + A/B 变体 | + 角色卡 | + **品牌套件全局锁** |
| **贴近需求** | + prompt 压缩 | + Claude 改 prompt | 沿用 | + **故事板拆 N 关键帧** |
| **生态闭环** | + 10 后端直出 | + VLM 五维评审 | + Obsidian 写入 | + **创意四件套整合** |
| **AI 联动** | 多轮编辑 | 闭环自动迭代 | + MCP server | + **跨技能联动** |
| **输入** | 一句话主体 | 一句话主体 | 一句话主体 | + **剧本/参考图/品牌规范** |
| **输出** | 单帧 prompt | 单帧 prompt | 单帧 prompt | + **完整短片脚本包** |

## 使用方式

### Agent 调用（推荐）

```
用户: 帮我出一张赛博朋克街头的图
```

Agent 识别到"赛博朋克"触发词，自动调用：

```bash
~/workspace/projects/openclaw/huo15-skills/huo15-img-prompt/scripts/enhance_prompt.py \
    "赛博朋克街头" -p 赛博朋克 -m Midjourney
```

### 直接调用

```bash
cd ~/workspace/projects/openclaw/huo15-skills/huo15-img-prompt

# 基础：指定预设
./scripts/enhance_prompt.py "一只猫" -p 动漫 -m Midjourney

# 自动意图（无需 -p，脚本从关键词推断）
./scripts/enhance_prompt.py "为咖啡品牌设计一个logo"   # → 自动选 Logo设计, 1:1
./scripts/enhance_prompt.py "产品白底图：无线耳机"     # → 自动选 产品摄影, 1:1
./scripts/enhance_prompt.py "微距 一滴露珠"            # → 自动选 微距摄影, 1:1

# 系列一致性（4 张共享 seed + camera/lighting/palette 锁）
./scripts/enhance_prompt.py "红发女侠" -p 动漫 -s 4 \
    --variations "持剑站立,骑马奔驰,弯弓射箭,与龙对视" \
    -m Midjourney

# 英文别名 + 多模型输出
./scripts/enhance_prompt.py "spaceship in nebula" -p scifi -m Flux -a 21:9
./scripts/enhance_prompt.py "minimalist camellia logo" -p logo -m SDXL

# JSON 输出（便于集成）
./scripts/enhance_prompt.py "森林少女" -p ghibli -j
```

## 88 款风格预设

### 【摄影 · 13】
写实摄影 / 胶片摄影 / 黑白摄影 / 人像摄影 / 时尚大片 / 美食摄影 / 产品摄影 / 微距摄影 / 航拍摄影 / 街拍纪实 / **暗黑美食 · 日杂 · 街头潮流** ⭐v2.1

### 【动漫 · 10】
动漫 / 新海诚 / 宫崎骏 / 美漫 / Q版 / 童话绘本 / **萌系 · 厚涂 · 轻小说封面 · 赛璐璐** ⭐v2.1

### 【插画 · 7】
水彩 / 油画 / 水墨 / 工笔国画 / 浮世绘 / 线稿 / 像素艺术

### 【3D · 7】
3DC4D / 盲盒手办 / 低多边形 / 等距视图 / 粘土 / 毛毡手工 / 纸艺

### 【设计 · 15】
极简主义 / 平面设计 / Logo设计 / 图标设计 / 信息图 / 品牌KV / 专辑封面 / 复古海报 / 电影海报 / 表情包 / **玻璃拟态 · 新拟态 · 孟菲斯 · 杂志编排 · 包豪斯 · 奶油风** ⭐v2.1

### 【艺术史 · 4】
印象派 / 后印象派 / 新艺术 / 装饰艺术

### 【场景氛围 · 17】
赛博朋克 / 蒸汽朋克 / 科幻 / 奇幻 / 黑暗奇幻 / 国潮 / Y2K / Vaporwave / 霓虹灯牌 / 建筑可视化 / 电影感 / 概念艺术 / **粗野主义 · 北欧极简 · 侘寂 · 疗愈治愈 · 美式复古** ⭐v2.1

### 【游戏艺术 · 7】⭐ v2.1 新类
原神 / 崩铁星穹 / 英雄联盟 / 暗黑4 / Valorant / Pokemon / 暴雪风

### 【东方传统 · 7】⭐ v2.1 新类
敦煌壁画 / 青花瓷 / 民国月份牌 / 年画 / 剪纸 / 和风 / 汉服写真

> 英文别名支持：`anime`、`ghibli`、`shinkai`、`cyberpunk`、`steampunk`、`scifi`、`minimal`、`logo`、`icon`、`3d`、`c4d`、`octane`、`isometric`、`vangogh`、`artdeco`、`neon`、`vapor`、`y2k`、`genshin`、`lol`、`diablo`、`valorant`、`pokemon`、`dunhuang`、`hanfu`、`wafu`、`glassmorphism`、`neumorphism`、`memphis`、`bauhaus`、`brutalism`、`nordic`、`wabisabi`、`healing`、`cozy`、`americana`、`darkfood`、`muji`、`streetwear`… 运行 `./scripts/enhance_prompt.py -l` 查看完整列表。

## 参数说明

| 参数 | 作用 | 示例 |
|------|------|------|
| `subject` | 主体描述（必填） | `"一只猫"` |
| `-p, --preset` | 风格预设（中文 / 英文别名） | `-p 赛博朋克` / `-p cyberpunk` |
| `-m, --model` | 目标模型 | `Midjourney` / `SD` / `SDXL` / `Flux` / `DALL-E` / `通用` |
| `-a, --aspect` | 画幅 | `1:1` / `3:4` / `16:9` / `21:9` / `9:16` |
| `-t, --tier` ⭐v2.1 | 质量档位 | `basic` / `pro`(默认) / `master` |
| `-cs, --character-sheet` ⭐v2.1 | 角色设定图 T-pose 多视图 | - |
| `--avoid` ⭐v2.1 | 额外负面词，逗号分隔 | `--avoid "cluttered, people"` |
| `--mood` | 情绪覆盖（不给则从主体自动抽） | `--mood 神秘` |
| `--composition` | 构图覆盖 | `--composition 俯拍` |
| `--seed` | 种子（不给则按 subject+preset 哈希生成稳定 seed） | `--seed 42` |
| `-s, --series` | 系列张数 | `-s 4` |
| `--variations` | 系列变体，逗号分隔 | `--variations "A,B,C,D"` |
| `-l, --list` | 列出所有预设 | - |
| `-j, --json` | JSON 输出 | - |

## 自动抽词（v2.1 扩展）

脚本会从主体描述中自动识别以下字段，无需显式参数：

| 维度 | 关键词示例 |
|------|-----------|
| **意图** | logo / 产品 / 海报 / 头像 / 美食 / 汉服 / 敦煌 / 原神 / 玻璃拟态 ... |
| **构图** | 特写 / 近景 / 中景 / 全身 / 俯拍 / 仰拍 / 鸟瞰 / 航拍 / 侧面 / 背面 |
| **情绪** | 温暖 / 冷峻 / 神秘 / 梦幻 / 欢快 / 忧郁 / 史诗 / 高级 / 治愈 / 浪漫 ⭐v2.1：紧张 |
| **时间** ⭐v2.1 | 清晨 / 早晨 / 正午 / 下午 / 黄昏 / 日落 / 夜晚 / 深夜 / 黎明 / 蓝调时刻 |
| **天气** ⭐v2.1 | 晴天 / 多云 / 阴天 / 下雨 / 雨天 / 大雨 / 下雪 / 雪天 / 雾天 / 风暴 / 雷雨 |
| **季节** ⭐v2.1 | 春/夏/秋/冬 / 樱花季 / 枫叶季 |
| **负向需求** ⭐v2.1 | 不要X / 没有X / 避免X / no X / avoid X / without X → 自动入负面 |

## 一致性四锁（核心机制）

每个预设内置以下锁项，所有系列张图共享 ⇒ 风格漂移大幅下降：

| 锁项 | 作用 | 示例（赛博朋克） |
|------|------|----------------|
| `camera` | 镜头焦段 / 视角 | `low angle wide, 24mm anamorphic` |
| `lighting` | 光源 / 光质 | `neon magenta and cyan rim, wet reflective streets` |
| `palette` | 色板 | `magenta cyan black, neon highlights` |
| `aspect` | 画幅 | `21:9` |

系列模式 (`-s N --variations ...`) 额外锁定 **seed**，变换仅发生在主体描述，框架完全不变。

## 模型适配细节

| 模型 | 输出格式 | 特有提示 |
|------|---------|---------|
| **Midjourney** | `主体, 风格, 光影, 色板, 画质 --ar X:Y --stylize 250` | `--cref <url>` 锁角色、`--sref <url>` 锁风格图 |
| **Stable Diffusion** | `(subject:1.2), 风格, ..., 质量` + 负面 | 权重语法 `(word:1.3)`、减弱 `[word]`、DPM++ 2M Karras |
| **SDXL** | 同 SD，尺寸建议 `1024x1024 / 1216x832 / 1536x640 ...` | Refiner 0.2-0.3 |
| **DALL-E 3** | 自然语言段落（已内化负面） | 连续对话中用 "same character / same scene" |
| **Flux** | 长句描述 | guidance 3.5（Dev） / 0（Schnell） |
| **通用** | 逗号分隔 tags | 三大模型通用骨架 |

## 完整示例

```bash
./scripts/enhance_prompt.py "一只戴墨镜的猫在霓虹街头" -p 赛博朋克 -m Midjourney
```

输出：

```
📌 原始描述   : 一只戴墨镜的猫在霓虹街头
🎨 风格预设   : 赛博朋克
🤖 目标模型   : Midjourney
📐 画幅       : 21:9
🎲 种子建议   : 1873940236

✅ 正向提示词：
一只戴墨镜的猫在霓虹街头, cyberpunk, neon-soaked, blade runner aesthetic,
megacity dystopia, holographic ads, low angle wide, 24mm anamorphic,
neon magenta and cyan rim, wet reflective streets,
magenta cyan black, neon highlights,
detailed cyberpunk cityscape, rainy night ambiance,
masterpiece, best quality, ultra detailed, 8k
--ar 21:9 --stylize 250

❌ 负向提示词：
--no rustic, medieval, natural countryside, low quality, worst quality, ...

🔒 一致性锁：
   camera  : low angle wide, 24mm anamorphic
   lighting: neon magenta and cyan rim, wet reflective streets
   palette : magenta cyan black, neon highlights
   aspect  : 21:9

💡 Midjourney tips：
  • 角色/产品系列一致：加 --cref <url> 或 --sref <url>
  • 想要更风格化加 --stylize 500~750；更写实降到 --stylize 50
  • 建议 seed 锁定：--seed 1873940236
```

## v3.0 新功能 ⭐⭐⭐⭐（定位升级：从工具到生态中枢）

### 1. 故事板模式 `storyboard.py` ⭐ 杀手级 feature

```bash
storyboard.py "一只猫从城市走进雨夜" -p 电影感 --scenes 4 \
    -m Midjourney --video-model Sora --output ./my_story
```

输入：一段剧本/文案
输出（在 `./my_story/`）：
- `storyboard.json` 完整 scene + transition 数据
- `scene-{01-N}-t2i.txt` × N 个关键帧 T2I 提示词
- `transition-{xx-to-yy}-t2v.txt` × N-1 个转场 T2V 提示词
- `README.md` 可读总览 + 生产管线说明

亮点：
- Claude 自动拆叙事弧（开场→起→承→转→合）
- 整段共享 base_seed，角色不漂移
- 复用 88 预设/混合/五锁机制
- 视频模型 9 选 1：Sora/Kling/Runway/Pika/Luma/Hailuo/即梦/Wan/通用
- **国内目前没人做到"剧本 → 完整 T2I+T2V 脚本包"**

### 2. 品牌套件持久化 `brand_kit.py`

```bash
# 创建品牌套件
brand_kit.py --create song_tea \
    --colors "#2C5F2D, #97BC62, #F7F4EA" \
    --fonts "Songti SC, Source Han Serif" \
    --keywords "宋韵, 极简, 留白, 文人画" \
    --forbidden "modern digital, neon, cyberpunk" \
    --logo "minimal flame mark in green"

# 出图时自动注入
enhance_prompt.py "茶饮品牌主视觉" -p 汉服写真 --brand-kit song_tea
```

注入位置：
- `colors` → 写入 prompt 作为 brand color palette
- `keywords` → 追加到主体描述
- `forbidden` → 合并到 negative prompt
- `logo_description` → 加入 brand identity 信号

完美对接 `huo15-openclaw-brand-protocol` 的输出（其 JSON 可直接 `--import`）。

### 3. 风格学习引擎 `style_learn.py`

```bash
# 给 N 张参考图，Claude Vision 提取共性 → 生成新预设
style_learn.py --name 我的小清新 \
    refs/morning_cafe.jpg refs/film_kodak.jpg refs/window_light.jpg

# 后续用 @ 前缀调用
enhance_prompt.py "猫咪坐在窗台" -p "@我的小清新"
```

工作流：
1. 每张图调一次 Claude Vision 提取 tags/camera/lighting/palette
2. 综合阶段让 Claude 归纳共性，输出和 STYLE_PRESETS 兼容的 spec
3. 自带 `confidence` 字段（< 0.5 警告参考图风格太散）
4. 存到 `~/.huo15/learned_presets/<name>.json`，运行期注册到 STYLE_PRESETS

### 4. 创意四件套整合食谱 `RECIPES.md`

5 个端到端食谱，演示和其他 huo15-openclaw-* 技能联动：

1. **品牌 KV 全流程**：design-director → brand-protocol → brand_kit → img-prompt → design-critique → frontend-design
2. **自学习风格 + 角色一致性 + 视频短片**：style_learn → character → storyboard
3. **电商商品图全套**：brand_kit + variants + character + obsidian
4. **Claude Code MCP 工作流**：IDE 内自然语言调用
5. **knowledge-base 联动**：资产沉淀到知识库

### 这一版的定位升级

| | v2.x | v3.0 |
|---|------|------|
| 输入 | 一句话主体 | 一段剧本 / 多张参考图 / 品牌规范 |
| 输出 | 单帧 prompt | **完整短片脚本包 + 学到的新预设 + 品牌一致出图** |
| 个性化 | 88 内置预设 | + **用户自学习风格 + 品牌套件** |
| 生态位 | 独立工具 | + **创意四件套核心节点**（5 个 huo15 技能联动） |

## v2.6 新功能 ⭐⭐⭐（用户群从 CLI → IDE/GUI/笔记四栖）

### 1. 角色卡持久化 `character.py`

```bash
# Turn 1: 创建角色（带 character-sheet 模式）
enhance_prompt.py "银发机甲少女 twin tails glowing visor" \
    -p 动漫 --character-sheet --save-char 银发机甲少女

# Turn 2 ~ N: 跨调用保持角色一致（自动锁 seed + 注入主体）
enhance_prompt.py "在霓虹街头" --char 银发机甲少女 -p 赛博朋克
enhance_prompt.py "在花海中" --char 银发机甲少女
enhance_prompt.py "持剑战斗" --char 银发机甲少女

# 角色卡管理（独立 CLI）
character.py --list
character.py --show 银发机甲少女
character.py --export 银发机甲少女 > char.json
cat char.json | character.py --import
```

存储：`~/.huo15/characters/<name>.json`，含 use_count + 时间戳 + 五锁。

### 2. Obsidian 集成 `--obsidian`

```bash
# 默认检测 ~/knowledge/huo15 / ~/Documents/Obsidian / ~/Obsidian
enhance_prompt.py "敦煌神女" -p 敦煌壁画 --obsidian

# 指定 vault
OBSIDIAN_VAULT=~/my-vault enhance_prompt.py "..." -p 原神 --obsidian
```

写入 `<vault>/图集/{date}-{subject}-{seed}.md`，含完整 frontmatter（tags/preset/seed/...）+ 正负向提示词 + 一致性锁 + 复现 CLI 命令。

跟 huo15 三层记忆生态吻合（L3 共享 KB wiki）。

### 3. MCP server `mcp_server.py` ⭐ IDE 用户的入口

让 **Claude Code / Cursor / Cline / Continue.dev** 直接调用 9 个工具：

```json
// ~/.claude/mcp.json
{
  "mcpServers": {
    "huo15-img-prompt": {
      "command": "python3",
      "args": ["~/path/to/huo15-img-prompt/scripts/mcp_server.py"]
    }
  }
}
```

暴露的工具：
- `enhance_prompt` / `list_presets` / `preset_examples`
- `suggest_presets` / `polish_prompt` / `safety_lint`
- `review_image` / `list_characters` / `load_character`

实现：手写 JSON-RPC 2.0 over stdio，零第三方依赖。

### 4. 本地 Web UI `web_ui.py` ⭐ 设计师/PM 用户的入口

```bash
python3 web_ui.py             # 默认 http://127.0.0.1:7155
python3 web_ui.py --port 8080
python3 web_ui.py --no-browser
```

特性：
- 单文件 HTML（vanilla JS + Tailwind CDN，零构建）
- Python `http.server.ThreadingHTTPServer` 做后端
- 三栏布局：输入 / 88 预设可视化 / 实时输出
- 角色卡下拉选择 + 一键复制
- 自动开浏览器、Ctrl+C 退出

## v2.5 新功能 ⭐⭐⭐（核心护城河）

### 1. Claude Vision 五维评审 `image_review.py`

```bash
# 单图评审
image_review.py img.png --prompt "原始 prompt"

# 多图排名（同一组 variants 出图后挑最优）
image_review.py renders/*.png --rank
```

输出：
- 五维分数（0-10）：subject_match / composition / lighting / palette / technical
- 加权 overall_score + 三档 verdict（PASS/RETRY/REJECT）
- **可执行修复**：每条 issue 不写"光线不好"，直接给 `add: golden hour rim light, soft fill from camera left`
- 简评模式 `--quick`（只 overall_score，省 token）

### 2. 闭环自动迭代 `auto_iterate.py` ⭐ 杀手级 feature

```
                ┌──────────────┐
                │ user prompt  │
                └──────┬───────┘
                       ↓
            ┌─────────────────────┐
            │  enhance_prompt     │
            └─────────┬───────────┘
                      ↓
            ┌─────────────────────┐
            │  render (10 后端)   │
            └─────────┬───────────┘
                      ↓
            ┌─────────────────────┐
            │  Claude Vision      │
            │  五维评审           │
            └─────────┬───────────┘
                      ↓
                  分数 ≥ 阈值?
                  ↙          ↘
                Y              N (≤ 3 轮)
                ↓               ↓
              完成        ┌────────────┐
                          │ Claude 改   │
                          │ prompt     │
                          └─────┬──────┘
                                ↑
                          (回到 enhance)
```

```bash
auto_iterate.py "持剑女侠" -p 赛博朋克 --backend dalle --target 7.5 --max-rounds 3
```

每轮锁定 seed，便于对比 prompt 改动到底改善了哪一维。Claude 的修改基于上轮 review 的 actionable_fixes，输出 revised_subject + extra_negatives + extra_mood + rationale。

**这个能力 GPT-4o image / Claude Imagen 内部做不到** — 它们是端到端黑盒，没有 prompt-image 闭环数据。

### 3. A/B 变体测试 `--variants N`

```bash
# 同 subject + 同 seed，仅在 mood/composition 上分化出 4 个变体
enhance_prompt.py "持剑女侠" -p 赛博朋克 --variants 4 -j > variants.json

# 出图后挑最优
image_review.py renders/*.png --rank
```

四个差异轴可选：`mood / composition / lighting / stylize`，`--variant-axes mood,lighting` 自定义。

### 4. 智能预设推荐 `--suggest`

```bash
# 模糊描述也能自动匹配预设
enhance_prompt.py "温柔治愈感的画面" --suggest
```

输出：top-3 候选预设 + 每个的 score (0-1) + reason + best_subject_example + mix_suggestion（自动判断是否需要混合）。

解决"温柔"、"高级"、"梦幻"等抽象描述硬关键词匹配不到的痛点。

## v2.4 新功能 ⭐

### 1. render_prompt.py 扩到 10 后端

```bash
# 国际开源
render_prompt.py "侠客" -p 水墨 --backend replicate --remote-model black-forest-labs/flux-schnell
render_prompt.py "猫" -p 动漫 --backend fal --remote-model fal-ai/flux/dev

# 国产模型（中文场景效果好）
render_prompt.py "敦煌神女" -p 敦煌壁画 --backend jimeng    # 字节即梦 / Seedream 3.0
render_prompt.py "汉服少女" -p 汉服写真 --backend kling     # 快手可灵 v1
render_prompt.py "原神少女" -p 原神 --backend hailuo        # 海螺 MiniMax image-01
```

环境变量：`REPLICATE_API_TOKEN` / `FAL_KEY` / `ARK_API_KEY`（火山方舟）/ `KLING_API_KEY` / `MINIMAX_API_KEY`。

### 2. prompt 压缩 `--compact`

```bash
enhance_prompt.py "持剑女侠" -p "赛博朋克+水墨" -m SD --compact
# 🗜  prompt 已压缩: 124→73 tokens (砍 12 段)
```

策略：去重 → 同义合并 → 保头 6 段（主体+camera）→ 按预算砍尾。专治 SDXL CLIP 77 token 截断。

### 3. 88 预设参考图链接 `--examples`

```bash
# 看单个预设的参考图（5 平台搜索 URL）
enhance_prompt.py --examples 敦煌壁画
# 列表模式带链接
enhance_prompt.py -l --with-examples
```

输出 5 平台搜索 URL：Lexica / Civitai / Pinterest / Google Images / Unsplash。零维护，靠搜索 query 永远有效。

### 4. 多轮编辑 `--session` / `--continue`

```bash
# Turn 1: 出图
enhance_prompt.py "猫坐在窗台" -p 写实摄影 --session catwindow

# Turn 2: 改画幅 + 加情绪，seed 自动锁定保证主体一致
enhance_prompt.py --continue catwindow --aspect 16:9 --mood 治愈

# Turn 3: 完全换主体描述但保 seed 测一致性
enhance_prompt.py "猫站起来伸懒腰" --continue catwindow

# 列出所有 session
enhance_prompt.py --list-sessions
```

持久化目录：`~/.huo15/sessions/<name>.json`。CLI 参数 > session 默认值 > 系统默认。

## v2.3 新功能 ⭐

### 5. Claude API 智能润色 `--polish`

```bash
# 直接润色（独立调用）
export ANTHROPIC_API_KEY=sk-ant-xxx
./scripts/claude_polish.py "一个温柔的女孩在花丛中"
./scripts/claude_polish.py "敦煌神女" --pipe   # 输出可直接喂给 enhance_prompt.py 的命令

# 在 enhance_prompt.py 里串联使用（润色 → 88 预设 → 输出）
./scripts/enhance_prompt.py "一个温柔的女孩在花丛中" --polish
./scripts/enhance_prompt.py "雪山下的小屋" --polish --safety MJ -m Midjourney
```

利用 Claude prompt engineering 优势：
- **Prompt caching**：system prompt 用 ephemeral cache，省 90% input token
- **Prefill `{`**：assistant 起手 `{` 强制 JSON 输出，无需 tool use
- **XML 思维链**：让 Claude 内部分步骤（refine/style/camera/safety/negatives）
- **88 预设嵌入 system**：Claude 从清单里挑，不凭记忆
- **零 SDK 依赖**：纯 urllib，避免企业扫描器拦截 anthropic 包

### 6. 平台合规润色 `--safety`

**只做合法艺术创作的平台误判规避，不做 jailbreak。**

```bash
# 独立调用
./scripts/safety_lint.py "战士手中沾满鲜血的剑" --target dalle
./scripts/safety_lint.py "古典维纳斯雕像 nude figure" --target MJ --apply
./scripts/safety_lint.py "如何制作炸弹"   # 命中红线 → exit 2

# 在 enhance_prompt.py 里串联
./scripts/enhance_prompt.py "古风战场鲜血飞溅" --safety dalle
./scripts/enhance_prompt.py "黑暗骑士斩杀恶魔" --safety MJ -p 黑暗奇幻
```

**红线（直接拒答）**：
- ✗ CSAM（未成年 + 性化任意组合）
- ✗ 真人 + 色情/政治污蔑
- ✗ 武器/毒品/爆炸物**制作方法/教程**
- ✗ 自残/自杀**方法诱导**

**黄区（艺术化重写）**：
| 类别 | 例子 | 重写策略 |
|------|------|----------|
| violence | 血、伤口、kill、weapon | crimson splash / battle-scarred / vanquish / ceremonial blade |
| nudity | 裸、naked、sexy | classical figure study / fine art reference / fashion editorial |
| horror | horror、gore、demon | gothic atmospheric tension / mythical creature |
| death | dead、skeleton、skull | memento mori / classical allegory / vanitas |
| real-person | celebrity、明星、politician | fictional character / 80s aesthetic |
| brand | marvel、disney、nike | superhero comic style / classic animated |

**平台分级**：
- DALL-E `max` 严格度
- MJ `high` 中等
- SD/SDXL/Flux `low` 宽松（开源本地）

### 7. Polish + Safety 串联（最强组合）

```bash
# Claude 智能润色 → 平台合规重写 → 88 预设增强
./scripts/enhance_prompt.py "战士在血战之后凝视远方" --polish --safety dalle -j
```

输出 JSON 包含 `claude_polish` 和 `safety_lint` 两个完整 meta 块，可追溯每一步改写过程。

## v2.2 新功能详解

### 1. 混合预设 `-p A+B --mix 0.6`

```bash
# 主预设 60% 权重，副预设 40%
enhance_prompt.py "持剑女侠" -p "赛博朋克+水墨" --mix 0.6 -m Midjourney
enhance_prompt.py "山中神女" -p "原神+敦煌壁画" --mix 0.5 -m SDXL
enhance_prompt.py "极简卡片" -p "玻璃拟态+侘寂" --mix 0.7 -m SD
```

融合策略：
- **tags**：主预设标签前置，副预设按权重补充；SD 自动加权重语法 `(tag:1.16)`
- **camera**：取主预设（避免镜头语言混乱）
- **lighting**：叠加 `主光照, blended with 副光照`
- **palette**：拼接两者
- **aspect**：取主预设默认画幅
- **neg**：合并去重 + PRESET_NEG_EXCLUDE 主辅都生效（避免 logo/text/signature 自我否定）
- **seed**：mix_label `A+B@0.60` 参与 hash，相同混合每次同 seed

### 2. 视频提示词 `enhance_video.py`

```bash
# Sora 8 秒赛博朋克
enhance_video.py "雨夜霓虹街头一只猫漫步" -p 赛博朋克 -m Sora --duration 8

# Kling 慢速跟拍
enhance_video.py "汉服少女转身回眸" -p 汉服写真 -m Kling --motion 慢速跟拍

# 史诗节奏 + 自定义动作
enhance_video.py "宇宙飞船穿越星云" -p scifi -m Runway --pacing 史诗 --action "ship accelerates, lens flare"

# 混合风格 + 海螺 MiniMax
enhance_video.py "山中神女腾云" -p "原神+敦煌壁画" --mix 0.6 -m Hailuo

# 列出所有视频模型规格
enhance_video.py --list-models
```

支持的视频模型：

| 模型 | 上限时长 | 默认画幅 | 提示词风格 |
|------|---------|---------|-----------|
| Sora | 20s (Sora 2 Pro) | 16:9 | 长自然语言 |
| Kling 可灵 | 10s (1080p Pro) | 16:9 | 中文优秀，前置主体 |
| Runway Gen-3/4 | 10s | 16:9 | 英文最佳 |
| Pika | 10s | 16:9 | 标签式 + `-gs/-motion` |
| Luma DreamMachine | 9s | 16:9 | 自然语言 + 关键帧 |
| Hailuo MiniMax | 10s | 16:9 | 中英双语 + 参考人物 |
| 即梦 Seedance | 12s | 16:9 | 中文多镜头剧情 |
| 通义 Wan2.1 | 8s | 16:9 | 阿里开源 14B/1.3B |

输出包含：正向 / 负向（视频专属：flicker、motion blur、identity drift）/ 三段式关键帧 / 一致性六锁（+ motion）。

### 3. 参考图反解 `reverse_prompt.py`

```bash
# 自动识别 A1111/ComfyUI/NovelAI metadata
reverse_prompt.py /path/to/image.png

# 远程 URL
reverse_prompt.py https://example.com/img.png

# 直接给 Midjourney 复用 prompt（一行）
reverse_prompt.py img.png --mj

# 强制 VLM 模板（图无 metadata）
reverse_prompt.py img.png --vlm

# JSON pipe 给 enhance_prompt.py
reverse_prompt.py img.png -j > recipe.json
```

三层反解：
1. **PNG metadata**：手写 `tEXt`/`iTXt` 解析，零 PIL 依赖
2. **A1111 / ComfyUI / NovelAI 三大格式自动识别**
3. **VLM fallback**：图无 metadata 时输出标准 prompt 给 GPT-4o/Claude/Gemini/Qwen-VL

启发式预设猜测：35+ 关键词映射（cyberpunk → 赛博朋克 / ghibli → 宫崎骏 / dunhuang → 敦煌壁画 ...）。

### 4. 直出图片 `render_prompt.py`

```bash
# Dry-run（只输出 recipe，不出图）
render_prompt.py "敦煌神女" -p 敦煌壁画 --backend none -j

# AUTOMATIC1111 / Forge SD WebUI
render_prompt.py "赛博朋克猫" -p 赛博朋克 --backend sd-webui

# ComfyUI（用内置 SDXL workflow）
render_prompt.py "原神少女" -p 原神 --backend comfyui

# ComfyUI（自定义 workflow）
render_prompt.py "原神少女" -p 原神 --backend comfyui --workflow ./workflows/sdxl.json

# DALL-E 3
render_prompt.py "极简logo" -p Logo设计 --backend dalle --size 1024x1024
```

特点：
- **零第三方依赖**：纯 urllib，避免企业扫描器命中
- **环境变量覆盖**：`COMFYUI_URL` / `SDWEBUI_URL` / `OPENAI_API_KEY`
- **支持混合预设直出**

## 参考文档

`references/t2i-guide.md` — 提示词要素表 / 88 预设对照 / 模型差异 / 一致性技巧。

## 版本历史

见 `CHANGELOG.md`。
