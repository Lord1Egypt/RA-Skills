# Installation guidance

Do not change the user's Python environment or install a large dependency
without permission. Prefer a dedicated virtual environment for the editing
task.

MovieStar needs Python 3.10 or newer, `ffmpeg`, and `ffprobe`. If FFmpeg is
missing, identify the platform package-manager command and ask the user before
installing it.

Install the current MovieStar release from PyPI:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install moviestar
```

Confirm that `moviestar --version` reports v0.7.0 or newer before using v0.7
commands.

Run `moviestar doctor` after installation. Treat blocked features in its JSON
response as setup failures to resolve or report before editing. Whisper models
download on first transcription; use `moviestar models pull MODEL` only after
the user approves the download, or use an already cached model. `--no-download`
guarantees a hermetic load.
