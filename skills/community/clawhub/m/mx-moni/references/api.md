# mx-moni API Reference

Read this only when changing `mx_moni.py`, debugging API payloads, or explaining endpoint behavior.

## Base Configuration

- `MX_API_URL`: defaults to `https://mkapi2.dfcfs.com/finskillshub`.
- Auth header: `apikey: ${MX_APIKEY}`.
- Content type: `application/json`; for `newPost`, use `application/json; charset=UTF-8`.

## Endpoints

- `POST /api/claw/mockTrading/positions`: current holdings. Payload: `{"moneyUnit": 1}`.
- `POST /api/claw/mockTrading/balance`: account funds and assets. Payload: `{"moneyUnit": 1}`.
- `POST /api/claw/mockTrading/orders`: current/historical orders. Common payload: `{"fltOrderDrt": 0, "fltOrderStatus": 0}`.
- `POST /api/claw/mockTrading/trade`: buy/sell simulated order. Payload includes `type`, `stockCode`, `quantity`, `useMarketPrice`, and optional scaled integer `price`.
- `POST /api/claw/mockTrading/cancel`: cancel order. Payload is either `{"type": "all"}` or `{"type": "order", "orderId": "...", "stockCode": "..."}`.
- `POST /api/claw/mockTrading/newPost`: publish simulated trading experience post. Payload: `{"text": "..."}`.

## Price Scaling

`mx_moni.py` scales limit prices before sending them:

- Shanghai-style codes beginning with `6` or `9`: 2 decimal places.
- Other supported A-share codes: 3 decimal places.

When the user says "市价", `useMarketPrice` is true and no price should be required.

## Safety Boundaries

- This API is for simulated A-share trading only.
- Do not use it for real brokerage operations, futures, FX, Hong Kong, US stocks, or third-party account management.
- Do not auto-submit broad trade operations from vague wording.
