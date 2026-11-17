---
name: nano-banana-2-image-edit
description: "使用 Nano Banana 2 对现有图片进行可追踪编辑，包括清理、对象替换、颜色修改、构图改版、人物或商品局部调整和渠道适配。Use this skill for Nano Banana 2图片编辑、AI修图、局部重绘、删除物体、改颜色、广告图改尺寸、人物编辑、商品修改和批量版本；通过 AI Hive 上传原图并生成。"
---

# Nano Banana 2 图片编辑

采用“编辑清单 + 差异复核”工作流。每次只做一组相互关联的修改，先锁定不可变化内容，再检查模型是否产生未请求的附带修改。

## 编辑清单

写清：原图用途、修改对象、精确位置、期望状态、必须保留、允许联动调整、禁止变化和输出规格。若有第二张参考图，说明它只提供什么，不允许复制什么。

## 场景与代码

### 1. 场景清理

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '清理原图：保留房间结构、家具位置、商品、相机和光线；移除桌面纸杯、地面纸袋和墙上临时胶带，用邻近材质自然补全，不改变墙色、Logo、商品和窗外景色' \
  --image /path/to/room.jpg
```

### 2. 对象替换

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '用图2的准确商品替换图1桌面中央旧商品。图1锁定场景、相机、人物和构图；图2只提供商品结构、包装、Logo与颜色。新商品尺度、遮挡、反射和接触阴影需匹配图1，不复制图2背景' \
  --image /path/to/scene.jpg \
  --image /path/to/new-product.png
```

### 3. 局部配色修改

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '只将沙发靠垫从亮红改为低饱和鼠尾草绿；保持沙发、人物、皮肤、商品、墙面、木地板和整体曝光不变，允许靠垫阴影与反射自然调整，不扩散颜色到其他物体' \
  --image /path/to/lifestyle.jpg
```

### 4. 渠道构图改版

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '将横版KV改为9:16竖版：锁定商品、人物、品牌色和场景事实，重新排列主体并向上扩展背景，为标题和CTA分别留出区域；不裁断商品，不生成文字、价格或平台UI' \
  --image /path/to/wide-kv.jpg
```

### 5. 三种可回滚版本

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '在保留人物、商品、姿势与相机的前提下生成三个背景整理强度：轻度只清杂物，中度简化家具，强度版改为干净影棚；所有版本禁止改变主体身份、商品和服装' \
  --image /path/to/source.jpg \
  --batch 3
```

## 差异复核

- 对比原图和输出，标记所有变化，包括未请求变化。
- 人物身份、商品事实、文字与 Logo 没有漂移。
- 编辑边缘、遮挡、阴影、反射和透视自然。
- 颜色修改没有污染其他区域。
- 构图改版没有裁断关键对象或新增虚假内容。
- 保存原图和版本编号，可随时回滚。

## 执行

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name nano-banana-2-image-edit
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

固定模型 `public_model_nano_banana_2`，支持多参考图、批量、实时参数、路由和仅提交任务。
