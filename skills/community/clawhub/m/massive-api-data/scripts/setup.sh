#!/bin/bash
# Massive Data Feed Skill - Environment Setup
# Run once before using the skill for the first time.

set -e

VENV_DIR=".venv-massive"

echo "Creating virtual environment at $VENV_DIR ..."
python3 -m venv "$VENV_DIR"

echo "Installing pinned dependencies..."
"$VENV_DIR/bin/pip" install --quiet \
  "massive-python-client==1.0.0" \
  "websockets==12.0" \
  "boto3==1.34.69" \
  "python-dotenv==1.2.2"

echo "Verifying installed versions..."
MASSIVE_VER=$("$VENV_DIR/bin/pip" show massive-python-client 2>/dev/null | grep "^Version:" | awk '{print $2}')
WS_VER=$("$VENV_DIR/bin/pip" show websockets | grep "^Version:" | awk '{print $2}')
BOTO_VER=$("$VENV_DIR/bin/pip" show boto3 | grep "^Version:" | awk '{print $2}')
echo "  massive-python-client: $MASSIVE_VER (expected 1.0.0)"
echo "  websockets:            $WS_VER (expected 12.0)"
echo "  boto3:                 $BOTO_VER (expected 1.34.69)"

echo ""
echo "Setup complete. Activate the environment with:"
echo "  source $VENV_DIR/bin/activate"
echo ""
echo "Required env vars (add to .env file):"
echo "  MASSIVE_API_KEY=<from https://massive.com/dashboard/keys>"
echo ""
echo "Optional (only needed for Flat Files bulk downloads):"
echo "  MASSIVE_S3_ACCESS_KEY=<from https://massive.com/dashboard/keys>"
echo "  MASSIVE_S3_SECRET_KEY=<from https://massive.com/dashboard/keys>"
