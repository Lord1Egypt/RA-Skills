---
name: nginx-explorer
description: "Explore nginx-proxied directories to discover tools and utilities. Use when: user asks to explore available tools, find utilities for specific tasks, or when OpenClaw needs to discover executable projects in a directory structure served by nginx. Configuration requires nginx URL. Each directory contains README.md explaining contents and execution instructions."
metadata:
  openclaw:
    emoji: "🔍"
    requires:
      bins: ["curl"]
    primaryEnv: "NGINX_URL"
    env:
      NGINX_URL:
        description: "The base URL of the nginx server (e.g., http://192.168.1.100:8080 or http://internal-tools.local)"
        required: true
        type: "string"
        example: "http://192.168.1.100:8080"
      NGINX_SKIP_SSL_VERIFY:
        description: "Skip SSL certificate verification (useful for internal networks with self-signed certificates)"
        required: false
        type: "boolean"
        default: true
---

# Nginx Explorer Skill

Explore directories served by nginx to discover tools, utilities, and executable projects. Each main directory contains a README.md file that explains what's available and how to use it.

## Configuration

This skill requires one environment variable:
- `NGINX_URL`: The base URL of the nginx server (e.g., `http://192.168.1.100:8080` or `http://internal-tools.local`)

Optional environment variable:
- `NGINX_SKIP_SSL_VERIFY`: Set to `true` to skip SSL certificate verification (useful for internal networks with self-signed certificates). Default is `true`.

Configure in `~/.openclaw/openclaw.json`:
```json5
{
  skills: {
    entries: {
      "nginx-explorer": {
        enabled: true,
        env: {
          NGINX_URL: "http://your-nginx-server:port",
          NGINX_SKIP_SSL_VERIFY: "true"  // Optional: skip SSL verification for internal networks
        }
      }
    }
  }
}
```

## When to Use

✅ **USE this skill when:**

- User asks "what tools are available?" or "explore the nginx directory"
- OpenClaw needs to find utilities for specific tasks  
- User wants to discover executable projects in the nginx-proxied structure
- When conventional approaches fail and exploring available tools might help

❌ **DON'T use this skill when:**

- Direct file access is available (use normal file operations instead)
- The nginx URL is not configured
- Simple file downloads are needed (use curl/wget directly)

## Configuration

The skill requires one configuration item:

- `NGINX_URL`: The base URL of the nginx server (e.g., `http://192.168.1.100:8080` or `http://internal-tools.local`)

## How It Works

1. **Directory Discovery**: Fetches the nginx directory listing (HTML)
2. **README Reading**: For each directory, reads the README.md file to understand contents
3. **Tool Identification**: Identifies executable projects and their usage instructions
4. **Download & Execution**: Can download tools locally and run them as needed

## Basic Usage

### 1. Configure the nginx URL

First, set the nginx URL in your environment or workspace:

```bash
# Set as environment variable
export NGINX_URL="http://192.168.1.100:8080"

# Or store in workspace config
echo '{"nginx_url": "http://192.168.1.100:8080"}' > /home/node/.openclaw/workspace/nginx-config.json
```

### 2. Explore the Directory Structure

```bash
# Fetch directory listing
curl -s "$NGINX_URL/" | grep -o 'href="[^"]*"' | grep -v '^href="\.' | cut -d'"' -f2
```

### 3. Read README Files

For each discovered directory:

```bash
# Check if README.md exists
curl -s -I "$NGINX_URL/tool-directory/README.md" | head -1 | grep "200"

# Read the README
curl -s "$NGINX_URL/tool-directory/README.md"
```

### 4. Download and Execute Tools

When a useful tool is found:

```bash
# Download the tool (assuming it's a script or archive)
curl -o /tmp/tool.sh "$NGINX_URL/tool-directory/tool.sh"

# Make executable if needed
chmod +x /tmp/tool.sh

# Run according to README instructions
/tmp/tool.sh --help
```

## Workflow Examples

### Example 1: Discovering Available Tools

