# iqiyi-skill 多平台市场分发方案

更新时间：2026-06-16

本文总结 `iqiyi-skill` 分发到 Codex、Claude Code、Cursor、OpenClaw、npm、Hermes 等 Agent Skill 生态的可行路径。结论基于当前公开官方文档；未能核验的入口会明确标注为不确定。

## 结论摘要

| 平台 | 官方公开入口状态 | 推荐分发形态 | 结论 |
| --- | --- | --- | --- |
| Codex | 支持 plugin marketplace、repo/personal marketplace 和 workspace sharing；官方公共 Plugin Directory 自助发布仍是 coming soon | Codex plugin 包，内含 `skills/iqiyi-skill/` | 可以做团队/仓库/个人分发；暂不能自助上官方公共目录 |
| Claude Code | 支持 plugin marketplace；有 `claude-community` 提交流程；官方 marketplace 由 Anthropic 自行精选 | Claude Code plugin 包，内含 `skills/iqiyi-skill/` | 可以提交社区市场审核；官方精选无申请流程 |
| Cursor | 支持 skills、plugins、Cursor Marketplace 提交审核；团队市场需要商业/团队能力 | Cursor plugin 包，内含 `skills/iqiyi-skill/` | 可以走 Cursor Marketplace 审核；注意其市场要求开源和人工 review |
| OpenClaw | ClawHub 是官方公开 registry，支持 skill 和 plugin 发布 | 直接发布 raw skill；如需代码插件再包成 OpenClaw plugin | 最直接，可用 `clawhub skill publish` |
| npm | npm public registry 支持发布 Node package；不是 Agent 官方市场，但可分发 CLI 和 raw skill 文件 | npm package，保留 `bin.iqiyi-cli` 和 `files` 白名单 | 可以作为跨平台安装源；scoped public 包需 `npm publish --access public` |
| Hermes | 未找到可核验的 Hermes Agent 官方 skill marketplace 文档 | 保留 Agent Skills 标准包，等待平台方确认 | 暂不写成确定市场路径 |

## 当前 skill 状态

`iqiyi-skill` 已具备跨平台 Agent Skills 基础结构：

```text
iqiyi-skill/
├── SKILL.md
├── agents/openai.yaml
├── docs/
├── references/
├── scripts/
└── package.json
```

当前 `SKILL.md` 已包含 Agent Skills 风格 frontmatter，`package.json` 也提供了 `iqiyi-cli` 的 package-style bin 入口。发布前仍需要确认：

- `license: Proprietary` 是否符合目标市场。Cursor Marketplace 明确要求 marketplace plugin 开源；Claude 社区市场和 OpenClaw ClawHub 也会涉及审核、扫描和用户信任。
- `description`、`compatibility`、`metadata.version` 与 `package.json.version` 保持一致。
- 对外说明网络依赖：需要访问 `mesh.if.iqiyi.com`，播放能力可能依赖 qips 协议处理器。
- 不承诺登录、会员态、个性化推荐或新增 native 指令能力，避免与当前 MVP 边界冲突。

## 推荐仓库组织

保留 `.cursor/skills/iqiyi-skill` 作为唯一真源，发布时生成平台包，避免在真源目录里混入多个平台 manifest：

```text
dist/agent-skills/iqiyi-skill/          # 标准 raw skill 包
dist/codex/iqiyi-video/                # Codex plugin 包
dist/claude/iqiyi-video/               # Claude Code plugin 包
dist/cursor/iqiyi-video/               # Cursor plugin 包
dist/openclaw/iqiyi-skill/             # ClawHub raw skill 包
dist/npm/iqiyi-skill/                  # npm package 包
```

每次发布前从真源复制这些目录：

```bash
rm -rf dist/agent-skills/iqiyi-skill
mkdir -p dist/agent-skills
cp -R .cursor/skills/iqiyi-skill dist/agent-skills/iqiyi-skill
```

复制后删除不应进入分发包的本地文件，例如 `.DS_Store`、临时验收材料、未确认草稿。`docs/` 可随包发布，但运行时依赖应继续放在 skill 自身的 `references/`、`scripts/`、`assets/` 等目录内。

