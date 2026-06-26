---
name: "minecraft-mod-search"
description: >
  Search and recommend Minecraft Java Edition mods from multiple platforms
  (Modrinth, CurseForge). Use when the user describes mod functionality needs,
  provides a mod name, or asks about Minecraft Java mods, mod packs, or
  compatible mod recommendations. Also use when the user provides a modpack
  concept (e.g. "我要做一个科技整合包，1.20.4，forge，包含自动化、能源、物流")
  and needs AI to analyze requirements, decompose into components, recommend
  best-fit mods for each, and verify MC version and inter-mod compatibility.
  Triggers include: "帮我找个XX功能的mod", "搜索XX mod", "我的世界mod推荐",
  "XX模组兼容吗", "mod依赖", "forge模组", "fabric模组", "1.20.4 mod",
  "minecraft java mod search", "整合包", "modpack推荐", "科技包", "魔法包",
  "生存包", "我的世界1.20.4 forge 整合包", "枪械mod", "枪包", "tacz",
  "枪模组", "手枪", "步枪", "霰弹枪", "狙击枪", "左轮", "火枪", "射击mod",
  "gun mod", "firearm", "gun pack", "tacz gunpack",
  "机械动力", "create", "create mod", "create addon", "传送带", "齿轮",
  "自动化", "流水线", "旋转动力", "蒸汽", "铁路", "机械", "工厂",
  "conveyor", "gear", "automation", "kinetic", "mechanical".
---

# Minecraft Java Mod Search Skill

## 1. 概述

本技能帮助用户在 Minecraft Java Edition 生态中搜索和推荐模组（Mod）。支持多平台搜索、智能排序、依赖解析、版本过滤和卡片化结果展示。

## 2. 支持的平台

| 平台 | API 类型 | 国内可访问性 | API Key | 优先级 |
|------|----------|-------------|---------|--------|
| **快查表** | 本地文件 | ✅ 离线 | ❌ 不需要 | 🥇 最优先 |
| **Modrinth** | REST API | ✅ 可裸连 | ❌ 不需要 | 🥈 主平台 |
| **CurseForge** | REST API | ⚠️ 需 Key | ✅ 需要（免费） | 🥉 备选 |
| **MC百科 mcmod.cn** | 网页抓取 | ✅ 国内直连 | ❌ 不需要 | 4️⃣ 兜底补充 |

> **策略**：
> 1. 快查表优先（离线命中，零延迟）
> 2. Modrinth 多关键词并行搜索（asyncio+aiohttp，超时 8s）
> 3. CurseForge 若有 API Key 则并行搜索（超时 5s）；**无 Key 时在回答中提示用户如何填写**
> 4. Modrinth 结果 < 3 条时，抓取 MC百科搜索页补充（超时 8s）

### CurseForge API Key 配置方法

1. 前往 https://console.curseforge.com/ 申请免费 API Key
2. 编辑 `references/curseforge_api.md`，在文件末尾添加：`CF_API_KEY=你的key`
3. 或设置环境变量：`export CF_API_KEY=你的key`
4. 或运行时通过 `--api-key 你的key` 参数传入

## 3. 搜索参数

用户可通过以下任意维度进行单一或组合搜索：

| 参数类型 | 示例 | 说明 |
|---------|------|------|
| **功能描述** | "帧率优化"、"自动 farming"、"新增生物群系" | AI 解析并转换为搜索关键词 |
| **模糊/精确名称** | "OptiFine" / "optif" | 支持前缀匹配和精确搜索 |
| **游戏版本** | "1.20.4"、"1.19.2"、"1.18.2" | 自动过滤不兼容版本 |
| **前置依赖** | "forge"、"fabric"、"rift" | 仅返回指定 Loader 的 Mod |
| **类别** | "科技"、"魔法"、"生存"、"装饰"、"优化" | 按分类筛选 |

### 搜索优先级规则

```
组合搜索 > 精确名称 > 模糊名称 > 功能描述
```

- 若用户提供精确 Mod 名称，优先精确匹配，再横向扩展推荐相似 Mod
- 若提供功能描述，将描述拆分为关键词进行多词联合搜索
- 版本参数：默认返回与指定版本兼容的最新 Mod，**不兼容版本自动过滤**
- Loader 参数：优先识别 Forge / Fabric / Quilt / Rift

## 4. 搜索执行流程

