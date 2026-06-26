#!/bin/bash
set -e

SKILL_DIR="$(dirname "$(realpath "$0")")"
VENV_DIR="$SKILL_DIR/.venv"
CONDA_ENV_NAME="kami-fall"
PYTHON_VERSION="3.10"

PYTHON_CMD=""

# Step 1: Check for conda first
if command -v conda &> /dev/null; then
    echo "✅ Conda detected"
    
    # Check if the kami-fall environment already exists
    if conda env list | grep -q "^${CONDA_ENV_NAME} "; then
        echo "✅ Conda environment '${CONDA_ENV_NAME}' found"
        
        # Check Python version in the environment
        CONDA_PYTHON_VERSION=$(conda run -n "$CONDA_ENV_NAME" python --version 2>&1 | awk '{print $2}')
        echo "   Python version: $CONDA_PYTHON_VERSION"
        
        # Check if Python version is 3.10.x
        if echo "$CONDA_PYTHON_VERSION" | grep -q "^3\.10\."; then
            echo "✅ Python 3.10 detected in conda environment"
            PYTHON_CMD="conda run -n $CONDA_ENV_NAME python"
        else
            echo "⚠️ Python version is not 3.10.x (found: $CONDA_PYTHON_VERSION)"
            echo "   Recreating conda environment with Python 3.10..."
            conda env remove -n "$CONDA_ENV_NAME" -y
            conda create -n "$CONDA_ENV_NAME" python="$PYTHON_VERSION" -y
            PYTHON_CMD="conda run -n $CONDA_ENV_NAME python"
        fi
    else
        echo "📦 Conda environment '${CONDA_ENV_NAME}' not found. Creating..."
        conda create -n "$CONDA_ENV_NAME" python="$PYTHON_VERSION" -y
        PYTHON_CMD="conda run -n $CONDA_ENV_NAME python"
    fi

# Step 2: Fall back to pyenv
elif command -v pyenv &> /dev/null; then
    echo "✅ pyenv detected"
    
    # Check if Python 3.10 is installed via pyenv
    if pyenv versions | grep -q "3\.10"; then
        PYENV_VERSION=$(pyenv version | awk '{print $1}')
        echo "✅ pyenv Python version: $PYENV_VERSION"
        PYTHON_CMD="python3"
    else
        echo "⚠️ Python 3.10 not installed via pyenv"
        echo "   Installing Python 3.10 via pyenv..."
        pyenv install 3.10
        pyenv global 3.10
        PYTHON_CMD="python3"
    fi

# Step 3: Fall back to system python3 or python
elif command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
fi

# Final check: If no Python found
if [ -z "$PYTHON_CMD" ]; then
    echo "❌ Python not found."
    echo ""
    echo "Please install Python 3.10+ before running this skill."
    echo "Recommended methods (no sudo required):"
    echo ""
    echo "  📦 Conda (preferred):"
    echo "     conda create -n kami-fall python=3.10"
    echo "     conda activate kami-fall"
    echo ""
    echo "  🐍 pyenv (Linux/macOS - user-level install):"
    echo "     curl https://pyenv.run | bash"
    echo "     pyenv install 3.10"
    echo "     pyenv global 3.10"
    echo ""
    echo "  🍎 macOS (Homebrew):"
    echo "     brew install python@3.10"
    echo ""
    echo "After installation, re-run this setup script."
    echo ""
    exit 1
fi

echo ""
echo "Using Python: $($PYTHON_CMD --version 2>&1 | head -1)"

# Install dependencies
if echo "$PYTHON_CMD" | grep -q "conda run"; then
    # Conda environment - use conda's pip
    echo "Installing dependencies in conda environment..."
    conda run -n "$CONDA_ENV_NAME" pip install -q -r "$SKILL_DIR/requirements.txt"
    PYTHON_RUN_CMD="conda run -n $CONDA_ENV_NAME python"
else
    # venv environment - create if needed
    if [ ! -d "$VENV_DIR" ]; then
        echo "Creating virtual environment..."
        $PYTHON_CMD -m venv "$VENV_DIR"
    fi
    "$VENV_DIR/bin/pip" install -q -r "$SKILL_DIR/requirements.txt"
    PYTHON_RUN_CMD="$VENV_DIR/bin/python"
fi

echo ""
echo "✅ Setup complete."
echo ""
echo "Run with:"
echo "  $PYTHON_RUN_CMD $SKILL_DIR/fall_detect_cloud_skill.py \\"
echo "      --rtsp_url <RTSP_URL> \\"
echo "      --api_key <KAMICLAW_KEY>"
echo ""
echo "Or activate environment and run:"
if echo "$PYTHON_CMD" | grep -q "conda run"; then
    echo "  conda activate $CONDA_ENV_NAME"
    echo "  python $SKILL_DIR/fall_detect_cloud_skill.py"
else
    echo "  source $VENV_DIR/bin/activate"
    echo "  python $SKILL_DIR/fall_detect_cloud_skill.py"
fi
