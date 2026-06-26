# OpenClaw配置模板库

本目录包含各种OpenClaw配置模板，适用于不同场景和需求。

## 模板列表

### 1. minimal.json - 最小配置
**适用场景**: 快速启动、测试、最小化部署
**特点**:
- 仅包含必需字段
- 单个Agent
- 默认模型
- 适合学习和测试

**使用命令**:
```bash
cp config_templates/minimal.json ~/.openclaw/openclaw.json
```

### 2. standard.json - 标准配置
**适用场景**: 日常使用、个人助手
**特点**:
- 多Agent协作
- 多模型Provider
- 工作空间配置
- 子Agent权限管理

**使用命令**:
```bash
cp config_templates/standard.json ~/.openclaw/openclaw.json
# 设置环境变量
export DEEPSEEK_API_KEY="your_key"
export QWEN_API_KEY="your_key"
```

### 3. enterprise.json - 企业级配置
**适用场景**: 团队协作、生产环境
**特点**:
- 完整的Agent团队
- 多通道集成（飞书、企业微信）
- 插件系统
- 环境变量配置
- 生产环境优化

**使用命令**:
```bash
cp config_templates/enterprise.json ~/.openclaw/openclaw.json
# 设置所有环境变量
export DEEPSEEK_API_KEY="your_key"
export QWEN_API_KEY="your_key"
export FEISHU_APP_ID="your_app_id"
export FEISHU_APP_SECRET="your_secret"
export WECOM_CORP_ID="your_corp_id"
export WECOM_SECRET="your_secret"
export WECOM_AGENT_ID="your_agent_id"
```

### 4. development.json - 开发配置
**适用场景**: 软件开发、本地测试
**特点**:
- 代码开发优化
- 本地模型集成（Ollama）
- 质量保证Agent
- 开发环境配置

**使用命令**:
```bash
cp config_templates/development.json ~/.openclaw/openclaw.json
# 确保Ollama服务运行
ollama serve
# 设置API密钥
export DEEPSEEK_API_KEY="your_key"
export QWEN_API_KEY="your_key"
```

## 模板选择指南

### 根据使用场景选择

| 场景 | 推荐模板 | 说明 |
|------|----------|------|
| **初次体验** | minimal.json | 最简单，无复杂配置 |
| **个人助手** | standard.json | 平衡功能和复杂度 |
| **团队协作** | enterprise.json | 完整的企业功能 |
| **代码开发** | development.json | 开发优化，本地模型 |
| **生产部署** | enterprise.json | 稳定可靠，功能完整 |

### 根据技术能力选择

| 技术水平 | 推荐模板 | 说明 |
|----------|----------|------|
| **初学者** | minimal.json | 配置简单，易于理解 |
| **中级用户** | standard.json | 需要基本的API密钥配置 |
| **高级用户** | enterprise.json | 需要完整的环境配置 |
| **开发者** | development.json | 需要本地模型和开发工具 |

## 自定义模板

### 基于现有模板修改
```bash
# 1. 复制模板
cp config_templates/standard.json my_config.json

# 2. 修改配置
# 编辑 my_config.json，调整Agent、模型等设置

# 3. 应用配置
cp my_config.json ~/.openclaw/openclaw.json
```

### 创建新模板
```bash
# 1. 创建新模板文件
touch config_templates/my_template.json

# 2. 编写配置
# 参考现有模板的结构

# 3. 更新README
# 添加新模板的描述
```

## 模板变量说明

### 环境变量
模板中使用 `${VARIABLE_NAME}` 格式表示需要设置的环境变量：

| 变量名 | 说明 | 获取方式 |
|--------|------|----------|
| `DEEPSEEK_API_KEY` | DeepSeek API密钥 | [DeepSeek平台](https://platform.deepseek.com) |
| `QWEN_API_KEY` | 千问API密钥 | [阿里云DashScope](https://dashscope.aliyun.com) |
| `FEISHU_APP_ID` | 飞书应用ID | 飞书开放平台 |
| `FEISHU_APP_SECRET` | 飞书应用密钥 | 飞书开放平台 |
| `WECOM_CORP_ID` | 企业微信企业ID | 企业微信管理后台 |
| `WECOM_SECRET` | 企业微信应用密钥 | 企业微信管理后台 |
| `WECOM_AGENT_ID` | 企业微信应用ID | 企业微信管理后台 |

### 路径变量
| 变量 | 说明 | 默认值 |
|------|------|--------|
| `~/OpenClaw输出` | 工作空间目录 | 用户主目录下的OpenClaw输出目录 |
| `.openclaw-memory` | 记忆存储目录 | 当前目录下的隐藏目录 |

## 验证模板

### 验证配置有效性
```bash
# 使用配置验证器
python3 ../config_validator.py --config your_template.json
```

### 测试模板
```bash
# 1. 备份当前配置
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.backup

# 2. 应用模板
cp config_templates/standard.json ~/.openclaw/openclaw.json

# 3. 启动测试
openclaw gateway start

# 4. 恢复配置（如果需要）
cp ~/.openclaw/openclaw.json.backup ~/.openclaw/openclaw.json
```

## 贡献指南

欢迎提交新的配置模板！

### 提交要求
1. **文件命名**: 使用描述性名称，如 `ai-research.json`
2. **JSON格式**: 使用2空格缩进，确保JSON有效性
3. **完整注释**: 在meta字段中添加详细描述
4. **测试验证**: 确保配置能正常工作
5. **文档更新**: 更新此README文件

### 模板结构要求
```json
{
  "gateway": { ... },
  "agents": { ... },
  "models": { ... },
  "meta": {
    "lastTouchedVersion": "2026.4.15",
    "createdAt": "YYYY-MM-DDTHH:MM:SSZ",
    "template": "template_name",
    "description": "模板描述"
  }
}
```

## 更新日志

### 2026-04-18
- 初始版本发布
- 包含4个基础模板
- 完整的文档说明

## 支持

如有问题或建议，请：
1. 查看OpenClaw官方文档
2. 提交GitHub Issue
3. 加入社区讨论

---

**注意**: 使用模板前请确保理解配置内容，生产环境建议先测试。