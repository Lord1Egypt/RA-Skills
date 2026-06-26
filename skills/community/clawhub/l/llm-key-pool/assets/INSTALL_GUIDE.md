# 平台集成安装快速指南

## 📋 概述

本文档帮助您快速集成安装以下4个平台：
- **小龙虾（XiaoLongXia）** - 专为大模型推理优化
- **OpenCode** - 专注代码生成
- **Qwen独立API** - 通义千问独立服务
- **ClaudeCode** - Anthropic Claude代码专用版本

## 🚀 三种配置方式

### 方式1：使用配置助手（推荐）

```bash
cd assets
python setup_helper.py
```

按照提示选择：
1. 快速配置向导 - 交互式创建配置文件
2. 查看获取API Key指南 - 了解如何获取各平台API Key
3. 测试现有配置 - 验证配置是否正确

### 方式2：使用快速配置模板

```bash
# 1. 复制快速配置模板
cp assets/llm_config.quickstart.yaml ./llm_config.yaml

# 2. 编辑配置文件，替换API Key
vim ./llm_config.yaml

# 3. 测试配置
python -m llm_key_pool.llm_client \
  --config ./llm_config.yaml \
  --test
```

### 方式3：手动配置

参考 `assets/PLATFORM_SETUP_GUIDE.md` 中的详细说明。

## 📖 详细文档

- **平台集成完整指南**：`assets/PLATFORM_SETUP_GUIDE.md`
- **配置格式说明**：`references/config_format.md`
- **支持平台列表**：`references/supported_providers.md`

## 🔧 最小配置示例

如果您只想配置1个平台快速开始：

```yaml
providers:
  xiaolongxia:
    tier: fallback
    model: "xiaolongxia-72b"
    api_keys:
      - "你的API-Key"
    base_url: "https://api.xiaolongxia.com/v1"

global:
  max_retries: 3
  cooldown_seconds: 300
```

## ✅ 验证步骤

配置完成后，执行以下命令验证：

```bash
# 1. 查看配置状态
python -m llm_key_pool.llm_client \
  --config ./llm_config.yaml \
  --status

# 2. 测试连接
python -m llm_key_pool.llm_client \
  --config ./llm_config.yaml \
  --test

# 3. 发送测试请求
python -m llm_key_pool.llm_client \
  --config ./llm_config.yaml \
  --prompt "你好，请介绍一下自己"
```

## 🎯 各平台特点

| 平台 | 层级推荐 | 模型 | 特色 |
|------|---------|------|------|
| 小龙虾 | primary | xiaolongxia-72b | 推理优化 |
| OpenCode | fallback | opencode-72b | 代码生成 |
| Qwen | fallback | qwen-max | 综合能力强 |
| ClaudeCode | fallback | claude-3-5-sonnet | 代码质量高 |

## 💡 使用建议

1. **小龙虾**：作为主力层，处理大部分任务
2. **OpenCode**：用于代码生成和审查
3. **Qwen**：日常对话和知识问答
4. **ClaudeCode**：复杂代码调试和架构设计

## ⚠️ 注意事项

1. **API Key安全**：不要将配置文件提交到版本控制
2. **额度监控**：定期检查各平台使用情况
3. **层级策略**：根据需求调整平台层级
4. **ClaudeCode价格**：相对较高，建议作为兜底使用

## 🆘 常见问题

**Q1: API Key在哪里获取？**
- 参考 `PLATFORM_SETUP_GUIDE.md` 中的详细说明

**Q2: 配置后无法调用？**
- 检查API Key是否正确
- 检查网络连接
- 查看错误日志

**Q3: 如何选择模型？**
- 72B模型：复杂任务，高质量
- 34B模型：平衡性能
- 14B模型：快速响应

**Q4: ClaudeCode为什么特殊？**
- 使用特殊的请求头格式
- Skill已自动处理，无需担心

## 📞 获取帮助

如遇问题，请查看：
1. `PLATFORM_SETUP_GUIDE.md` - 详细安装指南
2. `supported_providers.md` - 平台配置说明
3. `config_format.md` - 配置格式规范

## 🎉 开始使用

配置完成后，即可开始使用：

```bash
python -m llm_key_pool.llm_client \
  --config ./llm_config.yaml \
  --prompt "你的问题"
```

祝您使用愉快！🎊
