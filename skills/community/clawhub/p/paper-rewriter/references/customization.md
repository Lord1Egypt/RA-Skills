> **何时读我**：要调词表、固化误报守卫、或改评分标定之前。
> **最短路径**：误报固化用 learn_guards.py（不要手改 patterns_*.json）；词表与标定文件位置在下表。
> **回 [INDEX](INDEX.md)**

## 自定义

- `scripts/patterns_zh.json` / `patterns_en.json`：词表（含改写建议）、正则信号、
  术语保护（正当学术用法不误报，如 mutational landscape、pivotal trial、
  序列对齐、沉淀反应）、自动修复清单。
- **用户自学守卫**存放在 `scripts/user_guards.json`（由 `learn_guards.py`
  管理，不要手改；`list` 查看、`remove` 删除）。误报词固化请写这里而不是改
  `patterns_*.json`——词表文件升级会被覆盖，守卫文件不会。
- 评分标定系数在 `scripts/hxt_core.py`（`_LANG_K`）；开发仓库 `tests/` 四语料
  （发布包不含）记录了预期分离度。

## 外挂词表（--lexicon，v5.11.0）

detect / transform / pipeline 接受 `--lexicon 文件`：与内置词表**同名键逐项追加**
（`vocabulary` / `ai_freq_vocab` / `term_guards` / `auto_fixes` / `aggressive_fixes`），
默认权重 1.0、词族 custom；文件不可读时响亮报错。用途：

- 团队/学科自定义词族不进发布包（升级不丢）；
- **多 skill 共享同一外部词表文件（单一来源）**——paper-rewriter 与 paper-polisher
  约定同一 JSON schema 后，两边 `--lexicon 同一路径` 即共享，无需同步包内副本；
- term_guards 条目字段为 `term` / `allow_before` / `allow_after`（与内置守卫同构）。

最小示例：

```json
{"vocabulary": [{"w": "示例黑话", "alt": "改成的话", "weight": 1.0}],
 "term_guards": [{"term": "示例术语", "allow_before": ["正当搭配"], "allow_after": []}]}
```

注意：外挂词表与用户守卫（learn_guards.py）独立叠加；同名 term 的守卫先到先得。
