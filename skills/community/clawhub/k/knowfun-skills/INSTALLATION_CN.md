# 安装指南 - 多平台

[English](INSTALLATION.md) | 简体中文

Claude Code、Cursor、Cline 和 OpenClaw 的详细安装指南。

---

## 🎯 平台兼容性

| 平台 | 状态 | 主要安装方式 |
|------|------|-------------|
| **Claude Code** | ✅ 完全支持 | `curl` 下载 SKILL.md |
| **Cursor** | ✅ 支持 | `npm install -g knowfun-skills` |
| **Cline** | ✅ 支持 | `npm install -g knowfun-skills` |
| **OpenClaw** | ✅ 支持 | `npx clawhub install knowfun-skills` |

---

## 📦 Claude Code 安装

Claude Code 使用原生技能系统，只需将 `SKILL.md` 放到技能目录即可。

### 方法 1：curl（推荐 — 无需克隆仓库）

```bash
mkdir -p ~/.claude/skills/knowfun
curl -fsSL https://raw.githubusercontent.com/MindStarAI/KnowFun-Skills/master/SKILL.md \
  -o ~/.claude/skills/knowfun/SKILL.md
```

这会在所有 Claude Code 项目中全局安装该技能。

### 方法 2：项目专用

```bash
mkdir -p .claude/skills/knowfun
curl -fsSL https://raw.githubusercontent.com/MindStarAI/KnowFun-Skills/master/SKILL.md \
  -o .claude/skills/knowfun/SKILL.md
```

### 方法 3：通过 npm（如果已全局安装）

```bash
npm install -g knowfun-skills
mkdir -p ~/.claude/skills/knowfun
cp "$(npm root -g)/knowfun-skills/SKILL.md" ~/.claude/skills/knowfun/SKILL.md
```

### 验证安装

在 Claude Code 会话中运行：
```
/knowfun credits
```

预期结果：显示你的积分余额。

### 在 Claude Code 中使用

```bash
/knowfun create course "Python 编程入门"
/knowfun create poster "气候变化事实"
/knowfun status <taskId>
/knowfun detail <taskId>
/knowfun list
/knowfun credits
```

---

## 📦 Cursor 安装

### 步骤 1：安装 CLI 工具

```bash
# 推荐 — 通过 npm 安装
npm install -g knowfun-skills
```

<details>
<summary>备选方案：从本地克隆创建软链接</summary>

```bash
git clone https://github.com/MindStarAI/KnowFun-Skills.git
sudo ln -s $(pwd)/KnowFun-Skills/scripts/knowfun-cli.sh /usr/local/bin/knowfun
chmod +x KnowFun-Skills/scripts/knowfun-cli.sh
```
</details>

### 步骤 2：配置 API Key

```bash
export KNOWFUN_API_KEY="kf_your_api_key_here"

# 永久保存
echo 'export KNOWFUN_API_KEY="kf_your_api_key_here"' >> ~/.zshrc
source ~/.zshrc
```

### 步骤 3：添加 Cursor 规则（可选）

```bash
curl -fsSL https://raw.githubusercontent.com/MindStarAI/KnowFun-Skills/master/integrations/cursor/.cursorrules \
  -o .cursorrules
```

### 验证安装

```bash
knowfun credits
```

### 在 Cursor 中使用

**在终端直接使用：**
```bash
knowfun create course "你的主题"
knowfun status <taskId>
```

**通过自然语言：**
```
使用 knowfun 创建一个关于 Python 基础的课程
```

Cursor 会自动执行对应的 CLI 命令。

---

## 📦 Cline 安装

### 步骤 1：安装 CLI 工具

```bash
npm install -g knowfun-skills
```

### 步骤 2：配置 API Key

```bash
export KNOWFUN_API_KEY="kf_your_api_key_here"

echo 'export KNOWFUN_API_KEY="kf_your_api_key_here"' >> ~/.zshrc
source ~/.zshrc
```

### 步骤 3：添加 Cline 配置（可选）

