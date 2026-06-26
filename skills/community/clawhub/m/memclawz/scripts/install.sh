#!/bin/bash
set -e
echo "🧠 Installing MemClawz v5..."

# Check prerequisites
command -v python3 >/dev/null || { echo "❌ python3 required"; exit 1; }
command -v pip3 >/dev/null || { echo "❌ pip3 required"; exit 1; }

# Clone or update repo
if [ -d ~/memclawz ]; then
    cd ~/memclawz && git pull
else
    cd ~ && git clone https://github.com/yoniassia/memclawz.git && cd memclawz
fi

# Install Python deps
pip3 install -r requirements.txt

# Check Qdrant
if curl -s http://localhost:6333/healthz >/dev/null 2>&1; then
    echo "✅ Qdrant running"
else
    echo "⚠️ Qdrant not running. Starting..."
    if command -v docker >/dev/null; then
        docker run -d --name qdrant -p 6333:6333 -p 6334:6334 \
            -v ~/.openclaw/qdrant-storage:/qdrant/storage \
            --restart unless-stopped qdrant/qdrant
    else
        echo "📥 Downloading Qdrant binary..."
        curl -sL https://github.com/qdrant/qdrant/releases/latest/download/qdrant-x86_64-unknown-linux-musl.tar.gz | tar xz -C ~/memclawz/
        nohup ~/memclawz/qdrant --storage-path ~/.openclaw/qdrant-storage > /tmp/qdrant.log 2>&1 &
    fi
    sleep 3
fi

# Deploy systemd services
mkdir -p ~/.config/systemd/user
cp ~/memclawz/systemd/*.service ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable --now memclawz-api memclawz-watcher

echo "✅ MemClawz v5 installed!"
echo "API: http://localhost:3500/health"
echo "Watcher: systemctl --user status memclawz-watcher"
