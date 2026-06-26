# Verification Rules

Apply these checks in V1:

1. Require the sender to be in the trusted peer store before accepting a direct message.
2. Verify signatures against the stored public key.
3. Reject envelopes missing `type`, ID, timestamp, sender, or signature.
4. Reject timestamps older than the configured max age.
5. Keep message IDs unique to reduce replay risk.
6. Never trust discovery results alone; trust begins only after explicit approval.
