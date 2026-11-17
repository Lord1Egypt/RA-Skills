---
name: nano-banana-pro-product-image
description: "使用 Nano Banana Pro 制作品牌一致的产品摄影与电商商品套图，包括目录图、质感主视觉、场景图、细节图、套装组合、颜色SKU和渠道上新素材。Use this skill for Nano Banana Pro product images、AI商品摄影、淘宝天猫京东主图、Amazon Listing、Shopify商品图、产品渲染、SKU批量和新品视觉；通过 AI Hive 上传产品参考图并生成。"
---

# Nano Banana Pro 产品图生成

为商品建立“目录母版 + 镜头配方”，固定使用 `public_model_nano_banana_pro`。先锁定产品 DNA，再改变摄影语言；这样可以在白底目录、品牌质感和生活场景之间切换，同时保持商品像同一个真实 SKU。

## 建立产品 DNA

整理轮廓比例、正侧背面、部件连接、材质分区、颜色样本、Logo与标签位置、包装、配件、真实尺度和禁止生成项。为每个镜头记录相机高度、焦段感、商品占比、背景、主光方向、阴影软硬和留白位置。

## 场景与代码

### 1. 三角度目录母版

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '根据参考图建立同一双肩包的正面、45度和侧面三张目录图。锁定包型比例、肩带、拉链、口袋、Logo、缝线、黑色尼龙材质和所有连接点；统一浅灰背景、相机高度、商品占比与柔和阴影，不添加模特、吊牌、文字或配件' \
  --image /path/to/bag-front.jpg \
  --image /path/to/bag-side.jpg \
  --batch 3
```

### 2. 高质感新品主视觉

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '为参考精华瓶制作高端新品主视觉：深琥珀渐变背景，右后方轮廓光穿过玻璃，底部有克制反射，左侧留标题区域。严格保持瓶型、滴管、液体颜色、标签和Logo，不生成水花、植物、功效文字、价格或额外包装' \
  --image /path/to/serum.png
```

### 3. 真实使用与尺度关系

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '把参考便携音箱置于公园野餐毯上，成年人单手从侧面拿起，手指与提手接触自然，产品尺寸真实。保持音箱网布、按钮、提手、Logo和颜色，不改变型号，不生成防水、发光或播放状态，不添加文字' \
  --image /path/to/speaker.png
```

### 4. 套装组合与配件关系

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '制作护发套装组合图，只出现洗发水一瓶、护发素一瓶、发膜一罐和外包装盒。按照参考图保持每件商品的容器、标签、颜色和真实高低比例，采用前二后一的稳定构图；不重复商品、不增加赠品、文字、植物或功效符号' \
  --image /path/to/shampoo.png \
  --image /path/to/conditioner.png \
  --image /path/to/mask.png \
  --image /path/to/box.png
```

### 5. 多渠道上新镜头组

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '基于批准鞋款生成四张上新素材：方形白底主图、竖版生活场景、横版广告留白图、鞋底材质细节。四张保持鞋型、鞋带、鞋底纹路、Logo和配色一致；不出现价格、尺码、模特脸、认证或不存在功能' \
  --image /path/to/approved-shoe.png \
  --batch 4
```

## 摄影验收

- 三视图与不同场景中的轮廓、部件连接、标签和配色一致。
- 材质响应符合光线：玻璃、金属、织物、皮革和塑料不互相混淆。
- 手持、穿戴、摆放与配件组合符合真实尺度和接触关系。
- 套装数量、SKU 和包装内容准确，不制造赠品或功能。
- 渠道图保留足够安全区，并按当前平台规则进行最终排版与审核。

## 执行

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name nano-banana-pro-product-image
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

支持多参考图、批量、参数、路由与输出目录。把批准母版、镜头配方、提示词和任务 ID 一起归档，便于后续 SKU 扩展与复拍。
