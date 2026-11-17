---
name: nano-banana-pro-multi-reference-image
description: "使用 Nano Banana Pro 将多张人物、商品、构图、材质或风格参考图组合成一张受控图片，并明确每张参考图的职责。Use this skill for Nano Banana Pro多参考图生成、人物加商品、角色与场景合成、参考构图、风格迁移、品牌视觉统一、多商品组合和一致性创作；通过 AI Hive 上传多图并生成。"
---

# Nano Banana Pro 多参考图生成

多参考图不是“把所有图混在一起”。先为每张图分配单一职责，再声明冲突时的优先级。固定使用 `public_model_nano_banana_pro`。

## 参考图角色表

在提示词中逐张说明：

- 图 1：主体身份或商品结构。
- 图 2：姿势、构图或相机。
- 图 3：服装、材质或配色。
- 图 4：背景、灯光或品牌风格。

优先级通常为“事实与身份 > 结构与文字 > 姿势构图 > 风格气氛”。参考冲突时不要让模型猜，明确舍弃哪一项。

## 场景与代码

### 1. 人物、服装与场景组合

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '图1只锁定人物身份、脸部和发型；图2只提供米白风衣的版型与材质；图3只提供城市雨夜场景和灯光。生成人物穿该风衣站在雨夜街口的写实照片，身份优先于服装参考，服装必须顺应人物姿势，不复制图2模特，不复制图3人物' \
  --image /path/to/person.png \
  --image /path/to/coat.png \
  --image /path/to/rainy-city.jpg
```

### 2. 商品、构图与品牌风格

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '图1锁定商品结构、包装、Logo与颜色；图2只提供左商品右留白的构图；图3只提供品牌的深蓝、银色与轮廓光语言。生成原创商业KV，商品事实最高优先级，不复制图2产品和文字，不生成价格或新Logo' \
  --image /path/to/product.png \
  --image /path/to/layout.jpg \
  --image /path/to/brand-style.jpg
```

### 3. 多商品真实组合

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '三张参考图分别提供三个真实商品。生成一张套装俯拍图，每件商品保持结构、包装、Logo、颜色和比例关系，互不融合、每件只出现一次，背景统一，阴影方向一致，不添加赠品或套装文字' \
  --image /path/to/item-a.png \
  --image /path/to/item-b.png \
  --image /path/to/item-c.png
```

### 4. 角色与姿势参考

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '图1锁定角色五官、发型、年龄与服装；图2只提供奔跑姿势和相机角度；图3只提供科幻走廊环境。保持图1角色身份与服装最高优先级，采用图2动作，置于图3气氛中，不复制参考图中的其他人物' \
  --image /path/to/character.png \
  --image /path/to/pose.jpg \
  --image /path/to/environment.jpg
```

### 5. 冲突参考诊断

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '图1为商品事实源，图2仅提供材质灯光，图3仅提供构图。若图2或图3中的产品与图1冲突，全部忽略其产品外观；最终商品必须与图1一致，只吸收非冲突的灯光和布局，不生成参考图文字' \
  --image /path/to/source-of-truth.png \
  --image /path/to/lighting.jpg \
  --image /path/to/composition.jpg
```

## 多参考验收

- 每张参考图的职责可追溯到最终画面。
- 主体身份、商品结构和文字事实没有被风格图覆盖。
- 未将不同人物、产品或配件错误融合。
- 姿势、透视、光线与接触阴影一致。
- 没有复制参考图中无授权文字、Logo或人物。
- 记录参考图顺序、角色与优先级，便于复现。

## 执行

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name nano-banana-pro-multi-reference-image
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

使用多个 `--image` 按提示词顺序上传。生成前先去除用途重复或互相矛盾的参考图。
