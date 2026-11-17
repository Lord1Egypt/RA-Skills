---
name: nano-banana-pro-livestream-image
description: "使用 Nano Banana Pro 建立主播、商品与直播间风格一致的直播视觉套件，覆盖开播封面、主播主视觉、场景背景、品类转场、商品卡和多平台直播封面。Use this skill for Nano Banana Pro livestream images、直播带货视觉、抖音淘宝快手视频号直播、TikTok Live、主播与商品合成、直播背景、直播封面和导播素材；通过 AI Hive 生成。"
---

# Nano Banana Pro 直播带货图片

固定使用 `public_model_nano_banana_pro`。先锁定主播身份、主推商品和直播间视觉代码，再生成一套能在镜头、转场和商品讲解中保持连续的素材。把背景、覆盖层和商品卡按图层职责分开，避免直播画面过满。

## 直播视觉代码

记录主播参考图、服装版本、商品母图、主辅色、背景材质、灯光、边框、圆角、标题区、价格区、互动 UI 避让和各品类的识别色。每个资产标记“背景层、人物层、商品层或信息层”，只生成所需图层。

## 场景与代码

### 1. 主播与主推商品主视觉

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '图1锁定主播身份、发型和服装，图2锁定主推吹风机。生成直播主视觉：主播自然侧身展示商品，手指与握柄关系真实，珊瑚红与奶油白品牌背景，顶部留直播主题区。不得改变脸、服装、商品结构、Logo或颜色，不生成价格、销量和平台UI' \
  --image /path/to/host.jpg \
  --image /path/to/hair-dryer.png \
  --param aspect_ratio=4:5
```

### 2. 可叠加的直播背景层

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '生成9:16直播背景层，只包含珊瑚红到奶油白渐变、右后方柔和弧形灯带和两侧克制陈列架；中央下方完全留空给主播和桌面，左上留标题区，右侧避开评论UI。不要生成主播、商品、文字、Logo或按钮' \
  --param aspect_ratio=9:16
```

### 3. 品类切换转场

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '基于同一直播视觉代码生成护肤、彩妆、个护三个品类转场底图。统一弧形灯带、圆角框和奶油白基底，只用淡蓝、玫红、薄荷绿区分品类；中央保留品类标题区，不生成文字、商品、人物、价格或装饰图标' \
  --image /path/to/live-style-board.png \
  --batch 3
```

### 4. 竖版商品置顶卡

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '为参考精华液生成可叠加的竖版商品卡：透明/纯色简洁背景，商品位于上半区，下面依次留商品名、两条卖点、价格和按钮区域；商品瓶型、滴管、标签、Logo与液体颜色准确，不生成文字、价格、功效、认证或多余包装' \
  --image /path/to/serum.png \
  --param aspect_ratio=3:4
```

### 5. 多平台封面重构

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '把批准主视觉重构为方形预约封面、4:5预热海报和9:16直播封面。三版保持主播、商品、珊瑚红奶油白色板、弧形灯带与视觉焦点，重新安排留白以避开各平台UI；不裁切脸和商品，不生成文字、价格或按钮' \
  --image /path/to/approved-live-keyart.jpg \
  --batch 3
```

## 连续性检查

1. 主播脸部、发型、服装与商品在封面、转场和商品卡中保持一致。
2. 背景层、人物层、商品层和信息层职责清楚，可被导播安全叠加。
3. 主辅色、弧形灯带、圆角和品类色遵循同一视觉代码。
4. 在实际直播 UI 模拟中检查人物、商品、评论、购物车和信息区不冲突。
5. 文案、价格、库存与促销由运营真源填充，不让模型猜测。

## 执行

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name nano-banana-pro-livestream-image
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

支持多图、批量、比例、参数、路由和输出目录。每次更换主播服装、主推商品或活动主题时创建新视觉版本，不覆盖仍在使用的直播资产。
