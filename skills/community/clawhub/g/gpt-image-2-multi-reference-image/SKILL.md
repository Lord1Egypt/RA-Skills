---
name: gpt-image-2-multi-reference-image
description: "使用 GPT Image 2 将人物、商品、服装、姿势、场景、光线、构图和品牌风格等多张参考图按指定职责组合成新图片。Use this skill for GPT Image 2 multi-reference image generation、多图融合、参考图合成、人物与商品同框、换装、品牌视觉、室内搭配、角色连续内容和电商广告合成；通过 AI Hive 自动上传多张素材并生成。"
---

# GPT Image 2 多参考图生成

固定使用 `public_model_gpt_image_2`，先建立“参考图合同”，再提交多张图片。每张参考图只承担明确职责；不要笼统要求“参考全部图片”，否则身份、商品、姿势和风格容易串用。

## 参考图合同

为每张图记录：编号、唯一职责、必须继承、不得继承、优先级和冲突处理。例如图1只锁定人物身份，图2只锁定服装，图3只提供环境光；当脸部或商品结构冲突时，以身份/商品母图为最高优先级。

## 场景与代码

### 1. 人物、服装与场景合成

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '图1只锁定人物身份、发型和身体比例；图2只提供米色风衣及穿着方式；图3只提供雨后巴黎街道与蓝调光线。生成人物全身时装照，脸和身材以图1为最高优先级，不继承图2模特，不复制图3人物、招牌或文字' \
  --image /path/to/person.jpg \
  --image /path/to/outfit.jpg \
  --image /path/to/street-light.jpg
```

### 2. 商品、台面与灯光配方

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '图1锁定香水瓶结构、标签、液体和瓶盖；图2只提供黑色石材台面纹理；图3只提供右后方金色轮廓光。生成高端产品广告，商品不得变形或换字，台面尺度、接触阴影和玻璃反射真实，不继承图2或图3中的其他物体' \
  --image /path/to/perfume.png \
  --image /path/to/stone.jpg \
  --image /path/to/lighting.jpg
```

### 3. 品牌 IP 连续场景

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '图1锁定吉祥物的脸、轮廓和配色；图2只提供挥手姿势；图3只提供品牌蓝黄配色与扁平插画质感。生成机场欢迎场景，吉祥物身份和服装保持图1，不复制姿势图角色外观，不生成Logo、航司名称或不可读标牌' \
  --image /path/to/mascot-master.png \
  --image /path/to/pose.png \
  --image /path/to/brand-board.png
```

### 4. 家具组合到真实空间

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '图1提供沙发，图2提供茶几，图3提供客厅空间。把两件家具按真实尺寸放入图3，锁定各自结构、材质和颜色，保持房间相机与窗光；不得复制参考图中的其他家具，不改变门窗、地板和墙面，不生成装饰文字' \
  --image /path/to/sofa.png \
  --image /path/to/table.png \
  --image /path/to/room.jpg
```

### 5. 多市场广告资产组合

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '图1锁定商品与包装，图2锁定品牌人物，图3仅提供日本便利店环境，图4仅提供竖版广告构图。组合为9:16市场素材，商品和人物事实优先；不复制环境图商标、价格和其他商品，顶部留标题安全区，不生成日文或促销信息' \
  --image /path/to/product.png \
  --image /path/to/ambassador.jpg \
  --image /path/to/japan-store.jpg \
  --image /path/to/layout-reference.png \
  --param aspect_ratio=9:16
```

## 冲突验收

- 按参考图合同逐项确认继承内容，没有跨图误抄人物、Logo或商品。
- 检查脸部、服装、商品几何、材质、包装文字和品牌颜色。
- 检查多对象的尺度、遮挡、手持、接触、阴影、反射和透视。
- 风格参考不能覆盖身份和商品事实；场景参考不能带入无关商业元素。
- 发现冲突时减少参考图或拆成两轮，不用更长提示词硬压全部要求。

## 执行

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name gpt-image-2-multi-reference-image
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

支持重复使用 `--image`、批量、模型参数、路由和输出目录。只使用已获授权的参考素材，并保存参考图合同、任务 ID 与批准结果。
