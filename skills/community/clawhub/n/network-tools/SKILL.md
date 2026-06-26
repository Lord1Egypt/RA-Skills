# Network Tools Skill

## Description
Enables AI Agents to leverage various local network tools for efficient and reliable internet access. Supports intelligent tool selection, proxy routing, and comprehensive network diagnostics - all without requiring API keys.

**Core Philosophy**: Maximize network reliability, speed, and accessibility by providing a unified interface to the best available command-line network tools.

## 🔒 Security & Privacy Commitment
- **No External Dependencies**: Uses only locally installed command-line tools
- **No API Keys Required**: All functionality works without external authentication
- **Proxy Isolation**: Optional SOCKS5 proxy support (`127.0.0.1:9050`) for restricted content
- **Input Validation**: Validates URLs and parameters before execution
- **Transparent Operations**: Clear logging of all network activities
- **Local Execution Only**: All functionality operates within the OpenClaw environment

## Available Network Tools

### HTTP Clients (Core)
- **curl**: Versatile HTTP client with extensive protocol support
- **wget**: Reliable file downloader with resume capability  
- **httpie**: User-friendly HTTP client with excellent JSON support

### Download Accelerators
- **aria2**: High-speed download utility with multi-connection support (16 connections by default)
- **axel**: Multi-threaded download accelerator with 10 connections

### Network Diagnostics
- **dig/nslookup**: DNS lookup and record querying
- **ping**: Network connectivity testing
- **traceroute/mtr**: Network path tracing and analysis
- **whois**: Domain registration information lookup

### Media Tools
- **youtube-dl**: Video/audio downloading from 1000+ supported sites
- **ffmpeg**: Media processing and format conversion (when needed)

## Commands Overview

### Basic Web Operations
- `fetch`: Retrieve web content with intelligent tool selection
- `download`: Download files with resume support and format detection

### Network Diagnostics
- `dns`: Query DNS records (A, AAAA, MX, TXT, CNAME, etc.)
- `ping`: Test network connectivity and latency
- `traceroute`: Trace network route to destination
- `whois`: Get domain registration details
- `ipinfo`: Retrieve public IP address from multiple services

### Media Operations
- `media`: Download videos, audio, and other media from supported platforms

### Utility Commands
- `tools`: List all available network tools and their status

## Intelligent Features

### Auto Tool Selection
- **Large Files (>10MB)**: Automatically uses aria2 or axel for faster downloads
- **JSON APIs**: Prefers httpie for clean JSON output when available
- **Fallback Logic**: Gracefully falls back to available tools if preferred tool is missing

### Proxy Support
- **Manual Control**: Use `--proxy` flag to force proxy usage
- **Direct Access**: Default behavior uses direct connections for better performance
- **Universal Proxy**: Works with all supported tools through environment variables or native proxy options

### Enhanced Download Features
- **Resume Support**: Continue interrupted downloads with `--resume` flag
- **Smart Filenames**: Automatically generates safe filenames from URLs
- **Multiple Destinations**: Specify custom output paths with `--output`

### User-Agent Rotation
- **Anti-Detection**: Rotates between realistic browser user agents
- **Tool-Specific**: Uses appropriate user agents for different tools
- **Customizable**: Can be extended with additional user agent strings

## Usage Examples

### Basic Operations
```bash
# Simple fetch with auto tool selection
network-tools fetch https://api.github.com/users/octocat

# Force proxy usage for restricted content
network-tools fetch --proxy https://blocked-api.com/data

# Specify exact tool to use
network-tools fetch --tool=httpie https://jsonplaceholder.typicode.com/posts/1
```

### Advanced Downloads
```bash
# Large file download with resume capability
network-tools download --resume --output=myfile.zip https://example.com/large-file.zip

# Use specific download accelerator
network-tools download --tool=aria2 https://mirror.example.com/ubuntu.iso

# Custom headers for authentication or API keys
network-tools fetch --header="Authorization: Bearer token123" https://api.example.com/protected
```

### Network Diagnostics
```bash
# DNS record lookup
network-tools dns --type MX google.com

# Network connectivity test
network-tools ping --count 10 example.com

# Route tracing
network-tools traceroute cloudflare.com

# Domain information
network-tools whois example.com

# Public IP detection (with proxy support)
network-tools ipinfo --proxy
```

### Media Downloads
```bash
# YouTube video download
network-tools media --format mp4 https://youtube.com/watch?v=example

# Audio-only extraction
network-tools media --format bestaudio https://soundcloud.com/user/track
```

### Tool Discovery
```bash
# Check available tools
network-tools tools
```

## Error Handling & Recovery

### Connection Resilience
- **Multiple Retries**: Built-in retry logic for transient failures
- **Service Fallback**: Multiple IP info services for reliability
- **Tool Fallback**: Automatic switching to alternative tools on failure

### Input Validation
- **URL Validation**: Ensures proper URL format (http/https only)
- **Filename Safety**: Sanitizes output filenames to prevent directory traversal
- **Parameter Validation**: Validates all command-line options

### Graceful Degradation
- **Partial Feature Support**: Works even if only basic tools (curl/wget) are available
- **Clear Error Messages**: Provides actionable error messages for missing dependencies
- **Help Integration**: Built-in help with examples for all commands

## Implementation Guidelines for AI Agents

### When to Use This Skill
- **External Data Retrieval**: Any need to fetch data from internet resources
- **File Downloads**: Retrieving files, documents, datasets, or media
- **API Integration**: Communicating with REST APIs and web services
- **Network Troubleshooting**: Diagnosing connectivity or DNS issues
- **Media Processing**: Downloading content from video/audio platforms

### Best Practices
1. **Leverage Auto-Selection**: Let the skill choose the best tool unless you have specific requirements
2. **Use Proxy Judiciously**: Only enable proxy when accessing known restricted resources
3. **Handle Large Downloads**: Use resume capability for large or unreliable downloads
4. **Validate Results**: Always check download success and file integrity
5. **Respect Rate Limits**: Implement appropriate delays between requests when doing batch operations

### Security Considerations
- **Content Validation**: Verify downloaded content before processing
- **URL Sanitization**: Ensure URLs don't contain malicious parameters
- **File Safety**: Scan downloaded files for malware when possible
- **Privacy Awareness**: Avoid downloading sensitive content through shared proxies

## Compatibility Requirements

### Required Tools (at minimum)
- **curl** OR **wget** (for basic HTTP operations)

### Recommended Tools (for full functionality)
- **httpie** (better JSON handling)
- **aria2c** (fast downloads)
- **dig** (DNS queries)
- **ping/traceroute** (network diagnostics)
- **youtube-dl** (media downloads)

### Proxy Requirements
- **SOCKS5 Proxy**: Local proxy at `127.0.0.1:9050` (optional, for restricted content access)

## Language Support
- English documentation and error messages
- UTF-8 encoding support for international content and domains

## Success Metrics
- **Reliability**: High success rate across different network conditions
- **Performance**: Optimal tool selection for fastest results
- **Compatibility**: Works with minimal tool requirements
- **Security**: Safe handling of network requests and responses
- **Usability**: Intuitive command structure with helpful error messages