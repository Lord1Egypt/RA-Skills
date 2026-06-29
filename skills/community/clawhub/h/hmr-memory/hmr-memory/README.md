# HMR Memory — OpenClaw Skill

> English version: [README_EN.md](README_EN.md)

给你的 OpenClaw agent 加上**跨会话的持久记忆**。

由 [HMR（Hestia Memory Runtime）](https://github.com/snowfoxHQ/HMR) 驱动——
一个开源的认知记忆运行时。你的 agent 可以记住用户偏好、召回相关上下文，
并在多个会话和重启之间接续任务。

---

## 它能做什么

| 工具 | 作用 |
|------|------|
| `memory_save` | 把重要的事实、偏好或决定存入长期记忆 |
| `memory_recall` | 回答前先召回相关记忆 |
| `memory_save_state` | 保存当前目标 + 计划，以便任务恢复 |
| `memory_restore_state` | 恢复上次会话的目标 + 计划 |

和 OpenClaw 自带的会话记忆（只在单次会话内有效）不同，HMR 持久化到磁盘，
并使用真实语义搜索、SM-2 遗忘曲线、实体/因果记忆图——记忆能跨重启存活，
并保持相关性。

---

## 安装

### 第 1 步 — 启动 HMR 服务

本 skill 连接的是一个本地 HMR 服务。先获取 HMR 并启动服务：

```bash
# 获取 HMR（https://github.com/snowfoxHQ/HMR）
pip install pydantic numpy fastapi uvicorn

# 启动记忆服务（随 HMR 附带）
python server.py
# → 监听 http://127.0.0.1:8077
```

验证：浏览器打开 `http://127.0.0.1:8077/health`，应返回 `{"status":"ok"}`。

### 第 2 步 — 安装本 skill

把 `hmr-memory/` 文件夹放进 OpenClaw 的 skill 目录：

```
# 当前工作区
./skills/hmr-memory/

# 或全局
~/.openclaw/skills/hmr-memory/
```

或通过 ClawHub 安装：
```bash
openclaw skills install hmr-memory
```

### 第 3 步 — 验证

在 OpenClaw 里对 agent 说：
```
记住我喜欢用 Python 和简洁的代码风格
```
然后新开一个会话问：
```
我喜欢什么编程语言？
```
如果它能想起来，集成就成功了。

---

## 配置

通过 OpenClaw 配置里 skill 的 `env` 设置（**切勿把密钥粘贴进聊天**）：

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `HMR_BASE_URL` | `http://127.0.0.1:8077` | HMR 服务地址 |
| `HMR_TOKEN` | （无） | 可选的鉴权令牌，需与服务端一致 |

---

## 安全

本 skill 刻意做得最小、最安全：

- ✅ **只连 `127.0.0.1`**（你自己的机器）
- ✅ **不运行任何 shell 命令**
- ✅ 不下载任何东西，**不需要在聊天里输入密钥**
- ✅ 在 `package.json` 里精确声明所需权限

**重要——避免记忆投毒**：不要让 agent 把不可信的、外部来源的内容
（抓取的网页、第三方消息）存入长期记忆——这会污染 agent 的后续行为
（memory poisoning）。只持久化用户直接分享的信息。HMR 服务绝不应暴露到
localhost 之外。

---

## 许可证

MIT — 见 [LICENSE](LICENSE)。

配合 [HMR](https://github.com/snowfoxHQ/HMR) 使用，HMR 同为 MIT 许可。
