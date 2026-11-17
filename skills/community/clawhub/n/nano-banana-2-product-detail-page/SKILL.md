---
name: nano-banana-2-product-detail-page
description: "使用 Nano Banana 2 把商品信息拆成有顺序、可验证的详情页视觉模块，覆盖首屏、问题场景、核心利益、结构证明、使用步骤、规格与生活方式画面。Use this skill for Nano Banana 2 商品详情页、电商详情页、PDP、Amazon A+、淘宝天猫京东详情、抖店长图、Shopify product page、卖点模块、功能解释图、使用步骤图和上新素材；通过 AI Hive 逐模块生成。"
---

# Nano Banana 2 商品详情页

固定使用 `public_model_nano_banana_2`。不要一次生成一张塞满文字的超长详情页；先建立内容结构，再逐模块生成视觉底图，最后在设计工具中排版经过批准的文字与数据。

## 模块蓝图

常用顺序为：首屏定位 → 用户问题 → 核心利益 → 产品结构或证据 → 使用步骤 → 场景与人群 → 规格/包装清单 → 服务与合规信息。每个模块只承担一个问题，并定义商品锚点、画面任务、批准文案、证据来源、比例和衔接方式。

## 场景与代码

### 1. 首屏定位模块

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-desk-fan.png \
  --prompt '生成桌面循环扇详情页首屏底图：保持参考产品网罩、扇叶、支架、底座、旋钮和奶白色一致；夏日明亮书桌场景，产品位于右侧，左侧留两行标题与一句副标题区域，不生成文字、风量数字、人物、冰霜效果或不存在的遥控器' \
  --param aspect_ratio=16:9
```

### 2. 问题到利益模块

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-storage-box.png \
  --prompt '制作收纳箱详情页的问题与利益对照底图：左侧是凌乱但真实的儿童积木角落，右侧使用参考收纳箱完成分类，箱体尺寸、透明度、卡扣和轮子不变；中间留简短箭头和文字区域，不生成文字、夸张容量、额外箱体或无法放入的超大玩具' \
  --param aspect_ratio=16:9
```

### 3. 结构证明模块

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-headphones.png \
  --prompt '为参考头戴耳机生成结构说明底图：主体保持真实外形和Logo位置，展示耳罩、头梁调节、折叠转轴和实体按键四个局部近景，每个局部周围留标签空白；深灰技术视觉，不生成文字、内部芯片、声学数据、认证或未提供的结构' \
  --param aspect_ratio=16:9
```

### 4. 三步使用说明

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-vacuum-sealer.png \
  --prompt '制作真空封口机三步使用图底图：步骤1放入袋口，步骤2合上并按已存在的按钮，步骤3取出封好的袋子；产品外观和按钮布局依据参考图，三个等宽画面、相机角度一致，每格留步骤文字区，不生成文字、额外按钮、危险手势或无法实现的效果' \
  --param aspect_ratio=16:9
```

### 5. Amazon A+ 生活方式模块

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-camping-lantern.png \
  --prompt '生成露营灯 Amazon A+ 生活方式横图：保持灯体、提手、控制键和真实发光颜色，放在傍晚营地餐桌，远处帐篷虚化，产品仍为主要焦点，左侧保留标题和三条短卖点区域；不生成文字、平台Logo、防水等级、续航数字或未随附配件' \
  --param aspect_ratio=16:9
```

## 页面级验收

1. 模块顺序回答购买者真实问题，没有连续重复同一卖点。
2. 同一 SKU 的颜色、结构、比例、Logo和配件在所有模块一致。
3. 数据、对比、认证和功效均能追溯到批准证据。
4. 文字留白足够，关键主体避开移动端裁切与UI区域。
5. 最终文字在设计工具中排版并人工校对，不依赖生成图中的随机字符。

## 助手边界

脚本只调用固定 Nano Banana 2 图片模型，上传命令中明确提供的参考图，查询路由价格、生成和下载图片。所有携带 Key 的请求固定发送到 `https://ai-hive.iclip.cn/api`，不允许自定义目标地址。`init` 仅保存本地 Key；无聊天、视频、账户或余额功能。

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name nano-banana-2-product-detail-page
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

人物、用户评价、检测结果和前后对比必须有授权及证据。平台名称仅用于适配场景，不表示官方合作。
