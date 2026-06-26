# Örnek 6 Aylık Nakit Akış Tablosu ve Runway Hesaplama

> Kaynak: Şirket 101 — Tech Consulting (techsmmm.com)

## Temel Nakit Akış Tablosu (Örnek)

### Gelirler / Nakit Girişleri (TL)

| Kalem | Ocak | Şubat | Mart | Nisan | Mayıs | Haziran |
|-------|------|-------|------|-------|-------|---------|
| Mevcut sermaye / yatırım | 200.000 | — | — | — | — | 100.000 |
| Satış ve tahsilatlar | 50.000 | 60.000 | 90.000 | 120.000 | 80.000 | 100.000 |
| Hibe / destek (KOSGEB vb.) | — | 50.000 | — | — | — | — |
| **Toplam Nakit Girişi** | **250.000** | **110.000** | **90.000** | **120.000** | **80.000** | **200.000** |

---

### Giderler / Nakit Çıkışları (TL)

| Gider Kalemi | Ocak | Şubat | Mart | Nisan | Mayıs | Haziran |
|-------------|------|-------|------|-------|-------|---------|
| Personel Maaşları (3 kişi) | 90.000 | 90.000 | 90.000 | 90.000 | 90.000 | 90.000 |
| SGK Primleri | 15.000 | 15.000 | 15.000 | 15.000 | 15.000 | 15.000 |
| Kira + Ofis Giderleri | 20.000 | 20.000 | 20.000 | 20.000 | 20.000 | 20.000 |
| Yazılım / Bulut / Domain Lisansları | 10.000 | 12.000 | 12.000 | 12.000 | 12.000 | 12.000 |
| Ar-Ge / Donanım Alımları | 40.000 | 20.000 | 40.000 | 20.000 | 30.000 | 50.000 |
| Vergiler (KDV, Muhtasar, Damga, KDV2) | 15.000 | 8.000 | 25.000 | 5.000 | 20.000 | 25.000 |
| Eğitim / Danışmanlık / Hukuki Giderler | 5.000 | 5.000 | 5.000 | 5.000 | 5.000 | 5.000 |
| Ofis Malzeme / Kırtasiye / Genel Gider | — | — | — | — | 5.000 | 5.000 |
| **Toplam Aylık Nakit Çıkışı** | **195.000** | **170.000** | **207.000** | **167.000** | **177.000** | **222.000** |

---

### Net Nakit Değişimi

| | Ocak | Şubat | Mart | Nisan | Mayıs | Haziran |
|-|------|-------|------|-------|-------|---------|
| **Net Nakit (Giriş – Çıkış)** | **+55.000** | **-60.000** | **-117.000** | **-47.000** | **-97.000** | **-22.000** |

---

## Runway Hesaplama

> **Runway:** Şirketin mevcut nakitle kaç ay dayanabileceği.

### Formül

```
Runway (ay) = Mevcut Nakit / Aylık Ortalama Gider
```

### Örnek Hesaplama

```
Mevcut Nakit: 500.000 TL
Aylık Ortalama Gider: 180.000 TL
Runway = 500.000 / 180.000 = ~2,7 ay
```

Bu örnekte şirketin yeni gelir gelmese **2,7 ay** dayanabileceği görülmektedir.

---

## Nakit Akış Tablosunu Kullanma Rehberi

### Adım 1: Nakit Girişlerini Tahmin Et
- Vadeli satışlarda tahsilat tarihini kullan, fatura tarihini değil
- Hibe ve yatırım gelirlerini yalnızca onay alındıktan sonra ekle
- Muhafazakâr tahmin yap (iyimser değil)

### Adım 2: Sabit Giderleri Belirle
- Maaş, SGK, kira: kesin tutarlar
- Vergi ve SGK için aylık cironun **%15–20'sini** rezerv olarak ayır

### Adım 3: Değişken Giderleri Tahmin Et
- Proje bazlı harcamalar
- Sezonsal değişkenler

### Adım 4: Haftalık Bazda İzle
- Aylık tablo yeterli değil; **haftalık nakit pozisyonu** takip edilmeli
- Her hafta "gelecek hafta çıkış – elde nakit" farkı hesaplanmalı

### Adım 5: Erken Uyarı Eşiği Belirle
- Örnek: Nakit **2 aylık giderin altına** düştüğünde alarm ver
- Bu noktada tahsilat hızlandır, harcamaları ertele veya finansman ara

---

## Vergi Rezervi Hesaplama Rehberi

| Beyan Türü | Rezerv Önerisi |
|-----------|----------------|
| KDV (net ödenecek) | Aylık net KDV tahmini |
| Muhtasar (stopaj) | Brüt maaş × %15 civarı |
| SGK işveren payı | Brüt maaş × ~%22 |
| Geçici Vergi (3 ayda bir) | Tahmini dönem kârı × vergi oranı |
| **Toplam Rezerv Önerisi** | **Aylık cironun %15–20'si** |

---

> **Kaynak:** Şirket 101 — Tech Consulting (techsmmm.com)
