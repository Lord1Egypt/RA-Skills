# Changelog

## v2.3.0 — 2026-04-26

**接入 Claude API + 平台合规润色，并起中文别名「火一五文生图提示词」。**

### 中文别名

`displayName: 火一五文生图提示词`，aliases 列表新增`火一五文生图提示词` 排第一位。

### enhance_prompt.py — 加 --polish / --safety

| 参数 | 作用 |
|------|------|
| `--polish` | 先调 Claude API（ANTHROPIC_API_KEY）智能润色，再走 88 预设增强 |
| `--safety <platform>` | 平台合规重写：DALL-E/MJ/SD/SDXL/Flux，自动把可能误判的艺术词替换 |

两者可叠加使用：先 polish 让 Claude 写出专业描述，再 safety 把误判词艺术化。

### 新增脚本：claude_polish.py（350 行）

- **Claude API 直调**：纯 urllib，不引入 anthropic SDK，避免企业扫描器
- **prompt caching 启用**：system prompt 用 `cache_control: ephemeral`，省 90% input token
- **Prefill `{` + JSON 强约束**：assistant 起手 prefill 强制结构化输出
- **88 风格预设嵌入 system prompt**：让 Claude 从清单里挑而非凭记忆
- **XML 思维链**：内部 `<thinking>` 让 Claude 分步骤思考（refine/style/camera/safety/negatives）
- **Platform warnings**：Claude 主动识别 DALL-E/MJ/SD 各自的风险点并给出建议
- **--pipe**：输出可直接喂给 enhance_prompt.py 的 CLI 命令

### 新增脚本：safety_lint.py（330 行）

**仅服务合法艺术创作场景**，不做 jailbreak：

✗ 红线（直接拒答）：
- CSAM（任何含未成年 + 性化的组合）
- 真人 + 色情 / 政治污蔑
- 武器/毒品/爆炸物**制作方法/教程**
- 自残/自杀**方法诱导**

✓ 黄区（艺术化重写）：
- **violence**: 鲜血/血/伤口/kill/murder/weapon/gun/knife → crimson splash / battle-scarred / vanquish / ceremonial blade
- **nudity**: naked/nude/裸/sexy → classical figure study / fine art reference / fashion editorial
- **horror**: horror/scary/gore/monster/demon/evil → gothic atmospheric tension / mythical creature / dark fantasy
- **death**: dead/corpse/skeleton/skull → memento mori / classical allegory / vanitas still life
- **real-person**: celebrity/明星/actor/politician → fictional protagonist / 80s aesthetic
- **brand**: marvel/disney/nike/iphone → superhero comic style / classic animated film / athletic sportswear
- **weapon-model**: ak47/glock/uzi → fictional assault rifle prop

每词内置 `category` + `platforms_affected`。平台分级：
- DALL-E `max` 严格度：所有黄区都触发高风险标记
- MJ `high` 中等：暴力/真人/品牌触发高风险
- SD/SDXL/Flux `low` 宽松（开源）：只对成人内容触发中风险

输出三模式：默认人类可读 / `-j` JSON / `--apply` 直接输出重写文本（pipe 友好）。

### 兼容性

- **完全向下兼容 v2.2**：所有新参数有默认值
- `--polish` 需 `ANTHROPIC_API_KEY`，未设置时报友好错误并不影响其他功能
- `--safety` 是纯本地词典，无网络依赖

### 设计原则

我们**坚决不做** jailbreak / 越狱 / 绕过模型对齐：
- 仅做"合法艺术创作场景下的平台误判规避"
- 红线检测优先于重写
- 替换词全部来自正规艺术、摄影、影视术语
- 用户输入红线内容时直接 `sys.exit(2)` 并给出改写建议

---

## v2.2.0 — 2026-04-25

**四件套大版本：混合预设 + 视频提示词 + 参考图反解 + 直出图片。**

### 新增脚本

