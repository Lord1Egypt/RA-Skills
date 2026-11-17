---
name: pet-feedback
description: 桌宠反馈 Skill。触摸屏表情显示（按情绪/状态切换）+ 语音反馈（TTS 合成并播放）+ 触摸检测与自动亮屏，构成"感知—分析—反馈"闭环的反馈端。
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - python3
    envVars:
      - name: PET_STATE_FILE
        required: false
        description: 状态 JSON 文件路径（OpenClaw 写入，默认系统临时目录 pet_state.json）
      - name: PET_TTS_ENGINE
        required: false
        description: 语音合成引擎 auto|edge-tts|espeak-ng|gtts，默认 auto
      - name: PET_TTS_VOICE
        required: false
        description: edge-tts 音色，默认 zh-CN-XiaoxiaoNeural
      - name: PET_SCREEN_SIZE
        required: false
        description: 屏幕尺寸，默认 800x480
      - name: PET_WAKE_CMD / PET_BLANK_CMD
        required: false
        description: 亮屏/熄屏命令（树莓派 vcgencmd display_power 1/0）
    emoji: "🎭"
---

# pet-feedback — 桌宠反馈 Skill

## 概述

本 Skill 是「多模态情绪陪伴桌宠系统」的**反馈端**，把三类输出整合成一个守护进程：

1. **表情显示**：在 7 寸触摸屏上按情绪/状态切换桌宠表情（纯程序化绘制，无图片素材）
2. **语音反馈**：大模型生成的文本回复 → TTS 合成 → 主机喇叭播放
3. **触摸检测 + 亮屏控制**：后台循环持续监控触摸事件；待机超时熄屏，触摸/状态更新自动亮屏

配合 `pet-camera-vision`（感知端）与 OpenClaw 的"思考"能力，构成完整的
**感知 → 分析 → 反馈** 陪伴闭环。

## 架构

```
OpenClaw（思考：情绪分析、对话生成）
      │  写入状态 JSON
      ▼
pet_state.json  {"emotion":"happy","phase":"talking","message":"看到你笑我也很开心！"}
      │
      ▼
daemon.py（后台守护）
      ├── 表情显示   ← pygame 渲染，按 emotion/phase 切换
      ├── 语音反馈   ← message 字段 → TTS 合成 → 喇叭播放
      └── 触摸/亮屏  ← 触摸事件 → 唤醒；待机超时 → 熄屏
```

## 文件说明

| 文件 | 作用 |
| --- | --- |
| `SKILL.md` | 本说明文档 |
| `expressions.py` | 表情绘制模块（10 种情绪 × 5 种状态，纯图形绘制） |
| `show_expression.py` | 单次表情显示 CLI（也支持跟随状态文件、无头截图） |
| `tts.py` | 语音合成 + 播放 CLI（edge-tts / espeak-ng / gtts 自动回退） |
| `daemon.py` | 反馈守护进程（表情 + 语音 + 触摸 + 亮屏整合） |
| `examples/example_state.json` | 状态文件样例 |
| `examples/demo.md` | 演示脚本（含端到端闭环演示） |

## 依赖与安装

```bash
pip install pygame edge-tts        # pygame 必需；edge-tts 高质量中文语音
sudo apt install -y espeak-ng      # 可选：本地离线语音（音质一般）
sudo apt install -y ffplay         # 可选：备选播放器（或 mpv）
```

中文字体（显示 message 用，自动查找；找不到时仅显示表情）：
`fonts-wqy-zenhei`（`sudo apt install fonts-wqy-zenhei`）或系统自带 Noto CJK。

## 使用方法

### 1. 快速试一个表情（单次显示）

```bash
python3 show_expression.py --emotion happy --phase talking --message "你好呀"
# ESC / q 退出
```

### 2. 启动反馈守护进程（推荐）

```bash
python3 daemon.py --state-file /tmp/pet_state.json --fullscreen
```

OpenClaw 侧更新状态（触发表情 + 语音联动）：

```bash
echo '{"emotion":"happy","phase":"talking","message":"看到你笑我也很开心！"}' > /tmp/pet_state.json
echo '{"emotion":"sad","phase":"listening","message":"别难过，我陪着你"}' > /tmp/pet_state.json
```

每次写入，屏幕立即切换表情，喇叭播放 message 语音。

### 3. 语音反馈单独使用

```bash
python3 tts.py --text "该起来活动一下啦" --play          # 自动选引擎
python3 tts.py --text "你好" --engine espeak-ng --play   # 强制离线
python3 tts.py --text "你好" --no-play --outdir audio    # 只生成音频文件
```

### 4. 触摸检测 + 自动亮屏（树莓派）

```bash
python3 daemon.py --state-file /tmp/pet_state.json --fullscreen \
  --idle-timeout 120 \
  --wake-cmd "vcgencmd display_power 1" \
  --blank-cmd "vcgencmd display_power 0"
```

- 用户触摸/按键 → 立即唤醒屏幕并重置待机计时
- 连续 120 秒无互动 → 自动熄屏（省电、进入待机）
- 无 `vcgencmd` 的环境（如开发机）自动退化为软件黑屏

## 状态文件 JSON 格式

```json
{
  "emotion": "happy",
  "phase": "talking",
  "message": "看到你笑我也很开心！",
  "tts": true
}
```

| 字段 | 取值 | 说明 |
| --- | --- | --- |
| `emotion` | happy/sad/angry/surprised/fearful/disgusted/neutral/worried/sleepy/excited | 与 pet-camera-vision 情绪集合一致 |
| `phase` | idle/listening/thinking/talking/sleeping | 交互阶段（徽标显示） |
| `message` | 字符串 | 显示文字 + 语音内容（新值触发 TTS） |
| `tts` | true/false | 是否播放语音，默认 true |

## 与 OpenClaw 的集成（示例流程）

```text
1. OpenClaw 完成情绪分析/对话生成
2. 组装状态 JSON（emotion 来自 pet-camera-vision 分析结果，message 为对话回复）
3. 写入状态文件：echo '{"emotion":"happy","phase":"talking","message":"..."}' > /tmp/pet_state.json
4. daemon.py 检测到变化 → 切换表情 + 播放语音 + （如有触摸）保持亮屏
5. 用户触摸屏幕 → 触发 OpenClaw 主动互动（可选：触摸事件另写 event 文件）
```

## 演示样例

见 `examples/demo.md`，含：

- 单 skill 演示：直接写状态文件看表情/听语音
- 端到端闭环演示：摄像头感知 → 分析 → 表情 + 语音反馈
- 离线演示：无摄像头/无网络（espeak-ng 离线语音）方案

## 故障排查

| 现象 | 处理 |
| --- | --- |
| 没有声音 | `--wake/blank` 无关；检查喇叭；`aplay -l`；tts.py 换 `--engine espeak-ng` |
| 中文乱码/不显示 message | 安装中文字体 `fonts-wqy-zenhei`，或用 `--font` 指定字体路径 |
| 全屏分辨率不对 | `--size 宽x高` 与屏幕实际分辨率一致 |
| 树莓派无显示输出 | 确认 HDMI/DSI 连接；`vcgencmd display_power 1` 手动测试 |
| 触摸无反应 | 触摸屏以鼠标事件上报（pygame MOUSEBUTTONDOWN）；检查系统触摸校准 |

## 许可

按 ClawHub 规则，本 Skill 以 MIT-0 许可发布。