## 通用发布门禁

每个平台发布前至少跑：

```bash
npm run test:iqiyi-skill
npm run test:iqiyi-qips
npm pack --dry-run ./.cursor/skills/iqiyi-skill
```

如果本机安装了 Agent Skills reference validator，再跑：

```bash
skills-ref validate dist/agent-skills/iqiyi-skill
```

人工检查：

- `SKILL.md` 名称必须是 `iqiyi-skill`，与目录名一致。
- `SKILL.md` 主体保持导航型说明，长 API 文档留在 `references/`。
- CLI 脚本必须自包含、错误信息明确，不依赖仓库外隐式路径。
- qips 拉起必须保留安全护栏：只执行本 skill 生成或校验过的 qips，不执行用户直接粘贴的任意 deeplink 或 shell。
- 发布说明必须写明无登录 MVP 边界和降级策略。
- 对外市场物料准备：README、changelog、license、privacy/terms 链接、图标、截图、默认 prompt、支持邮箱或 issue 链接。
- npm 发布前检查 `npm pack --dry-run` 输出，只允许 `SKILL.md`、`agents/`、`docs/`、`references/`、`scripts/`、`package.json` 等预期文件进入 tarball。

## Codex 分发

Codex 当前分发单位是 plugin。plugin 可以包含 skills、apps、MCP servers 和 hooks。公开官方 Plugin Directory 的自助发布仍未开放；现阶段可用 repo marketplace、personal marketplace、workspace sharing，或等待官方公共目录开放。

### 包结构

```text
dist/codex/iqiyi-video/
├── .codex-plugin/plugin.json
└── skills/
    └── iqiyi-skill/
        ├── SKILL.md
        ├── docs/
        ├── references/
        └── scripts/
```

`dist/codex/iqiyi-video/.codex-plugin/plugin.json` 示例：

```json
{
  "name": "iqiyi-video",
  "version": "0.3.0",
  "description": "Search, recommend, and play iQiyi videos with no-login fallback.",
  "author": {
    "name": "iQiyi AI Native"
  },
  "license": "Proprietary",
  "keywords": ["iqiyi", "video", "search", "recommendation", "playback"],
  "skills": "./skills/",
  "interface": {
    "displayName": "iQiyi Video",
    "shortDescription": "Search, recommend, and play iQiyi videos",
    "longDescription": "No-login iQiyi video skill for content search, recommendation normalization, qips playback, and H5 fallback.",
    "developerName": "iQiyi AI Native",
    "category": "Productivity",
    "capabilities": ["Read", "Network"],
    "defaultPrompt": [
      "Use iQiyi Video to search for movies and return playable candidates.",
      "Use iQiyi Video to recommend family-friendly movies."
    ]
  }
}
```

### 本地和团队分发

Repo marketplace 示例：

```text
plugins/iqiyi-video/
.agents/plugins/marketplace.json
```

`.agents/plugins/marketplace.json` 示例：

```json
{
  "name": "iqiyi-local",
  "interface": {
    "displayName": "iQiyi Local Plugins"
  },
  "plugins": [
    {
      "name": "iqiyi-video",
      "source": {
        "source": "local",
        "path": "./plugins/iqiyi-video"
      },
      "policy": {
        "installation": "AVAILABLE",
        "authentication": "ON_INSTALL"
      },
      "category": "Productivity"
    }
  ]
}
```

验证方式：

```bash
codex plugin marketplace add ./local-marketplace-root
codex plugin marketplace list
```

然后在 Codex app 的 Plugins 页面或 CLI `/plugins` 中安装。若要分享给 ChatGPT workspace 成员，在 Codex app 中进入 Created by you，打开插件详情并 Share。该方式不等于发布到官方公共目录。

## Claude Code 分发

Claude Code 同时支持 standalone skills 和 plugins。要分发给团队或社区，使用 plugin；plugin 内 skill 命令会带命名空间，例如 `/iqiyi-video:iqiyi-skill`。

### 包结构

