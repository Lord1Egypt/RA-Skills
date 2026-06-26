#!/usr/bin/env python3
import json
import os
from pathlib import Path


def load_sender_config():
    cfg_path = os.environ.get('OUTREACH_DEMO_CONFIG')
    cfg = {}
    if cfg_path and Path(cfg_path).exists():
        cfg = json.loads(Path(cfg_path).read_text(encoding='utf-8'))
    return {
        'senderAccount': os.environ.get('OUTREACH_SENDER_EMAIL') or cfg.get('senderAccount') or 'you@example.com',
        'senderName': os.environ.get('OUTREACH_SENDER_NAME') or cfg.get('senderName') or 'Your Name',
        'senderTitle': os.environ.get('OUTREACH_SENDER_TITLE') or cfg.get('senderTitle') or 'OpenClaw assistant',
        'senderBrandLine': os.environ.get('OUTREACH_SENDER_BRAND_LINE') or cfg.get('senderBrandLine') or 'Built by Your Company · OpenClaw assistant',
    }
