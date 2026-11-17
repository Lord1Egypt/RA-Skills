# 开发者 SOP · 聚星逸配置

> 面向接手开发的工程师。涵盖架构内幕、运维流程、注意事项、踩坑经验。

---

## 一、项目概览

| 项 | 值 |
|----|-----|
| Slug | `huo15-juxingyi-configure` |
| 版本 | 1.2.0 |
| 仓库 | https://cnb.cool/huo15/ai/huo15-skills(主)/ https://github.com/zhaobod1/huo15-skills(镜像) |
| 目录 | `huo15-skills/huo15-juxingyi-configure/` |
| 技术栈 | Node.js 18+ ES Modules(零依赖) |
| 发布平台 | ClawHub |
| 接入文档 | https://fireworks-simulator.huo15.com/docs.html |

---

## 二、架构设计

### 2.1 核心设计决策

| 决策 | 原因 |
|------|------|
| **接口实时获取模型列表** | 聚星逸平台模型变化频繁,硬编码会过期。每次运行调 `/v1/models` 确保最新 |
| **不维护本地模型清单** | v1.2.0 起删除 `data/model-heuristics.json`,模型列表完全信任接口返回 |
| **模型参数填保守默认** | 接口只返回 `id`/`owned_by`,不返回上下文窗口等;填默认值保证 OpenClaw 可用 |
| **主模型取列表第一个** | 不硬编码特定模型;配完后主动询问切换 |
| **生图/视频过滤用脚本内正则** | 通用关键词(`image`/`t2v`/`i2v`/`video` 等),保证配置可用 |
| **零依赖 Node 脚本** | 不需要 npm install,Node 18+ 自带 fetch,用户直接运行 |
| **只操作 fireworks-hub provider** | 不碰其他 provider,保证幂等安全 |
| **写入前自动备份** | 可回滚,用户放心 |
| **SKILL.md 嵌入完整流程** | LLM 加载 SKILL.md 后 0 次 API 探索即可配置,省 token |

### 2.2 文件职责

```
huo15-juxingyi-configure/
├── SKILL.md                       # LLM 嵌入源(≤25KB),指导 AI 执行配置流程
├── _meta.json                     # ClawHub 元数据(ownerId/slug/version)
├── README.md                      # 公开文档(面向用户)
├── CLAUDE.md                      # 开发规范(面向接手开发者)
├── LICENSE                        # MIT
├── scripts/
│   └── configure.mjs              # 核心脚本(445行),所有逻辑在此
└── docs/
    ├── prd.md                     # 产品需求文档
    ├── user-guide.md              # 用户手册 SOP
    ├── dev-guide.md               # 开发者 SOP(本文档)
    └── changelog.md               # 版本变更历史
```

> v1.2.0 起**不再有** `data/` 目录——模型分类启发式数据已删除,模型列表完全来自接口。

### 2.3 configure.mjs 架构

```
参数解析 → Node 版本检查
    │
    ├── --help/-h      → cmdHelp()       显示帮助
    ├── --version/-v   → cmdVersion()    读 _meta.json,显示版本
    ├── --show         → cmdShow()       读 openclaw.json,展示当前配置
    ├── --switch X     → cmdSwitch()     读/写 openclaw.json,切换主模型(支持前缀匹配)
    ├── <key> --list   → fetchModels() + cmdList()       调接口,展示
    └── <key>          → fetchModels() + cmdConfigure()  调接口,写入 openclaw.json
```

**关键函数**:
- `fetchModels(apiKey)` — 调 `GET /v1/models`,带 15s 超时 + 错误分类(401/403/5xx)+ 空列表防护
- `toModelEntry(id)` — 单个模型配置项:`id` + `name` + 保守默认参数
- `buildConfig(apiKey, rawModels)` — 生成 provider + agents.defaults(primary 取第一个 + fallbacks + aliases)
- `resolveModelId(input, ids)` — 模型 ID 解析(精确→大小写不敏感→前缀唯一)
- `writeOpenclawJson(config)` — 备份 + 写入

**关键常量**:
- `BASE_URL` = `https://fireworks-simulator-api.huo15.com/v1`
- `PROVIDER` = `fireworks-hub`
- `ENV_VAR` = `FIREWORKS_API_KEY`
- `NON_TEXT_RE` = `/image|seedream|t2v|i2v|video|dall-?e|happyhorse/i`(生图/视频过滤)

