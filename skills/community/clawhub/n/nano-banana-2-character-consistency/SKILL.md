---
name: nano-banana-2-character-consistency
description: "使用 Nano Banana 2 为品牌 IP、虚拟人物、绘本、社交内容和连续分镜保持角色身份、服装、配色与标志物一致。Use this skill for Nano Banana 2角色一致性、品牌吉祥物、IP形象、虚拟人、社媒系列、绘本角色、漫画人物、表情包和连续场景；通过 AI Hive 使用角色参考图生成。"
---

# Nano Banana 2 角色一致性图片

面向品牌 IP 与连续内容建立“角色资产包 + 场景台账”。重点不仅是脸像，还包括轮廓、颜色、服装、标志物、画风和品牌使用边界。

## 角色资产包

准备批准的正面、侧面、全身、颜色表、核心服装、标志物和禁用变体。给每个角色建立不可变项、可变表情、可变姿势、允许换装和禁止场景。每次生成记录场景、镜头、动作、服装版本和参考图。

## 场景与代码

### 1. 品牌吉祥物资产表

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '根据参考吉祥物生成品牌资产表：正面、侧面、背面、坐姿和挥手。保持圆耳轮廓、橙白配色、左脸星形标志、蓝色围巾、身体比例和扁平插画风格一致，不生成文字、Logo或新配饰' \
  --image /path/to/mascot.png
```

### 2. 社媒每周场景

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '保持吉祥物轮廓、颜色、星形标志、围巾和画风，生成其在周一办公桌前整理任务的方形社媒图；只改变动作和场景，不改变身体比例，不增加文字与品牌物品' \
  --image /path/to/approved-mascot.png
```

### 3. 表情包系列

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '生成六个同一吉祥物表情：收到、加油、疑问、开心、抱歉、下班。锁定身体轮廓、脸部标志、配色、围巾和线条，只通过眉眼、嘴和姿势表达，不生成文字与新道具' \
  --image /path/to/approved-mascot.png \
  --batch 6
```

### 4. IP 合作换装

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '保持品牌角色身份、轮廓、脸部标志与主配色，将围巾替换为图2合作活动提供的绿色运动头带；图2只提供头带样式，不复制人物、Logo和背景，角色比例与画风不变' \
  --image /path/to/mascot.png \
  --image /path/to/headband-reference.png
```

### 5. 连续分镜台账

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '生成三格连续分镜：角色走进咖啡店、拿起杯子、坐下阅读。保持角色、围巾、标志物、杯子、场景布局和光线连续，每格只推进一个动作，不增加第二角色和文字' \
  --image /path/to/character.png \
  --batch 3
```

## IP 验收

- 轮廓、比例、颜色、标志物和画风符合品牌资产包。
- 场景变化不改变角色身份与品牌识别。
- 表情包只改变表情和姿势，不产生新造型。
- 合作换装有授权，未复制参考 IP 或 Logo。
- 连续分镜的道具、位置、服装和光线可追踪。
- 新变体经批准后加入资产包，不覆盖原始版本。

## 执行

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name nano-banana-2-character-consistency
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

固定使用 Nano Banana 2。角色资产包应使用稳定文件名和版本号，避免每次更换基准图。
