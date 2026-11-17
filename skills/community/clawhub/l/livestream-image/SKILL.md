---
name: livestream-image
description: "使用 Nano Banana 2 设计直播带货视觉套件，包括直播间背景、商品讲解卡、利益点板、倒计时占位和应急静态画面，并优先保证手机端可读性。Use this skill for 直播带货图片、直播间背景、直播贴片、商品讲解卡、直播商品图、价格牌底图、抖音快手淘宝直播视频号 TikTok Shop Amazon Live 视觉；通过 AI Hive 生成。"
---

# 直播带货图片

本 Skill 固定调用 `public_model_nano_banana_2`。直播视觉要在小屏、压缩和主播遮挡条件下仍然清楚，因此先画“主播安全区、商品展示区、文字区、互动区”，再做风格。价格、库存、倒计时与优惠券是实时信息，只生成容器，不把可能变化的数字烘焙进图片。

## 直播间版式图

确定横竖屏比例、主播站位、摄像头裁切、商品台、评论遮挡、平台按钮区域、标题字数和可替换模块。同一场直播的背景、卡片与贴片共用色彩和形状语言，但信息密度不同。

## 五件直播视觉

### 1. 竖屏直播间背景

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate   --image ./brand-palette.png   --prompt '生成9:16美妆直播间背景：品牌米白与珊瑚色，中央偏下为主播和商品台留出干净区域，顶部留主题区，两侧用柔和弧形层架增加空间；不生成文字、价格、品牌Logo、人物、商品或平台按钮'   --param aspect_ratio=9:16
```

### 2. 商品讲解卡

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate   --image ./approved-blender.png   --prompt '制作9:16直播商品讲解卡底图：料理机杯体、刀座、旋钮、颜色和Logo准确，产品置于下半部，上半部留三条短卖点，底部留实时价格与按钮区域；不生成文字、功率、容量、折扣、赠品或食材飞溅'   --param aspect_ratio=9:16
```

### 3. 可见结构利益点板

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate   --image ./approved-suitcase-open.png   --prompt '生成1:1直播利益点板：保持行李箱外形、轮子、拉杆、颜色和Logo，打开状态只突出实际分区、束带和网袋，右侧留解释文字区；不生成容量倍数、承重、人物、旅行地点、奖章或额外夹层'   --param aspect_ratio=1:1
```

### 4. 倒计时与优惠占位贴片

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate   --prompt '设计透明感强的16:9直播促销贴片底稿：左侧为短活动名，中央为可替换倒计时，右侧为优惠券按钮，使用红橙高对比但不过度遮挡画面；所有区域保持空白，不生成数字、价格、文字、Logo或平台标识'   --param aspect_ratio=16:9
```

### 5. 断流应急静态画面

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate   --image ./approved-store-visual.png   --prompt '生成9:16直播应急静态画面：延续参考店铺的品牌色、灯光和图形语言，中间留“稍后回来”信息区，下方留客服提示区，背景简洁且手机端可读；不生成具体文字、时间承诺、二维码、人物、商品价格或平台Logo'   --param aspect_ratio=9:16
```

## 开播前走查

用目标手机预览并模拟主播遮挡、评论区与平台按钮；核对商品结构和标配；将价格、库存、时间、优惠与二维码留给直播软件实时叠加；确认背景不过度抢主播，所有关键区域在安全框内。

## 安全调用边界

程序接受文字和用户主动提供的参考图，模型锁定为 Nano Banana 2。认证通信仅连接 `https://ai-hive.iclip.cn/api`；不会调用聊天、视频、用户资料或余额接口。

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name livestream-image
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

平台名称仅说明直播渠道；价格、优惠、库存和倒计时必须由现场人员确认。
