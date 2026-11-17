# 演示脚本（demo.md）— pet-feedback

## 演示一：单 Skill 演示（表情 + 语音）

```bash
# 终端 A：启动守护进程（全屏）
python3 daemon.py --state-file /tmp/pet_state.json --fullscreen

# 终端 B：依次写入不同状态，观察表情切换 + 语音播放
echo '{"emotion":"happy","phase":"talking","message":"看到你笑我也很开心！"}' > /tmp/pet_state.json
echo '{"emotion":"worried","phase":"listening","message":"你好像不太开心，我陪着你"}' > /tmp/pet_state.json
echo '{"emotion":"sleepy","phase":"sleeping","message":"我先眯一会儿，有事叫我"}' > /tmp/pet_state.json
```

**演示话术**：情绪变了、表情就变，说的话通过喇叭播出来——这就是"反馈端"。

## 演示二：端到端闭环（感知 → 分析 → 反馈）

```bash
# 终端 A：反馈守护进程
python3 ../pet-feedback/daemon.py --state-file /tmp/pet_state.json --fullscreen

# 终端 B：感知 → 分析 → 写状态 → 反馈
python3 ../pet-camera-vision/capture.py --outdir captures
python3 ../pet-camera-vision/analyze.py --image captures/<最新图>.jpg --local
# OpenClaw 多模态分析情绪后，写入状态：
echo '{"emotion":"happy","phase":"talking","message":"你看起来很开心呀！"}' > /tmp/pet_state.json
```

完整故事线：**用户对摄像头笑 → 识别 happy → 屏幕显示开心表情 + 语音"你看起来很开心呀！"**
→ 用户离开 → 识别 present=false → 写入 sleeping 状态 → 待机。

## 演示三：离线 / 无网络演示

```bash
# 语音用本地引擎（无需网络）
python3 tts.py --text "你好，我是你的桌宠" --engine espeak-ng --play

# 表情照常显示
python3 show_expression.py --emotion happy --phase talking
```

## 演示四：无头截图（预览）

```bash
# 生成各情绪预览图（无需显示器）
python3 show_expression.py --emotion happy  --snapshot preview_happy.png
python3 show_expression.py --emotion sad    --snapshot preview_sad.png
python3 show_expression.py --emotion worried --snapshot preview_worried.png
```

## 常见问题

| 问题 | 处理 |
| --- | --- |
| 无声音 | `python3 tts.py --text 测试 --engine espeak-ng --play` 验证；检查音量 |
| 表情不切换 | 确认状态文件路径与 daemon `--state-file` 一致 |
| 想手动看某个表情 | `show_expression.py --emotion sad`（单次） |
| 开发机（非树莓派） | 一切照常；亮屏/熄屏自动退化为软件黑屏 |
