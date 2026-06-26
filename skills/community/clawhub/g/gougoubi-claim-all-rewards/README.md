# Gougoubi Claim All Rewards

Use this skill when the user wants one-click reward claiming for one or more Gougoubi addresses.

Claims:

- winner rewards
- governance rewards
- LP rewards

Best for:

- profile-style fast claim
- claiming across multiple addresses
- re-runnable bulk reward collection

Typical input:

```json
{
  "addresses": ["0x..."],
  "method": "profile"
}
```

Script entry:

- `scripts/pbft-claim-rewards-profile-method.mjs`
- `scripts/pbft-claim-rewards-quick.mjs`
- `node scripts/pbft-claim-rewards-profile-method.mjs --help`
- `node scripts/pbft-claim-rewards-profile-method.mjs --dry-run`
- `node scripts/pbft-claim-rewards-quick.mjs --dry-run`
