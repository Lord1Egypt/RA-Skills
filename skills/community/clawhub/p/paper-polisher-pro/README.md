# Paper Polisher Pro — 论文降AI润色工具 · AI率检测

[![GitHub Stars](https://img.shields.io/github/stars/docsor1212/paper-polisher-pro?style=social&label=Star)](https://github.com/docsor1212/paper-polisher-pro)

AI 痕迹检测（AI率）· 去AI化改写建议 · 句子级改写建议（哪几句像AI、怎么改）· 术语标准化 · 翻译腔检查 · 质量报告 · AIGC 合规标识检查 · 段落级归因 · 期刊口径预检。

**100% 本地运行，零上传，零凭证**——论文数据不出本机。零网络承诺可用包内 `pp_verify.py`（AST 结构化扫描）自行验证，行为契约可用随包 `tests/` 单元测试套件（随版本增长，`pp.py test` 一键复跑当前全套）在自己机器上复跑。

## 这是什么

面向学术写作者的 AI 痕迹自查工具：概率化输出（非二元判定）、分层证据、指纹归因（GLM / DeepSeek / Qwen / Kimi / MiniMax / GPT / Claude / Gemini），全部指标可由随包留出集评测复现。

- 基础引擎（纯规则+词频谱）：留出集 AUROC 0.9187
- 可选监督层（本地 Qwen3-0.6B ONNX）：AUROC 0.9998（作者侧留出集、指纹绑定实测；版本时代档案另有 1.0 列，现行口径以指纹绑定为准）
- 短文本不出判定（<100 字，误报铁律）

## 快速开始

```bash
# 零模型零文件一键体验
python scripts/pp.py quickstart

# AI 痕迹检测（AI率）
python scripts/ai_detector.py draft.txt --format json

# 句子级改写建议（定位+策略，不代改）
python scripts/pp_fix_suggest.py draft.txt --top 10

# 学术写作规范自查（全半角/数字/缩写/单位/同概念异写一致性，不评分）
python scripts/pp_style_norm.py draft.txt

# 集成前看输出样例（真实引擎 JSON + 渲染好的 HTML 仪表盘）
ls examples/outputs/

# Word 文档直读 + 投稿前自查包
python scripts/pp_report_bundle.py thesis.docx --outdir ~/selfcheck

# 期刊口径预检（分学科语境）+ 指纹保鲜状态
python scripts/ai_detector.py draft.txt --profile journal --format json
python scripts/pp.py freshness --status

# 四层融合门禁
python scripts/deai_gate.py draft.txt

# 单文档可视化仪表盘（workflow/detect/fix/norm JSON → 一份自包含 HTML）
python scripts/pp.py html-report draft.workflow.json -o report.html

# 不知道用哪个命令？自然语言路由
python scripts/pp.py recommend "把这段的AI率降一降"

# 批量检测一个目录
python scripts/ai_detector.py --batch ./drafts --csv scores.csv

# 环境自检
python scripts/pp_doctor.py

# Python 编程接口（零网络，import 即用）
python -c "import sys; sys.path.insert(0,'scripts'); from pp_api import detect_text; \
print(detect_text(open('draft.txt').read())['overall_ai_score'])"

# 监督层一键装模（作者签发模型文件，指纹校验+推理自检）
python scripts/pp_setup.py --model <作者签发模型.onnx>
```

## 安装

克隆本仓库后直接使用，纯 Python 标准库即可运行（可选 onnxruntime 增强监督层，依赖声明见 `requirements.txt`）。

```bash
git clone https://github.com/docsor1212/paper-polisher-pro
cd paper-polisher-pro
python scripts/ai_detector.py your_draft.txt --format summary
```

**China mirror (ModelScope 魔搭)**: <https://modelscope.cn/skills/Docsor/paper-polisher-pro> — if you find this skill useful, a like there helps others find it.

## 论文工作流家族

写作是一条链，每环有专用工具（均在本账号下）：

| 工具 | 用途 |
|---|---|
| **paper-polisher-pro**（本仓库） | AI率检测·润色·降重·质量报告 |
| **paper-rewriter** | 论文降AI改写执行 |
| **pubmed-verifier** | PMID/DOI 引用核验 |
| **cite-holmes** | 深度调研 × 引用自证 |
| **cn-med-oa** | 中文医学文献 OA 下载 |
| **academic-figures** | 出版级科研图表 |
| **doc-holmes** | PDF 精准翻译 |

文档站：[docsor.cn](https://docsor.cn)

## 合规声明

本工具供作者自查与写作质量改进，**不用于规避机构的 AIGC 检测**；请遵循所在机构的 AI 使用与披露政策（标识合规可用包内 aigc_label_check 自查）。许可：MIT-0。
