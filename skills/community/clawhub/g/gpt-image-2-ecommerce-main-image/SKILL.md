---
name: gpt-image-2-ecommerce-main-image
description: "使用 GPT Image 2 制作电商主图、商品首图和 Listing Hero Image，兼顾商品事实、平台合规、缩略图可读性、卖点表达与A/B测图。Use this skill for GPT Image 2 ecommerce main image、淘宝天猫京东拼多多抖店主图、Amazon亚马逊主图、Shopify PDP首图、商品卡、白底图、测款测图和新品上架；通过 AI Hive 基于商品参考图生成。"
---

# GPT Image 2 电商主图

固定调用 `public_model_gpt_image_2`。先建立“渠道规则卡 + 商品事实卡”，再设计主图。主图的首要任务是让用户快速识别正确商品；装饰、文字和场景不得遮盖或歪曲商品事实。

## 两张卡片

- **渠道规则卡**：平台、版位、比例、背景、文字、边框、道具、Logo和安全区要求。规则会变化，提交前读取当前官方说明。
- **商品事实卡**：结构、颜色、材质、包装文字、数量、配件、真实尺寸、允许状态、批准卖点和禁止承诺。

## 场景与代码

### 1. 合规白底首图

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '根据参考图生成正方形白底商品首图：同一空气炸锅正面略俯视，完整居中，占画面约85%。锁定机身、炸篮、旋钮、显示区域、Logo、颜色和材质，保留自然接触阴影；不添加食物、餐具、文字、徽章、边框、赠品或功能状态' \
  --image /path/to/product.png \
  --param aspect_ratio=1:1
```

### 2. 单一卖点主图

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '为参考旅行箱制作“前开盖结构”主图：商品占主体，前盖打开到参考资料允许角度，内部结构与配件准确，右侧保留一处短卖点排版区。保持箱体、轮子、拉杆、Logo和颜色，不生成文案、尺寸、认证、人物或不存在隔层' \
  --image /path/to/suitcase-closed.png \
  --image /path/to/suitcase-open.jpg
```

### 3. 套装数量主图

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '制作厨房刀具套装主图，只出现参考资料中的一把主厨刀、一把面包刀、一把水果刀、一把剪刀和一个刀架。每件商品完整可辨、数量准确、比例真实，采用稳定组合构图；不重复刀具、不添加砧板、食材、赠品、文字或价格' \
  --image /path/to/set-reference.jpg
```

### 4. 缩略图 A/B 测试

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '基于同一参考面霜生成三个主图测试方向：A纯白目录图，B浅粉几何台面，C轻微水面反射。三版商品结构、标签、Logo、颜色、相机和占比一致，只改变背景策略；不生成文案、花朵、水花、功效符号或额外包装' \
  --image /path/to/cream.png \
  --batch 3
```

### 5. 大促视觉预留版

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '为批准商品生成节日促销主图底版：深红背景与克制金色光带，商品位于右下三分之一，左上保留价格、活动和按钮排版区。锁定商品、包装与Logo，不直接生成折扣、价格、日期、平台Logo、礼盒或赠品' \
  --image /path/to/approved-product.png
```

## 主图验收

1. 缩小到手机商品卡尺寸，确认商品仍能立即识别。
2. 对照事实卡检查型号、颜色、数量、配件、包装和使用状态。
3. 确认装饰不伪装成配件，场景不制造未经证实的功能或尺度。
4. 检查边缘、透明材质、反射、阴影、手持和接触关系。
5. 按当前渠道规则复核背景、文字、安全区和禁止元素，再进入测试。

## 执行

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name gpt-image-2-ecommerce-main-image
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

支持多参考图、批量、参数、路由和输出目录。A/B 测试一次只改变一个假设，并记录曝光、点击和转化数据，避免把多项变化混在同一结论中。
