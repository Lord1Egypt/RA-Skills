# Changelog

## v3.2.0 — 2026-04-28

**审美锚点系统 + 15 个 Master 档设计师级预设。从"风格预设"升级到"审美锚定"，从 88 流派升级到「88 流派 + 15 大师 + 锚点表」三层。**

### 新增

- **88 预设审美锚点表**（SKILL.md 头部新增章节）：每个预设 → 1-2 个具体导演 / 摄影师 / 艺术家 / 电影场景的锚定（如赛博朋克 → Roger Deakins《Blade Runner 2049》氪绿一段；汉服写真 → 张叔平《一代宗师》室内逆光；ghibli → 《千与千寻》汤屋夕照具体场景）。让 Claude 拼提示词时不只有标签拼接，而是真实意向锚定。
- **15 个 Master 档设计师级预设**：Pentagram / Saul Bass / Massimo Vignelli / Wim Crouwel / Paul Rand / Tibor Kalman / Sagmeister / Paula Scher / Otl Aicher / Bruno Munari / 杉本博司 / 原研哉 / 安藤忠雄 / 王家卫 / Wes Anderson — 用于品牌官网 KV / 高端杂志封面 / 投融资路演主视觉等 Master 档需求。
- **与 huo15 生态联动文档**：design-director v3.0 §二 视觉三元组 → img-prompt v3.2 Master 档预设 → design-critique v2.0 §五 对标的完整流转图。

### 与 design-director v3.0 / design-critique v2.0 的关系

- design-director 选定 Master 档方向时，brief 的 signatureHook 可直接指定本 skill 的 Master 档预设（如 wong-kar-wai / kenya-hara）
- design-critique 评审 Master 档作品时，从 §五 流派 Master 对标库 + 本 skill 锚点表配合做差距分析

### 不变

88 预设主表 / 14 件套脚本 / 一致性四锁 / Claude Vision 五维评审 / 闭环自动迭代 / 故事板 / brand_kit / style_learn 全部保留，纯审美补丁层。

---

## v3.1.0 — 2026-04-27

**稳定加固版：质量基础设施 + 上手文档 + 真实示例。不堆功能，先把底子打牢。**

发完 v3.0 大版本（14 件套、1770 行新代码、3 个新外部 API 集成）后，发现：
- 14 件套互相依赖，没自动化回归 → 改动风险高
- 新用户拿到不知道从哪开始
- 错误处理散在脚本里不统一
- API key / 服务可达性没统一诊断入口

v3.1 不加 feature，只补这些短板。

### 新增 1: doctor.py — 健康检查（~250 行）

```bash
python3 scripts/doctor.py            # 全量
python3 scripts/doctor.py --quick    # 跳过网络
python3 scripts/doctor.py --check api    # 只查 API keys
python3 scripts/doctor.py -j         # JSON 输出
```

检查项：
- 14 个脚本 import + VERSION 一致性
- 7 个 API key（ANTHROPIC 必填，其他按需）
- 2 个本地后端（ComfyUI / SD WebUI）可达性
- 4 个候选 Obsidian vault 路径
- 4 个持久化目录盘点（characters / sessions / brand_kits / learned_presets）
- Claude API 实测 ping（用 haiku 最便宜模型）

输出：彩色 ✓ / ⚠ / ✗ 表格 + 总结统计。

### 新增 2: tests/smoke.py — 自动回归测试（~250 行）

零依赖、纯本地、不调网络。33 个测试覆盖核心 API：

- 版本号一致性（15 个脚本）
- enhance_prompt 核心：resolve_preset / parse_mix_preset / build_prompt / mix / character_sheet / seed 稳定
- compact_prompt 长短场景
- safety_lint 红线 / 艺术化重写 / 双向 catch
- character / brand_kit save-load roundtrip + apply 注入
- variants 共享 seed
- reverse_prompt A1111 解析 + 启发式 preset 猜
- MCP server: initialize / tools/list / tools/call dispatch
- 88 预设字段完整性