---

## 三、开发环境

### 3.1 准备

```bash
# 仓库
cd ~/workspace/projects/openclaw/huo15-skills
cd huo15-juxingyi-configure

# Node 版本(需 18+)
node -v

# 无需 npm install(零依赖)
```

### 3.2 测试

```bash
# 语法检查
node --check scripts/configure.mjs

# 帮助 / 版本(不联网)
node scripts/configure.mjs --help
node scripts/configure.mjs --version

# 查看当前配置(不需 key)
node scripts/configure.mjs --show

# 列出模型(用真实 key 测试接口连通)
node scripts/configure.mjs fsk-测试key --list
```

### 3.3 修改模型默认参数

接口 `/v1/models` 只返回 `id`/`owned_by`,不返回上下文窗口等参数。如需调整保守默认值,编辑 `toModelEntry(id)` 函数:

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

> 如平台后续在 `/v1/models` 返回了精确参数,可改为读取接口字段(如 `m.context_window`)。

---

## 四、发布流程

### 4.1 标准发布(6 步)

```bash
# 1. 开发 & 测试
cd ~/workspace/projects/openclaw/huo15-skills/huo15-juxingyi-configure
node --check scripts/configure.mjs
node scripts/configure.mjs fsk-测试key --list

# 2. 自查
grep -riE "odoo|uniapp|uni-app|欧度" README.md SKILL.md CLAUDE.md docs/
wc -c SKILL.md  # 应 < 25600

# 3. 提交
cd ~/workspace/projects/openclaw/huo15-skills
git add huo15-juxingyi-configure/
git commit -m "feat(huo15-juxingyi-configure): vX.Y.Z 说明"

# 4. 推送双 remote
git push cnb main     # CNB(主)
git push origin main  # GitHub(镜像)

# 5. 发布 ClawHub
clawhub publish "$(pwd)/huo15-juxingyi-configure" \
  --slug huo15-juxingyi-configure \
  --version X.Y.Z \
  --changelog "说明"

# 6. chore commit(_meta.json 已是正确版本则跳过)
git commit --allow-empty -m "chore(huo15-juxingyi-configure): bump _meta to vX.Y.Z"
git push cnb main
```

### 4.2 版本号规则

| 变更类型 | 版本号 |
|---------|--------|
| 架构/哲学/触发器重构 | 次版本 +1(1.1 → 1.2) |
| 常规功能新增、新触发词 | 次版本 +1 |
| Bug 修复、文案调整、文档更新 | 补丁号 +1(1.0.0 → 1.0.1) |

### 4.3 ClawHub 发布六坑

| # | 坑 | 应对 |
|---|---|------|
| 1 | 必须绝对路径 | `clawhub publish "$(pwd)/huo15-juxingyi-configure"` |
| 2 | `--version` 必填 | CLI 不读 frontmatter / _meta.json |
| 3 | 新 slug 每小时 5 个配额 | 存量 slug 升版本不占额度 |
| 4 | `_meta.json` 不自动刷新 | 手动 bump + chore commit |
| 5 | 幽灵占用(inspect=2.5 但报 exists on 2.6) | 立刻跳 +1 patch,不重试 |
| 6 | Remote push 可能失败 | CNB 是主库,GitHub 镜像失败不阻塞 |

---

## 五、运维注意事项

### 5.1 密钥安全

- ❌ **密钥禁止出现在**:commit / log / PR / SKILL.md / README.md / 任何 LLM 上下文
- ✅ **用户每次运行时提供密钥**,skill 代码中不存储
- ✅ **推荐用 `--env` 模式**,配置文件中不存明文

### 5.2 openclaw.json 操作安全

- ✅ 每次写入前自动备份 `.bak.<timestamp>`
- ✅ 只操作 `fireworks-hub` provider 段
- ✅ 合并 `agents.defaults.models` 时保留非 `fireworks-hub/` 的已有条目
- ⚠️ 如果用户手动改了 openclaw.json 中 fireworks-hub 段,重新运行脚本会覆盖(但有备份)

### 5.3 模型列表维护

