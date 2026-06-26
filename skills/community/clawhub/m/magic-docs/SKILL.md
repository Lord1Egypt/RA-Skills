---
name: magic-docs
description: "自动更新的活文档。在 Markdown 文件开头加 `<!-- MAGIC DOC -->` 标记，Agent 会在每轮对话后自动检测是否需要更新该文档，并写入新发现的信息。灵感来自 Claude Code 的 Magic Docs 机制。触发词：magic doc、活文档、自动更新文档、auto doc。"
---

# Magic Docs — 自动更新的活文档

灵感来源：Claude Code 的 `# MAGIC DOC:` 机制。

## 核心问题

文档写完就开始过时。项目变了、API 改了、决策变了——但没人更新文档。
Agent 做了大量操作，学到了很多信息，但这些信息散落在对话里，不会自动沉淀到文档。

## 什么时候用

### 主动触发
- 用户说"创建活文档"、"magic doc"、"帮我维护这个文档"
- 用户指定一个 md 文件要求"保持更新"

### 自动触发（每轮对话结束时）
- 扫描 workspace 中的 Magic Doc 文件
- 判断本轮对话是否包含与该文档相关的新信息
- 如果有 → 自动更新

## Magic Doc 标记格式

在任何 Markdown 文件的**前 5 行内**加入标记：

```markdown
<!-- MAGIC DOC -->
# 项目架构笔记

记录项目的关键架构决策和技术选型。
```

### 可选参数

```markdown
<!-- MAGIC DOC scope="飞书API,权限配置" -->
<!-- MAGIC DOC scope="设备信息,网络配置" update="daily" -->
```

- `scope`：限定关注范围（逗号分隔的关键词），只在对话涉及这些主题时更新
- `update`：更新频率。`realtime`（每轮，默认）、`daily`（每天一次）、`manual`（只在主动要求时更新）

## 执行流程

### Phase 1 — 发现 Magic Docs

```bash
# 扫描 workspace 中的 Magic Doc 文件
grep -rl "<!-- MAGIC DOC" . --include="*.md" | head -20
```

建立索引：文件路径、scope、update 频率、最后更新时间。

### Phase 2 — 相关性判断

对每个 Magic Doc，判断**本轮对话**是否包含相关的新信息：

1. 读取文档的 scope 和现有内容摘要（前 50 行）
2. 对比本轮对话的主题
3. 判断：是否有**文档中还没有的新事实**？

判断标准（严格）：
- ✅ 新发现的技术事实（IP 变了、版本升级了、API 改了）
- ✅ 新的决策或约束（"我们决定用 X 不用 Y"）
- ✅ 新的问题和解决方案
- ❌ 对话中只是**使用**了文档中已有的信息（不算新）
- ❌ 临时的调试过程（不值得记录）

如果判断为"不相关" → 跳过，不更新。

### Phase 3 — 智能更新

读取文档完整内容，然后：

1. **追加新信息**：在合适的章节下追加，保持文档结构
2. **修正过时信息**：如果对话中发现文档内容已过时，直接修正
3. **不重写整个文档**：只改需要改的部分，用 `edit` 工具精确修改
4. **加时间戳**：每次更新在修改处加日期标注

```markdown
## 设备信息

- NAS IP: 192.168.5.27 <!-- updated 2026-04-02 -->
- SSH 密码: 旧密码已失效，新密码见 TOOLS.md <!-- updated 2026-04-02 -->
```

### Phase 4 — 更新日志

在文档末尾维护一个更新日志：

```markdown
---
## Changelog
- 2026-04-02: 更新 NAS SSH 密码，新增 IMA API 配置
- 2026-04-01: 新增 ESP32 方糖设备信息
```

## 创建新的 Magic Doc

当用户要求创建活文档时：

```markdown
<!-- MAGIC DOC scope="关键词1,关键词2" -->
# [文档标题]

[用户指定的初始内容，或从对话中提取的信息]

---
## Changelog
- YYYY-MM-DD: 初始创建
```

## 安全规则

1. **绝不删除用户手写的内容** — 只追加和修正
2. **不写入密钥/密码** — 如果对话中涉及敏感信息，写"见 TOOLS.md"或"见配置文件"
3. **不写入临时调试信息** — 只写确定的、长期有效的事实
4. **保持文档可读性** — 更新后文档应该比更新前更好，不是更乱
5. **冲突时保留两个版本** — 如果不确定哪个是对的，都保留并标注

## 与其他 Skill 的协作

- **Dream**：Dream 整理记忆，Magic Docs 整理文档。互补不冲突。
- **Context Doctor**：Context Doctor 可以检查 Magic Doc 的大小是否影响 context。
- **Session Resume**：Session Resume 恢复任务状态，Magic Doc 保持文档最新。

## 使用示例

```
用户：帮我创建一个活文档，记录所有设备的网络配置
Agent：
1. 创建 devices-network.md
2. 加 <!-- MAGIC DOC scope="IP,SSH,网络,设备" -->
3. 从 MEMORY.md 和 TOOLS.md 中提取现有设备信息写入
4. 此后每次对话涉及设备变更时自动更新
```

```
用户：（正常对话中）NAS 的 IP 换成 192.168.5.30 了
Agent：
1. 正常处理用户请求
2. 对话结束时，发现 devices-network.md 是 Magic Doc 且 scope 匹配
3. 自动更新文档中的 NAS IP
```