### Step 1 — 解析用户输入

从用户描述中提取以下字段：

- `query`: 搜索关键词（功能描述 / Mod 名称）
- `minecraft_version`: 游戏版本（如 1.20.4）
- `loader`: 加载器类型（forge / fabric / quilt / rift）
- `category`: Mod 类别

若用户未指定版本，询问确认或使用当前主流版本（优先 1.20.4 / 1.21.x）。

### Step 1.2 — 快查表优先命中（新功能）

在所有 API 搜索之前，**先检索 `references/mod_quickref.md`**：

```
search_quickref(query, version)
    │
    ├─ 命中 → 优先展示快查表结果（带 [📚 快查表] 标记）
    │         后续 API 搜索继续进行作为补充
    │
    └─ 未命中 → 继续 Step 1.5
```

快查表查询时同时匹配：Mod 名称、slug、功能描述、分类关键词、同义词表。

### Step 1.3 — 多关键词提取（新功能）

从用户查询中提取 **3-5 个候选搜索词**，并行发起搜索：

```python
keywords = _extract_keywords(query)
# 示例：query="自然生成的中立幸存者 NPC"
# 提取：["survivor", "npc", "neutral", "spawn"]
```

提取策略：
- 中文词通过 `_CN_EN_MAP` 映射为英文
- 保留查询中的英文词
- 最多 5 个候选词，去重

### Step 1.5 — 枪械意图检测与 TACZ 优先搜索

**当检测到用户查询涉及枪械/武器类需求时**，优先使用 TACZ（Timeless and Classics Zero）枪包生态搜索，而非普通 Mod 搜索。

#### 枪械意图关键词

以下关键词命中时自动触发 TACZ 优先模式：

| 语言 | 关键词 |
|------|--------|
| 中文 | 枪、枪械、枪包、枪mod、枪模组、射击、武器、手枪、步枪、狙击、霰弹、冲锋枪、机枪、左轮、燧发枪、火枪、现代战争、军事、弹药、子弹 |
| 英文 | gun, firearm, weapon, pistol, rifle, sniper, shotgun, smg, machine gun, revolver, musket, gunpack, gun pack, tacz, bullet, ammo, fps, combat, warfare, military |

#### TACZ 优先搜索流程

```
用户查询 "步枪" (含枪械关键词)
    │
    ├─ detect_gun_intent(query) == True ?
    │       │
    │       ├─ Yes → search_tacz_gunpacks(query, version, loader)
    │       │         │
    │       │         ├─ 策略1: "tacz <英文关键词>" + facets=[equipment + version]
    │       │         ├─ 策略2: "tacz <英文关键词>" + facets=[version]（无分类限制）
    │       │         │
    │       │         ├─ 找到结果 → 输出 TACZ 基础 Mod + 枪包列表
    │       │         │                包含：安装路径、枪包放置说明、依赖关系
    │       │         │
    │       │         └─ 无结果 → 回退到普通 Mod 搜索（Step 2）
    │       │
    │       └─ No → 直接进入普通 Mod 搜索（Step 2）
```

#### TACZ 枪包搜索特点

| 特点 | 说明 |
|------|------|
| **基础 Mod** | `timeless-and-classics-zero`（Forge 1.18.2–1.20.1），Fabric 有非官方移植 `tacz-refabricated` |
| **枪包格式** | `.zip` 压缩包，放入 `.minecraft/tacz/` 目录后执行 `/tacz reload` |
| **搜索平台** | Modrinth（category=`equipment`），脚本自动将中文枪械词翻译为英文关键词 |
| **多枪包共存** | 支持，命名空间不冲突即可同时加载 |
| **依赖解析** | 自动提取枪包的 required 前置依赖并补入结果列表 |

#### TACZ 相关参考

详细的 TACZ 生态信息（枪包安装路径、已知枪包列表、兼容性规则）参考：`references/mod_compat.md` 第 12 节。

### Step 1.6 — 机械/自动化意图检测与 Create 优先搜索

**当检测到用户查询涉及机械、自动化、科技类需求时**，优先使用 Create（机械动力）附属 mod 搜索，而非普通 Mod 搜索。

#### 机械/自动化意图关键词

以下关键词命中时自动触发 Create 优先模式：

