---
name: nano-banana-pro-product-detail-page
description: "使用 Nano Banana Pro 为商品详情页建立连贯的滚动视觉叙事，生成首屏氛围、问题场景、产品揭示、材质证明、使用体验和收尾转化模块。Use this skill for Nano Banana Pro product detail pages、淘宝天猫详情页、Amazon A+、Shopify PDP、详情页长图、品牌故事、卖点图、场景图和新品落地页；通过 AI Hive 生成一致的系列图片。"
---

# Nano Banana Pro 商品详情页

固定调用 `public_model_nano_banana_pro`，用“开场—需求—揭示—证明—体验—收尾”的滚动节奏构建详情页。先批准一张视觉母版，再让所有模块共享商品、人物、光线、色板和镜头语言，避免滚动时像不同品牌拼接。

## 叙事母版

定义目标人群、购买时刻、情绪起点、核心转变、商品 DNA、品牌色、主光方向、背景材质、人物身份和禁用表达。为每个模块记录它在叙事中的作用，不重复同一构图或同一句卖点。

## 模块与代码

### 1. 氛围开场

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '为参考香氛蜡烛生成详情页开场：黄昏室内，蜡烛置于深木桌面，暖光形成安静的空间层次，左侧大面积留白作为品牌标题区。锁定杯体、蜡面、标签、Logo和颜色，不生成文案、火焰夸张、花材、功效或价格' \
  --image /path/to/candle.png \
  --param aspect_ratio=16:9
```

### 2. 用户需求场景

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '展示通勤者在拥挤地铁中整理背包的真实瞬间，画面重点是物品难找与空间拥挤，右侧留问题文案区。使用与后续模块同一人物和深蓝背包，不夸张表情，不生成文字、品牌、危险动作或竞争商品' \
  --image /path/to/person-master.jpg \
  --image /path/to/backpack.png
```

### 3. 产品解决方案揭示

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '延续上一模块人物、服装、地铁光线和深蓝背包，展示背包打开后的分区收纳，电脑、耳机、充电器和水杯各在真实隔层。保持包型、拉链、Logo与物品数量，左上留卖点区，不生成标签文字、额外口袋或新配件' \
  --image /path/to/person-master.jpg \
  --image /path/to/backpack-open.jpg
```

### 4. 材质证明镜头

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '生成同一背包的三联材质细节：尼龙织纹、加固缝线、防护底部。统一冷灰背景与侧光，每个细节具有真实尺度并保留结构关系；不生成水珠、防水文字、测试图标、认证或不存在材料层' \
  --image /path/to/backpack-detail.jpg \
  --batch 3
```

### 5. 使用体验与收尾

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '详情页收尾场景：同一人物背着同一深蓝背包走出地铁进入清晨街道，动作轻松自然，商品轮廓和Logo清楚，右侧保留一句总结与CTA区域。保持人物、服装、背包和品牌色连续，不生成文字、按钮、价格、光环或夸张速度感' \
  --image /path/to/person-master.jpg \
  --image /path/to/backpack.png \
  --param aspect_ratio=16:9
```

## 连贯性检查

1. 快速滚动所有模块，确认色板、光线、人物、商品和品牌气质属于同一故事。
2. 检查相邻模块是否完成“提出问题—给出证据”的推进，而非重复美照。
3. 对照商品母图检查结构、材质、Logo、配件和颜色没有漂移。
4. 文案区足够清晰，移动端主体与细节无需放大即可理解。
5. 价格、尺寸、功效与条款使用批准文案后期排版并逐项审核。

## 执行

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name nano-banana-pro-product-detail-page
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

支持多图、批量、比例、参数、路由和输出目录。先锁定叙事母版再生产全页，最后按渠道组装桌面与移动端版本，不直接把桌面长图缩小交付。
