#!/usr/bin/env bash
set -euo pipefail

PYTHON_BIN="${PYTHON_BIN:-python3}"
USER_BIN="$HOME/.local/bin"

mkdir -p "$USER_BIN"

if ! "$PYTHON_BIN" -m pip --version >/dev/null 2>&1; then
  TMPDIR_RUN="$(mktemp -d)"
  cleanup() { rm -rf "$TMPDIR_RUN"; }
  trap cleanup EXIT
  curl -fsSL https://bootstrap.pypa.io/get-pip.py -o "$TMPDIR_RUN/get-pip.py"
  "$PYTHON_BIN" "$TMPDIR_RUN/get-pip.py" --user --break-system-packages
fi

"$PYTHON_BIN" -m pip install --user --break-system-packages \
  imageio-ffmpeg \
  more-itertools \
  numba \
  numpy \
  tiktoken \
  tqdm \
  triton \
  regex \
  filelock \
  sympy \
  networkx \
  fsspec

"$PYTHON_BIN" -m pip install --user --break-system-packages \
  --index-url https://download.pytorch.org/whl/cpu \
  torch

"$PYTHON_BIN" -m pip install --user --break-system-packages --no-deps openai-whisper

cat > "$USER_BIN/whisper" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
exec python3 -m whisper "$@"
EOF
chmod +x "$USER_BIN/whisper"

FFMPEG_BIN="$($PYTHON_BIN - <<'PY'
import imageio_ffmpeg
print(imageio_ffmpeg.get_ffmpeg_exe())
PY
)"
ln -sf "$FFMPEG_BIN" "$USER_BIN/ffmpeg"

printf 'Installed Whisper CLI: %s\n' "$USER_BIN/whisper"
printf 'Installed ffmpeg shim: %s -> %s\n' "$USER_BIN/ffmpeg" "$FFMPEG_BIN"
"$USER_BIN/whisper" --help >/dev/null
"$USER_BIN/ffmpeg" -hide_banner -version >/dev/null
printf 'Local Whisper install OK\n'
