---
name: guanyuan-data
description: 观远数据API工具 - 支持多种认证方式、Token自动管理、卡片数据获取和CSV导出
version: 1.0.0
author: Claude Code
tags: [guanyuan, api, data-export, csv, chinese]
requirements:
  - node>=14.0.0
---

# 观远数据 API Skill

## Description
This skill provides a command-line interface for GuanYuan Data (观远数据) API. It supports multiple authentication methods, automatic token management, card data retrieval, and CSV export with metadata generation.

## Usage Instructions

When a user requests GuanYuan data operations:

1. **Choose authentication method**:
   - Method 1: Provide `loginId` and `password` in config for automatic login
   - Method 2: Provide `token` directly in config file
   - Method 3: Use `guanyuan token <token>` command to set token interactively

2. **Get card data**: Use `guanyuan card <cardId>` to retrieve data in JSON format

3. **Export to CSV**: Use `guanyuan csv <cardId> --output file.csv` to export data

### Authentication Methods

#### Method 1: Automatic Login with Credentials
```json
{
  "baseUrl": "https://your-guanyuan-domain.com",
  "domain": "your-domain",
  "loginId": "your-login-id",
  "password": "your-password"
}
```
Then run: `guanyuan login`

#### Method 2: Direct Token in Config
```json
{
  "baseUrl": "https://your-guanyuan-domain.com",
  "domain": "your-domain",
  "token": "your-token-here"
}
```
No login needed, directly use commands.

#### Method 3: Token Command (Interactive)
```json
{
  "baseUrl": "https://your-guanyuan-domain.com",
  "domain": "your-domain"
}
```
Then run: `guanyuan token <your-token>` or `guanyuan token` (interactive)

## Available Resources

### Main Script
- **scripts/guanyuan.js**: Main CLI tool
  - `login()`: Authenticate and save token
  - `getCardData(cardId, options)`: Retrieve card data
  - `convertToCSV(cardData, sampleRows)`: Convert data to CSV format
  - `extractMetadata(cardData)`: Extract field metadata
  - `saveCSVWithMetadata(csv, filename, metadata, cardId)`: Save CSV and metadata files
  - `getValidToken(config)`: Auto-discover and use valid token from multiple sources

### Configuration Files
- **~/.guanyuan/config.json**: API credentials and settings
  - Required: `baseUrl`, `domain`
  - Optional (one of): `loginId` + `password`, `token`, or none (use token command)
- **~/.guanyuan/user.token**: Stored authentication token (auto-managed)

### Export Files
- **<filename>.csv**: CSV data file
- **<filename>_meta.json**: Metadata file with field information

### References
- **references/README.md**: Detailed user documentation in Chinese

## Commands Reference

| Command | Description | Example |
|---------|-------------|---------|
| `init` | Initialize configuration (show setup instructions) | `guanyuan init` |
| `login` | Login with credentials from config | `guanyuan login` |
| `token [token]` | Set token (via parameter or interactive) | `guanyuan token eyJ0eX...` |
| `card <id>` | Get card data (JSON) | `guanyuan card abc123 --limit 50` |
| `csv <id>` | Export to CSV | `guanyuan csv abc123 --output data.csv` |
| `status` | Show config and token status | `guanyuan status` |
| `help` | Show help | `guanyuan help` |

## Options Reference

### Common Options
| Option | Description | Default |
|--------|-------------|---------|
| `--view <GRAPH\|GRID>` | Data view type | GRAPH |
| `--limit <number>` | Number of rows | 100 |
| `--offset <number>` | Data offset | 0 |

### CSV Export Options
| Option | Description | Default |
|--------|-------------|---------|
| `--output <filename>` | Output to file | stdout |
| `--sample <number>` | Sample N rows | all rows |

## Example Prompts

