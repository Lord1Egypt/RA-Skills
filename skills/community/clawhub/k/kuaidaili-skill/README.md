# Kuaidaili Skill for OpenClaw

OpenClaw agent skill for [Kuaidaili (快代理)](https://www.kuaidaili.com/) proxy service integration.

## Features

- 🔌 **Get Proxy IPs** - Fetch private/dedicated/tunnel proxies
- 💰 **Check Balance** - Query account balance
- 🧪 **Test Proxies** - Test proxy connectivity
- 📚 **API Reference** - Complete API documentation

## Installation

### Via ClawHub (Recommended)

```bash
clawhub install kuaidaili-skill
```

### Manual Installation

```bash
git clone https://github.com/openclaw-baixing/kuaidaili-skill.git
cd kuaidaili-skill
# Copy to your OpenClaw skills directory
```

## Configuration

Set environment variables:

```bash
export KUAIDAILI_SECRET_ID="your_secret_id"
export KUAIDAILI_SIGNATURE="your_signature"
```

Get your credentials from Kuaidaili Dashboard → API Settings.

## Usage

### Get Proxy IPs

```bash
# Get 10 private proxies (JSON format)
python scripts/get_proxies.py --num 10 --format json

# Get 5 dedicated proxies from Beijing
python scripts/get_proxies.py --type dedicated --area 北京 --num 5
```

### Check Balance

```bash
python scripts/check_balance.py
```

### Test Proxy

```bash
python scripts/test_proxy.py --proxy "http://user:pass@ip:port"
```

## Skill Structure

```
kuaidaili-skill/
├── SKILL.md                    # Skill definition (required)
├── scripts/
│   ├── get_proxies.py         # Fetch proxy IPs
│   ├── check_balance.py       # Query account balance
│   └── test_proxy.py          # Test proxy connectivity
└── references/
    └── api_reference.md       # Kuaidaili API docs
```

## API Reference

See [references/api_reference.md](references/api_reference.md) for complete API documentation.

## License

MIT License

## Links

- [Kuaidaili Official](https://www.kuaidaili.com/)
- [Kuaidaili API Docs](https://www.kuaidaili.com/doc/)
- [ClawHub](https://clawhub.com)
- [OpenClaw](https://github.com/openclaw/openclaw)
