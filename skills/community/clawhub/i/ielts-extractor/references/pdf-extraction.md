# PDF 提取指南

## 定位文章和题目

### 页码查找
```python
with pdfplumber.open(pdf_path) as pdf:
    for i, page in enumerate(pdf.pages):
        text = page.extract_text()
        if "Test 2" in text and "READING PASSAGE 1" in text:
            print(f"Page {i+1}")
```

### 常见页码(Cambridge 4)
- Test 2: P43(P1), P47(P2), P50(P3)
- Test 3: P66(P1), P72(P2), P75(P3)

## 提取文章

### 关键规则:多页连续提取
```python
# 错误 ❌
text = pdf.pages[65].extract_text()

# 正确 ✅
text = ""
for i in range(65, 69):  # 连续多页
    text += pdf.pages[i].extract_text()
```

### 两栏布局
```python
def extract_twocolumn(page):
    chars = page.chars
    mid = page.width / 2
    left = sorted([c for c in chars if c['x0'] < mid], key=lambda x: (x['top'], x['x0']))
    right = sorted([c for c in chars if c['x0'] >= mid], key=lambda x: (x['top'], x['x0']))
    return ''.join([c['text'] for c in left]) + ''.join([c['text'] for c in right])
```

## 表格题截图

```python
import fitz  # PyMuPDF
doc = fitz.open(pdf_path)
page = doc.load_page(48)  # 0-indexed
pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
pix.save("public/images/xxx.png")
```

## 数据文件位置

```
ielts-tracker/
├── data/
│   └── tests/
│       └── cambridge-{4,5,6}/
│           └── test-{1,2,3,4}/
│               └── test.json
└── ielts-app/
    └── public/
        └── images/
```
