#!/bin/bash
set -e

SKILL_DIR="$(dirname "$(realpath "$0")")"
VENV_DIR="$SKILL_DIR/.venv"

# ==============================================================
# Bootstrap Python 3.10 WITHOUT sudo.
#
# Strategy (in order):
#   1. Use system python3.10 if it already exists.
#   2. Use a previously uv-managed python3.10.
#   3. Install uv (single-binary, user-local: ~/.local/bin) and
#      let it install a portable Python 3.10 to
#      ~/.local/share/uv/python/. NO sudo / NO apt required.
# ==============================================================

PYTHON_CMD=""

# Make sure user-local bin (where uv installs itself) is on PATH.
export PATH="$HOME/.local/bin:$PATH"

# 1. Try system python3.10
if command -v python3.10 &> /dev/null; then
    # Verify venv module is available; if not, fall through to uv.
    if python3.10 -c "import venv" &> /dev/null; then
        PYTHON_CMD="$(command -v python3.10)"
    fi
fi

# 2. Try uv-managed python3.10
if [ -z "$PYTHON_CMD" ] && command -v uv &> /dev/null; then
    UV_PY="$(uv python find 3.10 2>/dev/null || true)"
    if [ -n "$UV_PY" ] && [ -x "$UV_PY" ]; then
        PYTHON_CMD="$UV_PY"
    fi
fi

# 3. Install uv + python 3.10 (no sudo)
if [ -z "$PYTHON_CMD" ]; then
    echo "python3.10 not found. Installing it locally via uv (no sudo required)..."
    if ! command -v uv &> /dev/null; then
        if command -v curl &> /dev/null; then
            curl -LsSf https://astral.sh/uv/install.sh | sh
        elif command -v wget &> /dev/null; then
            wget -qO- https://astral.sh/uv/install.sh | sh
        else
            echo "ERROR: curl or wget is required to install uv."
            exit 1
        fi
        export PATH="$HOME/.local/bin:$PATH"
    fi
    uv python install 3.10
    PYTHON_CMD="$(uv python find 3.10)"
fi

echo "Using Python: $PYTHON_CMD ($($PYTHON_CMD --version))"

# Step 2: Create virtual environment
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    "$PYTHON_CMD" -m venv "$VENV_DIR"
fi

# Step 3: Install dependencies
"$VENV_DIR/bin/pip" install -q --upgrade pip
"$VENV_DIR/bin/pip" install -q -r "$SKILL_DIR/requirements.txt"

# Step 4: Download the pre-exported YOLO ONNX model bundle if missing.
# The model is distributed as a zip that extracts to a folder named
# ``kami-conflict-detection-model/`` containing one or more .onnx files
# (currently yolov8s-worldv2.onnx). We move the .onnx into the skill
# directory and remove the unpacked folder + zip afterwards.
MODEL_URL="https://publicfiles.xiaoyi.com/kami-conflict-detection-model.zip"
ONNX_TARGET="$SKILL_DIR/yolov8s-worldv2.onnx"
EXTRACT_DIR="$SKILL_DIR/kami-conflict-detection-model"
TMPZIP="$SKILL_DIR/kami-conflict-detection-model.zip"

if [ ! -f "$ONNX_TARGET" ]; then
    echo "YOLO ONNX model not found, downloading from $MODEL_URL ..."
    if command -v curl &> /dev/null; then
        curl -L --fail -o "$TMPZIP" "$MODEL_URL"
    elif command -v wget &> /dev/null; then
        wget -O "$TMPZIP" "$MODEL_URL"
    else
        echo "ERROR: curl or wget is required to download the model bundle."
        exit 1
    fi

    if ! command -v unzip &> /dev/null; then
        echo "ERROR: 'unzip' is required to extract the model bundle. "\
             "Install it (e.g., apt install unzip / brew install unzip) and rerun."
        exit 1
    fi

    echo "Extracting model bundle..."
    unzip -o "$TMPZIP" -d "$SKILL_DIR/" > /dev/null

    if [ -d "$EXTRACT_DIR" ]; then
        find "$EXTRACT_DIR" -name '*.onnx' -exec mv {} "$SKILL_DIR/" \;
        rm -rf "$EXTRACT_DIR"
    fi
    rm -f "$TMPZIP"

    if [ ! -f "$ONNX_TARGET" ]; then
        echo "ERROR: model bundle extracted but $ONNX_TARGET is still missing."
        exit 1
    fi
    echo "YOLO ONNX model ready: $ONNX_TARGET"
else
    echo "YOLO ONNX model already present: $ONNX_TARGET"
fi

# Step 5: Create alerts output directory
mkdir -p "$SKILL_DIR/alerts"

echo "Setup complete."
