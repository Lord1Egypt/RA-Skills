---
name: gpt-image-2-product-image
description: "使用 GPT Image 2 生成可上架的产品图与商品摄影套图，包括白底主图、场景图、材质细节、尺寸留白、使用步骤、包装清单和SKU系列。Use this skill for GPT Image 2 product photography、电商商品图、淘宝天猫京东主图、Amazon Listing、Shopify PDP、商品套图、新品上架和批量SKU；通过 AI Hive 基于产品参考图生成。"
---

# GPT Image 2 产品图生成

先建立“商品事实表”，再生成一套回答购买问题的图片。固定调用 `public_model_gpt_image_2`。不要用一张漂亮图承担全部销售任务；主图回答“是什么”，细节图回答“做得怎样”，场景图回答“如何使用”。

## 商品事实表

记录商品名称、正侧背面、颜色、材质、Logo、包装文字、尺寸、配件数量、开关状态、可动结构和禁止误导内容。指定一张批准母图作为几何与颜色基准；文字、尺寸和认证必须来自批准资料。

## 场景与代码

### 1. 白底上架主图

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '基于参考图生成正面略俯视的白底商品主图。锁定吹风机轮廓、出风口、按钮、线缆、Logo、颜色和表面材质；商品完整、居中、占画面约80%，保留自然接触阴影，不添加手、道具、文字、包装、赠品或不存在配件' \
  --image /path/to/product-master.png
```

### 2. 材质与工艺细节

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '为同一腕表生成三张微距细节：表盘刻度与指针、表壳拉丝边缘、表带连接结构。保持型号、颜色、Logo和真实部件一致，光线突出材质但不过度锐化；不创造刻度、按钮、宝石、认证或防水文字' \
  --image /path/to/watch-front.png \
  --image /path/to/watch-side.png \
  --batch 3
```

### 3. 展示真实尺度的使用场景

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '把参考台灯置于小型书桌的真实阅读场景，灯体尺寸与常见笔记本电脑、书本和成人手臂比例合理；保持灯具结构、颜色、按钮与线缆，光照范围自然。不改变产品、不生成触控界面、文字或未提供功能' \
  --image /path/to/lamp.png
```

### 4. 包装清单平铺图

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '根据参考资料制作开箱平铺图，只展示一台主机、一个电源适配器、一根USB-C线、一本说明书和原包装盒。每件物品完整分离、排列整齐、数量准确；保持包装与Logo，不添加赠品、标签、价格或无法确认的配件' \
  --image /path/to/product.png \
  --image /path/to/package-and-parts.jpg
```

### 5. SKU 颜色系列

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '以批准的黑色水杯为结构母版，生成雾白、森林绿、珊瑚橙三个SKU目录图。只改变杯身颜色，锁定尺寸、杯盖、吸管、Logo位置、相机、背景、光线和阴影；每张只出现一个商品，不生成颜色名、色号或装饰图案' \
  --image /path/to/approved-black-sku.png \
  --batch 3
```

## 上架前检查

- 商品结构、按钮、接口、Logo、包装文字、颜色与批准资料一致。
- 配件、数量、尺寸关系和使用状态没有虚构。
- 材质、边缘、透明部件、反射和接触阴影自然。
- 同一套图的相机高度、背景、色温和商品比例稳定。
- 平台白底、文字、安全区等规则以当前官方规范为准。

## 执行

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name gpt-image-2-product-image
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

支持多张产品参考图、`--batch`、模型参数、路由和输出目录。对医疗、美妆功效、食品成分、认证或精确尺寸等高风险信息，使用已批准资料后期排版并人工审核。