```bash
tests/smoke.py            # 全跑
tests/smoke.py --module TestSafetyLint
```

实测：33 测试 0.089 秒跑完。

### 新增 3: examples/ 目录 — 5 个真实可运行示例

| 文件 | 用途 |
|------|------|
| `brand_kit-song_tea.json` | 宋韵东方茶饮品牌套件示例 |
| `character-silver_mecha.json` | 银发机甲少女角色卡 |
| `learned_preset-fresh_film.json` | 清新胶片风学习预设 |
| `storyboard-cat_rainy_night.txt` | 6 帧短片剧本（一只猫的雨夜散步） |
| `recipe-1-brand_kv.sh` | RECIPES 食谱 1 的完整 bash 脚本 |
| `examples/README.md` | 导入指南 |

直接 `cat examples/xxx.json | scripts/<模块>.py --import` 即用。

### 新增 4: QUICKSTART.md — 三层级上手文档

- **30 秒**：第一条命令
- **5 分钟**：基础工作流（推荐预设 → 出图 → 保存角色卡 → 看示例图）
- **30 分钟**：完整工作流（品牌 KV / 风格学习 / 故事板 / IDE / Web UI / Obsidian）
- **6 个 FAQ**：API key 缺失能用哪些功能 / 哪些后端值得配 / prompt 太长怎么办 / 等

### 兼容性

- 纯加固，零 feature 改动
- doctor.py / tests/smoke.py / examples/ / QUICKSTART.md 全是新增
- 14 个 v3.0 脚本不变，仅 VERSION bump 到 3.1.0

### 文件改动

| 改动 | 内容 |
|------|------|
| 新文件 | `doctor.py` / `tests/smoke.py` / `QUICKSTART.md` / `examples/*` (6 文件) |
| VERSION bump | 14 个脚本 v3.0.0 → v3.1.0 |
| 总新增 | ~900 行（含 5 个示例文件） |

### 这一版的意义

| | v3.0 | v3.1 |
|---|------|------|
| 代码质量 | 14 件套手动 smoke | + **33 自动回归** |
| 上手成本 | RECIPES.md 抽象 | + **30 秒/5 分钟/30 分钟分级** |
| 错误诊断 | 各脚本散写 | + **doctor.py 一键体检** |
| 示例素材 | 文档里截图 | + **examples/ 真实文件** |

---

## v3.0.0 — 2026-04-27

**v3.0 大版本：从"提示词工具"升级为「AI 创作生态中枢」。**

四件大武器同时上线：故事板模式 / 品牌套件 / 风格学习引擎 / 创意四件套整合 cookbook。

### E3: storyboard.py — 故事板模式（新文件 ~430 行）⭐ 杀手级 feature

把一段剧本/文案 → Claude 拆 N 关键帧 → 每帧 T2I prompt + 帧间 T2V 衔接 prompt → 完整短片脚本包。

```bash
storyboard.py "一只猫从城市走进雨夜" -p 电影感 --scenes 4 \\
    -m Midjourney --video-model Sora --output ./my_story
```

输出：
- `storyboard.json`（完整 scene + transition 数据）
- `scene-{01-N}-t2i.txt`（每个关键帧的 T2I 提示词）
- `transition-{xx-to-yy}-t2v.txt`（每个转场的 T2V 提示词）
- `README.md`（可读总览 + 生产管线）

亮点：
- 整段共享 base_seed 锁定一致性，主角不漂移
- Claude 自动拆分叙事弧（开场→起→承→转→合）
- 复用 enhance_prompt + enhance_video，所有 88 预设/混合/五锁全部生效
- 视频模型 9 选 1：Sora/Kling/Runway/Pika/Luma/Hailuo/即梦/Wan

**国内目前没有人做到"剧本 → 完整 T2I+T2V 脚本包"这一点。**

### E4: brand_kit.py — 品牌套件持久化（新文件 ~280 行）

品牌 VI 沉淀到 `~/.huo15/brand_kits/<name>.json`，包含 colors / fonts / keywords / forbidden / logo_description。

