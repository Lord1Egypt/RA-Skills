# Setup — Configure Mag3nt Credentials

Before making any payments, the agent needs valid credentials.

## Environment Variables

Set the following in your `.env` or export them:

```bash
# Your Mag3nt API key (starts with mag3nt_live_)
MAG3NT_API_KEY=mag3nt_live_your_api_key_here

# Your Mag3nt card credentials (the agent's spending card)
# Card IDs use the mag3nt_ prefix (e.g. mag3nt_c40e2847-...)
# Legacy sx_ card IDs are also supported for backward compatibility
MAG3NT_CARD_ID=mag3nt_your-card-uuid
MAG3NT_CARD_TOKEN=tok_your-card-token
```

## Verify Connection

Test that the credentials work by listing cards:

```bash
node -e "
fetch('https://mag3nt.com/api/cards', {
  headers: { Authorization: 'Bearer ' + process.env.MAG3NT_API_KEY }
})
.then(r => r.json())
.then(data => {
  const card = data.cards.find(c => c.id === process.env.MAG3NT_CARD_ID);
  if (!card) { console.error('Card not found'); process.exit(1); }
  console.log('Status:', card.status, '| Remaining:', card.remaining, 'USDC | Spent:', card.balance, 'USDC');
  console.log('Network:', card.funding_network, '| Protocols:', card.accepted_protocols);
})
.catch(e => console.error('Error:', e.message));
"
```

If this returns the card status and balance, you are ready to pay.

## API Reference

- **Base URL:** `https://mag3nt.com`
- **Auth header:** `Authorization: Bearer mag3nt_live_...`
- **List cards:** `GET /api/cards` — returns `{ cards: [...] }`
- **Treasury balance:** `GET /api/balance` — returns `{ available, total_funded, ... }`
- **Universal pay:** `POST /api/pay` — auto-detects protocol and settles
- **Pay Link settle:** `POST /api/pay/{code}/settle` — no API key required