| 语言 | 关键词 |
|------|--------|
| 中文 | 机械、机械动力、自动化、传送带、齿轮、活塞、动力、轴承、铁路、火车、旋转、应力、流水线、工厂、制造、加工、搅拌、碾压、装配、机械臂、部署器、蒸汽、风车、水车 |
| 英文 | create mod, create addon, conveyor, belt, gear, pulley, bearing, piston, automation, factory, assembly, mechanical, train, railway, steam, windmill, waterwheel, rotational, kinetic, stress, deployer, mixer, press, millstone |

#### Create 优先搜索流程

```
用户查询 "传送带" (含机械/自动化关键词)
    │
    ├─ detect_create_intent(query) == True ?
    │       │
    │       ├─ Yes → search_create_addons(query, version, loader)
    │       │         │
    │       │         ├─ 策略1: "create <英文关键词>" + facets=[technology + version]
    │       │         ├─ 策略2: "create <英文关键词>" + facets=[version]（无分类限制）
    │       │         │
    │       │         ├─ 找到结果 → 输出 Create 基础 Mod + 附属 mod 列表
    │       │         │                包含：功能描述、版本兼容、依赖关系
    │       │         │
    │       │         └─ 无结果 → 回退到普通 Mod 搜索（Step 2）
    │       │
    │       └─ No → 直接进入普通 Mod 搜索（Step 2）
```

#### Create 附属 mod 搜索特点

| 特点 | 说明 |
|------|------|
| **基础 Mod** | `create`（Forge + Fabric 双平台），需配合 Flywheel（Forge 版） |
| **附属生态** | Steam 'n' Rails、Crafts & Additions、Slice & Dice、Big Cannons、Copycats+ 等 100+ 附属 |
| **搜索平台** | Modrinth（category=`technology`），脚本自动将中文机械词翻译为英文关键词 |
| **版本支持** | 1.14.4 / 1.15.2 / 1.16.5 / 1.18.2 / 1.19.2 / 1.20.1 |
| **依赖解析** | 自动提取附属 mod 的 required 前置依赖并补入结果列表 |
| **OptiFine 警告** | Create 与 OptiFine 不兼容，需使用 Oculus（Forge）或 Iris（Fabric） |

#### Create 相关参考

详细的 Create 生态信息（核心机制、已知附属 mod、兼容性规则）参考：`references/mod_compat.md` 第 13 节。

### Step 2 — 执行多平台并发搜索（新功能：asyncio + aiohttp）

**性能改进**：脚本使用 asyncio + aiohttp 并发请求，多关键词并行发起，同步等待最快结果。

**Modrinth（主平台）**：
- 调用 `GET https://api.modrinth.com/v2/search`（并发 3-5 个关键词）
- 参数：`query`, `facets=[categories, versions, loaders]`，每请求超时 `DEFAULT_TIMEOUT=8s`
- 总并发超时：`MULTI_SEARCH_TIMEOUT=12s`
- 参考文档：`references/modrinth_api.md`

**CurseForge（备选）**：
- 调用 `GET https://api.curseforge.com/v1/mods/search`
- 参数：`gameId=432`, `searchFilter`, `classId`（mods=6）
- 参考文档：`references/curseforge_api.md`
- **⚠️ 注意**：需要 `X-API-Key` 请求头。若未配置，**在回答中明确告知用户**：
  > "当前未设置 CurseForge API Key，已跳过该平台搜索。前往 https://console.curseforge.com/ 申请免费 Key，然后编辑 `references/curseforge_api.md` 填写。"

**MC百科 mcmod.cn（兜底补充）**：
- **仅在 Modrinth 搜索结果 < 3 个时触发**
- URL：`https://www.mcmod.cn/s?key=<query>&mold=1&version=<version>`
- 优先使用原始中文查询词（MC百科是中文数据库，中文命中率更高）
- 解析结果补充到搜索列表末尾，标注 `[MC百科]`
- 超时设置 8s，失败静默跳过

### Step 3 — 数据合并与去重（优先级：快查表 > Modrinth > CurseForge > MC百科）

- 快查表命中结果放在最前面，标注 `[📚 快查表]`
- 相同 Mod 在多平台出现时，保留下载量更高的记录，并标注来源
- **去重规则**：优先保留 Modrinth 记录（生态更活跃），其次 CurseForge

### Step 4 — 依赖关系解析（默认关闭，`--deps` 参数开启）

**重要变更（v2.0）**：为提升搜索速度，依赖查询**默认关闭**。

