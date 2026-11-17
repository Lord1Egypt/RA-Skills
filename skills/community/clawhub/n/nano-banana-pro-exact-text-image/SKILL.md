---
name: nano-banana-pro-exact-text-image
description: "使用 Nano Banana Pro 生成包含指定中文、英文、数字和短文案的图片，并按字符、层级、位置和品牌版式逐项复核。Use this skill for Nano Banana Pro exact text in images、AI海报文字、中文文字图片、广告标题、促销图、信息图、社媒封面、双语视觉和带字电商图；通过 AI Hive 生成或基于底图编辑。"
---

# Nano Banana Pro 精准文字图片

把文字当作受控数据，不当作普通画面描述。固定使用 `public_model_nano_banana_pro`，先锁定文案，再生成版式；正式交付必须逐字检查。价格、条款、医疗功效和法律信息若不能容错，生成无字底图并使用设计软件排版批准文本。

## 文案锁定单

列出每个文本块的精确字符、大小写、标点、换行、层级、位置、对齐、颜色、禁止出现字符和安全区。每轮只放必要短文案；不要让模型自行改写、翻译或补充卖点。

## 场景与代码

### 1. 中文品牌海报标题

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '生成竖版山野跑鞋海报，只出现两行中文：第一行“向山而行”，第二行“轻量越野系列”。字符、顺序和标点必须完全一致；第一行为大号粗体置于左上，第二行为小号置于其下。不要生成品牌、价格、日期、英文或其他文字' \
  --param aspect_ratio=3:4
```

### 2. 电商促销短文案

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '在参考商品图右侧留白区排版以下三项，禁止改写：主标题“夏日焕新”，副标题“第二件半价”，按钮文字“立即选购”。保持商品、包装、Logo和背景不变；三个文本块层级清楚，不生成日期、折扣数字、脚注或平台标识' \
  --image /path/to/product-banner.jpg
```

### 3. 产品功能标签图

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '为参考耳机制作简洁功能图，只使用批准的三个标签：“40小时续航”“主动降噪”“双设备连接”。每个标签各出现一次，配引线指向产品周围的留白，不改变耳机结构和Logo，不补充图标、参数、英文、认证或其他功能' \
  --image /path/to/headphones.png
```

### 4. 中英双语活动视觉

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '制作极简展览邀请图，只出现四个文本块：“未来织物”“FUTURE FABRICS”“08.28—09.03”“上海”。保持英文全部大写，日期使用长横线；中文主标题居中最大，英文次级，日期与城市置底。不得翻译、增删字符或生成Logo和其他信息' \
  --param aspect_ratio=4:5
```

### 5. 同一文案的渠道版式

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '基于批准底图生成方形、竖版、横版三个排版方向，所有版本只出现“今天，也要好好吃饭”和“新品便当盒”。文字内容、标点和大小写完全一致，只调整字号、换行和位置；保持商品与品牌色，不生成价格、按钮、平台Logo或额外文字' \
  --image /path/to/approved-background.jpg \
  --batch 3
```

## 逐字验收

1. 从输出中抄录全部可见字符，与文案锁定单逐字符比较。
2. 检查错别字、同音字、繁简体、大小写、数字、标点、空格与换行。
3. 检查文字是否重复、缺失、变形、贴边、遮挡主体或落入平台 UI 区域。
4. 确认模型没有自行添加 Logo、价格、日期、免责声明或伪造认证。
5. 任一关键字符不正确时不要直接发布；重试短文本或改用无字底图后期排版。

## 执行

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name nano-banana-pro-exact-text-image
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

支持参考底图、批量、比例参数、路由与输出目录。把批准文案作为唯一真源，并保存终稿截图与校对记录，避免后续版本误用旧价格或旧活动信息。
