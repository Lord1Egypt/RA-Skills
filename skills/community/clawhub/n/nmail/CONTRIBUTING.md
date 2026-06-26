# Contributing to nmail

Thanks for your interest in nmail! 🎉

## How to contribute

1. **Fork** the repository
2. **Create a branch** (`feat/my-feature` or `fix/my-bug`)
3. **Make changes** and add tests if applicable
4. **Submit a PR** against `main`

## Development

```bash
# Build
go build -o nmail .

# Test
go test ./...

# Run locally
./nmail --help
```

## Guidelines

- Keep JSON output stable (agents depend on it)
- Korean encoding (EUC-KR) must be handled for all providers
- Use conventional commits: `feat:`, `fix:`, `chore:`, `docs:`
- No secrets or credentials in code or tests

## Reporting Issues

Please include:
- `nmail version` output
- Email provider (Naver, Daum, etc.)
- Error message (JSON output)
- Steps to reproduce
