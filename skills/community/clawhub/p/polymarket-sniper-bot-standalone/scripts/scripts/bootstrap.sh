#!/bin/bash

# Polymarket Sniper Bot Bootstrap Script (v3 - Force system packages)
# This script initializes the environment, database, and system services.

echo "🚀 Starting Polymarket Sniper Bot bootstrap..."

# Check for Python
if ! command -v python3 &> /dev/null
then
    echo "❌ Error: python3 is not installed. Please install it first."
    exit 1
fi

# 1. Install Dependencies (Bypassing PEP 668 restrictions)
echo "📦 Installing Python dependencies (bypassing system restrictions)..."
pip3 install -r requirements.txt --quiet --break-system-packages

# 2. Initialize Database
echo "🗄️ Initializing SQLite database (sniper.db)..."
python3 db.py

# 3. Create config.yaml if it doesn't exist
if [ ! -f config.yaml ]; then
    echo "📄 Creating config.yaml from example..."
    cp config.yaml.example config.yaml
    echo "⚠️  Action Required: Update config.yaml with your RPC URL and Private Key."
fi

# 4. Success message
echo "✅ Bootstrap complete!"
echo "--------------------------------------------------------"
echo "To start the dashboard: python3 dashboard.py"
echo "To run a manual scan: python3 polymarket.py scan"
echo "To run with OpenClaw: openclaw cron add --agent polymarket-sniper"
echo "--------------------------------------------------------"
