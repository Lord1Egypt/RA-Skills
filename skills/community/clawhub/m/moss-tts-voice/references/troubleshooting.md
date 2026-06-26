# 问题排查

## 快速诊断

```bash
# 1. 检查 API Key
echo $MOSS_API_KEY
# 应该显示: sk-xxx...

# 2. 测试连通性
curl https://studio.mosi.cn/api/v1/voices \
  -H "Authorization: Bearer $MOSS_API_KEY"
# 应该返回 JSON（非 401）

# 3. 检查依赖
which python3 && which ffmpeg
# 两个都应该有路径
```

---

## 常见错误

### 1. "MOSS_API_KEY 环境变量未设置"

**原因**：未配置 API Key

**解决**：
```bash
# 临时（当前终端）
export MOSS_API_KEY="sk-xxx"

# 永久（写入配置文件）
echo 'export MOSS_API_KEY="sk-xxx"' >> ~/.zshrc
source ~/.zshrc
```

---

### 2. "ffmpeg: command not found"

**原因**：未安装 ffmpeg

**解决**：
```bash
brew install ffmpeg

# 验证
ffmpeg -version
```

---

### 3. 飞书收到文件而不是语音消息

**原因**：音频格式不对

**检查**：
```bash
file voice.ogg
# 应该显示: Ogg data, Opus audio

# 如果不是，重新转换：
ffmpeg -y -i input.wav -c:a libopus -b:a 64k output.ogg
```

**确保**：
- 文件后缀是 `.ogg`
- 编码是 `libopus`
- 不是 `libvorbis` 或其他编码

---

### 4. "Voice Not Found: voice not found"

**原因**：voice_id 无效

**解决**：
```bash
# 查询可用音色
curl https://studio.mosi.cn/api/v1/voices \
  -H "Authorization: Bearer $MOSS_API_KEY"

# 确认：
# 1. voice_id 正确
# 2. status 为 ACTIVE（不是 PENDING 或 FAILED）
```

---

### 5. API 返回 429 错误

**原因**：请求频率超限

**解决**：
1. 等待 5-10 秒后重试
2. 减少并发请求
3. 升级 MOSS Studio 套餐

---

### 6. 克隆任务失败 (status: FAILED)

**原因**：音频质量问题

**检查**：
- 音频时长是否 10-30 秒
- 是否清晰人声（无噪音、BGM）
- 文件是否损坏

**解决**：
```bash
# 检查音频
ffprobe voice.ogg

# 重新录制，确保：
# 1. 安静环境
# 2. 正常语速
# 3. 无背景音乐
```

---

### 7. Python "ModuleNotFoundError: No module named 'requests'"

**原因**：缺少依赖

**解决**：
```bash
cd ~/.openclaw/workspace/skills/moss-tts-voice
python3 -m venv .venv
source .venv/bin/activate
pip install requests
```

---

### 8. "Data too long for column 'input_source'"

**原因**：base64 音频太大

**解决**：
1. 使用预注册音色（推荐）
2. 或压缩音频：
   ```bash
   ffmpeg -i voice.ogg -t 20 -c:a libopus -b:a 32k compressed.ogg
   ```

---

### 9. 克隆效果不好

**原因**：参考音频质量差

**建议**：
- ✅ 时长 20 秒以上
- ✅ 清晰人声，无背景噪音
- ✅ 正常语速
- ❌ 不要有背景音乐
- ❌ 不要有其他人声
- ❌ 不要太快或太慢

---

### 10. 音频转换失败

**原因**：ffmpeg 参数错误

**解决**：
```bash
# 正确的转换命令
ffmpeg -y -i input.wav -c:a libopus -b:a 64k output.ogg

# 注意：
# - 必须用 libopus 编码
# - 不要用默认的 libvorbis
# - 比特率 64k 足够清晰
```

---

## 调试技巧

### 检查 API 连通性

```python
import requests, json

API_KEY = "sk-xxx"
headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

# 测试 TTS
resp = requests.post(
    "https://studio.mosi.cn/v1/audio/tts",
    headers=headers,
    json={"model": "moss-tts", "text": "测试", "voice_id": "YOUR_VOICE_ID"},
    timeout=30
)

print(f"Status: {resp.status_code}")
print(f"Response: {json.dumps(resp.json(), ensure_ascii=False)[:200]}")
```

### 检查音频格式

```bash
# 查看详细信息
ffprobe -v error -show_streams voice.ogg

# 检查编码
ffprobe -v error -select_streams a:0 -show_entries stream=codec_name -of default=noprint_wrappers=1:nokey=1 voice.ogg
# 应该输出: opus
```

### 检查音色状态

```bash
curl https://studio.mosi.cn/api/v1/voices \
  -H "Authorization: Bearer $MOSS_API_KEY" | jq .
```

---

## 联系支持

- **MOSS Studio**: https://studio.mosi.cn
- **OpenClaw 社区**: https://discord.com/invite/clawd

---

## 日志收集

如果问题持续，收集以下信息：

```bash
# 系统信息
uname -a
python3 --version
ffmpeg -version | head -1

# API 测试
curl -v https://studio.mosi.cn/api/v1/voices \
  -H "Authorization: Bearer $MOSS_API_KEY" 2>&1 | grep -E "HTTP|code|error"

# 音频信息
ffprobe -v error -show_format -show_streams your_audio.ogg
```
