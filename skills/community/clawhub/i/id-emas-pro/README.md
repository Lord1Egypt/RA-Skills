# id-emas-pro 🥇

Skill OpenClaw untuk cek harga emas Indonesia real-time.

## Instalasi

```bash
# Via ClawHub
clawhub install id-emas-pro

# Manual
git clone <repo> ~/.openclaw/workspace/skills/id-emas-pro
```

## Setup

1. Tidak ada dependensi npm — pure Node.js built-ins + native fetch (Node 18+)
2. Untuk fitur AI, set environment variable:

```json
# Di openclaw.json
{
  "env": {
    "KIMI_API_KEY": "sk-..."
  }
}
```

3. Restart gateway: `openclaw gateway restart`

## Penggunaan

| Perintah | Deskripsi | Tier |
|----------|-----------|------|
| `/emas` | Harga emas hari ini | Free |
| `/emas compare` | Bandingkan semua brand | Free |
| `/emas alert set` | Set alert harga | Pro |
| `/emas alert list` | Lihat alert aktif | Pro |
| `/emas alert delete` | Hapus alert | Pro |
| `/emas ai` | Analisis AI Kimi 2.5 | AI |

## Struktur

```
id-emas-pro/
├── SKILL.md              ← Entry point OpenClaw (diinjeksi ke system prompt)
├── _meta.json            ← Metadata ClawHub
├── package.json
├── config/
│   └── brands.js         ← Daftar brand & tier logic
├── scripts/
│   ├── main.js           ← CLI entry point (dipanggil via exec tool)
│   ├── scraper.js        ← Web scraping logammulia.com
│   ├── alerts.js         ← Alert system
│   ├── storage.js        ← File-based JSON storage
│   └── ai-analysis.js    ← Integrasi Kimi 2.5
└── .data/                ← Auto-generated, data runtime (gitignore)
    └── alerts.json
```

## Test Manual

```bash
# Test scraping
node scripts/main.js price --brand antam

# Test compare
node scripts/main.js compare --tier free

# Test alert
node scripts/main.js alert set --userId test --brand antam --condition above --price 1300000 --type buy
node scripts/main.js alert list --userId test

# Test AI (butuh KIMI_API_KEY)
KIMI_API_KEY=sk-xxx node scripts/main.js ai-analysis --tier ai
```

## Catatan

- Scraper target: logammulia.com — kalau situs berubah struktur, update scraper.js
- Data alert disimpan di `.data/alerts.json` (per-skill, bukan per-user global)
- Tidak ada dependensi eksternal — semua pakai Node.js built-ins + native fetch
