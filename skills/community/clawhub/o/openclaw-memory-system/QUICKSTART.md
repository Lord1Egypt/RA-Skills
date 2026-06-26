# 记忆系统技能 - 快速开始指南

## 🚀 5 分钟快速开始

### 1. 安装技能

```bash
# 使用 ClawHub
clawhub install openclaw-memory-system

# 或手动复制
cp -r skills/openclaw-memory-system/skills/* ~/.openclaw/workspace/skills/
cp -r skills/openclaw-memory-system/configs/* ~/.openclaw/workspace/configs/
```

### 2. 初始化配置

```bash
# 运行安装脚本
node skills/openclaw-memory-system/scripts/install.js
```

### 3. 测试功能

```bash
# 测试图片记忆
node skills/multimodal-memory/test-multimodal.js

# 测试反馈解析
node skills/memory-feedback/feedback-parser.js "不对，我不喜欢健身，喜欢游泳"
```

### 4. 开始使用

```javascript
// 保存图片记忆
const { ImageMemory } = require('./skills/multimodal-memory/image-memory');
const imgMem = new ImageMemory();

await imgMem.save({
  path: '/path/to/image.png',
  caption: '我的截图',
  tags: ['测试']
});

// 记录工具调用
const { ToolMemory } = require('./skills/multimodal-memory/tool-memory');
const toolMem = new ToolMemory();

await toolMem.record({
  toolName: 'web_search',
  parameters: { query: '测试' },
  result: { success: true }
});

// 自然语言修正
const { MemoryCorrect } = require('./skills/memory-feedback/memory-correct');
const corrector = new MemoryCorrect();

await corrector.autoCorrect('不对，我其实不喜欢健身，喜欢游泳');
```

## 📚 完整文档

- [README.md](README.md) - 完整使用文档
- [SKILL.md](SKILL.md) - 技能说明
- [configs/](configs/) - 配置文件示例

## 🆘 获取帮助

```bash
# 查看技能列表
clawhub list

# 查看技能详情
clawhub show openclaw-memory-system

# 提交问题
https://github.com/openclaw/openclaw-memory-system/issues
```

## 🎯 下一步

1. 阅读 [README.md](README.md) 了解完整功能
2. 编辑 `configs/multimodal-config.json` 自定义配置
3. 编辑 `configs/memory-namespaces.json` 配置项目/Agent/用户
4. 开始使用记忆系统！

---

**祝你使用愉快！** 🐱
