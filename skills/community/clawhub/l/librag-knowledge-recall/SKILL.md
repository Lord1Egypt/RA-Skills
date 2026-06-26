---
name: librag-knowledge-recall-zh
description: 使用 LibRAG 本地 `/api/v1/librag/knowbase/recall` 接口做知识库数据召回。适用于中文场景下的知识库检索、资料召回、证据段落提取、出处定位、基于知识库的问答取证，以及用户用“知识库查询”“数据召回”“从文档里找答案”等表达发起的任务。
homepage: https://github.com/openclaw/skills
metadata:
  openclaw:
    emoji: "🔎"
    requires:
      files:
        - config.json
        - scripts/recall.py
      anyBins:
        - python
        - py
        - python3
  clawdbot:
    emoji: "🔎"
    requires:
      files:
        - config.json
        - scripts/recall.py
      anyBins:
        - python
        - py
        - python3
---

# LibRAG 中文知识库召回

优先使用附带脚本调用 LibRAG，不要手写 HTTP 请求。

## 触发语义

遇到下列表达时优先使用本 Skill：
- “去知识库里查一下”
- “做一下数据召回”
- “从 LibRAG 找相关段落”
- “把出处和原文召回出来”
- “根据知识库检索证据”
- “从文档中找到答案”

## 输入

必需输入：
- `question`：用户要检索的问题或条件。

配置文件 `config.json`：
- `base_url`：LibRAG 服务地址。
- `api_key`：与目标知识库绑定的 API Key。
- `kb_id`：默认知识库 ID。
- `recall_mode`：默认召回模式。
- `vector_top_k`：向量召回 top-k。
- `fulltext_top_k`：全文召回 top-k。
- `return_tree`：是否返回树形结构。
- `has_source_text`：是否包含原文。
- `has_score`：是否保留分数字段。
- `filter_effective`：是否过滤无效结果。
- `reasoning_enhance`：是否启用推理增强。
- `score_threshold`：打分过滤阈值。

可选覆盖：命令行参数优先于 `config.json`：
- `kb_id`：覆盖 `config.json` 里的默认知识库 ID。
- `recall_mode`：`reasoning`、`hybrid`、`vector`，默认 `hybrid`。
- `vector_top_k`：默认 `20`。
- `fulltext_top_k`：默认 `20`。
- `return_tree`：默认 `true`。
- `has_source_text`：默认 `true`。
- `has_score`：默认 `true`。
- `score_threshold`：默认 `0`，作为打分过滤的分数阈值。
- `filter_effective`：默认 `true`。
- `reasoning_enhance`：默认 `true`。

## 执行

默认使用 `config.json` 中的知识库：

```bash
python {baseDir}/scripts/recall.py --config {baseDir}/config.json --question "<问题>"
```

需要覆盖知识库时：

```bash
python {baseDir}/scripts/recall.py --config {baseDir}/config.json --kb-id 12 --question "这个产品的违约金标准是什么？"
```

## 输出

默认直接返回脚本输出 JSON。

关键字段：
- `request`
- `response.msg`
- `response.data`
- `summary.item_count`
- `summary.result_shape`

## 约束

- 缺少 `config.json`，或其中的 `base_url`、`api_key`、`kb_id`，或缺少 `question` 时直接失败。
- 默认使用非流式调用。
- 默认使用 `return_tree=true`，只有明确要求平铺段落结果时才改成 `false`。
- 不要输出完整 API Key。
- 若返回 `401` 或 `403`，明确提示密钥无效或没有该知识库权限。
- 若返回 `404`，明确提示知识库不存在。

