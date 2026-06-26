#!/bin/bash
# Start M365 Webhook Handler mit korrektem Working Directory

cd /home/claw/.openclaw/workspace/skills/m365-unified
exec node scripts/webhook-handler.js
