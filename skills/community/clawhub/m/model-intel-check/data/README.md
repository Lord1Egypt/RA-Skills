# data/ 题库说明

题库文件**不随 skill 分发**（GPQA 有协议限制，且公开题面不宜二次传播），
首次使用前在 skill 目录运行 `python make_data.py` 生成。

## 需要的文件

### aime2025.jsonl / aime2026.jsonl（AIME 2025 / 2026，各 30 题）

每行一个 JSON：`{"id": "0", "index": 0, "problem": "...", "answer": "70"}`

- `id` 为下标字符串、`index` 为下标（0 起），行序 = 官方题序
- 来源：`math-ai/aime25`、`math-ai/aime26`（均匿名可下），`make_data.py` 默认两年都构建
- `intel_check.py` 默认用 2025（与既有参考线同口径）；跑 2026 加 `--aime-file aime2026.jsonl`
- **防背题优先用更新的年份**

### gpqa_diamond_50.jsonl（GPQA Diamond 前 50 条，选择题）

每行：`{"id": "recXXX", "question": "...", "choices": ["正确项", "干扰项1", "干扰项2", "干扰项3"], "correct_index": 0, "domain": "..."}`

- **`choices[0]` 必须是正确答案**（`correct_index: 0`）；选项洗牌由
  `intel_check.py` 在运行时用固定种子 `42+题号` 完成，不要在数据里预先洗牌
- 来源：`Idavidrein/gpqa`（gated），需 `HF_TOKEN`；拿不到就只跑 AIME
  （`intel_check.py --suite aime --aime-indices 0-29`）

## 换模型/换题库

测其他模型时协议不变；想防"背题"可用自改数字的变体题替换 AIME，
但那样分数只能和自建的基线比，不能与官方参考值直接对照。
