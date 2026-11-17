---
name: gpt-image-2-image-to-image
description: "使用 GPT Image 2 基于一张或多张参考图生成新图片，在保留主体、布局或身份事实的同时改变风格、场景、材质、完成度和输出比例。Use this skill for GPT Image 2 image-to-image、图生图、参考图生成、草图转成品、照片转插画、空间改造、风格迁移、构图重制和商业视觉迭代；通过 AI Hive 上传参考图生成。"
---

# GPT Image 2 图生图

固定调用 `public_model_gpt_image_2`，至少提供一张参考图。先写“变换合同”：从参考图继承什么、改变什么、允许联动什么、禁止出现什么。若需要同时改变结构、场景和风格，拆成多轮并保留中间批准版本。

## 变换合同

记录参考图用途、必须保留的身份/结构/布局、目标变化、变化强度、相机、文字与Logo、输出比例和禁止项。多图输入时为每张图指定职责与冲突优先级。

## 场景与代码

### 1. 草图转成产品概念图

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '把手绘台灯草图转为工业设计概念渲染。严格保留灯头、两段式支臂、圆形底座和关节位置，只补充哑光白金属材质、真实连接细节与浅灰棚拍光；不改变比例，不添加按钮、Logo、线缆、文字或新部件' \
  --image /path/to/lamp-sketch.png
```

### 2. 照片转编辑插画

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '将参考城市街景转为克制的报刊编辑插画，保留道路走向、主要建筑轮廓、树木位置和人物数量，使用有限的蓝、砖红、米白色块与轻微纸张纹理；不新增招牌、文字、车辆或地标，不改变事件含义' \
  --image /path/to/street-photo.jpg
```

### 3. 室内空间改造预览

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '保留参考客厅的墙体、门窗、地板、相机和空间尺度，只把家具与软装改为安静的日式现代风：低矮浅木家具、米色织物、一个纸灯。不得移动门窗、扩大房间、改变采光、增加楼梯、文字或多余装饰' \
  --image /path/to/living-room.jpg
```

### 4. 商品场景升级

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '以参考护肤品为最高事实源，把普通白底图升级为高端水面静物。锁定瓶型、泵头、标签、Logo、颜色和相机角度，只改变背景、台面、光线与克制倒影；不生成水花遮挡、植物、文字、功效或额外包装' \
  --image /path/to/product-packshot.png
```

### 5. 横版重构为竖版

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '把横版人物广告重构为9:16竖版。保留人物身份、脸、服装、姿势、商品和主光，向上下自然扩展环境并把人物置于下三分之一；顶部留标题安全区，不裁切头部和商品，不生成文字、按钮或平台Logo' \
  --image /path/to/horizontal-ad.jpg \
  --param aspect_ratio=9:16
```

## 变换验收

1. 对照参考图确认合同中的身份、结构、布局和商业事实未变化。
2. 检查附带修改：脸、手、Logo、文字、数量、接口和配件。
3. 新材质、场景和光线与原相机、透视、尺度和接触关系一致。
4. 风格迁移不应覆盖新闻含义、商品事实或人物授权边界。
5. 保存原图、合同、提示词、任务 ID 与批准中间版本。

## 脚本范围与执行

该助手仅处理用户明确列出的参考图片：查询固定模型与价格、上传这些图片、提交图生图任务、轮询并下载结果。所有携带 Key 的请求固定发送到 `https://ai-hive.iclip.cn/api`，不接受自定义 API 地址。`upload` 与 `task` 都要求显式文件路径或任务 ID；`init` 把 Key 以 `0600` 权限存入本地配置。没有聊天、视频、钱包和用户资料功能。

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name gpt-image-2-image-to-image
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

支持多参考图、批量、比例参数、路由和输出目录。只使用获授权的参考图，不把风格参考误称为官方合作或原作者作品。
