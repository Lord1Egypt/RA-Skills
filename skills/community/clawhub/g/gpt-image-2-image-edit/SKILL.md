---
name: gpt-image-2-image-edit
description: "使用 GPT Image 2 对现有图片进行精确、可复核的编辑，包括删除或替换物体、局部修复、改颜色材质、人物与服装调整、扩图改版和广告版本适配。Use this skill for GPT Image 2 image editing、AI修图、局部重绘、对象替换、改色、改材质、扩图、商品编辑、人物编辑和批量版本；通过 AI Hive 上传原图并下载结果。"
---

# GPT Image 2 图片编辑

使用“变更单—单轮编辑—差异验收”流程，固定调用 `public_model_gpt_image_2`。把每次修改限制在一组相互关联的变化，并明确不可变化的区域；若编辑目标跨度过大，拆成多轮并保留上一版。

## 写编辑变更单

记录原图用途、目标对象、位置、期望状态、必须保留项、允许联动项、禁止变化和输出比例。多图输入时，说明第二张图只提供替换对象、颜色、纹理或姿势中的哪一项。

## 场景与代码

### 1. 清除杂物并修复背景

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '只删除桌面右侧电线、纸杯和后方反光标牌，并根据周围纹理自然补全桌面与墙面。保持人物、笔记本电脑、手部、服装、构图、光线和景深完全不变；不得新增物体、文字或裁切' \
  --image /path/to/office-photo.jpg
```

### 2. 用指定商品替换原物体

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '图1是待编辑广告，图2只提供新的香水瓶。将图1中央旧瓶替换为图2商品，保持图2的瓶型、标签、颜色和盖子；匹配图1的尺度、视角、左侧光源、接触阴影与反射。图1其他元素、文案和构图不变' \
  --image /path/to/ad-master.jpg \
  --image /path/to/new-product.png
```

### 3. 精确修改颜色与材质

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '只把沙发的蓝色织物改为暖灰色细纹亚麻，保留沙发结构、缝线、褶皱、尺寸、摆放和磨损状态；让新材质继承原光线与阴影。房间、人物、靠垫、墙面和相机参数不得变化' \
  --image /path/to/interior.jpg
```

### 4. 扩图并重新安排留白

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '将方形商品图扩展为16:9横版广告。保留商品像素级结构、包装、Logo、位置比例和原接触阴影，在左侧自然延展背景并形成干净标题留白；不移动或重绘商品，不生成文字、按钮、价格或道具' \
  --image /path/to/square-product.jpg \
  --param aspect_ratio=16:9
```

### 5. 批量制作季节版本

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '以原广告为母版生成春季、夏季、秋季三个版本。人物、商品、动作、包装、Logo、主构图和标题安全区全部锁定；只改变背景植物、环境色与匹配光线，不生成季节文字、价格、赠品或新人物' \
  --image /path/to/approved-ad.jpg \
  --batch 3
```

## 差异验收

1. 把结果与原图并排比较，只允许变更单中的区域发生变化。
2. 放大检查人脸、手、Logo、包装文字、边缘、纹理和透明部件。
3. 检查新增或替换对象的尺度、透视、阴影、反射与接触关系。
4. 对广告文案、价格和法律信息逐字复核，必要时恢复后期排版。
5. 保存原图、变更单、提示词、任务 ID 和批准版本；失败时回滚上一版。

## 执行

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name gpt-image-2-image-edit
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

支持多张参考图、批量、参数、路由和自定义输出目录。涉及人物外貌、商品事实或广告承诺时，取得必要授权并由人工确认最终结果。
