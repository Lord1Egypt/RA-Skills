# Logos Node — Status Checks

Quick reference for verifying node health at any time.

---

## Service status

```bash
systemctl status logos-blockchain-node --no-pager
```

Expected: `active (running)`.

If `failed` or `inactive`, check logs:
```bash
journalctl -u logos-blockchain-node --no-pager -n 100
```

Common log errors and causes:

| Log line | Cause |
|---|---|
| `StartBlockNotFound` | Binary mismatch — `init` and runtime used different versions |
| `GLIBC_2.38 not found` | OS too old (need glibc ≥ 2.39) |
| `No such file or directory: circuits` | `LOGOS_BLOCKCHAIN_CIRCUITS` not set before `init` |
| `address already in use` | Another process using port 8080 or 3000 |

---

## Consensus info

```bash
curl -s http://localhost:8080/cryptarchia/info | python3 -m json.tool
```

Fields to check:

| Field | Good value | Problem if... |
|---|---|---|
| `mode` | `"Online"` | Still `"Bootstrapping"` after 30+ min → check peers |
| `slot` | Increasing | Not moving → node stalled; restart service |
| `height` | Increasing (slower than slot — normal) | Zero for a long time → sync not starting |
| `lib_slot` | Close to `slot` | Very far behind → still in IBD |

---

## Peer connectivity

```bash
curl -s http://localhost:8080/network/info | python3 -m json.tool
```

Fields to check:

| Field | Good value | Problem if... |
|---|---|---|
| `n_peers` | `> 0` (ideally 5–30) | 0 → firewall or NAT issue |
| `n_connections` | Same as `n_peers` | Mismatched → connection instability |
| `n_pending_connections` | Low or 0 | Very high → P2P storm (usually self-resolves) |

If `n_peers` is 0:
```bash
ufw status                     # is port 3000/udp open?
journalctl -u logos-blockchain-node -f   # look for connection errors
```

---

## Wallet balance

Find your key:
```bash
grep -A3 known_keys /pool0/logos/user_config.yaml
```

Check balance (replace `<key>` with the hex string from config):
```bash
curl -s http://localhost:8080/wallet/<key>/balance | python3 -m json.tool
```

Expected response:
```json
{
  "tip": "8f7523a0...",
  "balance": 1000,
  "notes": { "c73f3f3a...": 1000 },
  "address": "20385ef6..."
}
```

- `balance: 0` after faucet → wait 1–2 minutes and retry
- HTTP 400 `Requested wallet state for unknown block` → node still in IBD; wait for `mode: Online`

---

## Live block stream (optional)

To watch new blocks arrive in real time:
```bash
curl -N http://localhost:8080/cryptarchia/events/blocks/stream
```

Each block event confirms the node is actively participating in the network.

---

## Compare against official dashboard

The Logos team runs a public testnet dashboard (requires auth for full view):
```
https://testnet.blockchain.logos.co/web/
```

You can compare your node's `height` against the dashboard to confirm you are on the same chain.

---

## Day-2 operations

```bash
systemctl restart logos-blockchain-node    # restart
systemctl stop logos-blockchain-node       # stop
journalctl -u logos-blockchain-node -f     # follow live logs
journalctl -u logos-blockchain-node --since "1 hour ago"  # last hour
```