```bash
mkdir -p .cline
curl -fsSL https://raw.githubusercontent.com/MindStarAI/KnowFun-Skills/master/integrations/cline/knowfun.json \
  -o .cline/knowfun.json
```

### 验证安装

```bash
knowfun credits
```

### 在 Cline 中使用

```
创建一个关于"机器学习基础"的 Knowfun 课程
```

Cline 会自动执行 CLI 命令。

---

## 📦 OpenClaw 安装

### 步骤 1：安装技能

```bash
npx clawhub install knowfun-skills
```

技能将安装到 `~/.openclaw/workspace/skills/knowfun-skills/`。

### 步骤 2：安装 CLI 工具

OpenClaw 技能需要 `knowfun` 二进制文件：

```bash
npm install -g knowfun-skills
```

### 步骤 3：配置 API Key

```bash
export KNOWFUN_API_KEY="kf_your_api_key_here"

echo 'export KNOWFUN_API_KEY="kf_your_api_key_here"' >> ~/.zshrc
source ~/.zshrc
```

### 验证安装

```bash
openclaw skills list | grep knowfun
# 应显示：✓ ready  📚 knowfun
```

### 在 OpenClaw 中使用

**通过自然语言（聊天应用）：**
```
创建一个关于 Python 的 Knowfun 课程
```

**直接使用 CLI：**
```bash
knowfun create course "Python 编程入门"
```

---

## 🔧 通用设置（所有平台）

### 1. 获取 API Key

1. 访问 https://www.knowfun.io/api-platform
2. 点击"创建 API Key"
3. 命名（例如："开发密钥"）
4. 复制密钥（以 `kf_` 开头）

### 2. 设置环境变量

```bash
# 临时（当前会话）
export KNOWFUN_API_KEY="kf_your_api_key_here"

# 永久 — zsh（macOS 默认）
echo 'export KNOWFUN_API_KEY="kf_your_api_key_here"' >> ~/.zshrc && source ~/.zshrc

# 永久 — bash
echo 'export KNOWFUN_API_KEY="kf_your_api_key_here"' >> ~/.bashrc && source ~/.bashrc
```

### 3. 测试安装

```bash
knowfun credits
```

---

## 📊 功能对比

| 功能 | Claude Code | Cursor | Cline | OpenClaw |
|------|:-----------:|:------:|:-----:|:--------:|
| 斜杠命令（`/knowfun`） | ✅ | ❌ | ❌ | ❌ |
| 自动技能调用 | ✅ | ❌ | ❌ | ✅ |
| CLI 工具（`knowfun`） | ✅ | ✅ | ✅ | ✅ |
| 自然语言请求 | ✅ | ✅ | ✅ | ✅ |
| 远程访问（Telegram 等） | ❌ | ❌ | ❌ | ✅ |
| npm 安装 | ✅ | ✅ | ✅ | ✅ |

---

## 🆘 故障排除

### "找不到命令：knowfun"

```bash
npm install -g knowfun-skills
which knowfun  # 验证是否在 PATH 中
```

### "未找到 API Key"

```bash
echo $KNOWFUN_API_KEY    # 检查是否已设置
export KNOWFUN_API_KEY="kf_your_key"
```

### 脚本"权限被拒绝"

```bash
chmod +x $(npm root -g)/knowfun-skills/scripts/knowfun-cli.sh
```

### Claude Code 无法识别技能

确认 SKILL.md 在正确位置：
```bash
ls ~/.claude/skills/knowfun/SKILL.md
```

如果缺失，重新安装：
```bash
mkdir -p ~/.claude/skills/knowfun
curl -fsSL https://raw.githubusercontent.com/MindStarAI/KnowFun-Skills/master/SKILL.md \
  -o ~/.claude/skills/knowfun/SKILL.md
```

---

## 📚 下一步

安装完成后：

1. 跟随[快速入门指南](QUICKSTART_CN.md)
2. 浏览 [examples_CN.md](examples_CN.md) 了解使用模式
3. 阅读 [api-reference_CN.md](api-reference_CN.md) 了解高级配置

---
