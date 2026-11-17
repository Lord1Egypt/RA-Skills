This is experimental paper-trading software, not a claim of profitability.

All local fills are hypothetical model events. Actual Simmer API receipts refer only to virtual SIM, never pUSD/USDC or real-money orders. Native SIM pricing cannot reproduce Polymarket Maker queue priority. Do not combine the model's P&L, SIM P&L and connection-test transactions.

Real money trading is unavailable in this package. No wallet private key or signing credential is required. Configure only the Simmer API key using the runtime's secret environment. Do not publish it.

Initial policy is one strategy entry window, maximum five model shares, 50 model units of capital and unchanged 6/20 risk limits. Thresholds are valid only for their stated UTC month. All losses and outstanding positions must be included when evaluating results.
