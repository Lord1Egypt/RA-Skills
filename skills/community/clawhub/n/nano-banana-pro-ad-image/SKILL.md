---
name: nano-banana-pro-ad-image
description: "使用 Nano Banana Pro 制作移动端吸睛、品牌可辨并适合多版位适配的广告图片，覆盖信息流、社交广告、商品推广、UGC风格静帧和大促素材。Use this skill for Nano Banana Pro ad images、stop-scroll creative、Meta Ads、TikTok Ads、抖音千川、小红书广告、商品卡、促销图、广告改尺寸和批量创意；通过 AI Hive 生成或编辑。"
---

# Nano Banana Pro 广告图片

固定使用 `public_model_nano_banana_pro`，用“一秒识别”设计广告：先决定用户第一眼看到什么、第二眼读懂什么、最后在哪里行动。主体轮廓、视觉冲突和品牌记忆应在小屏中成立，复杂背景与装饰必须服务同一焦点。

## 视觉节奏卡

确定首焦点、次焦点、品牌线索、动作方向、对比色、标题区、CTA区、平台 UI 避让和禁止元素。先生成无字视觉，再加入批准文案；每个尺寸重新编排焦点，不用机械裁切。

## 场景与代码

### 1. 强轮廓停留型广告

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '为参考运动鞋制作竖版信息流广告：鞋子以低机位大比例悬停在红橙渐变背景前，鞋底轮廓和材质清楚，斜向光带形成速度感，顶部和底部保留标题与CTA安全区。保持鞋型、鞋带、鞋底纹路、Logo与配色，不生成运动员、文字或性能承诺' \
  --image /path/to/shoe.png \
  --param aspect_ratio=9:16
```

### 2. UGC 风格商品静帧

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '生成自然手机拍摄感的护手霜广告静帧：真实居家桌面，一只手把参考商品举到镜头前，环境轻微虚化，光线来自窗户。保持手部自然、包装、Logo、文字和颜色，不磨皮过度，不生成平台界面、评分、价格或使用效果' \
  --image /path/to/hand-cream.png
```

### 3. 动势产品广告

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '为参考气泡饮料制作具有动势的方形广告：罐体居中略倾斜，周围是冰块与气泡形成的环形轨迹，但商品标签、拉环和颜色完全清楚；右上保留短标题区，不生成液体飞溅遮挡、价格、口味文字或健康承诺' \
  --image /path/to/drink-can.png
```

### 4. 大促视觉底版

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '为参考家电制作大促广告底版：高对比深蓝与亮黄几何空间，商品占右侧55%，左侧预留活动机制、价格和CTA区域，角落留品牌标识位。保持商品结构、显示面板、Logo和颜色，不直接生成折扣、价格、日期、礼品或平台Logo' \
  --image /path/to/appliance.png \
  --param aspect_ratio=4:5
```

### 5. 同一创意多版位重构

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '把批准的横版香水广告重构为方形商品卡、4:5信息流和9:16故事三种版位。所有版本保持商品、品牌色、金色光带和高级氛围，重新安排主体与留白以避开平台UI；不裁切瓶身，不生成文案、按钮、价格或新道具' \
  --image /path/to/approved-horizontal-ad.jpg \
  --batch 3
```

## 一秒测试

1. 缩小到手机信息流尺寸，确认商品和品牌色能在一秒内识别。
2. 眯眼检查是否只有一个主焦点，背景与光效不抢商品。
3. 检查商品轮廓、Logo、包装、手部、阴影和接触关系。
4. 在各版位叠加平台 UI 模拟，确认标题、CTA 和商品不被遮挡。
5. 对照批准资料复核文字、优惠、价格和广告承诺后再投放。

## 执行

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name nano-banana-pro-ad-image
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

支持多图、批量、比例参数、路由和输出目录。为每个创意保留主版本、版位重构和表现数据，下一轮优先迭代已验证的视觉结构。
