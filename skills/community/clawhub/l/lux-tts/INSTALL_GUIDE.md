# LuxTTS 安装指南

## 安装选项

### 选项 1：一键安装（推荐）
```cmd
# 以管理员身份运行
E:\桌面\openclaw-main\workspace\lux-tts\install.bat
```

### 选项 2：分步安装
```cmd
# 步骤 1: 部署环境
cd D:\lux-tts\scripts
deploy.bat

# 步骤 2: 下载模型
download.bat

# 步骤 3: 测试功能
test.bat
```

### 选项 3：手动安装
如果上述方法都失败，可以手动安装：

1. **手动创建虚拟环境**
   ```cmd
   python -m venv D:\lux-tts\venv
   D:\lux-tts\venv\Scripts\activate.bat
   pip install zipvoice-luxvoice torch soundfile numpy huggingface-hub
   ```

2. **手动下载模型**
   - 访问：https://huggingface.co/YatharthS/LuxTTS
   - 下载所有文件到 `D:\lux-tts\models\`

3. **测试安装**
   ```cmd
   cd E:\桌面\openclaw-main\workspace\lux-tts
   python -c "from lux_tts import test_installation; test_installation()"
   ```

## 常见问题

### 1. PowerShell 执行策略错误
**错误信息**：`无法加载文件...，因为在此系统上禁止运行脚本`

**解决方案**：
- 使用批处理文件（.bat）而不是 PowerShell 脚本（.ps1）
- 或临时绕过执行策略：
  ```powershell
  powershell -ExecutionPolicy Bypass -File deploy.ps1
  ```

### 2. 模型下载失败
**可能原因**：
- 网络连接问题
- Hugging Face 访问限制
- 磁盘空间不足

**解决方案**：
- 检查网络连接
- 手动从浏览器下载模型
- 确保 D盘有足够空间（>2GB）

### 3. Python 包安装失败
**可能原因**：
- pip 版本过旧
- 网络问题
- 依赖冲突

**解决方案**：
```cmd
# 更新 pip
python -m pip install --upgrade pip

# 使用国内镜像源（如果在中国）
pip install torch -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 4. CUDA 不可用
**检查方法**：
```cmd
nvidia-smi
python -c "import torch; print(torch.cuda.is_available())"
```

**解决方案**：
- 更新 NVIDIA 驱动
- 安装 CUDA Toolkit
- 或使用 CPU 模式（修改 `config.yaml` 中的 `device: "cpu"`）

## 验证安装

安装完成后，运行以下命令验证：

```cmd
# 方法 1: 使用测试脚本
D:\lux-tts\scripts\test.bat

# 方法 2: 在 Python 中测试
cd E:\桌面\openclaw-main\workspace\lux-tts
python -c "
from lux_tts import test_installation
test_installation()
"

# 方法 3: 在 OpenClaw 中测试
python -c "
from lux_tts_tool import tts_status
print(tts_status())
"
```

## 安装成功标志

如果看到以下信息，说明安装成功：

```
✓ LuxTTS 安装正常
  安装位置: D:\lux-tts
  设备: cuda
  CUDA可用: True
✓ 音频生成成功
  文本: 你好，这是 LuxTTS 测试语音。
  时长: 2.34秒
✓ 测试音频已保存: D:/lux-tts/test_output.wav
```

## 后续步骤

1. **添加自定义语音**：将你的语音文件（WAV/MP3，≥3秒）复制到 `D:\lux-tts\voices\`
2. **在 OpenClaw 中使用**：
   ```python
   from lux_tts_tool import tts_generate
   result = tts_generate("需要转换为语音的文本")
   ```
3. **配置为默认 TTS**：修改 OpenClaw 配置，优先使用本地 LuxTTS

## 获取帮助

如果遇到问题：

1. 查看 `SKILL.md` 中的故障排除部分
2. 检查日志文件（如果有）
3. 运行 `test.bat` 查看详细错误信息
4. 确保所有步骤都正确执行

---
*最后更新: 2026-03-16*