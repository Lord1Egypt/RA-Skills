# CLAUDE.md · huo15-juxingyi-configure

> 聚星逸配置 skill —— 用 fsk- 密钥调 /v1/models 接口,把模型列表写入 openclaw.json
> 面向接手开发的 AI / 工程师,涵盖架构、规范、踩坑、运维。

---

## 一、项目定位

将聚星逸(Juxingyi)大模型聚合平台接入 OpenClaw。用户提供一个 `fsk-` 密钥,skill 调 `/v1/models` 接口拉取最新模型列表,自动写入 `~/.openclaw/openclaw.json`,主模型取接口返回列表的第一个,配好后询问用户是否切换。

**核心价值**:模型列表完全来自接口实时返回,不维护任何本地硬编码清单——平台新增模型无需更新本 skill。

---

## 二、技术栈

| 项 | 值 |
|----|----|
| 脚本语言 | Node.js ES Modules(零依赖,需 Node 18+) |
| API 协议 | OpenAI 兼容(`openai-completions`) |
| API 端点 | `GET https://fireworks-simulator-api.huo15.com/v1/models` |
| 接入文档 | https://fireworks-simulator.huo15.com/docs.html |
| 配置文件 | `~/.openclaw/openclaw.json` |

---

## 三、核心设计决策

| 决策 | 原因 |
|------|------|
| **接口实时获取**(非硬编码) | 平台模型变化频繁,硬编码会过期;每次运行调 `/v1/models` 确保最新 |
| **不维护本地模型清单** | v1.2.0 起删除 `data/model-heuristics.json`,模型列表完全信任接口 |
| **模型参数填保守默认** | 接口只返回 `id`/`owned_by`,不返回上下文窗口等;填默认值保证 OpenClaw 可用,用户可手动调 |
| **主模型取列表第一个** | 不硬编码特定模型;配完后主动询问切换 |
| **生图/视频过滤用脚本内正则** | 通用关键词(`image`/`t2v`/`i2v`/`video` 等),保证配置可用;非外部数据文件 |
| **零依赖 Node 脚本** | 不需 npm install,用户直接运行 |
| **只操作 fireworks-hub provider** | 不碰其他 provider,幂等安全 |
| **写入前自动备份** | 可回滚 |
| **SKILL.md 嵌入完整流程** | LLM 加载后 0 次 API 探索,省 token |

---

## 四、文件结构

```
huo15-juxingyi-configure/
├── SKILL.md                       # LLM 嵌入源(≤25KB)
├── _meta.json                     # ClawHub 元数据
├── README.md                      # 公开文档(面向用户)
├── CLAUDE.md                      # 开发规范(本文档)
├── LICENSE                        # MIT
├── .gitignore                     # skill 级忽略
├── scripts/
│   └── configure.mjs              # 核心脚本(540 行),所有逻辑在此
└── docs/
    ├── prd.md                     # 产品需求文档
    ├── user-guide.md              # 用户手册 SOP
    ├── dev-guide.md               # 开发者 SOP(更详细的架构内幕)
    └── changelog.md               # 版本变更历史
```

> v1.2.0 起**不再有** `data/` 目录——模型分类启发式数据已删除,模型列表完全来自接口。

---

## 五、configure.mjs 架构

```
参数解析 → Node 版本检查
    │
    ├── --help/-h      → cmdHelp()       显示帮助
    ├── --version/-v   → cmdVersion()    读 _meta.json,显示版本
    ├── --show         → cmdShow()       读 openclaw.json,展示当前配置
    ├── --switch X     → cmdSwitch()     读/写 openclaw.json,切换主模型(支持前缀匹配)
    ├── <key> --list   → fetchModels() + cmdList()       调接口,展示
    ├── <key> --update → fetchModels() + cmdUpdate()     调接口,保留主模型刷新模型列表
    └── <key>          → fetchModels() + cmdConfigure()  调接口,写入 openclaw.json(首次配置)
```

### 关键函数

| 函数 | 职责 |
|------|------|
| `fetchModels(apiKey)` | 调 `GET /v1/models`,带 15s 超时 + 错误分类(401/403/5xx)+ 空列表防护 |
| `toModelEntry(id)` | 单个模型配置项:`id` + `name` + 保守默认参数 |
| `buildConfig(apiKey, rawModels)` | 生成 provider + agents.defaults(primary 取第一个 + fallbacks + aliases) |
| `cmdUpdate(newProvider, textModels, skipped)` | **日常更新**:保留当前主模型,只刷新模型列表,报告新增/移除 |
| `resolveModelId(input, ids)` | 模型 ID 解析:精确 → 大小写不敏感 → 前缀唯一 |
| `readOpenclawJson()` | 读取 `~/.openclaw/openclaw.json` |
| `writeOpenclawJson(config)` | 备份 + 写入 |

### 模型处理逻辑

1. `fetchModels` 调接口拿 `data.data`(OpenAI 兼容标准格式)
2. `buildConfig` 遍历模型,用 `NON_TEXT_RE` 正则跳过生图/视频模型
3. 每个文本模型经 `toModelEntry` 生成配置项(保守默认参数)
4. 主模型 = 列表第一个,其余作 fallbacks

> **`NON_TEXT_RE = /image|seedream|t2v|i2v|video|dall-?e|happyhorse/i`** —— 脚本内常量,非外部数据文件。

---

## 六、修改指引