```bash
brand_kit.py --create song_tea \\
    --colors "#2C5F2D, #97BC62, #F7F4EA" \\
    --fonts "Songti SC, Source Han Serif" \\
    --keywords "宋韵, 极简, 留白, 文人画" \\
    --forbidden "modern digital, neon, cyberpunk"

# 出图时自动注入
enhance_prompt.py "茶饮品牌主视觉" -p 汉服写真 --brand-kit song_tea
```

注入逻辑：
- `colors` → 写入 prompt 作为 brand color palette 提示
- `keywords` → 追加到主体描述
- `forbidden` → 合并到 negative prompt
- `logo_description` → 加入 prompt 作 brand identity 信号

完美对接 `huo15-openclaw-brand-protocol` 的输出（其抓品牌规范的 JSON 可直接 `--import`）。

### C4: style_learn.py — 风格学习引擎（新文件 ~330 行）

给 N 张参考图（≥2），Claude Vision 提取每张特征 → 综合共性 → 生成 learned preset。

```bash
style_learn.py --name 我的小清新 ref1.jpg ref2.jpg ref3.jpg

# 后续直接用 @ 前缀调用
enhance_prompt.py "猫咪" -p "@我的小清新"
```

技术细节：
- 每张图调一次 Claude Vision 提取 tags/camera/lighting/palette/aspect
- 综合阶段让 Claude 统一归纳，输出和 STYLE_PRESETS schema 兼容的 spec
- 自带 `confidence` 字段（共性强度 0-1，< 0.5 警告太散）
- 存到 `~/.huo15/learned_presets/<name>.json`，运行期注册到 STYLE_PRESETS（不污染源文件）
- `resolve_preset` 支持 `@<name>` 前缀

### G2: RECIPES.md — 创意四件套整合食谱

新文档：5 个端到端食谱，演示 huo15-img-prompt 和其他 huo15-openclaw-* 技能联动：
1. **品牌 KV 全流程**（design-director → brand-protocol → brand_kit → img-prompt → design-critique → frontend-design）
2. **自学习风格 + 角色一致性 + 视频短片**（style_learn → character → storyboard）
3. **电商商品图全套**（brand_kit + variants + character + obsidian）
4. **Claude Code MCP 工作流**（IDE 内自然语言调用）
5. **knowledge-base 联动**（资产沉淀到知识库）

设计原则：
- 每个技能管自己一段（不重复造轮子）
- 数据格式互通（brand_kit / character / learned_preset 都是标准 JSON）
- Claude Code + MCP 当协调者
- 闭环优先（v2.5 的 image_review 免费用）

### enhance_prompt.py 集成

- 新增 `--brand-kit <name>` 加载品牌套件
- `resolve_preset` 支持 `@<name>` 前缀加载 learned preset

### 所有新文件（v3.0 共 ~1800 行）

| 文件 | 行数 | 关键能力 |
|------|------|---------|
| `storyboard.py` | 430 | 剧本 → 视频脚本包 |
| `brand_kit.py` | 280 | 品牌套件持久化 |
| `style_learn.py` | 330 | 风格学习引擎 |
| `RECIPES.md` | 250 | 创意四件套食谱 |
| `enhance_prompt.py` | + 50 | brand-kit 注入 + @learned 解析 |

### 兼容性

- 完全向下兼容 v2.6
- 所有新参数有默认值
- learned preset 用 `@` 前缀，不与 88 内置预设冲突
- 新文件不影响老脚本

### 这一版的定位升级

| | v2.x | v3.0 |
|---|------|------|
| 输入 | 一句话主体 | 一段剧本 / 多张参考图 / 品牌规范 |
| 输出 | 单帧 prompt | **完整短片脚本包** / **学到的新预设** / **品牌一致出图** |
| 个性化 | 88 内置预设 | + **用户自学习风格** + **品牌套件** |
| 生态位 | 独立工具 | + **创意四件套核心节点**（食谱整合 5 个 huo15 技能） |

---

## v2.6.0 — 2026-04-27

