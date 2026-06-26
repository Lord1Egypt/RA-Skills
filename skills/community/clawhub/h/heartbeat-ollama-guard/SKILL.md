# heartbeat-ollama-guard

将 OpenClaw 心跳切换为**本地 Ollama 模型**，并部署**配置守卫**防止被静默修改，从而避免心跳请求消耗付费云端 token。

---

## 背景

OpenClaw 的心跳机制每 30 分钟调用一次 LLM，默认走云端模型（kimi / claude 等）。
在 token 限额有限的情况下，这会白白消耗配额，甚至耗尽每周限额。

本技能：
1. 将所有 OpenClaw 实例的 `agents.defaults.heartbeat.model` 改为 `local/<model>`
2. 部署一个 60s 轮询守卫，检测到未授权修改立即回滚并发出系统通知

---

## 快速开始

```bash
cd ~/.openclaw/workspace/skills/heartbeat-ollama-guard

# 一键安装（需要先安装 Ollama）
python3 heartbeat_ollama_guard.py --setup

# 指定其他模型
python3 heartbeat_ollama_guard.py --setup --model llama3:8b

# 查看状态
python3 heartbeat_ollama_guard.py --status
```

---

## 安装 Ollama

**macOS：**
```bash
brew install ollama
# 或访问 https://ollama.com 下载 App
```

**Linux：**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

---

## CLI 命令

| 命令 | 说明 |
|------|------|
| `--setup` | 完整安装向导（自动检测、拉取模型、配置、部署守卫） |
| `--status` | 显示 Ollama、模型、守卫进程、所有实例的当前状态 |
| `--check` | 执行一次守卫检查（不循环）|
| `--uninstall` | 卸载守卫（LaunchAgent/systemd + 守卫脚本 + conf） |
| `--model <id>` | 指定本地模型 ID（默认 `qwen3.5:4b-q4_K_M`） |

---

## 安装向导步骤

```
Step 1  检测 Ollama 是否已安装（未安装则打印安装指引并退出）
Step 2  检测目标模型，未拉取则自动 ollama pull
Step 3  发现所有 openclaw.json 实例，确认需要配置哪些
Step 4  写入 heartbeat.model（自动备份原文件）
Step 5  生成守卫脚本、conf.json，部署 LaunchAgent（macOS）或 systemd（Linux）
Step 6  验证守卫进程 + 单次检查
Step 7  提示重启 gateway
```

---

## 授权修改 heartbeat.model

守卫会阻止任何未经授权的 heartbeat.model 修改。合法修改流程：

1. **先**更新 `~/.openclaw/workspace/.lib/heartbeat-guard.conf.json` 中对应实例的 `expected` 值
2. **再**修改 `openclaw.json`

守卫检测到 conf 与 openclaw.json 一致时自动放行，无需关闭守卫。

---

## 安全声明

| 操作 | 范围 |
|------|------|
| 读取 openclaw.json | 仅检测 `heartbeat.model` 现状 |
| 写入 openclaw.json | 仅 `heartbeat.model` + `models.providers.local` 字段 |
| 守卫守护进程 | 纯本地，60s 轮询，**无网络请求** |
| macOS 系统通知 | 仅守卫检测到未授权改动时触发 |
| 不需要 sudo | ✅ |
| 不读取对话内容 | ✅ |
| 不访问外部 API | ✅ |

---

## 备份与恢复

安装向导在修改 `openclaw.json` 前自动备份到：
```
~/.openclaw/workspace/.lib/.hog_backups/
```

如需手动恢复：
```bash
cp ~/.openclaw/workspace/.lib/.hog_backups/<backup>.json ~/.openclaw/openclaw.json
```

---

## 验证

1. 运行 `--status` → 所有项 ✅
2. 手动篡改 `openclaw.json` 的 `heartbeat.model` → 60 秒内自动回滚 + 系统通知
3. 查看日志 `~/.openclaw/workspace/.lib/heartbeat-guard.log` → 有 `[ALERT]` + `[REVERT]` 条目
4. 授权修改：先改 conf.json expected 值 → 再改 openclaw.json → 守卫放行

---

## 文件位置

| 文件 | 说明 |
|------|------|
| `~/.openclaw/workspace/.lib/heartbeat-guard.py` | 守卫守护进程脚本 |
| `~/.openclaw/workspace/.lib/heartbeat-guard.conf.json` | 守卫授权配置 |
| `~/.openclaw/workspace/.lib/heartbeat-guard.log` | 守卫运行日志 |
| `~/Library/LaunchAgents/com.openclaw.heartbeat-guard.plist` | macOS LaunchAgent |
| `~/.config/systemd/user/openclaw-heartbeat-guard.service` | Linux systemd |
| `~/.openclaw/workspace/.lib/.hog_backups/` | openclaw.json 备份 |
