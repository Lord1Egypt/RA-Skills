---
name: huo15-juxingyi-configure
displayName: 聚星逸配置
version: 1.3.0
description: "用聚星逸 fsk- 密钥调 /v1/models 接口,把最新模型列表写入 openclaw.json。模型列表完全来自接口实时返回,不依赖本地硬编码数据。支持日常更新(--update 保留主模型)、切换、查看。一个 Key 调 50+ 顶级大模型。"
homepage: https://github.com/zhaobod1/huo15-skills
metadata: { "openclaw": { "emoji": "🛰️", "requires": { "bins": ["node"] } } }
aliases:
  - 聚星逸配置
  - 聚星逸
  - juxingyi
  - 配置聚星逸
  - 聚星逸接入
  - 聚星逸模型
  - fireworks-hub
  - 烟花智汇配置
  - fsk配置
---

# 聚星逸配置 · huo15-juxingyi-configure

> 用 fsk- 密钥调聚星逸 /v1/models 接口 → 把模型列表写入 ~/.openclaw/openclaw.json。
> 模型列表完全来自接口实时返回,不依赖本地硬编码数据。
> 青岛火一五信息科技有限公司 · OpenClaw 生态

---

## 一、什么时候用

✅ **触发**:
- 用户说"配置聚星逸"/"接入聚星逸"/"juxingyi"/"fireworks-hub"
- 用户提供了 `fsk-` 开头的聚星逸 API Key,想接入 OpenClaw
- 用户说"把聚星逸的模型配到 openclaw"
- 用户想查看或切换聚星逸已配的模型

❌ **不触发**:
- 用户只是问聚星逸是什么(直接回答即可)
- 用户想查用量账单(走 `huo15-yh-usage` skill)

---

## 二、前置知识

