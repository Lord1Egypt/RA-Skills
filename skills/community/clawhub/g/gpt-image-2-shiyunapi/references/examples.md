# ShiyunApi GPT-Image-2 使用示例

## 示例1：文生图生成头像

输入：

```yaml
mode: generation
prompt: 一只戴着圆框眼镜的橘猫头像，干净背景，柔和光线，数字插画风格
size: 1024x1024
format: png
n: 1
```

调用：

```bash
python "scripts/generate_image.py" --prompt "一只戴着圆框眼镜的橘猫头像，干净背景，柔和光线，数字插画风格" --size 1024x1024 --format png --output-dir "C:/workspace/output"
```

输出：

```json
{
  "code": 0,
  "files": ["C:/workspace/output/image_1.png"],
  "msg": "图片生成成功"
}
```

## 示例2：文生图生成产品海报

输入：

```yaml
mode: generation
prompt: 高端蓝牙耳机产品海报，深蓝渐变背景，科技感光效，中心产品展示，留出中文标题区域
size: 1024x1024
quality: auto
format: png
```

调用：

```bash
python "scripts/generate_image.py" --prompt "高端蓝牙耳机产品海报，深蓝渐变背景，科技感光效，中心产品展示，留出中文标题区域" --size 1024x1024 --quality auto --format png --output-dir "C:/workspace/output"
```

## 示例3：图片编辑换背景

输入：

```yaml
mode: edit
image: C:/workspace/input/product.png
prompt: 保留产品主体和细节，将背景换成高级灰渐变摄影棚，增加柔和阴影
model: gpt-image-2
size: 1024x1024
n: 1
```

调用：

```bash
python "scripts/edit_image.py" --image "C:/workspace/input/product.png" --prompt "保留产品主体和细节，将背景换成高级灰渐变摄影棚，增加柔和阴影" --model gpt-image-2 --output-dir "C:/workspace/output"
```

输出：

```json
{
  "code": 0,
  "files": ["C:/workspace/output/image_1.png"],
  "msg": "图片编辑成功"
}
```

## 示例4：局部重绘

输入：

```yaml
mode: edit
image: C:/workspace/input/room.png
mask: C:/workspace/input/window_mask.png
prompt: 只修改透明遮罩区域，把窗外景色改成晴朗海景，室内其他区域保持不变
model: gpt-image-2
size: 1024x1024
```

调用：

```bash
python "scripts/edit_image.py" --image "C:/workspace/input/room.png" --mask "C:/workspace/input/window_mask.png" --prompt "只修改透明遮罩区域，把窗外景色改成晴朗海景，室内其他区域保持不变" --model gpt-image-2 --output-dir "C:/workspace/output"
```

## 示例5：多图合成

输入：

```yaml
mode: edit
images:
  - C:/workspace/input/person.png
  - C:/workspace/input/bag.png
prompt: 将人物和包自然合成为一张时尚街拍广告图，保持人物脸部不变，包在人物右手
model: gpt-image-2
size: 1024x1536
```

调用：

```bash
python "scripts/edit_image.py" --image "C:/workspace/input/person.png" --image "C:/workspace/input/bag.png" --prompt "将人物和包自然合成为一张时尚街拍广告图，保持人物脸部不变，包在人物右手" --model gpt-image-2 --size 1024x1536 --output-dir "C:/workspace/output"
```

## 示例6：只返回原始响应

输入：

```yaml
mode: generation_or_edit
prompt: 一张儿童绘本风格的海底城市插画
model_field: auto
```

输出：

```json
{
  "code": 202,
  "raw_response": "C:/workspace/output/response.json",
  "msg": "接口返回未识别为图片，已保存原始响应以便排查"
}
```
