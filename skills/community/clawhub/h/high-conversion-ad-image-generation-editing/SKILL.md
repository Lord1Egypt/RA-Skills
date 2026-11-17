---
name: high-conversion-ad-image-generation-editing
description: "使用 Nano Banana Pro 生成和编辑广告图片，并通过漏斗诊断、信息匹配、单变量实验和真实结果复盘寻找更高转化候选。Use this skill for 高转化广告图片生成与编辑、performance creative、信息流广告、展示广告、电商广告、Meta Ads、Google Ads、抖音千川、小红书聚光、Amazon Ads、TikTok Ads 和 A/B 测试；通过 AI Hive 生成，高转化不构成保证。"
---

# 高转化广告图片生成与编辑

固定使用 `public_model_nano_banana_pro`。先判断瓶颈发生在注意、理解、信任还是行动，再让图片只解决一个瓶颈。转化由受众、出价、页面、价格和产品共同决定；生成图只能提供可测试候选，不能保证高转化。

## 诊断循环

记录渠道、受众、当前数据、漏斗瓶颈、批准主张、视觉证据、落地页对应、唯一变量和成功指标。每轮生成一组只有一个差异的候选，上线后用真实数据决定保留、修改或停止。

## 场景与代码

### 1. 注意力瓶颈

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-bottle.png \
  --prompt '为运动水瓶生成两个注意力候选，只改变视觉焦点：A以瓶盖结构近景，B以整瓶轮廓。商品颜色、Logo、背景、留白和比例一致，不生成文字、健康效果、价格、人物或新配件' \
  --batch 2 \
  --param aspect_ratio=4:5
```

### 2. 理解瓶颈

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-cable-box.png \
  --prompt '生成理线盒功能广告底图：左侧展示盒盖打开后的真实内部，右侧展示关闭后的桌面状态，结构、孔位、颜色和Logo不变，中间留一句解释区；不生成文字、线材数量承诺、前后夸张、价格或额外功能' \
  --param aspect_ratio=1:1
```

### 3. 信任瓶颈

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-pan-detail.jpg \
  --prompt '制作平底锅材质证据广告：保持锅型、手柄、涂层颜色和Logo，主图展示正常外观，辅图放大已批准的锅底纹理和连接结构，留检测说明区域；不生成认证、耐用次数、无油效果、文字或实验室场景' \
  --param aspect_ratio=1:1
```

### 4. 行动瓶颈

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-course-cover.png \
  --prompt '为在线课程落地页广告生成简洁行动版：保持批准课程封面与讲师授权形象，右侧留课程名称、三条内容和按钮区域，背景低干扰；不生成文字、学员数量、收入承诺、证书、倒计时或平台Logo' \
  --param aspect_ratio=4:5
```

### 5. 落地页匹配修订

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./old-ad.png ./approved-product-page.png \
  --prompt '编辑旧广告以匹配批准商品页：保留广告构图与品牌色，用参考商品页中的真实产品外观和标配替换旧产品，移除页面未提供的赠品区域，保留标题与CTA留白；不复制网页文字、价格、评价或Logo之外的界面' \
  --param aspect_ratio=4:5
```

## 实验复盘

1. 确认素材只针对一个诊断瓶颈，且与落地页一致。
2. A/B 除目标变量外保持受众、预算、页面和时段尽量一致。
3. 视觉证据支持批准主张，不制造评分、用户或检测结果。
4. 用点击、页面行为和转化共同判断，不只看CTR。
5. 记录假设、版本、任务 ID、样本量与停止原因。

## 助手边界

脚本可从文字或用户指定图片生成，固定使用 Nano Banana Pro 图片模型并保存结果。带 Key 请求固定发往 `https://ai-hive.iclip.cn/api`，不允许自定义接口。无聊天、视频、账户或余额功能。

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name high-conversion-ad-image-generation-editing
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

“高转化”是实验方向而非保证；平台名称只表示投放环境，发布前需复核实时政策。
