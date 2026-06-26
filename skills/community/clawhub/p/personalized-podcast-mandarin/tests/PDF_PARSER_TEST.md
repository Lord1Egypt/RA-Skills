# PDF Parser 测试文档

## 测试目标
验证 `src/pdf_parser.py` 能够正确提取PDF文本内容。

## 测试方法

### 测试1：纯文本PDF
**操作步骤**:
1. 在下方 `test_pdf_paths` 列表中添加一个纯文本PDF文件路径
2. 运行测试: `pytest tests/test_pdf_parser.py -v`

**预期结果**:
- 成功解析PDF
- 提取的文本与原文一致
- 保留段落结构

**待输入测试文件路径**:
```python
test_pdf_paths = [
    # 请在此处添加PDF文件路径
    # 示例: "d:/documents/test_article.pdf",
]
```

---

### 测试2：学术论文PDF
**操作步骤**:
1. 添加学术论文PDF路径
2. 运行测试

**预期结果**:
- 正确提取标题、摘要、正文
- 处理多栏布局

**待输入测试文件路径**:
```python
academic_pdf_paths = [
    # 请在此处添加学术论文PDF路径
]
```

---

### 测试3：扫描版PDF
**操作步骤**:
1. 添加扫描版PDF路径（图片型PDF）
2. 运行测试

**预期结果**:
- 提示文本提取失败（当前不支持OCR）
- 或提取出空字符串

**待输入测试文件路径**:
```python
scanned_pdf_paths = [
    # 请在此处添加扫描版PDF路径
]
```

---

### 测试4：二进制流解析
**操作步骤**:
1. 准备PDF文件
2. 以二进制模式读取后传入 `parse_bytes()` 方法

**预期结果**:
- 正确解析并返回文本

---

### 测试5：错误处理
**操作步骤**:
1. 添加不存在的PDF路径
2. 运行测试

**预期结果**:
- 抛出 `PDFParserError` 异常
- 异常信息包含失败原因

---

## 运行测试命令

```bash
cd d:/vscode/AI-podcast/ai-podcast-dual-host
pytest tests/test_pdf_parser.py -v
```

## 测试报告模板

测试完成后，请填写以下结果：

| PDF文件 | 页数 | 提取字数 | 状态 | 备注 |
|---------|------|----------|------|------|
| | | | | |
| | | | | |
