# Registry

The registry is the single source of truth for:

- the active production-candidate validation chain: Base
- the reviewed historical empty-scope chain: BSC
- Morpho singleton address
- approved markets and market IDs
- allowed adapters and selectors
- risk limits including max single move, max daily move, and idle buffer

Do not derive mutable write targets from live market discovery.
