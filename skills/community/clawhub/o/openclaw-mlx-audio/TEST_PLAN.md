# openclaw-mlx-audio - 测试验证计划
**版本**: v0.2.0
**日期**: 2026-03-20

---

## 测试清单

### 1. 构建验证
```bash
cd /Users/user/.openclaw/workspace/openclaw-mlx-audio
bun install
bun run build
```

**验收标准**:
- [x] `dist/index.js` 生成成功
- [x] 无 TypeScript 错误
- [x] 无运行时错误

### 2. 依赖安装测试

#### 运行 install.sh
./install.sh

**预期输出**:
 Found: ffmpeg
 Found: uv
 Installing mlx-audio...
 Installation complete!

- [ ] ffmpeg 已安装
- [ ] uv 已安装
- [ ] mlx_audio.tts.generate 可用

# 测试 TTS
mlx_audio.tts.generate \
 --model mlx-community/Kokoro-82M-bf16 \
 --text "你好,这是测试语音" \
 --lang_code z \
 --output_path /tmp/test-tts.mp3

# 验证输出
ls -lh /tmp/test-tts.mp3
afplay /tmp/test-tts.mp3 # macOS 播放音频

- [ ] 音频文件生成
- [ ] 文件大小 > 0
- [ ] 音频可播放
- [ ] 语音清晰

# 测试 STT
mlx_audio.stt.generate \
 --model mlx-community/whisper-large-v3-turbo-asr-fp16 \
 --audio /tmp/test-tts.mp3 \
 --format txt \
 --output /tmp/test-stt

cat /tmp/test-stt.txt

- [ ] 转录文本生成, [ ] 文本内容正确, [ ] 语言识别准确

# 复制插件到 extensions
cp -r /Users/user/.openclaw/workspace/openclaw-mlx-audio \
 ~/.openclaw/extensions/openclaw-mlx-audio

# 重启 Gateway
openclaw gateway restart

#### 验证插件加载
openclaw plugins list | grep mlx

│ mlx-audio │ openclaw-mlx-audio │ loaded │ ...

- [ ] 插件出现在列表中
- [ ] 状态为 loaded
- [ ] 无错误消息

# 状态查询
/ mlx-tts status

# 测试生成
/ mlx-tts test "你好,这是测试语音"

# 模型列表
/ mlx-tts models

{
 "ready": true,
 "model": "mlx-community/Kokoro-82M-bf16",
 "langCode": "z"
}

 TTS 测试完成:/tmp/mlx-tts-*.mp3

- [ ] 状态查询返回正确
- [ ] TTS 生成成功
- [ ] 音频文件可播放

#### STT 命令
/ mlx-stt status

# 转录测试
/ mlx-stt transcribe /tmp/test-tts.mp3

 "model": "mlx-community/whisper-large-v3-turbo-asr-fp16",
 "language": "zh"

转录结果:
你好,这是测试语音

- [ ] 转录文本正确

### 6. OpenClaw 工具测试

#### TTS 工具调用
```json
 "tool": "mlx_tts",
 "parameters": {
 "action": "generate",
 "text": "Hello World",
 "outputPath": "/tmp/test-tool.mp3",
 "langCode": "a"

 "success": true,
 "model": "mlx-community/Kokoro-82M-bf16"

- [ ] 工具调用成功
- [ ] 返回正确结果

#### STT 工具调用
"tool": "mlx_stt",
 "action": "transcribe",
 "audioPath": "/tmp/test-tool.mp3",
 "language": "en"

 "language": "en",
 "model": "mlx-community/whisper-large-v3-turbo-asr-fp16"

# 临时重命名 CLI 工具
mv ~/.local/bin/mlx_audio.tts.generate ~/.local/bin/mlx_audio.tts.generate.bak

# 尝试调用 (应该失败并重试)
/ mlx-tts test "测试"

# 恢复 CLI 工具
mv ~/.local/bin/mlx_audio.tts.generate.bak ~/.local/bin/mlx_audio.tts.generate

# 再次调用 (应该成功)
**预期行为**:
- 第 1 次:失败,等待 1s
- 第 3 次:成功

- [ ] 自动重试 2 次
- [ ] 指数退避 (1s, 2s)
- [ ] 最终成功

# 缺失文件
/ mlx-stt transcribe /nonexistent.wav

# 预期错误:
Audio file not found: /nonexistent.wav

# 临时移除 ffmpeg
brew uninstall ffmpeg

 Missing dependencies: ffmpeg
 Run: ./install.sh

- [ ] 错误消息明确, [ ] 包含解决建议, [ ] 日志分级正确

# 测试 100 字
time / mlx-tts test "一百字的测试文本..."

# 测试 1000 字
time / mlx-tts test "一千字的测试文本..."

**目标**:
- 1000 字:<30 秒

# 测试 1 分钟音频
time / mlx-stt transcribe /path/to/1min-audio.wav

- 1 分钟音频:<30 秒

# 连续调用 10 次
for i in {1..10}; do
 echo "Test $i..."
 / mlx-tts test "测试 $i"
done

- [ ] 10 次全部成功
- [ ] 无内存泄漏
- [ ] 响应时间稳定

## 测试结果记录

### 测试环境
- **macOS**:, **Node.js**:, **Python**:, **mlx-audio**:

### 测试结果
构建验证, 状态=⬜ 待测试, 备注=
依赖安装, 状态=⬜ 待测试, 备注=
CLI-TTS, 状态=⬜ 待测试, 备注=
CLI-STT, 状态=⬜ 待测试, 备注=
插件加载, 状态=⬜ 待测试, 备注=
命令-TTS, 状态=⬜ 待测试, 备注=
命令-STT, 状态=⬜ 待测试, 备注=
工具-TTS, 状态=⬜ 待测试, 备注=
工具-STT, 状态=⬜ 待测试, 备注=
重试机制, 状态=⬜ 待测试, 备注=
错误处理, 状态=⬜ 待测试, 备注=
性能, 状态=⬜ 待测试, 备注=
稳定性, 状态=⬜ 待测试, 备注=

# 2. 测试 CLI
mlx_audio.tts.generate --model mlx-community/Kokoro-82M-bf16 \
 --text "测试" --lang_code z --output_path /tmp/test.mp3

# 3. 播放
afplay /tmp/test.mp3

# 4. STT
mlx_audio.stt.generate --model mlx-community/whisper-large-v3-turbo-asr-fp16 \
 --audio /tmp/test.mp3 --format txt --output /tmp/stt

# 5. 验证
cat /tmp/stt.txt

**最后更新**: 2026-03-20
**维护者**: OpenClaw Community