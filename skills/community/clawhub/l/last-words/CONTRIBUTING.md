# 贡献指南

感谢你对 last-words 项目的关注！

## 如何贡献

### 报告问题

如果你发现了 bug 或有功能建议，请通过 [GitHub Issues](https://github.com/yourusername/last-words/issues) 提交。

提交 Issue 时请包含：
- 问题描述
- 复现步骤
- 期望行为
- 实际行为
- 环境信息（操作系统、Python版本等）

### 提交代码

1. **Fork 项目**
   ```bash
   git clone https://github.com/yourusername/last-words.git
   cd last-words
   ```

2. **创建分支**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **提交更改**
   ```bash
   git commit -m "feat: add some feature"
   ```

4. **推送并创建 PR**
   ```bash
   git push origin feature/your-feature-name
   ```

### 代码规范

- 遵循 PEP 8 规范
- 添加适当的注释和文档字符串
- 确保代码能在 Python 3.8+ 运行

### 提交信息格式

使用 [Conventional Commits](https://www.conventionalcommits.org/)：

- `feat:` 新功能
- `fix:` 修复 bug
- `docs:` 文档更新
- `refactor:` 代码重构
- `test:` 测试相关
- `chore:` 构建/工具相关

## 开发环境设置

```bash
# 克隆项目
git clone https://github.com/yourusername/last-words.git
cd last-words

# 创建虚拟环境（可选）
python3 -m venv venv
source venv/bin/activate

# 安装依赖（本项目无外部依赖，仅使用标准库）
# 测试配置
python3 scripts/configure_delivery.py --help
```

## 测试

在提交 PR 前，请确保：

1. 所有脚本可以正常执行
2. 邮件发送功能已测试（使用调试模式）
3. 没有引入新的问题

```bash
# 测试配置
python3 scripts/get_status.py

# 测试调试模式
python3 scripts/debug_mode.py on
python3 scripts/debug_mode.py send
python3 scripts/debug_mode.py off
```

## 行为准则

- 尊重他人
- 接受建设性批评
- 关注对社区最有利的事
- 展现同理心

## 隐私提醒

**永远不要**在代码或提交中包含：
- 真实邮箱地址
- 邮箱密码或授权码
- 个人身份信息

使用示例数据：
- 邮箱：`example@qq.com`
- 授权码：`xxxxxxxxxxxxxxxx`

## 需要帮助？

- 查看 [README.md](README.md)
- 查看 [GitHub Discussions](https://github.com/yourusername/last-words/discussions)
- 加入 OpenClaw 社区

感谢你的贡献！