- **完全不需要手动维护**——脚本每次运行都从 `/v1/models` 接口实时获取
- 平台新增模型后,重新运行脚本即可自动包含
- 只有以下情况需要改脚本:
  1. 接口 Base URL 变了 → 改 `BASE_URL` 常量
  2. 新的生图/视频模型命名模式 → 改 `NON_TEXT_RE` 正则
  3. 想调整模型默认参数 → 改 `toModelEntry`

---

## 六、踩坑经验

### 坑 1:接口 /v1/models 不返回模型参数

**现象**:OpenAI 兼容的 `/v1/models` 端点标准只返回 `{id, object, created, owned_by}`,不返回 `contextWindow`/`reasoning`/`maxTokens`。

**解决(v1.2.0)**:`toModelEntry` 填保守默认值保证 OpenClaw 可用。如平台后续扩展返回字段,可改为读取。

### 坑 2:主模型不稳定(取列表第一个)

**现象**:接口返回顺序不保证稳定,主模型可能变化。

**解决**:配完后主动询问用户是否切换(SKILL.md §三 Step 3 强制要求),用户可立即选定稳定主模型。`--switch` 支持前缀匹配。

### 坑 3:`deepMerge` 函数未使用(已清理,v1.1.1)

开发初期设计了深度合并,后来改为直接覆盖 `fireworks-hub` 段。**v1.1.1 已删除该死代码**。

### 坑 4:MiniMax 误判(已随 v1.2.0 架构简化彻底消除)

v1.0/v1.1 时代 `tierPatterns` 中 `Mini` 关键词太宽泛,`MiniMax-M2.7` 被误判为 flash。v1.2.0 删除了整个 tier 分类体系,此问题不再存在。

### 坑 5:GitHub 推送失败

**现象**:`git push origin main` 报 `could not read Username` 或 HTTP2 framing error。

**解决**:CNB 是主库,GitHub 是镜像。CNB 推成功即可,GitHub 失败不阻塞发布。

### 坑 6:SKILL.md 中不能出现品牌违禁词

`grep -riE "odoo|uniapp|uni-app|欧度"` 不能命中(已发布 slug `huo15-odoo19-module-dev` 本身是例外,但描述文字不能含违禁词)。

---

## 七、与其他 skill 的关系

| Skill | 关系 |
|-------|------|
| `huo15-yh-usage` | **互补**:本 skill 配置聚星逸接入,yh-usage 查该 key 的用量账单 |
| `huo15-openclaw-bootstrap` | **上游**:bootstrap 初始化 workspace 后,用户可能需要配置模型供应商(本 skill) |
| `huo15-token-optimizer` | **参考**:token-optimizer 的 references 中有 openclaw.json 配置格式参考 |

---

## 八、调试技巧

### 8.1 查看当前 openclaw.json 中的聚星逸段

```bash
cat ~/.openclaw/openclaw.json | python3 -c "
import sys, json
d = json.load(sys.stdin)
print(json.dumps(d.get('models',{}).get('providers',{}).get('fireworks-hub',{}), indent=2, ensure_ascii=False))
"
```

### 8.2 测试 API 连通性

```bash
curl -s "https://fireworks-simulator-api.huo15.com/v1/models" \
  -H "Authorization: Bearer fsk-测试key" | python3 -m json.tool | head -20
```

### 8.3 查看备份文件

```bash
ls -lt ~/.openclaw/openclaw.json.bak.* | head -5
```

---

## 九、发布前自查 Checklist

```bash
# 1. 品牌词检查(必须无命中)
grep -riE "odoo|uniapp|uni-app|欧度" README.md SKILL.md CLAUDE.md docs/

# 2. SKILL.md 大小(应 < 25600 字节)
wc -c SKILL.md

# 3. 脚本语法检查
node --check scripts/configure.mjs

# 4. _meta.json 格式检查
python3 -c "import json; json.load(open('_meta.json'))"

# 5. 脚本功能测试
node scripts/configure.mjs --show
node scripts/configure.mjs --help
node scripts/configure.mjs --version

# 6. git 状态
git status
```

---

## 十、后续规划

| 版本 | 计划 |
|------|------|
| v1.3 | 如平台 `/v1/models` 返回精确参数(contextWindow/reasoning 等),改为读取接口字段 |
| v1.4 | 支持配置指定 agent 的模型(非 defaults) |
| v1.5 | 模型健康检查(测试每个模型是否可调用) |

---

**青岛火一五信息科技有限公司** · postmaster@huo15.com · QQ群 1093992108
