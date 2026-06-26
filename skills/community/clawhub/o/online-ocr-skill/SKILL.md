---
name: online-ocr
description: 在线OCR图片识别技能，使用免费的OCR.space API，无需安装Tesseract
metadata: {"clawdbot":{"emoji":"🌐","requires":{"bins":["python"]}}}
---

# Online OCR Skill

在线OCR图片识别技能，使用免费的OCR.space API，无需安装Tesseract OCR引擎。

## 特点

- ✅ **无需安装Tesseract** - 使用在线API
- ✅ **支持多种语言** - 包括中文、英文等
- ✅ **免费使用** - OCR.space免费API（每月1000次请求）
- ✅ **简单易用** - 只需Python和requests库
- ✅ **支持多种图片格式** - PNG, JPG, JPEG, PDF等

## 安装依赖

```bash
pip install requests pillow
```

## 使用方法

### Python脚本

```python
import requests
import base64
from PIL import Image
import io

class OnlineOCR:
    def __init__(self, api_key='helloworld'):  # 免费API密钥
        self.api_key = api_key
        self.api_url = 'https://api.ocr.space/parse/image'
    
    def ocr_from_file(self, image_path, language='chs'):
        """
        从图片文件识别文字
        
        参数:
        - image_path: 图片文件路径
        - language: 语言代码
            chs - 中文简体
            eng - 英文
            jpn - 日文
            kor - 韩文
            etc.
        
        返回: 识别结果文本
        """
        with open(image_path, 'rb') as f:
            img_data = f.read()
        
        return self.ocr_from_bytes(img_data, language)
    
    def ocr_from_bytes(self, image_bytes, language='chs'):
        """从字节数据识别文字"""
        # 将图片转换为base64
        img_base64 = base64.b64encode(image_bytes).decode('utf-8')
        
        # 准备请求数据
        payload = {
            'base64Image': f'data:image/png;base64,{img_base64}',
            'language': language,
            'isOverlayRequired': False,
            'apikey': self.api_key,
            'OCREngine': 2  # 使用引擎2（更准确）
        }
        
        # 发送请求
        response = requests.post(self.api_url, data=payload)
        
        if response.status_code == 200:
            result = response.json()
            if result['IsErroredOnProcessing']:
                raise Exception(f"OCR处理错误: {result['ErrorMessage']}")
            
            # 提取文本
            parsed_results = result.get('ParsedResults', [])
            if parsed_results:
                return parsed_results[0].get('ParsedText', '')
            return ''
        else:
            raise Exception(f"API请求失败: {response.status_code}")
    
    def ocr_from_url(self, image_url, language='chs'):
        """从URL识别图片文字"""
        payload = {
            'url': image_url,
            'language': language,
            'isOverlayRequired': False,
            'apikey': self.api_key,
            'OCREngine': 2
        }
        
        response = requests.post(self.api_url, data=payload)
        
        if response.status_code == 200:
            result = response.json()
            if result['IsErroredOnProcessing']:
                raise Exception(f"OCR处理错误: {result['ErrorMessage']}")
            
            parsed_results = result.get('ParsedResults', [])
            if parsed_results:
                return parsed_results[0].get('ParsedText', '')
            return ''
        else:
            raise Exception(f"API请求失败: {response.status_code}")

# 使用示例
if __name__ == "__main__":
    ocr = OnlineOCR()
    
    # 从文件识别
    text = ocr.ocr_from_file('test.png', language='chs')
    print(text)
    
    # 从URL识别
    # text = ocr.ocr_from_url('https://example.com/image.png', language='eng')
```

### 命令行工具

创建 `online_ocr_cli.py`：

```python
#!/usr/bin/env python3
import argparse
import os
import sys
from online_ocr import OnlineOCR

def main():
    parser = argparse.ArgumentParser(description='在线OCR图片识别工具')
    parser.add_argument('image', help='图片文件路径或URL')
    parser.add_argument('-l', '--lang', default='chs', 
                       help='语言代码 (默认: chs)')
    parser.add_argument('-o', '--output', help='输出文件路径')
    parser.add_argument('--api-key', default='helloworld',
                       help='OCR.space API密钥 (默认: helloworld)')
    
    args = parser.parse_args()
    
    # 创建OCR实例
    ocr = OnlineOCR(api_key=args.api_key)
    
    try:
        # 判断输入是文件还是URL
        if args.image.startswith('http://') or args.image.startswith('https://'):
            text = ocr.ocr_from_url(args.image, args.lang)
        else:
            if not os.path.exists(args.image):
                print(f"错误: 文件不存在 - {args.image}")
                return
            
            text = ocr.ocr_from_file(args.image, args.lang)
        
        # 输出结果
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(text)
            print(f"结果已保存到: {args.output}")
        else:
            print("\n=== 识别结果 ===")
            print(text)
            
    except Exception as e:
        print(f"错误: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

## 支持的语言

OCR.space支持多种语言，常用语言代码：

- `chs` - 中文简体
- `cht` - 中文繁体
- `eng` - 英文
- `jpn` - 日文
- `kor` - 韩文
- `fre` - 法文
- `ger` - 德文
- `spa` - 西班牙文
- `rus` - 俄文
- `ita` - 意大利文

完整列表参考：https://ocr.space/ocrapi

## API密钥

默认使用免费API密钥 `helloworld`，限制：
- 每月1000次请求
- 文件大小限制：1MB
- 不支持PDF文件

如需更多功能，可注册获取自己的API密钥：
1. 访问 https://ocr.space/ocrapi
2. 注册账号
3. 获取免费API密钥

## 示例

### 示例1：识别中文图片
```python
from online_ocr import OnlineOCR

