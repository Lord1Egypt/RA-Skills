# Prompt 模板说明

源码：[../scripts/prompts.py](../scripts/prompts.py)

## 两档模式

| 模式 | 适用 | 与 normal 的差异 |
|------|------|------------------|
| `normal` | A股/港股标准年报、清晰文字版 PDF | 标准 schema 提示词 |
| `detail` | 财报附注（多级表头）、扫描件、印章/水印、跨页表格 | 追加"逐字符确认"、"多级表头精确度"、"扫描件容错（用 `?` 占位）"、"币种推理"等约束 |

`prompts.build_prompt(mode)` 返回完整提示词。

## 评测建议

针对同一份 GT 集，跑两遍并对比：

```bash
# normal
for pdf in samples/documents/*.pdf; do
  .venv/bin/python3 scripts/skill.py parse \
    --input "$pdf" --output "samples/outputs_normal/$(basename "$pdf" .pdf)" \
    --parse-mode normal
done

# detail
for pdf in samples/documents/*.pdf; do
  .venv/bin/python3 scripts/skill.py parse \
    --input "$pdf" --output "samples/outputs_detail/$(basename "$pdf" .pdf)" \
    --parse-mode detail
done

python3 evaluation/scripts/run_eval.py --pred_dir samples/outputs_normal --gt_dir ...
python3 evaluation/scripts/run_eval.py --pred_dir samples/outputs_detail --gt_dir ...
```

报告中给出"normal vs detail 在 NumAcc / TEDS 上的提升"是课题加分项。

## 自定义 Prompt

若要在不改代码的前提下做 Prompt 实验：

1. 新建 `prompts_v2.py`，定义 `build_prompt(mode)`
2. 临时 `PYTHONPATH=skills/pdf-finance-parser/experiments python3 ...`
3. 或在 [prompts.py](../scripts/prompts.py) 里增加第三档 `detail-v2`

切忌往 prompt 里塞业务规则（如"千分位去逗号"、"括号代表负数"）—— 这些应由提示词的"输出 schema 约束"间接驱动模型完成，而不是预先做规则替换。
