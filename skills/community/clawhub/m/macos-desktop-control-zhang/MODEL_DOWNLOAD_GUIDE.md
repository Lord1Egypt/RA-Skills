# 📥 Vosk 模型下载指南

> **模型信息**:
> - 名称：vosk-model-small-zh-cn-0.22
> - 大小：~50MB
> - 语言：中文普通话
> - 位置：`~/.openclaw/vosk-models/`

---

## 🎯 下载方法

### 方法 1: 自动下载脚本（推荐）

```bash
cd /Users/zhangchangsha/.openclaw/workspace/skills/macos-desktop-control
python3 scripts/download_vosk_model.py
```

**如果下载失败**，请尝试以下手动方法。

---

### 方法 2: 手动下载（最可靠）

#### Step 1: 访问下载页面

打开浏览器访问：
```
https://alphacephei.com/vosk/models/
```

或者 HuggingFace 镜像：
```
https://huggingface.co/vosk-community/vosk-model-small-zh-cn-0.22
```

#### Step 2: 下载模型

找到并下载：
```
vosk-model-small-zh-cn-0.22.zip
```

#### Step 3: 解压到指定位置

```bash
# 创建目录
mkdir -p ~/.openclaw/vosk-models

# 解压（假设下载到了 Downloads 目录）
cd ~/Downloads
unzip vosk-model-small-zh-cn-0.22.zip -d ~/.openclaw/vosk-models/

# 验证
ls -la ~/.openclaw/vosk-models/vosk-model-small-zh-cn-0.22/
```

**应该看到**:
```
am/
conf/
graph/
ivector/
mfcc.conf
model.topo
...
```

---

### 方法 3: 使用 git 克隆

```bash
# 创建目录
mkdir -p ~/.openclaw/vosk-models
cd ~/.openclaw/vosk-models

# 克隆模型（如果有的话）
git clone https://github.com/vosk-community/vosk-model-small-zh-cn-0.22.git
```

---

### 方法 4: 使用 pip 下载

```bash
# 有些模型可以通过 pip 安装
pip3 install vosk-model-small-zh-cn
```

---

## ✅ 验证安装

### 检查模型文件

```bash
ls -lh ~/.openclaw/vosk-models/vosk-model-small-zh-cn-0.22/
```

**应该显示**:
```
total ~50M
drwxr-xr-x  am/
drwxr-xr-x  conf/
drwxr-xr-x  graph/
-rw-r--r--  mfcc.conf
...
```

### 测试模型加载

```bash
cd /Users/zhangchangsha/.openclaw/workspace/skills/macos-desktop-control
python3 -c "
from vosk import Model
model = Model('/Users/zhangchangsha/.openclaw/vosk-models/vosk-model-small-zh-cn-0.22')
print('✅ 模型加载成功！')
"
```

---

## 🎤 测试语音识别

### 录制测试音频

```bash
# 安装录音工具
brew install sox

# 录制 5 秒测试音频
rec -r 16000 -c 1 ~/test_audio.wav trim 0 5
```

### 识别测试

```bash
python3 scripts/voice_recognition_vosk.py
```

**对着麦克风说**:
```
"帮我截个屏"
```

**预期结果**:
```
✅ 识别结果："帮我截个屏"
🚀 执行命令...
📸 正在截屏...
✅ 截屏成功！
```

---

## 🐛 常见问题

### Q1: 下载速度慢

**解决**:
- 使用国内镜像
- 使用代理
- 夜间下载

### Q2: SSL 错误

**解决**:
```python
# 添加 SSL 验证跳过
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
```

### Q3: 找不到麦克风

**解决**:
```
系统设置 → 隐私与安全性 → 麦克风
勾选「终端」或你的终端应用
```

### Q4: 识别准确率低

**解决**:
- 说话清晰、慢一点
- 减少环境噪音
- 靠近麦克风
- 使用更好的麦克风

---

## 📝 模型位置总结

| 项目 | 路径 |
|------|------|
| **模型目录** | `~/.openclaw/vosk-models/vosk-model-small-zh-cn-0.22/` |
| **脚本目录** | `~/.openclaw/workspace/skills/macos-desktop-control/scripts/` |
| **测试音频** | `~/test_audio.wav` |

---

## 🎯 下一步

模型下载完成后：

1. **验证模型**:
   ```bash
   ls ~/.openclaw/vosk-models/vosk-model-small-zh-cn-0.22/
   ```

2. **测试识别**:
   ```bash
   python3 scripts/voice_recognition_vosk.py
   ```

3. **使用菜单**:
   ```bash
   bash scripts/voice_control_menu.sh
   ```

---

**祝下载顺利！** 🦐
