# Update Signing (Required)

> Goal: never apply updates without signature verification.

## Generate keypair (Ed25519 via OpenSSL)
```bash
openssl genpkey -algorithm ed25519 -out private_ed25519.pem
openssl pkey -in private_ed25519.pem -pubout -out public_ed25519.pem
```

## Sign artifact
```bash
openssl pkeyutl -sign -inkey private_ed25519.pem -rawin -in pengbo-space.skill -out pengbo-space.skill.sig
```

## Verify artifact
```bash
openssl pkeyutl -verify -pubin -inkey public_ed25519.pem -rawin -in pengbo-space.skill -sigfile pengbo-space.skill.sig
```

## Enforcement policy
1. Client embeds pinned public key(s).
2. Download `artifact + .sig`.
3. Verify signature first.
4. If verify fails: **hard fail** and stop update.
5. Do not fallback to hash-only verification.
