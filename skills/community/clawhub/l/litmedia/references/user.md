# User Module

Check your credit balance and review credit consumption history.

## When to Use

- Before running a generation task, verify you have enough credits.
- After running tasks, review usage history and costs.

## Usage

```bash
python {baseDir}/scripts/user.py <command> [options]
```

## Commands

### `credit` — Check Balance

```bash
python {baseDir}/scripts/user.py credit
```

Output:

```
Credit balance: 1000
```

With `--json`:

```bash
python {baseDir}/scripts/user.py credit --json
```

### `logs` — Usage History

```bash
python {baseDir}/scripts/user.py logs
```

With filters:

```bash
python {baseDir}/scripts/user.py logs \
  --type m2v \
  --start "2025-01-01" \
  --end "2025-12-31" \
  --page 1 \
  --size 20
```

## Options

### Global

| Option | Description |
|--------|-------------|
| `--json` | Output full JSON response (not used by default; only when the user explicitly requests raw JSON output) |
| `-q, --quiet` | Suppress status messages |

### `logs`

| Option | Description |
|--------|-------------|
| `--type TYPE` | Filter by task type (see below) |
| `--start TIME` | UTC start time (`yyyy-MM-dd`) |
| `--end TIME` | UTC end time (`yyyy-MM-dd`)|
| `--page N` | Page number (default: 1) |
| `--size N` | Items per page (default: 20) |

### Task Types

| Value   | Description    |
|---------|----------------|
| `image` | Image creation |
| `video` | Video creation |