**用户体验大版本：从 CLI 工具变成 GUI/IDE/笔记三栖产品。**

### E1: character.py — 角色卡持久化（新文件 220 行）

- 把 `--character-sheet` 模式的输出（subject 描述 + seed + camera/lighting/palette 五锁）存到 `~/.huo15/characters/<name>.json`
- 新增两个 enhance_prompt.py 参数：
  - `--save-char <name>` 保存当前调用为角色卡
  - `--char <name>` 加载角色卡，自动注入主体 + 锁 seed/preset/aspect
- 角色卡含 `use_count` 自增计数 + `created_at` / `updated_at` 时间戳
- 独立 CLI 管理：`character.py --list / --show / --delete / --export / --import`
- 用例：
  ```bash
  # Turn 1: 创建角色
  enhance_prompt.py "银发机甲少女 twin tails glowing visor" -p 动漫 \\
      --character-sheet --save-char 银发机甲少女
  
  # Turn 2 ~ N: 复用，多张图角色一致
  enhance_prompt.py "在霓虹街头" --char 银发机甲少女 -p 赛博朋克
  enhance_prompt.py "在花海中" --char 银发机甲少女
  ```

### D2: Obsidian 集成 — `--obsidian` 写入 vault

- 自动检测 vault 路径（环境变量 `OBSIDIAN_VAULT` → `~/knowledge/huo15` → `~/Documents/Obsidian` → `~/Obsidian`）
- 写入 `<vault>/图集/{date}-{subject}-{seed}.md`
- 完整 frontmatter（tags/preset/model/aspect/seed/tier/version/date/mix）
- markdown body 包含：原始描述、正负向提示词、一致性锁、元信息、Claude 润色记录、VLM 评审、复现 CLI 命令
- 跟用户记忆里的"L3 共享 KB wiki"层级吻合，完成 huo15 三层记忆生态闭环

### D3: mcp_server.py — MCP stdio server（新文件 280 行）

让 **Claude Code / Cursor / Cline / Continue.dev** 等 MCP IDE 直接调用本技能的 9 个工具：

- `enhance_prompt` — 88 预设 + 五锁
- `list_presets` / `preset_examples` — 浏览预设 + 5 平台参考图链接
- `suggest_presets` / `polish_prompt` — Claude 智能推荐 + 润色
- `safety_lint` — 平台合规检查
- `review_image` — Claude Vision 五维评审
- `list_characters` / `load_character` — 角色卡管理

实现细节：
- **手写 JSON-RPC 2.0 over stdio**，零第三方依赖（不引 mcp SDK）
- 完整 MCP 协议：initialize / tools/list / tools/call
- 注册到 `~/.claude/mcp.json`：
  ```json
  {
    "mcpServers": {
      "huo15-img-prompt": {
        "command": "python3",
        "args": ["/path/to/scripts/mcp_server.py"]
      }
    }
  }
  ```

### D1: web_ui.py — 本地 Web UI（新文件 380 行）

```bash
python3 web_ui.py             # 默认 http://127.0.0.1:7155
python3 web_ui.py --port 8080
python3 web_ui.py --no-browser
```

- 单文件 HTML（vanilla JS + Tailwind CDN，零构建）
- Python `http.server.ThreadingHTTPServer` 当后端，零第三方依赖
- 三栏布局：
  - 左：主体输入 + 混合预设权重 + 画质 + 模型 + 画幅 + 角色卡选择
  - 中：88 预设可视化卡片，按 9 大类分组，搜索过滤
  - 右：实时正/负向提示词 + 一致性锁表格 + 元信息 + 一键复制
- 自动开浏览器、Ctrl+C 退出

### 全部新文件（v2.6 共 ~880 行）

| 脚本 | 行数 | 用户群 |
|------|------|--------|
| `character.py` | 220 行 | CLI + 程序化复用 |
| `mcp_server.py` | 280 行 | IDE 用户（Claude Code/Cursor） |
| `web_ui.py` | 380 行 | 设计师/产品经理（GUI） |
| `enhance_prompt.py` | + 80 行（save-char/char/obsidian + helpers） | — |

