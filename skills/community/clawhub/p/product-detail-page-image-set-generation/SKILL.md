---
name: product-detail-page-image-set-generation
description: "使用 Nano Banana Pro 把商品资料转换成完整详情页套图镜头清单，并逐模块生成首屏、利益、结构、步骤、尺寸、场景和装箱图片。Use this skill for 商品详情页套图一键生成、PDP image set、淘宝天猫京东抖店详情页、Amazon A+、Shopify 商品页、卖点图、结构图、步骤图、规格图和电商长图；通过 AI Hive 生成。"
---

# 商品详情页套图一键生成

固定使用 `public_model_nano_banana_pro`。“一键”指从一份批准资料建立整套镜头清单，不是一次生成一张不可编辑的长图。逐模块创建图片，锁定商品母版，再在设计工具中排版文字和组合页面。

## 镜头清单

为每个模块写编号、购买问题、视觉答案、参考图、商品锁定项、证据、比例、留白和前后衔接。常见套图包括：首屏定位、核心利益、结构证据、使用步骤、尺寸适配、生活场景、装箱清单和限制说明。

## 场景与代码

### 1. 首屏 Hero

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-mini-printer.png \
  --prompt '生成迷你打印机详情页首屏：保持机身、出纸口、按钮、颜色和Logo，置于明亮学习桌，产品位于右侧，左侧留标题和一句定位区域；不生成文字、打印速度、学生脸、手机界面或不存在的配件' \
  --param aspect_ratio=16:9
```

### 2. 结构证据镜头

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-suitcase.png \
  --prompt '生成行李箱结构模块：主图保持箱体、轮子、拉杆、锁、颜色和Logo，周围放大四个已存在局部并留标签空位；不生成文字、耐摔测试、容量数字、内部未知结构或额外配件' \
  --param aspect_ratio=16:9
```

### 3. 使用步骤镜头

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-label-maker.png \
  --prompt '生成标签机三步使用底图：装入批准标签卷、合上上盖、取出打印标签，产品结构、按钮、颜色和相机角度一致，三格各留步骤文字区；不生成文字内容、手机品牌、速度数字、额外按钮或错误操作' \
  --param aspect_ratio=16:9
```

### 4. 尺寸适配镜头

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-side-table.png \
  --prompt '生成边几尺寸适配底图：保持桌面、支架、颜色、材质和Logo，放在沙发旁并预留宽高尺寸线与单位区域，尺度关系真实；不生成具体数字、文字、承重、人物、第二张桌子或改变家具比例' \
  --param aspect_ratio=16:9
```

### 5. 装箱清单镜头

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-mic-kit.png \
  --prompt '生成麦克风套装装箱图：只展示确认包含的麦克风、桌面支架、防喷罩、数据线和说明书，各一次、俯拍排列、右侧留清单区；不生成文字、声卡、耳机、赠品、认证或第二套商品' \
  --param aspect_ratio=16:9
```

## 套图一致性

1. 所有模块使用同一商品母版，颜色、结构、Logo和配件不漂移。
2. 每张只回答镜头清单中的一个问题，避免重复卖点。
3. 数字、认证、比较和功效与批准证据一一对应。
4. 模块间色板、镜头和留白连续，移动端裁切逐张验收。
5. 归档母版、镜头清单、任务 ID、批准图片和最终页面。

## 助手边界

程序可从文字或用户指定参考图生成，固定使用 Nano Banana Pro 图片模型并保存结果。带 Key 请求仅发往 `https://ai-hive.iclip.cn/api`，不允许自定义接口。无聊天、视频、账户或余额功能。

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name product-detail-page-image-set-generation
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

“一键”不省略事实、证据和人工排版审核；人物、规格、装箱和效果必须可追溯。
