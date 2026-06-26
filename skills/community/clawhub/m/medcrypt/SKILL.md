# License: MIT © 2026 Erick Adrián Zamora Tehozol / RheumaAI / Frutero Club

# MedCrypt — End-to-End Encryption for Medical Messaging

## Overview
Encrypts patient data (labs, images, clinical notes) with AES-256-GCM before sending through Telegram/WhatsApp. HIPAA/LFPDPPP/GDPR compliant.

## Usage
```bash
pip install cryptography
python medcrypt.py
```

## Protocol
- Key exchange: QR code at first visit → PBKDF2 shared secret
- Format: `[MEDCRYPT:v1:patient_id:nonce_b64:ciphertext_b64:tag_b64]`
- Key rotation: monthly, 7-day backward compatibility
- Emergency: 2-of-3 multisig break-glass

## Threat Model
Compromised server, stolen device, unauthorized group member, legal subpoena → all mitigated by client-side encryption + crypto-shredding.
