# IBCAT — 国际双语对照及中文高级原版翻译机 / International Bilingual Chinese Advanced Translator

> **本 Skill 由 Wang Dongjie 王东杰 创作 / Created by Wang Dongjie**  
> 资深复合型战略财务专家 · 上市公司资本运作操盘手 · 集团化财务管控与风险治理高级工程师  
> Senior Strategic Finance Expert · Listed Co. Capital Ops Lead · Group Finance Control & Risk Gov. Sr. Engineer  
> 📧 Wdj_@163.com · 📱 13952453499  
>
> **版本 / Version：** 1.0.0  
> **创建日期 / Created：** 2026-07-22  
> **引擎 / Engine：** BabelDOC + LLM Bridge  
> **许可 / License：** MIT  

---

## 描述 / Description

**中文：** PDF 双语翻译技能，基于 BabelDOC 引擎实现保留原始排版的 PDF 双语对照翻译。支持英译中及其他语言对，通过三阶段流水线（提取→翻译→渲染）生成高质量的双语 PDF。

**English:** A PDF bilingual translation skill powered by the BabelDOC engine, delivering layout-preserving side-by-side bilingual PDF translation. Supports English-to-Chinese and other language pairs through a three-phase pipeline (Extract → Translate → Render) to produce high-quality bilingual PDFs.

**触发条件 / Trigger Conditions：** 当用户请求翻译 PDF 文件、生成双语对照 PDF、或使用 "translate-pdf" / "BabelDOC" / "双语翻译" / "国际双语对照" / "bilingual translation" 等关键词时激活。  
**English:** Activate when the user requests PDF translation, bilingual side-by-side PDF generation, or uses keywords such as "translate-pdf", "BabelDOC", "bilingual translation", etc.

## 概览 / Overview

