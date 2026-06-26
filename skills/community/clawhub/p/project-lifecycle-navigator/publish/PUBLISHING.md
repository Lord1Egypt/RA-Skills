# Publishing to ClawHub / 发布到 ClawHub

This package is prepared for ClawHub as an instruction-only skill folder.

本包已按 ClawHub 纯文本 Skill 的方式整理。

## Confirmed structure

```text
project-lifecycle-navigator-bilingual/
  SKILL.md
  README.md
  README.zh.md
  README.en.md
  skill.json
  .clawhubignore
  prompts/
    zh/
    en/
  examples/
  publish/
```

## Suggested slug

```text
project-lifecycle-navigator
```

## Suggested display name

```text
Project Lifecycle Navigator / 项目生命周期导航助手
```

## Suggested short description

```text
Bilingual EN/ZH project lifecycle navigator for new project intake, mid-project realignment, and code review upgrade planning.
```

## Suggested tags

```text
project-management,product-management,ai-coding-agent,mvp,code-review,bilingual,chinese,english
```

## Publish command

According to current OpenClaw/ClawHub documentation, ClawHub publishes skills from a local folder containing `SKILL.md` with:

```bash
clawhub skill publish ./project-lifecycle-navigator-bilingual \
  --slug project-lifecycle-navigator \
  --name "Project Lifecycle Navigator / 项目生命周期导航助手" \
  --version 1.0.0 \
  --tags latest,project-management,product-management,ai-coding-agent,mvp,code-review,bilingual
```

Optional dry run if supported by your CLI version:

```bash
clawhub skill publish ./project-lifecycle-navigator-bilingual \
  --slug project-lifecycle-navigator \
  --name "Project Lifecycle Navigator / 项目生命周期导航助手" \
  --version 1.0.0 \
  --tags latest,project-management,product-management,ai-coding-agent,mvp,code-review,bilingual \
  --dry-run
```

## Safety / 安全说明

This skill does not declare or require:

- environment variables
- API keys
- external binaries
- install scripts
- code execution
- network access

本 Skill 不声明也不需要：

- 环境变量
- API Key
- 外部命令
- 安装脚本
- 代码执行
- 网络权限

## Version changelog

### 1.0.0

Initial bilingual release with three modes:

- New Project Intake
- Mid-Project Realignment
- Code Review & Upgrade Plan
