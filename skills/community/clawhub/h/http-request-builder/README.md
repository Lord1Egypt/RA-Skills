# HTTP Request Builder

A CLI tool to build, test, and save HTTP requests from the terminal. Send requests with custom headers, authentication, body, and cookies. Save requests as templates for reuse.

## Installation

Install via ClawHub:

```bash
clawhub install http-request-builder
```

## Usage

### Basic Commands

```bash
# Send a GET request
python3 scripts/main.py get https://api.example.com/data

# Send a POST request with JSON body
python3 scripts/main.py post https://api.example.com/api \
  --header "Content-Type: application/json" \
  --body '{"name": "test", "value": 123}'

# Send with Basic authentication
python3 scripts/main.py get https://api.example.com/secure \
  --auth basic --username admin --password secret

# Send with Bearer token
python3 scripts/main.py get https://api.example.com/secure \
  --auth bearer --token "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"

# Save request as template
python3 scripts/main.py post https://api.example.com/api \
  --header "Content-Type: application/json" \
  --body '{"name": "test"}' \
  --save-template my-request

# Load and execute template
python3 scripts/main.py template my-request

# View request history
python3 scripts/main.py history
```

### Interactive Mode

```bash
python3 scripts/main.py interactive
```

Interactive mode guides you through:
1. HTTP method selection
2. URL input
3. Headers configuration
4. Authentication setup
5. Request body input
6. Send request and view results

## Features

- Send HTTP requests with GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS methods
- Set custom headers with key-value pairs
- Add authentication (Basic Auth, Bearer tokens)
- Include request body (JSON, form data, raw text)
- Save requests as templates (JSON files) for reuse
- Load and execute saved templates
- Interactive mode for building requests step-by-step
- Request history tracks your recent HTTP calls

## Requirements

- Python 3.x
- `requests` library (installed automatically or via pip)

Install missing dependencies:
```bash
pip3 install requests
```

## Limitations

- No OAuth, API key in header, or complex authentication flows
- No cookie persistence across sessions
- No proxy configuration support
- No SSL certificate verification controls
- No support for websockets or streaming responses
- Request history limited to 100 entries by default
- Templates are simple JSON files without encryption

## Directory Structure

The tool stores data in `~/.http-request-builder/`:
- `templates/` - Saved request templates (JSON files)
- `history.json` - Request history log
- `config.json` - Configuration (if any)

## License

MIT