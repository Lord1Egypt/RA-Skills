#!/bin/bash
# =============================================================================
# pg-memory Client Setup Script
# =============================================================================
# Run this on EACH OpenClaw machine that wants to connect to shared database.
# Auto-generates instance ID on first run.
# =============================================================================

set -e  # Exit on error

echo "🦞 pg-memory Client Setup"
echo "=========================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Detect OS
OS="$(uname -s)"
case "$OS" in
    Linux*) OS_TYPE="linux" ;;
    Darwin*) OS_TYPE="macos" ;;
    CYGWIN*|MINGW*|MSYS*) OS_TYPE="windows" ;;
    *)
        echo -e "${RED}Unsupported OS: $OS${NC}"
        exit 1
        ;;
esac

echo "Detected OS: $OS_TYPE"
echo ""

# OS-Specific config paths
if [ "$OS_TYPE" = "macos" ]; then
    CONFIG_DIR="$HOME/Library/Application Support/pg-memory"
    # Also create legacy ~/.config for compatibility
    LEGACY_CONFIG_DIR="$HOME/.config/pg-memory"
elif [ "$OS_TYPE" = "windows" ]; then
    CONFIG_DIR="${APPDATA}/pg-memory"
else
    # Linux and others
    CONFIG_DIR="$HOME/.config/pg-memory"
fi

echo "Config file will be: $CONFIG_DIR/config.env"
echo ""

# Create config directory
mkdir -p "$CONFIG_DIR"
if [ -n "$LEGACY_CONFIG_DIR" ]; then
    mkdir -p "$LEGACY_CONFIG_DIR"
fi

# =============================================================================
# Step 1: Get Database Connection Info
# =============================================================================
echo -e "${YELLOW}Step 1: Database Connection${NC}"
echo ""
echo "Enter the connection details for the pg-memory server."
echo ""

read -p "Database host/IP (e.g., 192.168.1.100): " DB_HOST
read -p "Database port [5432]: " DB_PORT
DB_PORT=${DB_PORT:-5432}
read -p "Database name [openclaw_memory]: " DB_NAME
DB_NAME=${DB_NAME:-openclaw_memory}
read -p "Database user [openclaw_user]: " DB_USER
DB_USER=${DB_USER:-openclaw_user}
read -sp "Database password: " DB_PASSWORD
echo ""

# =============================================================================
# Step 2: Agent Identity
# =============================================================================
echo ""
echo -e "${YELLOW}Step 2: Agent Identity${NC}"
echo ""
echo "Choose a name for this OpenClaw instance."
echo "This identifies who captured each observation."
echo ""

read -p "Agent name (e.g., arty, brodie, maya): " AGENT_NAME

if [ -z "$AGENT_NAME" ]; then
    echo -e "${RED}Agent name is required${NC}"
    exit 1
fi

# Validate agent name (alphanumeric, hyphen, underscore only)
if [[ ! "$AGENT_NAME" =~ ^[a-zA-Z0-9_-]+$ ]]; then
    echo -e "${RED}Invalid agent name. Use only letters, numbers, hyphens, underscores.${NC}"
    exit 1
fi

echo ""
echo "This instance will be identified as: $AGENT_NAME"
echo ""

# =============================================================================
# Step 3: Install Python Dependencies
# =============================================================================
echo -e "${YELLOW}Step 3: Installing Python dependencies...${NC}"

# Check Python
echo "Checking Python..."
if command -v python3 &> /dev/null; then
    PYTHON=python3
elif command -v python &> /dev/null; then
    PYTHON=python
else
    echo -e "${RED}Python 3 required but not found${NC}"
    exit 1
fi

$PYTHON --version
echo "✓ Python found"

# Install psycopg2
echo ""
echo "Installing psycopg2-binary..."
$PYTHON -m pip install psycopg2-binary --quiet
echo "✓ psycopg2-binary installed"

# =============================================================================
# Step 4: Setup pg-memory Skill
# =============================================================================
echo ""
echo -e "${YELLOW}Step 4: Setting up pg-memory skill...${NC}"

# Determine install location
WORKSPACE="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
INSTALL_DIR="$WORKSPACE/skills/pg-memory"

echo "Installing to: $INSTALL_DIR"

# Create directory
mkdir -p "$INSTALL_DIR"

