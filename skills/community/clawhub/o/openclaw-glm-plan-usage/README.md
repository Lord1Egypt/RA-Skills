# OpenClaw GLM Plan Usage Skill

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-green.svg)](https://openclaw.dev)
[![Version](https://img.shields.io/badge/version-1.0.0-brightgreen.svg)](SKILL.md)

Query GLM Coding Plan usage statistics directly from OpenClaw. Monitors token quotas, model usage, and MCP tool usage with clean, formatted output.

[简体中文](#简体中文) | English

---

## Features

- **Quota Monitoring**: View token usage (5-hour) and MCP usage (1-month) with progress indicators
- **Model Usage**: Display 24-hour token and call statistics
- **Tool Usage**: Track MCP tool usage over 24 hours
- **Auto-detection**: Automatically detects GLM Coding Plan providers from OpenClaw configuration
- **Zero Dependencies**: Pure Bash implementation using curl and jq
- **Chinese Output**: Optimized for Zhipu platform with Chinese language output

## Preview

```
📊 GLM 编码套餐使用统计

提供商: zhipu
统计时间: 2026-02-13 20:30:15

配额限制
---
  Token 使用 (5小时): 45.2%
  MCP 使用 (1个月):   12.3%  (15000/120000 秒) [LEVEL_4]

模型使用 (24小时)
---
  总 Token 数:  12,500,000
  总调用次数:  1,234

工具使用 (24小时)
---
  bash: 156 次
  file-read: 89 次
  web-search: 34 次
```

## Quick Start

### Prerequisites

Install required dependencies:

```bash
# Linux
sudo apt-get install jq curl

# macOS
brew install jq curl
```

### Installation

1. Clone this repository:
```bash
git clone https://github.com/USERNAME/openclaw-glm-plan-usage.git
cd openclaw-glm-plan-usage
```

2. Copy to OpenClaw skills directory:
```bash
cp -r . ~/.openclaw/skills/glm-plan-usage/
chmod +x ~/.openclaw/skills/glm-plan-usage/scripts/query-usage.sh
```

3. Configure your GLM Coding Plan provider in `~/.openclaw/openclaw.json`:

```json
{
  "models": {
    "providers": {
      "zhipu": {
        "baseUrl": "https://open.bigmodel.cn/api/coding/paas/v4",
        "apiKey": "your-api-key-here"
      }
    }
  }
}
```

### Usage

Run the script directly:
```bash
bash ~/.openclaw/skills/glm-plan-usage/scripts/query-usage.sh
```

Or invoke via OpenClaw:
```bash
openclaw /glm-plan-usage:usage-query
```

## Configuration

The skill automatically reads your provider configuration from `~/.openclaw/openclaw.json`.

### Provider Detection

The skill recognizes GLM Coding Plan providers when:
- The `baseUrl` contains `api/coding/paas/v4` or `open.bigmodel.cn`
- The provider name includes `coding`, `glm-coding`, `zhipu`, or `bigmodel`

### Example Configuration

```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "zhipu/glm-4-flash"
      }
    }
  },
  "models": {
    "providers": {
      "zhipu": {
        "baseUrl": "https://open.bigmodel.cn/api/coding/paas/v4",
        "apiKey": "your-api-key-here"
      }
    }
  }
}
```

## Output Explanation

| Section | Description | Time Window |
|---------|-------------|-------------|
| 配额限制 (Quota Limits) | Token usage percentage and MCP usage time | 5-hour / 1-month |
| 模型使用 (Model Usage) | Total tokens consumed and API call count | 24-hour |
| 工具使用 (Tool Usage) | MCP tool usage breakdown | 24-hour |

## Troubleshooting

### "缺少依赖工具，请安装: jq"

Install jq using your package manager:
```bash
sudo apt-get install jq  # Linux
brew install jq           # macOS
```

### "未找到配置 GLM 编码套餐的提供商"

Ensure your provider's `baseUrl` contains `api/coding/paas/v4`:

```json
{
  "models": {
    "providers": {
      "your-provider": {
        "baseUrl": "https://open.bigmodel.cn/api/coding/paas/v4"
      }
    }
  }
}
```

### "认证失败，请检查 API 密钥配置"

Verify your API key in OpenClaw config:
```bash
jq -r '.models.providers.zhipu.apiKey' ~/.openclaw/openclaw.json
```

## Development

### Project Structure

```
openclaw-glm-plan-usage/
├── SKILL.md                 # Skill metadata
├── README.md                # This file
├── LICENSE                  # MIT License
├── .gitignore              # Git exclusions
├── scripts/
│   └── query-usage.sh       # Main script
├── references/
│   └── api-endpoints.md     # API documentation
└── docs/
    └── INSTALLATION.md      # Installation guide
```

### Testing

Test the script manually:
```bash
# Direct execution
bash scripts/query-usage.sh

# Check exit code
echo $?
```

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - See [LICENSE](LICENSE) for details.

## Credits

- Original implementation: [zai-coding-plugins](https://github.com/zai-org/zai-coding-plugins)
- Reference implementation: [opencode-glm-quota](https://github.com/guyinwonder168/opencode-glm-quota)
- OpenClaw integration: This skill

## Support

For issues or questions:
1. Check the [API documentation](references/api-endpoints.md)
2. Review the [Installation Guide](docs/INSTALLATION.md)
3. Verify your OpenClaw configuration

---

# 简体中文

用于查询 GLM 编码套餐使用统计的 OpenClaw 技能。监控 Token 配额、模型使用和 MCP 工具使用，提供清晰的格式化输出。

## 功能特性

- **配额监控**: 查看 Token 使用量（5小时）和 MCP 使用量（1个月），带进度指示器
- **模型使用**: 显示 24 小时内的 Token 数和调用统计
- **工具使用**: 跟踪 24 小时内的 MCP 工具使用情况
- **自动检测**: 自动从 OpenClaw 配置中检测 GLM 编码套餐提供商
- **零依赖**: 纯 Bash 实现，仅使用 curl 和 jq
- **中文输出**: 为智谱平台优化，提供中文输出

## 快速开始

### 前置要求

安装所需依赖：

```bash
# Linux
sudo apt-get install jq curl

# macOS
brew install jq curl
```

### 安装

1. 克隆本仓库：
```bash
git clone https://github.com/USERNAME/openclaw-glm-plan-usage.git
cd openclaw-glm-plan-usage
```

2. 复制到 OpenClaw 技能目录：
```bash
cp -r . ~/.openclaw/skills/glm-plan-usage/
chmod +x ~/.openclaw/skills/glm-plan-usage/scripts/query-usage.sh
```

3. 在 `~/.openclaw/openclaw.json` 中配置 GLM 编码套餐提供商：

```json
{
  "models": {
    "providers": {
      "zhipu": {
        "baseUrl": "https://open.bigmodel.cn/api/coding/paas/v4",
        "apiKey": "your-api-key-here"
      }
    }
  }
}
```

### 使用方法

直接运行脚本：
```bash
bash ~/.openclaw/skills/glm-plan-usage/scripts/query-usage.sh
```

或通过 OpenClaw 调用：
```bash
openclaw /glm-plan-usage:usage-query
```

## 配置说明

技能会自动读取 `~/.openclaw/openclaw.json` 中的提供商配置。

### 提供商检测

当满足以下条件时，技能会识别 GLM 编码套餐提供商：
- `baseUrl` 包含 `api/coding/paas/v4` 或 `open.bigmodel.cn`
- 提供商名称包含 `coding`、`glm-coding`、`zhipu` 或 `bigmodel`

## 故障排除

### "缺少依赖工具，请安装: jq"

```bash
sudo apt-get install jq  # Linux
brew install jq           # macOS
```

### "未找到配置 GLM 编码套餐的提供商"

确保提供商的 `baseUrl` 包含 `api/coding/paas/v4`。

### "认证失败，请检查 API 密钥配置"

验证 OpenClaw 配置中的 API 密钥：
```bash
jq -r '.models.providers.zhipu.apiKey' ~/.openclaw/openclaw.json
```

## 贡献

欢迎贡献！请：

1. Fork 本仓库
2. 创建特性分支
3. 提交更改
4. 发起 Pull Request

## 许可证

MIT License - 详见 [LICENSE](LICENSE)。

## 致谢

- 原始实现: [zai-coding-plugins](https://github.com/zai-org/zai-coding-plugins)
- 参考实现: [opencode-glm-quota](https://github.com/guyinwonder168/opencode-glm-quota)
