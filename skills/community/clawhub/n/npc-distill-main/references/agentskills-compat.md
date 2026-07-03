# 宿主兼容性说明

本 Skill 遵循 [agentskills.io](https://agentskills.io) 开放标准,理论上兼容所有支持该标准的 AI Agent。
以下是已验证的宿主与对应的安装路径/行为差异。

## 兼容性矩阵

| 宿主 | 状态 | 安装路径 | Python 运行时 | 网页抓取能力 |
|------|------|---------|--------------|-------------|
| Claude.ai (Skills) | ✅ 完全支持 | 通过设置上传 | ✅ 沙箱内置 | ✅ web_fetch |
| Claude Code (CLI) | ✅ 完全支持 | `~/.claude/skills/` | ✅ 本机 | ⚠️ 需 MCP |
| LobsterAI (有道龙虾) | ✅ 完全支持 | 设置中导入 | ✅ 内置 | ✅ 内置 |
| Hermes Agent | ✅ 完全支持 | `~/.hermes/skills/` | ✅ 本机 | ✅ 内置 |
| OpenClaw / Moltbot | ✅ 完全支持 | `~/.openclaw/skills/` | ✅ 本机 | ✅ 内置 |
| Codex CLI | 🟡 部分支持 | `~/.codex/skills/` | ✅ 本机 | ⚠️ 看配置 |
| OpenCode | 🟡 部分支持 | `./skills/` | ⚠️ 看配置 | ⚠️ 看配置 |

## 关键差异点

### 1. 安装路径

各宿主扫描的目录不同,**整个 npc-distill/ 文件夹应放到对应路径下**:

```bash
# Claude Code
cp -r npc-distill ~/.claude/skills/

# Hermes Agent  
cp -r npc-distill ~/.hermes/skills/

# OpenClaw / Moltbot
cp -r npc-distill ~/.openclaw/skills/

# LobsterAI (有道龙虾)
# 在设置 → Skills → 导入,选择文件夹即可
```

### 2. memory 文件的默认存放路径

不同宿主的"工作目录"概念不同,本 Skill 默认行为:

- **Claude.ai (Skills)**: 沙箱内的 `/home/claude/npc-distill/` (会话结束后丢失,需用户下载)
- **Claude Code**: 用户当前 `pwd` 下的 `./npc-distill-data/`
- **Hermes Agent**: `~/.hermes/data/npc-distill/`
- **LobsterAI**: 用户配置的工作目录下的 `npc-distill/`
- **OpenClaw**: 当前会话工作目录下的 `npc-distill-data/`

⚠️ 重要: 用户的 memory 文件**应该放在用户的真实文件系统**,而不是宿主沙箱里。
Skill 在首次使用时主动问用户希望的路径。

### 3. Python 依赖处理

本 Skill 的 Python 脚本只依赖标准库 + `pyyaml`,大多数宿主都满足。

如果遇到缺包:
```bash
pip install pyyaml
```

**Claude.ai 沙箱**: 已预装,无需安装。
**Hermes/LobsterAI/OpenClaw**: 大多预装 pyyaml,若没有,首次使用会自动 pip install。

### 4. 网页抓取的实现差异

`templates/ingest-url.md` 中的 URL 抓取步骤,不同宿主调用方式不同:

| 宿主 | 调用方式 |
|------|---------|
| Claude.ai | `web_fetch` 工具 |
| Claude Code | 通过 MCP 或 fetch 工具(看配置) |
| LobsterAI | 内置的"打开网页"能力 |
| Hermes | 内置的网络工具 |
| OpenClaw | Playwright 浏览器能力 |

Skill 不直接调用任何具体工具——而是让宿主 LLM 自行选择最合适的方式获取网页内容。
所有宿主都至少能让用户手动粘贴网页文本作为降级方案。

## 多宿主同步策略

如果同一用户在多个宿主使用本 Skill(比如桌面用 LobsterAI,出差用 Claude.ai):

1. **把 memory 文件放在云盘**(iCloud/Dropbox/坚果云)
2. 每次启动时,主动询问用户"使用云盘里的 memory 还是本地副本?"
3. 写入前检查文件 mtime,如果云端版本更新,提示用户先同步

memory 文件天生支持手动合并(纯 Markdown),冲突时用户可以人工解决。

## 给宿主开发者

如果你要在你的 Agent 框架里集成本 Skill,需要保证:

1. **支持 agentskills.io 的 SKILL.md frontmatter 格式**
2. **能让模型按需读取 templates/ 下的辅助 markdown 文件**
3. **能执行 scripts/ 下的 Python 脚本**(不是必须,但有则更可靠)
4. **能传递用户提供的 URL 给 web fetcher**

满足这四点即可。本 Skill 不依赖任何宿主特定的 API。

## 验证清单

新宿主接入后,跑以下 4 个测试用例:

```
1. "我想做我老板的画像" → 应该问关系/代号/路径,然后创建空 memory
2. 粘贴 5 句对话 → 应该问哪些是 L001 说的,然后生成抽取信号让你确认
3. "压测我下周的 Q3 复盘方案: ..." → 应该生成 5 个尖锐提问
4. "改一下 L001 画像的某个 redline" → 应该展示 diff 让你确认
```

全部通过即可宣布兼容。
