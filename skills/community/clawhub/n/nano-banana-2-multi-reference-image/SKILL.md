---
name: nano-banana-2-multi-reference-image
description: "使用 Nano Banana 2 将两张或更多授权参考图按身份、结构、服装、材质、构图、色板和风格分工，生成来源清晰、冲突可控的新图片。Use this skill for Nano Banana 2 multi-reference image、多参考图生成、多图融合、角色一致性、商品参考、姿势参考、风格参考、材质板、场景合成、品牌视觉、AI绘画和商业图片；通过 AI Hive 上传明确指定的图片，不等于简单拼图。"
---

# Nano Banana 2 多参考图生成

固定使用 `public_model_nano_banana_2`，至少提供两张图片。先给每张参考图分配唯一职责，再定义冲突优先级；不要用“参考全部图片”把身份、构图和风格混成不可验收的要求。

## 参考角色表

为每张图记录文件名、允许提取内容、必须忽略内容和优先级。推荐顺序：真实身份或商品事实 > 几何结构 > 姿势与布局 > 材质 > 光线与色板 > 装饰风格。两个来源冲突时，明确哪一个胜出；未授权人物、品牌和艺术作品不得作为参考。

## 场景与代码

### 1. 人物身份 + 服装 + 姿势

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-face.png ./approved-outfit.png ./pose-reference.png \
  --prompt '参考图1只负责已授权人物的脸型、五官、肤色和发型；参考图2只负责深蓝夹克、白衬衫与配饰；参考图3只负责站姿和手臂动作，忽略其中人物身份与服装。生成中性灰摄影棚全身照，人物年龄表现与身体比例自然，不带入任一参考图的背景、文字或Logo' \
  --param aspect_ratio=3:4
```

### 2. 商品事实 + 材质方向 + 场景

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-watch.png ./brushed-metal-board.jpg ./stone-set.jpg \
  --prompt '图1锁定手表表盘、表冠、表带、Logo和尺寸比例；图2只提供拉丝金属反光特征；图3只提供浅色石材台面与侧光构图。生成高端静物图，不改变表盘文字、指针数量、功能、颜色或标配内容，不复制图2和图3中的其他物品' \
  --param aspect_ratio=4:5
```

### 3. 室内结构 + 材料板 + 灯光

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-room.jpg ./oak-and-linen-board.jpg ./evening-light.jpg \
  --prompt '图1锁定房间墙体、门窗、梁柱、相机位置和家具尺度；图2只用于白橡木、亚麻与米色墙面的材质色板；图3只用于傍晚暖光方向与明暗层次。生成改造概念图，不移动门窗、不扩大面积、不复制参考灯具或添加结构' \
  --param aspect_ratio=16:9
```

### 4. 食品包装 + 摆盘 + 色板

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-snack-pack.png ./plate-layout.jpg ./palette.jpg \
  --prompt '图1锁定零食包装形状、Logo、标签版式和真实颜色；图2只参考俯拍摆盘关系；图3只参考橙色、奶油白和深棕色板。生成1:1上新图，包装必须完整可读，不复制图2食物品种，不生成新文字、价格、营养承诺或额外包装' \
  --param aspect_ratio=1:1
```

### 5. 系列视觉的共同锚点

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-bottle.png ./campaign-layout.png ./approved-palette.png \
  --prompt '图1锁定饮料瓶与标签；图2只提供中央主体、弧形背景和右上留白的版式；图3只提供珊瑚红、浅粉与深蓝色板。生成三张系列候选，分别表现清晨、午后、夜晚，但商品、版式骨架和色板保持一致，不出现文字、人物、平台Logo或功效暗示' \
  --batch 3 \
  --param aspect_ratio=4:5
```

## 冲突验收

1. 逐张确认只提取了角色表允许的属性。
2. 身份、商品几何、Logo和文字不受风格参考污染。
3. 姿势、布局或灯光参考没有偷偷带入其主体。
4. 新画面具备统一透视、光源、尺度和接触关系，不像剪贴拼图。
5. 保存参考角色表、来源授权、提示词、任务 ID 与批准结果。

## 助手边界

程序要求至少两张参考图片，只上传命令中明确列出的文件，固定调用 Nano Banana 2 图片模型并保存结果。所有携带 Key 的请求固定发往 `https://ai-hive.iclip.cn/api`，不接受自定义地址。`init` 可用 `0600` 权限保存本地 Key；没有聊天、视频、账户或余额接口。

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name nano-banana-2-multi-reference-image
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

不得通过多图融合伪造人物同框、官方合作、新闻现场、检测结果或商品功能。