**聚星逸**(Juxingyi)是青岛火一五的大模型聚合平台(接入文档:https://fireworks-simulator.huo15.com/docs.html):
- **Base URL**: `https://fireworks-simulator-api.huo15.com/v1`
- **API 协议**: OpenAI 兼容(`openai-completions`)
- **密钥格式**: `fsk-` 开头
- **模型列表端点**: `GET /v1/models`(动态返回最新可用模型)
- **一个 Key** 可调 50+ 主流大模型(DeepSeek / GPT / Claude / Qwen / GLM / Gemini / Kimi / MiniMax / 豆包等)

在 OpenClaw 中,聚星逸作为一个 **provider**(`fireworks-hub`)配置在 `~/.openclaw/openclaw.json` 的 `models.providers` 段。

---

## 三、配置流程(3 步)

### Step 1 · 获取用户的 API Key

向用户索要聚星逸 API Key(`fsk-` 开头)。如果用户没有,引导去 [聚星逸控制台](https://fireworks-simulator.huo15.com/app/) →「API 密钥」页创建。

### Step 2 · 运行配置脚本

```bash
node <skill_dir>/scripts/configure.mjs <fsk-key>
```

脚本会:
1. **调用** `GET /v1/models` 接口拉取最新模型列表(完全来自接口,无本地硬编码清单)
2. 跳过生图/视频模型(ID 含 `image`/`t2v`/`i2v`/`video` 等关键词的不能用于文本对话)
3. 写入 `~/.openclaw/openclaw.json`:
   - `models.providers.fireworks-hub`(provider + 全部文本模型)
   - `agents.defaults.model.primary` = 接口返回列表的第一个模型
   - `agents.defaults.model.fallbacks` = 其余文本模型
   - `agents.defaults.models` = 每个模型的 alias
4. 自动备份原配置到 `openclaw.json.bak.<timestamp>`

脚本输出示例:
```
✅ 聚星逸配置完成!
   备份: ~/.openclaw/openclaw.json.bak.2026-07-19T...
   模型数: 18 个文本对话模型
   主模型: fireworks-hub/DeepSeek-V4-Flash
   备选链: 17 个模型
```

> **关于模型参数**:接口 `/v1/models` 只返回模型 `id`/`owned_by`,不返回上下文窗口等参数。脚本除 `id`/`name` 外填保守默认值(`contextWindow`: 131072, `maxTokens`: 8192, `reasoning`: false)保证 OpenClaw 可用,用户可按需在 `openclaw.json` 手动调整。

### Step 3 · 询问用户是否切换主模型

**配置完成后,必须主动问用户**:

```
🛰️ 聚星逸配置完成!主模型是 <接口返回的第一个模型>。

需要切换到其他模型吗?回复模型名即可切换,如 "DeepSeek-V4-Pro"。
或回复 "列出全部" 看完整列表。不切换就回 "不用了"。
```

**如果用户要切换**:
```bash
node <skill_dir>/scripts/configure.mjs --switch <model-id>
```

**如果用户想看完整列表**:
```bash
node <skill_dir>/scripts/configure.mjs <fsk-key> --list
```

**如果用户想看当前配置**:
```bash
node <skill_dir>/scripts/configure.mjs --show
```

---

## 四、日常更新模型列表(平台新增了模型)

**当用户说"更新一下聚星逸模型"/"拉取最新模型列表"/"平台加了新模型"时,用 `--update`**:

```bash
node <skill_dir>/scripts/configure.mjs <fsk-key> --update
```

与首次配置(`<fsk-key>`)的区别:
- **首次配置**(无 `--update`):主模型取接口返回列表的第一个,重置 fallbacks
- **日常更新**(`--update`):**保留用户当前选定的主模型**(若仍在平台列表中),只刷新 providers 段的模型列表

`--update` 做什么:
1. 调 `/v1/models` 接口拿最新模型列表
2. 对比旧列表,报告新增 / 移除的模型
3. **保留当前主模型**(若仍在列表中);若旧主模型已下架(不在新列表),自动切到列表第一个并提示
4. 重新生成 fallbacks(新列表中除主模型外的全部)
5. 保留原密钥存储方式(明文 / env 引用都不动)
6. 自动备份

输出示例:
```
✅ 聚星逸模型列表已更新!
   备份: ~/.openclaw/openclaw.json.bak.2026-07-19T...
   模型数: 18 → 20 个文本对话模型
   ✨ 新增 2 个:
     + NewModel-X1
     + NewModel-X2
   主模型保留: fireworks-hub/DeepSeek-V4-Flash
   备选链: 19 个模型

重启 OpenClaw 后生效。
```

> **何时用 `--update` vs 重新配置**:已配置过且想保留主模型选择 → 用 `--update`;想从头重新配置 → 不加 `--update`。

## 五、脚本命令速查

| 命令 | 用途 |
|------|------|
| `node configure.mjs <fsk-key>` | 首次配置:拉取模型列表并写入(主模型取列表第一个) |
| `node configure.mjs <fsk-key> --list` | 只列出接口返回的模型(不写文件) |
| `node configure.mjs <fsk-key> --update` | **日常更新模型列表(保留当前主模型)** |
| `node configure.mjs <fsk-key> --env` | 首次配置时用环境变量引用存储密钥(更安全) |
| `node configure.mjs --switch <model-id>` | 切换主模型(支持前缀匹配) |
| `node configure.mjs --show` | 查看当前聚星逸配置 |
| `node configure.mjs --help` / `-h` | 显示帮助 |
| `node configure.mjs --version` / `-v` | 显示版本号 |

> `<skill_dir>` = 本 skill 安装目录,通常为 `~/.openclaw/workspace/skills/huo15-juxingyi-configure`

---

## 六、模型列表来源

**模型列表完全来自聚星逸 `/v1/models` 接口实时返回,本 skill 不维护任何本地模型清单。**

脚本处理逻辑:
1. 调 `GET /v1/models` 拿到平台当前所有可用模型
2. 跳过生图/视频模型(ID 含 `image`/`seedream`/`t2v`/`i2v`/`video`/`dall-e`/`happyhorse`)——它们不能用于文本对话
3. 剩余文本模型全部写入配置
4. 主模型取接口返回列表的第一个,其余作 fallbacks

> 这意味着**平台新增模型后,无需更新本 skill**——脚本每次运行都从接口拿最新列表。

---

## 七、openclaw.json 配置结构

配置完成后,`~/.openclaw/openclaw.json` 中新增/更新的段:

```json
{
  "models": {
    "mode": "replace",
    "providers": {
      "fireworks-hub": {
        "baseUrl": "https://fireworks-simulator-api.huo15.com/v1",
        "apiKey": "fsk-你的密钥",
        "api": "openai-completions",
        "models": [
          {
            "id": "DeepSeek-V4-Flash",
            "name": "Deepseek V4 Flash (聚星逸)",
            "reasoning": false,
            "contextWindow": 131072,
            "maxTokens": 8192,
            "input": ["text"],
            "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 }
          }
        ]
      }
    }
  },
  "agents": {
    "defaults": {
      "model": {
        "primary": "fireworks-hub/DeepSeek-V4-Flash",
        "fallbacks": ["fireworks-hub/DeepSeek-V4-Pro", "..."]
      },
      "models": {
        "fireworks-hub/DeepSeek-V4-Flash": { "alias": "Deepseek V4 Flash (聚星逸)" }
      }
    }
  }
}
```

> 模型项的 `reasoning` / `contextWindow` / `maxTokens` 为保守默认值(接口不返回精确参数),可手动调整。

---

## 八、安全注意

- API Key 默认**明文写入** openclaw.json。如需更安全,加 `--env` 用环境变量引用:
  ```bash
  node configure.mjs <fsk-key> --env
  # 然后设置: export FIREWORKS_API_KEY=fsk-你的密钥
  ```
- 脚本每次写入前自动备份 `openclaw.json.bak.<timestamp>`
- **密钥禁止出现在 commit / log / PR / 任何 LLM 上下文**

---

## 九、硬红线

1. ❌ **不在任何文件中硬编码 API Key** — 用户每次提供
2. ❌ **不跳过接口获取** — 必须调 `/v1/models`,不用本地清单
3. ❌ **配置完不问就结束** — 必须主动问用户是否切换模型
4. ❌ **不破坏其他 provider** — 只改 `fireworks-hub` 段
5. ❌ **不忘记备份** — 写入前必须备份 openclaw.json

---

## 十、文件清单

```
huo15-juxingyi-configure/
├── SKILL.md                       # 你正在看的这个(≤ 25KB)
├── _meta.json                     # ClawHub 元数据
├── README.md                      # 详细文档
├── CLAUDE.md                      # 开发规范(内部)
├── LICENSE                        # MIT
├── .gitignore
├── scripts/
│   └── configure.mjs              # 零依赖配置脚本(Node 18+)
└── docs/
    ├── prd.md                     # 产品需求文档
    ├── user-guide.md              # 用户手册 SOP
    ├── dev-guide.md               # 开发者 SOP
    └── changelog.md               # 版本变更历史
```

---

## 十一、版本

- **v1.3.0**(2026-07-19): 新增 `--update` 子命令 — 日常更新模型列表(保留当前主模型,只刷新 providers 段);对比旧列表报告新增/移除;旧主模型下架时自动切换并提示;保留原密钥存储方式。与首次配置(重置主模型)区分,适合平台新增模型后日常刷新。
- **v1.2.0**(2026-07-19): 架构简化 — 删除 `data/model-heuristics.json` 及所有本地硬编码分类逻辑(knownModels/tierPatterns/skipPatterns);模型列表完全来自 `/v1/models` 接口实时返回;主模型改为取接口返回列表的第一个(不再硬编码 DeepSeek-V4-Flash);生图/视频过滤改为脚本内通用正则;删除 `--json`/`--selftest` 子命令;模型参数填保守默认值(接口不返回精确参数)。
- **v1.1.1**(2026-07-19): 健壮性增强 — Node 版本检查、密钥校验、fetchModels 超时与错误分类、`--help`/`--version`/`--selftest` 子命令、`--switch` 前缀匹配、MiniMax 误判根治。
- **v1.0.0**(2026-07-11): 首版 — 动态获取模型列表,自动配置 openclaw.json,默认 DeepSeek-V4-Flash,支持切换。

---

**公司:** 青岛火一五信息科技有限公司 · postmaster@huo15.com · QQ群 1093992108
