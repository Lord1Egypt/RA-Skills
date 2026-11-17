# PRD · 聚星逸配置 Skill(huo15-juxingyi-configure)

> 产品需求文档 · v1.2.0 · 2026-07-19

---

## 一、产品定位

**聚星逸配置**是 OpenClaw 生态专用 skill,帮助用户将聚星逸(Juxingyi)大模型聚合平台接入 OpenClaw 运行时。

**核心价值**:用户只需提供一个 `fsk-` 密钥,skill 调聚星逸 `/v1/models` 接口拉取最新模型列表,自动写入 `~/.openclaw/openclaw.json`,无需手动查文档、记模型 ID、写 JSON。**模型列表完全来自接口,不维护任何本地硬编码清单。**

---

## 二、背景与问题

### 痛点

1. **模型列表变化频繁**:聚星逸平台不断新增模型,硬编码列表很快过期
2. **手动配置易出错**:openclaw.json 结构复杂(providers / models / agents.defaults / fallbacks / aliases),手写容易漏字段或拼错模型 ID
3. **每次探索浪费 token**:不沉淀配置知识,每次都要消耗 LLM token 去搜索文档、探索配置格式
4. **不知道有哪些模型可用**:用户不清楚平台有哪些模型,也不知道哪些适合文本对话、哪些是生图/视频

### 解决方案

| 痛点 | 解决方式 |
|------|---------|
| 模型列表过期 | 每次运行脚本调 `GET /v1/models`,完全信任接口返回 |
| 手动配置易错 | 脚本自动生成完整 JSON 片段并写入 |
| token 浪费 | SKILL.md 嵌入完整配置知识,0 次 API 探索 |
| 不知有哪些模型 | `--list` 模式列出接口返回的全部模型 |

---

## 三、用户故事

### US-1:首次配置

> 作为 OpenClaw 用户,我想用聚星逸的密钥接入平台,这样就能调用 50+ 大模型。

**验收**:
- ✅ 用户提供 `fsk-` 密钥后,脚本调 `/v1/models` 接口拉取模型列表
- ✅ 自动写入 `~/.openclaw/openclaw.json` 的 `models.providers.fireworks-hub` 段
- ✅ 主模型取接口返回列表的第一个
- ✅ 写入前自动备份原配置
- ✅ 配置完成后主动询问用户是否切换模型

### US-2:切换主模型

> 作为已配置用户,我想切换默认主模型。

**验收**:
- ✅ `--switch <model-id>` 一键切换(支持前缀匹配)
- ✅ 旧主模型自动加入 fallbacks 链
- ✅ 切换前自动备份

### US-3:查看可用模型

> 作为潜在用户,我想看看聚星逸有哪些模型可用,再决定是否配置。

**验收**:
- ✅ `--list` 模式调接口并展示,标注默认主模型(列表第一个)
- ✅ 生图/视频模型单独列出(标注"跳过")

### US-4:查看当前配置

> 作为已配置用户,我想看看当前聚星逸配了什么。

**验收**:
- ✅ `--show` 模式展示 provider 信息、主模型、备选链、全部已配模型
- ✅ 密钥脱敏显示

### US-5:安全存储密钥

> 作为安全敏感用户,我不想把 API Key 明文写在配置文件里。

**验收**:
- ✅ `--env` 模式用环境变量引用(`FIREWORKS_API_KEY`)
- ✅ 配置文件中只存 `{ source: "env", provider: "default", id: "FIREWORKS_API_KEY" }`,不存明文

### US-6:日常更新模型列表(保留主模型)

> 作为已配置用户,平台新增了模型,我想拉取最新列表但保留自己选的主模型。

**验收**:
- ✅ `--update` 子命令调接口拿最新列表
- ✅ **保留当前主模型**(若仍在平台列表中)
- ✅ 报告新增 / 移除的模型
- ✅ 旧主模型下架时自动切到列表第一个并提示
- ✅ 保留原密钥存储方式(明文 / env 不动)
- ✅ 更新前自动备份

---

## 四、功能需求

### F1:接口模型获取

- **输入**:`fsk-` 密钥
- **API**:`GET https://fireworks-simulator-api.huo15.com/v1/models`
- **鉴权**:`Authorization: Bearer <fsk-key>`
- **输出**:模型列表 JSON(OpenAI 兼容标准 `{ object: "list", data: [{ id, owned_by, ... }] }`)
- **容错**:15s 超时、401/403/5xx 错误分类、空列表防护

