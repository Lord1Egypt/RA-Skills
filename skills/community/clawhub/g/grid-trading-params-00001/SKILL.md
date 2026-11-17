---
name: grid-trading-params-00001
description: Safely install and run the bundled 00001 Grid Trading Bot in demo or sandbox mode, preview grid parameters, and generate paste-ready key=value or JSON configuration. Use when a user asks to install, start, stop, troubleshoot, or configure the 00001 grid bot, or requests grid levels, ranges, order size, or polling parameters. Never accept credentials in chat or enable live trading.
---

# 00001 Grid Trading Bot

Operate the bundled bot as a local demo lab. This marketplace build supports
exchange demo or sandbox environments only. Do not modify it to use live funds.

The plugin root contains:

```text
bot/
  package.json
  package-lock.json
  server.js
  strategy.js
  config.example.json
  public/
```

## Safety boundaries

- Never request, repeat, store, or display API keys, secrets, passphrases,
  wallet keys, seed phrases, or `.env` contents in chat.
- Tell the user to enter demo credentials only in the local page at
  `http://127.0.0.1:3030`.
- Keep the service bound to `127.0.0.1`. Do not expose it through a tunnel,
  reverse proxy, public firewall rule, or port-forward.
- Keep demo mode enabled. The marketplace build rejects live mode server-side.
- Explain commands before running dependency installation or starting a
  persistent process, then obtain confirmation.
- Show a parameter preview and wait for explicit confirmation before starting
  the strategy.
- Do not promise profit, a win rate, or a safe loss limit.

Credentials remain in process memory and are not written to `config.json`.
Restarting the server requires the user to re-enter them. The stored config
contains only the exchange name, demo mode, and strategy parameters.

## Install and run

1. Check for Node.js 18 or newer and npm.
2. Identify the plugin root from the active skill path.
3. Propose a writable destination, such as a user-selected project directory.
4. After confirmation, copy `bot/` to that destination.
5. In the copied directory, run:

   ```bash
   npm ci
   npm start
   ```

6. Verify that the process reports:

   ```text
   Grid Trading Bot demo: http://127.0.0.1:3030
   ```

7. Ask the user to open the local page themselves and enter demo credentials
   there. Never ask them to paste credentials into the conversation.

Use `PORT=<port> npm start` when port 3030 is unavailable. Continue to bind only
to `127.0.0.1`.

## Parameter workflow

Collect:

- one symbol, such as `BTC/USDT`;
- automatic range percentage or explicit lower and upper prices;
- grid level count from 2 to 50;
- positive amount per order that satisfies the demo exchange minimum;
- polling interval of at least 10,000 milliseconds.

Prefer an automatic range unless the user supplies current, intentional price
bounds. Return multiline `key=value` text:

```text
symbol=BTC/USDT
gridLevels=5
rangePercent=5
amountPerOrder=0.001
intervalMs=60000
```

For a manual range:

```text
symbol=BTC/USDT
gridLevels=5
lowerPrice=50000
upperPrice=60000
amountPerOrder=0.001
intervalMs=60000
```

JSON is also accepted:

```json
{"symbol":"BTC/USDT","gridLevels":5,"rangePercent":5,"amountPerOrder":0.001,"intervalMs":60000}
```

Before start, summarize:

- exchange and explicit demo/sandbox mode;
- symbol;
- automatic or manual range;
- grid levels;
- amount per order;
- polling interval;
- that orders are sent only to the exchange's test environment;
- that results do not predict live performance.

Wait for explicit confirmation. Then direct the user to save the configuration
and press the local page's start button. Report a strategy as running only after
the status endpoint or UI confirms it.

## Stop and troubleshoot

Stopping the strategy cancels only open orders created by the current bot
process. It must not cancel unrelated user orders. Explain that behavior before
stopping and report any cancellation errors.

For failures:

- authentication error: ask the user to verify demo credentials locally;
- network timeout: check ordinary connectivity and an explicitly approved local
  proxy setting;
- invalid range: require `upperPrice > lowerPrice`;
- rejected order: check the demo exchange minimum amount and symbol format;
- port conflict: select another local port.

Do not work around failures by enabling live mode, weakening the localhost
binding, deleting user data, or printing configuration files.
