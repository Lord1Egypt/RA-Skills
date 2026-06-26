# OpenClaw Skill 安装指南

本文档说明如何将龙虾电台Skill导入到OpenClaw中。

## 方法一：直接复制到工作区（推荐）

### 1. 找到OpenClaw工作区目录

OpenClaw的工作区目录通常位于：
- **macOS/Linux**: `~/.openclaw/workspace/skills/`
- **Windows**: `C:\Users\你的用户名\.openclaw\workspace\skills\`

### 2. 复制Skill目录

```bash
# 进入OpenClaw工作区
cd ~/.openclaw/workspace/skills/

# 复制Skill（假设你当前在lobster-radio-skill目录）
cp -r /path/to/lobster-radio-skill ./

# 或者使用符号链接（推荐，方便开发）
ln -s /path/to/lobster-radio-skill ./lobster-radio-skill
```

### 3. 重启OpenClaw

```bash
# 重启OpenClaw Gateway
openclaw gateway restart

# 或者重启整个OpenClaw服务
openclaw restart
```

### 4. 验证安装

```bash
# 查看已安装的skills
openclaw skills list

# 应该能看到 lobster-radio 在列表中
```

## 方法二：使用ClawHub安装（如果已发布）

### 1. 安装ClawHub CLI

```bash
npm install -g clawhub
```

### 2. 登录ClawHub（可选）

```bash
clawhub login
```

### 3. 安装Skill

```bash
# 如果skill已发布到ClawHub
clawhub install lobster-radio

# 或指定版本
clawhub install lobster-radio --version 1.0.0
```

### 4. 验证安装

```bash
clawhub list
```

## 方法三：使用OpenClaw命令安装

### 1. 打包Skill

```bash
# 在lobster-radio-skill目录下
cd lobster-radio-skill

# 打包为.skill文件（需要先创建打包脚本）
python scripts/package_skill.py
```

### 2. 安装Skill

```bash
# 使用OpenClaw命令安装
openclaw plugins install ./lobster-radio-skill.skill

# 或指定目录
openclaw plugins install ./lobster-radio-skill --local
```

## 方法四：手动配置（高级）

### 1. 创建Skill配置文件

在 `~/.openclaw/config/skills.json` 中添加：

```json
{
  "skills": [
    {
      "name": "lobster-radio",
      "path": "/path/to/lobster-radio-skill",
      "enabled": true,
      "priority": 10
    }
  ]
}
```

### 2. 重启OpenClaw

```bash
openclaw restart
```

## 安装后配置

### 1. 安装Python依赖

```bash
# 进入Skill目录
cd ~/.openclaw/workspace/skills/lobster-radio-skill

# 安装依赖
pip install -r requirements.txt
```

### 2. 下载Qwen3-TTS模型

龙虾电台使用Qwen3-TTS本地模型进行语音合成，**不需要Ollama**。

#### 方法一：从HuggingFace下载（推荐）

```bash
# 安装huggingface_hub
pip install huggingface_hub

# 下载模型
huggingface-cli download Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice --local-dir ./models/Qwen3-TTS-12Hz-0.6B-Base
```

#### 方法二：从ModelScope下载（国内用户推荐）

```bash
# 安装modelscope
pip install modelscope

# 使用Python下载
python -c "from modelscope import snapshot_download; snapshot_download('qwen/Qwen3-TTS-12Hz-0.6B-Base', cache_dir='./models')"
```

#### 方法三：首次运行时自动下载

Skill会在首次生成电台时自动检测并下载模型：

```bash
# 运行生成脚本，会自动下载模型
python scripts/generate_radio.py --topics "人工智能"
```

### 3. 配置TTS

```bash
# 配置音色
python scripts/configure_tts.py --voice xiaoxiao --emotion neutral

# 测试TTS
python scripts/configure_tts.py --test
```

**注意**：首次运行需要下载约5GB的模型文件，请确保网络畅通。

## 验证安装

### 1. 检查Skill状态

```bash
# 查看所有skills
openclaw skills list

# 查看特定skill详情
openclaw skills show lobster-radio
```

### 2. 测试Skill功能

在OpenClaw支持的聊天平台中（如飞书、Telegram）：

```
User: 生成关于人工智能的电台
Bot: 🎙️ 正在为您生成人工智能主题电台...
```

### 3. 查看日志

```bash
# 查看OpenClaw日志
tail -f ~/.openclaw/logs/openclaw.log

