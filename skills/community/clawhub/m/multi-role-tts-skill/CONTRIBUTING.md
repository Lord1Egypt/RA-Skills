# 贡献指南

感谢你考虑为多角色音频生成器Skill项目做出贡献！本指南将帮助你了解如何有效地参与贡献。

## 🎯 贡献方式

### 1. 报告问题
如果你发现了bug或有功能建议，请通过GitHub Issues报告。

**报告问题时请包含：**
- 清晰的问题描述
- 复现步骤
- 期望的行为
- 实际的行为
- 系统环境信息
- 相关日志或截图

### 2. 提交功能建议
如果你有新功能的想法，欢迎提交功能建议。

**功能建议应包含：**
- 功能描述和用途
- 使用场景示例
- 实现思路（可选）
- 相关参考或灵感

### 3. 代码贡献
如果你想贡献代码，请遵循以下流程：

#### 开发流程
1. **Fork仓库**：点击GitHub页面的Fork按钮
2. **克隆仓库**：`git clone https://github.com/yourusername/multirole-tts-skill.git`
3. **创建分支**：`git checkout -b feature/your-feature-name`
4. **进行修改**：实现你的功能或修复
5. **编写测试**：为你的修改添加测试
6. **提交更改**：`git commit -m "Add: your feature description"`
7. **推送到远程**：`git push origin feature/your-feature-name`
8. **创建Pull Request**：在GitHub上创建PR

#### 代码规范
- 遵循现有的代码风格
- 添加适当的注释
- 确保代码可读性
- 遵循Bash最佳实践

#### 测试要求
- 新功能必须包含测试
- 修复bug时添加回归测试
- 确保所有测试通过
- 测试覆盖率不应降低

### 4. 文档贡献
文档改进同样重要！

**文档贡献包括：**
- 修正拼写和语法错误
- 改进文档清晰度
- 添加使用示例
- 翻译文档
- 创建教程

### 5. 社区支持
你还可以通过以下方式贡献：
- 回答其他用户的问题
- 分享使用经验
- 推广项目
- 提供反馈和建议

## 📁 项目结构

了解项目结构有助于有效贡献：

```
multirole-tts-skill/
├── scripts/                 # 核心脚本
│   └── multirole-generator-final.sh
├── config/                  # 配置系统
│   └── config.sh
├── tests/                   # 测试文件
│   └── test_audio_concatenation.sh
├── examples/                # 示例文件
├── docs/                    # 文档
└── .github/                 # GitHub配置
```

## 🔧 开发环境设置

### 环境要求
- Bash 4.0+
- Python 3.7+
- FFmpeg
- Edge TTS

### 设置步骤
```bash
# 1. 克隆仓库
git clone https://github.com/yourusername/multirole-tts-skill.git
cd multirole-tts-skill

# 2. 安装依赖
./install.sh --check  # 检查依赖
./install.sh --install  # 安装依赖

# 3. 运行测试
./tests/test_audio_concatenation.sh
```

### 测试运行
```bash
# 运行所有测试
./run-tests.sh

# 运行特定测试
./tests/test_audio_concatenation.sh
```

## 📝 提交规范

### 提交消息格式
```
类型: 简要描述

详细描述（可选）

相关Issue: #123
```

### 类型说明
- **Add**: 新功能
- **Fix**: bug修复
- **Update**: 功能更新
- **Docs**: 文档更新
- **Style**: 代码格式
- **Refactor**: 代码重构
- **Test**: 测试相关
- **Chore**: 构建过程或辅助工具

### 示例
```
Add: 支持自定义语音配置文件

- 添加config/voices.json配置文件
- 支持从JSON文件加载语音配置
- 添加配置验证功能

相关Issue: #45
```

## 🧪 测试指南

### 测试类型
1. **单元测试**: 测试单个函数或模块
2. **集成测试**: 测试多个组件协作
3. **功能测试**: 测试完整功能流程
4. **性能测试**: 测试性能和资源使用

### 编写测试
- 测试文件应放在`tests/`目录
- 测试脚本应以`test_`开头
- 每个测试应独立运行
- 测试应清理临时文件

### 测试示例
```bash
#!/bin/bash
# tests/test_example.sh

set -e

# 测试准备
echo "Running example test..."

# 执行测试
# ... 测试代码 ...

# 验证结果
if [ $? -eq 0 ]; then
    echo "✅ Test passed"
else
    echo "❌ Test failed"
    exit 1
fi
```

## 🔍 代码审查

### Pull Request审查
所有Pull Request都需要经过审查。

**审查重点：**
- 代码质量
- 功能完整性
- 测试覆盖
- 文档更新
- 向后兼容性

### 审查流程
1. 创建Pull Request
2. 自动运行CI测试
3. 维护者审查代码
4. 根据反馈进行修改
5. 通过审查后合并

### 审查标准
- ✅ 代码符合项目风格
- ✅ 功能按描述工作
- ✅ 包含必要的测试
- ✅ 更新了相关文档
- ✅ 没有引入新的问题

## 🏆 质量要求

### 代码质量
- 遵循Bash最佳实践
- 添加适当的错误处理
- 保持代码简洁清晰
- 添加必要的注释

### 配置固化
所有命令和参数必须通过配置系统固化：
```bash
# 正确：使用配置变量
$AUDIO_CONCAT_CMD "$concat_list" $AUDIO_CONCAT_PARAMS "$output"

# 错误：硬编码命令
ffmpeg -f concat -safe 0 -i "$concat_list" -c copy "$output"
```

### 错误处理
- 检查命令返回值
- 提供有意义的错误信息
- 清理临时文件
- 支持优雅失败

## 🌍 国际化

### 文档语言
- 主要文档使用中文
- 提供英文翻译
- 欢迎其他语言翻译

### 代码注释
- 核心代码使用英文注释
- 功能说明使用中文注释
- 保持注释清晰准确

## 📊 性能要求

### 音频生成性能
- 单角色音频：< 5秒
- 3角色对话：< 15秒
- 内存使用：< 100MB
- CPU使用：合理范围

### 资源管理
- 及时清理临时文件
- 合理使用系统资源
- 支持并发处理
- 避免内存泄漏

## 🤝 社区行为准则

### 基本原则
- 尊重所有贡献者
- 建设性讨论
- 专业态度
- 互相帮助

### 沟通准则
- 使用清晰的语言
- 提供完整的上下文
- 尊重不同观点
- 保持专业礼貌

### 冲突解决
如发生冲突，请：
1. 保持冷静和专业
2. 寻求事实依据
3. 考虑不同观点
4. 寻求维护者帮助

## 🎖️ 认可贡献

### 贡献者名单
所有贡献者将被记录在：
- GitHub贡献者页面
- 项目README文件
- 发布说明中

### 特别致谢
对于重大贡献，我们会在：
- 项目主页特别致谢
- 发布公告中提及
- 相关文档中记录

## 📞 获取帮助

### 问题解决
- 首先查看文档
- 搜索现有Issue
- 在Discussions提问
- 联系维护者

### 开发帮助
- 查看开发指南
- 参考现有代码
- 询问技术问题
- 请求代码审查

### 社区支持
- 加入OpenClaw社区
- 参与技术讨论
- 分享使用经验
- 帮助其他用户

---

感谢你为多角色音频生成器Skill项目做出贡献！你的每一份贡献都让这个项目变得更好。🎉

**让我们一起创造更优秀的OpenClaw技能！**