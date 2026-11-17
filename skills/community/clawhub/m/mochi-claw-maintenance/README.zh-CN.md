# 龙虾维护与迁移管家

[English](README.md)

核对指定 OpenClaw 实例的助手与绑定，生成含校验值的私有备份，检查变化并在新目录演练恢复。

## 功能

核对指定 OpenClaw 实例的助手与绑定，生成含校验值的私有备份，检查变化并在新目录演练恢复。

## 用法示例

安装后，把下面任意一条发给 AI；涉及文件或网址时，一并提供。

```text
检查这台OpenClaw的助手、工作区和聊天账号绑定，列出需要注意的配置。
```

```text
备份我指定的OpenClaw配置和工作区，保存为私有备份并生成校验清单。
```

```text
验证这个备份，在新目录演练恢复，给我恢复结果和差异清单。
```

核对指定实例的配置与绑定，输出校验备份、差异和新目录恢复演练。实际更新、服务重启和正式迁移通过已有 OpenClaw 工具另行执行。

## 运行要求

Python 3.10+; installed OpenClaw CLI for live status checks

## 安装与开始使用

### MochiLab Skills 助手（推荐）

[首次安装并连接助手](https://mochilab.bz/Skills/Connect.aspx?lang=zh-CN)，然后发送：

```text
安装 mochi-claw-maintenance
```

### ClawHub

[打开 Skill 页面](https://clawhub.ai/hznetnewpower/skills/mochi-claw-maintenance)，或在当前助手工作区执行：

```text
npx clawhub@latest install @hznetnewpower/mochi-claw-maintenance
```

### GitHub

[打开源码目录](https://github.com/hznetnewpower/mochilab-free-skills/tree/main/skills/mochi-claw-maintenance)。下载仓库 ZIP，将 `skills/mochi-claw-maintenance` 放入当前助手工作区的 `skills/` 目录。

安装后新建对话。

## 详细操作说明

[查看技能操作契约](SKILL.md)。命令、字段名和文件路径保留原样；按当前助手工作区执行，先核对依赖，再检查实际输出。
