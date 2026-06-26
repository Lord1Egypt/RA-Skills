# Backblaze B2 (S3-compatible API)

## 1. Create a private bucket

1. Backblaze Console → **B2 Cloud Storage** → **Create a Bucket**
2. Set to **Private**
3. Disable Object Lock unless you need immutable backups

## 2. Create a least-privilege key

1. **App Keys** → **Add a New Application Key**
2. **Restrict to your backup bucket**
3. Allow: `listBuckets`, `listFiles`, `readFiles`, `writeFiles`, `deleteFiles`
4. Note the **keyID** (= access key) and **applicationKey** (= secret key)

## 3. Store the credentials (run this yourself — keep keys out of the chat)

```bash
aws configure --profile openclaw-backup   # paste keyID + applicationKey
chmod 600 ~/.aws/credentials
```

## 4. Configure the skill (non-secret keys only)

```bash
openclaw config patch 'skills.entries.cloud-backup.config.bucket="my-backup-bucket"'
openclaw config patch 'skills.entries.cloud-backup.config.region="us-west-004"'
openclaw config patch 'skills.entries.cloud-backup.config.endpoint="https://s3.us-west-004.backblazeb2.com"'
openclaw config patch 'skills.entries.cloud-backup.config.profile="openclaw-backup"'
```

The region is on the bucket details page and must match the endpoint.

## Credential safety (read me)

- This key can read, write, and DELETE your backups. Treat it like a password.
- Never commit it to git. Never store it in openclaw.json: **backups archive
  openclaw.json itself** — a key stored there rides along inside every archive
  it protects.
- Scope the key to this one bucket where the provider supports it. An
  account-wide key turns one leaked archive into an account takeover.
- Rotate every ~90 days and immediately on any suspicion: create new key →
  update the profile → verify a backup → revoke the old key.

## Notes

- Free tier: 10 GB storage, 1 GB/day egress.
- Bucket-scoped application keys cannot list other buckets — that is the point.
- Rotating the master key revokes ALL application keys.

## Deprecated (v1): keys in OpenClaw config — do not use

v1 documented `skills.entries.cloud-backup.env.ACCESS_KEY_ID/SECRET_ACCESS_KEY`.
It still works in v2 with loud warnings and is removed in v3. Migration:
`references/credentials.md`.
