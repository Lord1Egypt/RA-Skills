---
name: nano-banana-2-seeding-image
description: "使用 Nano Banana 2 设计具有真实使用情境、可观察细节和广告披露空间的种草图片，避免把合成画面冒充真实用户体验。Use this skill for Nano Banana 2 seeding image、种草图片、小红书种草、抖音种草、Instagram UGC、生活方式图片、达人合作底图、带货内容、产品体验图、电商内容营销和社媒封面；通过 AI Hive 生成或编辑授权素材。"
---

# Nano Banana 2 种草图片

固定使用 `public_model_nano_banana_2`。种草图要建立“使用情境 → 可观察细节 → 个人偏好 → 披露位置”的体验链，不制造无法从画面证明的功效、用户评价或购买结果。纯生成内容必须标注，不冒充真实消费者自拍。

## 体验证据链

记录内容身份（品牌、达人、虚构概念）、目标人群、真实场景、产品如何被使用、画面可观察的细节、允许的主观表达、禁止主张、广告披露位置和渠道比例。人物、住宅、商品与评价素材都要有授权。

## 场景与代码

### 1. 通勤包真实收纳

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-tote.png \
  --prompt '制作通勤包种草俯拍图：保持包型、材质、内袋、颜色和Logo，打开包展示已确认能放入的13英寸电脑、笔记本、钥匙和水杯，物品尺度真实，右上留内容标题与广告披露区；不生成容量数字、人物脸、价格、平台Logo或额外内袋' \
  --param aspect_ratio=3:4
```

### 2. 家居使用角落

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-table-lamp.png \
  --prompt '将参考台灯放在夜间阅读角，产品结构、颜色、按钮和Logo不变，展示书页上的自然光照范围和桌面氛围，构图像经过整理的品牌生活方式内容而非随手自拍，顶部留披露区；不生成护眼功效、色温数字、人物脸、文字或不存在的功能' \
  --param aspect_ratio=4:5
```

### 3. 美妆质地观察

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-cream.png \
  --prompt '制作面霜种草静物：保持包装、标签、容量和真实颜色，展示打开后的少量质地与干净取用勺，柔和浴室晨光，左侧留三行体验描述区；只表现可观察质地，不生成使用前后对比、皮肤治疗、即时效果、人物脸、文字或虚假认证' \
  --param aspect_ratio=4:5
```

### 4. 食品分享场景

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-granola.png \
  --prompt '为参考麦片制作早餐分享图：包装文字、品牌、颜色和商品数量不变，旁边是一碗正常份量酸奶与水果，窗边自然光，画面右上留标题和合作披露区域；不生成减脂、营养功效、卡路里数字、价格、人物或额外包装' \
  --param aspect_ratio=3:4
```

### 5. 穿搭参考而非真人评价

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-jacket.png \
  --prompt '基于参考夹克生成穿搭灵感图：保持版型、长度、颜色、纽扣和面料，搭配无品牌白T恤与深色直筒裤，使用无脸模特、自然街角光线，顶部留“搭配灵感”和广告披露区；不生成真实达人身份、购买评价、文字、价格或平台Logo' \
  --param aspect_ratio=4:5
```

## 真实性检查

- 明确内容是实拍编辑、授权达人素材还是 AI 生成概念，使用对应披露。
- 画面只支持可观察事实，不替代真实试用、检测或用户评价。
- 商品结构、颜色、数量、包装和标配与上架 SKU 一致。
- 场景道具不会被误认为赠品，人物和住宅没有授权风险。
- 发布前核对广告披露、平台规则和禁限用表达。

## 助手边界

脚本可提交纯文字图片任务或上传用户指定参考图，固定使用 Nano Banana 2 模型并下载结果。所有带 Key 请求固定发送到 `https://ai-hive.iclip.cn/api`，不接受自定义地址。无聊天、视频、账户或余额接口。

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name nano-banana-2-seeding-image
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

不得生成虚假用户证言、伪造达人合作或把 AI 合成图冒充真实使用记录。
