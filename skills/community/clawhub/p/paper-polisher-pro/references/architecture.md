# 架构与指纹保鲜（Architecture & fingerprint freshness）

> 从 SKILL.md 迁出的深度参考（v6.1.0）。日常使用无需阅读；按需查阅。

---

## Fingerprint freshness (against "detectors lag one generation")

Coverage as of 2026-09-26: kimi-k3 & kimi-k2.7 registered (OpenCode Go fresh sampling, attribution-verified); qwen3.8 / deepseek-v4 / deepseek-v4.1 / minimax-m3 sampled — mining produced no family-distinctive low-FP patterns, honestly unregistered; glm-5.3 refreshed (no new patterns). Next: deepseek-v4.1 & minimax-m3 with larger corpora.

On a new-model release day: `python scripts/fingerprint_miner.py --corpus <new_samples.jsonl> --model <family> --apply`
Monthly full pass: `python scripts/freshness_refresh.py` (schedule it with your own system timer, e.g. monthly; the script never creates or modifies system schedules). Compare adjacent `eval/results/freshness_*.json`; investigate if AUROC drops by more than 3 percentage points.

---

## 指纹保鲜（对抗"检测器慢一代"）

覆盖截至 2026-09-26：kimi-k3 与 kimi-k2.7 已入册（OpenCode Go 新鲜采样，归因验证通过）；qwen3.8 / deepseek-v4 / deepseek-v4.1 / minimax-m3 已采样——无家族区分性低误报模式，如实不入册；glm-5.3 已刷新（无新模式）。后续：deepseek-v4.1 与 minimax-m3 扩大语料再战。

新模型发布当天：`python scripts/fingerprint_miner.py --corpus <新采样.jsonl> --model <family> --apply`
月度全量：`python scripts/freshness_refresh.py`（用你自己的系统定时器调度；本脚本不创建、不修改任何系统调度项）。对比相邻两次 `eval/results/freshness_*.json`，AUROC 掉幅 >3pt 人工介入。

---

## Architecture (v3)

Reference section — read on demand; everyday use needs none of it.

```
ai_detector.py            Main engine: 8 rule layers (125 recalibrated patterns, markdown caps,
                          EN openers, paragraph-level language) + length-routed fusion
 + layers_surface.py      L9 surface stats L10 token-spectrum (9,955-token delta spectrum)
                          L11 chain-of-thought features
 + ai_detector L12        discourse-structure heuristics (v3.7.0: hook/reversal/slogan/engagement)
 + fusion_config.json     Weights & thresholds (calib-half grid search + human p95/p99)
 + model_fingerprints.json v4 fingerprint registry (13 families incl. GLM-5.3 & Kimi K-series self-sampled; attribution only)
 + layers_lm.py           Optional supervised layer (local ONNX + pure-Python Qwen tokenizer;
                          PP_NO_SUP=1 falls back to rules)
paragraph_report.py       Paragraph-level attribution HTML (pattern×spectrum 50/50 fusion)
pp_report_html.py         Single-document visual dashboard (workflow/detect/fix/norm JSON → one HTML; v5.8.0)
aigc_label_check.py       AIGC compliance labels (China labeling rules 2025-09: metadata/C2PA/explicit)
fingerprint_miner.py      Fingerprint mining (new model drop → sample → mine → register)
pattern_recalibrator.py   Data-driven pattern recalibration (human-hit filtering)
build_spectrum.py / calibrate_v3.py   Spectrum build / weight calibration
freshness_refresh.py         Monthly freshness pipeline (sample → rebuild → calibrate → regression)
pp_doctor.py              Environment self-check (v3.5; v5.0.0 adds latest-eval-record row)
pp_verify.py              AST-level structured zero-network self-verification (v5.0.0)
pp_fix_suggest.py         Sentence-level rewrite suggestions (v5.0.0: locate + strategy, no auto-rewrite)
tests/                    Bundled unit-test suite, `python3 -m unittest discover -s tests -t .` (v5.0.0)
requirements.txt          Dependency declaration: core zero-dep; optional supervised-layer extras (v5.0.0)
eval/                     corpus_builder / attack_gen / run_eval (AUROC, TPR@FPR, per-model, attack decay)
```

---

## v3 架构

参考节——按需阅读，日常使用无需读完。

```
ai_detector.py            主引擎: 8个规则层(重校准125条模式, markdown限帽, 段落级语言)
                          + 长度路由融合
 + layers_surface.py      L9表面统计 L10词频谱(9,955 token差谱) L11思维链特征
 + ai_detector L12        篇章结构启发层(v3.7.0: 自媒体钩子/反转/口号/互动引导)
 + fusion_config.json     权重与阈值(calib半网格搜索 + 人类p95/p99)
 + model_fingerprints.json v4指纹registry(13家族含GLM-5.3/Kimi K系列自采样注册, 只归因)
 + layers_lm.py           可选监督层(本地ONNX + 纯Python Qwen tokenizer; PP_NO_SUP=1 回退纯规则)
paragraph_report.py       段落级归因HTML(模式×谱 50/50 融合段评分)
pp_report_html.py         单文档可视化仪表盘(workflow/detect/fix/norm JSON → 单文件 HTML; v5.8.0 新增)
aigc_label_check.py       AIGC合规标识(《标识办法》2025-09: 元数据/C2PA/显式声明)
fingerprint_miner.py      指纹自动挖掘 | pattern_recalibrator.py 模式库数据驱动重校准
build_spectrum.py / calibrate_v3.py   词频谱构建 / 权重校准
freshness_refresh.py         月度保鲜流水线(采样→重建→校准→回归)
pp_doctor.py              环境自检（v3.5 新增；v5.0.0 增最近评测记录行）
pp_verify.py              结构化零网络自证（AST 级，v5.0.0 新增）
pp_fix_suggest.py         句子级改写建议（v5.0.0 新增：指位+策略，不代改）
tests/                    随包单元测试套件，`python3 -m unittest discover -s tests -t .`（v5.0.0 新增）
requirements.txt          依赖声明：核心零依赖；可选监督层依赖注释声明（v5.0.0 新增）
eval/                     corpus_builder / attack_gen / run_eval(AUROC/TPR@FPR/分模型/攻击衰减)
```
