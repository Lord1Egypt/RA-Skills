# IBKR Connection & Authentication Reference

## Prerequisites

1. Download TWS or IB Gateway from https://www.interactivebrokers.com
2. Enable API in TWS: **Edit → Global Configuration → API → Settings**
   - Check "Enable ActiveX and Socket Clients"
   - Set Socket port: `7497` (paper) or `7496` (live)
   - Uncheck "Read-Only API" if you want to place orders
3. Install `ib_insync`:
   ```bash
   pip install ib_insync
   ```

## Paper vs Live Ports

| Mode | Port |
|------|------|
| TWS Paper Trading | 7497 |
| TWS Live Trading | 7496 |
| IB Gateway Paper | 4002 |
| IB Gateway Live | 4001 |

## Basic Connection Pattern

```python
from ib_insync import IB, util

ib = IB()
ib.connect("127.0.0.1", 7497, clientId=1)

# Always disconnect on exit
try:
    # Your trading logic
    pass
finally:
    ib.disconnect()
```

## Async Pattern (for production loops)

```python
from ib_insync import IB, util

async def main():
    ib = IB()
    await ib.connectAsync("127.0.0.1", 7497, clientId=1)
    # ...
    ib.disconnect()

util.run(main())
```

## Environment Variable Auth (recommended)

Store credentials in `.env`, never hardcode:

```bash
# .env
IBKR_HOST=127.0.0.1
IBKR_PORT=7497
IBKR_CLIENT_ID=1
ENABLE_LIVE_TRADING=false
```

Load with:
```python
import os
from dotenv import load_dotenv
load_dotenv()

host = os.environ["IBKR_HOST"]
port = int(os.environ["IBKR_PORT"])
```

## Reconnection Pattern

```python
def connect_with_retry(ib, host, port, client_id, max_attempts=5):
    for attempt in range(1, max_attempts + 1):
        try:
            ib.connect(host, port, clientId=client_id)
            return True
        except Exception as e:
            print(f"Attempt {attempt} failed: {e}")
            time.sleep(5)
    return False
```

## Common Issues

| Error | Cause | Fix |
|-------|-------|-----|
| `ConnectionRefusedError` | TWS not running | Start TWS/Gateway |
| `clientId already in use` | Duplicate connection | Change clientId or disconnect first |
| `No security definition found` | Bad contract | Use `qualifyContracts()` |
| `Order rejected` | Insufficient margin / permissions | Check paper account balance |
