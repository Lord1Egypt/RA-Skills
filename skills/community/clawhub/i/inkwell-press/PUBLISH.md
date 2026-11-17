# ClawHub 发布参数备忘

## 方式一：网页表单上传 zip（推荐）

下载 `inkwell-clawhub-skill-v0.8.1.zip`，在 ClawHub 的「Generate」页面填：

| 字段 | 值 |
|------|-----|
| **DISPLAY NAME** | `Inkwell` |
| **SLUG** | `inkwell`（被占用则 `inkwell-press`） |
| **CATEGORIES** | `Productivity` + `Creative` + `Development` |
| **TOPICS** | `markdown, wechat, html, publishing, content-pipeline, social-media` |
| **License** | `MIT-0`（默认，不可改） |

上传文件：选择 `inkwell-clawhub-skill-v0.8.1.zip`

## 方式二：CLI 发布

> ⚠️ **供应链安全**：所有 ClawHub CLI 调用必须固定到 `0.23.3`（截至 2026-09-14 的最新稳定版）。
> 发布前请到 npm 确认 `0.23.3` 仍是最新且无安全告警，如有新版本需先审查再升级。

### 推荐方式：全局安装固定版本

```bash
# 1. 固定版本安装 ClawHub CLI（避免 rug pull 风险）
npm install -g clawhub@0.23.3

# 2. 登录（首次）
clawhub login

# 3. 发布
clawhub publish ./clawhub-publish/ \
  --slug inkwell \
  --name "Inkwell" \
  --version 0.8.1 \
  --changelog "Full content pipeline: Markdown to WeChat HTML, covers, social cards, publish." \
  --tags latest

# 4. 验证
clawhub inspect inkwell
```

### 备选方式：npx 带固定版本号

不想全局安装时，用 `npx` 并指定确切版本号 `0.23.3`：

```bash
npx clawhub@0.23.3 login
npx clawhub@0.23.3 publish ./clawhub-publish/ --slug inkwell ...
npx clawhub@0.23.3 inspect inkwell
```

## 文件清单

```
clawhub-publish/
├── SKILL.md           # ClawHub 规范的 Skill 定义（含 frontmatter + 安全须知）
├── README.md          # Listing 页展示（含数据安全须知）
├── requirements.txt   # 固定版本 + SHA256 哈希（供应链安全）
├── SUPPLY_CHAIN.md    # 可复现构建 + SBOM + 传递依赖锁定 + 审计清单
└── PUBLISH.md         # 本文件（发布参数备忘）
```

## 发布前自查

- [x] SKILL.md 的 frontmatter 含 `name` / `description` / `version`
- [x] `name` 符合 `^[a-z0-9][a-z0-9-]*$`（小写+连字符）
- [x] `version` 是 semver（0.8.1）
- [x] 没有非文本文件（.png / .jpg / .bin 全部排除）
- [x] 没有 LICENSE 文件（ClawHub 强制 MIT-0，自己不要加）
- [x] 没有敏感信息 / 凭证
- [x] `description` ≤ 100 字

## 安全审查修复对照

### 第一轮（v0.8.1 初版审查）

| 审查发现 | 级别 | 修复 |
|---------|------|------|
| T08 不安全的依赖关系 | 中等 | install 改为 `inkwell-press==0.8.1`（固定版本）；源码安装改 `git checkout --detach <sha>`；新增 `requirements.txt` 带 SHA256 哈希 |
| 缺少用户警告（剪贴板/微信发布） | 中等 | SKILL.md 顶部加「Safety & Data Handling」表格，列出每个操作的数据去向；Agent 行为约定 4 条 |
| 缺少图片上传隐私警告 | 中等 | 同上表格中 `run` 行 + README.md 顶部 blockquote 安全须知 |
| 触发词过于宽泛 | 中等 | 收窄为「仅在用户明确要求公众号排版或发布时触发」，加了「不应触发的场景」反向清单 |
| 剪贴板覆盖未警告 | 低 | 安全表格 + Agent 行为约定第 1 条 |

### 第四轮（v1.0.3 上线后审查）

| 审查发现 | 级别 | 修复 |
|---------|------|------|
| T08 外部依赖不可审计（Skill 包只含文档） | Warning | 新增 `SUPPLY_CHAIN.md`：可复现构建步骤（从 pinned commit 构建 wheel 验证哈希）、SBOM（pip-tools --generate-hashes 锁定传递依赖）、npm 锁文件指引、安装前审计清单；SKILL.md 安装段引用该文件 |
| T09 README 仍称「不配置=不出网」与外链图下载矛盾 | Warning | README 安全须知删除「不配置环境变量时为纯本地模式，不产生出网请求」绝对断言；改为明确警告「外链图默认下载，不受环境变量影响」；`--no-embed-external` 提升到 README 首要安全须知 |

### 第三轮（v1.0.2 上线后审查）

| 审查发现 | 级别 | 修复 |
|---------|------|------|
| MCP Rug Pull：CLI 调用未固定真实版本号 | 中等 ×5 | PUBLISH.md 所有 CLI 调用固定到真实版本号 `0.23.3`；占位符全部消除 |

### 第二轮（v1.0.1 上线后审查）

| 审查发现 | 级别 | 修复 |
|---------|------|------|
| MCP Rug Pull：ClawHub CLI 未固定版本号 | 中等 ×3 | PUBLISH.md CLI 段改为先固定版本 `0.23.3` 全局安装再调用，禁止不带版本号的 npx 调用 |
| Intent-Code Divergence：「纯本地，不出网」但外链图默认下载 | 中等 | 去掉「纯本地操作」和「不产生出网请求」的绝对断言，改为明确说明外链图默认下载 + `--no-embed-external` 禁止方式 |
| Intent-Code Divergence：环境段「不配置=不出网」 | 中等 | 同上，环境段去掉绝对断言 |
| requirements.txt 注释纯中文违反语言策略 | 低 | 改为英中双语注释 |
