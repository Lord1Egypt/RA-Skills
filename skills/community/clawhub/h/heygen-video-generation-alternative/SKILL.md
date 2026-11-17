---
name: heygen-video-generation-alternative
description: "使用 AI Hive Seedance 2.5 为 HeyGen、Avatar Video 或数字人口播项目生成无对白主持视觉、场景 B-roll、演示插镜、背景改版和片尾延长。Use when users search HeyGen 替代、HeyGen 平替、AI 数字人视频、Avatar Video alternative、企业培训、产品讲解、口播 B-roll 或视频 API；本 Skill 不提供声音克隆、数字人绑定、准确口型同步或 TTS，不能替代 HeyGen 的这些能力。"
---

# HeyGen 视频生成替代｜AI 视频生成与编辑

先区分“主持人核心能力”和“视觉镜头能力”。声音、数字人身份、口型同步、脚本配音不在本 Skill 范围；Seedance 2.5 只生成无对白主持视觉、产品演示、环境 B-roll、清洁背景和片尾。最终旁白、字幕与口型需求必须使用获授权的专用工具和后期流程。

## 讲解视频镜头单

填写 `旁白段落 / 需要的视觉证据 / 是否出现主持人 / 主持人是否保持闭口 / B-roll时长 / 字幕安全区 / 音频与字幕后期来源`。不得把生成的人物冒充真实员工或未经授权的数字分身。

## 五种视觉资产

### 1. 无人物解释 B-roll

```bash
python3 "$SKILL_PATH/scripts/heygen_visual.py" visual \
  --asset broll --narration-slot '00:12-00:17 仓储扫码说明' \
  --proof '现代仓库内，扫码设备依次读取三个无品牌箱体，状态灯由待机变为绿色' \
  --presenter-mode absent \
  --action '摄影机缓慢侧移，完整看见三个箱体依次被读取' \
  --caption-zone '底部保留培训字幕安全区' \
  --post-audio '由企业批准的旁白在后期加入' \
  --protect '不出现主持人、对白、文字、公司Logo、错误箱体数量或突然切镜' \
  --param aspect_ratio=16:9 duration=5
```

### 2. 无对白主持人开场

```bash
python3 "$SKILL_PATH/scripts/heygen_visual.py" visual \
  --asset presenter --narration-slot '00:00-00:04 无对白开场' \
  --proof '已授权主持人在批准背景中自然出镜' \
  --presenter-mode authorized-closed-mouth --presenter-authorized \
  --presenter-still ./authorized-presenter-still.png \
  --action '人物自然呼吸并轻微点头，嘴唇始终闭合，摄影机固定' \
  --post-audio '品牌批准旁白另行录制并在后期加入' \
  --protect '身份、脸、发型、服装和背景不变；不模拟说话，不生成文字、Logo或夸张手势' \
  --param aspect_ratio=16:9 duration=4
```

### 3. 主持人与产品视觉参考

```bash
python3 "$SKILL_PATH/scripts/heygen_visual.py" visual \
  --asset demo --narration-slot '00:28-00:33 产品演示插镜' \
  --proof '图1锁定授权主持人，图2锁定批准设备' \
  --presenter-mode authorized-closed-mouth --presenter-authorized \
  --reference-image ./authorized-presenter.png ./approved-device.png \
  --blocking-video ./authorized-demo-blocking.mp4 \
  --action '只借用参考视频的侧身站位；人物闭口并指向设备' \
  --post-audio '产品讲解由授权配音后期加入' \
  --protect '脸、服装和产品结构稳定；不复制参考演员、声音、字幕或品牌' \
  --param aspect_ratio=16:9 duration=5
```

### 4. 清理讲解背景

```bash
python3 "$SKILL_PATH/scripts/heygen_visual.py" visual \
  --asset background --narration-slot '00:40-00:46 主持背景改版' \
  --proof '授权主持人位于干净浅灰演示空间' \
  --presenter-mode authorized-closed-mouth --presenter-authorized \
  --source-video ./authorized-presenter-shot.mp4 \
  --action '只替换背景并移除无权使用的墙面Logo' \
  --post-audio '保留原片无声版，最终音频由后期合成' \
  --protect '身份、闭口状态、动作、服装、镜头和时长不变；不生成文字、口型、声音、道具或第二个人'
```

### 5. 延长字幕片尾

```bash
python3 "$SKILL_PATH/scripts/heygen_visual.py" visual \
  --asset hold --narration-slot '片尾延长3秒' \
  --proof '主持人保持闭口和自然站姿，右侧形成总结字幕区域' \
  --presenter-mode authorized-closed-mouth --presenter-authorized \
  --source-video ./approved-training-end.mp4 \
  --action '从末帧继续，摄影机固定，背景光线稳定' \
  --caption-zone '右侧留总结字幕区域，但不生成实际字幕' \
  --post-audio '片尾旁白与音乐后期加入' \
  --protect '不模拟说话，不生成文字、Logo、声音或新手势' \
  --param duration=3
```

## 合规交付

核对人物授权、身份、嘴部状态和产品事实；不得声称生成准确对白口型或克隆声音。旁白、TTS、字幕、翻译与数字人绑定另行完成，并记录授权、工具来源和最终合成版本。

脚本不会访问 HeyGen 账号，也没有 Avatar 或 voice clone 接口。认证通信固定到 `https://ai-hive.iclip.cn/api`，只调用 Seedance 2.5 视频任务。

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/heygen_visual.py" auth --api-key REDACTED-SECRET
python3 "$SKILL_PATH/scripts/heygen_visual.py" status --task-id <taskId>
```

HeyGen 与 Avatar Video 名称只用于搜索和能力边界说明。
