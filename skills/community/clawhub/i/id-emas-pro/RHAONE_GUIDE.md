# 🦞 Rhaone — Operator Guide
> Panduan lengkap setup, deployment, dan operasional skill `id-emas-pro` di OpenClaw

---

## Daftar Isi

1. [Prasyarat](#1-prasyarat)
2. [Struktur File](#2-struktur-file)
3. [Instalasi](#3-instalasi)
4. [Konfigurasi OpenClaw](#4-konfigurasi-openclaw)
5. [Environment Variables](#5-environment-variables)
6. [Perintah Lengkap](#6-perintah-lengkap)
7. [Cron Jobs](#7-cron-jobs)
8. [Testing & Health Check](#8-testing--health-check)
9. [Publish ke ClawHub](#9-publish-ke-clawhub)
10. [Troubleshooting](#10-troubleshooting)
11. [Changelog](#11-changelog)

---

## 1. Prasyarat

| Kebutuhan | Versi | Cek |
|-----------|-------|-----|
| Node.js | `>= 18` | `node --version` |
| OpenClaw Gateway | `>= 1.0.0` | `openclaw --version` |
| clawhub CLI | latest | `clawhub --version` |
| Kimi API Key | — | [platform.moonshot.cn](https://platform.moonshot.cn) |

> **Tidak ada dependensi npm** — skill ini murni Node.js built-ins + native `fetch`.

---

## 2. Struktur File

```
id-emas-pro/
├── SKILL.md                  ← Instruksi untuk LLM (diinjeksi ke system prompt)
├── SKILL.md                  ← Entry point OpenClaw
├── _meta.json                ← Metadata ClawHub (slug, version, tags)
├── package.json              ← "type": "module", no deps
├── test.js                   ← Unit tests (18 test cases)
│
├── config/
│   └── brands.js             ← Daftar brand + tier logic
│
├── scripts/
│   ├── main.js               ← CLI entry — semua command masuk sini
│   ├── scraper.js            ← Multi-brand scraper dengan 3-source fallback
│   ├── alerts.js             ← Alert system
│   ├── storage.js            ← File-based JSON storage untuk alerts
│   ├── cache.js              ← Price cache + stale fallback
│   ├── history.js            ← Histori harga harian + ASCII chart
│   ├── health.js             ← Health check semua scraper
│   ├── portfolio.js          ← Portfolio tracker + P&L
│   └── ai-analysis.js        ← Integrasi Kimi 2.5
│
├── utils/
│   └── retry.js              ← Exponential backoff utility
│
└── .data/                    ← Auto-generated, jangan di-commit
    ├── alerts.json           ← Data alert per user
    ├── cache.json            ← Cache harga terakhir per brand
    ├── history.json          ← Histori harga harian
    └── portfolio.json        ← Data portfolio per user
```

---

## 3. Instalasi

### Opsi A — Via ClawHub (Rekomendasi)

```bash
clawhub install id-emas-pro
```

### Opsi B — Manual

```bash
# Clone ke workspace OpenClaw
git clone <repo-url> ~/.openclaw/workspace/skills/id-emas-pro

# Atau copy folder
cp -r id-emas-pro ~/.openclaw/workspace/skills/
```

### Verifikasi instalasi

```bash
openclaw skills list
# Harus muncul: id_emas_pro
```

---

## 4. Konfigurasi OpenClaw

Tambahkan ke `~/.openclaw/openclaw.json`:

```json
{
  "env": {
    "KIMI_API_KEY": "sk-xxxxxxxxxxxxxxxxxxxx"
  },
  "tools": {
    "allow": ["exec", "group:fs"]
  },
  "agents": {
    "list": [
      {
        "id": "rhaone",
        "name": "Rhaone",
        "model": "moonshot-v1-8k",
        "tools": {
          "profile": "coding"
        }
      }
    ]
  }
}
```

Reload config tanpa restart:

```bash
# Simpan file → hot-reload otomatis (hybrid mode)
# Atau force restart:
openclaw gateway restart
```

---

## 5. Environment Variables

| Variable | Wajib | Keterangan |
|----------|-------|------------|
| `KIMI_API_KEY` | Tier AI saja | API key dari platform.moonshot.cn |

Set via `openclaw.json` (direkomendasikan) atau shell:

```bash
export KIMI_API_KEY="sk-xxxx"
```

---

## 6. Perintah Lengkap

> Semua perintah dijalankan dari dalam direktori skill:
> ```bash
> cd ~/.openclaw/workspace/skills/id-emas-pro
> ```

### Harga

```bash
# Cek harga satu brand
node scripts/main.js price --brand antam
node scripts/main.js price --brand pegadaian
node scripts/main.js price --brand treasury

# Bandingkan semua brand (sesuai tier)
node scripts/main.js compare --tier free
node scripts/main.js compare --tier pro
node scripts/main.js compare --tier ai
```

### Histori

```bash
# Histori 7 hari (default)
node scripts/main.js history --brand antam

# Histori 30 hari
node scripts/main.js history --brand antam --days 30
```

### Alert

```bash
# Buat alert: beritahu kalau harga BELI Antam naik di atas 3 juta
node scripts/main.js alert set \
  --userId <userId> \
  --brand antam \
  --condition above \
  --price 3000000 \
  --type buy

# Buat alert: beritahu kalau harga JUAL turun di bawah 2.7 juta
node scripts/main.js alert set \
  --userId <userId> \
  --brand antam \
  --condition below \
  --price 2700000 \
  --type sell

# Lihat semua alert aktif
node scripts/main.js alert list --userId <userId>

# Hapus alert
node scripts/main.js alert delete --userId <userId> --id <alertId>

# Cek semua alert (dipakai oleh cron)
node scripts/main.js alert check --userId all
```

### Portfolio

```bash
# Tambah pembelian emas
node scripts/main.js portfolio add \
  --userId <userId> \
  --brand antam \
  --grams 5 \
  --buyPrice 2800000 \
  --buyDate 2026-03-01

# Lihat portfolio + P&L
node scripts/main.js portfolio show --userId <userId> --tier free

# Hapus entry
node scripts/main.js portfolio remove --userId <userId> --id <entryId>
```

### AI Analisis

```bash
# Analisis harga + histori 30 hari via Kimi 2.5 (tier AI)
KIMI_API_KEY=sk-xxx node scripts/main.js ai-analysis \
  --tier ai \
  --brand antam \
  --days 30
```

### Health Check

```bash
node scripts/main.js health
# atau
npm run health
```

Contoh output:

```
🏥 Health Check — 27/3/2026, 09.30.00
   Mengecek 5 brand...

✅ Logam Mulia Antam         Rp 2.850.000   823ms  [emasantam.id]  (cache: 2h)
✅ Pegadaian (Galeri24)      Rp 2.827.000  1204ms  [sahabat.pegadaian.co.id]  (no cache)
✅ Treasury                  Rp 2.841.000   991ms  [treasury.id]  (cache: 5h)
❌ Tamasia                   GAGAL  15001ms
   Error   : Timeout 15s
   Cache   : fallback cache tersedia (8h lalu)
✅ BRI Mas Gold              Rp 2.950.000   831ms  [estimasi]  (cache: 2h)
   ⚠️  Harga BRI adalah estimasi, konfirmasi ke aplikasi BRImo

────────────────────────────────────────────────────────────
Hasil: 4/5 OK, 1 gagal
```

### Unit Tests

```bash
npm test
# atau
node test.js
```

---

## 7. Cron Jobs

### Setup (jalankan sekali)

```bash
# Job 1 — Cek alert setiap jam (09.00–21.00 WIB, Senin–Sabtu)
openclaw cron add \
  --name "emas-alert-check" \
  --cron "0 2-14 * * 1-6" \
  --tz "Asia/Jakarta" \
  --session isolated \
  --message "node ~/.openclaw/workspace/skills/id-emas-pro/scripts/main.js alert check --userId all" \
  --announce \
  --channel telegram

# Job 2 — Morning brief 09.30 WIB (setelah Antam update harga)
openclaw cron add \
  --name "emas-morning-brief" \
  --cron "30 2 * * 1-6" \
  --tz "Asia/Jakarta" \
  --session isolated \
  --message "node ~/.openclaw/workspace/skills/id-emas-pro/scripts/main.js price --brand antam" \
  --announce \
  --channel telegram
```

### Manajemen cron

```bash
# Lihat semua cron aktif
openclaw cron list

# Test jalankan manual
openclaw cron run <job-id>

# Lihat log run terakhir
openclaw cron runs --id <job-id>

# Pause sementara
openclaw cron update <job-id> --enabled false

# Hapus
openclaw cron remove <job-id>
```

### Jadwal referensi (WIB = UTC+7)

| Jadwal | Cron Expression | Keterangan |
|--------|----------------|------------|
| Setiap jam (jam kerja) | `0 2-14 * * 1-6` | 09.00–21.00 WIB Senin–Sabtu |
| Pagi 09.30 | `30 2 * * 1-6` | Setelah Antam update (08.30 WIB) |
| Setiap 30 menit | `*/30 2-14 * * 1-6` | Untuk Pro/AI tier lebih responsif |

---

## 8. Testing & Health Check

### Urutan test saat pertama setup

```bash
# 1. Test unit
npm test

# 2. Test scraper satu per satu
node scripts/scraper.js antam
node scripts/scraper.js pegadaian
node scripts/scraper.js treasury

# 3. Health check komprehensif
npm run health

# 4. Test full flow
node scripts/main.js price --brand antam
node scripts/main.js compare --tier free
node scripts/main.js history --brand antam --days 7
```

### Interpretasi health check

| Status | Arti | Aksi |
|--------|------|------|
| `✅ [source]` | Scraper OK, data fresh | — |
| `✅ [cache:brand]` | Data dari cache (stale) | Cek koneksi ke situs |
| `❌ Timeout` | Situs lambat/down | Tunggu, atau cek `cache` untuk fallback |
| `❌ Cloudflare` | IP diblokir | Coba dari IP/lokasi berbeda |
| `❌ no cache` | Scraper gagal + tidak ada cache | Urgent — data tidak tersedia sama sekali |

---

## 9. Publish ke ClawHub

```bash
cd ~/.openclaw/workspace/skills/id-emas-pro

# Login (sekali)
clawhub login

# Publish / update versi
clawhub publish

# Verifikasi live
clawhub search "emas indonesia"
```

### Konvensi versioning

| Perubahan | Bump |
|-----------|------|
| Bug fix scraper, tweak minor | `1.x.PATCH` |
| Fitur baru (brand, command) | `1.MINOR.0` |
| Breaking change struktur file | `MAJOR.0.0` |

Edit `_meta.json` → field `"version"` → `clawhub publish`.

---

## 10. Troubleshooting

### Scraper gagal semua

```bash
# 1. Cek koneksi
curl -I https://emasantam.id

# 2. Cek apakah ada data cache
cat .data/cache.json

# 3. Cek log error detail
node scripts/scraper.js antam 2>&1
```

### Skill tidak terdeteksi OpenClaw

```bash
# Cek lokasi skill
ls ~/.openclaw/workspace/skills/id-emas-pro/SKILL.md

# Reload
openclaw gateway restart
openclaw skills list
```

### Alert tidak trigger

```bash
# Test manual check
node scripts/main.js alert list --userId <userId>
node scripts/main.js alert check --userId <userId>

# Pastikan cron aktif
openclaw cron list
```

### KIMI_API_KEY tidak terbaca

```bash
# Verifikasi env terbaca
node -e "console.log(process.env.KIMI_API_KEY ? 'OK' : 'TIDAK ADA')"

# Kalau tidak ada, set di openclaw.json:
# { "env": { "KIMI_API_KEY": "sk-xxx" } }
```

### Cache expired / data sangat lama

```bash
# Hapus cache lama, force scrape ulang
rm .data/cache.json
node scripts/main.js health
```

---

## 11. Changelog

| Versi | Perubahan |
|-------|-----------|
| `1.3.0` | Cache + stale fallback, histori harga, health check, retry backoff, portfolio tracker, AI konteks histori, 18 unit tests |
| `1.2.0` | Scraper Pegadaian, Treasury, Tamasia, BRI. Cron job support |
| `1.1.0` | Cron auto-check alert. Support `--userId all` |
| `1.0.0` | Initial release — Antam scraper, alert system, Kimi 2.5 AI |

---

*Rhaone — powered by OpenClaw + Kimi 2.5 · skill: id-emas-pro · by @Rhaone21*
