#!/bin/bash
# =============================================================================
# pg-memory Server Setup Script
# =============================================================================
# Run this ONCE on the database server machine.
# Sets up PostgreSQL with pgvector for multi-instance OpenClaw deployment.
# =============================================================================

set -e  # Exit on error

echo "🦞 pg-memory Server Setup"
echo "=========================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
DB_NAME="${PG_MEMORY_DB:-openclaw_memory}"
DB_USER="${PG_MEMORY_USER:-openclaw_user}"
DB_PORT="${PG_MEMORY_PORT:-5432}"
PG_VERSION="${PG_VERSION:-17}"

# Detect OS
OS="$(uname -s)"
case "$OS" in
    Linux*)
        if [ -f /etc/debian_version ]; then
            OS_TYPE="debian"
        elif [ -f /etc/redhat-release ]; then
            OS_TYPE="rhel"
        else
            OS_TYPE="linux"
        fi
        ;;
    Darwin*)
        OS_TYPE="macos"
        ;;
    *)
        echo -e "${RED}Unsupported OS: $OS${NC}"
        exit 1
        ;;
esac

echo "Detected OS: $OS_TYPE"
echo ""

# =============================================================================
# Step 1: Check/Install PostgreSQL
# =============================================================================
echo -e "${YELLOW}Step 1: Installing PostgreSQL...${NC}"

if command -v pg_ctl &> /dev/null || command -v pg_isready &> /dev/null; then
    echo "✓ PostgreSQL appears to be installed"
    pg_config --version
else
    case "$OS_TYPE" in
        macos)
            if ! command -v brew &> /dev/null; then
                echo -e "${RED}Homebrew required. Install from https://brew.sh${NC}"
                exit 1
            fi
            echo "Installing PostgreSQL $PG_VERSION via Homebrew..."
            brew install postgresql@$PG_VERSION
            brew services start postgresql@$PG_VERSION
            ;;
        debian)
            echo "Installing PostgreSQL via apt..."
            sudo apt update
            sudo apt install -y postgresql-$PG_VERSION postgresql-contrib-$PG_VERSION
            sudo systemctl start postgresql
            ;;
        rhel)
            echo "Installing PostgreSQL via yum..."
            sudo yum install -y postgresql$PG_VERSION-server postgresql$PG_VERSION-contrib
            sudo systemctl start postgresql-$PG_VERSION
            ;;
    esac
fi

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to start..."
for i in {1..30}; do
    if pg_isready -q 2>/dev/null || sudo -u postgres pg_isready -q 2>/dev/null; then
        echo "✓ PostgreSQL is running"
        break
    fi
    sleep 1
done

# =============================================================================
# Step 2: Install pgvector Extension
# =============================================================================
echo ""
echo -e "${YELLOW}Step 2: Installing pgvector extension...${NC}"

case "$OS_TYPE" in
    macos)
        if brew list pgvector &>/dev/null; then
            echo "✓ pgvector already installed"
        else
            echo "Installing pgvector via Homebrew..."
            brew install pgvector
        fi
        ;;
    debian)
        if dpkg -l | grep -q postgresql-$PG_VERSION-pgvector; then
            echo "✓ pgvector already installed"
        else
            echo "Installing pgvector..."
            sudo apt install -y postgresql-$PG_VERSION-pgvector
        fi
        ;;
    rhel)
        echo "Please install pgvector manually from https://github.com/pgvector/pgvector"
        echo "Or use: sudo dnf install pgvector_$PG_VERSION"
        ;;
esac

# =============================================================================
# Step 3: Create Database and User
# =============================================================================
echo ""
echo -e "${YELLOW}Step 3: Creating database and user...${NC}"

# Use postgres user for database operations
PSQL="sudo -u postgres psql"
if [ "$OS_TYPE" = "macos" ]; then
    # On macOS with Homebrew, use current user if not using system postgres
    PSQL="psql"
fi

# Create database user
echo "Creating database user: $DB_USER"
if $PSQL -tAc "SELECT 1 FROM pg_roles WHERE rolname='$DB_USER'" | grep -q 1; then
    echo "✓ User $DB_USER already exists"
