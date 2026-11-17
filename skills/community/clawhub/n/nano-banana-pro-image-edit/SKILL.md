---
name: nano-banana-pro-image-edit
description: "使用 Nano Banana Pro 按自然语言编辑现有图片，同时明确保留区、修改区和禁止变化项。Use this skill for Nano Banana Pro图片编辑、局部重绘、删除物体、改颜色、换服装、修复瑕疵、调整构图、广告图改版、批量图片修改和参考图编辑；通过 AI Hive 自动上传、生成与下载。"
---

# Nano Banana Pro 图片编辑

把编辑要求写成可核验的变更合同，而不是一句“帮我优化”。固定调用 `public_model_nano_banana_pro`，通过 `scripts/imagegen.py` 上传原图并返回编辑结果。

## 编辑合同

每次任务都列出：

1. **必须保留**：人物身份、商品结构、Logo、文字、相机、背景区域等。
2. **必须改变**：具体对象、位置、颜色、材质或光线。
3. **允许调整**：为自然融合可变化的阴影、反射、边缘和邻近像素。
4. **禁止变化**：未授权品牌、身体特征、产品功能、价格和证据性内容。
5. **验收方法**：与原图逐项对比，而不是只看“更好看”。

## 场景与代码

### 1. 删除杂物但保留主体

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '编辑原图。必须保留人物身份、姿势、服装、桌面商品、相机角度和整体光线；删除左后方纸箱与地面电线，使用原墙面和地面纹理自然补全；不得改变人物面部、商品包装、Logo或桌面物品' \
  --image /path/to/source.jpg
```

### 2. 只修改商品颜色

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '只把商品外壳从黑色改为商家确认的哑光墨绿色。必须锁定结构、尺寸、接口、包装文字、Logo、相机、背景和阴影；允许反射随新颜色自然调整，不得改变配件或材料纹理' \
  --image /path/to/product.jpg
```

### 3. 服装局部替换

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '将人物上衣替换为参考图中的米白针织开衫。必须保持人物身份、脸部、发型、身体比例、裤装、姿势、手部和场景；参考图只提供上衣版型与材质，衣服需顺应原姿势与光线，不复制参考人物' \
  --image /path/to/person.jpg \
  --image /path/to/cardigan-reference.jpg
```

### 4. 广告图重新构图

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '把方形广告图调整为竖版构图：必须保留商品、包装、品牌色和核心场景；将商品移到下半部视觉中心，上方扩展背景形成标题留白，重新计算接触阴影和透视；不生成新文字、价格、Logo或功能'
  --image /path/to/square-ad.png
```

### 5. 批量统一修改规则

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '按同一规则生成3个编辑版本：保留商品与人物，分别将背景整理为暖白居家、浅灰影棚、柔和木质空间；所有版本锁定主体身份、结构、尺度和相机，只改变背景与匹配光线，不添加道具和文字' \
  --image /path/to/source.jpg \
  --batch 3
```

## 编辑验收

- 逐项核对保留清单，没有附带改变。
- 修改区域边缘、遮挡、透视、阴影和反射自然。
- 人物脸部、手部和身体比例无漂移。
- 商品结构、包装、Logo、文字和配件无误改。
- 没有新增价格、功效、认证或未授权品牌。
- 保存原图、提示词和输出版本，便于回滚。

## 执行

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name nano-banana-pro-image-edit
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

`generate` 支持多次 `--image`、`--batch`、`--param key=value`、`--routing`、`--output-dir` 和 `--no-download`。任务超时后查询原 `taskId`。
