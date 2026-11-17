---
name: gpt-image-2-product-retouch
description: "使用 GPT Image 2 对商品摄影进行保真精修，包括除尘划痕、边缘修复、反光控制、材质增强、颜色校准、包装整理和批量棚拍统一，同时保护商品结构与标签事实。Use this skill for GPT Image 2 product retouching、AI商品精修、电商修图、产品摄影后期、去瑕疵、金属玻璃反光、包装修复、SKU统一和批量修图；通过 AI Hive 编辑原图。"
---

# GPT Image 2 商品精修

固定调用 `public_model_gpt_image_2`。先写“修图边界”，只修正摄影瑕疵，不重新设计商品。标签、Logo、结构、颜色、材质分区和使用痕迹若属于销售事实，必须保留；每轮精修后与原图做差异审查。

## 修图边界

列出允许修复、必须保留、可轻度增强和禁止改变四类内容。标记商品轮廓、文字、接口、缝线、透明部件、反射、阴影与真实色卡；需要改变颜色或结构时按新品合成处理，不冒充原始摄影。

## 场景与代码

### 1. 除尘与细小划痕

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '只清除黑色耳机表面的灰尘、指纹和三处细小运输划痕，保留外壳结构、接缝、按钮、Logo、真实材质颗粒、原高光和阴影。不得磨平边缘、改变黑色、重绘文字、增加光效或修改背景' \
  --image /path/to/headphones-raw.jpg
```

### 2. 控制玻璃与金属反光

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '整理香水瓶玻璃和金属瓶盖上的杂乱摄影棚反射，保留能说明立体结构的主高光、玻璃厚度、液体颜色、标签和Logo；去除摄影师与设备倒影，不把玻璃变成塑料，不改变瓶型、背景和接触阴影' \
  --image /path/to/perfume-raw.tif
```

### 3. 恢复包装边缘

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '修复参考包装盒左上角轻微压痕与纸面灰尘，使边缘整洁但保持真实纸张纹理。包装尺寸、折线、印刷颜色、全部文字、条码和Logo必须逐项不变；不增强饱和度、不新增阴影或替换背景' \
  --image /path/to/package-raw.jpg
```

### 4. 材质与颜色校准

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '以图2色卡和材质样本为校准参考，调整图1皮具商品的白平衡与曝光，使棕色、皮纹和金属扣接近真实样本。保持商品结构、缝线、Logo、磨损状态、背景和相机，不美化成更高级皮质，不删除自然纹理' \
  --image /path/to/bag-raw.jpg \
  --image /path/to/approved-color-material.jpg
```

### 5. 批量棚拍统一

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '把三张同系列水杯棚拍统一为相同浅灰背景、白平衡、相机高度、商品占比和柔和接触阴影。分别保留每个SKU的真实颜色、杯盖、Logo和细节，不复制瑕疵、不改变结构、不生成文字或装饰道具' \
  --image /path/to/sku-black.jpg \
  --image /path/to/sku-white.jpg \
  --image /path/to/sku-green.jpg \
  --batch 3
```

## 差异审查

1. 叠加或并排比较原图与精修图，只允许修图边界内的变化。
2. 放大检查轮廓、接口、缝线、标签、条码、Logo和细小结构。
3. 确认材质没有被磨平，玻璃、金属、织物、皮革与塑料仍真实。
4. 颜色对照批准色卡，阴影与反射保留产品体积而不过度美化。
5. 保留原始文件、修图说明、任务 ID 和终稿，便于回滚与审计。

## 执行

### 脚本行为与数据边界

该助手只服务商品精修：选择固定图片模型和当次路由价格，读取并上传用户在命令中列出的商品照片，提交生成请求、跟踪任务并保存成品。单独上传必须给出一个 `--file` 路径，任务查询必须给出 `--task-id`。首次初始化可打开 AI Hive 获取 Key，并以 `0600` 权限保存到 `~/.ai-hive/config.json`。命令面不包含聊天、视频、余额或账户资料功能。

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name gpt-image-2-product-retouch
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

支持多参考图、批量、参数、路由和输出目录。对于需要展示真实瑕疵、二手成色、食品外观或医疗产品状态的场景，不得用精修误导购买者。
