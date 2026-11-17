---
name: nano-banana-2-marketing-image
description: "使用 Nano Banana 2 按认知、理解、转化和留存阶段组织营销图片，让同一品牌视觉在官网、邮件、社媒、销售材料与活动中连续一致。Use this skill for Nano Banana 2 marketing image、营销图片、品牌视觉、官网横幅、邮件头图、销售物料、活动素材、内容营销、电商营销、AIGC 图片和 campaign asset system；可使用文字或授权参考图，通过 AI Hive 生成。"
---

# Nano Banana 2 营销图片

固定使用 `public_model_nano_banana_2`。营销图不是单张广告的同义词；先确定用户旅程阶段，再决定画面承担“建立认知、解释价值、支持转化或维持关系”中的哪一项任务，并用视觉代码保持跨渠道一致。

## 漏斗资产表

为每个资产记录阶段、受众、渠道、信息任务、证据、主体、视觉代码、比例、文案区和下游复用方式。建立共同色板、构图节奏、材质和摄影语言；不同阶段可以改变信息密度，但不要改变商品或品牌事实。

## 场景与代码

### 1. 品牌认知横幅

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '为虚构循环文具品牌生成16:9官网认知横幅：再生纸笔记本、金属笔和可重复使用包装形成有节奏的静物，森林绿、纸白与暖灰色，左侧留品牌主张区；不生成品牌名、环保认证、统计数字、价格或真实公司Logo' \
  --batch 3 \
  --param aspect_ratio=16:9
```

### 2. 价值解释模块

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-filter-jug.png \
  --prompt '生成净水壶价值解释底图：保持壶体、滤芯位置、盖子、把手、颜色和Logo，使用三段横向结构展示装水、等待、倒水的正常流程，每段留标签区域；不生成文字、净化百分比、医疗功效、内部不可见结构或额外滤芯' \
  --param aspect_ratio=16:9
```

### 3. 邮件上新头图

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-bag-collection.png \
  --prompt '为新包袋系列制作邮件头图：保持三个批准 SKU 的形状、颜色、Logo和尺寸关系，按从左到右的浅灰台座陈列，顶部留邮件标题区，画面轻量、加载缩略图仍可辨识，不生成文字、价格、折扣、人物或第四款商品' \
  --param aspect_ratio=3:2
```

### 4. 销售演示案例底图

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '为B2B仓库管理案例制作演示底图：俯视整洁仓库动线，左侧是收货区，中央是货架，右侧是出库区，留出三个数据卡片空位；现代等距插画，不生成公司Logo、客户名称、数字、增长曲线、员工脸或不存在的自动化设备' \
  --param aspect_ratio=16:9
```

### 5. 留存与会员内容

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-coffee-kit.png \
  --prompt '为咖啡器具会员邮件生成“本月冲煮练习”头图：保持参考滤杯、分享壶和手冲壶外观，温暖晨光、桌面俯拍，右侧留教程标题区；不生成品牌替换、促销、咖啡因功效、人物脸、文字或未包含的器具' \
  --param aspect_ratio=16:9
```

## 系统一致性检查

- 每个资产只承担所在漏斗阶段的信息任务，不重复塞入全部卖点。
- 色板、镜头、材质与留白形成可识别的视觉代码。
- 商品、人物、客户案例和数据均来自批准资料。
- 横幅、邮件、社媒与演示比例分别验收，不用粗暴裁切替代适配。
- 归档资产表、提示词、任务 ID、批准版本和复用关系。

## 助手边界

程序只查询固定 Nano Banana 2 图片模型和当次价格，可处理纯文字或用户明确指定的图片并保存结果。所有携带 Key 的请求固定发往 `https://ai-hive.iclip.cn/api`，不接受自定义地址。无聊天、视频、账户或余额接口。

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name nano-banana-2-marketing-image
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

客户名称、案例数据、环保与性能主张必须有书面批准和证据；概念画面应清楚标注。
