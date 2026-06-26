# Contributing to Multi-Robot Coordination Skill

感谢你对本项目的关注！我们欢迎各种形式的贡献。

## 如何贡献

### 报告 Bug

如果你发现了 bug，请创建一个 Issue，包含：
- 清晰的标题和描述
- 复现步骤
- 预期行为和实际行为
- 环境信息（Python 版本、操作系统等）
- 相关的错误日志

### 提出新功能

如果你有新功能的想法：
1. 先创建一个 Issue 讨论
2. 说明功能的用途和价值
3. 如果可能，提供设计方案

### 提交代码

1. Fork 本仓库
2. 创建你的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的修改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

### 代码规范

- 遵循 PEP 8 Python 代码风格
- 为新功能添加文档字符串
- 为新功能添加示例
- 确保代码通过现有测试

### 添加新的机器人适配器

如果你想添加新的机器人支持：

1. 在 `adapters/` 目录下创建新的适配器文件
2. 继承 `RobotAdapter` 基类
3. 实现所有必需的方法
4. 添加到 `skill.py` 的注册逻辑中
5. 在 `examples/` 中添加使用示例
6. 更新 README.md

示例结构：
```python
from .base import RobotAdapter, RobotCapability, ActionResult

class MyRobotAdapter(RobotAdapter):
    def __init__(self, name, endpoint, **config):
        super().__init__(name, endpoint, **config)
        # 初始化代码

    def connect(self):
        # 连接逻辑
        pass

    # 实现其他必需方法...
```

## 开发环境设置

```bash
# 克隆仓库
git clone https://github.com/yourusername/multi-robot-skill.git
cd multi-robot-skill

# 安装依赖
pip install -r requirements.txt

# 运行测试
pytest tests/
```

## 行为准则

- 尊重所有贡献者
- 保持友好和专业
- 接受建设性的批评
- 关注对项目最有利的事情

## 问题？

如果有任何问题，欢迎：
- 创建 Issue
- 发送邮件
- 在 Discussions 中讨论

感谢你的贡献！🎉
