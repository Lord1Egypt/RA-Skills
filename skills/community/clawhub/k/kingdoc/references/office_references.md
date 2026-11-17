# 文本提取 / 格式转换 API 参考（kdoc.office.*）

> 金山文档独有增强能力，对标腾讯文档**无此功能**。

## kdoc.office.convert — 格式转换

```json
POST /office/convert
{ "file_id": "<id>", "target_format": "pdf" }
```

| 源 \ 目标 | pdf | docx | xlsx | pptx |
|-----------|-----|------|------|------|
| 智能文档/文字 | ✅ | ✅ | — | — |
| 电子表格 | ✅ | — | ✅ | — |
| 演示文稿 | ✅ | — | — | ✅ |

> 大文件（>阈值）自动转异步任务，`kdoc.batch.query` 轮询结果。

## kdoc.office.extract — 纯文本提取

```json
POST /office/extract
{ "file_id": "<id>" }
```
返回文档纯文本，便于检索、摘要、二次处理。

## 本地 OCR（免密钥）

见 `engine/local/ocr.py`：优先调用本机 Tesseract（免费、离线、零密钥），
未安装则降级云端 OCR（需 App Key），都不可用给出安装指引。

```python
from engine.local.ocr import extract_text
print(extract_text("invoice.png"))   # 无需任何 key
```

## 常见错误

| 错误码 | 含义 | 处理 |
|--------|------|------|
| KD015 | 转换失败 | 格式不支持或文件损坏，换源格式 |
| KD008 | 文件过大 | 走异步上传 + 轮询 |
| KD009 | 类型被拦截 | 见 `references/security.md` |

*最后更新：2026-07-12 | v3.0.0*
