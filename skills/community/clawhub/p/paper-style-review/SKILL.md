---
name: paper-style-review
description: 结构化审校中文论文：从参考论文学习风格，统一结构图谱，执行格式/术语/逻辑/风格融合审查，并将结果回写为 Word 批注。
---

# paper-style-review

用这个 skill 处理中文论文的“风格学习 + 结构化审校 + Word 批注回挂”任务。

## 保持的公开版边界

- 只保留可公开发布的脚本、schema、派生规则和运行说明。
- 不保留真实论文、命名样例、历史输出、原始 `.doc` 附件或本地工作区绝对路径。
- 风格学习依赖用户自行提供的 `refs`，仓库不内置参考论文。

## 当前主链

```text
scripts/run_review.py
  -> orchestrators/review_orchestrator.run_review()
  -> style-profile handoff or build
  -> format checker
  -> target style units
  -> fused review runtime
  -> annotation assembly
  -> inject Word comments
```

## 能力范围

1. refs 风格学习
   - 为每篇 ref 建立统一结构图谱
   - 按 `paragraphType` 聚类
   - 生成 `style-profile.json` 与 `ref-style-basis.md`

2. target 审查
   - 建立 target 结构图谱
   - 运行格式检查
   - 运行 fused LLM 审查：术语 / 逻辑 / 风格偏离

3. Word 批注回挂
   - 汇总为 `annotations.json`
   - 生成 `<target>-annotated.docx`

## 关键边界

- target 风格判断只消费 `style-profile.json`，不在 target 阶段回读 refs 原文。
- 风格学习、target 审查、批注定位共用统一结构图谱。
- 所有正式输出都走统一锚点与注入链路。
- `chapterScope` 只收窄 target-side LLM 审查；格式检查仍是文档级。

## 运行方式

完整主链：

```bash
python3 scripts/run_review.py --config ./references/review-config.example.json
```

独立阶段：

```bash
python3 scripts/run_review.py --config ./references/review-config.example.json --stage style_profile
python3 scripts/run_review.py --config ./references/review-config.example.json --stage style_annotation
python3 scripts/run_review.py --config ./references/review-config.example.json --stage annotation
```

限制章节范围：

```bash
python3 scripts/run_review.py --config ./references/review-config.example.json --chapters abstract,1
```

## 最小配置

```json
{
  "target": {
    "path": "./inputs/target.docx"
  },
  "refs": [
    {
      "id": "ref-style-01",
      "path": "./inputs/ref-style-01.docx",
      "enabled": true,
      "styleProfileEnabled": true
    }
  ],
  "outputDir": "./outputs"
}
```

## 重要文件

- `scripts/job_defaults.py` / `scripts/runtime_config.py`：配置归一化
- `scripts/paper_structure_anchor.py`：统一结构图谱
- `scripts/profilers/ref_style_profiler.py`：refs 风格学习
- `scripts/fused_review_runtime.py`：target-side fused 审查
- `scripts/annotation_anchor_infra.py` / `scripts/annotation_assembler.py` / `scripts/inject_word_comments.py`：批注链路
- `references/format-rules.json` / `references/format-rule-matrix.md`：公开可分发的派生格式规则
- `references/style-profile-extractor.md`：风格画像提取约束

## 使用时要做的事

1. 准备自己的 `target` 与 `refs`。
2. 按配置文件指定 `outputDir`、检查项和可选 `chapterScope`。
3. 若已存在稳定 `style-profile.json`，可直接通过 `styleProfilePath` 复用。
4. 调试结构或定位问题时，优先检查 `target-structure-map.json`、`target-style-units.json`、`annotations.json`。

## 不要做的事

- 不要假设仓库内自带任何真实论文样本。
- 不要把 target 阶段改成直接回读 refs 原文。
- 不要在公开版里加入历史输出、用户文档、原始附件或本地路径。
