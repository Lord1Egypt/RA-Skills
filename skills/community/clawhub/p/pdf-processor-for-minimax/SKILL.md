---
name: "pdf-processor"
description: "使用MiniMax模型从PDF文件中提取文本和图片。当用户需要处理PDF内容、从PDF中提取信息或分析PDF文档时调用此技能。"
---

# PDF 处理器

本技能使用MiniMax AI模型处理PDF文件并提取内容（文本和图片）。

## 何时调用

在以下情况下调用此技能：
- 用户想要从PDF文件中提取文本
- 用户想要从PDF中提取并分析图片
- 用户要求处理或分析PDF文档
- 用户提到PDF内容提取
- 用户需要将PDF内容转换为结构化数据

## 前置要求

使用此技能前，请确保：

1. **MiniMax API密钥**：设置环境变量 `MINIMAX_API_KEY` 或 `MINIMAX_GROUP_ID` 和 `MINIMAX_API_KEY`
2. **必需的Python包**：如果尚未安装，请安装以下包：
   ```bash
   pip install pymupdf  # 用于PDF处理
   pip install minimax-client  # MiniMax SDK
   pip install pillow  # 用于图片处理
   ```

## 使用说明

### 步骤1：读取PDF文件

使用PyMuPDF（fitz）打开并读取PDF：

```python
import fitz  # PyMuPDF

def extract_pdf_content(pdf_path):
    """从PDF中提取文本和图片。"""
    doc = fitz.open(pdf_path)
    content = {
        'text': [],
        'images': []
    }
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        
        # 提取文本
        text = page.get_text()
        if text.strip():
            content['text'].append({
                'page': page_num + 1,
                'text': text
            })
        
        # 提取图片
        images = page.get_images()
        for img_index, img in enumerate(images):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            # 保存或处理图片
            content['images'].append({
                'page': page_num + 1,
                'index': img_index,
                'bytes': image_bytes,
                'ext': base_image["ext"]
            })
    
    doc.close()
    return content
```

### 步骤2：使用MiniMax模型进行分析

使用MiniMax的视觉模型分析提取的内容：

```python
import base64
from minimax import MiniMax

# 初始化MiniMax客户端
client = MiniMax(
    api_key=os.environ.get("MINIMAX_API_KEY"),
    group_id=os.environ.get("MINIMAX_GROUP_ID")
)

def analyze_with_minimax(text=None, image_bytes=None, prompt=None):
    """使用MiniMax模型分析内容。"""
    
    messages = []
    
    # 准备内容
    content = []
    
    if text:
        content.append({"type": "text", "text": text})
    
    if image_bytes:
        # 将图片转换为base64
        base64_image = base64.b64encode(image_bytes).decode('utf-8')
        content.append({
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
            }
        })
    
    if prompt:
        content.insert(0, {"type": "text", "text": prompt})
    
    messages.append({
        "role": "user",
        "content": content
    })
    
    # 调用MiniMax API
    response = client.chat.completions.create(
        model="abab6.5s-chat",  # 或适当的视觉模型
        messages=messages
    )
    
    return response.choices[0].message.content
```

### 步骤3：完整工作流程

结合提取和分析：

```python
def process_pdf(pdf_path, analysis_prompt="请分析这个PDF的内容"):
    """完整的PDF处理工作流程。"""
    
    # 步骤1：提取内容
    content = extract_pdf_content(pdf_path)
    
    results = {
        'text_analysis': [],
        'image_analysis': []
    }
    
    # 步骤2：分析文本
    for text_item in content['text']:
        analysis = analyze_with_minimax(
            text=text_item['text'],
            prompt=f"{analysis_prompt}\n\n文本内容：\n{text_item['text']}"
        )
        results['text_analysis'].append({
            'page': text_item['page'],
            'analysis': analysis
        })
    
    # 步骤3：分析图片
    for img_item in content['images']:
        analysis = analyze_with_minimax(
            image_bytes=img_item['bytes'],
            prompt="请描述这张图片的内容"
        )
        results['image_analysis'].append({
            'page': img_item['page'],
            'analysis': analysis
        })
    
    return results
```

## 使用示例

```python
# 处理PDF文件
pdf_path = "/path/to/document.pdf"
results = process_pdf(pdf_path, "请总结这个文档的主要内容")

# 打印结果
for item in results['text_analysis']:
    print(f"第{item['page']}页：{item['analysis']}")

for item in results['image_analysis']:
    print(f"第{item['page']}页图片：{item['analysis']}")
```

## 重要注意事项

1. **API限制**：MiniMax API可能有速率限制。对于大型PDF，请实现适当的延迟。
2. **图片大小**：大型图片在发送到API之前可能需要调整大小。
3. **成本**：处理包含大量图片的大型文档时，请注意API成本。
4. **错误处理**：始终为API调用和文件操作实现适当的错误处理。
5. **隐私**：确保根据隐私要求处理敏感的PDF内容。

## 可选模型

MiniMax提供不同的模型。根据您的需求选择：

- `abab6.5s-chat`：快速、高效，适合文本分析
- `abab6.5g-chat`：更强大的复杂推理能力
- 视觉模型：用于图片分析（查看MiniMax文档获取当前视觉模型名称）

## 故障排除

1. **API密钥问题**：验证您的MiniMax API密钥设置正确
2. **图片格式**：确保图片为支持的格式（JPEG、PNG）
3. **内存问题**：对于大型PDF，分批处理页面
4. **超时错误**：增加超时设置或减少内容大小
