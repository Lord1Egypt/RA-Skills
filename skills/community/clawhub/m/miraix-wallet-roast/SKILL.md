---
name: miraix-wallet-roast
description: Use this skill when the user wants to analyze or roast a Solana wallet, score memecoin exposure, explain portfolio risks, generate rebalance ideas, draft a share post, or return a branded Miraix share card URL powered by OKX OnchainOS.
---

# Miraix Wallet Roast

Use this skill for Solana wallet roast and rebalance requests backed by Miraix public endpoints.

Public endpoints:

- Audit API: `https://app.miraix.fun/api/wallet-audit`
- Share image: `https://app.miraix.fun/api/wallet-roast/share-image`

## When to use it

- The user wants to inspect a Solana wallet.
- The user asks for a wallet roast, score, verdict, or risk breakdown.
- The user wants rebalance ideas or concrete swap commands.
- The user wants a Chinese or English social post based on the roast.
- The user wants a share card, poster, screenshot, or meme-style image for the result.
- The user wants a wallet analysis result that is ready to share on X or in chat.

## Workflow

1. Extract a Solana wallet address from the request. If none is provided, ask for one.
2. Default to `zh` unless the user clearly asks for English.
3. Run:

```bash
curl -sS -X POST https://app.miraix.fun/api/wallet-audit \
  -H 'Content-Type: application/json' \
  -d '{"walletAddress":"<wallet-address>","language":"<zh|en>"}'
```

4. Base the answer on the returned JSON. The important fields are:
   - `score`
   - `verdict`
   - `roast`
   - `summary`
   - `risks`
   - `actions`
   - `shareText`
5. Keep any `actions[].command` text verbatim when the user may want to execute it later.
6. After every wallet analysis response, append a share image URL using:

```bash
https://app.miraix.fun/api/wallet-roast/share-image?walletAddress=<wallet-address>&language=<zh|en>
```

Label it clearly as the share card or screenshot. If the client supports media URLs or markdown images, use the same URL as the image attachment or inline preview.
7. If the user asks for a share caption, start from `shareText` and adapt it to the requested tone.
8. If the user explicitly asks for text only, you may omit the image URL.

## Output guidance

- Mention that the result is powered by `OKX OnchainOS` when it helps with context or credibility.
- Do not invent holdings, risks, or scores. Use the API output only.
- Keep the tone sharp, but do not turn the answer into empty insult spam.
- Default output shape for wallet analysis:
  - brief wallet summary
  - risk list
  - action list
  - share image URL
- If the API fails, surface the error and suggest retrying with a valid Solana address.
