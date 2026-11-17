# Optional AI Media Setup

The original Miao Vision report, poster, deck, article, and validation workflows remain local and work on Node.js 20 without ai-cli. Only optional image/video generation requires Node.js 22 or newer, ai-cli, a Vercel AI Gateway account, and separate usage charges.

## Enable Once

1. Install or select Node.js 22+.
2. After the user explicitly approves installation, run `npm install -g ai-cli`. Never install automatically.
3. Ask the user to create a Vercel AI Gateway key and set `AI_GATEWAY_API_KEY` in their own environment.
4. Ask them to restart or re-enter the Agent environment so it inherits the variable.
5. Verify with `node scripts/check-ai-media.mjs image` or `video`. Do not use a paid generation request as a configuration test.

Never ask the user to paste the Key. Do not read, print, copy, persist, or pass its value in command arguments. Do not write it to the repository or a repository `.env`. Supplier-direct keys are not part of the supported first release.

## Price and Data Notice

Vercel AI Gateway bills according to its live model catalog and does not add a platform markup. Present catalog pricing as informational text, not a guaranteed exact charge. Do not enable or change automatic recharge. Every remote generation needs confirmation; one confirmation covers only the displayed media kinds, quantities, tiers, prompts, and references.

The configured GPT Image 2 and Seedance 2.0 routes currently do not provide Zero Data Retention. Do not upload sensitive raw data. Send only the minimum aggregate story and approved visual references. Refer users to the live Gateway model pages for current pricing, retention, and availability.

If ai-cli, Node.js 22, the Key, the model, balance, or service is unavailable, report the structured media error and continue offering all original Miao Vision workflows.
