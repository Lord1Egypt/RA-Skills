# No More Forget

> 让 OpenClaw 不再失忆！一键解决记忆问题

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Compatible-blue.svg)](https://github.com/openclaw/openclaw)

## 简介

No More Forget 是一个 OpenClaw Agent Skill，专注于解决记忆系统的三大痛点：

- **失忆** - Agent 忘记之前的对话、决策、约束
- **Token 消耗高** - API 费用快速增长
- **搜不到** - 记忆内容存在但无法检索

## 特性

- ✅ **一键安装** - 5 分钟完成配置
- ✅ **Memory Flush** - 自动保存关键记忆
- ✅ **记忆模板** - 优化的 MEMORY.md 结构
- ✅ **诊断工具** - 一键检测记忆问题
- ✅ **备份恢复** - 自动备份记忆文件

## 安装

### 方式一：从 ClawHub 安装

```bash
clawhub install no-more-forget
cd ~/.openclaw/skills/no-more-forget
bash scripts/install.sh
```

### 方式二：手动安装

```bash
# 克隆仓库
git clone https://github.com/Steventsang18/NoMoreForget.git
cd NoMoreForget

# 运行安装脚本
bash scripts/install.sh

# 验证安装
bash scripts/verify.sh
```

## 使用

### 诊断记忆问题

```bash
bash scripts/diagnose.sh
```

### 优化记忆文件

```bash
bash scripts/optimize_memory.sh
```

### 备份记忆

```bash
bash scripts/backup_memory.sh
```

### 恢复记忆

```bash
bash scripts/restore_memory.sh
```

## 项目结构

```
no-more-forget/
├── SKILL.md              # Skill 主文档
├── scripts/              # 脚本工具
│   ├── install.sh       # 一键安装
│   ├── verify.sh        # 验证安装
│   ├── diagnose.sh      # 诊断问题
│   ├── optimize_memory.sh
│   ├── backup_memory.sh
│   └── restore_memory.sh
├── references/           # 参考文档
│   ├── architecture.md
│   ├── plugins.md
│   └── troubleshooting.md
└── assets/               # 模板文件
    ├── MEMORY.md.template
    └── daily-log.template.md
```

## 与其他插件配合

No More Forget 可以与以下插件配合使用：

| 插件 | 解决问题 | 安装命令 |
|------|---------|---------|
| qmd | 搜索增强 | `clawhub install qmd` |
| lossless-claw | 无损压缩 | `clawhub install lossless-claw` |

**推荐组合**：No More Forget + qmd + lossless-claw

## 许可证

[MIT License](LICENSE)

## 作者

Steventsang18

## 链接

- [GitHub](https://github.com/Steventsang18/NoMoreForget)
- [ClawHub](https://clawhub.com/skills/no-more-forget) (即将上线)