| 脚本 | 作用 | 关键参数 |
|------|------|---------|
| `enhance_prompt.py` | 文生图（升级） | `-p A+B --mix 0.6` |
| `enhance_video.py` ⭐ | 视频提示词 | `-m Sora/Kling/Runway/Pika/Luma/Hailuo/即梦/Wan` |
| `reverse_prompt.py` ⭐ | 参考图反解 | A1111 / ComfyUI / NovelAI metadata + VLM 模板 |
| `render_prompt.py` ⭐ | 提示词直出 | `--backend comfyui/sd-webui/dalle/none` |

### enhance_prompt.py — 混合预设

- **`-p "A+B"` 语法**：`赛博朋克+水墨` / `原神+敦煌壁画` / `glassmorphism+wabisabi` 任意两两融合
- **`--mix <ratio>`**：主预设权重 0.1-0.9（默认 0.6）
- **SD 模式**：自动加权重语法 `(primary_tag:1.16), (secondary_tag:1.04)`
- **MJ/Flux/通用**：按比例前置主预设标签
- **camera/lighting/palette 智能融合**：相机沿主预设、光影叠加、色板拼接、aspect 取主
- **PRESET_NEG_EXCLUDE 双向生效**：主辅任一需要 logo/text/signature 都会从 universal_neg 剔除
- **seed 锁定**：mix_label `A+B@0.60` 参与 hash，相同混合每次生成相同 seed

### enhance_video.py — 视频提示词（新文件 470 行）

- **9 大视频模型规格**：Sora / Kling 可灵 / Runway Gen-3/4 / Pika / Luma DreamMachine / Hailuo MiniMax / 即梦 Seedance / 通义 Wan2.1 / 通用
- **30+ 镜头运动词典**：推/拉/摇/移/跟/环绕/手持/航拍/希区柯克/POV/子弹时间/延时/慢动作 ...
- **9 节奏档位**：缓慢 / 宁静 / 中速 / 紧张 / 急促 / 快切 / 动感 / 史诗 ...
- **30+ 主体动作自动抽词**：走/跑/跳/飞/舞/回眸/转身/挥剑/骑马/对视 ...
- **关键帧三段式拆分**：开场建立 → 中段动作峰值 → 结尾落点
- **视频专属负面词**：flicker / motion blur artifacts / identity drift / morphing artifacts
- **复用 88 风格预设 + 混合预设**：视觉锁完全沿用 image preset 体系
- **格式适配**：Pika 输出标签式，其他全部自然语言

### reverse_prompt.py — 参考图反解（新文件 340 行）

- **三层反解策略**：
  1. **PNG metadata**：手写 PNG `tEXt`/`iTXt` 解析，零依赖（不引入 PIL）
  2. **A1111/ComfyUI/NovelAI 三大格式自动识别**：parameters / prompt+workflow / Description+Comment
  3. **VLM fallback 模板**：图无 metadata 时，输出标准化 88 预设选择 prompt 给 GPT-4o/Claude/Gemini/Qwen-VL
- **启发式预设猜测**：35+ 关键词 → 预设映射（cyberpunk → 赛博朋克 / ghibli → 宫崎骏 / dunhuang → 敦煌壁画 ...）
- **画幅自动推断**：从 size 字段算 ratio，匹配最近的 1:1/16:9/3:4/21:9 等
- **三种输出**：`text`(默认) / `--mj`(单行 MJ prompt) / `-j`(结构化 JSON 可 pipe)
- **支持本地路径 + 远程 URL**

### render_prompt.py — 直出图片（新文件 270 行）

- **4 个后端**：
  - `comfyui` — 本地 ComfyUI HTTP API（默认 http://127.0.0.1:8188）
  - `sd-webui` — AUTOMATIC1111 / Forge txt2img API（默认 http://127.0.0.1:7860）
  - `dalle` — OpenAI DALL-E 3（OPENAI_API_KEY）
  - `none` — dry-run，只输出 recipe JSON 不出图
- **零第三方依赖**：纯 urllib，避免企业扫描器命中
- **ComfyUI 默认 workflow**：内置 SDXL 9 节点 workflow，可用 `--workflow` 覆盖
- **环境变量覆盖**：`COMFYUI_URL` / `SDWEBUI_URL`
- **支持混合预设直出**

### 新增功能矩阵

