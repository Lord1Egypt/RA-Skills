# Logos Node — Install Procedure

> Generated from the official [v0.1.2 release notes](https://github.com/logos-blockchain/logos-blockchain/releases/tag/0.1.2)
> and the citizenweb3 runbook (`logos/docs/logos-testnet-v01-amd64-systemd.md`).
> 
> **Always fetch the latest release first** (SKILL.md Step 0) to get the current
> binary URLs and bootstrap peers before running these commands.

---

## Prerequisites

- Linux `x86_64` (no ARM binary provided)
- `glibc ≥ 2.39` — Ubuntu 22.04 ships 2.35 and is **not supported**
- `≥ 64 GB` free storage
- `curl`, `tar`, `systemctl` available
- Root (or sudo) access for systemd setup

## Step 0 — Verify host compatibility

```bash
uname -m            # must be x86_64
getconf GNU_LIBC_VERSION   # must be >= 2.39
df -h /pool0        # check free space
```

If glibc is too old, upgrade the OS before continuing.

## Step 1 — Create the service user and directories

```bash
apt update
apt install -y curl tar ca-certificates
id -u logos >/dev/null 2>&1 || useradd -m -s /bin/bash logos
install -d -o logos -g logos /pool0/logos /pool0/logos/.logos-blockchain-circuits
```

## Step 2 — Download binary and circuits

Replace `<VERSION>` and `<CIRCUITS_VERSION>` with values from the latest GitHub release response.

```bash
su - logos -c '
set -e
cd /pool0/logos

# node binary
curl -L -o logos-blockchain-node.tar.gz "<BINARY_URL_FROM_RELEASE>"
tar -xf logos-blockchain-node.tar.gz

# ZK circuits
curl -L -o logos-blockchain-circuits.tar.gz "<CIRCUITS_URL_FROM_RELEASE>"
tar -xf logos-blockchain-circuits.tar.gz
rm -rf /pool0/logos/.logos-blockchain-circuits
mv /pool0/logos/logos-blockchain-circuits-* /pool0/logos/.logos-blockchain-circuits
'
```

Verify binary is executable:
```bash
su - logos -c '/pool0/logos/logos-blockchain-node --version'
```

## Step 3 — Initialise node config

`LOGOS_BLOCKCHAIN_CIRCUITS` **must be exported** before running `init`.
The `-p` peers come from the `body` field of the latest GitHub release JSON.

```bash
su - logos -c '
cd /pool0/logos
export LOGOS_BLOCKCHAIN_CIRCUITS=/pool0/logos/.logos-blockchain-circuits
./logos-blockchain-node init \
  -p /ip4/65.109.51.37/udp/3000/quic-v1/p2p/12D3KooWFrouXfmrR4nsLMtE7wu15DoMJ6VtoUtHinREZCvbWHar \
  -p /ip4/65.109.51.37/udp/3001/quic-v1/p2p/12D3KooWJRGau8M1rjT7R5e4YYsgdFhsMX35nRDtMwCDjxQkXAHz \
  -p /ip4/65.109.51.37/udp/3002/quic-v1/p2p/12D3KooWQXJavMDTRscjauFSgVAB1VLB6Rzpy2uY5SU9Tk7927tb \
  -p /ip4/65.109.51.37/udp/3003/quic-v1/p2p/12D3KooWSQc7CcGtvWDPF1yCbBthFnQjprfCVHmfmNDUrSmqQsU1
'
```

> **Critical:** Use the **same binary** for `init` and for runtime. If you run `init` with an RC
> or devnet binary while connecting to testnet peers, the node generates an incompatible genesis
> and every subsequent start fails with `StartBlockNotFound`. See [sharp-edges.md](./sharp-edges.md).

After `init`, a wallet key is printed to stdout and saved to `user_config.yaml`. Save it.

## Step 4 — Create the systemd service

```bash
cat >/etc/systemd/system/logos-blockchain-node.service <<'EOF'
[Unit]
Description=Logos Blockchain Node
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=logos
Group=logos
WorkingDirectory=/pool0/logos
Environment=LOGOS_BLOCKCHAIN_CIRCUITS=/pool0/logos/.logos-blockchain-circuits
ExecStart=/pool0/logos/logos-blockchain-node /pool0/logos/user_config.yaml
Restart=on-failure
RestartSec=10
KillSignal=SIGINT
TimeoutStopSec=30
NoNewPrivileges=true
PrivateTmp=true

[Install]
WantedBy=multi-user.target
EOF
```

## Step 5 — Start the node

```bash
systemctl daemon-reload
systemctl enable logos-blockchain-node
systemctl start logos-blockchain-node
systemctl status logos-blockchain-node --no-pager
```

## Step 6 — Open the peer port

```bash
ufw allow 3000/udp
ufw status
```

## Step 7 — Verify sync

```bash
curl -w "\n" http://localhost:8080/cryptarchia/info
curl -w "\n" http://localhost:8080/network/info
```

Expected progression:
- `mode: Bootstrapping` immediately after start (IBD in progress)
- `mode: Online` after sync completes (minutes to hours depending on chain length)
- `n_peers > 0` means P2P is working

Check slot/height again after 60 seconds — both should be increasing.

## Step 8 — Request faucet tokens

```bash
grep -A3 known_keys /pool0/logos/user_config.yaml
```

Take the hex key and visit the official faucet:
```
https://testnet.blockchain.logos.co/web/faucet/
```

After 1–2 minutes, verify the balance landed:
```bash
curl http://localhost:8080/wallet/<your_key>/balance
```

> Note: balance queries return HTTP 400 while the node is still in `Bootstrapping` mode.

## Step 9 — Wait for stake aging

The node begins participating in block production automatically after roughly 2 epochs
(≈ 3.5 hours) from when the funded wallet key was staked.
