---
name: openclaw-update-researcher
description: 专门用于调研 OpenClaw 最新更新的 Skill。该 Skill 能够自动抓取 GitHub 上的 Release 和 Tag 信息，筛选出指定日期（通常是当前日期的前一天）的更新内容，并生成结构化的 Markdown 报告。特别关注记忆（Memory）相关的更新。适用场景：(1) 自动化生成 OpenClaw 技术更新日报，(2) 追踪 OpenClaw 的最新功能和修复，(3) 重点调研记忆系统的演进。
---

# OpenClaw Update Researcher

这是一个自动化调研 OpenClaw 更新的流程，主要关注 GitHub 上的最新发布。

若前一天没有更新，则直接结束调研。

## 核心流程

1.  **确定调研日期**：默认调研当前日期（Asia/Shanghai）的前一天。
2.  **抓取更新信息**：
    *   访问 `https://github.com/openclaw/openclaw/tags` 获取最新的版本号和日期。
3.  **判断与筛选**：
    *   检查是否有在前一天发布的新版本（Stable 或 Beta）。
    *   **如果没有新版本发布**：直接结束流程，不生成报告。
    *   **如果有新版本发布**：提取该版本的所有更新内容。
4.  **重点调研内容**：
    *   描述重大功能更新、Breaking Changes 和重要的 Fixes。
    *   **记忆（Memory）专项**：重点搜索并描述涉及 `memory`, `embeddings`, `lancedb`, `sqlite` 等记忆系统相关的更新。
5.  **生成报告**：
    *   格式：Markdown (MD)。
    *   路径：`report_v1/YYYY-MM-DD/openclaw [版本号] 更新报告.md`（YYYY-MM-DD 为报告生成日期）。
    *   在报告最后附上对应的 GitHub Release 链接。

## 报告模板与结构

报告结构应根据具体的版本更新内容**灵活处理**，不强制固定所有章节，但必须遵守以下硬性要求：

1.  **版本标题**：标题必须包含具体的版本号。
2.  **基本元数据**：在报告开头注明调研日期、更新周期和版本状态。
3.  **🧠 记忆 (Memory) 专项（强制性）**：如果该版本中包含任何与记忆、向量数据库（LanceDB/SQLite）、嵌入（Embeddings）或上下文管理相关的更新，**必须**设立独立章节进行详细描述和技术分析。
4.  **其他更新（灵活性）**：除记忆外，可根据更新的重要性灵活组合章节（如：核心功能、Breaking Changes、重要修复、UI/UX 改进等）。
5.  **更新链接（强制性）**：在报告最后附上该版本在 GitHub 上的 Release 原始链接。

## 报告文件规范
*   **路径**：`report_v1/YYYY-MM-DD/openclaw [版本号] 更新报告.md`（YYYY-MM-DD 为调研的目标更新日期）。

## 注意事项

*   优先使用 `browser` 获取 GitHub 页面内容。
*   如果 GitHub 页面因为反爬虫或其他原因无法读取，尝试多次或更换工具。
*   始终保持专业、技术性的描述口吻。
