# pass-secrets — Password Store Skill

Store and retrieve secrets using `pass` (password-store) with GPG encryption.

## Setup

```bash
# Already initialized:
# - GPG key: 4FA146198B574BE88C2FCE607BCA61011E422C14
# - Pass store: ~/.password-store/
```

## Usage

### Store a secret
```bash
pass insert -m path/to/secret
# Type value, press Ctrl+D
```

Or pipe directly:
```bash
echo "value" | gpg --encrypt --recipient 4FA146198B574BE88C2FCE607BCA61011E422C14 > ~/.password-store/path.gpg
```

### Retrieve a secret
```bash
pass show path/to/secret
```

### List all secrets
```bash
pass ls
```

### Remove a secret
```bash
pass rm path/to/secret
```

## Current Secrets

| Path | Description |
|------|-------------|
| `api/kimi` | Kimi API key |
| `api/kimi-plugin` | Kimi plugin API key |
| `api/gemini` | Gemini API key |
| `api/openrouter` | OpenRouter API key |

## Security

- Secrets are GPG-encrypted at rest
- Only the holder of the private key can decrypt
- Back up `~/.password-store/` and `~/.gnupg/` separately
