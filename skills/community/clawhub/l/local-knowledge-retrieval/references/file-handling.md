# 文件类型处理细则

> 本文档覆盖各种文件格式的读取策略、工具选择、缓存规则。
> 在 Phase B 读取候选文件时按需查阅。

---

## 1. Markdown / 纯文本（.md / .txt）

**工具：** `read` / `Select-String`（Mac: `grep`）
**策略：** 直接全文或部分读取。通过关键词定位相关段落，只读匹配行及其前后文。
**缓存：** 不需要（秒读）。

## 2. PDF

### 2.1 文字版 PDF

**工具：** `pdfminer.six`（Python）
**策略：**
```python
from pdfminer.high_level import extract_text
text = extract_text("file.pdf")
```
→ 在提取结果上做关键词搜索 → 提取相关段落返回
**缓存：** 不需要（< 3 秒/份）。

### 2.2 扫描件/图片版 PDF

**判定：** 先尝试 pdfminer 提取 → 提取结果 < 100 字则判定为扫描件
**工具：** PaddleOCR（优先，中文效果好）→ 备选 EasyOCR
**策略：** OCR → 写入缓存
```python
# 写入 cache/<文件名>.txt
```
**缓存：** ✅ 需要（首次 10-30 秒，缓存后秒回）。
**注意：** 中文准确率约 85-90%，数字和英文更好。

## 3. PPTX（PowerPoint）

**工具：** `python-pptx` + 缓存
**策略：**
1. 递归遍历所有 slide 及 slide 内所有形状（含 GroupShape 组合图形内的子形状）→ 提取 text_frame + notes_slide + 标题
2. 合并为平铺文本 → 写入缓存
3. 在缓存文本上搜索
4. 遇到「如下图所示」等表述 → 转图片处理流程（见第 5 节）
**性能：** 50 页 PPT ≈ 10-20 秒（首次），缓存后秒回。
**局限：** 图表（Chart）、SmartArt、嵌入图片中的文字无法提取。
**缓存：** ✅ 需要（首次慢格式）。

## 4. XLSX（Excel）

**工具：** `pandas`
**策略：**
```python
import pandas as pd
df = pd.read_excel("file.xlsx", nrows=10)  # 仅预览表头+前10行
```
→ 按关键词匹配表头 → 筛选相关行
**注意：** 严格限制 `nrows=10`，绝不全表加载。
**缓存：** 不需要。

## 5. 图片处理

### 触发条件
- Phase B 定位到的段落中出现「如下图所示」「见图X」等线索
- 独立图片文件落入候选列表

### 操作（仅具备视觉能力的 Agent）

> ⚠️ 图片分析需要当前模型支持多模态视觉。如果不支持，跳过图片并如实告知用户无法解读，基于可提取的文字继续回答。
> 纯文字搜索不会触发此流程。
> 
> ⚠️ Image analysis requires the active model to support multimodal vision.
> If it doesn't, skip the image, report honestly, and continue with
> extractable text. Text-only search never triggers this path.

1. 从 PDF/PPTX 中提取该页的图片资源，或直接读取图片文件
2. 执行视觉分析（仅当前模型支持多模态视觉时执行）
3. 解读结果写入 `cache/<文件名>.img-<页码>.txt`
4. 后续搜到同一页 → 直接读缓存

### 不触发条件
- 装饰性图片（封面图、图标、背景）

### 不具备视觉能力的 Agent
- 如实标注「该文件包含图片，无法自动解读」
- 继续回答基于可提取的文字内容

## 6. 缓存策略

### 核心规则：缓存只服务于慢操作

| 格式 | 是否缓存 | 原因 |
|------|---------|------|
| .md / .txt | ❌ 不缓存 | 秒读，无需转换 |
| .xlsx | ❌ 不缓存 | 只读前 10 行，秒级 |
| .pdf（文字版，≤ 15 页） | ❌ 不缓存 | pdfminer < 3 秒 |
| .pdf（文字版，> 15 页） | ✅ 缓存 | 长文档提取成本高，BM25 建索引和 Phase B 都走缓存 |
| .pdf（扫描件） | ✅ 缓存 | OCR 10-30 秒 |
| .pptx | ✅ 缓存 | 50 页 10-20 秒 |
| .docx（如安装） | ✅ 可选缓存 | 格式转换不稳定 |
| 嵌入图片解析 | ✅ 缓存 | 仅当前模型支持时执行 |
| 独立图片描述 | ✅ 缓存 | 仅当前模型支持时执行，desc 可被搜索命中 |

### 缓存路径
`knowledge-base/<项目名>/cache/`

### 有效判定
原始文件 `lastModified` <= 缓存文件 `createdAt` → 有效
原始文件 `lastModified` > 缓存文件 `createdAt` → 过期，下次读取时重建

### 缓存文件名规则
- 文本提取缓存：`<文件名>.txt`
- 图片解读缓存：`<文件名>.img-<页码>.txt`
- 图片描述缓存：`<文件名>.desc.txt`

