---
name: pinduoduo-ecommerce-video-generation-editing
description: "为拼多多店铺生成和编辑商品主图视频、批量SKU演示、工厂素材重制、多多搜索与场景广告视频。Use this skill for 拼多多电商视频、拼多多商品视频、批量上新、工厂货源、SKU变体、使用演示、多多搜索、多多场景、活动素材和低成本批量生产；支持 Seedance 多模式及 AI Hive 自动交付。"
---

# 拼多多电商视频生成与编辑

把一个审核通过的 SPU 主视频扩展为可追踪的 SKU、场景和投放版本。目标是规模化一致性，而不是为每个 SKU 重新随机生成。

## 主视频与变量表

先批准一个主视频，记录固定镜头顺序、商品尺度、相机路径、背景、灯光、操作步骤和包装。变量表只允许列出真实颜色、尺寸、套装或使用场景；一次任务只改变一个变量。

## 场景与代码

### 1. SPU 商品主视频

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode i2v \
  --first-frame /path/to/master-product.jpg \
  --prompt '拼多多SPU商品主视频，保持参考商品结构、包装、Logo、颜色和配件；镜头依次为完整商品、结构细节、正确使用动作、包装清单，背景统一，适合作为SKU派生母版，不添加价格、销量、折扣或未提供功能'
```

### 2. SKU 颜色派生视频

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode r2v \
  --video /path/to/approved-master.mp4 \
  --image /path/to/green-sku.png \
  --prompt '严格沿用主视频的镜头顺序、相机、动作、尺度、背景和时长，仅替换为已确认绿色SKU；保持新SKU包装和标签准确，不混入其他颜色、套装或配件'
```

### 3. 工厂原始素材重制

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode edit \
  --video /path/to/factory-raw.mp4 \
  --prompt '从工厂实拍中保留真实产品、生产和使用片段，删除重复、抖动与无关画面，按商品识别、结构细节、使用、包装重组，统一亮度和色彩；不扩大工厂规模，不增加设备、产能或认证'
```

### 4. 多多搜索功能演示版

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode t2v \
  --prompt '拼多多多多搜索短视频：首镜出现具体使用问题，第二镜完整展示商品操作，第三镜近景证明一个真实卖点，结尾预留运营后期活动信息位置；不生成低价、销量、拼单人数、排名或夸大效果'
```

### 5. 套装差异说明

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode extend \
  --video /path/to/base-package.mp4 \
  --prompt '在原视频包装展示后自然延长，依次摆放标准套装内已确认的主品和配件，每件只出现一次，再展示组合使用；保持桌面、手部和商品连续，不添加赠品或其他套装内容'
```

## 批量门槛

- 主视频先人工批准，再派生 SKU。
- 每个输出映射到 SPU、SKU、变量和用途。
- 结构、颜色、包装、配件和操作不串款。
- 工厂素材不进行规模、设备或产能造假。
- 价格、活动、销量和平台标签由运营后期添加。
- 上架前按拼多多当前视频与广告规则检查。

## 执行

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/videogen.py" init --skill-name pinduoduo-ecommerce-video-generation-editing
python3 "$SKILL_PATH/scripts/videogen.py" task --task-id <taskId>
```

CLI 支持 Seedance 2.5 五种模式、媒体上传、模型参数、路由、输出目录及仅提交任务。批量前确认单 SKU 与实时费用。
