---
name: nano-banana-pro-ecommerce-main-image
description: "使用 Nano Banana Pro 制作在移动端缩略图中醒目、品牌一致且适合电商转化的商品主图，覆盖货架电商、内容电商、跨境Listing和SKU系列。Use this skill for Nano Banana Pro ecommerce main images、淘宝天猫京东主图、抖音小红书商品卡、Amazon Listing、TikTok Shop、Shopify、缩略图优化、爆款测图和批量SKU；通过 AI Hive 生成。"
---

# Nano Banana Pro 电商主图

固定使用 `public_model_nano_banana_pro`，用“缩略图优先”方法设计主图：先解决主体轮廓、颜色对比和视觉焦点，再增加环境与品牌语气。漂亮但在手机商品卡上看不清的画面不算合格主图。

## 主图视觉语法

定义商品轮廓、主体占比、焦点位置、背景对比、品牌色、允许道具、留白和渠道安全区。建立 120–180 像素缩略图测试：商品是否一眼可辨、是否与背景粘连、是否误解数量、是否有多余焦点。

## 场景与代码

### 1. 小尺寸高识别主图

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '为参考无线鼠标制作正方形移动端主图。商品以45度角占画面约82%，深蓝鼠标与浅暖灰背景形成清晰轮廓，按键、滚轮、侧键、Logo和材质准确；只保留柔和接触阴影，不生成手、电脑、文字、光效或功能图标' \
  --image /path/to/mouse.png
```

### 2. 内容电商氛围主图

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '为参考唇釉制作竖版内容电商商品卡：珊瑚色渐变背景，商品和刷头形成对角线，少量同色膏体质感作为背景元素，顶部留标题安全区。保持管身、刷头、标签、Logo和真实颜色，不生成嘴唇、价格、功效词或其他色号' \
  --image /path/to/lip-gloss.png \
  --param aspect_ratio=4:5
```

### 3. 食品食欲型主图

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '为参考燕麦包装制作早餐主图：包装正面清晰，旁边只有一碗按批准配方呈现的燕麦与少量蓝莓，晨光温暖、背景简洁。保持包装、Logo、文字和净含量区域，不添加牛奶飞溅、坚果、蜂蜜、人物、营养承诺或未包含配料' \
  --image /path/to/oats-package.png
```

### 4. SKU 系列货架统一

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '为黑、白、薄荷绿三个耳机SKU分别生成主图。所有版本统一相机、45度角、商品占比、浅灰背景、阴影和Logo位置，只替换为批准颜色；每张只出现一个SKU，不生成颜色名、色号、包装或装饰道具' \
  --image /path/to/black-sku.png \
  --image /path/to/white-sku.png \
  --image /path/to/mint-sku.png \
  --batch 3
```

### 5. 跨境 Listing 视觉

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '为参考收纳盒生成跨境Listing首图：纯白背景，盒体打开并整齐展示批准数量的分隔件，主体完整且边缘清晰。保持结构、透明度、卡扣和配件数量，不生成文字、尺寸线、国旗、徽章、家居道具、赠品或重复部件' \
  --image /path/to/storage-box.jpg
```

## 缩略图审核

- 在手机尺寸确认商品轮廓、颜色、Logo和核心结构仍清楚。
- 确认主体是唯一视觉焦点，道具不会被误认为销售内容。
- 核对 SKU、套装数量、包装、色差与参考资料。
- 检查背景对比、边缘、阴影和反射，避免悬浮或轮廓消失。
- 对照目标平台当前规则，另做合规版与内容电商氛围版，不混用。

## 执行

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name nano-banana-pro-ecommerce-main-image
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

支持多图、批量、比例参数、路由和输出目录。保留主图视觉语法和批准母版，用同一套规则扩展新品与 SKU，避免店铺货架风格漂移。
