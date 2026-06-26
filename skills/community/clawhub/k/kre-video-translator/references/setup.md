# Setup

## API Key

Get the API key from:

- `https://kretrans.com/console#api-management`

Use the copied key as the `KRETRANS_API_KEY` environment variable.
No other environment variables are required.

PowerShell:

```powershell
$env:KRETRANS_API_KEY = "<KRETRANS_API_KEY>"
```

Bash:

```bash
export KRETRANS_API_KEY="<KRETRANS_API_KEY>"
```

## Runtime

- Install `ffmpeg` and make sure it is available in `PATH`.
- Use `python`, `python3`, or `py` to run the script.
- Install the Python package `requests` before the first run, for example: `python -m pip install requests`
- Do not pass `--base-url`; the script uses the built-in KreTrans API endpoint.
- The built-in API endpoint is `https://api.kretrans.com/v1/api`.
- The script uploads extracted audio plus request metadata such as filename and language settings to the API endpoint.
- Built-in defaults are used for task creation timeout, polling timeout, polling interval, and translate language count limit unless explicit CLI flags override them.

## Typical Run

```powershell
python "{baseDir}/scripts/translate.py" "D:/videos/demo.mp4" --source-language auto --target-language zh
```

Single target rule:

- If the user requests one target language, pass `--source-language auto --target-language <code>`.
- Do not add `--translate-languages <same_code>` for a single-target translation.
