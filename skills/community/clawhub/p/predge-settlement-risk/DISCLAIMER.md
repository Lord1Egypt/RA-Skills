# Disclaimer

This skill is a decision-support gate. It is a template, not a production trading system, and not financial advice.

## Vendor disclosure

This skill is vendor-authored by Predge (https://predge.io). The facts it returns are UMA's on-chain state on Polygon; Predge reads them through public RPC, labels them and signs the result. Judge its claims accordingly.

## Observe-only

This skill places no orders, real-money or paper. It returns a trade or skip decision and a size multiplier. Whether and how to act is the calling framework's responsibility.

## No validated edge

The gate (skip on a contested resolution, half size during a challenge window or after a fresh bulletin-board update) is a conservative starting point, not a tested edge. It does not estimate the probability of any outcome. The 2026 statistics in SKILL.md describe past Polymarket disputes; they do not predict a given market.

## Data can be late or incomplete

Each record is a chain read at `checked_at`, cached for up to 60 seconds. Public RPC or the Polymarket market index can be slow or unavailable; the gate then fails closed (skip). Bulletin-board kinds come from a text heuristic. An `ok` is not a guarantee that a market will resolve without a dispute.

## Use at your own risk

By using this skill you agree the authors are not liable for any losses, direct or indirect, arising from its use or from the data it surfaces.
