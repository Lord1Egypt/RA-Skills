---
name: http-request-builder
description: Build and test HTTP requests with CLI interface: headers, auth, body, cookies, with history and templates.
version: 1.0.0
author: skill-factory
metadata:
  openclaw:
    requires:
      bins:
        - python3
      python:
        - requests
---

# HTTP Request Builder

## What This Does

A CLI tool to build, test, and save HTTP requests. Send requests with custom headers, authentication, body, and cookies. Save requests as templates for reuse and maintain a history of your HTTP calls.

Key features:
- **Send HTTP requests** with GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS methods
- **Set custom headers** with key-value pairs
- **Add authentication** (Basic Auth, Bearer tokens)
- **Include request body** (JSON, form data, raw text)
- **Manage cookies** for requests
- **Save requests as templates** (JSON files) for reuse
- **Load and execute** saved templates
- **Interactive mode** for building requests step-by-step
- **Command-line mode** for scripting and automation
- **Request history** tracks your recent HTTP calls

## When To Use

- You need to test REST API endpoints quickly from the terminal
- You want to save and reuse complex API requests
- You prefer a CLI tool over GUI applications like Postman
- You need to automate API testing in scripts
- You want to share API request configurations with team members
- You're debugging API issues and need to replay requests

## Usage

Basic commands:

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

# Interactive mode
python3 scripts/main.py interactive

# View request history
python3 scripts/main.py history

# Clear history
python3 scripts/main.py history --clear
```

## Examples

### Example 1: Simple GET request

```bash
python3 scripts/main.py get https://jsonplaceholder.typicode.com/posts/1
```

Output:
```
Response Status: 200 OK
Response Headers:
  content-type: application/json; charset=utf-8
  ...

Response Body:
{
  "userId": 1,
  "id": 1,
  "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
  "body": "quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto"
}
```

### Example 2: POST request with JSON body and headers

```bash
python3 scripts/main.py post https://jsonplaceholder.typicode.com/posts \
  --header "Content-Type: application/json" \
  --header "X-API-Key: my-secret-key" \
  --body '{
    "title": "foo",
    "body": "bar",
    "userId": 1
  }'
```

### Example 3: Save and reuse request template

```bash
# Save template
python3 scripts/main.py post https://api.example.com/users \
  --header "Content-Type: application/json" \
  --header "Authorization: Bearer token123" \
  --body '{"name": "New User"}' \
  --save-template create-user

# Use template later
python3 scripts/main.py template create-user

# List all templates
python3 scripts/main.py templates
```

### Example 4: Interactive mode

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

## Requirements

- Python 3.x
- `requests` library (installed automatically or via pip)

Install missing dependencies:
```bash
pip3 install requests
```

## Limitations

- This is a CLI tool, not a GUI application
- History and templates stored in simple JSON files in `~/.http-request-builder/`
- Limited authentication support (Basic, Bearer tokens only)
- No OAuth, API key in header, or complex authentication flows
- No cookie persistence across sessions (cookies only for single request)
- No proxy configuration support
- No SSL certificate verification controls
- No support for websockets or streaming responses
- No advanced features like response validation or testing assertions
- Request history limited to 100 entries by default
- Templates are simple JSON files without encryption
- No built-in support for environment variables in templates
- Performance limited by Python requests library
- Large response bodies may be truncated for display
- No support for multipart form data file uploads
- No built-in rate limiting or retry logic
- No support for HTTP/2 or HTTP/3 protocols

## Directory Structure

The tool stores data in `~/.http-request-builder/`:
- `templates/` - Saved request templates (JSON files)
- `history.json` - Request history log
- `config.json` - Configuration (if any)

## Error Handling

- Invalid URLs return helpful error messages
- Network timeouts after 30 seconds
- JSON parsing errors show the problematic content
- Missing templates indicate which template wasn't found
- Authentication failures suggest correct format

## Contributing

This is a skill built by the Skill Factory. Issues and improvements should be reported through the OpenClaw project.