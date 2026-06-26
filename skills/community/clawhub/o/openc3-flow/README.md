# openc3-flow - Open-C3 Flow Management Skill

🚀 An OpenClaw skill to manage and list all CI/CD flows from Open-C3 platform.

## Features

- ✅ List all CI/CD flows in the system
- ✅ Display flows in a formatted table with complete information
- ✅ Show service tree grouping and statistics
- ✅ Support for any Open-C3 deployment

## Installation

```bash
# Install via ClawHub CLI
clawhub install openc3-flow
```

## Configuration

1. Copy the example configuration file:
   ```bash
   cp config.env.example config.env
   ```

2. Edit `config.env` and fill in your Open-C3 credentials:
   ```bash
   OPEN_C3_URL="http://your-open-c3-server/"
   APP_NAME="your_app_name"
   APP_KEY="your_app_key"
   ```

3. **Important**: Never commit `config.env` to version control!

## Usage

Once installed and configured, you can use natural language commands:

- "List all Open-C3 flows"
- "Show me all CI/CD pipelines"
- "Get all flows from the system"
- "What flows are configured in Open-C3?"

### Example Output

```
✅ **系统共有 36 条流水线：**

| ID | 名称 | 服务树 ID | 服务树名称 | 源码地址 |
|----|------|----------|-----------|---------|
| 1 | 普通主机发布 | 21 | demo.cicd | https://... |
| 2 | 普通 k8s 发布 | 21 | demo.cicd | https://... |
...

**统计信息：**
- **dev.package** (ID:23): 11 条
- **demo.cicd** (ID:21): 7 条
- **demo** (ID:20): 7 条
```

## Requirements

- `curl` - For API requests
- `jq` - For JSON parsing and formatting

## API Endpoint

This skill uses the Open-C3 API endpoint:
- `GET /api/ci/group/ci/dump` - Returns all flows across all service trees

## Security Notes

- ⚠️ Keep your `APP_KEY` secret and never share it
- ⚠️ The `config.env` file is gitignored by default
- ⚠️ Only use this skill with trusted Open-C3 instances

## License

GPL-2.0

## Support

For issues or questions, please open an issue on the skill repository.
