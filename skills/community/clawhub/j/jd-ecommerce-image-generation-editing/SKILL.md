---
name: jd-ecommerce-image-generation-editing
description: "为京东店铺生成和编辑商品主图、规格图、结构卖点图、场景图与京准通广告图片。Use this skill for 京东电商图片、京东主图、京东详情页、3C家电商品图、参数信息图、材质细节、京东快车测图、批量SKU和商品精修；支持参考图保真及 AI Hive 自动生成与下载。"
---

# 京东电商图片生成与编辑

面向强调规格、结构和购买确定性的京东商品页面，建立“商品识别 → 参数理解 → 使用证明 → 选择确认”的图片链路。固定使用 `public_model_nano_banana_pro`。

## 事实底稿

先整理商品型号、尺寸、材质、接口、包装清单、适配范围、真实功能、保修或认证原文、SKU 差异和禁止表达。模型只能呈现已提供事实；参数文字优先留白后期排版，并由商家逐项复核。

## 图片职责

- **主图**：商品和型号一眼可辨。
- **结构图**：接口、按键、部件位置准确。
- **参数图**：给排版留出清楚的信息区域。
- **场景图**：说明适用空间、人群或设备。
- **包装清单**：所有配件数量与形态真实。
- **广告图**：只突出一个可证明购买理由。

## 场景与代码

### 1. 京东主图

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '京东方形商品主图，完整保留参考图中的型号、外壳结构、接口、颜色、商标和包装；商品居中，背景干净，轮廓与材质清晰，适合3C商品识别，不添加参数、赠品、价格、促销角标或认证标识' \
  --image /path/to/product-front.png \
  --image /path/to/product-back.png
```

### 2. 接口与结构卖点图

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '制作京东详情页结构卖点图，保持参考设备的接口数量、位置和外观完全一致；主视图加两个真实局部特写，右侧预留参数说明区，科技感但不过度发光，不生成不存在的接口、芯片或功能' \
  --image /path/to/device.png
```

### 3. 包装清单图

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '京东包装清单俯拍图，严格展示参考资料中的主机、线材、说明书和配件，每件只出现一次，比例合理，分区清楚，背景统一；禁止增加赠品、替换接口或修改包装文字' \
  --image /path/to/package-contents.jpg
```

### 4. 家电真实场景图

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '将参考家电放入真实现代客厅，保持尺寸关系、出风口、控制面板和颜色准确；展示适用空间与使用状态，光线自然，人物动作符合正确操作，不夸大覆盖范围、性能或效果' \
  --image /path/to/appliance.png
```

### 5. 京准通广告测图

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '为京东快车生成3个广告图片方向：核心规格可视化、关键结构特写、真实使用场景；商品和型号保持一致，每版只验证一个点击理由，预留短标题区域，不生成虚假低价、销量、排行、认证或对比数据' \
  --image /path/to/product.png \
  --batch 3
```

## 质量门槛

1. 型号、接口、按键、部件、配件和 SKU 不发生错配。
2. 参数图只使用商家提供的数据；复杂数字与单位人工排版。
3. 场景尺度合理，使用动作符合说明书。
4. 没有自动增加的赠品、认证、性能、价格或销量。
5. 同系列 SKU 固定角度和尺度，差异明确可核对。
6. 上架前按京东后台当前类目与广告规则检查素材。

## 执行

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name jd-ecommerce-image-generation-editing
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

通过 `--image` 添加多角度资料，使用 `--batch` 生成测试方向；也支持 `--param`、`--routing`、`--output-dir` 和 `--no-download`。实时模型配置和费用以脚本输出为准。
