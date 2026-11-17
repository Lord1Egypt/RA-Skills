# Safety boundaries

## Wallet and funds

P-ACP prepares and verifies unsigned settlement plans. The consuming application owns wallet selection, approval, broadcast, confirmation, and user-visible errors.

Never:

- request, print, store, or load a seed phrase or private key;
- load a local keypair file;
- sign or broadcast a transaction on the user's behalf;
- infer successful payment from plan creation;
- claim funds moved without verified chain evidence;
- replace the selected wallet with a server-side signer.

Always:

- make network, mint, amount, recipient, fee payer, expiry, and nonce explicit;
- show the reviewed plan before wallet approval;
- use a fresh blockhash at approval time when building a live Solana transaction;
- verify recipient and instruction commitments;
- confirm the signature through the application's selected RPC path;
- surface simulation, broadcast, confirmation, and status failures.

## Claims

- Current public settlement support is Solana through `@p-acp/settlement-solana`.
- Do not describe additional settlement rails as implemented unless their adapters and tests exist.
- Do not describe deterministic examples as live commerce.
- Do not expose internal provider, RPC, debug, or secret values in public output.

## Privacy

Encryption does not remove the need for access policy. Bind envelopes and disclosures to explicit sessions, recipients, grants, and expiry. Do not place plaintext sensitive content into journals, receipt commitments, logs, exceptions, or test snapshots.
