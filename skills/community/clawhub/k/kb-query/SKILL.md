---
name: kb_query
description: Answer simple lookup and factual Q&A questions from Java-specified personal/team Research KB repositories with source grounding and structured citations for the desktop source list. Use for ordinary knowledge-base retrieval; do not use for GitHub/open-source project usefulness evaluation or cross-document literature/special-topic reviews.
---

# Skill: kb_query

## 职责边界

`kb_query` 只负责在 Java 后端指定的 Research KB 仓库中检索资料、读取相关 Markdown 页面，并基于这些已读页面回答问题。它不负责身份识别、权限判断、知识库范围选择、会话存储、查询历史写入或 Gitea 日志记录。

如果用户问题是在评估开源/GitHub 项目是否有用、是否值得复现、环境风险如何，交给对应的开源项目评估 skill。
如果用户问题是在写专项综述、跨多篇资料做方法对比、研究缺口分析或主题综合，交给对应的专项综述 skill。

只能访问 `kbTargets[]` 中列出的仓库。不要读取或推断任何未列出的仓库。

## 可接受任务

只接受满足以下条件的 JSON：

- `protocol = research_kb_agent_task`
- `taskType = kb_query`
- `kbTargets[]` 中有一个或两个目标
- `payload.question` 非空

## 查询流程

每次回答必须按以下顺序执行：

1. 校验任务协议和输入字段。
2. 读取每个目标仓库的 `catalog.json` 和 `index.md`。
3. 从 catalog、index 和仓库 Markdown 树中收集候选页面。
4. 基于问题进行中文/英文 token 化检索，对标题、路径、标题层级和正文分别评分。
5. 只读取和使用评分相关的 Markdown 页面。
6. 回答中的知识库事实必须只来自本次已读页面，不能用常识、模型记忆或外部网页补全知识库事实。
7. 如果问题是“你是谁”“介绍一下自己”“你能做什么”等身份类问题，优先读取 `README.md`、`AGENTS.md`、`index.md` 等系统页面。
8. `citations[]` 只能引用本次已读页面，路径必须是仓库相对路径，供桌面端渲染为来源清单并点击打开。
9. 不要在回答正文末尾生成 Markdown 链接、脚注或“[来源](path)”列表；来源只放入 `citations[]`。
10. 不要向 Gitea 写入查询日志；查询历史由 Java 后端保存。

## 证据不足规则

如果知识库中没有足够资料回答问题，答案必须先说明：

`知识库中没有足够资料回答这个问题。`

此时可以继续给出一般性说明，但必须用“以下是非知识库结论的一般性说明”这样的文字明确标记。`citations` 必须返回空数组。不要把一般性说明伪装成知识库事实。

## 引用规则

每条 citation 必须包含：

- `kbType`
- `repoFullName`
- `path`
- `title`
- `snippet`
- `anchor`

`snippet` 应该是支撑答案的短证据片段。不要引用未读取页面，不要引用 `source_files/` 下的原始归档文件。

桌面端会把 `citations[]` 渲染为“来源 1 / 来源 2 / 来源 3”清单。回答正文要专注于结论，不要重复输出来源清单。

## 输出

必须返回一个合法 JSON 对象，不能包 Markdown 代码块：

```json
{
  "protocol": "research_kb_agent_result",
  "protocolVersion": "1.0",
  "taskId": "...",
  "taskType": "kb_query",
  "success": true,
  "result": {
    "answer": "...",
    "citations": [],
    "usedScopes": ["personal", "team"],
    "readPages": []
  },
  "errors": []
}
```

字段名、层级和类型不能改变。

## 辅助入口

稳定入口是：

```bash
python3 scripts/run_task.py --stdin
python3 scripts/run_task.py --task-json <path>
```

脚本会执行候选页收集、证据检索、引用生成和 JSON schema 输出。Agent 如需生成更自然的中文回答，也必须先读取页面；知识库事实必须限制在已读页面证据内，一般性说明必须清楚标注为非知识库结论。
