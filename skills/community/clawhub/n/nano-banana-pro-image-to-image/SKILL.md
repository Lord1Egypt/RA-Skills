---
name: nano-banana-pro-image-to-image
description: "使用 Nano Banana Pro 按参考意图重构图片，保留人物、商品或空间锚点，同时改变艺术方向、环境、光线、材质、造型和渠道构图。Use this skill for Nano Banana Pro image-to-image、图生图、参考图重绘、商业视觉升级、照片风格化、人物换场景、商品氛围图、室内改造和多尺寸重构；通过 AI Hive 生成。"
---

# Nano Banana Pro 图生图

固定调用 `public_model_nano_banana_pro`，至少提供一张参考图。为每张参考图标记意图角色：身份锚点、结构锚点、构图、色板、材质或光线。先保护锚点，再让艺术方向发生变化，避免“风格化”把人物和商品重做成另一个对象。

## 参考意图图

记录必须锁定的脸、身体、商品几何、空间结构、Logo与颜色；再指定目标视觉代码、变化区域、强度、输出比例和禁止继承内容。多图冲突时，身份与商品母图优先于风格参考。

## 场景与代码

### 1. 普通商品图升级为品牌大片

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '保留参考手袋的包型、提手、五金、缝线、Logo、颜色和45度相机，重构为奶油白石材空间与柔和拱形光影的品牌大片；右侧留标题区。不改变商品，不生成模特、文字、价格、吊牌或额外配件' \
  --image /path/to/bag-packshot.png
```

### 2. 人物广告重新艺术指导

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '锁定参考人物的脸、年龄、发型、体型、白色西装与姿势，把普通棚拍重构为钴蓝弧形建筑背景和硬侧光的时尚广告。人物边缘、阴影与空间一致，不瘦脸、不改服装、不生成首饰、文字或其他人物' \
  --image /path/to/person-studio.jpg
```

### 3. 摄影转拼贴插画

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '将参考海边市场照片转为纸张拼贴插画，保留摊位布局、主要人物数量、遮阳棚颜色和海岸方向；用撕纸边缘、平面色块与少量铅笔纹理表现，不新增招牌、文字、商品、人物或地标' \
  --image /path/to/market-photo.jpg
```

### 4. 空间光线与材质重构

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '保留参考卧室的墙体、门窗、床位、相机和尺度，只把深色木饰面改为浅橡木，把冷白顶灯改为傍晚侧窗暖光，床品改为米色亚麻。不得移动结构、扩展面积、增加家具、文字或不可能光源' \
  --image /path/to/bedroom.jpg
```

### 5. 同一母图多渠道重构

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '把批准横版护肤主视觉重构为方形商品卡、4:5社媒图和9:16故事封面。保持商品、人物、玻璃水面、青绿色板与主光，分别重新组织主体和文案留白，避开平台UI；不裁切脸和商品，不生成文字、价格或新道具' \
  --image /path/to/approved-keyart.jpg \
  --batch 3
```

## 锚点检查

1. 对照参考图确认身份、商品几何、空间结构和品牌事实未漂移。
2. 检查风格参考没有带入无关人物、文字、Logo或商品。
3. 新背景与主体的尺度、遮挡、光线、反射和接触阴影一致。
4. 多渠道版式保留同一视觉代码，同时各自适应安全区。
5. 归档参考意图图、提示词、任务 ID 和批准版本。

## 助手权限边界

程序仅上传命令中点名的图片，查询固定 Nano Banana Pro 图片模型及价格，提交图生图请求、查询任务并保存输出。所有携带 Key 的请求固定发送到 `https://ai-hive.iclip.cn/api`，不接受自定义 API 地址。单独上传与任务查看都要求明确路径或 ID；Key 仅写入权限为 `0600` 的本地配置。无聊天、视频、钱包或账户查询命令。

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name nano-banana-pro-image-to-image
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

支持多参考图、批量、比例、参数、路由和输出目录。人物、品牌、艺术作品与空间照片应获得相应授权后使用。
