#!/bin/bash
#
# pg-memory v2.6.0 Installation Script
# PostgreSQL-based structured memory for OpenClaw
#
# Usage: ./install.sh [options]
#   --skip-db-check    Skip PostgreSQL connection test
#   --reset            Reset database (WARNING: destroys data)
#   --help             Show this help

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VERSION="2.6.0"
DB_NAME="${PG_MEMORY_DB:-openclaw_memory}"
DB_USER="${PG_MEMORY_USER:-$USER}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_info() { echo -e "${BLUE}ℹ️  $1${NC}"; }
print_success() { echo -e "${GREEN}✅ $1${NC}"; }
print_warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
print_error() { echo -e "${RED}❌ $1${NC}"; }

show_help() {
    cat << EOF
pg-memory v${VERSION} Installation Script

Usage: ./install.sh [OPTIONS]

Options:
  --skip-db-check    Skip PostgreSQL connection verification
  --reset            Reset database (DESTROYS all data)
  --help             Show this help message

Environment Variables:
  PG_MEMORY_DB       Database name (default: openclaw_memory)
  PG_MEMORY_USER     Database user (default: current user)
  PG_MEMORY_HOST     Database host (default: localhost)
  PG_MEMORY_PORT     Database port (default: 5432)
  PG_MEMORY_PASSWORD Database password (if needed)

Examples:
  ./install.sh                      # Fresh install
  ./install.sh --reset              # Reset everything
  PG_MEMORY_DB=mydb ./install.sh    # Use custom database

EOF
    exit 0
}

# Parse arguments
SKIP_DB_CHECK=false
RESET_DB=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --skip-db-check) SKIP_DB_CHECK=true; shift ;;
        --reset) RESET_DB=true; shift ;;
        --help) show_help ;;
        *) print_error "Unknown option: $1"; show_help ;;
    esac
done

echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║          pg-memory v${VERSION} Installation              ║"
echo "║     PostgreSQL-based Memory for OpenClaw                 ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Step 1: Check Python
print_info "Checking Python..."
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 not found. Please install Python 3.10+"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | grep -oE '[0-9]+\.[0-9]+' | head -1)
print_success "Python ${PYTHON_VERSION} found"

# Step 2: Check PostgreSQL
print_info "Checking PostgreSQL..."
if ! command -v psql &> /dev/null; then
    print_warning "PostgreSQL not found. Installing..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        if command -v brew &> /dev/null; then
            brew install postgresql@18
            brew services start postgresql@18
        else
            print_error "Homebrew not found. Please install PostgreSQL 18 manually."
            exit 1
        fi
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        print_error "Please install PostgreSQL 18 manually: sudo apt install postgresql-18"
        exit 1
    else
        print_error "Unsupported OS. Please install PostgreSQL 18 manually."
        exit 1
    fi
else
    PG_VERSION=$(psql --version | grep -oE '[0-9]+' | head -1)
    print_success "PostgreSQL ${PG_VERSION} found"
fi

# Step 3: Install Python dependencies
print_info "Installing Python dependencies..."
pip3 install --user psycopg2-binary 2>/dev/null || pip3 install psycopg2-binary
print_success "Python dependencies installed"

# Step 4: Test database connection (unless skipped)
if [[ "$SKIP_DB_CHECK" == false ]]; then
    print_info "Testing PostgreSQL connection..."
    if ! psql -U "$DB_USER" -d postgres -c "SELECT 1;" &> /dev/null; then
        print_warning "Cannot connect to PostgreSQL as user '$DB_USER'"
        print_info "Attempting to create database user..."
        
        # Try to create user and database
        if [[ "$OSTYPE" == "darwin"* ]]; then
            # macOS with Homebrew PostgreSQL
            if command -v brew &> /dev/null; then
                PG_BIN="$(brew --prefix postgresql@18)/bin"
                if [[ -d "$PG_BIN" ]]; then
                    export PATH="$PG_BIN:$PATH"
                fi
            fi
        fi
        
        # Create user if doesn't exist
        if command -v createuser &> /dev/null; then
            createuser -s "$DB_USER" 2>/dev/null || true
        fi
    fi
    
    # Test again
    if psql -U "$DB_USER" -d postgres -c "SELECT 1;" &> /dev/null; then
        print_success "PostgreSQL connection successful"
    else
        print_warning "Could not verify PostgreSQL connection"
        print_info "You may need to:"
        echo "  1. Start PostgreSQL: brew services start postgresql@18"
        echo "  2. Create user: createuser -s $USER"
        echo "  3. Or use: ./install.sh --skip-db-check"
        exit 1
    fi
