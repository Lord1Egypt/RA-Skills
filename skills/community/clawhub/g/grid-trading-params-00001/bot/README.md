# 00001 Grid Trading Bot — Demo Build

Local grid-strategy lab for exchange demo or sandbox environments.

## Safety properties

- Listens only on `127.0.0.1`.
- Rejects live trading server-side.
- Keeps API credentials in process memory and never writes them to
  `config.json`.
- Cancels only orders created by the current bot process.
- Does not enable CORS or public network access.

Never paste API credentials into chat, commands, screenshots, issues, or logs.
Enter demo credentials only in the local page.

## Run

Requires Node.js 18 or newer:

```bash
npm ci
npm start
```

Open `http://127.0.0.1:3030`. Use `PORT=3031 npm start` if the default port is
unavailable.

The server stores only non-secret settings in `config.json` with owner-only
file permissions. Credentials must be re-entered after a restart.

## Strategy parameters

Automatic range:

```text
symbol=BTC/USDT
gridLevels=5
rangePercent=5
amountPerOrder=0.001
intervalMs=60000
```

Manual range:

```text
symbol=BTC/USDT
gridLevels=5
lowerPrice=50000
upperPrice=60000
amountPerOrder=0.001
intervalMs=60000
```

The strategy requires 2–50 levels, a positive order amount, and an interval of
at least 10 seconds. Demo results do not predict live performance.

Stop from the local page or press `Ctrl+C` in the server terminal. The bot
attempts to cancel only its own open demo orders.