- 默认模式：不额外发起 `/dependencies` API 请求（比 v1.0 快约 3-5x）
- 开启方式：脚本传入 `--deps` 参数，或在需要时告知用户该参数
- 开启后使用 asyncio 并发查询所有 Mod 的依赖，不会串行卡顿

**依赖查询逻辑（开启时）**：

1. 提取 `dependencies` 字段
2. 识别前置 Mod（如 Sodium → Fabric API）
3. 若前置 Mod 未在结果中，自动调用 API 补充查询
4. 将依赖 Mod 合并到推荐列表中，标注为 `[前置依赖]`

### Step 5 — 智能排序

按以下权重综合评分（满分 100）：

| 维度 | 权重 | 说明 |
|------|------|------|
| **下载量** | 30% | 标准化到 0-100，取对数平滑 |
| **更新频率** | 25% | 最近 6 个月内更新 = 100，每增加 1 年 -20 |
| **评价指数** | 25% | 下载量 × 评分系数 |
| **版本匹配度** | 20% | 完全匹配指定版本 = 100，邻近版本 = 60 |

### Step 6 — 过滤不兼容 Mod

- 过滤条件：`game_versions` 不包含用户指定版本 → 标记为 `[版本不兼容]` 并降权
- 若 Mod 无版本标注，跳过该过滤

## 5. 结果展示

### 卡片化展示

每个 Mod 以独立卡片形式展示，结构如下：

```
┌─────────────────────────────────────────────┐
│  [🏷️ 类别标签]  [🔧 Loader标签]               │
│                                             │
│  Mod 名称                                   │
│  作者：<author>   发布：<date>                │
│                                             │
│  📥 下载量：<downloads>  ⭐ 收藏：<favorites>  │
│  🎮 游戏版本：<versions>                     │
│                                             │
│  简介：<description, 最多3行>               │
│                                             │
│  🔗 链接：<modrinth_link> / <cf_link>      │
│  ⚠️ 警告：<dependency_note> / <update_note>  │
└─────────────────────────────────────────────┘
```

### 特殊标注

- `[🔥 推荐]` — 综合评分 Top 3 Mod
- `[⬆️ 需前置]` — 存在未安装的前置依赖
- `[⚠️ 久未更新]` — 超过 12 个月未更新
- `[🚫 版本不兼容]` — 与指定游戏版本不兼容
- `[🇨🇳 国内可直连]` — 来源为 Modrinth

### 推荐排序输出顺序

1. 🔥 综合评分 Top 3（带推荐理由）
2. ✅ 版本兼容 + 无需依赖的 Mod
3. ⬆️ 需要前置依赖的 Mod（依赖也需安装）
4. ⚠️ 久未更新的 Mod（低优先级）

## 6. 脚本工具（v2.0）

核心搜索脚本位于 `scripts/search_mods.py`。

**v2.0 新特性**：
- `asyncio + aiohttp` 并发请求（需安装 `pip install aiohttp`；无 aiohttp 时自动降级到同步模式）
- 多关键词并行搜索（`_extract_keywords` 提取 3-5 个候选词）
- 快查表优先命中（`references/mod_quickref.md`）
- 默认不查依赖（用 `--deps` 开启）
- CurseForge API Key 未配置时输出提示信息
- Modrinth 结果 < 3 条时自动触发 MC百科补充搜索
- 所有请求统一设置超时时间（`DEFAULT_TIMEOUT=8s`），避免卡死

### 安装依赖

```bash
pip install aiohttp  # 强烈推荐，启用并发模式
```

### 使用方法

```bash
# 普通 Mod 搜索（async 并发，多关键词）
python scripts/search_mods.py --query "帧率优化" --version "1.20.4" --loader "fabric"
python scripts/search_mods.py --query "自然生成的中立幸存者 NPC" --version "1.20.1"

# 开启依赖查询
python scripts/search_mods.py --query "存储系统" --version "1.20.1" --deps

# TACZ 枪包搜索（自动检测枪械意图）
python scripts/search_mods.py --query "步枪" --version "1.20.1" --loader "forge"

# Create 附属 mod 搜索（自动检测机械/自动化意图）
python scripts/search_mods.py --query "传送带" --version "1.20.1"

# 整合包分析模式
python scripts/search_mods.py --modpack --query "科技包" --version "1.20.1" --loader "forge" --directions 能源 自动化 物流
```

