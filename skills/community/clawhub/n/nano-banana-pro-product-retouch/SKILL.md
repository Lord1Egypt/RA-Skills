---
name: nano-banana-pro-product-retouch
description: "使用 Nano Banana Pro 精修商品照片，清理灰尘与划痕、校正颜色和白平衡、控制反光、修复背景与阴影，同时锁定商品几何和包装事实。Use this skill for Nano Banana Pro商品精修、电商修图、产品摄影后期、去灰尘、控制反光、颜色校准、包装修复、批量SKU统一和商业图片优化；通过 AI Hive 生成。"
---

# Nano Banana Pro 商品精修

商品精修的目标是提高照片质量，不是重新设计商品。固定使用 `public_model_nano_banana_pro`；所有结构、材料、颜色、标签、包装文字和真实瑕疵边界必须由原图控制。

## 精修等级

- **清洁级**：去除灰尘、临时指纹、传感器污点与背景杂物。
- **摄影级**：校正白平衡、曝光、反射、边缘和接触阴影。
- **电商统一级**：统一 SKU 角度、尺度、背景和色彩基准。
- **限制**：不能重画结构、隐藏应披露损伤、修正产品设计或伪造材质。

## 场景与代码

### 1. 灰尘与指纹清理

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '精修商品照片：保留产品结构、材质纹理、边缘、Logo、包装文字和真实颜色；只去除表面灰尘、临时指纹和背景小污点，保持真实反光与接触阴影，不磨平纹理、不改变标签和接口' \
  --image /path/to/raw-product.jpg
```

### 2. 高反光产品控制

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '精修不锈钢商品：保持几何、金属拉丝、刻度和Logo准确，降低遮挡细节的过曝反射，建立连续柔和高光与真实暗部，去除摄影棚杂乱倒影，但不把金属变成塑料或哑光' \
  --image /path/to/reflective-product.jpg
```

### 3. 商品颜色校准

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '根据图2色卡校正图1商品颜色与白平衡。图1锁定结构、材质、包装与文字，图2只提供颜色基准；保持阴影和质感自然，不改变商品颜色设计，不让背景色污染产品' \
  --image /path/to/product.jpg \
  --image /path/to/color-reference.jpg
```

### 4. 白底与接触阴影统一

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '将商品照片整理为干净浅色背景，保持商品外观、相机角度和比例；修正抠图毛边，重建与原光源一致的柔和接触阴影，保留透明/半透明和细小结构，不生成悬浮感、文字或新配件' \
  --image /path/to/product-cutout.png
```

### 5. SKU 批量一致性

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '以参考母版为摄影标准，精修当前SKU：匹配相机角度、商品占比、背景亮度、阴影柔度和色彩基准；保持当前SKU真实颜色、包装、结构和Logo，不复制母版SKU的颜色或标签' \
  --image /path/to/current-sku.jpg \
  --image /path/to/approved-master.jpg
```

## 精修验收

- 原图与精修图叠加比较，轮廓和结构不漂移。
- 材质纹理、透明度、反光和边缘仍然真实。
- Logo、标签、包装文字、接口和配件准确。
- 颜色在统一显示与参考基准下复核。
- 应披露的损伤、磨损或商品差异没有被隐藏。
- 批量 SKU 的角度与背景统一，但每个 SKU 事实保留。

## 执行

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name nano-banana-pro-product-retouch
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

使用 `--image` 提供原图和可选摄影标准，必要时用 `--batch` 比较精修强度。保留原始文件供回滚。
