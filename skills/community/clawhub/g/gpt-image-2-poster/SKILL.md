---
name: gpt-image-2-poster
description: "使用 GPT Image 2 制作信息层级清晰的活动、产品上市、促销、招聘、展览、会议和双语海报，并为标题、日期、地点、CTA和法律信息预留可校对版式。Use this skill for GPT Image 2 poster design、AI海报、活动海报、产品发布、展览海报、会议海报、促销海报、招聘海报、中文文字和双语排版；通过 AI Hive 生成。"
---

# GPT Image 2 海报生成

固定使用 `public_model_gpt_image_2`。先建立信息层级，再生成视觉与版式底图。把标题、日期、地点、价格、二维码、主办方和法律文字视为数据字段；关键字段必须逐字校对，不能容错时生成无字底图并在设计工具中排版。

## 海报信息表

按优先级记录：主标题、单一行动、日期/时区、地点、受众、主视觉、次级信息、Logo、二维码、版权与输出尺寸。每个字段指定精确字符、换行、大小写、位置和禁止改写项。

## 场景与代码

### 1. 文化活动海报

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '制作竖版当代舞活动海报底图：两位舞者形成对角线动态剪影，深蓝到紫色渐变与克制粒子感，左上留活动名，右下留日期、地点和购票区。不要生成任何文字、Logo、二维码、票价或赞助商' \
  --param aspect_ratio=3:4
```

### 2. 产品上市海报

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '为参考智能手表制作新品上市海报：商品位于右侧55%，黑色玻璃与银色金属质感清楚，左侧依次留产品名、核心卖点和CTA区域。保持表盘、表壳、表带、按钮与Logo，不生成文字、价格、发布日期、功能界面或认证' \
  --image /path/to/watch.png \
  --param aspect_ratio=4:5
```

### 3. 促销信息海报

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '生成商场夏季促销海报底版：亮黄与湖蓝几何层叠，中间保留折扣主标题区，下方依次留活动日期、参与条件与按钮区，两侧用抽象购物袋轮廓平衡构图。不生成折扣数字、日期、品牌、商品、价格或二维码' \
  --param aspect_ratio=3:4
```

### 4. 会议议程海报

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '制作人工智能行业论坛竖版海报底图：冷灰背景、精密网格和一条青色数据流，顶部留会议名称和主题，中段留四位嘉宾头像位，底部留日期、地点和报名二维码位。不要生成真实人物、文字、Logo、二维码或虚假科技界面' \
  --param aspect_ratio=2:3
```

### 5. 中英双语展览海报

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '为纤维艺术展生成极简双语海报底图：白色空间中悬浮半透明织物，柔和侧光和细腻阴影；上方预留中文主标题，下方预留英文标题、日期、地点与主办方。版式留白清楚，不生成任何字符、Logo、二维码或艺术家姓名' \
  --param aspect_ratio=4:5
```

## 排版与校对

1. 按信息表检查层级：三秒内读到主标题与行动，一次滚动内找到日期地点。
2. 逐字符核对中英文、数字、大小写、标点、空格、时区和换行。
3. 检查二维码静区、Logo安全区、出血、平台 UI 与印刷裁切线。
4. 确认商品、人物和活动事实来自批准资料，无虚构主办方或嘉宾。
5. 同时导出线上与印刷版本，分别检查颜色、分辨率和最小字号。

## 执行

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name gpt-image-2-poster
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

支持参考图、批量、比例参数、路由与输出目录。关键活动信息使用批准真源后期排版，并保留校对记录与终稿版本。
