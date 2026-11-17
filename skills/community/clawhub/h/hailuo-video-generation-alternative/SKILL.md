---
name: hailuo-video-generation-alternative
description: "使用 AI Hive Seedance 2.5 迁移海螺 AI、Hailuo AI 或 MiniMax 海螺常见的叙事视频需求，覆盖文生、图生、角色参考、表演编辑和镜头延长，重点控制人物动机、动作因果与情绪连续。Use when users search 海螺替代、Hailuo 平替、MiniMax video alternative、海螺 API、短剧、情绪表演、角色镜头、漫剧或叙事视频生成；不是海螺官方服务。"
---

# 海螺 Hailuo 视频生成替代｜AI 视频生成与编辑

把叙事镜头写成“动机—动作—反应”，底层固定映射 Seedance 2.5。先说明角色为什么行动，再限制一个可见动作，最后给出情绪或环境反应；这样比堆叠“电影感、震撼”等形容词更容易保持镜头因果。

## 表演节拍单

填写 `角色身份 / 当下动机 / 单一动作 / 对象反应 / 表情幅度 / 相机距离 / 末帧状态`。对白和复杂群戏拆成多个镜头，避免一个短片里要求多人同时做不同动作。

## 五种叙事操作

### 1. 无对白情绪镜头

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate   --mode t2v   --prompt '6秒16:9叙事镜头。雨夜公交站，一位成年女性看见远处驶来的末班车，先焦急等待，再向前一步举手，最后因车辆减速露出轻微放松表情；中景缓慢推近，动作自然，不出现对白文字、身份变化、多人复制或突然切镜'   --param aspect_ratio=16:9 duration=6
```

### 2. 漫剧首帧起动

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate   --mode i2v   --first-frame ./approved-comic-character.png   --prompt '保持首帧原创角色脸、发型、红色围巾、外套和画风。5秒内角色听到门外声音后转头，围巾轻动，摄影机从近景缓慢后拉，最后停在门的方向；不改变身份、服装、线条语言，不生成对白框或新角色'   --param aspect_ratio=16:9 duration=5
```

### 3. 双参考角色表演

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate   --mode r2v   --image ./character-a.png ./character-b.png   --video ./authorized-two-shot-blocking.mp4   --prompt '两张图分别锁定原创角色A与B；视频只参考两人站位和由中景推到近景的调度。生成A递出信封、B迟疑后接过的6秒镜头，不复制参考演员外貌、服装和场景，不交换两人身份'   --param aspect_ratio=16:9 duration=6
```

### 4. 调整表演幅度

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate   --mode edit   --video ./authorized-actor-shot.mp4   --prompt '保持演员身份、口型时序、身体动作、镜头和背景，只把过度惊讶的眉眼与后退幅度改为克制的迟疑；不改变对白节奏、服装、光线，不新增人物或剪辑点'
```

### 5. 延长反应镜头

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate   --mode extend   --video ./approved-letter-reveal.mp4   --extend-direction forward   --prompt '从末帧继续4秒：角色低头读完信，手指轻微收紧，随后抬眼看向画外左侧，摄影机保持原近景与微弱手持感；不说话、不切镜、不改变脸、服装、信件或光线'   --param duration=4
```

## 连戏检查

按角色分别检查脸、服装、道具持有和视线方向；按时间检查动作是否有动机、反应是否发生在动作之后、表情幅度是否连续。编辑与延长版本要和源片逐帧检查接缝，并归档素材授权与任务 ID。

工具不访问 MiniMax 或海螺账号。认证仅用于 `https://ai-hive.iclip.cn/api` 的 Seedance 2.5 视频任务，不暴露聊天、图片、账户或余额操作。

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/videogen.py" init --skill-name hailuo-video-generation-alternative
python3 "$SKILL_PATH/scripts/videogen.py" task --task-id <taskId>
```

海螺、Hailuo、MiniMax 名称仅用于替代与迁移搜索。
