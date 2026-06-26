# `ghst api`

Direct raw Ghost API requests.

## Usage
```bash
ghst api [options] [endpointPath]
```

## Options
- `-X`, `--method <method>`: HTTP method (default: GET).
- `--body <json>`: Inline JSON request body.
- `--input <path>`: Read JSON request body from file.
- `-f`, `--field <pairs...>`: Request body field in key=value format.
- `--query <pairs...>`: Query params in key=value format.
- `--content-api`: Use Content API instead of Admin API.
- `--paginate`: Auto-paginate list responses.
- `--include-headers`: Include response headers in output.
