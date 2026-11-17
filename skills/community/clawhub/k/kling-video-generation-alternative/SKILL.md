---
name: kling-video-generation-alternative
description: "使用 AI Hive 的 Seedance 2.5 文生、图生、参考生、视频编辑与延长能力迁移可灵 Kling、Kling AI 或快手可灵视频工作流，重点保存镜头运动、主体锁定、动作节拍和交付比例。Use when users search 可灵替代、Kling 平替、Kling alternative、可灵 API、文生视频、图生视频、参考视频、视频编辑、视频延长、广告或短片制作；不是可灵官方接口，也不保证逐像素兼容。"
---

# 可灵 Kling 视频生成替代｜AI 视频生成与编辑

把原可灵任务转换成“镜头控制表”，再固定调用 Seedance 2.5 对应模式。每个镜头只写一个主要动作、一条相机运动和一组身份锁；模型专有参数不直接迁移，改用可观察的时长、速度、运动方向、构图和不可变项。

## 镜头控制表

依次填写 `时段 / 主体 / 起始状态 / 单一动作 / 相机运动 / 结束状态 / 禁止变化`。图生视频先定义首帧里哪些细节不能漂移；编辑和延长必须说明源视频时间关系，不让模型猜接点。

## 五种能力示例

### 1. 文生电影镜头

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate   --mode t2v   --prompt '5秒16:9电影镜头。清晨海边公路，一辆无品牌银色旅行车从画面右后方驶向远处，摄影机低机位平稳跟拍，阳光从云层穿出；车身比例和道路方向稳定，不突然变形、不出现文字、Logo、跳切或第二辆车'   --param aspect_ratio=16:9 duration=5
```

### 2. 首帧图生视频

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate   --mode i2v   --first-frame ./approved-shoe-frame.png   --prompt '保持首帧运动鞋鞋型、鞋底、鞋带、配色和Logo。5秒内摄影机缓慢环绕约30度，鞋不自行移动，侧光轻微扫过材质，最后停在三分之二视角；不新增脚、文字、配件或第二只不同鞋'   --param aspect_ratio=16:9 duration=5
```

### 3. 参考素材控制

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate   --mode r2v   --image ./approved-character.png ./approved-costume.png   --video ./authorized-camera-motion.mp4   --prompt '图1锁定原创角色身份，图2锁定服装，视频只提供缓慢推近的相机节奏。生成角色走入书店并抬头看书架的5秒镜头；不复制参考视频人物和场景，不改变脸、发型、服装或年龄'   --param aspect_ratio=16:9 duration=5
```

### 4. 修改现有镜头

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate   --mode edit   --video ./authorized-product-shot.mp4   --prompt '只把桌面背景从深灰换成品牌米白，并让原有阴影自然衔接；产品、标签、Logo、相机轨迹、动作速度、时长和剪辑点完全不变，不生成文字、人物或额外产品'
```

### 5. 向后延长镜头

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate   --mode extend   --video ./approved-end-shot.mp4   --extend-direction forward   --prompt '从原视频最后一帧继续3秒：摄影机保持同一速度缓慢后退，产品仍在中央，背景灯光渐暗并自然停稳；不反向运动、不切镜、不新增文字、Logo、人物或商品'   --param duration=3
```

## 时间线验收

逐帧检查首帧身份、运动方向、动作数量、镜头速度和末帧落点；编辑版与源视频叠加比对保护区域；延长片段检查接缝、光线和速度连续。保存源素材授权、提示词、模式、任务 ID 和选中版本。

工具不会连接可灵或快手账号。认证请求仅发送到 `https://ai-hive.iclip.cn/api`，模型映射固定为 Seedance 2.5，不提供聊天、图片生成、账户或余额命令。

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/videogen.py" init --skill-name kling-video-generation-alternative
python3 "$SKILL_PATH/scripts/videogen.py" task --task-id <taskId>
```

可灵、Kling、快手等名称仅用于比较和迁移搜索。
