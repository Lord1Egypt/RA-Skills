---
name: base64-toolkit
description: Provides base64 encoding, decoding, and validation utilities for data handling and transformation. Use when you need to encode or decode base64 data, validate base64 strings, or convert between formats.
---

# Base64 Toolkit

Encoding, decoding, and validation utilities for base64 data.

## Usage

```javascript
const b64 = require('./skills/base64-toolkit');

// Encode
const encoded = b64.encode('Hello World');

// Decode
const decoded = b64.decode('SGVsbG8gV29ybGQ=');

// Validate
const valid = b64.isValid('SGVsbG8gV29ybGQ=');

// URL-safe encoding
const urlSafe = b64.encodeURLSafe('data?param=value');
```

## Features

- Standard base64 encoding/decoding
- URL-safe base64 support
- Validation and detection
- Buffer support
- File encoding/decoding
