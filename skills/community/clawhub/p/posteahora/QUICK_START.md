# Quick Start

From zero to a published social post in four steps.

## 1. Install

```bash
npm install -g @posteahora/cli
```

Requires Node.js 18+. The command is `posteahora`.

## 2. Authenticate

Create an API key in PosteAhora → **Settings → API & integrations** (looks like
`pah_live_…`), then:

```bash
posteahora auth --key pah_live_xxxxxxxx
```

## 3. Find your accounts

Publishing targets an account by its ID:

```bash
posteahora accounts
```

```
PLATFORM   USERNAME    ACCOUNT ID    STATUS
instagram  myhandle    a1b2c3d4      connected
twitter    myhandle    e5f6g7h8      connected
```

## 4. Publish

```bash
# Publish now to X and Instagram
posteahora post "Hello from the PosteAhora CLI 👋" \
  --to twitter:e5f6g7h8 --to instagram:a1b2c3d4

# Or schedule it
posteahora post "Morning tip ☕" --to instagram:a1b2c3d4 --at 2026-07-20T09:00:00Z
```

That's it. Check status with `posteahora posts`.

## Next steps

- Attach media: [SUPPORTED_FILE_TYPES.md](SUPPORTED_FILE_TYPES.md)
- Full command list: [README.md](README.md)
- How scheduling & publishing work: [PUBLISHING.md](PUBLISHING.md)
- More examples: [examples/](examples/)
