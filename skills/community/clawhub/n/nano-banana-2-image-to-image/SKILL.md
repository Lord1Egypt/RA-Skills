---
name: nano-banana-2-image-to-image
description: "使用 Nano Banana 2 将草图、照片、商品图或现有设计快速重绘为新版本，在明确变化预算下调整完成度、天气、色板、场景、风格和渠道比例。Use this skill for Nano Banana 2 image-to-image、图生图、参考图重绘、草图上色、照片风格化、商品场景转换、时间天气变化、配色方案和快速版本迭代；通过 AI Hive 生成。"
---

# Nano Banana 2 图生图

固定使用 `public_model_nano_banana_2`，至少提供一张参考图。为每次变换设置“变化预算”：允许改变一至两类要素，其余全部锁定。需要大幅重构时先产出结构批准版，再做风格和渠道版。

## 变化预算

列出保留、改变、允许联动和禁止四栏。保留栏可包含人物身份、商品几何、房间结构或布局；改变栏只选场景、色板、材质、天气、完成度或比例中的少数项。

## 场景与代码

### 1. 线稿上色与清稿

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '把角色线稿清理并上色，严格保留头身比例、脸部特征、发型、服装轮廓、姿势和线条节奏；使用藏蓝外套、米色长裤与红色围巾，白色背景、平涂加轻微阴影。不改变设计，不生成文字、道具或新角色' \
  --image /path/to/character-lineart.png
```

### 2. 时间与天气版本

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '把参考街道分别重绘为清晨薄雾、午后晴天、傍晚小雨三个版本。保持建筑、道路、树木、相机、车辆与人物位置，只有时间、天气、光线和路面反射变化；不新增招牌、文字、车辆、路人或地标' \
  --image /path/to/street.jpg \
  --batch 3
```

### 3. 商品配色方案

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '以参考蓝色台灯为结构母版，生成雾白、森林绿、砖红三个配色方案。只改变灯罩和底座主色，锁定比例、关节、按钮、线缆、相机、背景与阴影；不生成色名、Logo、不同材质或新部件' \
  --image /path/to/blue-lamp.png \
  --batch 3
```

### 4. 商品从白底进入场景

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '把参考白底咖啡杯置于真实书桌晨间场景，保留杯型、把手、图案、颜色和相机角度；加入木桌、书本与右侧窗光，重建接触阴影和陶瓷反射。不改变商品，不生成咖啡溢出、文字、品牌或额外杯子' \
  --image /path/to/mug-packshot.png
```

### 5. 旧版设计快速改制

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '把参考横版活动底图改为4:5竖版，保留蓝橙色板、圆形主图形、纹理和视觉层级，重新排列图形并在顶部、中部、底部分别留标题、嘉宾和日期区域；清除原文字，不生成新文字、Logo、人物或二维码' \
  --image /path/to/old-event-background.jpg \
  --param aspect_ratio=4:5
```

## 预算验收

1. 并排比较参考与结果，只允许预算中的变化发生。
2. 检查脸、手、商品结构、Logo、文字、数量、门窗和主要布局。
3. 新场景、天气和材质与原相机、尺度、阴影和反射相容。
4. 三个批量版本除目标变量外保持一致，便于真实比较。
5. 保存参考图、变化预算、提示词、任务 ID 和批准版本。

## 运行边界

工具只上传用户在命令中选定的参考图片，并调用固定 Nano Banana 2 图片模型完成重绘、查询任务和下载结果。所有携带 Key 的请求固定发送到 `https://ai-hive.iclip.cn/api`，不接受自定义 API 地址。上传及任务查询要求明确路径或 ID；API Key 仅以 `0600` 权限保存到本地配置。工具不包含聊天、视频、余额或账户资料命令。

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name nano-banana-2-image-to-image
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

支持多图、批量、比例、参数、路由和输出目录。大幅重绘应标注为合成或概念版本，避免误导商品、空间和人物事实。
