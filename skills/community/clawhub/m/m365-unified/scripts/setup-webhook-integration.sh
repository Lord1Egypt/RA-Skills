#!/bin/bash
# M365 Webhook Setup Script for MerkelDesign
# 
# Dieses Script richtet die Webhook-Integration ein:
# 1. Prüft Konfiguration
# 2. Startet den Webhook Handler
# 3. Erstellt Subscription für Inbox-Monitoring
# 4. Richtet Cron-Job für Auto-Renewal ein

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
cd "$SKILL_DIR"

echo "🔔 M365 Webhook Setup für MerkelDesign"
echo "======================================"
echo ""

# 1. Konfiguration prüfen
echo "📋 Prüfe Konfiguration..."
if [ ! -f ".env" ]; then
    echo "❌ .env Datei nicht gefunden!"
    exit 1
fi

WEBHOOK_URL=$(grep "^M365_WEBHOOK_URL=" .env | cut -d'"' -f2)
WEBHOOK_SECRET=$(grep "^M365_WEBHOOK_SECRET=" .env | cut -d'"' -f2)
MAILBOX=$(grep "^M365_MAILBOX=" .env | cut -d'"' -f2)

if [ -z "$WEBHOOK_URL" ]; then
    echo "❌ M365_WEBHOOK_URL nicht in .env konfiguriert!"
    exit 1
fi

echo "   ✅ Webhook URL: $WEBHOOK_URL"
echo "   ✅ Mailbox: $MAILBOX"
echo "   ✅ Secret konfiguriert: ${WEBHOOK_SECRET:0:4}..."
echo ""

# 2. Webhook Handler starten (als Background-Service)
echo "🚀 Starte Webhook Handler..."
if pm2 list | grep -q "m365-webhook"; then
    echo "   ℹ️  Webhook Handler läuft bereits (pm2)"
    pm2 restart m365-webhook
else
    echo "   📦 Starte neuen Handler mit pm2..."
    pm2 start scripts/webhook-handler.js --name m365-webhook
    pm2 save
fi
echo ""

# 3. Bestehende Webhooks prüfen
echo "📋 Bestehende Webhook-Subscriptions..."
node scripts/manage-webhooks.js list
echo ""

# 4. Neue Subscription erstellen (wenn nicht vorhanden)
read -p "🔔 Webhook Subscription für Inbox erstellen? [y/N] " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "   Erstelle Subscription für neue E-Mails in Inbox..."
    
    node scripts/manage-webhooks.js create \
        --resource=mail_inbox \
        --type=created \
        --days=3
    
    echo ""
    echo "✅ Subscription erstellt!"
    echo ""
    echo "⚠️  WICHTIG:"
    echo "   - Webhook läuft lokal auf Port 3000"
    echo "   - Für Production: ngrok oder Reverse Proxy einrichten"
    echo "   - Subscription muss alle 3 Tage erneuert werden (Cron automatisch)"
    echo ""
fi

# 5. Cron-Job für Auto-Renewal einrichten
echo "⏰ Cron-Job für Auto-Renewal einrichten..."
read -p "   Cron-Job hinzufügen? (erneuert Webhooks täglich automatisch) [y/N] " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # Cron-Job hinzufügen (täglich um 2:00 Uhr)
    CRON_CMD="0 2 * * * cd $SKILL_DIR && node scripts/auto-renew-webhooks.js >> /tmp/m365-webhook-renewal.log 2>&1"
    
    if crontab -l 2>/dev/null | grep -q "auto-renew-webhooks"; then
        echo "   ℹ️  Cron-Job existiert bereits"
    else
        (crontab -l 2>/dev/null | grep -v "auto-renew-webhooks"; echo "$CRON_CMD") | crontab -
        echo "   ✅ Cron-Job hinzugefügt"
    fi
    echo ""
fi

echo "✅ Setup abgeschlossen!"
echo ""
echo "📊 Status prüfen:"
echo "   pm2 status m365-webhook"
echo "   node scripts/manage-webhooks.js list"
echo ""
echo "🔧 Nützliche Commands:"
echo "   pm2 logs m365-webhook    # Logs ansehen"
echo "   pm2 restart m365-webhook # Handler neustarten"
echo "   curl http://localhost:3000/health # Health Check"
echo ""
