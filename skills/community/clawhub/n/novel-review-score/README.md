# 小说审稿评分

由当前 AI 阅读实际小说材料并完成六维审稿，结论包含可定位的原文证据、阅读影响、待确认项和可执行修改建议。脚本仅检查 AI 写好的结果结构并生成 Markdown/JSON 排版，不会阅读小说、分析文本或自行评分。

## 使用

提供原文或梗概，并说明本次范围和目标读者。可以直接要求：

> 请阅读我提供的章节，按六维量表审稿。逐项引用可定位的原文证据，说明阅读影响和具体修改动作；证据不足处标待确认，不要虚构评分。注明你评的是本次提供的范围。

AI 应直接给出真实审稿结论。需要保存结构化结果时，由 AI 根据 `examples/success-output.json` 生成完整 JSON，再运行：

```bash
python3 scripts/self_test.py render --input /absolute/path/review.json --output /absolute/path/new-review-dir
```

输出目录若已有 `review.json` 或 `review.md`，脚本会拒绝覆盖。缺少正文/梗概时使用 `needs_more_source`，不评分；任何维度仍待核实时，整体状态为 `needs_review`；无法可靠评分时该项 `score` 和总 `average` 都填 `null`，不要为了算平均数猜分。

## 自测

```bash
python3 scripts/self_test.py self-test
```

自测只验证校验器行为，不代表任何小说已被审过。评分是编辑辅助意见，不承诺签约、收益或平台结果。
