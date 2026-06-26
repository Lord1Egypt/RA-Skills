# Nginx Explorer Skill for OpenClaw

A skill that enables OpenClaw to explore nginx-proxied directories containing tools and utilities, read their README.md files, and download/execute them when needed.

## Purpose

When OpenClaw encounters difficult problems that conventional approaches can't solve, this skill allows it to explore a pre-configured nginx server hosting various tools and utilities. Each tool directory contains a README.md explaining its purpose and usage.

## Key Features

1. **Directory Exploration**: Automatically discovers available tools in nginx directory
2. **README Parsing**: Reads and understands tool documentation
3. **Tool Discovery**: Identifies relevant tools for specific problems
4. **Download & Execution**: Downloads tools locally and runs them as needed
5. **Decision Integration**: Helps OpenClaw decide when to use external tools

## Directory Structure

```
nginx-explorer/
├── SKILL.md                    # Main skill documentation
├── scripts/
│   ├── explore-directory.sh    # Explore nginx directory structure
│   ├── download-tool.sh        # Download and prepare tools
│   └── test-mock-nginx.sh      # Test with mock nginx server
├── references/
│   ├── decision-workflow.md    # When to use this skill
│   └── configuration-examples.md # Configuration examples
└── README.md                   # This file
```

## Quick Start

### 1. Configure nginx URL

```bash
export NGINX_URL="http://your-nginx-server:port"
```

### 2. Explore Available Tools

```bash
./scripts/explore-directory.sh
```

### 3. Download and Use a Tool

```bash
./scripts/download-tool.sh "http://your-nginx-server:port" "tool-name"
```

### 4. Test with Mock Server

```bash
./scripts/test-mock-nginx.sh
```

## How It Works

### Discovery Phase
1. Fetches directory listing from nginx
2. Identifies directories with README.md files
3. Reads and parses README content
4. Categorizes tools by functionality

### Decision Phase
1. Assesses problem complexity
2. Determines if conventional approaches are insufficient
3. Identifies relevant tools from discovery
4. Selects the most appropriate tool

### Execution Phase
1. Downloads selected tool and dependencies
2. Configures tool for specific problem
3. Executes tool and monitors results
4. Cleans up temporary files

## Integration with OpenClaw

This skill is designed to be triggered when:
- Conventional problem-solving approaches fail
- Specialized tools are needed
- User explicitly asks for tool exploration
- Complex data processing is required

## Example Use Cases

1. **Data Processing**: CSV/JSON transformation, data cleaning
2. **Media Operations**: Image/video processing, format conversion
3. **System Utilities**: File management, backup, monitoring
4. **Development Tools**: Code generation, testing, documentation
5. **Network Tools**: API testing, network analysis

## Security Considerations

- Tools are downloaded from trusted nginx servers only
- Scripts can be reviewed before execution
- Tools run in appropriate security context
- User confirmation for unknown tools

## Testing

A mock nginx server is included for testing:

```bash
# Start test environment
./scripts/test-mock-nginx.sh

# Test exploration
export NGINX_URL="http://localhost:9999"
./scripts/explore-directory.sh

# Test tool download
./scripts/download-tool.sh "http://localhost:9999" "data-cleaner"
```

## Requirements

- `curl` for HTTP requests
- `grep`, `sed`, `awk` for text processing
- Python 3.x for some tools
- Network access to nginx server

## License

This skill is provided as-is for use with OpenClaw. Modify as needed for your environment.