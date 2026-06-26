# 🏗️ master-agent-workflow-global

## 📖 概述

`master-agent-workflow-global` 是一个全局可迁移的主控代理工作流技能，专为需要并行任务调度、代理层级控制和完整错误处理的场景设计。

这是原始 `master-agent-workflow` 技能的全局可迁移版本，支持一键安装、配置迁移和跨平台使用。

## ✨ 特性

- ✅ **全局可迁移**: 在任何OpenClaw实例中安装即可使用
- ✅ **一键安装**: 通过安装脚本或ClawdHub快速安装
- ✅ **配置迁移**: 支持导出/导入配置和模板
- ✅ **模板系统**: 预定义任务模板，快速启动
- ✅ **跨平台兼容**: Windows/Linux/macOS全支持
- ✅ **版本管理**: 语义化版本，支持升级和回滚

## 🚀 快速开始

### 安装

```bash
# 方法1: 使用安装脚本
./install.sh

# 方法2: 通过ClawdHub
clawdhub install master-agent-workflow-global

# 方法3: 手动安装
cp -r master-agent-workflow-global ~/.openclaw/global-skills/
```

### 基本使用

```bash
# 使用默认配置执行任务
使用 master-agent-workflow-global execute "处理我的任务"

# 快捷命令
maw "处理我的任务"

# 指定并行数和超时
maw "批量处理" --max-workers 10 --timeout 2h
```

## 📦 发布信息

### 当前版本
- **版本**: 2.0.0
- **发布日期**: 2026-03-27
- **作者**: 小龙
- **许可证**: MIT

### 发布包
- **文件名**: `master-agent-workflow-global-v2.0.0.tar.gz`
- **大小**: 约 50KB
- **校验和**: 见 `SHA256SUMS` 文件

## 🔧 开发

### 项目结构
```
master-agent-workflow-global/
├── .clawhub/                    # ClawdHub元数据
├── assets/                      # 资源文件
├── hooks/                       # 钩子脚本
├── references/                  # 参考文档
├── scripts/                     # 脚本文件
├── templates/                   # 模板文件
├── skill.json                   # 技能元数据
├── SKILL.md                     # 技能主文档
├── install.sh                   # 安装脚本
└── publish-to-clawdhub.sh       # 发布脚本
```

### 构建发布包
```bash
# Linux/macOS
./publish-to-clawdhub.sh

# Windows
publish-to-clawdhub.bat
```

## 📄 文档

- [SKILL.md](SKILL.md) - 完整技能文档
- [references/examples.md](references/examples.md) - 使用示例
- [migration-guide.md](migration-guide.md) - 迁移指南

## 🤝 贡献

欢迎贡献！请遵循以下步骤：

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📝 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 📞 联系

- **作者**: 小龙
- **GitHub**: [xiaolong-ai](https://github.com/xiaolong-ai)
- **问题反馈**: [GitHub Issues](https://github.com/xiaolong-ai/master-agent-workflow/issues)

## 🙏 致谢

感谢所有为这个项目做出贡献的人！

---

**技能状态**: ✅ 生产就绪  
**最后更新**: 2026-03-27  
**兼容性**: OpenClaw >= 1.0.0