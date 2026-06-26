# Logos Node — Update Procedure (Breaking Release)

> This procedure applies to any release marked **breaking** in the release notes.
> Breaking updates require full re-initialisation: old state is incompatible with
> the new genesis block.

Read [sharp-edges.md](./sharp-edges.md) before starting.

---

## When is an update breaking?

The release notes on GitHub will say:
> "This is a breaking update. Existing node operators will need to delete their node data before rejoining."

If the release does NOT say breaking, you may be able to just swap the binary (check the notes).

---

## Step 0 — Fetch the latest stable release

Fetch the full release list and pick the first **non-prerelease** entry.
`/releases/latest` may return an RC — always filter explicitly:

```bash
curl -s https://api.github.com/repos/logos-blockchain/logos-blockchain/releases \
  | python3 -c "
import sys, json
releases = [r for r in json.load(sys.stdin) if not r['prerelease'] and not r['draft']]
r = releases[0]
print('tag:', r['tag_name'])
for a in r['assets']:
    print('asset:', a['name'], '->', a['browser_download_url'])
print()
print(r['body'][:2000])
"
```

Ignore any tag containing `-rc`, `-dev`, or `-beta`.
If the API is unreachable, check the official quickstart:
`https://github.com/logos-co/logos-docs/blob/main/docs/blockchain/quickstart-guide-for-the-logos-blockchain-node.md`

Note from the response:
- Stable version tag
- Asset URLs for the `linux-x86_64` binary tarball and circuits tarball
- New bootstrap peers (may differ from previous release)
- Whether this is a breaking release

---

## Step 1 — Stop the service

```bash
systemctl stop logos-blockchain-node
systemctl status logos-blockchain-node --no-pager
```

Wait until the service shows `inactive (dead)` before continuing.

---

## Step 2 — Delete old state, config, and circuits

All three paths must be removed. Skipping any one causes genesis mismatch errors.

```bash
rm -rf /pool0/logos/state
rm -f  /pool0/logos/user_config.yaml
rm -rf /pool0/logos/.logos-blockchain-circuits
```

Verify all are gone:
```bash
ls /pool0/logos/
```

Expected: only the old binary tarball(s) and binary file remain — no `state/`, no `user_config.yaml`, no `.logos-blockchain-circuits`.

---

## Step 3 — Download new binary and circuits

Replace URLs with values from the latest release JSON fetched in Step 0.

```bash
su - logos -c '
set -e
cd /pool0/logos

# new binary
curl -L -o logos-blockchain-node-new.tar.gz "<NEW_BINARY_URL>"
tar -xf logos-blockchain-node-new.tar.gz
# the binary will overwrite the old one in-place

# new circuits
curl -L -o logos-blockchain-circuits-new.tar.gz "<NEW_CIRCUITS_URL>"
tar -xf logos-blockchain-circuits-new.tar.gz
mv /pool0/logos/logos-blockchain-circuits-* /pool0/logos/.logos-blockchain-circuits
'
```

Verify the version:
```bash
su - logos -c '/pool0/logos/logos-blockchain-node --version'
```

---

## Step 4 — Re-initialise with the new bootstrap peers

`LOGOS_BLOCKCHAIN_CIRCUITS` must be exported **before** `init`.
Use the peer list from the new release body (it may differ from the previous release).

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

> **Critical**: the peers above are the v0.1.2 bootstrap peers. Always use the peers from the
> **current release body**, not hardcoded values from this file. See SKILL.md Step 0.

After `init` completes, a new wallet key is printed and saved to `user_config.yaml`.
The old wallet key is gone — faucet again if needed.

---

## Step 5 — Restart the service

The systemd unit does not need to be recreated (it uses the same binary path).

```bash
systemctl daemon-reload
systemctl start logos-blockchain-node
systemctl status logos-blockchain-node --no-pager
```

---

## Step 6 — Verify sync

```bash
curl -w "\n" http://localhost:8080/cryptarchia/info
curl -w "\n" http://localhost:8080/network/info
```

Wait until `mode` changes from `Bootstrapping` to `Online`.
If `n_peers` stays at 0 for more than 2 minutes, check:
```bash
ufw status
journalctl -u logos-blockchain-node --no-pager -n 50
```

---

## Checklist

- [ ] Service stopped
- [ ] `/pool0/logos/state` deleted
- [ ] `/pool0/logos/user_config.yaml` deleted
- [ ] `/pool0/logos/.logos-blockchain-circuits` deleted
- [ ] New binary downloaded and verified
- [ ] New circuits downloaded and moved into place
- [ ] `LOGOS_BLOCKCHAIN_CIRCUITS` exported before `init`
- [ ] `init` run with new binary and new peers
- [ ] Service restarted
- [ ] `mode: Online` confirmed
