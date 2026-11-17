# MLB Live Trader Disclaimer

MLB Live Trader is experimental software for evaluating and, only after an explicit `--live` opt-in, trading prediction-market contracts. It is not financial, investment, legal, tax, or gambling advice. No return, win rate, calibration quality, or profitability claim is made.

Prediction-market contracts can lose their entire purchase price. Market prices, liquidity, fees, settlement rules, API responses, external sports data, and local laws can change. ESPN's public feeds are undocumented and may lag, omit, revise, or misidentify plays. Simmer and its connected venues may reject, partially fill, delay, or fail orders.

Paper results do not establish live performance. Before risking funds:

- review the market's exact resolution rules and your local legal obligations;
- run paper mode over a meaningful out-of-sample period;
- measure data latency, probability calibration, spread, fees, fill quality, and drawdown;
- keep per-order and daily limits at amounts you can afford to lose;
- supervise the first live runs and verify positions independently.

The included safeguards reduce specific implementation risks but cannot prevent every loss, feed error, venue failure, software defect, account compromise, or operator mistake. Passing `--no-safeguards` removes the optional Simmer context check in paper mode only; live mode always requires that context.

The live process lock coordinates only instances that use the same state path on a lock-capable filesystem. Multiple hosts or containers using one Simmer account must share `SIMMER_MLB_STATE_PATH` and one scheduler; independent local files cannot enforce an account-wide budget.

Before first live use, the explicit initialization workflow checks the entire Polymarket account through a read-only SDK client. Any returned position or trade receipt from the prior 96 hours blocks empty initialization, including activity from another strategy. This conservative check cannot make an uncoordinated older scheduler atomic with the new process: stop all older writers before initialization. There is no force flag. Missing central state alongside an initialization marker or migrated snapshot requires deliberate restoration or reconciliation.

Keep API keys and wallet material in an environment-managed secret store. Never commit them, paste them into logs or issue reports, or place them in `config.json`.

Use this software at your own risk. The GitHub source is distributed under its repository license. ClawHub applies its own registry license terms to published skill versions.
