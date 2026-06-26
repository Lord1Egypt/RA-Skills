---
name: jwt-toolkit
description: Decode, inspect, and validate JWT (JSON Web Token) tokens from the command line. Shows header, payload, algorithm, expiry status, and known claim labels. Use when debugging auth tokens, checking if a JWT is expired, inspecting JWT claims, decoding Bearer tokens, or analyzing token structure. Triggers on "decode JWT", "inspect token", "JWT expired", "parse JWT", "check Bearer token", "token claims".
---

# JWT Toolkit

Zero-dependency JWT decoder and inspector. Decodes any JWT token and shows header, payload claims, algorithm info, expiry status, and signature details.

## Quick Start

```bash
# Decode a JWT token
python3 scripts/jwt_decode.py eyJhbGciOiJIUzI1NiIs...

# Read token from file
python3 scripts/jwt_decode.py --file token.txt

# Read from stdin (pipe from curl, etc.)
echo "eyJ..." | python3 scripts/jwt_decode.py --stdin

# JSON output for scripting
python3 scripts/jwt_decode.py eyJ... --format json

# Also handles "Bearer " prefix automatically
python3 scripts/jwt_decode.py "Bearer eyJhbGciOiJIUzI1NiIs..."
```

## Features

- Decodes header and payload with human-readable claim labels
- Shows algorithm details and security warnings (e.g., `none` algorithm)
- Checks token expiry with remaining time or time-since-expired
- Recognizes 20+ standard and common claims (iss, sub, aud, roles, scope, etc.)
- Strips "Bearer " prefix automatically
- JSON and text output formats
- No external dependencies — pure Python stdlib
