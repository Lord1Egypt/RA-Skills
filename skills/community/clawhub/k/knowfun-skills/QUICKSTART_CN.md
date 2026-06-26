# 🚀 快速入门指南

[English](QUICKSTART.md) | 简体中文

5 分钟内开始使用 Knowfun.io — 支持 Claude Code、Cursor、Cline 和 OpenClaw。

---

## 选择你的平台

| 平台 | 安装方式 | 耗时 |
|------|----------|------|
| **Claude Code** | `curl` 下载 SKILL.md | ~1 分钟 |
| **Cursor / Cline** | `npm install -g knowfun-skills` | ~30 秒 |
| **OpenClaw** | `npx clawhub install knowfun-skills` | ~30 秒 |

---

## 第 1 步：安装

### Claude Code

```bash
# 全局安装技能
mkdir -p ~/.claude/skills/knowfun
curl -fsSL https://raw.githubusercontent.com/MindStarAI/KnowFun-Skills/master/SKILL.md \
  -o ~/.claude/skills/knowfun/SKILL.md
```

### Cursor / Cline

```bash
npm install -g knowfun-skills
```

### OpenClaw

```bash
npx clawhub install knowfun-skills
```

---

## 第 2 步：获取 API Key（2 分钟）

1. 访问 https://www.knowfun.io/api-platform
2. 点击"创建 API Key"
3. 命名（例如："我的开发密钥"）
4. 复制 API key（以 `kf_` 开头）

---

## 第 3 步：配置（30 秒）

```bash
# 当前会话临时生效
export KNOWFUN_API_KEY="kf_your_api_key_here"

# 或永久写入配置（推荐）
echo 'export KNOWFUN_API_KEY="kf_your_api_key_here"' >> ~/.zshrc
source ~/.zshrc
```

---

## 第 4 步：验证安装

```bash
knowfun credits
```

预期输出：
```
✅ Available: 1,000 credits
📊 Total Earned: 1,000 credits
📉 Total Used: 0 credits
```

> **Claude Code 用户**：在 Claude Code 会话中运行 `/knowfun credits`。

---

## 第 5 步：创建第一个内容（2 分钟）

### Claude Code

自然语言提问：
```
帮我创建一个关于"Python 编程入门"的 Knowfun 课程
```

或直接使用斜杠命令：
```
/knowfun create course "Python 编程入门：变量、循环和函数"
```

### Cursor / Cline / OpenClaw

```bash
knowfun create course "Python 编程入门"
```

或告诉你的 AI 助手：
```
使用 knowfun 创建一个关于 Python 基础的课程
```

---

## 接下来会发生什么

任务将在后台处理，2–5 分钟内你将获得一个可分享的 URL。

查看状态：
```bash
knowfun status <taskId>
```

获取结果 URL：
```bash
knowfun detail <taskId>
```

---

## 所有内容类型

```bash
knowfun create course "Python 编程入门"
knowfun create poster "气候变化：关键事实"
knowfun create game   "学习 JavaScript 变量"
knowfun create film   "互联网的历史"
```

处理时间：海报 1–3 分钟 · 课程 2–5 分钟 · 游戏 3–7 分钟 · 视频 5–10 分钟

---

## 查看积分与配置

```bash
knowfun credits   # 查看积分余额
knowfun schema    # 查看所有配置选项
knowfun list 10   # 最近的任务
```

---

## 故障排除

### "找不到命令：knowfun"
```bash
npm install -g knowfun-skills
```

### "未找到 API Key"
```bash
echo $KNOWFUN_API_KEY          # 检查是否已设置
export KNOWFUN_API_KEY="kf_…"  # 设置它
```

### "积分不足"
访问 https://www.knowfun.io/api-platform 充值。

### 任务卡在 "processing"
再等几分钟。若超过 15 分钟仍未完成，请联系支持团队。

---

## 文档

- **[README_CN.md](README_CN.md)** — 完整概述
- **[INSTALLATION_CN.md](INSTALLATION_CN.md)** — 各平台详细安装指南
- **[api-reference_CN.md](api-reference_CN.md)** — 完整 API 参考
- **[examples_CN.md](examples_CN.md)** — 20+ 使用示例

---

**需要更多帮助？** 查看 [examples_CN.md](examples_CN.md) 或提交 [GitHub Issue](https://github.com/MindStarAI/KnowFun-Skills/issues)。