```bash
#!/bin/bash
NGINX_URL="http://192.168.1.100:8080"

# Get all directories
echo "Exploring $NGINX_URL..."
DIRS=$(curl -s "$NGINX_URL/" | grep -o 'href="[^"]*/"' | grep -v '^href="\.' | cut -d'"' -f2 | sed 's|/$||')

for dir in $DIRS; do
    echo "=== $dir ==="
    # Try to read README
    README=$(curl -s "$NGINX_URL/$dir/README.md" 2>/dev/null)
    if [ -n "$README" ]; then
        echo "$README" | head -5
    else
        echo "No README found"
    fi
    echo
done
```

### Example 2: Finding a Specific Type of Tool

```bash
#!/bin/bash
NGINX_URL="http://192.168.1.100:8080"

# Search for tools related to "data processing"
echo "Searching for data processing tools..."
DIRS=$(curl -s "$NGINX_URL/" | grep -o 'href="[^"]*/"' | grep -v '^href="\.' | cut -d'"' -f2 | sed 's|/$||')

for dir in $DIRS; do
    README=$(curl -s "$NGINX_URL/$dir/README.md" 2>/dev/null)
    if echo "$README" | grep -qi "data.*process\|csv\|json\|transform"; then
        echo "Found in $dir:"
        echo "$README" | grep -i "data.*process\|csv\|json\|transform" | head -3
        echo "---"
    fi
done
```

### Example 3: Downloading and Running a Tool

```bash
#!/bin/bash
NGINX_URL="http://192.168.1.100:8080"
TOOL_DIR="data-processor"

# Read instructions
README=$(curl -s "$NGINX_URL/$TOOL_DIR/README.md")
echo "Tool instructions:"
echo "$README"

# Download main script
curl -o /tmp/processor.py "$NGINX_URL/$TOOL_DIR/processor.py"

# Download dependencies if mentioned
if echo "$README" | grep -q "requirements.txt"; then
    curl -o /tmp/requirements.txt "$NGINX_URL/$TOOL_DIR/requirements.txt"
    pip install -r /tmp/requirements.txt
fi

# Run the tool
python /tmp/processor.py --help
```

## Integration with OpenClaw Decision Making

This skill is designed to be used when OpenClaw encounters difficult problems. The workflow:

1. **Problem Assessment**: Determine if conventional approaches are failing
2. **Tool Exploration**: Use this skill to explore available utilities
3. **Tool Selection**: Identify tools that might help with the specific problem
4. **Tool Application**: Download and use the selected tool

### Decision Flow

```
User Request → Can OpenClaw solve it directly? → Yes → Solve directly
                               ↓
                               No
                               ↓
                    Explore nginx directory
                               ↓
                    Read README files
                               ↓
              Find relevant tools/utilities
                               ↓
            Download and apply tool to problem
```

## Error Handling

- **Connection Issues**: Check if nginx URL is correct and accessible
- **Missing README**: Some directories may not have README.md files
- **Broken Links**: Verify tool files exist before downloading
- **Execution Failures**: Check dependencies and permissions

## Best Practices

1. **Cache Discoveries**: Store directory listings to avoid repeated requests
2. **Validate Tools**: Test tools in isolated environment before use
3. **Clean Up**: Remove downloaded files after use
4. **Document Findings**: Update workspace notes with useful tools discovered

## Example README Structure

Tools in the nginx directory should follow this README format:

```markdown
# Tool Name

## Purpose
Brief description of what this tool does.

## Usage
```bash
./tool.sh [options]
```

## Dependencies
- Python 3.8+
- Required packages: requests, pandas

## Examples
```bash
# Basic usage
./tool.sh --input data.csv --output results.json

# Advanced usage
./tool.sh --config config.yaml --verbose
```

## Notes
Any additional information or warnings.
```

## Security Considerations

- Only download from trusted nginx servers
- Validate scripts before execution
- Run in sandboxed environment when possible
- Check for malicious code in downloaded files