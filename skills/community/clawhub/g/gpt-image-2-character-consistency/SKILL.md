---
name: gpt-image-2-character-consistency
description: "使用 GPT Image 2 建立角色设定并在不同姿势、表情、服装、镜头和场景中保持身份一致。Use this skill for GPT Image 2角色一致性、人物设定、角色三视图、表情表、绘本角色、短剧人物、漫画分镜、品牌IP、虚拟人和连续图片；通过 AI Hive 上传角色参考并生成。"
---

# GPT Image 2 角色一致性图片

先建立可核验的角色“身份锚点”，再扩展动作和场景。固定调用 `public_model_gpt_image_2`。一致性不是让每张图完全相同，而是在年龄、五官比例、发型、体态与核心服装等身份特征上稳定。

## 角色圣经

记录：

- 年龄范围、脸型、眼鼻嘴比例与辨识特征。
- 发型、发色、肤色、身高体态与常用姿势。
- 核心服装、配色、配饰与禁止变化项。
- 画风、线条、材质、光线和色彩基准。
- 场景可变项和剧情阶段允许的变化。

优先生成中性正面、侧面、全身和表情基准，批准后再做场景图。

## 场景与代码

### 1. 角色三视图

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '根据角色参考生成设定三视图：正面、侧面、背面，中性站姿与中性表情，统一比例和光线。必须保持年龄、脸型、五官、短卷发、左眉小痣、身高体态、蓝色夹克和银色胸针一致，不增加文字和其他人物' \
  --image /path/to/character-reference.png
```

### 2. 表情表

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '为同一角色生成六格表情表：平静、喜悦、担忧、惊讶、愤怒、疲惫。锁定脸型、五官比例、眉间特征、发型、肤色和年龄，只改变合理面部肌肉和眼神，不改变身份、发长或画风' \
  --image /path/to/approved-character.png
```

### 3. 新场景中的同一角色

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '保持参考角色身份、体态、蓝色夹克和银色胸针，生成其在雨夜车站查看地图的中景。新场景只改变动作、环境和光线，脸部辨识特征、服装结构与画风必须一致，不增加第二人物' \
  --image /path/to/approved-character.png
```

### 4. 合理换装但身份不变

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '角色身份、脸部、发型、年龄、体态和银色胸针保持不变，将蓝色夹克换为参考图中的正式黑色礼服；礼服顺应角色比例和姿势，不复制服装参考中的人物、脸和背景' \
  --image /path/to/character.png \
  --image /path/to/outfit-reference.jpg
```

### 5. 双角色连续分镜

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '图1锁定角色A，图2锁定角色B。生成两人在图书馆隔桌交谈的连续分镜，A与B的五官、发型、体态、服装和配饰互不混淆，保持相对身高与座位关系，不生成第三人物' \
  --image /path/to/character-a.png \
  --image /path/to/character-b.png \
  --batch 3
```

## 一致性验收

- 与角色圣经逐项核对，而不是只凭“像不像”。
- 五官比例、年龄、发型、体态与标志物稳定。
- 表情和动作变化不改变身份。
- 多角色没有特征、服装和配饰串用。
- 场景光线可以变化，但画风和材质语言一致。
- 保存批准角色基准与每次使用的参考图顺序。

## 执行

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name gpt-image-2-character-consistency
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

固定使用 GPT Image 2，支持多参考图、批量和实时参数。角色发生剧情性变化时创建新基准版本，而不是覆盖旧设定。
