# Viewer Management Commands

Viewer information query and tag management commands for managing viewers.

## Commands

### View Viewer Commands

| Command | Description |
| ------- | ----------- |
| `viewer get` | Get single viewer details |
| `viewer list` | List viewers with pagination and filters |
| `viewer tag list` | List all viewer tags |
| `viewer tag add` | Add tags to viewers |
| `viewer tag remove` | Remove tags from viewers |

### viewer get

Get single viewer details by viewer unique ID.

```bash
<CLI> viewer get -i <viewerID>
<CLI> viewer get -i "2_v378gn997yovtl3p8h77db9e224t6hg9"
```

**Options:**
- `-i, --viewer-id <id>` - Viewer unique ID (required)
- `-o, --output <format>` - Output format: `table` (default) or `json`

**Examples:**
```bash
# Get viewer details
<CLI> viewer get -i "2_v378gn997yovtl3p8h77db9e224t6hg9"

# JSON output
<CLI> viewer get -i "2_v378gn997yovtl3p8h77db9e224t6hg9" -o json
```

### viewer list

List viewers with pagination and filters.

```bash
<CLI> viewer list
<CLI> viewer list --page 1 --size 20
<CLI> viewer list --source IMPORT
<CLI> viewer list --mobile "13800138000"
<CLI> viewer list --email "user@example.com"
<CLI> viewer list --area "Beijing"
```

**Options:**
- `--source <type>` - Filter by source: `IMPORT`, `WX`, `MOBILE`
- `--mobile <number>` - Filter by mobile number
- `--email <email>` - Filter by email
- `--area <area>` - Filter by area
- `--page <number>` - Page number (default: 1)
- `--size <number>` - Page size (default: 10, max: 1000)
- `-o, --output <format>` - Output format: `table` (default) or `json`

### viewer tag list

List all viewer tags with optional keyword filter and pagination.

```bash
<CLI> viewer tag list
<CLI> viewer tag list --keyword "VIP"
<CLI> viewer tag list --page 1 --size 20
```

**Options:**
- `-k, --keyword <keyword>` - Keyword to search tag name
- `--page <number>` - Page number (default: 1)
- `--size <number>` - Page size (default: 10, max: 1000)
- `-o, --output <format>` - Output format: `table` (default) or `json`

**Examples:**
```bash
# List all tags
<CLI> viewer tag list

# Search tags by keyword
<CLI> viewer tag list -k "VIP"

# Pagination
<CLI> viewer tag list --page 1 --size 20

# JSON output
<CLI> viewer tag list -o json
```

### viewer tag add

Add tags to viewers (supports batch operation)

```bash
<CLI> viewer tag add -V <viewer-ids> -l <label-ids>
<CLI> viewer tag add -V "viewer1" -l 1
<CLI> viewer tag add -V "viewer1,viewer2,viewer3" -l 1,2,3
```

**Options:**
- `-V, --viewer-ids <ids>` - Comma-separated viewer IDs (required)
- `-l, --label-ids <ids>` - Comma-separated label IDs (required)
- `-o, --output <format>` - Output format: `table` (default) or `json`

**Examples:**
```bash
# Add single tag to single viewer
<CLI> viewer tag add -V "viewer1" -l 1

# Add multiple tags to single viewer
<CLI> viewer tag add -V "viewer1" -l 1,2,3

# Batch: add tags to multiple viewers
<CLI> viewer tag add -V "viewer1,viewer2,viewer3" -l 1,2

# JSON output
<CLI> viewer tag add -V "viewer1" -l 1 -o json
```

### viewer tag remove

Remove tags from viewers (supports batch operation)

```bash
<CLI> viewer tag remove -V <viewer-ids> -l <label-ids>
<CLI> viewer tag remove -V "viewer1" -l 1
<CLI> viewer tag remove -V "viewer1,viewer2" -l 1,2,3
```

**Options:**
- `-V, --viewer-ids <ids>` - Comma-separated viewer IDs (required)
- `-l, --label-ids <ids>` - Comma-separated label IDs (required)
- `-o, --output <format>` - Output format: `table` (default) or `json`

**Examples:**
```bash
# Remove single tag from single viewer
<CLI> viewer tag remove -V "viewer1" -l 1

# Remove multiple tags from single viewer
<CLI> viewer tag remove -V "viewer1" -l 1,2,3

# Batch: remove tags from multiple viewers
<CLI> viewer tag remove -V "viewer1,viewer2" -l 1,2

# JSON output
<CLI> viewer tag remove -V "viewer1" -l 1 -o json
```

## Output Formats

All viewer commands support the following output formats:

| Format | Description |
| ------ | ----------- |
| `table` | Default. Formatted table output for human reading |
| `json` | JSON format for programmatic use |

Specify with `-o table` or `-o json` option.

## Global Options

All viewer commands support these global options

| Option | Description |
| ------ | ----------- |
| `--appId <id>` | PolyV application ID |
| `--appSecret <secret>` | PolyV application secret |
| `--userId <id>` | PolyV user ID (optional) |
| `-a, --account <name>` | Use specified account |
| `--verbose` | Show verbose output |
| `--debug` | Enable debug mode |
| `--timeout <ms>` | API timeout (default: 30000) |

## Authentication

Before using viewer commands, ensure you authentication is configured:

1. **Session account**: `<CLI> use <account-name>`
2. **Environment variables**: `POLYV_APP_ID`, `POLYV_APP_SECRET`
3. **Default account**: `<CLI> account set-default <name>`
4. **Command-line options**: `--appId`, `--appSecret`, `--userId`

See [Authentication Guide](./authentication.md) for more details.

## Related Documentation

- [Authentication Guide](./authentication.md)
- [Channel Management](./channel-management.md)
- [API Documentation](https://help.polyv.net/#/live/api/)
