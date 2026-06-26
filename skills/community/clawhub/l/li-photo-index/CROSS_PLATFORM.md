# 跨平台兼容性说明

**作者**: 北京老李（beijingLL）  
**日期**: 2026-05-16

---

## ✅ 支持的平台

PhotoIndexWithLLM Skill 完全支持以下操作系统：

| 平台 | 版本 | 状态 | 备注 |
|------|------|------|------|
| **Windows** | 10/11 | ✅ 完全支持 | 原生支持 |
| **Ubuntu** | 20.04/22.04/24.04 | ✅ 完全支持 | 推荐 |
| **Linux** | 其他发行版 | ✅ 支持 | 需要 Python 3.10+ |
| **macOS** | 12+ | ✅ 支持 | Intel/Apple Silicon |

---

## 🔧 跨平台特性

### 1. 自动路径检测

Skill 会自动检测当前操作系统并尝试相应的项目路径：

**Windows:**
```
G:\python\PhotoIndexWithLLM
C:\python\PhotoIndexWithLLM
D:\python\PhotoIndexWithLLM
%USERPROFILE%\PhotoIndexWithLLM
```

**Ubuntu/Linux:**
```
~/PhotoIndexWithLLM
/opt/PhotoIndexWithLLM
/usr/local/share/PhotoIndexWithLLM
~/projects/PhotoIndexWithLLM
```

**macOS:**
```
~/PhotoIndexWithLLM
/Applications/PhotoIndexWithLLM
~/projects/PhotoIndexWithLLM
```

### 2. 路径分隔符

使用 Python 的 `pathlib.Path`，自动处理路径分隔符：
- Windows: `\`
- Linux/macOS: `/`

### 3. 文件权限

提供平台特定的权限设置建议：

**Linux/macOS:**
```bash
chmod 600 .env
chmod 600 data/photo_index.db
```

**Windows (PowerShell):**
```powershell
icacls .env /inheritance:r /grant:r "${env:USERNAME}:R"
```

---

## 📦 安装指南

### Windows

```powershell
# 1. 安装 Python 3.10+
# 从 https://python.org 下载

# 2. 安装依赖
pip install requests

# 3. 安装 LM Studio（可选，用于本地 VL 模型）
# 从 https://lmstudio.ai 下载

# 4. 使用 skill
python skill.py scan --dir D:\Photos
```

### Ubuntu/Linux

```bash
# 1. 安装 Python 3.10+
sudo apt update
sudo apt install python3 python3-pip

# 2. 安装依赖
pip3 install requests

# 3. 安装 LM Studio（可选）
# 从 https://lmstudio.ai 下载 AppImage

# 4. 使用 skill
python3 skill.py scan --dir /home/user/Photos
```

### macOS

```bash
# 1. 安装 Python 3.10+
brew install python

# 2. 安装依赖
pip3 install requests

# 3. 安装 LM Studio（可选）
# 从 https://lmstudio.ai 下载

# 4. 使用 skill
python3 skill.py scan --dir /Users/user/Photos
```

---

## 🔍 跨平台使用示例

### 扫描照片

**Windows:**
```bash
python skill.py scan --dir D:\Photos
python skill.py scan --dir C:\Users\User\Pictures
```

**Ubuntu/Linux:**
```bash
python3 skill.py scan --dir /home/user/Photos
python3 skill.py scan --dir /mnt/external/Photos
```

**macOS:**
```bash
python3 skill.py scan --dir /Users/user/Photos
python3 skill.py scan --dir /Volumes/External/Photos
```

### 搜索照片

所有平台使用相同命令：
```bash
python skill.py search "beach sunset"
python skill.py search "海滩" --format json
```

---

## ⚠️ 平台差异注意事项

### 1. 路径大小写

- **Windows**: 不区分大小写
- **Linux**: 区分大小写
- **macOS**: 默认不区分（但建议区分）

**建议**: 始终使用正确的大小写。

### 2. 文件权限

- **Windows**: 使用 `icacls` 或文件属性
- **Linux/macOS**: 使用 `chmod`

### 3. 环境变量

- **Windows**: `%USERPROFILE%`, `%APPDATA%`
- **Linux/macOS**: `$HOME`, `$XDG_CONFIG_HOME`

### 4. LM Studio 安装

- **Windows**: 安装程序 (.exe)
- **Linux**: AppImage
- **macOS**: 应用程序 (.dmg)

---

## 🧪 跨平台测试

### 测试脚本

```bash
# 测试平台兼容性
python -c "
import platform
from pathlib import Path

print(f'平台: {platform.system()}')
print(f'版本: {platform.version()}')
print(f'架构: {platform.machine()}')
print(f'Python: {platform.python_version()}')
print(f'主目录: {Path.home()}')
"
```

### 预期输出

**Windows:**
```
平台: Windows
版本: 10.0.19045
架构: AMD64
Python: 3.10.11
主目录: C:\Users\User
```

**Ubuntu:**
```
平台: Linux
版本: #1 SMP Ubuntu
架构: x86_64
Python: 3.10.12
主目录: /home/user
```

---

## 📋 兼容性检查清单

- [x] 使用 `pathlib.Path` 处理路径
- [x] 自动检测操作系统
- [x] 平台特定的默认路径
- [x] 跨平台文件权限说明
- [x] Python 3.10+ 兼容
- [x] 无平台特定依赖
- [x] 文档包含多平台说明

---

## 🐛 常见问题

### Q: Linux 上找不到项目？

**A**: 确保项目在以下路径之一：
```
~/PhotoIndexWithLLM
/opt/PhotoIndexWithLLM
```

或者手动指定配置路径：
```bash
python skill.py --config /path/to/.env scan --dir /photos
```

### Q: Windows 上路径错误？

**A**: 使用原始字符串或双反斜杠：
```python
# 正确
r"D:\Photos"
"D:\\Photos"

# 错误（可能被转义）
"D:\Photos"
```

### Q: macOS 权限问题？

**A**: 授予终端完全磁盘访问权限：
1. 系统偏好设置 → 安全性与隐私
2. 隐私 → 完全磁盘访问权限
3. 添加终端应用

---

## 📞 支持

如有跨平台问题，请报告：

**作者**: 北京老李（beijingLL）  
**项目**: PhotoIndexWithLLM

---

**完全跨平台支持！** 🌍