fi

# Step 5: Initialize database
print_info "Initializing database..."

if [[ "$RESET_DB" == true ]]; then
    print_warning "Resetting database (DESTROYS all data)..."
    psql -U "$DB_USER" -c "DROP DATABASE IF EXISTS $DB_NAME;" 2>/dev/null || true
    psql -U "$DB_USER" -c "DROP USER IF EXISTS openclaw;" 2>/dev/null || true
fi

# Create database if doesn't exist
if ! psql -U "$DB_USER" -lqt | cut -d \| -f 1 | grep -qw "$DB_NAME"; then
    print_info "Creating database: $DB_NAME"
    psql -U "$DB_USER" -c "CREATE DATABASE $DB_NAME;"
    print_success "Database created"
else
    print_info "Database $DB_NAME already exists"
fi

# Step 6: Run schema initialization
print_info "Running database schema initialization..."
if [[ -f "$SCRIPT_DIR/scripts/init_memory_schema.sql" ]]; then
    psql -U "$DB_USER" -d "$DB_NAME" -f "$SCRIPT_DIR/scripts/init_memory_schema.sql" || {
        print_error "Schema initialization failed"
        exit 1
    }
    print_success "Schema initialized"
else
    print_error "Schema file not found: $SCRIPT_DIR/scripts/init_memory_schema.sql"
    exit 1
fi

# Step 7: Run v2.5 migrations
if [[ -f "$SCRIPT_DIR/scripts/schema_v2_5_partitioning.sql" ]]; then
    print_info "Applying v2.5 partitioning..."
    psql -U "$DB_USER" -d "$DB_NAME" -f "$SCRIPT_DIR/scripts/schema_v2_5_partitioning.sql" || {
        print_warning "Partitioning migration may have already been applied"
    }
fi

# Step 8: Make CLI executable
print_info "Setting up CLI..."
chmod +x "$SCRIPT_DIR/scripts/pg-memory-cli" 2>/dev/null || true
print_success "CLI ready"

# Step 9: Create config file
print_info "Creating configuration..."
CONFIG_FILE="$SCRIPT_DIR/.pg_memory_config"
cat > "$CONFIG_FILE" << EOF
# pg-memory v${VERSION} Configuration
# Generated: $(date)

# Database settings
export PG_MEMORY_DB="${DB_NAME}"
export PG_MEMORY_USER="${DB_USER}"
export PG_MEMORY_HOST="${PG_MEMORY_HOST:-localhost}"
export PG_MEMORY_PORT="${PG_MEMORY_PORT:-5432}"

# Optional: Set password if needed
# export PG_MEMORY_PASSWORD="your_password"

# Add to your shell profile (.zshrc or .bashrc):
# source $CONFIG_FILE
EOF

print_success "Config saved to $CONFIG_FILE"

# Summary
echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║           Installation Complete! 🎉                      ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
print_success "pg-memory v${VERSION} is ready!"
echo ""
echo "Next steps:"
echo "  1. Source the config: source $CONFIG_FILE"
echo "  2. Add to your profile: echo 'source $CONFIG_FILE' >> ~/.zshrc"
echo "  3. Test it: $SCRIPT_DIR/scripts/pg-memory-cli --version"
echo ""
echo "Quick start:"
echo "  $SCRIPT_DIR/scripts/pg-memory-cli capture 'Hello pg-memory!' --tags test"
echo "  $SCRIPT_DIR/scripts/pg-memory-cli search 'hello'"
echo ""
echo "New in v2.6.0:"
echo "  • Duplicate detection: --check-duplicates"
echo "  • Tag autocomplete: pg-memory-cli tags --content '...'"
echo ""
