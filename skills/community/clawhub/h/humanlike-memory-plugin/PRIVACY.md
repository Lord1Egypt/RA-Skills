# Privacy Policy

Last updated: 2026-04-07

## Overview

Human-Like Memory Plugin ("the Plugin") stores conversation data on remote servers operated by Human-Like.me ("the Service"). This document explains how your data is handled.

## Data Collection

### What We Collect

| Data Type | Purpose | Retention |
|-----------|---------|-----------|
| Conversation content | Memory storage and retrieval | Until deletion requested |
| User identifiers | Memory isolation | Until deletion requested |
| Platform metadata | Cross-platform memory sync | Until deletion requested |
| API request logs | Debugging and abuse prevention | 30 days |

### What We Don't Collect

- Personal information (name, email) unless included in conversations
- Device information
- Location data
- Browsing history

## Data Usage

Your data is used ONLY for:
1. Storing and retrieving memories for your conversations
2. Improving memory retrieval accuracy
3. Debugging technical issues

Your data is NEVER used for:
- Advertising
- Selling to third parties
- Training AI models (unless you opt-in)
- Profiling or behavioral analysis

## Data Isolation

- Each API key has a completely isolated memory space
- Memories are not shared between different API keys
- User IDs are prefixed with API key hash to prevent collisions

## Data Deletion

### Delete All Your Data

```bash
curl -X DELETE "https://plugin.human-like.me/api/plugin/v1/user/data" \
  -H "x-api-key: YOUR_API_KEY"
```

### Delete Specific Memories

```bash
curl -X DELETE "https://plugin.human-like.me/api/plugin/v1/memory/{memory_id}" \
  -H "x-api-key: YOUR_API_KEY"
```

### Account Deletion

Contact support@human-like.me to request complete account deletion.

## Data Security

- All data transmitted via HTTPS (TLS 1.2+)
- Data at rest encrypted with AES-256
- Servers hosted in secure data centers
- Regular security audits

## Third-Party Sharing

We do NOT share your data with third parties except:
- When required by law
- With your explicit consent
- To service providers who assist in operating the Service (under strict confidentiality agreements)

## Children's Privacy

This Service is not intended for users under 13. We do not knowingly collect data from children.

## Changes to This Policy

We will notify users of material changes via:
- Email (if provided)
- Notice on the Service website
- Changelog in new plugin versions

## Contact

For privacy concerns or data requests:
- Email: privacy@human-like.me
- Website: https://plugin.human-like.me/privacy

## Your Rights

You have the right to:
- Access your data
- Correct inaccurate data
- Delete your data
- Export your data
- Withdraw consent

To exercise these rights, contact privacy@human-like.me or use the API endpoints above.
