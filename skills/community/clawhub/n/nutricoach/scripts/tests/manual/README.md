# Manual Tests

此目录存放手动测试脚本，用于开发调试，非自动化测试套件。

## 测试文件

| 文件 | 用途 |
|------|------|
| `test_barcode_match.py` | 条形码匹配功能测试 |
| `test_ocr_flow.py` | OCR 识别流程测试 |
| `test_silent_scan.py` | 静默扫描功能测试 |

**运行方式：**
```bash
python3 scripts/tests/manual/test_xxx.py
```

**注意：** 这些测试需要手动检查输出结果，非 CI/CD 自动化测试。
