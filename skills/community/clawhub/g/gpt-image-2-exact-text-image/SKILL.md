---
name: gpt-image-2-exact-text-image
description: "使用 GPT Image 2 生成包含指定中文、英文、数字或多语言文案的海报、包装、菜单、信息图和广告图片，并执行逐字校验。Use this skill for GPT Image 2精准文字图片、中文海报、英文广告、包装文字、菜单、标题图、信息图、多语言本地化、文字替换和商业设计；通过 AI Hive 生成与编辑。"
---

# GPT Image 2 精准文字图片

把文案视为不可改写的数据，而不是创意建议。固定使用 `public_model_gpt_image_2`。模型生成后必须逐字、逐数字、逐标点人工核对；高风险法律、价格、医疗或金融文字不应只靠图片模型定稿。

## 文案锁定表

为每段文字记录：精确内容、语言、大小写、标点、换行、层级、位置、对齐和不可变部分。先压缩文案，再生成版式；复杂正文优先生成留白底图后由专业排版工具完成。

## 场景与代码

### 1. 中文商业海报

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '竖版商业海报，必须逐字出现主标题“让创意快速落地”，副标题“AI 视觉工作流体验日”，日期“2026.09.12”。保持中文笔画清楚，三段文字不得改写、增删或重复；主标题上方居中，副标题与日期分层，下方留CTA区域，不生成其他文字' 
```

### 2. 英文广告与大小写

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt 'Square product ad. Render the exact headline “MAKE EVERY DETAIL COUNT.” and subline “Designed for focused work.” Preserve capitalization, punctuation and spelling exactly. Headline top-left, subline beneath it, product on right. Generate no price, badge, legal copy or additional word.'
```

### 3. 包装文字修改

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '编辑包装正面：保留包装结构、Logo、颜色、插画、条码区域和所有其他文字，只将原口味名称替换为准确中文“青柠薄荷”，保持原字号、位置、材质印刷和透视，不修改配料、净含量或品牌' \
  --image /path/to/package.png
```

### 4. 菜单与价格留白

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '生成咖啡店菜单视觉底图，必须出现三个栏目标题“咖啡”“茶饮”“甜点”，栏目标题逐字准确；每栏下方只留整齐空白行供人工填写品名和价格，不生成菜单项、数字、货币符号或装饰性伪文字' 
```

### 5. 多语言本地化海报

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '将参考英文海报本地化为日文版，保留商品、品牌、构图和色彩，只使用商家批准的准确标题「毎日を、もっと軽やかに。」；删除全部旧英文，不自动翻译其他文字，为法律与价格信息留白' \
  --image /path/to/english-poster.jpg
```

## 文字 QA

1. 将生成图放大，逐字核对内容、笔画、拼写、数字和标点。
2. 检查大小写、换行、重复、缺字和伪文字。
3. 与文案锁定表对照位置、层级和对齐。
4. 商品、Logo、包装和背景没有因改字发生漂移。
5. 高风险价格、法律、认证和说明文字用排版工具重新制作。
6. 保存可编辑文案源与最终人工校对记录。

## 执行

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name gpt-image-2-exact-text-image
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

支持参考图、批量、模型参数、路由与仅提交任务。需要多版文案时每次只改变一个锁定字段。
