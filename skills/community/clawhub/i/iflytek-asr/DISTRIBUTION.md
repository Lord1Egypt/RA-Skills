# 📦 分发指南

## 如何分享这个 Skill

### 方式 1：打包为 ZIP 文件

```bash
cd ~/.openclaw/workspace
zip -r iflytek-asr-skill.zip iflytek-asr-skill-template/ \
  -x "*.pyc" "**/__pycache__/*" ".env" "*.mp3" "*.wav" "*.txt"
```

生成的 `iflytek-asr-skill.zip` 就可以分享给别人了！

### 方式 2：上传到 GitHub

```bash
cd iflytek-asr-skill-template
git init
git add .
git commit -m "Initial commit: iFlytek ASR Skill"
git remote add origin https://github.com/你的用户名/iflytek-asr-skill.git
git push -u origin main
```

⚠️ **重要**：确保 `.gitignore` 已配置，不要泄露你的 `.env` 凭证！

### 方式 3：创建 OpenClaw Skill 包

在 skill 根目录创建 `SKILL.md`：

```markdown
---
name: iflytek-asr
description: 使用科大讯飞 API 将音频转文本，支持 YouTube 下载和中文方言识别
---

# iFlytek ASR Skill

详细文档请查看 README.md
```

然后可以被 OpenClaw 的 skill 系统识别。

---

## 接收者如何使用

### 快速安装（推荐）

```bash
# 1. 解压文件
unzip iflytek-asr-skill.zip
cd iflytek-asr-skill-template/

# 2. 运行安装脚本
./install.sh

# 3. 配置凭证
nano .env  # 填入讯飞 API 凭证

# 4. 测试
python3 scripts/speech_to_text.py --help
```

### 手动安装

详见 `QUICKSTART.md` 文档。

---

## 注意事项

### ⚠️ 安全提醒

1. **绝对不要**在分发的包里包含你的 `.env` 文件
2. **绝对不要**把真实凭证写在示例或文档里
3. `.gitignore` 已配置，确保它包含 `.env`

### ✅ 分发前检查清单

- [ ] 移除所有 `.env` 文件（只保留 `.env.example`）
- [ ] 检查代码中没有硬编码的凭证
- [ ] 测试 `install.sh` 脚本能正常运行
- [ ] README.md 和 QUICKSTART.md 文档完整
- [ ] .gitignore 配置正确

---

## 文件结构（分发版本）

```
iflytek-asr-skill/
├── README.md              # 完整文档
├── QUICKSTART.md          # 快速开始
├── DISTRIBUTION.md        # 本文档
├── .env.example           # 凭证模板（无真实key）
├── .gitignore             # Git忽略配置
├── install.sh             # 安装脚本
├── requirements.txt       # Python依赖
└── scripts/
    ├── speech_to_text.py
    ├── download_audio.py
    └── download_and_transcribe.py
```

**不应包含：**
- ❌ `.env` (真实凭证)
- ❌ `__pycache__/`
- ❌ 任何音频/文本输出文件

---

## 更新说明

分享时建议附上版本号和更新日志，方便用户知道有哪些改进。
