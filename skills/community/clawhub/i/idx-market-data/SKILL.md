---
name: idx-market-data
description: Memberikan data pasar saham Bursa Efek Indonesia (IDX) secara real-time dan historis melalui API GoAPI. Gunakan skill ini saat pengguna bertanya tentang harga saham, daftar emiten, indeks pasar, atau profil perusahaan di BEI.
metadata:
  openclaw:
    emoji: "📈"
    requires:
      config:
        - GOAPI_KEY
---

# IDX Market Data (GoAPI)

Skill ini memungkinkan OpenClaw untuk mengakses data pasar modal Indonesia secara langsung.

## Konfigurasi
Pastikan Anda telah memiliki API Key dari [GoAPI.io](https://goapi.io) dan mengaturnya di environment variable:
- `GOAPI_KEY`: API Key Anda dari GoAPI Key Manager.

## Format Autentikasi
**PENTING:** Gunakan query parameter, BUKAN header Authorization.
```
https://api.goapi.io/stock/idx/companies?api_key={GOAPI_KEY}
```

## Endpoint Utama & Penggunaan

### 1. Daftar Emiten (Stocks)
Mendapatkan daftar seluruh perusahaan yang tercatat di bursa.
- **Endpoint**: `/stock/idx/companies?api_key={GOAPI_KEY}`
- **Tujuan**: Mencari kode saham (ticker) atau nama perusahaan.

### 2. Saham Trending & Harga Terbaru
Mendapatkan harga saham terbaru dan yang sedang trending.
- **Endpoint**: `/stock/idx/trending?api_key={GOAPI_KEY}`
- **Output**: Harga close, change (poin & persentase), nama perusahaan
- **Catatan**: Endpoint ini berisi data harga real-time untuk saham aktif

### 3. Data Historis (EOD)
Mendapatkan data harga harian (End of Day).
- **Endpoint**: `/stock/idx/{symbol}/historical?api_key={GOAPI_KEY}`
- **Parameter**: `from` (YYYY-MM-DD), `to` (YYYY-MM-DD)

### 4. Indeks Pasar (IHSG & Lainnya)
Memantau pergerakan indeks.
- **Endpoint**: `/stock/idx/indices?api_key={GOAPI_KEY}`

## Panduan Instruksi Agen
1. **Identifikasi Simbol**: Jika pengguna menyebutkan nama perusahaan (misal: "Telkom"), cari kodenya terlebih dahulu menggunakan endpoint `/companies` sebelum memanggil data harga.
2. **Harga Real-time**: Gunakan endpoint `/trending` untuk mendapatkan harga terbaru saham yang aktif diperdagangkan.
3. **Format Output**: Sajikan data dalam bentuk tabel atau list yang mudah dibaca. Sertakan perubahan harga (dalam poin dan persentase) jika tersedia.
4. **Mata Uang**: Semua harga dalam Rupiah (IDR).
5. **Batasan**: Informasikan kepada pengguna jika API Key tidak valid atau limit kuota tercapai berdasarkan response dari server.

## Contoh Prompt
- "Berapa harga saham BBCA hari ini?"
- "Tampilkan daftar saham yang sedang trending di IDX."
- "Berikan data historis saham ASII selama seminggu terakhir."
- "Cari harga ANTM saat ini"