# MCP Integration Guide

## Overview

The Gomboc MCP server enables agent integration for automated code remediation.

## Running the MCP Server

### Docker (Recommended)

```bash
docker-compose -f scripts/docker-compose.yml up
```

Server runs on `http://localhost:3100`

### Manual Setup

```bash
pip install -r requirements.txt
python -m gomboc.mcp.server --port 3100
```

## Agent Integration

### OpenClaw Agent

Add to your agent config:

```yaml
skills:
  - gomboc-remediation:
      mcp_url: http://localhost:3100
      env:
        GOMBOC_PAT: ${GOMBOC_PAT}
```

### Claude Code

Use the skill commands:

```
@gomboc scan path:./src
@gomboc fix path:./src format:pull_request
@gomboc remediate path:./src commit:true
```

## MCP Endpoints

### Health Check

```bash
curl http://localhost:3100/health
```

### Scan

```bash
curl -X POST http://localhost:3100/scan \
  -H "Content-Type: application/json" \
  -d '{"path": "./src", "policy": "default"}'
```

### Generate Fixes

```bash
curl -X POST http://localhost:3100/fix \
  -H "Content-Type: application/json" \
  -d '{"path": "./src", "scanId": "scan-id"}'
```

## Configuration

Set environment variables:

- `GOMBOC_PAT` — Personal Access Token (required)
- `MCP_PORT` — Server port (default: 3100)
- `LOG_LEVEL` — Logging level (default: info)

## Troubleshooting

### Server won't start

1. Check port 3100 is not in use: `lsof -i :3100`
2. Check GOMBOC_PAT is set: `echo $GOMBOC_PAT`
3. Check Docker is running: `docker ps`

### Agent can't connect

1. Check server is running: `curl http://localhost:3100/health`
2. Check MCP_URL is correct
3. Check firewall allows port 3100

### Scans are slow

- Large codebases take longer to scan
- API rate limits may apply
- Check Gomboc dashboard for usage

## Advanced

### Custom Policies

Use different remediation policies:

```bash
curl -X POST http://localhost:3100/scan \
  -H "Content-Type: application/json" \
  -d '{"path": "./src", "policy": "aws-cis"}'
```

Available policies:
- `default` — General best practices
- `aws-cis` — AWS CIS benchmark
- More coming...

## Support

- **MCP Server Docs:** https://docs.gomboc.ai/mcp
- **GitHub Issues:** https://github.com/Gomboc-AI/gomboc-ai-feedback/discussions