else
    # Prompt for password
    read -sp "Enter password for $DB_USER: " DB_PASSWORD
    echo ""
    read -sp "Confirm password: " DB_PASSWORD_CONFIRM
    echo ""
    
    if [ "$DB_PASSWORD" != "$DB_PASSWORD_CONFIRM" ]; then
        echo -e "${RED}Passwords do not match${NC}"
        exit 1
    fi
    
    $PSQL -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';"
    $PSQL -c "ALTER USER $DB_USER CREATEDB;"
    echo "✓ User created"
fi

# Create database
echo "Creating database: $DB_NAME"
if $PSQL -tAc "SELECT 1 FROM pg_database WHERE datname='$DB_NAME'" | grep -q 1; then
    echo "✓ Database $DB_NAME already exists"
    read -p "Drop and recreate? (y/N): " RECREATE
    if [[ $RECREATE =~ ^[Yy]$ ]]; then
        $PSQL -c "DROP DATABASE $DB_NAME;"
        $PSQL -c "CREATE DATABASE $DB_NAME OWNER $DB_USER;"
    fi
else
    $PSQL -c "CREATE DATABASE $DB_NAME OWNER $DB_USER;"
    echo "✓ Database created"
fi

# Grant permissions
$PSQL -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;"

# =============================================================================
# Step 4: Enable Extensions and Run Schema
# =============================================================================
echo ""
echo -e "${YELLOW}Step 4: Setting up schema...${NC}"

# Enable extensions
echo "Enabling extensions..."
$PSQL -d $DB_NAME -c "CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";"
$PSQL -d $DB_NAME -c "CREATE EXTENSION IF NOT EXISTS \"pg_trgm\";"
$PSQL -d $DB_NAME -c "CREATE EXTENSION IF NOT EXISTS \"vector\";"
echo "✓ Extensions enabled"

# Find schema file
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCHEMA_FILE="$SCRIPT_DIR/scripts/init_memory_schema.sql"

if [ ! -f "$SCHEMA_FILE" ]; then
    echo -e "${RED}Schema file not found: $SCHEMA_FILE${NC}"
    echo "Please ensure pg-memory is cloned properly"
    exit 1
fi

# Run schema
echo "Creating database schema..."
$PSQL -d $DB_NAME -f "$SCHEMA_FILE"
echo "✓ Schema created"

# =============================================================================
# Step 5: Network Configuration (for remote clients)
# =============================================================================
echo ""
echo -e "${YELLOW}Step 5: Network configuration...${NC}"

echo "To allow remote connections:"
echo ""
echo "1. Edit postgresql.conf:"
echo "   listen_addresses = '*'"
echo ""
echo "2. Edit pg_hba.conf and add:"
echo "   host  all  all  0.0.0.0/0  md5"
echo ""
echo "3. Restart PostgreSQL:"
case "$OS_TYPE" in
    macos)
        echo "   brew services restart postgresql@$PG_VERSION"
        ;;
    debian|rhel)
        echo "   sudo systemctl restart postgresql"
        ;;
esac

echo ""
echo "⚠️  Security Note: Use specific IP ranges instead of 0.0.0.0/0 for production!"

# =============================================================================
# Step 6: Display Connection Info
# =============================================================================
echo ""
echo -e "${GREEN}✅ Server Setup Complete!${NC}"
echo "=========================="
echo ""
echo "Database: $DB_NAME"
echo "User: $DB_USER"
echo "Port: $DB_PORT"
echo ""
echo "Connection strings for clients:"
echo ""
echo "URI format:"
echo "  postgresql://$DB_USER:PASSWORD@YOUR_SERVER_IP:$DB_PORT/$DB_NAME"
echo ""
echo "psql command:"
echo "  psql -h YOUR_SERVER_IP -p $DB_PORT -U $DB_USER -d $DB_NAME"
echo ""
echo "Test locally:"
echo "  psql -d $DB_NAME -c \"SELECT version();\""
echo ""
echo -e "${YELLOW}Next Steps:${NC}"
echo "1. Note the database password you set"
echo "2. Configure network access if clients are remote"
echo "3. Run client-setup.sh on each OpenClaw machine"
echo ""
echo "🦞 pg-memory server is ready for multi-instance deployment!"