### 参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--query` | （必填） | 搜索关键词 |
| `--version` | 无 | Minecraft 版本，如 1.20.4 |
| `--loader` | 无 | 加载器类型（forge/fabric/quilt） |
| `--platform` | all | 搜索平台（modrinth/curseforge/all） |
| `--limit` | 15 | 返回结果数量 |
| `--timeout` | 8 | 单请求超时（秒） |
| `--api-key` | 无 | CurseForge API Key |
| `--output` | text | 输出格式（text/json） |
| `--deps` | False | **开启依赖查询**（默认关闭） |
| `--modpack` | False | 启用整合包分析模式 |
| `--directions` | 无 | 整合包各功能方向关键词（配合 --modpack） |

## 7. Mod 快查表（新模块）

快查表文件位于 `references/mod_quickref.md`，包含：

- **热门/经典 Mod 数据**（Modrinth 热门榜 2025-05 整理）
- **按分类组织**：前置库、性能优化、存储、机械动力、魔法、食物农业、NPC/村民、枪械、建筑装饰等
- **关键词同义词对照表**（便于 AI 意图扩展匹配）
- **数据格式**：`- 英文名 | slug: xxx | 功能描述 | 支持加载器和版本`

### 快查表匹配规则

| 匹配优先级 | 条件 | 加分 |
|----------|------|------|
| 1（最高） | Mod 名称在查询中或查询在名称中 | +100 |
| 2 | slug 在查询中 | +80 |
| 3 | 提取关键词命中快查表 keywords 字段 | +30/词 |
| 4 | 分类名称在查询中 | +20 |
| 5（扣分） | 版本不匹配 | -20 |

### 更新快查表

当发现有价值的新 Mod 时，在对应 `## 分类` 下追加一行：

```markdown
- Mod英文名 [| 中文名] | slug: slug名 | 功能描述（20字以内）| fabric/forge 版本范围
```

## 8. 版本兼容性参考

Minecraft Java Edition 主要版本及兼容性说明参考：
`references/mc_versions.md`

## 9. 整合包分析模式（Modpack Analyzer）

当用户提供**整合包设想**（含 MC 版本 + 多功能方向）时，启用本模式。

### 8.1 触发条件

以下表述任一出现即触发：

- "做一个整合包" / "modpack" / "整合包推荐"
- "我想玩科技包" / "魔法包" / "生存包" / "工业包"
- 描述中包含 **3 个及以上功能方向**（如自动化 + 能源 + 物流 + 机器）
- "这些 mod 兼容吗" / "帮我配一个包" / "推荐一个 1.20.4 的整合包"

### 8.2 分析流程

#### Step A — 解析整合包需求

从用户描述中提取：

| 字段 | 来源 | 示例 |
|------|------|------|
| `minecraft_version` | 用户明确指定或询问确认 | `1.20.4` |
| `loader` | 用户指定或根据方向推断 | `forge` / `fabric` |
| `功能方向列表` | 从描述中拆解 | `["自动化农场", "能源管理", "物流传输", "机器制造"]` |
| `包规模` | 从描述推断或询问 | `轻量(10-20个)` / `中型(20-50个)` / `大型(50+个)` |

**功能方向 → 关键词映射**：

| 功能方向 | 搜索关键词（英文） | 对应 Mod 类别 |
|---------|----------------|--------------|
| 帧率优化/性能 | optimization, fps boost, performance | optimization |
| 基础优化 | sodium, lithium, phosphor, ferritecore | optimization |
| 自动化农场 | auto farm, mob farm, crop automation | farming, automation |
| 能源管理 | energy, power, rf, eu, generator | technology, energy |
| 物流传输 | logistics, pipes, item transport | technology, storage, transportation |
| 机器制造/工业 | industrial, factory, machines | technology |
| 魔法/法术 | magic, spells, enchantment, Thaumcraft | magic |
| 新增生物 | new mobs, creatures, vanilla+ | mobs, nature |
| 存储管理 | storage, inventory, warehouse | storage, organization |
| 战斗增强 | combat, weapons, armor | equipment, combat |
| 建筑/装饰 | building, decoration, aesthetics | decoration, construction |
| 科技/红石替代 | automation, redstone, computercraft | redstone, technology |
| 探索/地牢 | adventure, dungeon, exploration | adventure |
| 生态/生物群系 | biomes, terrain, generation | nature, world generation |
| 工具/物品 | tools, items, utility | equipment, utility |
| 村民交易 | villager, trades | gameplay, economy |
| 地狱/末地 | nether, end, dimensions | adventure |

