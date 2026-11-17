# IBCAT — 国际双语对照及中文高级原版翻译机 / International Bilingual Chinese Advanced Translator

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)]()
[![BabelDOC](https://img.shields.io/badge/Engine-BabelDOC-green.svg)](https://github.com/funstory-ai/BabelDOC)
[![Language](https://img.shields.io/badge/Language-Python%203-red.svg)]()

> **本 Skill 由 Wang Dongjie 王东杰 创作 / Created by Wang Dongjie**
>
> 资深复合型战略财务专家 · 上市公司资本运作操盘手 · 集团化财务管控与风险治理高级工程师
>
> Senior Strategic Finance Expert · Listed Co. Capital Ops Lead · Group Finance Control & Risk Gov. Sr. Engineer
>
> 📧 Wdj_@163.com · 📱 13952453499

---

## 📖 项目简介 / Introduction

**中文：** 基于 [BabelDOC](https://github.com/funstory-ai/BabelDOC) 引擎的 PDF 双语翻译自动化技能。通过三阶段流水线（提取→翻译→渲染），将英文 PDF 转换为保留原始排版的中英双语对照 PDF 和纯中文 PDF。内置本地字体补丁方案，支持离线/受限网络环境运行。

**English:** An automated PDF bilingual translation skill powered by [BabelDOC](https://github.com/funstory-ai/BabelDOC). Through a three-phase pipeline (Extract → Translate → Render), it converts English PDFs into layout-preserving bilingual side-by-side PDFs and monolingual Chinese PDFs. Includes a local font patching solution for offline/restricted-network environments.

## ✨ 核心特性 / Key Features

| 特性 / Feature | 说明 / Description |
|---|---|
| 🔄 三阶段流水线 / Three-Phase Pipeline | 提取→翻译→渲染，全程自动化 / Extract → Translate → Render, fully automated |
| 📐 保留原始排版 / Layout Preservation | 完整保留原始 PDF 的版面设计 / Fully preserves the original PDF layout design |
| 🌐 双语对照输出 / Bilingual Side-by-Side Output | 英文原文与中文翻译并排显示 / English original and Chinese translation displayed side-by-side |
| 🔌 LLM 桥接代理 / LLM Bridge Proxy | OpenAI 兼容代理服务器，支持任意 LLM / OpenAI-compatible proxy server, supports any LLM |
| 🔤 离线字体支持 / Offline Font Support | 自动补丁本地 CJK 字体，无需网络下载 / Auto-patches local CJK fonts, no network download required |
| 📊 并行翻译 / Parallel Translation | 支持分批并行翻译，提升效率 / Supports batch parallel translation for improved efficiency |
| ✅ 内置验证 / Built-in Verification | 自动验证中文渲染和字体嵌入 / Automatically verifies Chinese rendering and font embedding |

## 🏗️ 架构 / Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐     ┌──────────────┐
│  原始 PDF    │────▶│  BabelDOC    │────▶│  翻译代理    │────▶│  双语 PDF     │
│  Source PDF  │     │  解析+排版    │     │  Translation │     │  Bilingual   │
│  (English)   │     │  Parse+Layout│     │  Proxy (LLM) │     │  PDF Output  │
└─────────────┘     └──────────────┘     └─────────────┘     └──────────────┘
```

| 阶段 / Phase | 模式 / Mode | 说明 / Description |
|---|---|---|
| Phase 1: 提取 / Extract | `extract` | BabelDOC 解析 PDF，通过代理收集所有待翻译文本段落 / BabelDOC parses the PDF and collects all text segments via the proxy |
| Phase 2: 翻译 / Translate | — | 将提取的文本段落分批送入 LLM 翻译 / Send extracted segments to LLM in batches |
| Phase 3: 渲染 / Render | `translate` | BabelDOC 使用翻译结果重新排版，生成最终双语 PDF / BabelDOC re-typesets with translations |

## 🚀 快速开始 / Quick Start

### 安装 / Installation

```bash
# 克隆仓库 / Clone the repository
git clone https://github.com/your-username/International-Bilingual-PDF-Translation-SKILL.git

# 安装依赖 / Install dependencies
pip install babeldoc pdfplumber --break-system-packages

# 应用字体补丁 / Apply font patches
python3 scripts/setup_fonts.py
```

### 使用 / Usage

```bash
# Phase 1: 提取文本段落 / Extract text segments
bash scripts/translate_pdf.sh \
  --input "your-document.pdf" \
  --output-dir "/workspace/output" \
  --lang-in en \
  --lang-out zh-cn

# Phase 2: 翻译（使用 LLM 子代理）/ Translate (using LLM sub-agents)
python3 scripts/split_segments.py /data/user/work/segments.json /data/user/work
# ... translate batches with LLM ...

# Phase 3: 生成最终 PDF / Generate final PDF
bash scripts/render_pdf.sh \
  --input "your-document.pdf" \
  --output-dir "/workspace/output" \
  --work-dir "/data/user/work"
```

详细使用说明请参阅 [SKILL.md](SKILL.md)。  
For detailed usage instructions, see [SKILL.md](SKILL.md).

## 📁 文件结构 / File Structure

```
├── SKILL.md                      # 技能完整文档 / Complete skill documentation
├── README.md                     # 本文件 / This file
├── LICENSE                       # MIT 许可证 / MIT License
├── scripts/
│   ├── proxy_server.py           # OpenAI 兼容翻译代理 / OpenAI-compatible translation proxy
│   ├── setup_fonts.py            # 字体补丁脚本 / Font patching script
│   ├── translate_pdf.sh          # Phase 1 提取脚本 / Phase 1 extraction script
│   ├── render_pdf.sh             # Phase 3 渲染脚本 / Phase 3 rendering script
│   ├── verify_pdf.py             # PDF 验证脚本 / PDF verification script
│   └── split_segments.py         # 段落分批工具 / Segment splitting utility
└── templates/
    └── glossary_template.csv     # 术语表模板 / Glossary template
```

## ✅ 已验证案例 / Verified Use Case

**中文：** 本技能已在 Rise2040 Vision Report（47页，AICPA & CIMA 发布）上完成完整验证。

**English:** This skill has been fully verified on the Rise2040 Vision Report (47 pages, published by AICPA & CIMA).

| 指标 / Metric | 数值 / Value |
|---|---|
| PDF 页数 / PDF pages | 47 |
| 提取段落数 / Extracted segments | 760 |
| 翻译批次 / Translation batches | 3 (并行 / parallel) |
| 双语对照 PDF / Bilingual PDF | ✅ 通过 / Pass |
| 纯中文 PDF / Monolingual PDF | ✅ 通过 / Pass |
| CJK 字体嵌入 / CJK font embedding | ✅ 验证通过 / Verified |

## ⚠️ 注意事项 / Important Notes

- **必须清除翻译缓存 / Must clear translation cache:** `rm -f /root/.cache/babeldoc/cache.v1.db`
- **字体补丁需在 BabelDOC 更新后重新应用 / Font patches must be reapplied after BabelDOC updates**
- **需要系统安装 Noto CJK 字体 / Requires Noto CJK fonts installed on the system**

## 📝 许可证 / License

本项目基于 MIT 许可证开源。详见 [LICENSE](LICENSE)。

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## 👤 作者 / Author

**Wang Dongjie 王东杰**

资深复合型战略财务专家 · 上市公司资本运作操盘手 · 集团化财务管控与风险治理高级工程师

Senior Strategic Finance Expert · Listed Co. Capital Ops Lead · Group Finance Control & Risk Gov. Sr. Engineer

- 📧 Email: Wdj_@163.com
- 📱 Phone: 13952453499

## 🙏 致谢 / Acknowledgments

- [BabelDOC](https://github.com/funstory-ai/BabelDOC) - PDF 解析与排版引擎 / PDF parsing & typesetting engine
- [pdfplumber](https://github.com/jsvine/pdfplumber) - PDF 验证工具 / PDF verification tool
- [Noto CJK Fonts](https://github.com/notofonts/noto-cjk) - CJK 字体支持 / CJK font support

---

*IBCAT SKILL v1.0.0 — (c) 2026 Wang Dongjie 王东杰*

*IBCAT SKILL v1.0.0 — (c) 2026 Wang Dongjie*