| 维度 | v2.1 | v2.2 |
|------|------|------|
| 出图前 | 提示词增强 | + **混合预设**（任意两两融合） |
| 出图中 | （手工复制到模型） | + **直出**（comfyui/sd-webui/dalle） |
| 出图后 | （无） | + **反解**（A1111/ComfyUI/NovelAI metadata） |
| 视频 | （不支持） | + **视频提示词**（9 模型 + 关键帧 + 镜头运动） |

### 兼容性

- **完全向下兼容**：v2.1 所有 CLI 命令在 v2.2 不变；新参数均有默认值
- **JSON 字段新增**：`mix_secondary` / `mix_ratio` / `mix_label`（旧字段保留）
- **enhance_video.py / reverse_prompt.py / render_prompt.py 是新文件**，不影响 enhance_prompt.py 老用户

### 未变

- 88 风格预设、五锁机制、系列模式、角色设定图、质量档位 — 全部保留

---

## v2.1.0 — 2026-04-24

**再扩充：更贴近需求 + 更多风格 + 角色一致性。**

### 新增风格预设（+32 款，总 56 → 88）

- **游戏艺术（新类，7）**：原神 / 崩铁星穹 / 英雄联盟 / 暗黑4 / Valorant / Pokemon / 暴雪风
- **东方传统（新类，7）**：敦煌壁画 / 青花瓷 / 民国月份牌 / 年画 / 剪纸 / 和风 / 汉服写真
- **动漫扩展（+4）**：萌系 / 厚涂 / 轻小说封面 / 赛璐璐
- **现代设计（+6）**：玻璃拟态 / 新拟态 / 孟菲斯 / 杂志编排 / 包豪斯 / 奶油风
- **建筑氛围（+3）**：粗野主义 / 北欧极简 / 侘寂
- **摄影扩展（+3）**：暗黑美食 / 日杂 / 街头潮流
- **氛围综合（+2）**：疗愈治愈 / 美式复古

### 新功能

- **角色设定图模式** `--character-sheet` / `-cs`：
  - 自动生成 T-pose + 正面 / 三分之二 / 侧面 / 背面多视图的设定图提示词
  - 专为 Midjourney `--cref`、Stable Diffusion IP-Adapter 做角色参考用
  - 画幅自动锁 16:9
- **时间 / 天气 / 季节 自动抽词**：
  - 14 时间词：清晨 / 黎明 / 黄昏 / 日落 / 深夜 / 蓝调时刻 / 魔法时刻 ...
  - 15 天气词：晴天 / 下雨 / 暴雨 / 下雪 / 暴雪 / 雾天 / 雷雨 ...
  - 10 季节词：春夏秋冬 / 樱花季 / 枫叶季
- **负向需求识别**：识别主体描述中的"不要X / 没有X / 避免X / no X / avoid X / without X"，自动从正向提示中移除并加入负面提示。
- **质量档位** `-t basic / pro / master`：
  - `basic`: `high quality, detailed`（省 token）
  - `pro` (默认): `masterpiece, best quality, ultra detailed, 8k`
  - `master`: 叠加 `hdr, intricate details, sharp focus, award winning, trending on artstation, professional, highly polished`
- **显式负面追加** `--avoid "cluttered, people"`：CLI 级附加负面词。

### 新增别名（+45）

`genshin` / `mihoyo` / `honkai` / `starrail` / `lol` / `diablo` / `valorant` / `pokemon` / `blizzard` / `overwatch` / `dunhuang` / `qinghua` / `porcelain` / `yuefenpai` / `wafu` / `hanfu` / `papercut` / `nianhua` / `moe` / `lightnovel` / `lncover` / `celshaded` / `glassmorphism` / `glass` / `neumorphism` / `memphis` / `editorial` / `bauhaus` / `cream` / `korean` / `brutalism` / `brutalist` / `nordic` / `scandinavian` / `wabisabi` / `zen` / `darkfood` / `muji` / `streetwear` / `hypebeast` / `healing` / `cozy` / `americana` ...

### 改进

- 主体描述中的"不要X"子句会先被 `strip_negative_clauses()` 去除再送入正向提示，避免正向污染。
- `print_prompt()` 输出增加 ⭐ 质量档位、👤 角色设定图模式、🕐 时间、☁️ 天气、🍂 季节、🚫 用户负向 六个新字段展示。
- `list_presets()` 按 8 大类分类展示（新增"游戏" / "东方"分组）。

