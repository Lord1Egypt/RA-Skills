# 环境安装与检测

> 本文档覆盖 BM25 检索环境、Python 依赖、脚本文件等运行前提。
> 在 Phase 0 环境检查或 Stage 0 初始化时按需查阅。

---

## 1. Python 环境与依赖

```bash
# 必须（BM25 检索核心）
pip install bm25s

# 文件格式支持（按需安装）
pip install pdfminer.six    # PDF 文字提取
pip install python-pptx     # PPTX 提取
pip install pandas          # Excel 读取
pip install Pillow          # 图片处理

# 可选
pip install easyocr         # OCR（中文）
pip install paddleocr       # 百度 OCR（中文效果最好）
pip install python-docx     # DOCX 提取
```

---

## 2. 脚本文件

本 Skill 依赖两个 Python 脚本，包含在 skill 文件夹内：

| 脚本 | 位置 | 用途 | 调用阶段 |
|------|------|------|---------|
| `build_kb_index.py` | `.agents/skills/knowledge-retrieval/scripts/build_kb_index.py` | 全量扫描原始文件 → 建 BM25 索引 | Stage 0 Step 3、Phase 0.3 |
| `search_kb.py` | `.agents/skills/knowledge-retrieval/scripts/search_kb.py` | LLM 扩展搜索词 → BM25 搜索 → 分数排序候选文件 | Phase A 通道② |

> **工作目录说明：** 调用以上脚本时，确保工作目录为 workspace 根目录。
> 脚本使用相对于 workspace 的路径 `knowledge-base/` 来定位项目目录。

---

## 3. 前置检查清单（AI 自查）

搜索前快速自查：

- [ ] `pip list` 中是否有 `bm25s`（或 `import bm25s` 是否成功）？
- [ ] `.agents/skills/knowledge-retrieval/scripts/build_kb_index.py`、`.agents/skills/knowledge-retrieval/scripts/search_kb.py` 是否存在？
- [ ] 如果以上任一缺失 → 先补齐再开始搜索流程
- [ ] 无 BM25 环境或缺失脚本 → 自动降级为纯 AI 搜索模式（不报错，能力受限）

---

## 4. 索引存储位置

```
knowledge-base/<项目名>/.bm25_index/
└── index/
    ├── corpus.jsonl    ← 文件文本内容（用于搜索时匹配）
    └── metadata.json   ← 文件元数据
```