```text
dist/claude/iqiyi-video/
├── .claude-plugin/plugin.json
└── skills/
    └── iqiyi-skill/
        ├── SKILL.md
        ├── docs/
        ├── references/
        └── scripts/
```

`dist/claude/iqiyi-video/.claude-plugin/plugin.json` 示例：

```json
{
  "name": "iqiyi-video",
  "description": "Search, recommend, and play iQiyi videos with no-login fallback.",
  "version": "0.3.0",
  "author": {
    "name": "iQiyi AI Native"
  },
  "homepage": "https://www.iqiyi.com/",
  "repository": "https://github.com/<org>/<repo>",
  "license": "Proprietary"
}
```

本地验证：

```bash
claude --plugin-dir ./dist/claude/iqiyi-video
/iqiyi-video:iqiyi-skill
claude plugin validate ./dist/claude/iqiyi-video
```

社区市场提交：

- 先把插件放到公开或可审核的 Git 仓库，并固定版本。
- 运行 `claude plugin validate`。
- 用 Anthropic 提供的插件提交表单提交审核。
- 通过后进入 `claude-community`，用户可添加社区市场并安装。

注意：`claude-plugins-official` 是 Anthropic 自行精选的官方市场，没有公开申请流程；提交表单面向社区市场，不保证进入官方精选。

## Cursor 分发

Cursor 支持 `.cursor/skills/` 的 raw skills，也支持 `.cursor-plugin/plugin.json` 的 plugin。要进入 Cursor Marketplace，使用 plugin。

### 包结构

```text
dist/cursor/iqiyi-video/
├── .cursor-plugin/plugin.json
└── skills/
    └── iqiyi-skill/
        ├── SKILL.md
        ├── docs/
        ├── references/
        └── scripts/
```

`dist/cursor/iqiyi-video/.cursor-plugin/plugin.json` 示例：

```json
{
  "name": "iqiyi-video",
  "description": "Search, recommend, and play iQiyi videos with no-login fallback.",
  "version": "0.3.0",
  "author": {
    "name": "iQiyi AI Native"
  }
}
```

本地验证：

```bash
mkdir -p ~/.cursor/plugins/local
ln -s /absolute/path/to/dist/cursor/iqiyi-video ~/.cursor/plugins/local/iqiyi-video
```

然后重启 Cursor 或执行 Developer: Reload Window，确认 Rules/Skills 面板中能看到 skill，并在 Agent chat 中用 `/iqiyi-skill` 或 plugin 暴露的入口验证。

市场提交：

- Cursor 文档指向 `https://cursor.com/marketplace/publish`。
- Marketplace plugin 需要人工 review。
- Cursor FAQ 写明 marketplace plugins 必须 open source，且每次更新也会 review。若 `iqiyi-skill` 继续保持 `Proprietary`，发布前必须先确认是否能改许可证或走私有团队市场。
- 多插件仓库可增加 `.cursor-plugin/marketplace.json`。

## OpenClaw / ClawHub 分发

OpenClaw 的 ClawHub 是公开 registry，支持直接发布 skills，也支持发布 plugins。`iqiyi-skill` 当前最适合先走 raw skill。

### Raw skill 发布

准备包：

```bash
rm -rf dist/openclaw/iqiyi-skill
mkdir -p dist/openclaw
cp -R .cursor/skills/iqiyi-skill dist/openclaw/iqiyi-skill
```

发布前 dry-run：

```bash
npm i -g clawhub
clawhub login
clawhub skill publish dist/openclaw/iqiyi-skill \
  --slug iqiyi-skill \
  --name "iQiyi Skill" \
  --version 0.3.0 \
  --changelog "Initial no-login MVP marketplace package." \
  --tags latest,video,search,recommendation,playback \
  --dry-run
```

确认计划无误后移除 `--dry-run`：

```bash
clawhub skill publish dist/openclaw/iqiyi-skill \
  --slug iqiyi-skill \
  --name "iQiyi Skill" \
  --version 0.3.0 \
  --changelog "Initial no-login MVP marketplace package." \
  --tags latest,video,search,recommendation,playback
```

用户安装：

```bash
openclaw skills search "iqiyi"
openclaw skills install iqiyi-skill
openclaw skills update --all
```