### F2:模型处理

| 类别 | 判定规则 | 处理方式 |
|------|---------|---------|
| 生图/视频模型 | ID 匹配 `NON_TEXT_RE`(`image`/`seedream`/`t2v`/`i2v`/`video`/`dall-e`/`happyhorse`) | 跳过,不配置文本对话 |
| 文本对话模型 | 其余全部 | 写入配置 |

> **不维护本地模型清单**:v1.2.0 起删除了 `data/model-heuristics.json`,模型列表完全来自接口。

### F3:模型参数

接口 `/v1/models` 只返回 `id`/`owned_by`,不返回上下文窗口等参数。脚本填保守默认值:

| 字段 | 默认值 |
|------|--------|
| `reasoning` | `false` |
| `contextWindow` | `131072` |
| `maxTokens` | `8192` |
| `input` | `["text"]` |
| `cost` | 全 0 |

> 用户可按需在 `openclaw.json` 手动调整。如平台后续扩展接口返回字段,可改为读取。

### F4:openclaw.json 写入

写入以下段:

```
models.providers.fireworks-hub     ← provider 配置 + 全部文本模型
agents.defaults.model.primary      ← 列表第一个模型
agents.defaults.model.fallbacks    ← 其余文本模型列表
agents.defaults.models             ← 每个模型的 alias
```

**安全规则**:
- 只操作 `fireworks-hub` provider,不碰其他 provider
- 合并 `agents.defaults.models` 时,保留非 `fireworks-hub/` 前条的已有条目
- 写入前自动备份 `openclaw.json.bak.<timestamp>`

### F5:子命令

| 命令 | 功能 |
|------|------|
| `<fsk-key>` | 首次配置:拉取模型列表并写入(主模型取列表第一个) |
| `<fsk-key> --list` | 列出接口返回的模型(不写文件) |
| `<fsk-key> --update` | **日常更新**:保留当前主模型,只刷新模型列表 |
| `<fsk-key> --env` | 首次配置时用环境变量引用存储密钥 |
| `--switch <model-id>` | 切换主模型 |
| `--show` | 查看当前配置 |
| `--help` / `--version` | 帮助 / 版本 |

---

## 五、非功能需求

| 项 | 要求 |
|----|------|
| 运行时 | Node.js 18+(自带 fetch),零依赖 |
| 安全 | 密钥不硬编码,不出现在 commit/log/PR |
| 可逆 | 每次写入前备份 |
| 品牌合规 | 对外文档无 `odoo` / `uniapp` / `uni-app` / `欧度` |
| 体积 | SKILL.md ≤ 25KB(8192 tokens 限制) |
| 可维护 | 平台新增模型后无需更新 skill(接口实时获取) |

---

## 六、技术约束

- **API 协议**:OpenAI 兼容(`openai-completions`)
- **Provider 名称**:`fireworks-hub`(openclaw.json 中的 key)
- **密钥格式**:`fsk-` 开头
- **Base URL**:`https://fireworks-simulator-api.huo15.com/v1`
- **接入文档**:https://fireworks-simulator.huo15.com/docs.html

---

## 七、不做什么

- ❌ 不查用量账单(走 `huo15-yh-usage` skill)
- ❌ 不配置生图/视频模型为文本对话(跳过)
- ❌ 不修改 openclaw.json 中其他 provider 配置
- ❌ 不自动重启 OpenClaw(只提示用户手动重启)
- ❌ 不缓存模型列表(每次都调接口,确保最新)
- ❌ 不维护本地模型分类数据(v1.2.0 起完全依赖接口)

---

## 八、里程碑

| 版本 | 日期 | 内容 |
|------|------|------|
| v1.0.0 | 2026-07-11 | 首版:动态获取、启发式分类、配置写入、切换、show、list、json、env |
| v1.1.1 | 2026-07-19 | 健壮性增强:Node 检查、密钥校验、超时错误分类、help/version/selftest、前缀匹配 |
| v1.3.0 | 2026-07-19 | 新增 `--update` 子命令(日常更新模型列表,保留主模型) |
| v1.2.0 | 2026-07-19 | 架构简化:删除本地硬编码分类数据,模型列表完全来自接口;主模型取列表第一个;删 --json/--selftest |

---

## 九、后续规划

- v1.3:如平台 `/v1/models` 返回精确参数,改为读取接口字段
- v1.4:支持配置指定 agent 的模型(非 defaults)
- v1.5:模型健康检查(测试每个模型是否可调用)
