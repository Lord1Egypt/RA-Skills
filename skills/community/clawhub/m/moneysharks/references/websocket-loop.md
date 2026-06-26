# WebSocket Loop

Use stream inputs when available for:
- market updates
- order updates
- fill updates

Keep reconciliation logic authoritative.
Do not trust stream state without periodic REST reconciliation.