# 或使用openclaw命令
openclaw logs
```

## 故障排除

### Skill未识别

**问题**: `openclaw skills list` 中看不到 lobster-radio

**解决方案**:
1. 检查SKILL.md文件是否存在
2. 检查SKILL.md格式是否正确
3. 重启OpenClaw服务
4. 查看错误日志

```bash
# 检查SKILL.md
cat ~/.openclaw/workspace/skills/lobster-radio-skill/SKILL.md

# 查看日志
openclaw logs | grep lobster-radio
```

### 模型下载失败

**问题**: "模型下载失败" 或 "模型未找到"

**解决方案**:
```bash
# 方法1: 使用HuggingFace镜像（国内用户）
export HF_ENDPOINT=https://hf-mirror.com
huggingface-cli download Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice --local-dir ./models/Qwen3-TTS-12Hz-0.6B-Base

# 方法2: 使用ModelScope（国内用户推荐）
pip install modelscope
python -c "from modelscope import snapshot_download; snapshot_download('qwen/Qwen3-TTS-12Hz-0.6B-Base', cache_dir='./models')"

# 方法3: 手动下载
# 访问 https://modelscope.cn/models/qwen/Qwen3-TTS-12Hz-0.6B-Base 手动下载
```

### Python依赖缺失

**问题**: "ModuleNotFoundError"

**解决方案**:
```bash
# 进入Skill目录
cd ~/.openclaw/workspace/skills/lobster-radio-skill

# 重新安装依赖
pip install -r requirements.txt

# 或使用虚拟环境
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 权限问题

**问题**: "Permission denied"

**解决方案**:
```bash
# 修改权限
chmod -R 755 ~/.openclaw/workspace/skills/lobster-radio-skill

# 或修改所有者
chown -R $USER:$USER ~/.openclaw/workspace/skills/lobster-radio-skill
```

## 卸载Skill

### 方法一：删除目录

```bash
# 删除Skill目录
rm -rf ~/.openclaw/workspace/skills/lobster-radio-skill

# 重启OpenClaw
openclaw restart
```

### 方法二：禁用Skill

```bash
# 禁用Skill
openclaw skills disable lobster-radio

# 启用Skill（如果需要）
openclaw skills enable lobster-radio
```

## 更新Skill

### 方法一：Git更新（如果使用Git）

```bash
# 进入Skill目录
cd ~/.openclaw/workspace/skills/lobster-radio-skill

# 拉取最新代码
git pull

# 更新依赖
pip install -r requirements.txt

# 重启OpenClaw
openclaw restart
```

### 方法二：手动更新

```bash
# 备份配置
cp -r ~/.openclaw/workspace/skills/lobster-radio-skill/data ./backup

# 删除旧版本
rm -rf ~/.openclaw/workspace/skills/lobster-radio-skill

# 复制新版本
cp -r /path/to/new-lobster-radio-skill ~/.openclaw/workspace/skills/

# 恢复配置
cp -r ./backup/data ~/.openclaw/workspace/skills/lobster-radio-skill/

# 重启OpenClaw
openclaw restart
```

## 开发模式

### 使用符号链接（推荐）

```bash
# 创建符号链接
ln -s /path/to/lobster-radio-skill ~/.openclaw/workspace/skills/lobster-radio-skill

# 这样修改代码后会立即生效，无需重新复制
```

### 热重载

OpenClaw支持Skill热重载，修改SKILL.md后会自动重新加载：

```bash
# 修改SKILL.md后，OpenClaw会自动检测并重新加载
# 无需手动重启
```

## 最佳实践

1. **使用符号链接**: 方便开发和调试
2. **定期备份**: 备份配置和生成的音频文件
3. **查看日志**: 遇到问题时先查看日志
4. **测试环境**: 先在测试环境验证，再部署到生产环境
5. **版本管理**: 使用Git管理Skill版本

## 相关命令

```bash
# 查看所有skills
openclaw skills list

# 查看skill详情
openclaw skills show lobster-radio

# 启用skill
openclaw skills enable lobster-radio

# 禁用skill
openclaw skills disable lobster-radio

# 重启OpenClaw
openclaw restart

# 查看日志
openclaw logs

# 查看配置
openclaw config
```

## 获取帮助

- **OpenClaw文档**: https://docs.openclaw.ai
- **ClawHub**: https://clawhub.com
- **GitHub Issues**: https://github.com/your-repo/lobster-radio-skill/issues
- **社区支持**: https://discord.gg/openclaw

---

**注意**: 确保OpenClaw版本 >= 1.0.0，并且已正确配置LLM服务。
