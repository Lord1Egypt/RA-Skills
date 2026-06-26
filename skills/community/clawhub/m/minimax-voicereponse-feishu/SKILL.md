# Voice Reply Skill - 语音回复技能

> 🤖 支持平台：飞书（Feishu）
> 
> 将文字转换为语音气泡，通过飞书发送

---

## ⚠️ 首次使用必读

**使用前必须配置 MiniMax API Key**，否则无法运行！

配置方式：
1. 获取 Key：https://www.minimaxi.com/
2. 设置环境变量：`export MINIMAX_VOICE_API_KEY="your-key"`
   或创建配置文件：`cp config.example.txt config.txt` 并填入 Key
3. 验证：`python3 scripts/voice_reply.py "测试"`

详见下方「首次使用配置」章节。

---

## 功能

当检测到用户请求语音回复时，自动：
1. 获取要转换的文字
2. 调用 MiniMax TTS API 生成语音
3. 转换为 OGG 格式（飞书语音气泡格式）
4. 通过飞书发送语音消息

## 触发方式

用户发送以下任一方式都会触发：
- `语音回复：xxx` 或 `语音回复 xxx`
- `/voice xxx`
- 直接说"说给我听"
- 说"语音回复"

---

## 首次使用配置

### 1. 获取 MiniMax API Key

1. 注册 MiniMax 开放平台：https://www.minimaxi.com/
2. 在控制台创建项目，获取 API Key
3. 设置环境变量（推荐）：
   ```bash
   export MINIMAX_VOICE_API_KEY="your-api-key-here"
   ```

### 2. 配置文件方式（可选）

如果不想设置环境变量，可以创建配置文件：

```bash
cp config.example.txt config.txt
# 编辑 config.txt，填入你的 API Key
```

### 3. 验证

```bash
python3 scripts/voice_reply.py "你好，测试一下"
```

成功后会在终端打印：`/path/to/output.ogg`

---

## 技术细节

### 流程
```
文字 → MiniMax TTS (MP3) → FFmpeg转OGG → 飞书语音气泡
```

### 音频格式
- TTS 输出：MP3 (32kHz)
- 飞书语音气泡：OGG (Opus codec)
- 转换后采样率：48000Hz
- 比特率：128kbps

### 依赖
- Python 3.8+
- `requests` 库：`pip install requests`
- `ffmpeg`（系统命令）
- MiniMax TTS API Key

### 可用音色

| voice_id | 说明 |
|----------|------|
| male-qn-qingse | 男性青涩音色（默认） |
| female-qn-qingse | 女性青涩音色 |
| male-qn-jingqi | 男性京片子 |
| female-qn-tianmei | 女性甜妹 |
| ... | 更多音色见 MiniMax 文档 |

修改方法：编辑 `scripts/voice_reply.py`，找到 `voice_id` 字段

---

## 文件结构

```
minimax_ttsresponse_feishu/
├── SKILL.md              # 本文件
├── config.example.txt    # 配置示例
├── scripts/             # 脚本目录
│   └── voice_reply.py   # 主脚本
└── references/         # 参考文档
    └── README.md        # 详细说明
```

---

## 常见问题

### Q: 提示"网络请求失败"
A: 检查 API Key 是否正确配置，网络是否畅通

### Q: 提示"API返回错误"
A: 检查 API Key 是否有 TTS 权限，或额度是否充足

### Q: 飞书收不到语音
A: 确认是飞书平台，微信不支持原生语音气泡

### Q: 想换音色
A: 编辑 `scripts/voice_reply.py`，修改 `voice_id` 参数

---

## 贡献

欢迎提交 Issue 和 PR！
