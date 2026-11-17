---
name: nano-banana-2-ad-image
description: "使用 Nano Banana 2 将受众、问题、产品证据、允许主张和单一测试变量转成广告图片候选，便于投放前审查与 A/B 测试。Use this skill for Nano Banana 2 ad image、广告图片、效果广告、信息流广告、展示广告、商品广告、Meta Ads、Google Ads、抖音千川、小红书聚光、淘宝京东亚马逊 TikTok Shop 创意素材；通过 AI Hive 生成，不代表平台官方合作。"
---

# Nano Banana 2 广告图片

固定使用 `public_model_nano_banana_2`。每张广告只验证一个创意假设：给谁看、希望对方注意什么、画面用什么证据支持、允许说到什么程度、测试变量是什么。不要把未经证实的功效、销量和比较结论包装成视觉事实。

## 创意假设卡

记录目标受众、投放位置、用户情境、核心问题、商品事实、已批准主张、证据来源、行动意图、UI安全区和唯一变量。先生成无字或短标题候选，再由投放团队加入批准文案、价格与按钮。

## 场景与代码

### 1. 痛点场景广告

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-cable-organizer.png \
  --prompt '为桌面理线器制作信息流广告底图：左侧展示三根杂乱但安全的充电线，右侧使用参考产品完成整齐固定；产品形状、槽位数量、颜色和Logo不变，中间留一句短标题区，不生成文字、价格、百分比、夸张前后对比或不存在的收纳容量' \
  --param aspect_ratio=4:5
```

### 2. 产品证据近景

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-backpack.png \
  --prompt '生成通勤背包广告近景：保持包型、面料、拉链、肩带和真实颜色，画面聚焦已确认的独立电脑隔层与拉链结构，背景为简洁地铁站虚化，右上留卖点区；不生成防水测试、容量数字、品牌替换、人物脸或非标配物品' \
  --param aspect_ratio=1:1
```

### 3. Meta / Instagram 方形候选

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-candle.png \
  --prompt '为香薰蜡烛生成两个1:1广告候选：A以产品静物与柔和晚光表达放松场景，B以阅读角生活方式表达使用情境。两版保持包装、标签、蜡体颜色和商品占比一致，不生成文字、医学情绪承诺、折扣、平台Logo或第二个产品' \
  --batch 2 \
  --param aspect_ratio=1:1
```

### 4. 抖音千川竖版底图

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-mop.png \
  --prompt '制作4:5竖版商品广告底图：保持参考拖把结构、颜色、连接件和标配数量，在明亮家庭地板场景展示正常使用状态，顶部和底部避开UI，左侧留三行卖点区域；不生成主播、文字、价格、污渍瞬间消失、清洁百分比或未提供的配件' \
  --param aspect_ratio=4:5
```

### 5. 单变量 A/B 测试

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-water-bottle.png \
  --prompt '为同一运动水杯生成两个广告版本，只测试背景情境：A室内健身房长凳，B户外慢跑补给台。商品角度、尺寸、颜色、Logo、光线强度、画布占比和留白完全一致，不改变瓶盖结构，不生成文字、人物脸、速度或健康效果' \
  --batch 2 \
  --param aspect_ratio=4:5
```

## 投放前检查

1. 画面能在一秒内传达单一信息，商品事实与上架 SKU 一致。
2. 视觉证据确实支持批准主张，没有暗示超出证据的效果。
3. A/B 版本只改变一个变量，命名和投放记录可追溯。
4. 主体避开各平台 UI、裁切与文字安全区。
5. 价格、促销、比较和法规声明由人工加入并按实时政策审查。

## 助手边界

脚本可从文字开始或上传用户指定图片，固定调用 Nano Banana 2 模型，创建图片任务并保存结果。认证请求仅发送到 `https://ai-hive.iclip.cn/api`，不允许自定义接口。Key 可由 `init` 本地保存；没有聊天、视频、账户或余额能力。

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name nano-banana-2-ad-image
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

平台名称仅用于描述投放环境；发布前核对目标平台最新广告政策和素材规格。