### 修改接口常量

编辑 `scripts/configure.mjs` 顶部的常量段:

```js
const BASE_URL = 'https://fireworks-simulator-api.huo15.com/v1'
const PROVIDER = 'fireworks-hub'
const ENV_VAR = 'FIREWORKS_API_KEY'
const NON_TEXT_RE = /image|seedream|t2v|i2v|video|dall-?e|happyhorse/i
```

### 修改模型默认参数

编辑 `toModelEntry(id)` 函数中的默认值:

```js
function toModelEntry(id) {
  return {
    id,
    name: `${fmtName(id)} (聚星逸)`,
    reasoning: false,        // ← 推理能力默认
    contextWindow: 131072,   // ← 上下文窗口默认
    maxTokens: 8192,         // ← 最大输出 token 默认
    input: ['text'],
    cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
  }
}
```

> 这些是保守默认值(接口不返回精确参数)。如平台后续在 `/v1/models` 返回了精确参数,可改为读取接口字段。

---

## 七、铁律

1. ❌ **不在任何文件中硬编码 API Key** — 用户每次运行时提供
2. ❌ **不跳过接口获取** — 必须调 `/v1/models`,不用本地清单
3. ❌ **配置完不问就结束** — 必须主动问用户是否切换模型(见 SKILL.md §三 Step 3)
4. ❌ **不破坏其他 provider** — 只改 `fireworks-hub` 段
5. ❌ **不忘记备份** — 写入前必须备份 openclaw.json
6. ❌ **密钥禁止出现在 commit / log / PR / 任何 LLM 上下文**
7. ✅ **SKILL.md ≤ 25KB** — 检查:`wc -c SKILL.md`

---

## 八、踩坑经验

### 坑 1:接口 /v1/models 不返回模型参数

**现象**:OpenAI 兼容的 `/v1/models` 端点标准只返回 `{id, object, created, owned_by}`,不返回 `contextWindow`/`reasoning`/`maxTokens`。

**解决(v1.2.0)**:`toModelEntry` 填保守默认值(`contextWindow`: 131072, `maxTokens`: 8192, `reasoning`: false)保证 OpenClaw 可用。用户可按需手动调整。如平台后续扩展了返回字段,可改为读取。

### 坑 2:主模型不稳定(取列表第一个)

**现象**:接口返回顺序不保证稳定,主模型可能变化。

**解决**:配完后主动询问用户是否切换(SKILL.md §三 Step 3 强制要求),用户可立即选定稳定主模型。`--switch` 支持前缀匹配。

### 坑 3:`deepMerge` 函数定义了但未使用(已清理,v1.1.1)

开发初期设计了深度合并,后来改为直接覆盖 `fireworks-hub` 段(更安全可预测)。**v1.1.1 已删除该死代码**。

### 坑 4:MiniMax 误判(已随 v1.2.0 架构简化彻底消除)

v1.0/v1.1 时代 `tierPatterns` 中 `Mini` 关键词太宽泛,`MiniMax-M2.7` 被误判为 flash。v1.2.0 删除了整个 tier 分类体系,此问题不再存在。

### 坑 5:GitHub 推送可能失败

`git push origin main` 可能报 `could not read Username`。CNB 是主库,GitHub 是镜像,CNB 成功即可。

### 坑 6:品牌词检查

对外文档不能出现 `odoo` / `uniapp` / `uni-app` / `欧度`。已发布目录名 `huo15-odoo19-module-dev` 本身是例外(slug 不可改名),但描述文字不能含违禁词。

---

## 九、发布前自查

```bash
# 品牌词检查(必须无命中)
grep -riE "odoo|uniapp|uni-app|欧度" README.md SKILL.md CLAUDE.md docs/

# SKILL.md 大小(应 < 25600 字节)
wc -c SKILL.md

# 脚本语法检查
node --check scripts/configure.mjs

# _meta.json 格式检查
python3 -c "import json; json.load(open('_meta.json'))"

# 功能测试
node scripts/configure.mjs --show
node scripts/configure.mjs --help
node scripts/configure.mjs --version
```

---

## 十、发布流程

```bash
# 1. 提交
cd ~/workspace/projects/openclaw/huo15-skills
git add huo15-juxingyi-configure/
git commit -m "feat(huo15-juxingyi-configure): vX.Y.Z 说明"

# 2. 推送
git push cnb main     # CNB(主)
git push origin main  # GitHub(镜像,失败不阻塞)

# 3. 发布 ClawHub
clawhub publish "$(pwd)/huo15-juxingyi-configure" \
  --slug huo15-juxingyi-configure \
  --version X.Y.Z \
  --changelog "说明"

# 4. chore commit
git commit --allow-empty -m "chore(huo15-juxingyi-configure): bump _meta to vX.Y.Z"
git push cnb main
```

**版本号规则**:架构重构/新功能 → 次版本+1;Bug修复/文案 → 补丁+1。

---

## 十一、与其他 skill 协作

| Skill | 关系 |
|-------|------|
| `huo15-yh-usage` | 互补:本 skill 配置接入,yh-usage 查用量账单 |
| `huo15-openclaw-bootstrap` | 上游:bootstrap 初始化 workspace 后配置模型供应商 |

---

## 十二、联系方式

- **公司**: 青岛火一五信息科技有限公司
- **邮箱**: postmaster@huo15.com
- **QQ群**: 1093992108
