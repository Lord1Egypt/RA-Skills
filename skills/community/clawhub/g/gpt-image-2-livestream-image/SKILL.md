---
name: gpt-image-2-livestream-image
description: "使用 GPT Image 2 制作直播带货全流程图片，包括预约预热海报、直播封面、直播间背景、商品讲解卡、福利节点图、导播转场和回放封面。Use this skill for GPT Image 2 livestream commerce images、抖音直播、淘宝直播、快手直播、视频号、小红书直播、TikTok Live、Amazon Live、直播预告、商品卡和直播运营物料；通过 AI Hive 生成。"
---

# GPT Image 2 直播带货图片

固定调用 `public_model_gpt_image_2`。先从直播排期与商品清单建立“场次真源”，再制作开播前、直播中和回放后的图片。模型负责人物、商品、背景和版式留白；时间、价格、库存、优惠门槛和口播承诺必须从场次真源后期排版。

## 场次真源

记录场次名称、平台、日期与时区、主播、商品/SKU、出场顺序、批准卖点、价格与优惠、赠品、库存口径、客服说明、平台 UI 安全区和禁用词。每张物料关联一个场次与商品节点，避免复用旧价格或旧赠品。

## 场景与代码

### 1. 预约预热海报

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '制作美妆直播预约海报底图：图1锁定主播身份与服装，图2锁定三款批准商品；主播位于右侧，商品组合位于左下，顶部保留主题、日期和预约按钮区。保持人物、商品、包装与Logo，不生成时间、价格、折扣、赠品或平台界面' \
  --image /path/to/host.jpg \
  --image /path/to/products.jpg \
  --param aspect_ratio=4:5
```

### 2. 直播间背景

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '生成竖版家居直播间背景：温暖木色与浅米色，中央下方留主播和桌面区域，左上留商品讲解卡，右侧避开评论与互动UI，背景包含克制陈列架但无具体商品。不要生成主播、文字、价格、Logo或密集装饰' \
  --param aspect_ratio=9:16
```

### 3. 商品讲解卡

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '为参考料理机制作直播讲解卡底图：左侧商品45度角完整展示，右侧设置三个卖点占位和一个规格占位，底部留商品编号区。保持杯体、刀座、按钮、配件、Logo和颜色，不生成卖点文字、参数、价格、认证或未提供配件' \
  --image /path/to/blender-and-parts.jpg \
  --param aspect_ratio=16:9
```

### 4. 福利节点转场图

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '制作直播福利节点转场底图：高对比品牌红与金色几何光效，中间保留“福利名称”大标题区，下方保留优惠条件与时间区，右下展示参考商品。保持商品与Logo，不生成折扣数字、倒计时、价格、赠品、平台Logo或夸张金币' \
  --image /path/to/featured-product.png \
  --param aspect_ratio=16:9
```

### 5. 回放与切片封面

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '为直播回放制作竖版封面：保持主播身份、服装和主推商品，选用自然讲解姿势，商品位于下方且不被手遮挡；上方留回放主题，下方留商品名称区，避开平台UI。不生成直播时间、价格、销量、评分或“最低价”承诺' \
  --image /path/to/host.jpg \
  --image /path/to/featured-product.png \
  --param aspect_ratio=9:16
```

## 上线检查

- 逐项对照场次真源核对日期、时区、SKU、价格、门槛、赠品和库存口径。
- 主播身份、商品结构、包装、Logo与颜色在所有物料中一致。
- 在平台 UI 模拟图上检查评论区、按钮、购物车、标题和人物安全区。
- 商品卡只展示本节点实际销售内容，不把道具误作赠品或配件。
- 场次结束后归档或标记过期物料，避免旧优惠再次上线。

## 执行

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name gpt-image-2-livestream-image
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

支持多参考图、批量、比例、参数、路由与输出目录。各平台直播广告与促销规则会变化，发布前按当前政策审核。
