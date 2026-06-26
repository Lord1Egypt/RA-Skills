# AGENTS.md — 多工具适配配置

本文件定义了个人 AI 记忆系统在不同 AI 工具中的配置建议。
选择你使用的工具，按对应说明安装和配置。

---

## Claude Code

**推荐程度**：⭐⭐⭐⭐⭐（最佳适配）

```bash
# 推荐方式（通过 skills CLI）
npx skills add ChenChen913/memory-system -a claude-code

# 或手动克隆安装
git clone https://github.com/ChenChen913/memory-system.git
cp -r memory-system/ ~/.claude/skills/
```

**配置建议：**
- 在 `.claude/settings.json` 中设置 `"autonomousInvocation": false`，确保 Skill 仅在用户明确触发时调用
- 将 `/memory/` 目录添加到项目工作区，或放在 `~/.memory/` 全局目录
- 建议开启对话持久化，确保跨会话的上下文一致性

**使用示例：**
```
# 触发记录
"记录今天"
"帮我做个决策推演"
"生成本月月报"
```

---

## Cursor

**推荐程度**：⭐⭐⭐⭐

**安装方式：**
将 `memory-system/` 文件夹放入项目根目录或 `~/.cursor/rules/` 目录。

在 `.cursorrules` 中添加：
```
当用户说"记录今天"、"写日记"、"帮我做决策"等相关指令时，
读取 memory-system/SKILL.md 并按其中的指引执行。
所有文件操作限制在 /memory/ 目录内，不访问其他目录。
```

**注意事项：**
- Cursor 的 AI 内容会通过 OpenAI/Anthropic API 处理，你的日记内容会发送至相应服务器
- 建议将 `/memory/` 加入 `.gitignore`，避免隐私数据被提交到代码仓库

---

## Gemini CLI

**推荐程度**：⭐⭐⭐⭐

**安装方式：**
```bash
# 将 Skill 放入 Gemini CLI 的 instructions 目录
cp -r memory-system/ ~/.gemini/instructions/memory-system/
```

在 `~/.gemini/config.yaml` 中添加：
```yaml
instructions:
  - path: ~/.gemini/instructions/memory-system/SKILL.md
    trigger_keywords:
      - "记录今天"
      - "写日记"
      - "帮我做决策"
      - "生成月报"
```

**注意事项：**
- Gemini CLI 的内容会发送至 Google 服务器，受 Google 隐私政策约束
- 建议查阅 Google AI 的企业数据保护选项

---

## OpenClaw

**推荐程度**：⭐⭐⭐⭐⭐

**安装方式：**
```bash
# OpenClaw 直接支持 Skill 文件
openclaw skill add ./memory-system.skill
```

**配置建议：**
在 OpenClaw 的 memory 配置中，将 `/memory/` 指定为持久化目录：
```json
{
  "memory_dir": "~/.memory/",
  "skill_auto_invoke": false,
  "skill_data_local_only": true
}
```

**OpenClaw 特别说明：**
- OpenClaw 通过 API 直接调用，不经过大厂的排队系统，隐私性相对更可控
- 建议使用支持本地模型的 OpenClaw 配置，实现数据完全不出本地

---

## Trae

**推荐程度**：⭐⭐⭐

**安装方式：**
在 Trae 的 Agent 配置中，将 SKILL.md 内容添加为 System Prompt 的一部分。

```
# 在 Trae 的 Agent 设置中：
System Prompt 开头添加：
"你是用户的个人AI记忆系统，以下是你的操作规范：[粘贴 SKILL.md 内容]"
```

**注意事项：**
- Trae 属于大厂产品，数据会经过其服务器处理
- 建议关闭 Trae 的"任务监控"功能，减少不必要的数据分析
- 敏感内容建议使用脱敏或代号代替真实姓名

---

## Codex（OpenAI Codex CLI）

**推荐程度**：⭐⭐⭐

**安装方式：**
```bash
# 将 SKILL.md 作为 Codex 的 instructions 文件
export CODEX_INSTRUCTIONS_FILE="./memory-system/SKILL.md"

# 或在项目中创建 .codex/instructions.md
cp memory-system/SKILL.md .codex/instructions.md
```

**注意事项：**
- Codex 内容发送至 OpenAI 服务器，受 OpenAI 隐私政策约束
- OpenAI 提供企业级零数据保留选项，如有需要可申请

---

## 本地模型（Ollama / LM Studio 等）

**推荐程度**：⭐⭐⭐⭐⭐（最高隐私保护）

**推荐理由：**
如果你对隐私要求极高，使用本地模型是最安全的方案——你的日记内容完全不会离开本地设备。

**安装方式：**
```bash
# 以 Ollama 为例，将 SKILL.md 作为 system prompt
ollama run llama3 --system "$(cat memory-system/SKILL.md)"
```

**推荐本地模型：**
- Llama 3.1 70B（综合能力强）
- Qwen 2.5 72B（中文理解优秀）
- Mixtral 8x7B（推理能力好）

**注意**：本地模型能力弱于顶尖云端模型，复杂推演可能准确度下降。

---

## 通用安全建议（所有工具适用）

```bash
# 1. 对 /memory/ 目录设置权限限制
chmod 700 ~/memory/

# 2. 将 /memory/ 加入 .gitignore
echo "/memory/" >> .gitignore
echo "memory/" >> .gitignore

# 3. 定期备份（本地加密备份）
tar -czf memory-backup-$(date +%Y%m%d).tar.gz ~/memory/
# 建议存储到加密的外部硬盘或加密云存储

# 4. 如使用 macOS，可创建加密磁盘镜像
hdiutil create -size 1g -encryption AES-256 -fs HFS+ -volname Memory ~/memory-encrypted.dmg
```
