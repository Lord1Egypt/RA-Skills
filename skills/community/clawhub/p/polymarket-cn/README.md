# Polymarket

> 请在此处填写一句话描述

## 🚀 快速开始

```bash
cd /home/gem/workspace/agent/skills/polymarket

# 运行测试
./scripts/main.sh --test

# 查看帮助
./scripts/main.sh --help
```

## 📖 详细文档

请参阅 [SKILL.md](SKILL.md) 获取完整的使用说明。

## 🛠️ 开发指南

### 本地测试

```bash
# 修改代码后测试
./scripts/main.sh --test

# 查看日志
tail -f data/*.log
```

### 调试技巧

1. 启用调试模式：在 config.json 中设置 `"debug": true`
2. 查看详细日志：`bash -x scripts/main.sh`
3. 单步调试：在脚本中添加 `set -x`

## 📝 待办事项

- [ ] 实现核心功能
- [ ] 添加单元测试
- [ ] 完善文档
- [ ] 添加更多示例

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 License

MIT
