# ⏰ Cron Jobs — id-emas-pro

Dua cron job untuk skill ini:

| Job | Jadwal | Fungsi |
|-----|--------|--------|
| `emas-alert-check` | Setiap jam (09.00–21.00 WIB) | Cek harga & trigger alert user |
| `emas-morning-brief` | 09.30 WIB setiap hari kerja | Kirim update harga pagi otomatis |

---

## Setup via CLI

### Job 1: Auto-check alert setiap jam

```bash
openclaw cron add \
  --name "emas-alert-check" \
  --cron "0 2-14 * * 1-6" \
  --tz "Asia/Jakarta" \
  --session isolated \
  --message "Jalankan: node ~/.openclaw/workspace/skills/id-emas-pro/scripts/main.js alert check --userId all" \
  --announce \
  --channel telegram
```

> Jadwal `0 2-14 * * 1-6` = jam 02.00–14.00 UTC = 09.00–21.00 WIB, Senin–Sabtu.

### Job 2: Morning brief harga emas

```bash
openclaw cron add \
  --name "emas-morning-brief" \
  --cron "30 2 * * 1-6" \
  --tz "Asia/Jakarta" \
  --session isolated \
  --message "Ambil harga emas hari ini dan kirimkan rangkuman pagi: node ~/.openclaw/workspace/skills/id-emas-pro/scripts/main.js price --brand antam" \
  --announce \
  --channel telegram
```

> Jadwal `30 2 * * 1-6` = 02.30 UTC = 09.30 WIB (tepat setelah Antam update harga).

---

## Verifikasi

```bash
# Lihat semua cron aktif
openclaw cron list

# Test jalankan manual
openclaw cron run <job-id>

# Lihat history run
openclaw cron runs --id <job-id>
```

---

## Hapus / edit jadwal

```bash
# Hapus
openclaw cron remove <job-id>

# Ubah jadwal (misal tiap 30 menit)
openclaw cron update <job-id> --cron "*/30 2-14 * * 1-6"
```

---

## Catatan

- Harga Antam di-update pukul **08.30 WIB** setiap hari kerja — morning brief di 09.30 memastikan data sudah fresh.
- Weekend & libur: logammulia.com tidak update, scraper akan return harga hari kerja terakhir.
- Kalau mau notif ke WhatsApp, ganti `--channel telegram` → `--channel whatsapp`.
