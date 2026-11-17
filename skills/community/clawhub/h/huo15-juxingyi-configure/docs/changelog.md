# 变更历史 · huo15-juxingyi-configure

---

## v1.3.0(2026-07-19)

**新增 `--update` 子命令:日常更新模型列表,保留主模型。**

### 新增

- **`--update` 子命令**:已配置用户日常刷新模型列表(平台新增模型后),与首次配置区分
- **`cmdUpdate` 函数**:保留当前主模型(若仍在平台列表中),只刷新 providers 段模型列表
- **变更报告**:对比旧/新列表,报告新增 / 移除的模型
- **旧主模型下架处理**:若旧主模型不在新列表(被下架),自动切到列表第一个并提示
- **保留密钥存储方式**:更新模型列表不改密钥配置(明文 / env 引用都保留原状)

### 与首次配置的区别

| 场景 | 命令 | 主模型处理 |
|------|------|-----------|
| 首次配置 | `<fsk-key>` | 取接口返回列表第一个,重置 fallbacks |
| 日常更新 | `<fsk-key> --update` | 保留当前主模型(若仍在列表),只刷新模型列表 |

### 文档

- SKILL.md:新增第四节"日常更新模型列表";命令速查表加 `--update`;章节顺延;版本历史加 v1.3.0
- README.md:命令表加 `--update`;特性列表加日常更新
- CLAUDE.md:架构图加 `--update` 分支;关键函数表加 `cmdUpdate`;脚本行数 445→540
- docs/dev-guide.md、docs/prd.md、docs/user-guide.md 同步

---

## v1.2.0(2026-07-19)

**架构简化:模型列表完全来自接口,删除本地硬编码分类数据。**

### 变更

- **删除 `data/model-heuristics.json`**:移除 30 个已知模型元数据(knownModels)、tier 模式匹配规则(tierPatterns)、skipPatterns 等全部本地硬编码分类数据
- **删除 `data/` 目录**:不再需要
- **模型列表完全来自接口**:脚本只调 `GET /v1/models`,信任接口返回,不维护本地清单
- **主模型改为取接口返回列表的第一个**:不再硬编码 `DeepSeek-V4-Flash`
- **生图/视频过滤改为脚本内通用正则**:`NON_TEXT_RE = /image|seedream|t2v|i2v|video|dall-e|happyhorse/i`(常量,非外部数据文件)
- **模型参数填保守默认值**:接口 `/v1/models` 只返回 `id`/`owned_by`,不返回上下文窗口等;`toModelEntry` 填 `contextWindow`: 131072 / `maxTokens`: 8192 / `reasoning`: false 保证 OpenClaw 可用,可手动调整

### 删除

- **`--json` 子命令**:偏离核心(输出 JSON 片段),移除
- **`--selftest` 子命令**:依赖已删除的分类逻辑(classifyModel/guessTier),移除
- **`classifyModel` / `guessTier` / `tierWeight` 函数**:分类体系整体移除
- **`cmdJson` / `cmdSelftest` 函数**:对应子命令已删

### 文档

- SKILL.md:第五节"模型分类规则"改为"模型列表来源";命令速查去掉 `--json`/`--selftest`;配置结构说明参数为保守默认;文件清单去掉 `data/`
- README.md:"模型分类规则"章节改为"模型列表来源";文件结构去掉 `data/`;命令表同步
- CLAUDE.md:核心设计决策、架构图、关键函数表、修改指引、踩坑全部重写以反映接口直取设计
- docs/dev-guide.md、docs/prd.md、docs/user-guide.md 同步

### 背景

用户要求技能"只通过聚星逸的接口文档和 Key 更新大模型列表配置到配置文件上"。据此去掉所有本地启发式分类数据,模型列表完全依赖接口实时返回。

---

## v1.1.1(2026-07-19)

**健壮性增强与代码质量提升。**(远程 1.1.0 已被 7-11 旧内容占用,跳 +1 patch 发布)

### 新增

- **`--help` / `-h` 子命令**:显示完整用法说明
- **`--version` / `-v` 子命令**:从 `_meta.json` 读取并显示版本号
- **`--selftest` 子命令**:不联网、不读写配置的内置自检(19 项断言)
- **`--switch` 前缀匹配**:`resolveModelId` 按 精确 → 大小写不敏感 → 前缀唯一 三级解析
- **Node 版本检查**:Node < 18 时给出友好提示
- **API Key 格式校验**:`fsk-` 后必须有内容
- **`fetchModels` 增强**:15s 超时 + 错误分类(401/403/5xx/超时)+ 空模型列表防护

### 变更

- **根治 MiniMax 误判**:`tierPatterns.flash` 里 `Mini` 改为 `\bMini\b`(词边界匹配)
- **删除死代码**:移除从未调用的 `deepMerge` 函数

### 文档

- 同步 `CLAUDE.md` / `docs/dev-guide.md` 的脚本行数(385 → 561)、架构图、关键函数表、踩坑记录

> 注:v1.2.0 删除了整个 tier 分类体系,上述 MiniMax 相关修复已成为历史。

---

## v1.0.0(2026-07-11)

**首版发布。**

### 新增

- **动态模型获取**:每次运行脚本调 `GET /v1/models`,确保模型列表最新
- **启发式分类**:`data/model-heuristics.json` 提供已知模型元数据 + 未知模型模式匹配
- **自动配置**:写入 `~/.openclaw/openclaw.json` 的 `models.providers.fireworks-hub` 段
- **默认主模型**:`DeepSeek-V4-Flash`(快速、支持推理)
- **备选链**:其余文本模型自动加入 fallbacks
- **模型别名**:每个模型自动生成 alias
- **子命令**:`<fsk-key>` / `--list` / `--json` / `--env` / `--switch` / `--show`
- **安全**:写入前自动备份 `openclaw.json.bak.<timestamp>`
- **分类**:自动跳过生图/视频模型,按 tier(flash/pro/reasoner)排序
- **SKILL.md**:嵌入完整配置流程
- **文档**:PRD、用户手册 SOP、开发者 SOP

> 注:v1.2.0 删除了启发式分类体系,模型列表改为完全来自接口。