ClawHub 是开放上传模型，官方文档说明发布需要通过 GitHub 账号门槛，公开页会展示扫描状态，scan-held 或 blocked release 可能从公开 catalog 和安装入口消失。发布后要持续关注安全扫描和用户报告。

## npm 分发

npm 可以作为独立分发渠道，但它是 JavaScript package registry，不是 Agent 官方 marketplace。它适合分发两类东西：

- `iqiyi-cli`：当前 `package.json` 已声明 `bin.iqiyi-cli`，用户可全局安装后直接执行命令。
- raw skill 文件：当前 `files` 已包含 `SKILL.md`、`agents/`、`docs/`、`references/`、`scripts/`，支持其他平台或安装器从 npm 包中解出 skill。

### 包结构

当前 skill 目录已经接近可发布 npm package：

```text
.cursor/skills/iqiyi-skill/
├── package.json
├── SKILL.md
├── agents/
├── docs/
├── references/
└── scripts/
```

建议发布前补一个 npm 面向用户的 `README.md`，说明：

- 这是无登录 MVP，不支持登录、会员态和个性化推荐闭环。
- Node.js 版本要求是 22+。
- 需要访问 `mesh.if.iqiyi.com`。
- qips 播放能力依赖本机协议处理器；无客户端时返回 H5 降级。
- CLI 示例和 Agent Skills 安装方式。

如果准备公开发布，建议把包名改成组织 scope，例如：

```json
{
  "name": "@iqiyi/iqiyi-skill",
  "version": "0.3.0",
  "description": "iQiyi video search, recommendation, and playback skill with a package-style CLI entry.",
  "license": "Proprietary",
  "type": "module",
  "bin": {
    "iqiyi-cli": "./scripts/iqiyi-cli.mjs"
  },
  "files": [
    "SKILL.md",
    "agents",
    "docs",
    "references",
    "scripts"
  ],
  "engines": {
    "node": ">=22"
  },
  "keywords": [
    "agent-skill",
    "iqiyi",
    "video",
    "search",
    "recommendation",
    "playback"
  ]
}
```

使用 scoped public 包时，npm 官方要求发布命令带 `--access public`。如果继续使用 unscoped `iqiyi-skill`，则可直接 `npm publish`，但包名抢占、品牌归属和命名冲突风险更高。

### 发布流程

准备 npm 包：

```bash
rm -rf dist/npm/iqiyi-skill
mkdir -p dist/npm
cp -R .cursor/skills/iqiyi-skill dist/npm/iqiyi-skill
```

检查包内容：

```bash
cd dist/npm/iqiyi-skill
npm pack --dry-run
```

本地安装验证：

```bash
npm install /absolute/path/to/dist/npm/iqiyi-skill
node ./scripts/iqiyi-cli.mjs video search --q "周星驰" --pageNum 1 --dry-run
```

发布 unscoped public 包：

```bash
npm login
npm publish
```

发布 scoped public 包：

```bash
npm login
npm publish --access public
```

如果通过 GitHub Actions 或 GitLab CI/CD 发布，优先使用 npm trusted publishing 或 `--provenance`。npm provenance 能把包和公开源码、构建流程关联起来，提高供应链可审计性，但不代表包本身无恶意或已被 npm 审核。

用户安装：

```bash
npm install -g @iqiyi/iqiyi-skill
iqiyi-cli video search --q "周星驰" --pageNum 1
```

临时执行：

```bash
npx @iqiyi/iqiyi-skill video search --q "周星驰" --pageNum 1
```

如果目标 Agent 客户端不支持直接从 npm 加载 Agent Skill，需要提供一个安装脚本或平台插件，把 npm 包里的 `SKILL.md`、`references/`、`scripts/` 复制到该平台的 skill 目录。npm 在这里承担“下载和版本分发”职责，不自动完成 Agent 平台注册。

## Hermes 分发

截至 2026-06-16，未找到可核验的 Hermes Agent 官方 skill marketplace、提交表单、CLI 发布命令或 manifest 规范。不要把 Hermes 写成已经具备官方市场发布路径。