#### Step B — 逐方向搜索最佳 Mod

对每个功能方向，按以下优先级选取最佳 Mod：

1. 在该方向中**下载量最高**且**版本兼容**的 Mod → 标记为 `[🔥 核心推荐]`
2. 补充 1-2 个**功能互补**的备选 Mod → 标记为 `[✅ 备选]`
3. 自动查询每个推荐 Mod 的**前置依赖**，补入推荐列表

**单方向 Mod 选取规则**：

- 每个功能方向最多推荐 **3 个 Mod**（1 个核心 + 2 个备选）
- 优先选择**同一个 Loader** 下的 Mod（减少兼容性问题）
- 若多个 Mod 功能高度重叠（同类替代），只推荐 1 个

#### Step C — 整体兼容性检查

**MC 版本兼容性验证**：

对整合包中所有推荐 Mod 逐一验证：

```
for mod in all_recommended_mods:
    if target_version not in mod.game_versions:
        mark [🚫 版本不兼容: mod_name — 最高支持 version]
```

若存在不兼容 Mod，给出**替代方案**。

**Mod 间兼容性矩阵检查**（参考 `references/mod_compat.md`）：

```
known_conflicts = {
    ("optifine", "sodium"): "两者功能重叠，安装后会冲突",
    ("optifine", "sodium"): "两者功能重叠，安装后会冲突",
    ("optifine", "iris"): "OptiFine 着色器与 Iris 不兼容，应使用 Iris + Sodium",
    ("forge", "fabric"): "加载器不同，Mod 生态不互通，Fabric 和 Forge Mod 不可混用",
    ("applicants", "create"): "两者都修改物品处理逻辑，可能导致机械联动异常",
    ("mekanism", "ic2"): "两个能源 Mod 可能存在 EU/RF 单位冲突",
    ("ae2", "refinedstorage"): "两个存储系统不可同时启用",
    ("jade", "wthit"): "同类信息展示 Mod，仅需一个",
    ("roughly enough items", "emi"): "REI 与 EMI 功能重叠，只能选择一个",
}

check_compatibility(all_mods):
    for (mod_a, mod_b), reason in known_conflicts:
        if mod_a in selected and mod_b in selected:
            report conflict with reason
```

**依赖完整性检查**：

```
for mod in all_recommended_mods:
    for dep in mod.dependencies:
        if dep.required and dep.slug not in all_selected_slugs:
            auto_add_dependency(dep)
            report [⬆️ 自动补充前置: dep.name]
```

#### Step D — 整合包规划输出

最终输出包含以下部分：

**1. 整合包概览**

```
┌─────────────────────────────────────────────────┐
│  🎮 整合包规划报告                               │
│  版本: 1.20.4  |  加载器: Forge  |  规模: 中型   │
│  功能方向: 自动化农场 / 能源管理 / 物流传输       │
└─────────────────────────────────────────────────┘
```

**2. 分模块推荐卡片**

按功能方向分组展示，每个方向的 Mod 卡片后接兼容性说明。

**3. 兼容性总览表**

| Mod A | Mod B | 兼容状态 | 说明 |
|-------|-------|---------|------|
| Sodium | Lithium | ✅ 兼容 | 无冲突，均为优化 Mod |
| Create | Mekanism | ✅ 兼容 | 可联动，推荐使用 Create 管道连接 |
| AE2 | Refined Storage | ❌ 冲突 | 两者均为存储系统，不可同时安装 |
| OptiFine | Sodium | ⚠️ 替代关系 | 功能重叠，应选择 Sodium（Fabric 生态）或 OptiFine（Forge 生态）|

**4. 安装顺序建议**

按依赖层级给出推荐安装顺序：

```
安装顺序（按此顺序安装，避免启动崩溃）：

[1] 前置依赖层
    ├── Fabric API / Architectury API
    └── Cloth Config API

[2] 核心优化层
    ├── Sodium（帧率优化）
    ├── Lithium（物理/AI 优化）
    └── Phosphor（光照优化）

[3] 功能层
    ├── Storage Drawers（存储）
    ├── Create（机械自动化）
    └── Mekanism（能源管理）

[4] UI/辅助层
    ├── Jade（信息展示）
    └── REI（物品查看）
```

