#!/bin/bash

WORKSPACE_DIR="$HOME/.openclaw/zhaining"
SECRETS_DIR="$WORKSPACE_DIR/.secrets"
VAULT_FILE="$SECRETS_DIR/vault.json.enc"

show_usage() {
  echo "OpenClaw Key Manager (Fixed Version)"
  echo "Usage: $0 [command] [options]"
  echo ""
  echo "Commands:"
  echo "  init          Initialize key vault"
  echo "  add NAME      Add new secret"
  echo "  get NAME      Get secret value"
  echo "  list          List all secrets"
  echo "  backup        Create backup"
  echo "  migrate       Migrate existing credentials"
}

case "$1" in
  "init")
    mkdir -p "$SECRETS_DIR/backup" "$SECRETS_DIR/temp"
    echo "Vault initialized at $SECRETS_DIR"
    ;;
    
  "add")
    if [ -z "$2" ]; then
      echo "Error: Secret name required"
      exit 1
    fi
    SECRET_NAME="$2"
    echo -n "Enter secret value for '$SECRET_NAME': "
    read -s SECRET_VALUE
    echo
    
    # Create a temporary script file
    TEMP_SCRIPT=$(mktemp)
    cat > "$TEMP_SCRIPT" << EOF
const SecureKeyVault = require('$WORKSPACE_DIR/scripts/key_vault_simple.js');
const vault = new SecureKeyVault('$WORKSPACE_DIR');

async function addSecret() {
  try {
    await vault.initialize();
    await vault.setSecret('$SECRET_NAME', '$SECRET_VALUE', {type: 'manual'});
    console.log('Secret added successfully');
  } catch (err) {
    console.error('Error:', err.message);
    process.exit(1);
  }
}

addSecret();
EOF

    node "$TEMP_SCRIPT"
    rm "$TEMP_SCRIPT"
    ;;
    
  "get")
    if [ -z "$2" ]; then
      echo "Error: Secret name required"
      exit 1
    fi
    SECRET_NAME="$2"
    
    TEMP_SCRIPT=$(mktemp)
    cat > "$TEMP_SCRIPT" << EOF
const SecureKeyVault = require('$WORKSPACE_DIR/scripts/key_vault_simple.js');
const vault = new SecureKeyVault('$WORKSPACE_DIR');

async function getSecret() {
  try {
    await vault.initialize();
    const value = await vault.getSecret('$SECRET_NAME');
    console.log(value);
  } catch (err) {
    console.error('Error:', err.message);
    process.exit(1);
  }
}

getSecret();
EOF

    node "$TEMP_SCRIPT"
    rm "$TEMP_SCRIPT"
    ;;
    
  "list")
    if [ -f "$VAULT_FILE" ]; then
      echo "Stored secrets:"
      TEMP_SCRIPT=$(mktemp)
      cat > "$TEMP_SCRIPT" << EOF
const SecureKeyVault = require('$WORKSPACE_DIR/scripts/key_vault_simple.js');
const vault = new SecureKeyVault('$WORKSPACE_DIR');

async function listSecrets() {
  try {
    await vault.initialize();
    const keys = Object.keys(vault.vault);
    if (keys.length === 0) {
      console.log('No secrets found');
    } else {
      keys.forEach(key => {
        console.log('- ' + key);
      });
    }
  } catch (err) {
    console.error('Error:', err.message);
    process.exit(1);
  }
}

listSecrets();
EOF

      node "$TEMP_SCRIPT"
      rm "$TEMP_SCRIPT"
    else
      echo "No vault file found"
    fi
    ;;
    
  "backup")
    if [ -f "$VAULT_FILE" ]; then
      BACKUP_FILE="$SECRETS_DIR/backup/vault_$(date +%Y-%m-%d).json.enc"
      cp "$VAULT_FILE" "$BACKUP_FILE"
      echo "Backup created: $BACKUP_FILE"
    else
      echo "No vault file to backup"
    fi
    ;;
    
  "migrate")
    echo "Migrating existing credentials from MEMORY.md..."
    # Extract Instreet API key from MEMORY.md
    if grep -q "sk_inst_" "$WORKSPACE_DIR/MEMORY.md"; then
      API_KEY=$(grep "sk_inst_" "$WORKSPACE_DIR/MEMORY.md" | sed 's/.*sk_inst_/sk_inst_/' | cut -d' ' -f1 | tr -d '\r\n')
      if [ -n "$API_KEY" ]; then
        echo "Found Instreet API key, migrating..."
        TEMP_SCRIPT=$(mktemp)
        cat > "$TEMP_SCRIPT" << EOF
const SecureKeyVault = require('$WORKSPACE_DIR/scripts/key_vault_simple.js');
const fs = require('fs');
const vault = new SecureKeyVault('$WORKSPACE_DIR');

async function migrateCredentials() {
  try {
    await vault.initialize();
    await vault.setSecret('instreet_api_key', '$API_KEY', {type: 'api_key', service: 'instreet'});
    console.log('Instreet API key migrated successfully');
    
    // Update MEMORY.md to use reference
    let memoryContent = fs.readFileSync('$WORKSPACE_DIR/MEMORY.md', 'utf8');
    memoryContent = memoryContent.replace(/sk_inst_[a-f0-9]+/, '{SECRET:instreet_api_key}');
    fs.writeFileSync('$WORKSPACE_DIR/MEMORY.md', memoryContent);
    console.log('MEMORY.md updated with secure reference');
  } catch (err) {
    console.error('Migration error:', err.message);
    process.exit(1);
  }
}

migrateCredentials();
EOF

        node "$TEMP_SCRIPT"
        rm "$TEMP_SCRIPT"
      fi
    fi
    ;;
    
  *)
    show_usage
    ;;
esac