**中文：** 本技能使用 [BabelDOC](https://github.com/funstory-ai/BabelDOC) 作为 PDF 解析与排版引擎，通过本地翻译代理服务器桥接 LLM 翻译能力，实现端到端的 PDF 双语翻译流水线。

**English:** This skill uses [BabelDOC](https://github.com/funstory-ai/BabelDOC) as the PDF parsing and typesetting engine, bridging LLM translation capabilities through a local translation proxy server to achieve an end-to-end PDF bilingual translation pipeline.

### 工作原理 / How It Works

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐     ┌──────────────┐
│  原始 PDF    │────▶│  BabelDOC    │────▶│  翻译代理    │────▶│  双语 PDF     │
│  Source PDF  │     │  解析+排版    │     │  Translation │     │  Bilingual   │
│  (English)   │     │  Parse+Layout│     │  Proxy (LLM) │     │  PDF Output  │
└─────────────┘     └──────────────┘     └─────────────┘     └──────────────┘
```

**三阶段流水线 / Three-Phase Pipeline：**

| 阶段 / Phase | 模式 / Mode | 说明 / Description |
|------|------|------|
| Phase 1: 提取 / Extract | `extract` | BabelDOC 解析 PDF，通过代理收集所有待翻译文本段落 / BabelDOC parses the PDF and collects all text segments via the proxy |
| Phase 2: 翻译 / Translate | — | 将提取的文本段落分批送入 LLM 翻译，生成 translations.json / Send extracted segments to LLM in batches, generate translations.json |
| Phase 3: 渲染 / Render | `translate` | BabelDOC 使用翻译结果重新排版，生成最终双语 PDF / BabelDOC re-typesets with translations, generates the final bilingual PDF |

### 输出文件 / Output Files

- **双语对照 PDF / Bilingual Side-by-Side PDF** (`.dual.pdf`)：英文原文 + 中文翻译并排显示，保留原始排版 / English original + Chinese translation displayed side-by-side, preserving original layout
- **纯中文 PDF / Monolingual Chinese PDF** (`.mono.pdf`)：中文翻译替换原文 / Chinese translation replacing the original text

## 前置条件 / Prerequisites

### 系统依赖 / System Dependencies

```bash
# BabelDOC
pip install babeldoc --break-system-packages

# PDF 验证工具 / PDF verification tool
pip install pdfplumber --break-system-packages
```

### CJK 字体要求 / CJK Font Requirements

**中文：** 系统需安装 Noto CJK 字体（或兼容的思源黑体/宋体）：

**English:** The system requires Noto CJK fonts (or compatible Source Han Sans/Serif fonts):

```bash
# Ubuntu/Debian
apt-get install fonts-noto-cjk

# 验证 / Verify
fc-list | grep -i "noto.*cjk"
```

### 字体补丁（关键步骤）/ Font Patching (Critical Step)

**中文：** BabelDOC 默认从网络下载字体并校验哈希。在离线/受限网络环境中，需要补丁字体加载逻辑以使用本地字体。运行 `scripts/setup_fonts.py` 自动完成补丁：

**English:** BabelDOC downloads fonts from the network and verifies hashes by default. In offline or restricted-network environments, the font loading logic must be patched to use local fonts. Run `scripts/setup_fonts.py` to apply patches automatically:

```bash
python3 scripts/setup_fonts.py
```

**该脚本会 / This script will：**
1. 将系统 Noto CJK 字体符号链接到 BabelDOC 缓存目录 / Symlink system Noto CJK fonts to BabelDOC's cache directory
2. 修改 BabelDOC 源码，跳过字体哈希验证 / Patch BabelDOC source to skip font hash verification
3. 修改 CMap 文件加载逻辑，跳过哈希验证 / Patch CMap file loading to skip hash verification
4. 修改 `get_fastest_upstream_for_font` 避免网络调用 / Patch `get_fastest_upstream_for_font` to avoid network calls

## 工作流程 / Workflow

### 完整自动化流程 / Full Automated Workflow

**中文：** 使用 `scripts/translate_pdf.sh` 一键执行 Phase 1 提取流水线：

**English:** Use `scripts/translate_pdf.sh` to execute the Phase 1 extraction pipeline in one shot:

```bash
bash scripts/translate_pdf.sh \
  --input "input.pdf" \
  --output-dir "/workspace/output" \
  --lang-in en \
  --lang-out zh-cn \
  --work-dir "/data/user/work/translate_work" \
  --glossary "glossary.csv"
```

### 分步手动执行 / Step-by-Step Manual Execution

#### Step 1: 环境准备 / Environment Setup

```bash
# 安装 BabelDOC（如未安装）/ Install BabelDOC (if not installed)
pip install babeldoc --break-system-packages

# 应用字体补丁 / Apply font patches
python3 scripts/setup_fonts.py

# 清除旧缓存（重要！避免使用过期翻译缓存）
# Clear old cache (IMPORTANT! Avoid using stale translation cache)
rm -f /root/.cache/babeldoc/cache.v1.db
```

#### Step 2: 启动翻译代理（提取模式）/ Start Translation Proxy (Extract Mode)

```bash
# 清理旧数据 / Clean old data
rm -f /data/user/work/segments.json /data/user/work/translations.json /data/user/work/unknown_segments.json

# 启动代理服务器（extract 模式）/ Start proxy server (extract mode)
PROXY_MODE=extract python3 scripts/proxy_server.py &
sleep 2

# 验证代理运行 / Verify proxy is running
curl -s http://127.0.0.1:8899/v1/models
```

#### Step 3: 运行 BabelDOC 提取文本 / Run BabelDOC to Extract Text

```bash
babeldoc \
  --files "input.pdf" \
  --lang-in en \
  --lang-out zh-cn \
  --openai \
  --openai-base-url http://127.0.0.1:8899/v1 \
  --openai-api-key dummy-key \
  --openai-model gpt-4o-mini \
  --output /workspace/babeldoc_output \
  --working-dir /data/user/work/babeldoc_work \
  --no-auto-extract-glossary \
  --skip-scanned-detection \
  --no-watermark \
  --qps 100
```

#### Step 4: 翻译提取的文本段落 / Translate Extracted Text Segments

**中文：** 提取完成后，`segments.json` 包含所有待翻译文本。使用子代理分批翻译：

**English:** After extraction, `segments.json` contains all text segments to translate. Use sub-agents for batch translation:

```bash
# 查看段落数量 / Check segment count
python3 -c "import json; d=json.load(open('/data/user/work/segments.json')); print(f'Segments: {len(d)}')"

# 分批翻译（建议每批 ≤260 段，最多 3 批并行）
# Batch translation (recommended ≤260 segments per batch, max 3 parallel batches)
# 使用 Task 工具启动子代理，每个子代理读取一批段落并输出 translations_batch_N.json
# Use Task tool to launch sub-agents; each reads a batch and outputs translations_batch_N.json

# 合并所有批次 / Merge all batches
python3 -c "
import json
all_t = {}
for i in range(1, 4):
    with open(f'/data/user/work/translations_batch_{i}.json') as f:
        all_t.update(json.load(f))
with open('/data/user/work/translations.json', 'w') as f:
    json.dump(all_t, f, ensure_ascii=False, indent=2)
print(f'Merged: {len(all_t)} translations')
"
```

**翻译规则要点 / Translation Rules：**
- 保留 BabelDOC 占位符原样不变：`{v1}`、`{v2}` 等花括号占位符 / Preserve BabelDOC placeholders as-is: `{v1}`, `{v2}`, etc.
- 保留样式标签结构：`<style id='N'>text</style>` — 标签原样保留，标签内文字翻译 / Preserve style tag structure: `<style id='N'>text</style>` — tags kept as-is, text inside translated
- 纯数字/百分比/符号段落原样返回 / Return pure numbers/percentages/symbols as-is
- 专有名词按术语表处理 / Handle proper nouns per glossary

#### Step 5: 重启代理（翻译模式）并生成最终 PDF / Restart Proxy (Translate Mode) and Generate Final PDF

```bash
# 停止旧代理 / Stop old proxy
kill $(lsof -ti:8899) 2>/dev/null; sleep 1

# 启动翻译模式代理 / Start translate-mode proxy
PROXY_MODE=translate python3 scripts/proxy_server.py &
sleep 2

# 清除 BabelDOC 翻译缓存（重要！）/ Clear BabelDOC translation cache (CRITICAL!)
rm -f /root/.cache/babeldoc/cache.v1.db

# 运行 BabelDOC 生成最终 PDF / Run BabelDOC to generate final PDF
babeldoc \
  --files "input.pdf" \
  --lang-in en \
  --lang-out zh-cn \
  --openai \
  --openai-base-url http://127.0.0.1:8899/v1 \
  --openai-api-key dummy-key \
  --openai-model gpt-4o-mini \
  --output /workspace/babeldoc_final \
  --working-dir /data/user/work/babeldoc_work_final \
  --no-auto-extract-glossary \
  --skip-scanned-detection \
  --no-watermark \
  --qps 100

# 停止代理 / Stop proxy
kill $(lsof -ti:8899) 2>/dev/null
```

#### Step 6: 验证输出 / Verify Output

```python
import pdfplumber

with pdfplumber.open("output.dual.pdf") as pdf:
    for i, page in enumerate(pdf.pages):
        text = page.extract_text() or ""
        has_chinese = any('\u4e00' <= c <= '\u9fff' for c in text)
        fonts = set(c.get('fontname', '?') for c in page.chars)
        has_cjk_font = any('Source Han' in f or 'Noto' in f for f in fonts)
        print(f"Page {i+1}: Chinese={has_chinese}, CJK Font={has_cjk_font}")
```

## 关键注意事项 / Critical Notes

### 必须清除翻译缓存 / Must Clear Translation Cache

**中文：** 每次重新翻译时，**必须**清除 BabelDOC 的翻译缓存数据库，否则会使用上一次的过期翻译：

**English:** Before each re-translation, you **MUST** clear BabelDOC's translation cache database, otherwise stale translations from the previous run will be used:

```bash
rm -f /root/.cache/babeldoc/cache.v1.db
```

### 字体补丁持久性 / Font Patch Persistence

**中文：** BabelDOC 更新后补丁会被覆盖，需重新运行 `setup_fonts.py`。可通过以下命令检查补丁状态：

**English:** Patches will be overwritten after a BabelDOC update; re-run `setup_fonts.py`. Check patch status with:

```python
import babeldoc.assets.assets as assets
import inspect
src = inspect.getsource(assets.get_font_and_metadata_async)
print("PATCHED" if "LOCAL PATCH" in src else "NOT PATCHED")
```

### 代理服务器端口 / Proxy Server Port

**中文：** 默认使用端口 `8899`。如端口被占用，修改 `proxy_server.py` 中的 `port` 变量。

**English:** Default port is `8899`. If the port is occupied, modify the `port` variable in `proxy_server.py`.

### 翻译质量保证 / Translation Quality Assurance

- 使用术语表（glossary.csv）确保专有名词一致性 / Use glossary (glossary.csv) to ensure proper noun consistency
- 分批翻译时每批不超过 260 段 / Each batch should not exceed 260 segments
- 翻译完成后检查 `unknown_segments.json`，确保无遗漏 / Check `unknown_segments.json` after translation to ensure no segments are missed
- 验证最终 PDF 中文字体正确嵌入（非 Roboto/Latin 字体）/ Verify CJK fonts are properly embedded in the final PDF (not Roboto/Latin fonts)

## 文件结构 / File Structure

```
IBCAT/
├── SKILL.md                      # 技能说明文件 / Skill documentation
├── README.md                     # GitHub README (中英双语 / Bilingual)
├── LICENSE                       # MIT 许可证 / MIT License
├── scripts/
│   ├── proxy_server.py           # OpenAI 兼容翻译代理服务器 / OpenAI-compatible translation proxy
│   ├── setup_fonts.py            # 字体补丁脚本 / Font patching script
│   ├── translate_pdf.sh          # Phase 1 一键提取脚本 / Phase 1 one-shot extraction script
│   ├── render_pdf.sh             # Phase 3 一键渲染脚本 / Phase 3 one-shot rendering script
│   ├── verify_pdf.py             # PDF 验证脚本 / PDF verification script
│   └── split_segments.py         # 段落分批工具 / Segment splitting utility
└── templates/
    └── glossary_template.csv     # 术语表模板 / Glossary template
```

## 限制 / Limitations

- 需要系统安装 CJK 字体（Noto CJK 或思源字体）/ Requires CJK fonts installed on the system (Noto CJK or Source Han fonts)
- 网络受限环境需要本地字体补丁 / Restricted-network environments require local font patching
- 翻译质量取决于 LLM 子代理的翻译能力 / Translation quality depends on the LLM sub-agent's translation capability
- 大型 PDF（>50页）可能需要较长时间和较大内存（~5GB）/ Large PDFs (>50 pages) may require significant time and memory (~5GB)
- 扫描版 PDF 需先进行 OCR / Scanned PDFs require OCR preprocessing first

## 已验证案例 / Verified Use Case

**中文：** 本技能已在 Rise2040 Vision Report（47页，AICPA & CIMA 发布）上完成完整验证。提取 760 个唯一文本段落，分 3 批并行翻译，生成双语对照 PDF 和纯中文 PDF，所有页面中文渲染正确，CJK 字体嵌入验证通过。

**English:** This skill has been fully verified on the Rise2040 Vision Report (47 pages, published by AICPA & CIMA). 760 unique text segments were extracted, translated in 3 parallel batches, and both bilingual side-by-side PDF and monolingual Chinese PDF were generated. All pages rendered Chinese correctly with CJK font embedding verified.

---

## 致谢与版权 / Acknowledgments & Copyright

**作者 / Author：** Wang Dongjie 王东杰  
资深复合型战略财务专家 · 上市公司资本运作操盘手 · 集团化财务管控与风险治理高级工程师  
Senior Strategic Finance Expert · Listed Co. Capital Ops Lead · Group Finance Control & Risk Gov. Sr. Engineer  
📧 Wdj_@163.com · 📱 13952453499  

**创建日期 / Created：** 2026-07-22  
**版本 / Version：** 1.0.0  

**中文：** 本 SKILL 基于 [BabelDOC](https://github.com/funstory-ai/BabelDoc) 开源项目构建，结合 LLM 翻译能力实现 PDF 双语翻译自动化。

**English:** This SKILL is built upon the [BabelDOC](https://github.com/funstory-ai/BabelDoc) open-source project, combining LLM translation capabilities to achieve automated PDF bilingual translation.

**技术栈 / Tech Stack：**
- PDF 解析与排版引擎 / PDF parsing & typesetting engine：BabelDOC (funstory-ai)
- 翻译代理 / Translation proxy：自研 OpenAI 兼容 HTTP 代理服务器 / Custom OpenAI-compatible HTTP proxy server
- 字体支持 / Font support：Noto CJK / Source Han Sans
- 验证工具 / Verification tool：pdfplumber

---

*IBCAT SKILL v1.0.0 — (c) 2026 Wang Dongjie 王东杰*  
*IBCAT SKILL v1.0.0 — (c) 2026 Wang Dongjie*