当前可准备的动作：

1. 保留 `dist/agent-skills/iqiyi-skill/` 作为符合 Agent Skills 标准的 raw skill 包。
2. 保留 `package.json` 的 `bin.iqiyi-cli`，方便支持 Node package-style 扩展的客户端使用。
3. 等 Hermes 平台方确认以下信息后再补专属适配：
   - skill 安装目录或 marketplace manifest。
   - 是否接受 raw `SKILL.md` 包，还是要求 plugin。
   - 是否支持 `scripts/` 执行和 Node 22+。
   - 发布审核、许可证、隐私、网络访问声明要求。
   - 是否有 dry-run/validate 命令。

临时对外说法：

```text
iqiyi-skill is packaged as an Agent Skills-compatible folder. Hermes-specific marketplace publishing is pending official distribution documentation.
```

## 发布顺序建议

1. 先发布 OpenClaw ClawHub raw skill：路径最短，可验证 install/update 闭环。
2. 发布 npm package：为 `iqiyi-cli` 和 raw skill 提供稳定包源，后续平台插件可复用该包。
3. 同步整理 Claude Code plugin：社区市场有明确提交流程，适合作为跨 Agent Skills 生态样板。
4. 做 Cursor plugin：先解决许可证和开源要求，再提交 Cursor Marketplace。
5. 做 Codex plugin：先走 repo/personal marketplace 或 workspace sharing；等待官方公共目录自助发布开放。
6. Hermes 保持标准包，不承诺具体市场发布。

## 主要风险

| 风险 | 影响 | 处理 |
| --- | --- | --- |
| 许可证不匹配 | Cursor 等市场可能拒绝 proprietary 包 | 发布前决定是否改开源许可证、拆出公开版，或只走私有分发 |
| 品牌和内容授权 | 第三方市场公开展示 iQiyi 名称、接口、播放能力可能触发合规审查 | 准备官网、隐私、服务条款、品牌授权说明 |
| 外网/内网接口可达性 | 用户环境访问不了 `mesh.if.iqiyi.com` 或 qips handler | compatibility 和 README 中写清楚环境要求与 H5 降级 |
| qips deeplink 安全 | 误执行用户粘贴 deeplink 或嵌套危险协议 | 保留现有 qips 安全护栏，发布说明强调只执行生成/校验过的 qips |
| 市场安全扫描 | OpenClaw/Cursor/Claude 审核可能拦截脚本型 skill | 减少安装时副作用，脚本只在用户任务触发时运行，提供 dry-run 和明确错误信息 |
| npm 包污染或误发 | npm 无人工上架审核，错误版本名发布后不可复用同一 name/version | 使用 scope、2FA/trusted publishing、`npm pack --dry-run`、staged publishing 或 CI 审批 |
| npm 不等于 Agent 注册 | 用户装到 npm 包后，Agent 客户端未必自动发现 `SKILL.md` | 文档中明确安装器责任，必要时提供平台插件或复制脚本 |
| 能力边界误解 | 用户以为支持登录、会员、个性化推荐 | marketplace 文案明确写 no-login MVP 和排除项 |

## 参考链接

- Agent Skills specification: https://agentskills.io/specification
- Codex skills: https://developers.openai.com/codex/skills
- Codex plugins and marketplace: https://developers.openai.com/codex/plugins
- Codex build plugins: https://developers.openai.com/codex/plugins/build
- Claude Code skills: https://code.claude.com/docs/en/skills
- Claude Code plugins: https://code.claude.com/docs/en/plugins
- Cursor skills: https://cursor.com/docs/skills
- Cursor plugins: https://cursor.com/docs/plugins
- Cursor publish: https://cursor.com/marketplace/publish
- OpenClaw docs: https://docs.openclaw.ai/
- ClawHub docs: https://docs.openclaw.ai/clawhub
- npm scoped public packages: https://docs.npmjs.com/creating-and-publishing-scoped-public-packages
- npm publish CLI: https://docs.npmjs.com/cli/v11/commands/npm-publish
- npm provenance: https://docs.npmjs.com/generating-provenance-statements
