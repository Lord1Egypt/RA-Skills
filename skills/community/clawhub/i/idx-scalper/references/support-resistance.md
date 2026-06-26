# Support & Resistance untuk Scalping IDX

## Konsep Dasar

Support = Batas bawah harga (lantai)
Resistance = Batas atas harga (atap)

Scalping fokus pada level **terdekat** (nearest S/R), bukan jangka panjang.

## Identifikasi Support & Resistance

### Swing High/Low Method
- **Support:** Lowest point sebelum harga naik
- **Resistance:** Highest point sebelum harga turun
- **Valid:** Minimal 2-3 times tested

### Moving Average Dynamic S/R
- **EMA 9:** Dynamic S/R jangka pendek
- **EMA 20:** Dynamic S/R jangka menengah
- **VWAP:** Fair value intraday

### Round Numbers
- **Contoh:** 100, 500, 1000, 5000, 10000
- **Psikologis:** Sering jadi S/R karena psychological level

## Scalping Entry Strategies

### 1. Buy on Dip (Support Entry)
**Setup:**
- Trend overall bullish (M15)
- Price turun ke support terdekat
- Ada rejection candle (Hammer, Doji)
- Volume konfirmasi

**Entry Point:**
- Agresif: Pas rejection candle
- Konservatif: Pas candle berikutnya konfirmasi hijau

**Stop Loss:** Di bawah support -5-10 points

**Target:** Next resistance atau 1-2% dari entry

### 2. Buy on Breakout (Resistance Entry)
**Setup:**
- Price konsolidasi di resistance
- Volume spike saat tembus
- Close di atas resistance
- ADIP confirmation

**Entry Point:**
- Agresif: Saat breakout candle (risky)
- Konservatif: Pas pullback ke resistance lama (sekarang jadi support)

**Stop Loss:** Di bawah resistance lama -5-10 points

**Target:** 1-2% dari entry atau next resistance

### 3. VWAP Bounce
**Setup:**
- Price menyentuh VWAP
- Ada rejection
- Volume konfirmasi

**Entry Point:**
- Agresif: Pas rejection
- Konservatif: Pas candle berikutnya

**Stop Loss:** 5-10 points di bawah VWAP

**Target:** 1-1.5% dari entry

## Fakeout Detection

### Signs of Fakeout
- Volume spike tapi tidak sustain
- Close kembali di bawah resistance
- ADOS masuk setelah breakout
- Shadow panjang di atas (rejection)

### How to Avoid Fakeout
- Tunggu close candle M5/M15
- Cek volume sustain atau spike sesaat
- Konfirmasi dengan ADIP/ADOS
- Jangan FOMO entry

## Multiple Timeframe S/R

### H1 (Hourly) S/R
- Major support/resistance
- Gunakan untuk target take profit
- Tidak untuk entry scalping

### M15 S/R
- Intermediate level
- Gunakan untuk konfirmasi tren
- Support untuk M5 entry

### M5 S/R
- Minor support/resistance
- Gunakan untuk entry scalping
- Sniping entry point

## Dynamic S/R (Indicators)

### VWAP (Volume Weighted Average Price)
- **Formula:** Cumulative (Price × Volume) / Cumulative Volume
- **Artinya:** Fair value intraday
- **Gunakan:** Dynamic S/R, reversal confirmation
- **Stockbit:** Tersedia di Chartbit

### EMA 9 & 20
- **EMA 9:** Signal momentum pendek
- **EMA 20:** Trend utama
- **Gunakan:**
  - Price di atas EMA 20 = Bullish
  - Price di bawah EMA 20 = Bearish
  - EMA 9 cross EMA 20 = Trend change

### Bollinger Bands
- **Upper Band:** Dynamic resistance
- **Lower Band:** Dynamic support
- **Gunakan:** Reversal saat menyentuh band

## Position Sizing berdasarkan S/R

### Tight Stop Loss (S/R dekat)
- Risk: 1-2%
- Risk:Reward: 1:2-1:3
- Position: Bigger (karena SL dekat)

### Wide Stop Loss (S/R jauh)
- Risk: 2-3%
- Risk:Reward: 1:1.5-1:2
- Position: Smaller (karena SL jauh)

## Practical Example

```
Stock: BBRI | Timeframe: M5
Current: 3750

Support Terdekat: 3720
Resistance Terdekat: 3800
EMA 20: 3700
VWAP: 3745

Setup: Buy on Dip
Entry: 3730 (rejection di support)
CL: 3715 (di bawah support)
Target 1: 3770 (+1.07%)
Target 2: 3800 (+1.88%)
R:R: 1:2.2

Konfirmasi:
- Hammer candle di 3720 ✓
- Volume 1.5x ✓
- ADIP masuk ✓
```

## Warning Signs

❌ Price bouncing di support tapi volume turun = Weak support
❌ Fakeout breakout dengan shadow panjang = Trap
❌ Close di bawah VWAP + volume tinggi = Bearish
❌ Support tested >3x = Breakout risk

## Tips Scalping IDX

- Fokus level **terdekat** (nearest)
- Tunggu **konfirmasi** sebelum entry
- **Fakeout** sering terjadi di IDX
- **VWAP** lebih akurat untuk intraday
- **EMA 9/20** konfirmasi tren
