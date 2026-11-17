---
name: pinduoduo-ecommerce-image-generation-editing
description: "为拼多多店铺生成和编辑商品主图、SKU 套图、活动图、使用场景图和多多搜索/多多场景测图。Use this skill for 拼多多电商图片、拼多多主图、批量上新、工厂商品图、白底图、规格图、低成本SKU生产、活动素材和商品换背景；支持参考图保真及 AI Hive 批量生成。"
---

# 拼多多电商图片生成与编辑

服务多 SKU、快速上新和高频测图场景。核心不是堆促销字，而是在批量生产中保持商品准确、版本可追踪、创意假设可测试。固定调用 `public_model_nano_banana_pro`。

## 建立商品母版

为每个 SPU 选定一张母版图并记录：固定相机角度、商品占比、背景、阴影、商标、配件、颜色表和规格表。所有 SKU 从母版派生，不能让模型自由重画结构。

## 批量策略

1. 先用一个 SKU 验证商品保真。
2. 再生成颜色或规格变体，每次只改变一个已确认属性。
3. 将主图、场景图、规格图和活动图分开生成。
4. 测图时改变的是卖点呈现或使用场景，不只是饱和度。
5. 所有价格、折扣、拼单、销量和活动文字由运营后期添加并复核。

## 场景与代码

### 1. 工厂商品母版主图

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '拼多多方形商品母版图，严格保持参考产品结构、包装、商标、颜色和配件，商品完整居中且占画面主要区域，背景纯净，阴影真实，适合后续批量SKU派生，不添加价格、折扣、销量或促销贴纸' \
  --image /path/to/master-product.png
```

### 2. 批量 SKU 颜色变体

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '从母版生成SKU图：锁定相机角度、尺度、结构、背景和阴影，只将商品颜色分别改为商家确认的米白、深灰、橄榄绿；包装文字和配件不变，每张只出现一个SKU' \
  --image /path/to/master-product.png \
  --batch 3
```

### 3. 规格选择图

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '制作拼多多规格选择底图，展示参考商品的三种真实尺寸，保持造型和材质一致，按从小到大排列并留出尺寸文字区域；不自行生成数值、容量、适用人数或功能差异' \
  --image /path/to/sizes-reference.jpg
```

### 4. 使用场景图

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '将参考商品放入普通家庭真实使用场景，人物按正确方式操作，产品大小和功能状态合理，画面直接说明解决的具体问题；保持商品结构和颜色，不营造虚假豪华环境，不夸大使用效果' \
  --image /path/to/product.png
```

### 5. 多多搜索与场景测图

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '为同一拼多多商品制作4个测图方向：商品大特写、具体痛点场景、结构细节、使用结果；保持商品、背景基调和品牌色一致，每版只验证一个创意假设，预留运营后期添加活动信息的区域，不生成价格和销量' \
  --image /path/to/product.png \
  --batch 4
```

## 批量验收

- 每个 SKU 与颜色/规格表一一对应，没有串色或串款。
- 商品结构、商标、包装、配件和数量一致。
- 母版与变体角度、尺度、背景和阴影统一。
- 活动图没有模型生成的虚假价格、折扣、销量和平台标识。
- 文件名包含 SPU、SKU、用途和版本，方便回滚。
- 发布前按拼多多后台当期类目、主图和广告规范检查。

## 执行

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name pinduoduo-ecommerce-image-generation-editing
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

`generate` 支持重复的 `--image`、`--batch`、`--param key=value`、`--routing`、`--output-dir` 与 `--no-download`。批量前先查看实时价格并完成单 SKU 验证；超时后查询原任务。
