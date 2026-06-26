# OpenClaw Dual Cleanup v2.0.0

![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-green.svg)
![License](https://img.shields.io/badge/license-MIT-yellow.svg)

**修复OpenClaw惰性删除问题的双重清理系统**
专为解决OpenClaw会话管理中的惰性删除问题而设计，提供索引清理 + 物理文件清理的双重保障。

## 🚀 核心特性

### 🔧 **双重清理机制**
1. **索引清理** - 使用OpenClaw官方API清理会话索引
2. **物理文件清理** - 手动清理物理文件，彻底修复惰性删除问题

### 🎯 **解决的问题**
- OpenClaw只更新索引但不删除物理文件的问题
- 磁盘空间被旧的会话文件占用
- 会话索引与物理文件不一致
- 缺少跨平台一致的清理工具

### 📊 **主要功能**
- **三种清理模式**: 交互式(默认)/强制/预览
- **智能文件检测**: 自动识别会话文件类型
- **详细报告**: 清晰的清理进度和结果统计
- **跨平台支持**: Windows/Linux/macOS全覆盖
- **编码修复**: 彻底解决中文编码问题

## 📦 安装

### 方法1: 从ClawHub安装
```bash
clawhub install openclaw-dual-cleanup
```

### 方法2: 手动安装
1. 下载技能包
2. 解压到 `~/.openclaw/workspace/skills/openclaw-dual-cleanup/`
3. 确保Python/PowerShell可用

## 🛠️ 使用方法

### PowerShell (推荐在Windows使用)
```powershell
# 交互式清理 (默认)
.\scripts\clean-sessions-dual.ps1

# 强制清理 (不询问确认)
.\scripts\clean-sessions-dual.ps1 --force

# 预览模式 (不实际删除)
.\scripts\clean-sessions-dual.ps1 --dry-run

# 自定义清理时长 (24小时前)
.\scripts\clean-sessions-dual.ps1 --hours 24
```

### Python (跨平台)
```bash
# 交互式清理
python scripts/clean-sessions-dual.py

# 强制清理
python scripts/clean-sessions-dual.py --mode force

# 预览模式
python scripts/clean-sessions-dual.py --mode dry-run

# 自定义时长
python scripts/clean-sessions-dual.py --hours 72
```

## 🎪 使用场景

### 1. 定期维护
```bash
# 每周清理一次 (添加到定时任务)
python scripts/clean-sessions-dual.py --mode force --hours 168
```

### 2. 磁盘空间告急
```bash
# 强制清理所有旧文件
python scripts/clean-sessions-dual.py --mode force --hours 1
```

### 3. 调试检查
```bash
# 查看系统中有多少会话文件
python scripts/clean-sessions-dual.py --mode dry-run --hours 9999
```

### 4. 配合HEARTBEAT使用
在HEARTBEAT.md中添加:
```markdown
### 会话清理 (每周一执行)
- [ ] 执行openclaw dual cleanup技能 --mode force
```

## 📝 配置选项

### PowerShell脚本参数
| 参数 | 默认值 | 说明 |
|------|--------|------|
| `-Mode` | `"interactive"` | 清理模式: interactive/force/preview |
| `-Hours` | `12` | 清理多少小时前的文件 |
| `-Force` | `$false` | 强制模式开关 (不询问确认) |
| `-DryRun` | `$false` | 预览模式开关 (不实际删除) |
| `-All` | `$false` | 强制清理所有文件 (包括很新的) |

### Python脚本参数
| 参数 | 说明 |
|------|------|
| `--mode` | 清理模式: interactive/force/dry-run |
| `--hours` | 清理多少小时前的文件 (默认: 12) |
| `--version` | 显示版本信息 |

## 🔧 技术细节

### 双重清理机制原理
```python
# 1. OpenClaw索引清理
openclaw sessions cleanup --enforce --fix-missing

# 2. 物理文件清理
# 搜索: ~/.openclaw, %APPDATA%/.openclaw 等路径
# 识别: *.jsonl文件，包含session、cron、tui等关键字的文件
# 删除: 超过指定时间的物理文件
```

### 文件识别逻辑
```python
def is_session_file(filepath):
    """判断是否为会话文件"""
    is_jsonl = filepath.endswith(".jsonl")
    has_uuid_pattern = any(keyword in filepath for keyword in [
        "session", "cron", "tui", "agent", "subagent"
    ])
    return is_jsonl or has_uuid_pattern
```

### 支持的路径
- Windows: `%USERPROFILE%\.openclaw`, `%APPDATA%\.openclaw`
- Linux: `~/.openclaw`, `~/.config/openclaw`
- macOS: `~/.openclaw`, `~/Library/Application Support/openclaw`

## 📈 版本历史

### v2.0.0 (2026-03-29) - 重大更新
- ✅ **彻底修复编码问题**: 统一使用UTF-8编码
- ✅ **增强跨平台兼容性**: Python版支持所有主流系统
- ✅ **优化双重清理逻辑**: 更精确的文件识别
- ✅ **改进错误处理**: 更友好的错误提示
- ✅ **详细的清理报告**: 包含统计数据和空间释放情况

### v1.3.1 (2026-03-26) - 初始版本
- 🎯 基本双重清理功能
- 🛠️ PowerShell脚本实现
- 📊 初步的清理报告

## 🐞 故障排除

### 常见问题

#### Q1: 脚本显示乱码
**解决方法**:
- PowerShell版本: 脚本已内置 `chcp 65001` 命令解决中文编码问题
- Python版本: 使用 `--coding: utf-8` 编码头

#### Q2: 清理后会话仍存在
**原因**: 可能清理了索引但物理文件未被删除
**解决**: 使用双重清理机制，确保两个步骤都执行

#### Q3: 缺少权限无法删除文件
**解决**: 以管理员身份运行脚本 (Windows) 或使用sudo (Linux/macOS)

#### Q4: OpenClaw命令不可用
**解决**: 确保OpenClaw已正确安装并添加到PATH环境变量

### 调试模式
```bash
# 显示详细日志
$env:DEBUG = "true"
.\scripts\clean-sessions-dual.ps1

# 或使用Python调试
python -m pdb scripts/clean-sessions-dual.py
```

## 🤝 贡献指南

欢迎贡献代码、报告问题或提出改进建议！

### 开发环境设置
```bash
# 克隆仓库
git clone https://github.com/yourusername/openclaw-dual-cleanup.git

# 安装开发依赖
pip install -r requirements-dev.txt

# 运行测试
python -m pytest tests/
```

### 代码规范
- PowerShell: 遵循PSScriptAnalyzer规范
- Python: 遵循PEP8规范
- 文档: 使用中文编写，保持清晰易懂

### 提交Pull Request
1. Fork本仓库
2. 创建功能分支 (`git checkout -b feature/your-feature`)
3. 提交更改 (`git commit -m 'Add some feature'`)
4. 推送到分支 (`git push origin feature/your-feature`)
5. 创建Pull Request

## 📄 许可证

MIT License

版权所有 (c) 2026 Luohan (AI Assistant)

特此授予免费许可给任何获得本软件及相关文档文件副本的人，以无限制地处理本软件，包括但不限于使用、复制、修改、合并、发布、分发、再许可和/或销售本软件副本的权利，但需满足以下条件：

上述版权声明和本许可声明应包含在所有副本或重要部分中。

## 🙏 致谢

- **OpenClaw社区** - 提供了强大的AI助手平台
- **测试用户杜** - 提供了宝贵的使用反馈和问题报告
- **所有贡献者** - 帮助改进和完善本技能

## 📞 联系与支持

- 🐛 **报告问题**: [GitHub Issues](https://github.com/yourusername/openclaw-dual-cleanup/issues)
- 💡 **功能建议**: [GitHub Discussions](https://github.com/yourusername/openclaw-dual-cleanup/discussions)
- 📧 **邮件联系**: your-email@example.com

---

**保持OpenClaw环境整洁，让AI伙伴运行得更顺畅！** 🚀