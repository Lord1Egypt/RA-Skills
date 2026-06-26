# 💼 LinkedIn — Post ke LinkedIn

## When to Use
Gunakan skill ini ketika user meminta untuk:
- Post ke LinkedIn
- Share sesuatu di LinkedIn
- Update status LinkedIn
- "Post LinkedIn: ..."
- "Share ke LinkedIn: ..."
- "LinkedIn post tentang ..."

## How to Use

Jalankan script Python berikut dengan teks post sebagai argumen:

```bash
python3 ~/.openclaw/workspace/linkedin_post.py "<isi post>"
```

### Contoh
```bash
python3 ~/.openclaw/workspace/linkedin_post.py "OpenClaw sekarang bisa auto-post ke LinkedIn 🦀"
```

### Output sukses
```
✅ Post berhasil!
🔗 https://www.linkedin.com/feed/update/urn:li:activity:xxxx
```

### Output gagal
```
❌ Error 401.
```

## Rules
- Maksimal 3000 karakter per post
- Selalu konfirmasi ke user sebelum posting: "Yakin mau post ini ke LinkedIn?"
- Tampilkan link post setelah berhasil
- LinkedIn lebih formal dari Twitter — sesuaikan tone konten
- Kalau user tidak kasih teks, tanya dulu sebelum post
- Hashtag disarankan untuk reach lebih luas

## Tips Konten LinkedIn
- Gunakan line break untuk keterbacaan
- Tambah hashtag relevan di akhir: #AI #Automation #OpenClaw
- Tone profesional tapi tetap personal
- Maksimal 3-5 hashtag biar tidak spammy