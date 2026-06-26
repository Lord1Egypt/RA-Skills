# Logos Node — Sharp Edges

Operational gotchas observed during actual node deployments. Read before every install or update.

---

## 1. `init` binary must match runtime binary

**Problem**: Running `init` with one binary version and then starting the node with a different
version generates an incompatible genesis block. Every subsequent node start fails with:
```
StartBlockNotFound
```

**Rule**: The binary you pass to `./logos-blockchain-node init` and the binary in the systemd
`ExecStart` line must be the **exact same file**.

If you downloaded a new binary, re-run `init` before starting the service.

---

## 2. `LOGOS_BLOCKCHAIN_CIRCUITS` must be exported before `init`

**Problem**: If the env var is not set when `init` runs, the circuits path is not written into
`user_config.yaml`. The node starts but immediately crashes looking for ZK circuits.

**Rule**: Always run:
```bash
export LOGOS_BLOCKCHAIN_CIRCUITS=/pool0/logos/.logos-blockchain-circuits
./logos-blockchain-node init ...
```

The systemd unit sets this var via `Environment=`, but `init` is run manually — you must export it yourself.

---

## 3. Breaking update = delete ALL three paths

A breaking update is not a binary swap. Three separate artifacts must be removed:

| Path | Why |
|---|---|
| `/pool0/logos/state` | Old chain state — incompatible with new genesis |
| `/pool0/logos/user_config.yaml` | Old config — references old genesis hash and old peers |
| `/pool0/logos/.logos-blockchain-circuits` | Old ZK circuits — may not match new proof format |

Missing any one path causes either a genesis mismatch on start or a silent ZK failure.

---

## 4. Ubuntu 22.04 is NOT supported

**Problem**: Ubuntu 22.04 ships `glibc 2.35`. The Logos binary requires `glibc ≥ 2.39`.
The binary will fail to run with:
```
/lib/x86_64-linux-gnu/libc.so.6: version GLIBC_2.38 not found
```

**Rule**: Use Ubuntu 24.04 or Debian 12+. Always check before downloading:
```bash
getconf GNU_LIBC_VERSION
```

---

## 5. ARM is not supported

The official release only ships `linux-x86_64`. There is no `aarch64` / ARM binary.
Do not attempt to run under QEMU emulation — it is too slow for block production timing.

---

## 6. Bootstrap peers change between breaking releases

The bootstrap peer addresses (IP + peer ID) are embedded in `user_config.yaml` during `init`.
They may change with each breaking release. Always use the peer list from the **current release
body** on GitHub, not from this file or any old runbook.

Current v0.1.2 peers:
```
/ip4/65.109.51.37/udp/3000/quic-v1/p2p/12D3KooWFrouXfmrR4nsLMtE7wu15DoMJ6VtoUtHinREZCvbWHar
/ip4/65.109.51.37/udp/3001/quic-v1/p2p/12D3KooWJRGau8M1rjT7R5e4YYsgdFhsMX35nRDtMwCDjxQkXAHz
/ip4/65.109.51.37/udp/3002/quic-v1/p2p/12D3KooWQXJavMDTRscjauFSgVAB1VLB6Rzpy2uY5SU9Tk7927tb
/ip4/65.109.51.37/udp/3003/quic-v1/p2p/12D3KooWSQc7CcGtvWDPF1yCbBthFnQjprfCVHmfmNDUrSmqQsU1
```

---

## 7. Wallet balance returns HTTP 400 during IBD

`GET /wallet/<key>/balance` returns:
```
Requested wallet state for unknown block: ...
```
while the node is still in `Bootstrapping` mode. This is expected — wait for `mode: Online`.

---

## 8. Peer port must be open on the host firewall

The default peer port is `3000/udp`. If `ufw` is active, you must allow it:
```bash
ufw allow 3000/udp
```

If the host is behind NAT, upstream port forwarding for `3000/udp` is also required.

---

## 9. Slot ≠ Block height (many empty slots)

Not every slot produces a block. The `slot` counter increments every 20 seconds regardless.
`height` only increments when a block is produced. During Bootstrapping, `height` may lag far
behind `slot`. This is normal behaviour — not a sign of a stuck node.

---

## 10. RC and devnet binaries cause testnet genesis mismatch

Logos occasionally publishes release candidates (e.g. `0.1.2-rc1`) and devnet binaries. These are
**not compatible** with the public testnet genesis. Only use binaries tagged without `-rc` or `-devnet`
from the releases page for testnet operation.
