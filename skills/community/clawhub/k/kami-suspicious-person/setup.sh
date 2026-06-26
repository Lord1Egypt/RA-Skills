#!/bin/bash
set -e

SKILL_DIR="$(dirname "$(realpath "$0")")"
VENV_DIR="$SKILL_DIR/.venv"
MODELS_DIR="$SKILL_DIR/models"

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

# Step 4: Create directories
mkdir -p "$SKILL_DIR/alerts"
mkdir -p "$SKILL_DIR/face_db"
mkdir -p "$MODELS_DIR"

# Step 5: Download ONNX models if not present
DET_MODEL="$MODELS_DIR/det_10g.onnx"
REC_MODEL="$MODELS_DIR/w600k_r50.onnx"
MODEL_URL="https://publicfiles.xiaoyi.com/kami-suspicious-person-model.zip"

if [ ! -f "$DET_MODEL" ] || [ ! -f "$REC_MODEL" ]; then
    echo "Downloading face detection and recognition models..."
    TMPZIP=$(mktemp /tmp/kami_model_XXXXXX.zip)
    if command -v curl &> /dev/null; then
        curl -L -o "$TMPZIP" "$MODEL_URL"
    elif command -v wget &> /dev/null; then
        wget -O "$TMPZIP" "$MODEL_URL"
    else
        echo "ERROR: Neither curl nor wget found. Please install one of them."
        echo "  Or manually download the model zip from:"
        echo "  $MODEL_URL"
        echo "  and place det_10g.onnx and w600k_r50.onnx into $MODELS_DIR/"
        exit 1
    fi

    echo "Extracting models..."
    EXTRACT_DIR="$SKILL_DIR/kami-suspicious-person-model"
    if command -v unzip &> /dev/null; then
        unzip -o "$TMPZIP" -d "$SKILL_DIR/"
    else
        # Fallback: use Python to extract
        "$VENV_DIR/bin/python" -c "
import zipfile, sys
with zipfile.ZipFile('$TMPZIP', 'r') as z:
    z.extractall('$SKILL_DIR/')
print('Extracted successfully.')
"
    fi
    # Move model files to models/ directory
    if [ -d "$EXTRACT_DIR" ]; then
        find "$EXTRACT_DIR" -name '*.onnx' -exec mv {} "$MODELS_DIR/" \;
        rm -rf "$EXTRACT_DIR"
    fi
    rm -f "$TMPZIP"
    echo "Models downloaded successfully."
else
    echo "Models already present."
fi

echo ""
echo "Setup complete."
echo ""
echo "Next steps:"
echo "  1. Place registered face images in face_db/<person_name>/xxx.jpg"
echo "     Example: face_db/John/photo1.jpg"
echo "  2. (Optional) Build face database: .venv/bin/python build_face_db.py"
echo "  3. Run: .venv/bin/python suspicious_person_detector.py --rtsp_url <your-url>"
