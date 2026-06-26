# 常见问题 FAQ

## Q1: 为什么不直接用 PyMuPDF / pdfplumber / Camelot 抽内容？

A：那是规则路线。本 Skill 是 AI-first：规则路线在面对**无边框表格 / 多级表头 / 跨页延续 / 扫描件 / 印章**时易碎，每条 case 都要写专门启发式。多模态 VLM 把这些都收敛到"模型理解"层面，只要 Prompt 给到位，本地代码就不需要维护任何专家规则。

PyMuPDF 在本仓库**只用于把 PDF 栅格化成 PNG**（即给模型送图），不再用 `get_text()` / `find_tables()`。

## Q2: 模型偶尔返回非 JSON 怎么办？

A：[vlm_client.py](../scripts/vlm_client.py) 内部按"剥 Markdown 围栏 → 截取首个 `{` 到末尾 `}`"两层兜底；仍失败抛 `VLMError`，调用方在 `meta.json.failed_pages` 中记录该页。重跑该页通常即可恢复。

设置 `temperature=0.0` 已经能极大降低非 JSON 概率。

## Q3: 跨页表格如何合并？

A：本 Skill 当前**不在本地合并**。每页独立输出，caption 中由模型标注 "(续上页)" / "(续下页)"。如果评测时需要"合并后再比 TEDS"，请在 evaluation 侧加一个合并步骤（按 caption 前缀 + 列数匹配），而不要把合并逻辑写到本 Skill 内部。

理由：跨页合并是评测口径问题，不是解析问题；让它留在评测层更可控。

## Q4: 长文档怎么提速？

A：
1. 优先用 `--pages` 切片（如 `1-50` 然后 `51-100`），分批 parse 后用 evaluation 合并
2. ARK 等付费 provider 通常可申请提 QPS 配额，比并发本地进程稳
3. 不要 `xargs -P` 并发跑多个 skill.py，会触发 rate limit

## Q5: detail 模式贵多少？

A：`detail` 提示词更长、要求模型"逐字符确认"，输出 token 也更多。粗略估计是 normal 的 1.5~2x 成本，但 NumAcc 通常能从 ~85% 升到 ~95%（具体看模型与文档质量，以你自己的评测为准）。

## Q6: 评测脚本读哪个字段？

A：`evaluation/scripts/run_eval.py` 读 `<output_dir>/output.json`，其结构由 `_merge_doc_json` 合成，符合 [output_schema.json](../assets/output_schema.json)。表格按 `table_id`（`t_001` / `t_002` ...）对齐 GT 中的同名 ID。

## Q7: 想换其他多模态模型测试？

A：两种方式：
- 一次性切换：`--model qwen-vl-max` 或 `export VLM_MODEL=...`
- 改默认：编辑 [vlm_client.py](../scripts/vlm_client.py) 的 `_PROVIDER_DEFAULTS`

不要 fork 出多个 `vlm_client_qwen.py` / `vlm_client_doubao.py`—— OpenAI 兼容协议一份代码就够。

## Q8: `_legacy/` 目录是干嘛的？

A：之前规则路线的代码（parse.py / table_extractor.py / layout.py / numeric_normalizer.py 等）。保留作为对比 baseline 参考，**不在生产路径上调用**。评测时若想做"规则 vs AI"对比，可单独写一个 baseline runner 调用 `_legacy/`，但 SKILL 本体不依赖。
