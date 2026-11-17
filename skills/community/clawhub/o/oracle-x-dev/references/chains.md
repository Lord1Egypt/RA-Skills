# Adding a blockchain

There is no Protocol, no ABC and no decorator registry here. The contract is
duck-typed, enforced by one hand-written dispatcher and by tests. That is worth
knowing before you go looking for a base class to subclass.

## 1. Register the chain

`backend/services/chains/registry.py`. Append a `Chain(...)` to the `CHAINS`
tuple:

```python
@dataclass(frozen=True)
class Chain:
    key: str                    # url-safe id
    name: str
    symbol: str                 # the coin fees are PAID in, not the chain's token
    family: str                 # "evm" | "bitcoin" | "solana" | "tron"
    target_block_seconds: float
    explorer_block_url: str
    rpc_urls: tuple[str, ...] = ()      # tried in order; empty for REST families
    gas_ceiling: bool = True            # False where gasLimit is a sentinel (Arbitrum)
    l1_data_fee: bool = False           # OP-stack: execution fee is only part of the bill
    hash_height_prefix_chars: int = 0   # hex chars of the hash encoding height (TRON: 16)
```

Two derived constants come free: `BY_KEY` and `FEE_SYMBOLS`, which dedupes
symbols so five ETH-settling chains cost one price lookup. **Tuple order is the
board's render order.**

If the chain is EVM, you are almost done — set `family="evm"` and `rpc_urls`,
and the existing adapter handles it.

## 2. Write the adapter, if the family is new

`backend/services/chains/<family>.py`, one `async def fetch_<family>(...)`.
Note that each family has a different signature — the dispatcher passes only
what that family needs:

```python
async def _fetch_one(chain: Chain) -> dict[str, Any]:
    if chain.family == "evm":     return await evm.fetch_evm(chain)
    if chain.family == "bitcoin": return await bitcoin.fetch_bitcoin(chain.target_block_seconds)
    if chain.family == "solana":  return await solana.fetch_solana(chain.rpc_urls, chain.target_block_seconds)
    if chain.family == "tron":    return await tron.fetch_tron()
    raise ValueError(f"no adapter for family {chain.family!r}")
```

The snapshot it returns:

```python
{
  "height": int | None,
  "last_block_at": int | None,          # epoch MILLIseconds
  "block_time_seconds": float | None,
  "cadence_span_seconds": int | None,
  "tx_count": int | None,
  "load": {"percent": float, "basis": "block_fullness"} | None,
  "fee": {"transfer_native": float | None, ...family-specific keys...},
  "blocks": [                            # newest first
    {"height", "hash", "timestamp_ms", "tx_count", "fill_percent"}, ...
  ],
}
```

Optional extras that exist today: `burn_native_per_day` (evm),
`mempool` / `economics` (bitcoin), `throughput` (solana),
`fee.is_fixed` / `fee.free_reason` (tron).

**Raise when the chain cannot be read. Never return a zeroed row.** An
unmeasurable reading is `None`, never `0` — a zero fee and an unmeasured fee
render identically on the board and mean opposite things. `fetch_board()`
gathers adapters with `return_exceptions=True` and turns a raised exception
into `_empty_row(chain, str(exc))`, which is an all-`None` row carrying the
error, so failing loudly is what produces the correct UI.

Pricing is not the adapter's job: `_price_the_fee` adds `fee["transfer_usd"]`
afterwards. Bitcoin is special-cased there because its fee arrives per-vbyte.

## 3. Health

Use `services.http_client.post_json` / `get_json` for the node so the call
lands on the badge, map the RPC hostname to `"onchain"` in
`health_registry._HOST_MAP`, and add the provider name to the `onchain`
category's `providers` tuple. See `upstream.md`.

## 4. Anomaly detection, if it needs any

`backend/services/chains/anomaly.py` holds the detectors — `_fee_flag`,
`_load_flag`, `_fill_trend`, `_mempool_flag`, `_difficulty_flag`,
`_skipped_slots` — listed in two tuples inside `detect`. `history.METRICS`
names what gets sampled for baselines.

Detection is per chain against that chain's own history. A fee level that is
ordinary on one chain is an event on another, which is why there is no shared
global threshold to tune.

## 5. Tests

`backend/tests/test_chains.py::TestRegistry` already asserts that
`{c.family for c in CHAINS}` is a subset of the known families, that keys are
unique, and that EVM and Solana chains carry an RPC URL. **A new family fails
the suite until you widen that set** — which is the intended reminder that the
dispatcher needs a branch too.
