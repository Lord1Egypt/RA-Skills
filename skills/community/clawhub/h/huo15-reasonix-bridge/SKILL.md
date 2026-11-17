---
name: huo15-reasonix-bridge
displayName: Reasonix 项目桥
version: 1.0.0
description: "OpenClaw ↔ Reasonix 桌面版项目/会话同步桥。列出 Reasonix 桌面版所有项目及其会话，续跑/新建项目会话。CLI 与桌面版共享 ~/.reasonix/ 存储，已验证可续跑桌面版会话。"
metadata: { "openclaw": { "emoji": "🔗", "requires": { "bins": ["reasonix"] } } }
aliases:
  - Reasonix桥
  - reasonix项目
  - reasonix会话
  - 龙虾项目
  - 龙虾会话
  - 桌面版项目
  - reasonix project
  - reasonix session
---

# Reasonix 项目桥 · huo15-reasonix-bridge

> OpenClaw 通过 CLI 操控 Reasonix 桌面版的项目树和会话。
> CLI 与桌面版读同一套 `~/.reasonix/` 存储，已验证 `reasonix run --resume` 可续跑桌面版项目会话。

---

## 一、什么时候用

✅ **触发**:
- 用户说"列出 Reasonix 所有项目"/"列出龙虾项目"
- 用户说"查看 XXX 项目的会话"/"XXX 项目有哪些会话"
- 用户说"续跑 XXX 会话"/"继续上次的会话"
- 用户想让 OpenClaw 操控 Reasonix 桌面版的项目/会话
- 用户说"用 Reasonix 做 XXX"但没指定项目

❌ **不触发**:
- 用户只是问 Reasonix 是什么
- 用户想配置 Reasonix（走 `reasonix setup`，非本 skill 范畴）

---

## 二、前置知识

**存储架构**：Reasonix CLI 和桌面版共享同一套存储：
- 项目注册表：`~/.reasonix/desktop-projects.json`（JSON 数组，含 root 路径 + topics 列表）
- 项目会话：`~/.reasonix/projects/<哈希>/sessions/`（每个项目独立目录）
- 全局会话：`~/.reasonix/sessions/`（非项目级会话）
- 桌面版运行时数据：`~/.openclaw/.reasonix/`（任务等）

**关键命令**：
- `reasonix run --resume <会话文件路径>` — 续跑桌面版项目会话（已验证，2026-09-05）
- `reasonix run --dir <项目根目录>` — 在指定项目下新建会话
- `reasonix run --continue` — 续跑最近会话（全局 sessions 目录）

**会话文件命名**：`<timestamp>-session.jsonl` 或 `<timestamp>-<model>.jsonl`

---

## 三、操作流程

### 3.1 列出所有项目

```bash
cat ~/.reasonix/desktop-projects.json | python3 -c "
import json,sys
d=json.load(sys.stdin)
for p in d.get('projects',[]):
    print(f\"{p['root']} ({len(p.get('topics',[]))} 个话题)\")
"
```

输出示例：
```
/Users/jobzhao/.openclaw (7 个话题)
/Users/jobzhao/workspace/projects/openclaw/openclaw-butler (1 个话题)
/Users/jobzhao/workspace/huo15/Juxingyi (5 个话题)
...
```

> 执行此命令展示项目列表，等用户选择要操作的项目。

### 3.2 列出项目会话

用户指定项目后，用 `read` 工具读 `desktop-projects.json`，找到该项目 root 对应的 topics 列表。然后：

```bash
# 列出该项目的会话文件
ls -lt ~/.reasonix/projects/<哈希>/sessions/*.jsonl 2>/dev/null
```

从文件名提取会话 ID（`<timestamp>.jsonl` 或 `<timestamp>-session.jsonl`）。

> 注意：桌面版会话标题可读性有限，文件名中日期时间戳是主要标识。如需标题，可用 `reasonix run --resume <会话文件路径> --max-steps 1` 让模型自我描述（极耗 token，仅用户明确要求时用）。

### 3.3 续跑桌面版会话

用户指定要续跑的项目和会话后：

```bash
reasonix run --resume ~/.reasonix/projects/<哈希>/sessions/<会话文件> --dir <项目根目录> "<用户任务>"
```

**重要参数**：
- `--resume`：必须用**完整文件路径**（不是 session ID，CLI 用 ID 找不到项目级会话）
- `--dir`：指向项目根目录（`/Users/jobzhao/...`），确保 reasonix 的 cwd 正确
- 用户任务直接传给 reasonix（reasonix 会加载历史上下文后执行新任务）

**已验证**（2026-09-05）：marketing_docs 项目 `20260902-180857.725540000-session.jsonl` 成功 resume，模型回忆起标题「柠檬豆 FDE PPT（index）改造与演讲稿同步」，169k input tokens 完整加载。

### 3.4 新建项目会话

在指定项目下新建会话：

```bash
reasonix run --dir <项目根目录> "<任务>"
```

这会自动在 `~/.reasonix/projects/<哈希>/sessions/` 下创建新会话文件。

### 3.5 续跑最近全局会话

```bash
reasonix run --continue "<任务>"
```

扫 `~/.reasonix/sessions/` 下最近会话。

---

## 四、项目根目录 → 哈希目录 映射

Reasonix 使用路径哈希作为项目目录名。映射规则：

项目根目录 `/Users/jobzhao/workspace/projects/openclaw/marketing_docs` → 哈希目录 `-Users-jobzhao-workspace-projects-openclaw-marketing_docs`

即：`/` 替换为 `-`，前缀 `-`。可用以下命令查：

```bash
ls -d ~/.reasonix/projects/*/ | grep -i "<关键词>"
```

或通过 `desktop-projects.json` 的 `root` 字段反查。

---

## 五、注意事项

- **CLI 的 `session list` 默认只扫全局 `~/.reasonix/sessions/`**，不扫 `projects/` 子目录，因此桌面版项目会话不在 CLI 默认列表里。用本 skill 的 `--resume <文件路径>` 方式绕过。
- **resume 会消耗 token**（加载完整历史上下文），建议在用户明确要求续跑时才用。
- **Reasonix 桌面版正在运行时**，同一会话文件可能被锁定。如果 resume 报错，用 `--copy` 参数复制会话继续。
- 如果 Reasonix CLI 不在 PATH 中，用完整路径：`/Applications/Reasonix.app/Contents/MacOS/reasonix`。