### 兼容性

- 完全向下兼容 v2.5
- 新参数有默认值
- 新文件不影响老脚本

### 用户群拓展

| 之前 | 现在 |
|------|------|
| 命令行用户 | + IDE 用户（MCP）+ GUI 用户（Web UI）+ Obsidian 用户 |
| 单次调用 | + 跨调用一致性（角色卡）+ 三层记忆同步（Obsidian） |

---

## v2.5.0 — 2026-04-27

**核心护城河上线：图生评审 + 闭环自动迭代。GPT-4o image / Claude Imagen 内部都做不到。**

### C1: image_review.py — Claude Vision 五维评审（新文件 320 行）

- 调 Claude Sonnet 4.5 Vision 评审一张图
- 五维结构化打分（0-10）：subject_match / composition / lighting / palette / technical
- 输出加权 overall_score（subject 0.3 / composition 0.2 / lighting 0.2 / palette 0.15 / technical 0.15）
- 三档 verdict：PASS ≥ 7.5 / RETRY 5-7.5 / REJECT < 5
- **可执行修复**：每个 issue 不写"光线不好"，直接给"add: golden hour rim light, soft fill from camera left"
- 多图排名：`image_review.py a.png b.png c.png --rank` 自动批量评审排序
- 简评模式 `--quick`（只输出 overall_score，省 token）
- 完整模式启用 prompt caching，多图调用省 90% input token

### C2: auto_iterate.py — 闭环自动迭代（新文件 350 行）

把整个流程串成闭环：

```
enhance_prompt → render → image_review → 不达标？让 Claude 改 prompt → 回到第一步（≤ 3 轮）
```

- 9 个后端可选（DALL-E / SD-WebUI / ComfyUI / Replicate / Fal / 即梦 / 可灵 / 海螺）
- 整轮锁定 seed，便于对比每轮的 prompt 改动到底改善了哪一维
- Claude 改 prompt 的 system prompt 单独设计，输入是上轮评审，输出是 revised_subject + extra_negatives + extra_mood + rationale
- 每轮 trace 全保留（subject + recipe + image_path + review + revision），最终选最高分
- 用例：
  ```bash
  auto_iterate.py "持剑女侠" -p 赛博朋克 --backend dalle --target 7.5 --max-rounds 3
  ```

### C3: enhance_prompt.py 加 `--variants N`（A/B 测试）

- 同 subject + 同 seed，仅在指定轴上分化
- 内置 4 维差异轴：mood / composition / lighting / stylize
- `--variant-axes mood,composition` 选差异轴（默认这俩）
- 用例：
  ```bash
  # 出 4 个变体（mood × composition 笛卡尔积取 4 个）
  enhance_prompt.py "持剑女侠" -p 赛博朋克 --variants 4 -j > variants.json

  # 出图后挑最优（用 image_review.py 排名）
  for f in renders/*.png; do echo "$f"; done | xargs image_review.py --rank
  ```

### A1: 智能预设推荐 `--suggest`

- 解决"温柔感"、"高级感"等模糊描述匹配不到预设的痛点
- 让 Claude 看用户描述 + 88 预设清单，返回 **top 3** 候选
- 每个候选附 score (0-1) + 一句话 reason + best_subject_example
- 同时给 mix_suggestion（自动判断该不该混合）
- 同时暴露在 `enhance_prompt.py --suggest` 和 `claude_polish.py --suggest`
- 用例：
  ```bash
  enhance_prompt.py "温柔治愈感的画面" --suggest
  # → top_3: 疗愈治愈 / 奶油风 / 童话绘本，附理由 + 适合主体
  ```

### 兼容性

- 完全向下兼容 v2.4
- 新文件 `image_review.py` / `auto_iterate.py` 不影响老脚本
- 所有新参数有默认值

### 文件改动

