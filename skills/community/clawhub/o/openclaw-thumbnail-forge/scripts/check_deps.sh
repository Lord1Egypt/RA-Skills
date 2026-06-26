#!/usr/bin/env bash
# Verify dependencies for openclaw-thumbnail-forge.
# Exits 0 if all are available, 1 if any are missing.

set -u

missing=0

check_bin() {
  local bin="$1"
  if command -v "$bin" >/dev/null 2>&1; then
    local version
    version="$("$bin" --version 2>&1 | head -n 1 || echo 'version unknown')"
    printf "  ok   %-9s %s\n" "$bin" "$version"
  else
    printf "  miss %-9s not found in PATH\n" "$bin"
    missing=1
  fi
}

for bin in ffmpeg ffprobe python3; do
  check_bin "$bin"
done

# Check Pillow availability
if python3 -c "import PIL; print('PIL', PIL.__version__)" 2>/dev/null; then
  printf "  ok   %-9s %s\n" "Pillow" "$(python3 -c 'import PIL; print(PIL.__version__)')"
else
  printf "  miss %-9s not importable (run: pip install Pillow)\n" "Pillow"
  missing=1
fi

if [ "$missing" -eq 1 ]; then
  echo
  echo "One or more dependencies are missing." >&2
  echo "Install missing system binaries via your package manager (apt, brew, choco)." >&2
  echo "Install Pillow via: pip install Pillow" >&2
  exit 1
fi

echo
echo "All dependencies satisfied."
exit 0
