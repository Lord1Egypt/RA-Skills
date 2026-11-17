---
name: nano-banana-product-detail-page
description: "用 AI Hive Nano Banana 2 为真实商品逐张制作电商详情页、PDP、Amazon A+ 与 Listing 卖点图；每张图只表达一个已核准主张，并记录商品事实、主张来源、视觉证据、文案安全区和不可虚构项。Use when ecommerce sellers, brand teams and designers need Nano Banana product detail pages, PDP modules, Amazon A+ content, listing images, feature panels, material close-ups, how-it-works visuals, verified specifications or comparison graphics for Taobao, Tmall, JD, Douyin, Xiaohongshu, TikTok Shop and Shopify."
---

# Nano Banana 商品详情页｜PDP 与 Amazon A+

详情页不是一张无限长的“万能图”，而是一组有顺序的证据面板。每次只生成一张：先确定本图唯一主张，再写主张来源和画面如何证明。至少提供一张已授权商品参考图；脚本固定调用 Nano Banana 2，不允许模型自己补参数、内部结构、对比结果或功效。

## 面板清单

为整页建立 `Page ID / 顺序 / 面板类型 / 唯一主张 / 来源 / 视觉证据 / 文案区 / 下一张承接`。`how-it-works`、`spec`、`comparison` 和 `steps` 面板还必须填写已核实依据。需要出现的文字可以传入，但交付前必须逐字人工检查。

## 五张详情页面板

### 1. PDP 首屏 Hero 面板

```bash
python3 "$SKILL_PATH/scripts/nano_detail_panel.py" panel \
  --page-id 'KETTLE-K1-PDP-CN' --sequence 1 --panel-type hero \
  --reference ./approved-kettle-front.png ./approved-kettle-side.png \
  --product-facts '黑色不锈钢电热水壶，单个壶体和一个底座；结构、接口与颜色以参考图为准' \
  --claim '先让用户看清商品是什么，不表达未经核准的性能结论' \
  --claim-source '品牌批准的 SKU 资料 K1-v3' \
  --visual-proof '壶体与底座完整同框，壶嘴、把手、开关和接口清晰可见' \
  --must-keep '数量、比例、黑色材质、底座、开关、接口和Logo' \
  --style-system '深灰到暖白渐变背景，真实棚拍光，整页统一低饱和色彩' \
  --text-zone '左上保留标题区，商品不得进入该区域' \
  --do-not-show '不生成容量、认证、沸腾速度、价格、折扣、配件或文字' \
  --param resolution=1024x1024
```

### 2. 单卖点 Feature 面板

```bash
python3 "$SKILL_PATH/scripts/nano_detail_panel.py" panel \
  --page-id 'HEADPHONE-H7-PDP' --sequence 3 --panel-type feature \
  --reference ./approved-headphone.png ./approved-control-detail.png \
  --product-facts '灰色头戴耳机；右耳罩有三个实体按键，位置以细节参考图为准' \
  --claim '三个实体按键集中在右耳罩，便于用户看清操作位置' \
  --claim-source '已批准产品结构图 H7-control-v2' \
  --visual-proof '商品整体与右耳罩按键放大细节并列，但仍保持同一副耳机身份' \
  --must-keep '耳罩、头梁、三个按键、接口、颜色、材质和Logo' \
  --style-system '延续首屏的蓝灰背景与右侧轮廓光' \
  --text-zone '左侧预留两行卖点文案区，先输出无字底片' \
  --do-not-show '不虚构触控、降噪等级、电池时长、认证、图标或第二副耳机'
```

### 3. 材质细节面板

```bash
python3 "$SKILL_PATH/scripts/nano_detail_panel.py" panel \
  --page-id 'BAG-M5-PDP' --sequence 4 --panel-type material \
  --reference ./approved-bag-front.png ./approved-bag-material-macro.png \
  --product-facts '棕褐色单肩包，金属扣、肩带连接、缝线和表面纹理以参考图为准' \
  --claim '展示已经拍摄并批准的表面纹理与缝线细节' \
  --claim-source '商品摄影批次 M5-2026-08 与质检确认图' \
  --visual-proof '左侧完整包型，右侧只放大同一商品的表面纹理和缝线' \
  --must-keep '包型、颜色、金属扣、肩带连接、缝线方向、纹理和Logo' \
  --style-system '暖灰背景、柔和侧光、与前序面板一致的留白' \
  --text-zone '底部保留材质说明区' \
  --do-not-show '不命名未提供的材料成分，不生成耐磨、防水、真皮等未经确认的宣称'
```

### 4. How-it-works 使用原理面板

```bash
python3 "$SKILL_PATH/scripts/nano_detail_panel.py" panel \
  --page-id 'FILTER-F2-PDP' --sequence 5 --panel-type how-it-works \
  --reference ./approved-filter-product.png ./approved-filter-cutaway.png \
  --product-facts '滤芯外壳与批准剖面图中的三层结构，仅按已提供文件呈现' \
  --claim '用批准剖面图解释水流经过三层结构的顺序' \
  --claim-source '工程批准图 F2-cutaway-rev4' \
  --visual-proof '产品外观、剖面与单向水流路径并列，层数和先后顺序清楚' \
  --evidence 'rev4 图纸确认三层，从外到内编号 1、2、3；不添加净化率或去除物声明' \
  --must-keep '外壳、三层数量、层序、接口方向和尺寸关系' \
  --style-system '白底技术说明风，使用品牌蓝作为路径辅助色' \
  --text-zone '右侧预留三条说明，不生成实际参数文字' \
  --do-not-show '不增加第四层，不虚构过滤材料、效率、认证、医学或健康功效'
```

### 5. 规格与对比面板

```bash
python3 "$SKILL_PATH/scripts/nano_detail_panel.py" panel \
  --page-id 'BOTTLE-B8-APLUS' --sequence 7 --panel-type comparison \
  --reference ./approved-bottle-500.png ./approved-bottle-750.png ./approved-scale-photo.png \
  --product-facts '同系列 500 mL 与 750 mL 两个已批准 SKU，外形和颜色以参考图为准' \
  --claim '帮助用户比较两个 SKU 的已核实容量与相对高度' \
  --claim-source '商品规格表 B8-rev2 与带标尺摄影原图' \
  --visual-proof '两个 SKU 以同一视角并排，底部基线对齐，容量标签区清晰分开' \
  --evidence 'SKU-B8-500=500 mL；SKU-B8-750=750 mL；相对高度只按标尺照片呈现' \
  --must-keep '两个瓶型、颜色、瓶盖、Logo、数量和各自容量归属' \
  --style-system 'Amazon A+ 简洁信息图底片，浅灰背景，统一阴影' \
  --text-zone '每个 SKU 下方独立文字区，交付前再叠加已核准参数' \
  --do-not-show '不生成优于、更多、保温时长、百分比、价格、促销或未经验证的尺寸'
```

## 组页验收

先单张核对商品身份、主张和证据，再按顺序检查整页是否重复、跳步或视觉风格漂移。规格、比较、原理和步骤图必须回到原始文件核验；无字底片可交给设计师后期排版。用 `preview` 替换 `panel` 可先检查提示词，不上传素材也不产生任务。

认证流量固定前往 `https://ai-hive.iclip.cn/api`，模型固定为 `public_model_nano_banana_2`。本工具不连接 Amazon、淘宝、天猫、京东、抖音、小红书或 Shopify 后台，也不会自动发布页面。

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/nano_detail_panel.py" auth --api-key REDACTED-SECRET
python3 "$SKILL_PATH/scripts/nano_detail_panel.py" status --task-id <taskId>
```
