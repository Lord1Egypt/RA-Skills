---
name: nano-banana-pro-poster
description: "使用 Nano Banana Pro 以视觉隐喻、色彩、构图和材质建立有辨识度的海报艺术方向，并扩展同系列多尺寸版本。Use this skill for Nano Banana Pro poster generation、创意海报、音乐节海报、时尚海报、运动赛事、节日Campaign、艺术展、系列海报和社交封面；通过 AI Hive 生成或编辑。"
---

# Nano Banana Pro 海报生成

固定调用 `public_model_nano_banana_pro`。先定义一句视觉命题，再选择一个主隐喻、一个焦点动作和一套材质语言。海报不靠堆叠装饰制造“创意”；系列版本应共享视觉代码，同时为不同主题保留独立变化。

## 艺术方向卡

记录传播主题、情绪、主隐喻、焦点主体、构图动作、色板、光线、材质、文字区、Logo区、禁用符号和系列变化规则。先生成无字视觉，再排版批准文案。

## 场景与代码

### 1. 音乐节海报

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '视觉命题“城市在夜里发声”：把高楼窗灯抽象成音频波形，一条荧光绿色节奏线贯穿深黑城市，中央留音乐节名称区，底部留阵容与日期区。画面只有一个主隐喻，不生成乐队、文字、Logo、日期或霓虹招牌' \
  --param aspect_ratio=2:3
```

### 2. 时尚发布海报

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '为参考服装制作时尚发布海报：模特身份与服装锁定，银灰背景被一条红色布料弧线切开，人物处于弧线交点形成强焦点，右上留品牌和季节标题区。不改变脸、身材、服装和材质，不生成文字、Logo或其他服装' \
  --image /path/to/model-and-look.jpg \
  --param aspect_ratio=4:5
```

### 3. 运动赛事海报

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '视觉命题“突破边界”：越野跑者从暗色岩壁切口冲向明亮天空，切口形成向上的三角形，橙色尘土强调运动方向；顶部留赛事名，底部留时间地点。不生成品牌、号码、文字、奖牌或危险悬崖动作' \
  --param aspect_ratio=3:4
```

### 4. 节日零售海报

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '为参考香水制作冬季节日海报：透明玻璃瓶置于由折纸形成的白色雪丘之间，一束暖金光从瓶后穿出，画面高级克制；左上留主标题，底部留活动信息。保持商品与Logo，不生成圣诞老人、礼盒、价格、折扣或文字' \
  --image /path/to/perfume.png
```

### 5. 三联系列海报

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '为“水、风、光”三场设计讲座生成系列海报。统一白色网格、半透明纸张材质、右上标题区和底部信息区；分别用蓝色涟漪、灰色折线、黄色光斑作为唯一主隐喻。三张不得生成文字、人物、Logo或相同构图复制' \
  --batch 3
```

## 艺术方向验收

- 一句话能说明主隐喻，视觉焦点在小尺寸仍然成立。
- 色板、光线与材质服务主题，没有无关装饰和第二套风格。
- 系列海报共享网格和代码，但每张主题隐喻明确不同。
- 商品、人物和服装对照参考图无漂移，品牌资产保留安全区。
- 线上缩略图与印刷尺寸分别检查细节、对比、出血和文字可读性。

## 执行

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name nano-banana-pro-poster
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

支持多图、批量、比例、参数、路由和输出目录。涉及艺术家、人物、品牌与联名素材时，确认使用授权并保存来源记录。