- "使用账号密码登录观远数据并获取卡片abc123的数据"
- "使用token设置观远数据认证"
- "Export card data to CSV with metadata"
- "Get the first 50 rows of card l059d768f28bd404caf8df3e"
- "导出卡片数据到CSV文件，只采样前10行"
- "Check GuanYuan API configuration status"
- "Save card data as query_data.csv with metadata"
- "Set token for GuanYuan API without providing credentials"

## Authentication Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  User wants to access GuanYuan data                         │
└────────────────────┬────────────────────────────────────────┘
                     │
                     v
┌─────────────────────────────────────────────────────────────┐
│  Check ~/.guanyuan/user.token                               │
│  Is there a valid token?                                    │
└────────────────────┬────────────────────────────────────────┘
                     │
            ┌────────┴────────┐
            │                 │
         Yes │                 │ No
            │                 │
            v                 v
┌───────────────────┐  ┌──────────────────────────────────┐
│  Use saved token  │  │  Check config.json              │
└───────────────────┘  │  - Has loginId + password?       │
                      │  - Has token?                   │
                      │  - Neither? → Use token command  │
                      └────────────┬─────────────────────┘
                                   │
                    ┌──────────────┼──────────────┐
                    │              │              │
                Has Creds      Has Token    Neither
                    │              │              │
                    v              v              v
            ┌───────────┐  ┌───────────┐  ┌───────────────┐
            │  Auto     │  │  Use      │  │  Prompt user │
            │  Login    │  │  Config   │  │  to run      │
            │           │  │  Token   │  │  'guanyuan    │
            └───────────┘  └───────────┘  │   token'      │
                                         └───────────────┘
```

## Metadata File Format

When exporting CSV with `--output`, a `_meta.json` file is automatically generated:

```json
{
  "cardId": "card-id",
  "cardType": "CHART",
  "chartType": "PIVOT_TABLE",
  "view": "GRAPH",
  "exportTime": "2026-03-25T07:52:00.924Z",
  "totalRows": 10,
  "dataLimit": 10,
  "hasMoreData": false,
  "fields": [
    {
      "name": "字段显示名称",
      "originalName": "字段原始名称",
      "type": "STRING/TIMESTAMP/DOUBLE",
      "metaType": "DIM/METRIC",
      "fieldType": "dimension/metric",
      "fieldId": "field-id"
    }
  ]
}
```

## Output Format

### JSON Output
- Full API response with chart data
- Includes dimensions, metrics, and formatting info
- Suitable for debugging and data inspection

### CSV Output
- Tabular format with headers
- Dimensions first, then metrics
- Proper CSV escaping for special characters
- Metadata file with field types and descriptions

## Token Management

### Token Sources (Priority Order)
1. **`~/.guanyuan/user.token`** - Saved token (highest priority)
2. **`config.json`** - Token field in config
3. **Auto-login** - Using `loginId` + `password` from config

### Token Behavior
- **With expireAt**: Automatically validated against expiration time
- **Without expireAt**: Used indefinitely (user-manually set tokens)
- **Expired/Invalid**: Triggers auto-refresh (if credentials available) or prompts user

### Manual Token Setting
```bash
# Via parameter
guanyuan token eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...

# Interactive mode
guanyuan token
# Then paste your token when prompted
```

## Notes

- **Flexible Authentication**: Three authentication methods for different use cases
- **Token Management**: Tokens are automatically discovered from multiple sources
- **Auto-Login**: Credentials-based auth with automatic token refresh
- **Password Handling**: Passwords are automatically Base64 encoded before API call
- **URL Support**: baseUrl can include protocol prefix (http:// or https://)
- **CSV Escaping**: Special characters (commas, quotes, newlines) are properly escaped
- **File Safety**: Existing files are overwritten without warning
- **Data Limits**: Use `--limit` to control API response size
- **Sampling**: Use `--sample` to export only N rows without fetching all data
- **No Credentials Required**: Can work with just baseUrl + domain + token command

## API References

- [User Login API](https://api.guandata.com/apidoc/docs-site/345092/710/api-3470502)
- [Get Card Data API](https://api.guandata.com/apidoc/docs-site/345092/710/api-3471043)