**5. 警告与注意事项**

- `[❌ 冲突]` 开头的行列出所有不可兼容的 Mod 组合
- `[⚠️ 注意]` 开头列出可能的兼容性问题
- `[💡 建议]` 开头给出优化建议（如轻量化方案）

## 9. 脚本工具

核心搜索脚本位于 `scripts/search_mods.py`。

### 9.1 单 Mod 搜索

```bash
# 普通 Mod 搜索
python scripts/search_mods.py --query "帧率优化" --version "1.20.4" --loader "fabric"
python scripts/search_mods.py --query "optifine" --version "1.20.1"
python scripts/search_mods.py --query "自动化" --version "1.19.2" --loader "forge"

# TACZ 枪包搜索（自动检测枪械意图）
python scripts/search_mods.py --query "步枪" --version "1.20.1" --loader "forge"
python scripts/search_mods.py --query "rifle" --version "1.20.1" --limit 5
python scripts/search_mods.py --query "狙击枪" --version "1.20.1" --output json

# Create 附属 mod 搜索（自动检测机械/自动化意图）
python scripts/search_mods.py --query "传送带" --version "1.20.1"
python scripts/search_mods.py --query "automation factory" --version "1.20.1" --limit 8
python scripts/search_mods.py --query "齿轮轴承" --version "1.20.1" --output json
```

### 9.2 参数说明

- `--query`: 搜索关键词（支持多词，用空格分隔）
- `--version`: Minecraft 版本（如 1.20.4）
- `--loader`: 加载器类型（forge / fabric / quilt）
- `--platform`: 搜索平台（modrinth / curseforge / all），默认 all
- `--limit`: 返回结果数量，默认 15
- `--timeout`: 请求超时秒数，默认 8

### 9.3 输出格式

支持 `--output text`（人类可读）和 `--output json`（JSON 格式）。

**text 格式示例（含快查表命中）**：

```
【快查表命中 — 高可信度推荐】
★ 1. Human Companions  [📚 快查表]
    添加中立幸存者 NPC，可自然生成于世界中
    Modrinth: https://modrinth.com/mod/human-companions

【API 搜索结果】
▶ 1. Easy NPC  [🔥 TOP推荐]
    ...
```

## 10. 版本兼容性参考

Minecraft Java Edition 主要版本及兼容性说明参考：
`references/mc_versions.md`

## 11. Mod 兼容性矩阵参考

Mod 之间已知冲突与兼容关系参考：
`references/mod_compat.md`

## 12. 注意事项

- **避免虚假信息**：仅返回实际 API / 网页查询到的结果，不编造 Mod 数据
- **版本敏感性**：明确告知用户当前 Mod 兼容的版本范围，避免误导
- **依赖提示（按需）**：默认不查询依赖（节省时间）；若用户明确要求查看依赖，运行时加 `--deps` 参数
- **失效检测**：若 Mod 超过 12 个月未更新，标注 `[⚠️ 久未更新]`
- **中文友好**：返回给用户的内容使用中文描述
- **CurseForge 无 Key 时提示**：若 CurseForge API Key 未配置，**必须在回答中明确告知**用户配置方法（不可静默跳过）
- **整合包模式**：始终先确认 MC 版本和加载器，再进行多方向搜索和兼容性检查
- **诚实报告不兼容**：若用户选择的 Mod 之间确实存在冲突，必须如实报告，不可忽略或回避
- **枪械类 Mod → TACZ 优先**：当检测到枪械/武器需求时，优先搜索 TACZ 枪包生态，告知用户需先安装 TACZ 基础 Mod；仅当 TACZ 枪包无结果时才回退到普通 Mod 搜索
- **TACZ 版本限制**：TACZ 官方版仅支持 Forge 1.18.2–1.20.1；若用户使用 Fabric 或更高 MC 版本，需提示关注社区移植版
- **机械/自动化类 Mod → Create 优先**：当检测到机械、自动化、科技需求时，优先搜索 Create 附属 mod 生态，告知用户需先安装 Create 基础 Mod；仅当 Create 附属无结果时才回退到普通 Mod 搜索
- **Create 与 OptiFine 互斥**：Create 依赖 Flywheel 渲染引擎，与 OptiFine 不兼容；Forge 环境需使用 Oculus，Fabric 环境使用 Iris
