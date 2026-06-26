# GLM Plan Usage Skill - Installation Guide

[简体中文](#简体中文) | English

---

# English

## Prerequisites

Before installing this skill, ensure you have:

1. **OpenClaw** installed and configured
2. **jq** - JSON processor for command-line
3. **curl** - HTTP client (usually pre-installed)
4. **GLM Coding Plan** subscription with valid API key

### Installing Dependencies

#### Linux (Debian/Ubuntu)
```bash
sudo apt-get update
sudo apt-get install -y jq curl
```

#### Linux (CentOS/RHEL/Fedora)
```bash
sudo dnf install -y jq curl
# or for older systems:
sudo yum install -y jq curl
```

#### macOS
```bash
brew install jq curl
```

#### Verify Installation
```bash
jq --version
curl --version
```

## Installation Methods

### Method 1: Clone from GitHub (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/USERNAME/openclaw-glm-plan-usage.git
cd openclaw-glm-plan-usage
```

2. Copy to OpenClaw skills directory:
```bash
cp -r . ~/.openclaw/skills/glm-plan-usage/
```

3. Make the script executable:
```bash
chmod +x ~/.openclaw/skills/glm-plan-usage/scripts/query-usage.sh
```

### Method 2: Manual Download

1. Download the repository as ZIP from GitHub
2. Extract the archive:
```bash
unzip openclaw-glm-plan-usage.zip
cd openclaw-glm-plan-usage
```

3. Copy to OpenClaw skills directory:
```bash
cp -r . ~/.openclaw/skills/glm-plan-usage/
chmod +x ~/.openclaw/skills/glm-plan-usage/scripts/query-usage.sh
```

### Method 3: Direct File Creation

Create the directory structure manually:
```bash
mkdir -p ~/.openclaw/skills/glm-plan-usage/{scripts,references,docs}
```

Then download individual files from GitHub and place them in the corresponding directories.

## Configuration

### Step 1: Obtain GLM Coding Plan API Key

1. Visit [GLM Coding Plan](https://open.bigmodel.cn)
2. Sign up or log in
3. Navigate to API Keys section
4. Generate or copy your API key

### Step 2: Configure OpenClaw

Edit your OpenClaw configuration file:
```bash
nano ~/.openclaw/openclaw.json
```

Add or update the provider configuration:

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

**Important Configuration Notes**:
- The `baseUrl` **must** contain `api/coding/paas/v4` or `open.bigmodel.cn`
- Replace `your-api-key-here` with your actual API key
- The provider name (`zhipu` in example) can be any name you prefer

### Alternative Configuration (Multiple Providers)

If you have multiple providers configured, the skill will automatically detect the GLM Coding Plan provider:

```json
{
  "models": {
    "providers": {
      "anthropic": {
        "baseUrl": "https://api.anthropic.com/v1",
        "apiKey": "anthropic-key"
      },
      "glm-coding": {
        "baseUrl": "https://open.bigmodel.cn/api/coding/paas/v4",
        "apiKey": "glm-coding-key"
      }
    }
  }
}
```

The skill will detect `glm-coding` as the GLM Coding Plan provider based on its `baseUrl`.

## Verification

### Test the Script

Run the script directly to verify installation:
```bash
bash ~/.openclaw/skills/glm-plan-usage/scripts/query-usage.sh
```

Expected output:
```
📊 GLM 编码套餐使用统计

提供商: zhipu
统计时间: 2026-02-13 20:30:15

配额限制
---
  Token 使用 (5小时): XX.X%
  MCP 使用 (1个月):   XX.X%  (XXXXX/XXXXXX 秒) [LEVEL_X]

模型使用 (24小时)
---
  总 Token 数:  X,XXX,XXX
  总调用次数:  XXX

工具使用 (24小时)
---
  tool-name: XX 次
```

### Test via OpenClaw

If OpenClaw supports skill invocation, test it:
```bash
openclaw /glm-plan-usage:usage-query
```

### Verify Exit Code

The script returns:
- `0` - Success
- `1` - Error (missing dependencies, config issues, API errors)

```bash
bash ~/.openclaw/skills/glm-plan-usage/scripts/query-usage.sh
echo $?  # Should print 0 on success
```

## Troubleshooting

### Issue: "缺少依赖工具，请安装: jq"

**Solution**: Install jq using your package manager (see Prerequisites above)

### Issue: "未找到 OpenClaw 配置文件"

**Solution**: Ensure OpenClaw is installed and has created `~/.openclaw/openclaw.json`

```bash
# Check if config exists
ls -la ~/.openclaw/openclaw.json

# If not, create basic config
mkdir -p ~/.openclaw
echo '{"models":{"providers":{}}}' > ~/.openclaw/openclaw.json
```

### Issue: "未找到配置 GLM 编码套餐的提供商"

**Solution**: Verify your provider configuration includes the correct `baseUrl`:

```bash
# Check current providers
jq '.models.providers' ~/.openclaw/openclaw.json
```

Ensure the `baseUrl` contains `api/coding/paas/v4`.

### Issue: "认证失败，请检查 API 密钥配置"

**Solution**: Verify your API key is valid and correctly configured:

```bash
# Test API key manually
curl -H "Authorization: your-api-key" \
     "https://open.bigmodel.cn/api/coding/paas/v4/api/monitor/usage/quota/limit"
```

### Issue: "API 请求超时"

**Solution**: Check network connectivity and API availability:

```bash
# Test connectivity
ping open.bigmodel.cn
curl -I https://open.bigmodel.cn
```

## Uninstallation

To remove the skill:
```bash
rm -rf ~/.openclaw/skills/glm-plan-usage
```

To remove only the configuration (keeping other providers):
```bash
# Edit config and remove the GLM Coding Plan provider
nano ~/.openclaw/openclaw.json
```

## Upgrading

To upgrade to the latest version:

```bash
# Backup current version
mv ~/.openclaw/skills/glm-plan-usage ~/.openclaw/skills/glm-plan-usage.bak

# Clone latest version
git clone https://github.com/USERNAME/openclaw-glm-plan-usage.git /tmp/glm-plan-usage
cp -r /tmp/glm-plan-usage/. ~/.openclaw/skills/glm-plan-usage/
chmod +x ~/.openclaw/skills/glm-plan-usage/scripts/query-usage.sh

# Remove backup
rm -rf ~/.openclaw/skills/glm-plan-usage.bak
```

## Next Steps

After successful installation:

1. Review the [main README](../README.md) for usage examples
2. Check the [API documentation](../references/api-endpoints.md) for endpoint details
3. Consider setting up a cron job to periodically check usage:
```bash
# Check usage every hour
crontab -e
# Add: 0 * * * * bash ~/.openclaw/skills/glm-plan-usage/scripts/query-usage.sh >> ~/.glm-usage.log
```

---

# 简体中文

## 前置要求

安装此技能前，请确保您拥有：

1. 已安装并配置 **OpenClaw**
2. **jq** - 命令行 JSON 处理器
3. **curl** - HTTP 客户端（通常预装）
4. **GLM 编码套餐**订阅和有效的 API 密钥

### 安装依赖

#### Linux (Debian/Ubuntu)
```bash
sudo apt-get update
sudo apt-get install -y jq curl
```

#### Linux (CentOS/RHEL/Fedora)
```bash
sudo dnf install -y jq curl
# 或旧系统:
sudo yum install -y jq curl
```

#### macOS
```bash
brew install jq curl
```

#### 验证安装
```bash
jq --version
curl --version
```

## 安装方法

### 方法 1: 从 GitHub 克隆（推荐）

1. 克隆仓库：
```bash
git clone https://github.com/USERNAME/openclaw-glm-plan-usage.git
cd openclaw-glm-plan-usage
```

2. 复制到 OpenClaw 技能目录：
```bash
cp -r . ~/.openclaw/skills/glm-plan-usage/
```

3. 设置脚本可执行权限：
```bash
chmod +x ~/.openclaw/skills/glm-plan-usage/scripts/query-usage.sh
```

### 方法 2: 手动下载

1. 从 GitHub 下载 ZIP 压缩包
2. 解压缩：
```bash
unzip openclaw-glm-plan-usage.zip
cd openclaw-glm-plan-usage
```

3. 复制到 OpenClaw 技能目录：
```bash
cp -r . ~/.openclaw/skills/glm-plan-usage/
chmod +x ~/.openclaw/skills/glm-plan-usage/scripts/query-usage.sh
```

### 方法 3: 直接创建文件

手动创建目录结构：
```bash
mkdir -p ~/.openclaw/skills/glm-plan-usage/{scripts,references,docs}
```

然后从 GitHub 下载单个文件并放置到相应目录。

## 配置

### 步骤 1: 获取 GLM 编码套餐 API 密钥

1. 访问 [GLM 编码套餐](https://open.bigmodel.cn)
2. 注册或登录
3. 导航到 API 密钥部分
4. 生成或复制您的 API 密钥

### 步骤 2: 配置 OpenClaw

编辑 OpenClaw 配置文件：
```bash
nano ~/.openclaw/openclaw.json
```

添加或更新提供商配置：

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

**重要配置说明**：
- `baseUrl` **必须**包含 `api/coding/paas/v4` 或 `open.bigmodel.cn`
- 将 `your-api-key-here` 替换为您的实际 API 密钥
- 提供商名称（示例中的 `zhipu`）可以是您喜欢的任何名称

### 备选配置（多个提供商）

如果您配置了多个提供商，技能会自动检测 GLM 编码套餐提供商：

```json
{
  "models": {
    "providers": {
      "anthropic": {
        "baseUrl": "https://api.anthropic.com/v1",
        "apiKey": "anthropic-key"
      },
      "glm-coding": {
        "baseUrl": "https://open.bigmodel.cn/api/coding/paas/v4",
        "apiKey": "glm-coding-key"
      }
    }
  }
}
```

技能会根据 `baseUrl` 检测到 `glm-coding` 为 GLM 编码套餐提供商。

## 验证安装

### 测试脚本

直接运行脚本以验证安装：
```bash
bash ~/.openclaw/skills/glm-plan-usage/scripts/query-usage.sh
```

预期输出应包含配额、模型使用和工具使用统计信息。

### 验证退出码

脚本返回：
- `0` - 成功
- `1` - 错误（缺少依赖、配置问题、API 错误）

```bash
bash ~/.openclaw/skills/glm-plan-usage/scripts/query-usage.sh
echo $?  # 成功时应输出 0
```

## 故障排除

### 问题: "缺少依赖工具，请安装: jq"

**解决方案**: 使用包管理器安装 jq（见上方前置要求）

### 问题: "未找到配置 GLM 编码套餐的提供商"

**解决方案**: 验证提供商配置包含正确的 `baseUrl`：

```bash
# 检查当前提供商
jq '.models.providers' ~/.openclaw/openclaw.json
```

确保 `baseUrl` 包含 `api/coding/paas/v4`。

### 问题: "认证失败，请检查 API 密钥配置"

**解决方案**: 验证 API 密钥有效且配置正确：

```bash
# 手动测试 API 密钥
curl -H "Authorization: your-api-key" \
     "https://open.bigmodel.cn/api/coding/paas/v4/api/monitor/usage/quota/limit"
```

## 卸载

要移除技能：
```bash
rm -rf ~/.openclaw/skills/glm-plan-usage
```

## 升级

升级到最新版本：

```bash
# 备份当前版本
mv ~/.openclaw/skills/glm-plan-usage ~/.openclaw/skills/glm-plan-usage.bak

# 克隆最新版本
git clone https://github.com/USERNAME/openclaw-glm-plan-usage.git /tmp/glm-plan-usage
cp -r /tmp/glm-plan-usage/. ~/.openclaw/skills/glm-plan-usage/
chmod +x ~/.openclaw/skills/glm-plan-usage/scripts/query-usage.sh

# 删除备份
rm -rf ~/.openclaw/skills/glm-plan-usage.bak
```

## 后续步骤

成功安装后：

1. 查看 [主 README](../README.md) 了解使用示例
2. 查看 [API 文档](../references/api-endpoints.md) 了解端点详情
3. 考虑设置定期检查使用情况的 cron 任务：
```bash
# 每小时检查使用情况
crontab -e
# 添加: 0 * * * * bash ~/.openclaw/skills/glm-plan-usage/scripts/query-usage.sh >> ~/.glm-usage.log
```
