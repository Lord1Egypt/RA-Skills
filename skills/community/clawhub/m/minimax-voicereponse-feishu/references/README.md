# Voice Reply Skill for OpenClaw

飞书语音回复技能 - 将文字转换为语音气泡通过飞书发送

## 快速开始

### 1. 安装依赖

```bash
pip install requests
```

确保系统已安装 `ffmpeg`（用于音频格式转换）：

```bash
# Ubuntu/Debian
sudo apt install ffmpeg

# macOS
brew install ffmpeg

# Windows
# 下载 ffmpeg.exe 并添加到 PATH
```

### 2. 配置 API Key

**方式一：环境变量（推荐）**
```bash
export MINIMAX_VOICE_API_KEY="your-api-key-here"
```

**方式二：配置文件**
```bash
cp config.example.txt config.txt
# 编辑 config.txt，填入你的 API Key
```

### 3. 测试

```bash
python3 scripts/voice_reply.py "你好，这是一个测试"
```

成功后会打印输出文件路径，如：
```
/home/xxx/.openclaw/workspace/voice_reply.ogg
```

### 4. 集成到 OpenClaw

在 OpenClaw 的 `SOUL.md` 或 `AGENTS.md` 中添加触发指令：
- 用户说"语音回复：xxx" → 调用本脚本 → 用 message 工具发送

## OpenClaw 配置示例

```json
{
  "skills": {
    "minimax_ttsresponse_feishu": {
      "enabled": true,
      "trigger": ["语音回复", "/voice"]
    }
  }
}
```

## 目录结构

```
minimax_ttsresponse_feishu/
├── SKILL.md              # 技能说明（OpenClaw 读取）
├── config.example.txt    # 配置示例
├── scripts/             # 脚本目录
│   └── voice_reply.py   # 主脚本
└── references/          # 参考文档
    └── README.md        # 本文件
```

## 获取 MiniMax API Key

1. 访问 https://www.minimaxi.com/
2. 注册/登录账号
3. 进入控制台 → 创建项目
4. 获取 API Key

注意：TTS API 可能需要付费，首次使用有免费额度。

## 常见问题

**Q: 提示"网络请求失败"**
- 检查 API Key 是否正确
- 检查网络连接

**Q: 提示"API返回错误"**
- 检查 API Key 是否有 TTS 权限
- 检查账户额度是否充足

**Q: 飞书收不到语音**
- 确认使用的是飞书平台
- 微信不支持原生语音气泡

## License

MIT
