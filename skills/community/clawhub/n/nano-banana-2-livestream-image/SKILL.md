---
name: nano-banana-2-livestream-image
description: "使用 Nano Banana 2 制作直播预热封面、直播间背景、产品讲解卡、机制占位卡和回放封面，并围绕实时 UI 与主播位置预留安全区。Use this skill for Nano Banana 2 livestream image、直播带货图片、直播间背景、直播封面、商品讲解卡、抖音直播、快手直播、淘宝直播、视频号直播、小红书直播、电商直播素材；通过 AI Hive 生成，不表示平台官方合作。"
---

# Nano Banana 2 直播带货图片

固定使用 `public_model_nano_banana_2`。直播素材要在运动画面、评论区、商品卡、主播和压缩画质中保持清楚。先画直播界面安全区，再分别制作预热、场内和回放资产；价格、库存、优惠与时间由直播系统或设计工具实时排版。

## 直播画布图

记录平台比例、主播站位、商品展示区、评论区、商品卡、顶部状态栏、字幕区和切换动画区域。为每张素材指定显示时长、观看距离和唯一任务，避免把背景、讲解卡和促销机制做成同一张拥挤海报。

## 场景与代码

### 1. 直播预热封面

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-skincare-set.png \
  --prompt '制作4:5护肤套装直播预热封面底图：保持三个商品的包装、标签、颜色和数量，商品位于下方三分之二，顶部留直播主题与时间区域，暖白棚拍背景；不生成主播脸、文字、价格、折扣、功效、平台Logo或第四件商品' \
  --param aspect_ratio=4:5
```

### 2. 直播间竖版背景

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '生成9:16家居用品直播间虚拟背景：米白墙面、浅木层板和柔和暖光，中央下半部留主播与桌面区域，左上留品牌标识区，右侧避开评论与商品卡；不生成文字、Logo、人物、商品、门窗强透视或复杂小装饰' \
  --param aspect_ratio=9:16
```

### 3. 商品讲解卡

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-pan.png \
  --prompt '生成平底锅直播讲解卡底图：左侧保留参考商品完整外观，结构、手柄、涂层颜色和Logo不变；右侧预留三个短卖点单元格，底部避开商品购买卡，不生成文字、价格、认证、耐用次数、主播或不存在的配件' \
  --param aspect_ratio=16:9
```

### 4. 优惠机制占位卡

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '生成直播优惠机制卡的无字背景：深红与米白几何层级，中央留一行机制标题，下面留三格规则区域，右下留二维码或按钮占位，但不生成任何文字、数字、价格、券额、二维码、平台Logo或商品；用于后期填入实时批准信息' \
  --param aspect_ratio=16:9
```

### 5. 回放与切片封面

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-demo-frame.jpg \
  --prompt '基于已授权直播演示帧制作回放封面：保持主播身份、商品、动作和现场事实，适度整理背景并增强主体分离，左上留六字以内标题区，右下避开时长标签；不改变表情、产品数量、演示结果，不生成文字、价格或平台Logo' \
  --param aspect_ratio=16:9
```

## 上线检查

1. 将素材叠加真实直播 UI，关键内容不被评论、商品卡或字幕遮挡。
2. 低码率与小屏预览中，商品轮廓和唯一信息仍清楚。
3. 价格、优惠、库存和时间不固化在生成图中，除非已批准并人工校对。
4. 主播、商品、演示和场地保持真实，不制造使用结果。
5. 保存平台画布图、素材用途、提示词、任务 ID 和过期时间。

## 助手边界

工具固定使用 Nano Banana 2 图片模型，可从文字开始或上传用户点名的参考图片，提交任务并保存结果。认证请求只发送到 `https://ai-hive.iclip.cn/api`；不允许自定义地址，也不提供聊天、视频、钱包或账户功能。

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name nano-banana-2-livestream-image
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

直播平台规则与促销信息变化快，上线前必须由运营核对实时政策和批准口径。
