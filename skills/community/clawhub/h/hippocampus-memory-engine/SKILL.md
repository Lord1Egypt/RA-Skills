---
name: hippocampus-memory-engine
description: "以海马体神经环路为隐喻的 Agent 外部记忆引擎。当用户要求搭建/维护海马体知识库、把分散记忆统一向量化检索、生成可视化知识库、或同步到 GitHub/Obsidian 时调用。"
agent_created: true
---

# 海马体记忆流引擎 (Hippocampus Memory Engine)

## 概览

把 LLM 当作"大脑皮层"、把外部存储当作"海马体"。本 skill 提供一套**离线、零模型下载**的 Python 引擎，把分散在各处的记忆（会话日志、账号级 `MEMORY.md`、知识库 `knowledge.json`、归档 README、TRAE 记忆工作流）统一向量化、持久化，并支持 RAG 检索、自动蒸馏、SVG 可视化、Obsidian 同步与 GitHub 站点发布。

## 何时调用

- 用户要求搭建/维护 Agent 的"外部记忆""海马体记忆""记忆中枢"。
- 用户有多个记忆源需要统一检索或可视化。
- 用户要求把知识库更新到 GitHub、发布为 Skill、同步到 Obsidian。
- 用户要求新建任务/新建对话/每日更新自动汇入海马体。
- 每个会话/任务结束前，用户说"把这次内容更新到海马体""巩固记忆""incremental sync"。

## 本地路径

- 引擎本体：`D:\\D盘workbuddy办公\\记忆流存储\\记忆流引擎\\`
- 可视化站点：`D:\\D盘workbuddy办公\\记忆流存储\\海马体知识库\\index.html`
- 结构化数据：`D:\\D盘workbuddy办公\\记忆流存储\\海马体知识库\\knowledge.json`
- Obsidian Vault：`C:/Users/Administrator/Documents/Obsidian Vault/海马体记忆流`
- GitHub 仓库：`https://github.com/wzx11223344/hippocampus-memory-engine`

## 核心用法

1. **完整同步（推荐每日一次）**
   ```powershell
   cd 'D:\\D盘workbuddy办公\\记忆流存储\\记忆流引擎'
   python sync.py all
   ```
   `all` = 清空 L3/L2 → seed → distill → rebuild index.html/flow.html → 导出 Obsidian。

2. **增量同步（新建任务/对话结束时）**
   ```powershell
   python sync.py incremental --text "本次会话核心结论：..."
   ```
   不重置引擎，只追加本轮内容，自动刷新可视化、flow 图谱与 Obsidian。

3. **单条记忆写入**
   ```powershell
   python sync.py ingest --text "关键事实/约束/决策" --type semantic --importance 0.8
   ```

4. **只更新可视化**
   ```powershell
   python sync.py rebuild
   ```

5. **只导出 Obsidian**
   ```powershell
   python sync.py obsidian
   ```

6. **检索记忆**
   ```python
   from engine import HippocampusEngine
   eng = HippocampusEngine("config.json")
   hits = eng.retrieve("链主申报书 附件3", top_k=3, threshold=0.05)
   ```

## 自动迭代

- **每日汇总**：已配置每日 23:00 自动任务运行 `sync.py all`，把当天新任务、新对话、日志与 TRAE 记忆汇流进海马体。任务 ID 见 `Schedule` 列表。
- **会话级增量**：在每个会话/任务结束时，调用 `python sync.py incremental --text "..."` 把当轮关键内容实时写入海马体；AI 会在后续任务中通过检索或读取 `knowledge.json` 复用这些记忆。
- **自我更迭**：高价值记忆经 `distill` 自动进入 `knowledge.json` 的 `auto` 区，成为长期语义记忆；可视化与 Obsidian 随每次同步自动重建。

## 注意事项

- 唯一依赖：`numpy`。
- 中文稀疏 TF-IDF 下 `threshold` 可调低到 0.03–0.05 提升召回。
- 写入知识库 `knowledge.json` 后必须重新运行 `sync.py all` 才能更新可视化与 Obsidian。
