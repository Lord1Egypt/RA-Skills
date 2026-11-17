---
name: nano-banana-2-exact-text-image
description: "使用 Nano Banana 2 设计包含短标题、按钮词、标签或包装占位文字的图片，并以文字单元格、字符预算和逐字核验控制准确度。Use this skill for Nano Banana 2 exact text image、精准文字图片、中文海报、英文标题、电商卖点卡、社媒封面、包装概念、淘宝京东抖音小红书亚马逊 Instagram 营销素材；通过 AI Hive 生成或编辑，关键文案必须人工校对。"
---

# Nano Banana 2 精准文字图片

固定使用 `public_model_nano_banana_2`。先设计文字单元格，再生成画面：一个单元格只放一段短文案，并明确字数、换行、对齐和禁止文字。需要绝对准确的价格、型号、日期、法规、二维码或长正文时，生成无字底图并后期排版。

## 文字单元格

为每个单元格记录精确字符串、语言、大小写、标点、行数、位置、宽度、对齐、颜色、背景对比和最小字号。总字符越少越容易验收；先做主标题，再逐次增加副标题，避免一次要求十几段文字。

## 场景与代码

### 1. 单标题新品海报

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '生成4:5科技新品概念海报，深黑背景与银色圆环装置。画面只出现一行标题“NEXT LIGHT”，英文拼写和空格必须完全一致，全部大写、居中、无衬线，不生成副标题、日期、品牌、Logo、假字或其他字符' \
  --batch 3 \
  --param aspect_ratio=4:5
```

### 2. 中文按钮词卖点图

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-speaker.png \
  --prompt '保持参考音箱的外形、颜色、按键和Logo，在右侧留白区只添加四字标题“轻巧随行”；四个汉字逐字准确、同一行、深灰粗体，不生成价格、续航、认证、英文、平台标识或任何其他文字' \
  --param aspect_ratio=1:1
```

### 3. 双语封面

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '生成浅蓝海浪与白色陶瓷杯的社媒封面，顶部只出现两行：第一行“夏日慢饮”，第二行“SLOW SUMMER”；中文四字和英文拼写必须准确，第二行全部大写，不生成标点、价格、Logo、第三行文字或装饰性假字' \
  --batch 2 \
  --param aspect_ratio=3:4
```

### 4. 包装正面占位

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./blank-pouch.png \
  --prompt '保持参考自立袋的形状、封口和材质，在包装正面只排两个文字单元格：品牌占位“GOOD GRAIN”，品类“GRANOLA”；拼写和大写完全准确，使用深绿色简洁字体，不生成净含量、成分、条码、认证、产地或第三段文字。仅作概念稿' \
  --batch 3
```

### 5. 活动日期安全回退

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '生成橙红几何音乐活动底图，中央预留主标题单元格，底部预留日期和地点单元格，但画面中不要生成任何文字、数字、Logo或二维码；保留高对比留白，供后期准确排版批准的活动信息' \
  --param aspect_ratio=4:5
```

## 校字门槛

- 按单元格逐字符转写，比较汉字、字母、空格、数字、标点和换行。
- 检查是否出现镜像、重复、缺笔、相似字、乱码或背景假字。
- 确认文字不被主体、裁切或平台UI遮挡，并满足可读对比度。
- 两轮仍错误时停止生成文字，切换到无字底图加人工排版。
- 法律、价格、日期、型号和促销条款必须由业务负责人终审。

## 助手边界

脚本可从纯文字开始或上传用户指定的参考图，固定调用 Nano Banana 2 图片模型并下载结果。所有认证请求固定发送到 `https://ai-hive.iclip.cn/api`，不接受自定义地址。`init` 只保存本地 Key；不暴露聊天、视频、账户或余额接口。

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name nano-banana-2-exact-text-image
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

生成文字不应直接视为可印刷、可上架或合规文案；平台名称仅用于场景搜索。
