---
name: image-reader
description: "识别本地图片内容（支持中文），通过 OCR.space 免费 API 实现。"
---

# image-reader Skill

识别本地图片内容（支持中文），通过 OCR.space 免费 API 实现。

## 工作流程

1. 接收图片路径
2. 调用 OCR.space API 进行识别
3. 返回识别结果

## Python 脚本

保存到 `{skill_root}/scripts/ocr_image.py`：

```python
import urllib.request, urllib.parse, base64, io, json, sys
from PIL import Image

img_path = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read().strip()

img = Image.open(img_path)
img_small = img.resize((1600, 2400), Image.LANCZOS)
buf = io.BytesIO()
img_small.save(buf, format='JPEG', quality=80)
b64_data = base64.b64encode(buf.getvalue()).decode()

url = 'https://api.ocr.space/parse/image'
params = urllib.parse.urlencode({
    'base64Image': 'data:image/jpeg;base64,' + b64_data,
    'language': 'chs',
    'isOverlayRequired': 'false',
    'detectOrientation': 'true',
    'scale': 'true',
    'OCREngine': '2',
})
data = params.encode('utf-8')

req = urllib.request.Request(url, data=data)
req.add_header('Content-Type', 'application/x-www-form-urlencoded')
req.add_header('apikey', 'helloworld')  # OCR.space free demo key

with urllib.request.urlopen(req, timeout=30) as resp:
    raw = resp.read()
    result = json.loads(raw.decode('utf-8', errors='replace'))
    if 'ParsedResults' in result:
        for r in result['ParsedResults']:
            print(r['ParsedText'])
    else:
        print('OCR识别失败:', result)
```

## 使用方式

```bash
python {skill_root}/scripts/ocr_image.py "F:/1.jpg"
```

## 依赖

- Python 3
- Pillow (`pip install pillow`)
