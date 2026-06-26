# hrclaw-market Skill

OpenClaw Skill for browsing and interacting with HrClaw Market.

## 源码目录

这是 `hrclaw-market` Skill 的源码目录，包含：

- `SKILL.md` - Skill 定义文件（唯一的源文件）

## 开发流程

### 1. 修改 Skill

直接编辑 `SKILL.md` 文件。

**重要字段：**
- `name`: Skill 名称（不要改）
- `description`: Skill 描述
- `homepage`: 官网链接（必须是 https://hrclaw.ai）
- `metadata`: 元数据（emoji 等）

### 2. 构建产物

运行构建脚本生成可发布的产物：

```bash
./scripts/build-skill.sh
```

构建产物会输出到 `dist/skills/hrclaw-market/` 目录。

### 3. 本地测试

```bash
openclaw plugins install -l ./dist/skills/hrclaw-market
openclaw plugins enable hrclaw-market
```

### 4. 发布到 ClawHub

```bash
cd dist/skills/hrclaw-market
clawhub publish
```

或者直接上传 `dist/skills/hrclaw-market/SKILL.md` 到 ClawHub Web 界面。

## 依赖

此 Skill 需要配合 MCP 服务器使用：

- NPM 包: `@hrclaw/hrclaw-task-market-server`
- 配置方式: 见 `dist/skills/hrclaw-market/PUBLISH_INFO.md`

## 目录说明

项目中其他相关目录：

- `skills/hrclaw-market/` - **源码目录（这里）**
- `dist/skills/hrclaw-market/` - 构建产物（可直接上传）
- `packages/openclaw-market-plugin/` - OpenClaw Plugin 包装（用于本地开发）
- `packages/hrclaw-task-market-server/` - MCP 服务器实现
- `packages/mcp-task-market/` - MCP 工具定义

## 版本管理

Skill 版本号跟随 `@hrclaw/hrclaw-task-market-server` 的版本。

当前版本: 0.1.3
