# MyKnowledge 安装指南

## 支持的 AI 平台

| 平台 | 支持版本 | 安装方式 |
|------|----------|----------|
| CodeBuddy | 最新版 | SkillHub / GitHub |
| WorkBuddy | 最新版 | SkillHub / GitHub |
| OpenClaw | 最新版 | SkillHub / GitHub |
| Claude | 最新版 | SkillHub / GitHub |

---

## 安装步骤

### 方式一：SkillHub 安装（推荐，无需终端）

对 AI 说一句话即可：
```
安装 my-knowledge 技能
```

> 💡 升级方法：对 AI 说"安装 my-knowledge 技能"即可覆盖为新版，用户数据（~/.myknowledge/）不受影响。

---

### 方式二：Git 安装（备选，需要终端）

一行命令完成下载+安装（以 CodeBuddy 为例）：

```bash
# 国内用户推荐 Atomgit
git clone https://atomgit.com/CoderMoray/MyKnowledge.git ~/.codebuddy/skills/myknowledge/

# 或使用 GitHub
git clone https://github.com/CoderMoray/MyKnowledge.git ~/.codebuddy/skills/myknowledge/
```

其他平台替换路径：
- WorkBuddy：`~/.workbuddy/skills/myknowledge/`
- OpenClaw：`~/.openclaw/skills/myknowledge/`
- Claude：`~/.claude/plugins/myknowledge/`

---

## 验证安装

> ⚠️ **重要**：安装完成后 Skill 不会自动运行。你需要主动说一句话来触发首次引导。

对 AI 说：

```
创建知识库
```

AI 会自动检测到首次使用，执行约 1 分钟的引导设置（选择知识库类型、开启自动记录等）。之后说同样的话会直接创建知识库。

> 💡 如果 AI 只回复"安装完成"没有引导，说明它没加载 Skill。直接说"创建知识库"即可触发。

---

## 可选配置

### OpenClaw 启用 Hook（推荐）

OpenClaw 用户可启用 Hook 实现真正的智能任务追踪：

```bash
# 启用 Hook
openclaw hooks enable myknowledge

# 验证 Hook 状态
openclaw hooks list
```

---

## 卸载

```bash
# CodeBuddy
rm -rf ~/.codebuddy/skills/myknowledge

# WorkBuddy
rm -rf ~/.workbuddy/skills/myknowledge

# OpenClaw
rm -rf ~/.openclaw/skills/myknowledge
```

---

## 故障排除

### 问题：Skill 未加载

**检查清单**:
1. 目录名是否为 `myknowledge`（小写）
2. SKILL.md 是否在目录根级别
3. AI 是否已重启

### 问题：首次引导未显示

**检查清单**:
1. 检查 `skill-state.yaml` 是否已存在
2. 删除 `skill-state.yaml` 重新加载

### 问题：权限错误

**解决**: 在系统设置或终端中调整目录权限，确保 AI 有读取权限。

---

## 获取帮助

- GitHub Issues: https://github.com/CoderMoray/MyKnowledge/issues
- 文档: https://github.com/CoderMoray/MyKnowledge/blob/main/README.md

---

**最后更新**: 2026-06-10
