---
name: osnk-trainer
version: 1.0.2
description: "Pelatih OSNK - Bank soal OSK/OSNK/SNK/Bebras (2006-2025) dengan latihan cerdas, speed run, performance tracking, dan mentoring lengkap."
---

# OSNK Trainer Skill

Skill OpenClaw untuk latihan olimpiade komputer OSNK (Olimpiade Sains Nasional Kompetisi) Informatika dengan fitur pelatihan cerdas.

## Fitur

### Latihan Soal

Dapatkan soal acak dari bank soal dengan berbagai topik dan tingkat kesulitan:

```
openclaw, beri saya 5 soal acak
openclaw, 10 soal teori graf
openclaw, tampilkan soal kombinatorika
openclaw, 5 soal DP dari OSNK 2023
```

### Speed Run Training

Sesi latihan dengan waktu untuk meningkatkan kecepatan dan akurasi:

```
openclaw, mulai speed run 30 menit
openclaw, 20 menit speed run soal PG
openclaw, 45 menit speed run soal essay
```

Scoring:
- Pilihan Ganda: +4 benar, -1 salah, 0 kosong
- Essay: Cek jawaban manual

### Performance Tracking

Lacak progres danidentifikasi area lemah:

```
openclaw, tampilkan statistik saya
openclaw, laporan performa saya
openclaw, topik apa yang lemah?
openclaw, tampilkan kemajuan
```

Metrik yang dilacak:
- Total soal yangdicoba
- Akurasi per kategori
- Waktu per soal
- Trend peningkatan
- Topik kuat/lemah

### Mentoring

Penjelasan dan coaching:

```
openclaw, jelaskan dynamic programming
openclaw, apa itu BFS dan DFS?
openclaw, beri hint untuk soal nomor 3
openclaw, rekomendasi apa yang harus dipelajari
```

### Kategori yang Didukung

- **Computational Thinking** (Bebas-style)
- **Dynamic Programming** (DP)
- **Teori Graf** (BFS, DFS, MST, Shortest Path)
- **Kombinatorika** (Permutasi, Kombinasi)
- **Teori Bilangan** (Prima, Modular, GCD/LCM)
- **Aljabar Boolean** (Gerbang logika, Peta Karnaugh)
- **Analisis Algoritma** (Big O, Kompleksitas)
- **Struktur Data** (Array, Tree, Heap)

## Bank Soal

Bank soal berasal dari kompetisi OSK/OSNK asli:
- **OSK** 2006-2019 (Olimpiade Sains Tingkat Kabupaten/Kota) - ✅ **Baru! Update April 2026**
- **OSNK/SNK** 2022-2025 (Tingkat Provinsi, full database lengkap)
- **KSNK** 2020-2021 (Sistem baru pandemi)
- **Bebras Indonesia & International**

Total: **780+ soal** dengan kunci jawaban dan verifikasi

### Sumber soal:
- OSK: Bank soal dari TLX TOKI (tlx.toki.id)
- Bebras: Berbagai sumber publik internet

### 🤝 Kolaborasi & Update

> **bergabunglah!** Jika Anda menemukan jawaban yang salah atau ingin menambahkan soal baru, fork repo ini dan buat pull request. Dengan bersama-sama memeriksa dan memperbarui, kita dapat membuat resource yang lebih akurat dan berguna bagi semua peserta olimpiade komputer Indonesia.

### ⚠️ Catatan Penting: Kunci Jawaban

> **Perhatian:** Kunci jawaban yang tersedia di bank soal **belum tentu 100% benar**. Beberapa jawaban mungkin salah atau berbeda dengan kunci resmi. 
> 
> **Disarankan:** Untuk memastikan kebenaran, selalu cocokkan dengan:
> - Kunci jawaban resmi dari TLX TOKI
> - Pembahasan dari forum olimpiade
> - Rujukan lain yang terpercaya
>
> Penggunaan skill ini sebagai latihan, tetapi validasi jawaban tetap menjadi tanggung jawab pengguna.

## Penyimpanan Data

Semua data pengguna disimpan secara lokal di workspace Anda:
- Progres: `memory/osnk-progress.json`
- Statistik: `memory/osnk-stats.json`
- Konfigurasi: `memory/osnk-config.json`

Tidak ada informasi pribadi yang dikumpulkan. Semua data bersifat anonim.

## 🔒 Keamanan & Transparansi (April 2026)

Skill ini mencakup dokumen keamanan lengkap **SECURITY.md** yang menjelaskan fungsi shell script `run.sh`:

### Apa yang run.sh lakukan:
- Command routing bash sederhana untuk parsing perintah natural language
- Mengambil soal dari file markdown lokal atau GitHub fallback (opsional)
- Menyimpan statistik performa ke JSON di workspace user

### Yang **TIDAK** dilakukan:
- ❌ Tidak mengeksekusi kode arbitrer
- ❌ Tidak mendownload executable pihak ketiga
- ❌ Tidak mengirim data keluar tanpa izin explisit  
- ❌ Tidak memodifikasi sistem files diluar workspace

Untuk detail teknis lengkap, baca: [`SECURITY.md`](./SECURITY.md)

## Contoh Penggunaan

### Memulai
```
openclaw, mulai pelatihan
openclaw, beri saya 5 soal pemanasan
```

### Latihan Topik Tertentu
```
openclaw, soal tentang rekursi
openclaw, beri saya soal greedy algorithm
openclaw, tampilkan soal graph traversal
```

### Simulasi Kompetisi
```
openclaw, simulasi OSK 2024
openclaw, full 50 soal latihan
```

### Review Kesalahan
```
openclaw, tampilkan jawaban salah saya
openclaw, review soal nomor 10
```

## Detail Teknis

- **Bahasa**: Bash
- **Dependencies**: Tidak ada (bash murni)
- **Penyimpanan**: File JSON di direktori memory
- **API**: Tidak diperlukan (bank soal offline)
- **Path**: Menggunakan `$OPENCLAW_WORKSPACE/memory` jika tersedia, atau fallback ke `./memory`

> **Catatan Path:** Script menggunakan path dinamis untuk kompatibilitas dengan OpenClaw environment. Jika tidak tersedia, akan fallback ke direktori lokal `./memory`.

## Privasi

- Tidak memerlukan akun pengguna
- Tidak ada data dikirim keluar
- Semua progres disimpan secara lokal
- Pelacakan hanya anonim

## Lisensi

MIT

## Kredit

- **Developer**: suluhadi
- **Email**: suluhadi@gmail.com
- **Bank Soal OSK**: TLX TOKI (tofi.or.id)
- **Soal Bebras**: Berbagai sumber publik internet