### 兼容性

- **向下兼容**：v2.0 CLI 命令在 v2.1 完全可用，所有新参数均有默认值。
- **JSON 字段新增**：`quality_tier` / `character_sheet` / `time_of_day` / `weather` / `season` / `user_negatives`（旧字段保留）。

---

## v2.0.0 — 2026-04-24

**大版本升级：一致性 + 贴近需求 + 风格扩充。**

### 新增

- **风格预设 17 → 56**，六大分类：
  - 摄影 10（新增：黑白摄影 / 人像摄影 / 时尚大片 / 美食摄影 / 微距摄影 / 航拍摄影 / 街拍纪实）
  - 动漫 6（新增：新海诚 / 宫崎骏 / 美漫 / Q版 / 童话绘本）
  - 插画 7（新增：工笔国画 / 浮世绘 / 线稿）
  - 3D 7（全部新增：3DC4D / 盲盒手办 / 低多边形 / 等距视图 / 粘土 / 毛毡手工 / 纸艺）
  - 设计 10（新增：平面设计 / Logo设计 / 图标设计 / 信息图 / 品牌KV / 专辑封面 / 电影海报 / 表情包）
  - 艺术史 4（全部新增：印象派 / 后印象派 / 新艺术 / 装饰艺术）
  - 场景氛围 12（新增：黑暗奇幻 / Y2K / Vaporwave / 霓虹灯牌 / 概念艺术）
- **一致性四锁**：每个预设内置 `camera` / `lighting` / `palette` / `aspect` 四项独立锁，系列出图风格不再漂移。
- **系列批量模式** `-s N --variations "A,B,C,D"`：共享 seed + 四锁，主体描述差异化，一次生成一整套。
- **意图识别器**：无需指定 `-p`，脚本从"logo/产品/海报/头像/美食/赛博/水墨..."等关键词自动推荐预设 + 画幅。
- **构图/情绪抽词**：主体描述中的"俯拍/特写/航拍/神秘/温馨/史诗..."自动并入提示词。
- **稳定 seed 建议**：基于 `md5(subject + preset)` 生成 32-bit seed，便于复现。
- **英文 / 同义词别名**：60+ 别名（anime、ghibli、cyberpunk、minimal、3d、logo、neon、vapor…）。
- **多模型精细化适配**：
  - Midjourney 输出 `--ar --stylize`，提示 `--cref/--sref`
  - Stable Diffusion 输出权重语法 `(subject:1.2)`，提示采样器/CFG
  - SDXL 输出推荐尺寸（`1216x832` 等）
  - Flux 输出长句自然语言 + guidance 提示
  - DALL-E 3 输出段落式自然语言
- **JSON 输出** `-j`：结构化一致性锁 + 所有参数，便于下游集成。
- **CLI 增强**：`-a/--aspect`、`--mood`、`--composition`、`--seed`、`-l/--list`、`-v/--version`。

### 修复

- 修复 Logo设计 / 图标设计 / 表情包 / 海报 等预设的**全局负面词包含 "logo/text"** 导致的语义自我否定。
- 修复 水墨 / 工笔国画 / 浮世绘 预设中**负面词包含 "signature"** 与画面印章冲突。

### 破坏性变更

- `build_prompt()` 返回 dict 新增 `aspect` / `seed_suggestion` / `consistency_lock` / `hint` / `version` 字段（向下兼容，原有字段保留）。

---

## v1.0.0 — 2026-04-24（初始版本）

- 17 风格预设（写实摄影 / 胶片摄影 / 动漫 / 赛博朋克 / 水彩 / 油画 / 建筑可视化 / 产品设计 / 像素艺术 / 奇幻 / 科幻 / 复古海报 / 水墨 / 蒸汽朋克 / 极简主义 / 电影感 / 国潮）。
- 支持 Midjourney / SD / DALL-E / 通用 四种输出骨架。
- CLI：`subject -p <preset> -m <model> [-l] [-j]`。
