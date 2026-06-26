# Network Tools Skill

A comprehensive network toolkit for AI Agents that provides intelligent access to various command-line network utilities without requiring API keys.

## Features

- **Intelligent Tool Selection**: Automatically chooses the best available tool based on content type and size
- **Multiple HTTP Clients**: curl, wget, httpie support with user-agent rotation
- **Download Acceleration**: aria2 and axel support for faster downloads
- **Network Diagnostics**: DNS lookup, ping, traceroute, whois, and IP information
- **Media Downloads**: youtube-dl integration for video/audio downloading
- **Proxy Support**: Optional SOCKS5 proxy routing (`127.0.0.1:9050`)
- **Resume Capability**: Continue interrupted downloads
- **Input Validation**: Safe URL and parameter handling

## Commands

- `fetch` - Retrieve web content with auto tool selection
- `download` - Download files with resume support  
- `dns` - Query DNS records (A, AAAA, MX, TXT, etc.)
- `ping` - Test network connectivity
- `traceroute` - Trace network route to destination
- `whois` - Get domain registration information
- `ipinfo` - Retrieve public IP address
- `media` - Download media from supported platforms
- `tools` - List available network tools

## Requirements

### Minimum (basic functionality)
- curl OR wget

### Recommended (full functionality)
- curl, wget, httpie
- aria2c (for fast downloads)
- dig, nslookup (for DNS queries)
- ping, traceroute, mtr (for network diagnostics)
- youtube-dl (for media downloads)

## Usage Examples

```bash
# Basic fetch
network-tools fetch https://api.example.com/data

# Download with resume
network-tools download --resume --output=file.zip https://example.com/large-file.zip

# DNS lookup
network-tools dns --type MX google.com

# Get public IP
network-tools ipinfo

# Media download
network-tools media --format mp4 https://youtube.com/watch?v=example
```

## Security

- No external API keys required
- All operations use locally installed tools
- Input validation prevents malicious URLs
- Optional proxy isolation for restricted content
- Transparent logging of all network activities

## License

MIT License - Free to use, modify, and distribute.