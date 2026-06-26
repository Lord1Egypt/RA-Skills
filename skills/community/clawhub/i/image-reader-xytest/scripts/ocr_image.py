import urllib.request, urllib.parse, base64, io, json, sys, os
from PIL import Image

img_path = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read().strip()
if not img_path:
    print("Usage: python ocr_image.py <image_path>")
    sys.exit(1)

img_name = os.path.splitext(os.path.basename(img_path))[0]
output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f'{img_name}_ocr.txt')

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
req.add_header('apikey', 'helloworld')

with urllib.request.urlopen(req, timeout=30) as resp:
    raw = resp.read()
    result = json.loads(raw.decode('utf-8', errors='replace'))
    if 'ParsedResults' in result:
        with open(output_path, 'w', encoding='utf-8') as f:
            for r in result['ParsedResults']:
                f.write(r['ParsedText'])
        print(f'[OCR识别完成，保存到 {output_path}]')
    else:
        print('OCR识别失败:', result)
