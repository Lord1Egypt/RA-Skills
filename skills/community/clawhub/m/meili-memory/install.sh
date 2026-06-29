#!/bin/bash
set -e

echo "=== MeiliSearch Memory Skill Installer ==="

# 1. Install MeiliSearch binary
if ! command -v meilisearch &> /dev/null; then
  echo "Installing MeiliSearch..."
  curl -L https://install.meilisearch.com | sh
  sudo mv ./meilisearch /usr/local/bin/
else
  echo "MeiliSearch already installed: $(meilisearch --version)"
fi

# 2. Generate a master key
MASTER_KEY="ms-$(openssl rand -hex 16)"
echo "Generated master key: $MASTER_KEY"

# 3. Create data directory
sudo mkdir -p /var/lib/meilisearch

# 4. Install systemd service
echo "Installing systemd service..."
cat > /tmp/meilisearch.service << EOF
[Unit]
Description=MeiliSearch
After=network.target

[Service]
Type=simple
ExecStart=/usr/local/bin/meilisearch --http-addr 127.0.0.1:7700 --master-key ${MASTER_KEY} --db-path /var/lib/meilisearch/data.ms
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

sudo cp /tmp/meilisearch.service /etc/systemd/system/meilisearch.service
sudo systemctl daemon-reload
sudo systemctl enable meilisearch
sudo systemctl start meilisearch
sleep 3

if systemctl is-active --quiet meilisearch; then
  echo "MeiliSearch service is running ✅"
else
  echo "MeiliSearch service failed to start ❌"
  exit 1
fi

# 5. Install skill files
SKILL_DIR="${HOME}/.openclaw/workspace/skills/meili-memory"
mkdir -p "${SKILL_DIR}/scripts"
cp scripts/*.sh "${SKILL_DIR}/scripts/"
cp SKILL.md "${SKILL_DIR}/"
chmod +x "${SKILL_DIR}/scripts/"*.sh
echo "Skill files installed to ${SKILL_DIR} ✅"

# 6. Update scripts with the generated key
sed -i "s/ms-323a144af37bf9ab26ddc8bc4edd1b3c/${MASTER_KEY}/g" "${SKILL_DIR}/scripts/search.sh"
sed -i "s/ms-323a144af37bf9ab26ddc8bc4edd1b3c/${MASTER_KEY}/g" "${SKILL_DIR}/scripts/indexer.sh"
echo "Scripts configured with master key ✅"

# 7. Set up cron for hourly indexing
(crontab -l 2>/dev/null | grep -v "meili-memory"; echo "0 * * * * cd ${SKILL_DIR} && bash scripts/indexer.sh >> /tmp/meili-indexer.log 2>&1") | crontab -
echo "Hourly auto-indexing cron job installed ✅"

# 8. Run initial index
echo "Running initial index..."
bash "${SKILL_DIR}/scripts/indexer.sh" 2>&1

echo ""
echo "=== Installation complete ==="
echo "MeiliSearch: http://127.0.0.1:7700"
echo "Skill dir:   ${SKILL_DIR}"
echo "Master key:  ${MASTER_KEY}"
echo ""
echo "To search manually: bash ${SKILL_DIR}/scripts/search.sh 'your query'"
echo "To reindex:         bash ${SKILL_DIR}/scripts/indexer.sh --full"