| 文件 | 改动 |
|------|------|
| `scripts/image_review.py` | 新文件 320 行 |
| `scripts/auto_iterate.py` | 新文件 350 行 |
| `scripts/enhance_prompt.py` | + 100 行（variants + suggest dispatch） |
| `scripts/claude_polish.py` | + 90 行（suggest_presets 函数 + CLI） |
| 其他 4 脚本 | VERSION bump |

### 真实差异化

这一版做完，huo15-img-prompt 有了 GPT-4o image / Claude Imagen 都没有的能力：
- **闭环反馈**：能告诉用户"这张图差在哪"+"下轮怎么改"
- **可解释性**：5 维分项打分 + 改进 trace 全留
- **多模型协作**：Claude 评审 + DALL-E/Replicate/即梦 出图，跨厂商组合
- **A/B 实验**：同 seed 控变量比较

---

## v2.4.0 — 2026-04-27

**补齐 CLI 体验：扩 7 后端、prompt 压缩、参考图链接、多轮编辑。**

### B1+B2: render_prompt.py 扩 7 个后端

| 后端 | 环境变量 | 用例 |
|------|---------|------|
| `replicate` | `REPLICATE_API_TOKEN` | `--remote-model black-forest-labs/flux-schnell` |
| `fal` | `FAL_KEY` | `--remote-model fal-ai/flux/schnell` |
| `jimeng` | `ARK_API_KEY`（火山方舟） | 字节即梦 / Seedream 3.0 |
| `kling` | `KLING_API_KEY` | 快手可灵 v1 |
| `hailuo` / `minimax` | `MINIMAX_API_KEY` | 海螺 image-01 |

加上原有的 `comfyui` / `sd-webui` / `dalle` / `none(dry-run)`，**共 10 个后端**。

### F2: enhance_prompt.py 加 `--compact`

- 自动估算 prompt token 数（中文按字、英文按 1.3 token/word）
- 超过 CLIP 77 token 触发压缩：去重 + 同义合并 + 按权重保留
- 必保头 6 段（主体 + camera 锁），尾部按预算砍
- 输出 `compaction` meta：before/after token 数、砍了几段
- 实测：v2.3 长 prompt 124 → 73 tokens（不损失主体）

### F1: enhance_prompt.py 加 `--examples` / `--with-examples`

- 88 预设全量映射到搜索关键词（`PRESET_SEARCH_TERMS`）
- 实时生成 5 平台搜索 URL：Lexica / Civitai / Pinterest / Google Images / Unsplash
- 用法：
  - `enhance_prompt.py --examples 敦煌壁画` 单预设的 5 平台链接
  - `enhance_prompt.py -l --with-examples` 列表模式带链接
- **零维护策略**：不内置静态图 URL，靠搜索 query 永远有效

### A2: enhance_prompt.py 加 `--session` / `--continue`

- 持久化目录 `~/.huo15/sessions/<name>.json`
- `--session catwindow` 保存当前调用
- `--continue catwindow` 加载历史 session 作为默认值，**自动锁定 seed** 保持多轮一致性
- CLI 参数 > session 默认值 > 系统默认（标准三层覆盖）
- `--list-sessions` 列出全部历史
- 用例：

```bash
# Turn 1
enhance_prompt.py "猫坐在窗台" -p 写实摄影 --session catwindow
# Turn 2: 改画幅 + 加情绪，seed 自动锁定保证主体一致
enhance_prompt.py --continue catwindow --aspect 16:9 --mood 治愈
# Turn 3: 完全换主体描述但保 seed 测一致性
enhance_prompt.py "猫站起来伸懒腰" --continue catwindow
```

### 兼容性

- 完全向下兼容 v2.3，所有新参数有默认值
- session 文件格式版本化（`name`/`iterations[]`/`latest`/`count`），未来扩字段不破坏老文件

### 文件改动

| 文件 | 改动 |
|------|------|
| `scripts/enhance_prompt.py` | + 220 行（compaction + sessions + preset URLs） |
| `scripts/render_prompt.py` | + 230 行（5 后端函数） |
| 其他 4 脚本 | 仅 VERSION bump |

---

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
