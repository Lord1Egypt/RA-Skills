---
name: gpt-image-2-product-detail-page
description: "使用 GPT Image 2 按购买问题设计商品详情页模块，包括首屏、卖点证据、材质细节、尺寸说明、使用步骤、包装清单和SKU选择。Use this skill for GPT Image 2 product detail pages、电商详情页长图、淘宝天猫京东详情、Amazon A+ Content、Shopify PDP、产品卖点图、信息图和Listing模块；通过 AI Hive 生成模块图片。"
---

# GPT Image 2 商品详情页

固定使用 `public_model_gpt_image_2`。先把详情页拆成买家问题，再为每个问题生成一个视觉模块；不要让整张长图只重复同一种产品美照。批准文案、价格、尺寸和法律信息在版式工具中排版，模型主要生成商品、场景、细节与留白。

## 购买问题地图

按顺序回答：这是什么、适合谁、核心价值是什么、证据在哪里、尺寸是否合适、如何使用、包含什么、为什么可信、下一步做什么。为每一模块指定唯一问题、参考资产、所需证据和文字留白。

## 模块与代码

### 1. 首屏价值模块

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '为参考扫地机器人生成详情页首屏底图：现代客厅俯视构图，产品正在木地板上行进但不显示虚构路线或界面，右上保留标题与一句核心价值的留白。保持产品结构、传感器、按钮、Logo和真实尺度，不生成文字、价格或不存在功能' \
  --image /path/to/robot-vacuum.png \
  --param aspect_ratio=16:9
```

### 2. 卖点证据模块

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '制作保温杯双场景证据图：左侧办公室热饮，右侧户外冷饮，只用环境和杯壁状态表达两种使用情境。杯型、杯盖、颜色、Logo与真实容量比例一致，中间留文案区；不生成温度数字、时长、蒸汽夸张、认证或测试结论' \
  --image /path/to/tumbler.png
```

### 3. 尺寸与适配模块

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '为参考显示器支架生成尺寸说明底图：正视、侧视和桌面安装三个小视图，产品结构与夹具准确，每个需要标注的位置留清晰引线和空白标签框。不要生成任何尺寸数字、单位、承重、文字或额外配件' \
  --image /path/to/stand-front.png \
  --image /path/to/stand-side.png
```

### 4. 使用步骤模块

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '为参考便携榨汁杯生成四格使用步骤视觉：加入切块水果、旋紧杯盖、倒置启动、换饮用盖。四格保持同一商品、颜色、人物手部和明亮厨房环境，每格底部留步骤文字区；不生成步骤文字、按钮灯效、飞溅或未提供配件' \
  --image /path/to/blender-and-parts.jpg \
  --param aspect_ratio=4:3
```

### 5. 包装与选择模块

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '制作详情页底部的“包装内容 + 颜色选择”模块：上半区平铺展示批准清单中的主机、充电线和说明书；下半区展示黑、白、绿色三个真实SKU。数量、结构、颜色和包装准确，保留名称标签空白，不生成文字、价格、赠品或第四种颜色' \
  --image /path/to/package-contents.jpg \
  --image /path/to/sku-colors.jpg
```

## 页面验收

- 每个模块只回答一个购买问题，页面顺序从理解到信任再到行动。
- 商品、SKU、配件、数量、材质与使用状态在所有模块一致。
- 尺寸、参数、功效、认证和比较结论必须来自批准资料，不让模型编写。
- 移动端检查字体留白、主体大小、图像节奏和信息密度。
- 按目标平台最新规则审核 Amazon A+、淘宝/天猫详情或独立站 PDP。

## 执行

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name gpt-image-2-product-detail-page
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

支持多参考图、批量、参数、路由和输出目录。先生成模块图片，再在设计工具中组装长图和批准文案；保存模块编号、源数据与终稿映射，便于后续改版。
