# MiniMax Skill Setup

This skill reads the API token from the `MINIMAX_API_KEY` environment variable.
Do not hardcode the token into the skill files.

## 1) Linux / macOS (bash, zsh)

Temporary for current shell:

```bash
export MINIMAX_API_KEY="your_minimax_api_key"
```

Persist in `~/.bashrc`:

```bash
export MINIMAX_API_KEY="your_minimax_api_key"
```

Persist in `~/.zshrc`:

```bash
export MINIMAX_API_KEY="your_minimax_api_key"
```

Important: place the `export` before any early `return` in shell startup files.

## 2) fish shell

Temporary:

```fish
set -x MINIMAX_API_KEY your_minimax_api_key
```

Persist:

```fish
set -Ux MINIMAX_API_KEY your_minimax_api_key
```

## 3) Windows PowerShell

Current session:

```powershell
$env:MINIMAX_API_KEY = "your_minimax_api_key"
```

Persist for user:

```powershell
[Environment]::SetEnvironmentVariable("MINIMAX_API_KEY", "your_minimax_api_key", "User")
```

Reopen PowerShell after persisting.

## 4) Windows CMD

Current session:

```cmd
set MINIMAX_API_KEY=your_minimax_api_key
```

Persist for future sessions:

```cmd
setx MINIMAX_API_KEY "your_minimax_api_key"
```

Reopen the terminal after `setx`.

## 5) Docker

Pass through an environment variable:

```bash
docker run -e MINIMAX_API_KEY="$MINIMAX_API_KEY" your-image
```

Or in `docker-compose.yml`:

```yaml
environment:
  MINIMAX_API_KEY: ${MINIMAX_API_KEY}
```

## 6) GitHub Actions / CI

Store the token as a secret, then expose it at runtime:

```yaml
env:
  MINIMAX_API_KEY: ${{ secrets.MINIMAX_API_KEY }}
```

## Quick verification

```bash
python scripts/minimax.py --help
python scripts/minimax.py image --prompt "a cute orange cat" --output /tmp/minimax-images
```

If the token is missing, the scripts exit with:

```text
MINIMAX_API_KEY is required
```
