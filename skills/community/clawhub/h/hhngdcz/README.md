# claude-config-generator

一键为项目生成完整的 `.claude` 配置体系。

## 功能概述

通过交互式引导，自动扫描项目并生成以下配置：

- `CLAUDE.md` — 项目说明文件（通过 `/init` 生成）
- `.claude/settings.json` — 权限、hooks、环境变量配置
- `.claude/settings.md` — 配置字段说明文档
- `.claude/README.md` — 目录结构说明
- `.claude/rules/` — 编码规范等规则文件
- `.claude/skills/` — 从本地或 ClawHub 安装的 skills

## 工作流程

```
阶段 1：扫描项目
   ↓ （静默，自动识别语言、包管理器、目录结构）
阶段 2：安全敏感文件配置
   ↓ （根据扫描结果推荐敏感文件，可跳过）
阶段 3：生成配置文件
   ↓ （目录骨架 + CLAUDE.md + settings + rules）
阶段 4：Skills Hub
   ↓ （本地 skills 选择 → ClawHub 在线安装）
阶段 5：输出汇总
```

## 使用方式

在 Claude Code 中运行：

```
/claude-config-generator
```

## 各阶段说明

### 阶段 1：扫描项目

自动执行，无需交互。扫描项目目录结构，识别包管理器（`package.json`、`pyproject.toml`、`go.mod` 等），推断语言和项目类型。

### 阶段 2：安全敏感文件配置

先询问是否需要配置，可跳过。若选择配置，根据项目目录中的文件名自动推荐敏感文件路径（`.env`、证书、Spring 配置文件、Terraform 变量等），用户选择后写入 `settings.json` 的 `permissions.deny`。

### 阶段 3：生成配置文件

- **目录骨架**：检查 `.claude/` 是否存在，仅创建缺失的子目录
- **CLAUDE.md**：已存在则跳过；不存在则询问是否通过 `/init` 后台生成
- **settings.json**：已存在做深合并，不覆盖；新建则根据包管理器填充 `permissions.allow`
- **其余文件**：`settings.md`（配置说明）、`README.md`（目录说明）、`rules/coding-standards.md`（编码规范）

### 阶段 4：Skills Hub

分两步：

1. **本地 skills**：递归扫描 `~/.claude/skills/` 和 `~/.claude/plugins/marketplaces/` 下所有 SKILL.md，分页展示（每页 10 个），用户输入编号选择安装
2. **ClawHub 在线安装**：根据项目特征自动推荐搜索关键词，通过 `clawhub search` 搜索，`clawhub install` 安装到 `.claude/skills/`

每步均可跳过。

### 阶段 5：输出汇总

等待后台任务完成（如 `/init`），输出完整目录结构预览、已安装 skills 清单和后续操作提示。

## 安全约束

- `CLAUDE.md` 已存在时不做任何修改
- `settings.json` 已存在时做 JSON 深合并
- 严禁在配置文件中写入 API Key、密码等密钥
- 写入文件后自动验证内容正确性

## 依赖

- **ClawHub CLI**（可选，仅在线安装 skills 时需要）：`npm i -g clawhub`

## 版本

- 当前版本：5.0
- 许可证：MIT
