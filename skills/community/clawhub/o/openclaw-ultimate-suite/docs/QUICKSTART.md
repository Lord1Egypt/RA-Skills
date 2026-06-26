# 🚀 OpenClaw 终极套件 - 快速开始指南

> 30 个技能一站式整合 × 61 个专业 Agent × 安全内置 × 自动激活

---

## ⏱️ 5 分钟快速开始

### 步骤 1：安装整合包 (1 分钟)

```bash
# 方式 1：ClawHub 一键安装
clawhub install openclaw-ultimate-suite

# 方式 2：本地使用 (已安装技能)
cd ~/.openclaw/workspace/openclaw-ultimate-suite
```

### 步骤 2：验证安装 (1 分钟)

```bash
# 检查技能数量
ls skills/ | wc -l  # 应该显示 30

# 测试安全检测
python3 skills/ironclaw-guardian-evolved/scripts/ironclaw_audit.py scan skills/office/SKILL.md
```

### 步骤 3：首次使用 (3 分钟)

#### 方式 A：自动激活 (推荐)
```bash
# 直接说需求，晴晴自动识别并激活技能
"我想做个电商网站"
→ 自动激活：agency-agents + ironclaw + todolist
```

#### 方式 B：手动调用
```bash
# 办公场景
/openclaw skill use office "帮我创建周报模板"

# 社交媒体场景
/openclaw skill use xiaohongshu-mcp "发布一篇产品测评"

# 产品开发场景
/orchestrator "开发一个电商网站 MVP"
```

---

## 🎯 核心功能

### 1. 自动技能激活

晴晴自动识别你的需求并激活最合适的技能组合：

| 场景 | 触发词 | 自动激活 |
|------|--------|----------|
| 产品开发 | "开发"、"MVP"、"网站" | agency-agents + ironclaw + todolist |
| 市场调研 | "分析"、"竞品"、"报告" | multi-search-engine + playwright + summarize |
| 办公效率 | "文档"、"周报"、"会议" | office + note + calendar |
| 社交媒体 | "小红书"、"抖音"、"发布" | xiaohongshu-mcp + social-media-scheduler |

### 2. 61 个专业 Agent

```bash
# 使用编排器 (推荐)
/orchestrator "开发一个完整的电商网站"

# 使用单个 Agent
/agent frontend-developer "创建 React 登录页面"
/agent growth-hacker "设计增长策略"
```

### 3. 安全内置

所有技能经过 **ironclaw-guardian-evolved** 免费本地检测：
- ✅ 无危险命令
- ✅ 无硬编码密钥
- ✅ 无 Prompt Injection

---

## 📋 完整技能清单

### 办公效率 (6 个)
office, productivity, note, writing-assistant, calendar, todolist

### 生活助手 (2 个)
weather, email-daily-summary

### 社交媒体 (3 个)
xiaohongshu-mcp, social-media-scheduler, tiktok-crawling

### 信息收集 (4 个)
multi-search-engine, playwright, summarize, ontology

### AI 代理 (3 个)
agency-agents (61 个 Agent), proactive-agent-lite, xiucheng-self-improving-agent

### 安全守护 (3 个)
ironclaw-guardian-evolved, skill-vetter, openclaw-guardian-ultra

### GitHub 克隆 (4 个)
openclaw-free-web-search, openclaw-hierarchical-task-spawn, openclaw-github-repo-commander, openclaw-feishu-file-delivery

### CLI 工具 (1 个)
cli-anything

---

## 🔧 初始化配置

### P0 - 立即配置 (免费)

```bash
# Playwright 浏览器自动化
playwright install
playwright install-deps
```

### P1 - 可选配置

```bash
# SearXNG 自托管搜索 (可选)
docker run -d -p 8080:8080 searxng/searxng
```

---

## 🧠 多模型策略 - 优先云端

**默认配置**: 优先云端模型 (质量最高)

| 模型 | 用途 |
|------|------|
| qwen3.5:397b-cloud | 主模型，复杂任务 |
| kimi-k2.5:cloud | 长文本 (128k 上下文) |
| qwen3-coder:480b-cloud | 编码专用 |
| deepseek-v3.1:671b-cloud | 深度分析 |
| minimax-m2.5:cloud | 创意写作 |

**Fallback**: 云端不可用时自动切换到本地模型

---

## 📚 下一步学习

1. **自动激活规则** → `docs/auto-activation.md`
2. **安全指南** → `docs/security-guide.md`
3. **最佳实践** → `docs/best-practices.md`
4. **使用示例** → `examples/` 目录

---

## 🎉 完成！

现在你可以：
- ✅ 直接说需求，晴晴自动激活技能
- ✅ 手动调用特定技能
- ✅ 使用 61 个专业 Agent
- ✅ 享受免费安全检测

**开始你的第一个任务吧!** ✨

---

*最后更新：2026-03-15*  
*版本：3.0.0 晴晴超级版*