ocr = OnlineOCR()
text = ocr.ocr_from_file('chinese_text.png', language='chs')
print(text)
```

### 示例2：识别英文图片
```python
text = ocr.ocr_from_file('english_text.png', language='eng')
print(text)
```

### 示例3：批量处理
```python
import os
from online_ocr import OnlineOCR

ocr = OnlineOCR()

def batch_ocr(image_folder, output_folder, lang='chs'):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for filename in os.listdir(image_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(image_folder, filename)
            output_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.txt")
            
            try:
                text = ocr.ocr_from_file(image_path, lang)
                
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(text)
                
                print(f"已处理: {filename}")
            except Exception as e:
                print(f"处理失败 {filename}: {str(e)}")
```

## 集成到OpenClaw

### 作为工具使用
```python
# 在OpenClaw技能中集成在线OCR功能
def online_ocr_tool(image_path, language='chs'):
    """在线OCR工具函数"""
    try:
        from online_ocr import OnlineOCR
        
        ocr = OnlineOCR()
        text = ocr.ocr_from_file(image_path, language)
        
        return {
            "success": True,
            "text": text,
            "language": language,
            "source": "OCR.space API"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "source": "OCR.space API"
        }
```

## 故障排除

### 常见问题

1. **API请求限制**
   ```
   错误: 超过API限制
   ```
   解决方案：等待下个月或注册获取自己的API密钥

2. **图片太大**
   ```
   错误: 文件大小超过限制
   ```
   解决方案：压缩图片或减小尺寸

3. **网络问题**
   ```
   错误: 连接超时
   ```
   解决方案：检查网络连接，或使用代理

### 性能优化

1. **图片预处理**
   ```python
   from PIL import Image
   
   def preprocess_image(image_path, max_size=800):
       """预处理图片以优化OCR"""
       img = Image.open(image_path)
       
       # 调整大小
       if max(img.size) > max_size:
           ratio = max_size / max(img.size)
           new_size = tuple(int(dim * ratio) for dim in img.size)
           img = img.resize(new_size, Image.Resampling.LANCZOS)
       
       # 转换为RGB（如果不是）
       if img.mode != 'RGB':
           img = img.convert('RGB')
       
       # 保存临时文件
       temp_path = 'temp_processed.jpg'
       img.save(temp_path, 'JPEG', quality=85)
       
       return temp_path
   ```

2. **使用本地缓存**
   ```python
   import hashlib
   import json
   import os
   
   class CachedOCR(OnlineOCR):
       def __init__(self, cache_dir='.ocr_cache', **kwargs):
           super().__init__(**kwargs)
           self.cache_dir = cache_dir
           if not os.path.exists(cache_dir):
               os.makedirs(cache_dir)
       
       def ocr_from_file(self, image_path, language='chs'):
           # 生成缓存键
           with open(image_path, 'rb') as f:
               file_hash = hashlib.md5(f.read()).hexdigest()
           
           cache_key = f"{file_hash}_{language}"
           cache_file = os.path.join(self.cache_dir, f"{cache_key}.json")
           
           # 检查缓存
           if os.path.exists(cache_file):
               with open(cache_file, 'r', encoding='utf-8') as f:
                   return json.load(f)['text']
           
           # 调用API
           text = super().ocr_from_file(image_path, language)
           
           # 保存缓存
           with open(cache_file, 'w', encoding='utf-8') as f:
               json.dump({'text': text, 'language': language}, f)
           
           return text
   ```

## 许可证

MIT License

## 支持

- OCR.space API文档：https://ocr.space/ocrapi
- 问题反馈：创建GitHub Issue
- 功能建议：欢迎贡献代码