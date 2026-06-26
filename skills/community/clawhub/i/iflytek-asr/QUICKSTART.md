# 🚀 快速开始

## 5分钟上手讯飞语音转文本

### 步骤 1：安装依赖 (1分钟)

```bash
pip3 install yt-dlp requests python-dotenv
```

### 步骤 2：获取讯飞凭证 (2分钟)

1. 打开 https://www.xfyun.cn
2. 注册/登录
3. 进入控制台 → 创建应用
4. 选择"语音识别"服务
5. 复制三个凭证：
   - APP ID
   - Access Key ID  
   - Access Key Secret

### 步骤 3：配置凭证 (1分钟)

```bash
# 复制模板文件
cp .env.example .env

# 编辑 .env 文件，粘贴你的凭证
nano .env  # 或用任何文本编辑器
```

`.env` 文件示例：
```env
XFYUN_APP_ID=12345678
XFYUN_ACCESS_KEY_ID=AbCdEfGhIjKlMnOp
XFYUN_ACCESS_KEY_SECRET=QrStUvWxYz123456789
```

### 步骤 4：测试运行 (1分钟)

```bash
# 测试：转录一个本地音频文件
python3 scripts/speech_to_text.py test.mp3

# 或者：从 YouTube 下载并转录
python3 scripts/download_and_transcribe.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

---

## ✅ 完成！

你现在可以：
- 📄 转录任何音频文件为文本
- 🎥 从 YouTube 下载音频并自动转录
- 🌐 处理中文各种方言

## 下一步

查看 [README.md](README.md) 了解：
- 所有功能详解
- 高级用法
- 常见问题解决

---

**遇到问题？** 检查：
1. ✅ 凭证是否正确配置在 `.env`
2. ✅ 依赖是否安装完整
3. ✅ 网络连接是否正常