# Check if we have the files locally (running from git clone)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ -f "$SCRIPT_DIR/scripts/pg_memory.py" ]; then
    # Copy from local git repo
    echo "Copying from local repository..."
    cp -r "$SCRIPT_DIR"/* "$INSTALL_DIR/"
else
    # Clone from GitHub
    echo "Cloning from GitHub..."
    if [ -d "$INSTALL_DIR/.git" ]; then
        echo "✓ Already cloned, pulling updates..."
        cd "$INSTALL_DIR" && git pull
    else
        git clone https://github.com/pottertech/pg-memory.git "$INSTALL_DIR"
    fi
fi

echo "✓ pg-memory skill installed"

# =============================================================================
# Step 5: Create Configuration
# =============================================================================
echo ""
echo -e "${YELLOW}Step 5: Creating configuration...${NC}"

# Determine config directory based on OS
case "$OS_TYPE" in
    macos)
        CONFIG_DIR="$HOME/Library/Application Support/pg-memory"
        ;;
    windows)
        CONFIG_DIR="$APPDATA/pg-memory"
        ;;
    linux)
        CONFIG_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/pg-memory"
        ;;
esac

mkdir -p "$CONFIG_DIR"

# Create config.env
cat > "$CONFIG_DIR/config.env" << EOF
# pg-memory Configuration
# Generated: $(date -Iseconds)

# Database Connection
PG_MEMORY_HOST=$DB_HOST
PG_MEMORY_PORT=$DB_PORT
PG_MEMORY_DB=$DB_NAME
PG_MEMORY_USER=$DB_USER
PG_MEMORY_PASSWORD=$DB_PASSWORD

# Agent Identity
OPENCLAW_NAME=$AGENT_NAME

# Performance
PG_MEMORY_POOL_MIN=2
PG_MEMORY_POOL_MAX=10
PG_MEMORY_TIMEOUT=30
EOF

echo "✓ Configuration saved to: $CONFIG_DIR/config.env"

# =============================================================================
# Step 6: Generate Instance ID (First Run)
# =============================================================================
echo ""
echo -e "${YELLOW}Step 6: Generating instance ID...${NC}"
echo ""
echo "This ID uniquely identifies this machine."
echo "It's generated once and never changes."
echo ""

# Create Python script for first run
FIRST_RUN_SCRIPT=$(cat << 'PYTHON_SCRIPT'
import os
import sys
import json
import uuid
from pathlib import Path

# Load config
config_file = Path.home() / ".config" / "pg-memory" / "config.env"
if sys.platform == "darwin":
    config_file = Path.home() / "Library" / "Application Support" / "pg-memory" / "config.env"

if config_file.exists():
    with open(config_file) as f:
        for line in f:
            if '=' in line and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ[key] = value

# Generate instance ID
instance_file = config_file.parent / "instance.json"

if instance_file.exists():
    with open(instance_file) as f:
        data = json.load(f)
        instance_id = data['instance_id']
        print(f"Using existing instance ID: {instance_id}")
else:
    instance_id = str(uuid.uuid4())
    data = {
        "instance_id": instance_id,
        "created_at": str(uuid.uuid1()),  # Timestamp
        "platform": sys.platform
    }
    with open(instance_file, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Generated new instance ID: {instance_id}")

print(f"\nAgent: {os.environ.get('OPENCLAW_NAME', 'unknown')}")
print(f"Instance: {instance_id}")
print(f"Config: {config_file}")
PYTHON_SCRIPT
)

# Run the script
$PYTHON -c "$FIRST_RUN_SCRIPT"

INSTANCE_ID=$($PYTHON -c "import json; print(json.load(open('$CONFIG_DIR/instance.json'))['instance_id'])")

echo ""
echo "✓ Instance ID generated: ${INSTANCE_ID:0:8}..."

# =============================================================================
# Step 7: Test Connection
# =============================================================================
echo ""
echo -e "${YELLOW}Step 7: Testing database connection...${NC}"
echo ""

TEST_SCRIPT=$(cat << PYTHON_SCRIPT
import os
import sys
sys.path.insert(0, "$INSTALL_DIR/scripts")

# Import after setting path
try:
    from pg_memory import PostgresMemory
    
    print("Connecting to database...")
    mem = PostgresMemory()
    
    # Test capture
    result = mem.capture(
        content="Test observation from $AGENT_NAME",
        source="setup",
        agent_label="$AGENT_NAME"
    )
    
    print(f"\n✓ Connected successfully!")
    print(f"✓ Test observation captured: {result['id'][:8]}...")
    print(f"\nInstance Details:")
    print(f"  Agent: {result.get('agent_label', '$AGENT_NAME')}")
    print(f"  Instance: {result.get('instance_id', 'N/A')[:8]}...")
    
except Exception as e:
    print(f"\n✗ Connection failed: {e}")
    sys.exit(1)
PYTHON_SCRIPT
)

if $PYTHON -c "$TEST_SCRIPT" 2>&1; then
    echo ""
    echo -e "${GREEN}✅ Client Setup Complete!${NC}"
else
    echo ""
    echo -e "${RED}✗ Setup failed. Check connection details and try again.${NC}"
    exit 1
fi

# =============================================================================
# Summary
# =============================================================================
echo ""
echo "=========================="
echo ""
echo -e "${BLUE}Configuration Summary:${NC}"
echo ""
echo "Agent Name:     $AGENT_NAME"
echo "Instance ID:    ${INSTANCE_ID:0:8}...${INSTANCE_ID: -8}"
echo "Database Host:  $DB_HOST"
echo "Database:       $DB_NAME"
echo "Config File:    $CONFIG_DIR/config.env"
echo "Instance File:  $CONFIG_DIR/instance.json"
echo ""
echo -e "${YELLOW}Usage:${NC}"
echo ""
echo "From Python:"
echo "  from pg_memory import PostgresMemory"
echo "  mem = PostgresMemory()"
echo "  mem.capture('My observation', tags=['test'])"
echo ""
echo "From CLI:"
echo "  pg-memory capture 'My observation' --tags test"
echo ""
echo -e "${GREEN}🦞 This OpenClaw is ready for shared memory!${NC}"
echo ""
