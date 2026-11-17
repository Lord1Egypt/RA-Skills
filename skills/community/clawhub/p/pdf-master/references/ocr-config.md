# OCR 配置指南

> OCR 任务调参、识别效果不达标排障时阅读。脚本入口：`scripts/pdf_ocr.py`。

## 目录
- [默认配置](#默认配置开箱即用)
- [场景调参](#场景调参)
- [速度与精度](#速度-vs-精度)
- [识别率排障决策树](#识别率排障决策树)
- [低置信区处理](#低置信区处理)

---

## 默认配置（开箱即用）

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `OCR_ENGINE` | `paddleocr` | 中文场景首选 |
| `DETECTION` | `ch_PP-OCRv4_det` | 文字区域检测模型 |
| `RECOGNITION` | `ch_PP-OCRv4_rec` | 文字识别模型 |
| `LANGUAGE` | `ch+en` | 中英混合 |
| `DESKEW` | `true` | 自动纠偏 |
| `DENOISE` | `true` | 去噪 |
| `BINARIZATION` | `adaptive` | 自适应二值化 |
| `DPI` | `300` | 页面渲染分辨率（<150dpi 原图先超分） |

## 场景调参

### 高质量扫描件（清晰、无倾斜）
```json
{ "deskew": false, "denoise": false, "binarization": "otsu" }
```

### 手机拍照 / 有倾斜 / 阴影
```json
{ "deskew": true, "denoise": true, "binarization": "adaptive", "contrast_enhance": true, "perspective_correct": true }
```

### 手写体 / 低质量
```json
{ "engine": "paddleocr", "model": "ch_PP-OCRv4_rec_mobile", "handwriting": true, "denoise": true, "super_resolution": true }
```

### 纯英文文档
```json
{ "engine": "tesseract", "language": "eng", "oem": 3, "psm": 6 }
```

### 表格密集文档
```json
{ "table_mode": true, "structure_model": "SLANet", "line_detect": "morphology" }
```

## 速度 vs 精度

| 模式 | 适用场景 | 速度 |
|------|---------|------|
| `fast` | 预览/草稿 | 3-5 秒/页 |
| `balanced` | 日常使用（默认） | 8-12 秒/页 |
| `accurate` | 关键文档/出版 | 15-25 秒/页 |

> 单批 ≤50 页，超出自动分批并批间报进度。

## 识别率排障决策树

识别结果不达标时按序排查，每步验证后再进下一步：

1. **原图质量**：渲染 dpi 是否 ≥300？→ 提高渲染 dpi 重跑
2. **预处理是否误伤**：清晰件开了 denoise/binarization 反而掉字 → 换"高质量扫描件"配置
3. **语言配置**：纯英文用了中文模型 → 切 Tesseract eng；日文/韩文 → 切对应语言包
4. **引擎切换**：PaddleOCR 异常 → 降级 Tesseract（告知中文识别率下降）；反之亦然
5. **手写体**：印刷体模型识别手写 → 切手写模型，并告知手写识别率上限（~85%）
6. **特殊区域**：公章覆盖、底纹、水印区 → 标记低置信区（见下）
7. **仍不达标**：如实报告"该页识别置信度低"，附原图请用户人工核对，**不得硬凑结果**

## 低置信区处理

- 以下区域自动标记「低置信区」：公章覆盖区、手写批注区、底纹/水印重叠区、分辨率 <150dpi 区
- 交付时附《低置信区清单》：页码 + 区域截图 + 识别结果 + "请人工核对"提示
- 金额/日期/编号类字段落在低置信区 → 升级为必核项，置顶提醒
