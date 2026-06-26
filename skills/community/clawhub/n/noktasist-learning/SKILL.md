---
name: self-learning
description: Noktasist için sürekli öğrenme ve kendini geliştirme skill'i
---

# Self-Learning Skill

Bu skill, Noktasist'in sürekli kendini geliştirmesi için rehberlik sağlar.

## Temel Prensip

**Her hata bir ders, her çıktı bir veri, her dosya bir keşif.**

## Öğrenme Protokolü

### 1. Yeni bir sistem keşfettiğinde
1. Sistemin ne yaptığını anla (read the code/docs)
2. Konfigürasyonu not et (MEMORY.md'ye yaz)
3. Nasıl çalıştığını test et (exec ile kontrol)
4. Deneyimlerini memory/YYYY-MM-DD.md'ye logla

### 2. Bir hata ile karşılaştığında
1. Hata mesajını tam olarak oku
2. Log dosyalarını incele
3. Çözümü bul ve uygula
4. Çözümü MEMORY.md'ye yaz (nasıl çözdüğünü)

### 3. Yeni bir tool/özellik keşfettiğinde
1. Dokümantasyonu oku (docs/tools/, docs/concepts/)
2. Basit bir test yap
3. Kullanım senaryosu bul
4. TOOLS.md veya MEMORY.md'ye ekle

## Zorunlu Güncellemeler

Her önemli öğrenmeden sonra şu dosyaları güncelle:

| Durum | Güncelle |
|-------|----------|
| Yeni sistem bilgisi | MEMORY.md |
| Günlük aktivite | memory/YYYY-MM-DD.md |
| Yeni tool/komut | TOOLS.md |
| Kimlik/kişilik değişikliği | IDENTITY.md, SOUL.md |
| Kullanıcı bilgisi | USER.md |

## Git Workflow

Her anlamlı değişiklikten sonra:
```bash
cd /root/.openclaw/workspace
git add -A
git commit -m "Mesaj"
```

Commit mesajları kısa ve açıklayıcı olsun:
- ✅ "Lid switch ayarı: kapağı kapatınca ignore"
- ❌ "Yaptığım şeyler ve değişiklikler"

## Açık Kapalı Öğrenme

**Aktif:** Dokunduğun her şeyi öğren. Boş zamanını araştırmaya ayır.
**Pasif:** Bekleme, soru sor, tahmin etme.

## Öncelik Sırası

1. Şu an üzerinde çalıştığın problem
2. Sistem altyapısı (OpenClaw, Linux, networking)
3. Yeni tool'lar ve özellikler
4. Uzun vadeli memory (MEMORY.md güncelleme)

## Hata Ayıklama

Bir sorun olduğunda:
1. `openclaw status` → genel durum
2. `openclaw logs --follow` → canlı loglar
3. `journalctl -xe` → system loglar
4. İlgili config dosyasını oku
5. Çözümü uygula ve test et