# Kayıtlı Elektronik Posta (KEP) Rehberi — Türkiye

> **Son güncelleme:** Mart 2026  
> **Kaynak:** BTK, Türkkep, TNB KEP, resmi mevzuat  
> **Resmi portal:** https://www.btk.gov.tr/kep

---

## 1. KEP Nedir?

**Kayıtlı Elektronik Posta (KEP)**, gönderilen e-postanın **içeriğinin, gönderildiğinin ve iletildiğinin** yasal olarak ispat edilebilir şekilde belgelendiği, zaman damgalı elektronik posta sistemidir.

### Normal E-Posta vs. KEP

| Özellik | Normal E-Posta | KEP |
|---------|---------------|-----|
| Yasal geçerlilik | Sınırlı | Tam (mahkemede delil) |
| İçerik bütünlüğü | Garanti yok | Şifreli, değiştirilemez |
| Teslim kanıtı | Yok | Zaman damgalı delil |
| İnkar edilebilirlik | Yüksek | İnkar edilemez |
| Maliyet | Ücretsiz/düşük | Ücretli |
| Denetim | Yok | BTK denetimli |

### KEP'in Hukuki Temeli
KEP, **"iadeli taahhütlü mektup"** ile eşdeğer hukuki güce sahiptir. Mahkemelerde delil olarak kabul edilir.

---

## 2. Yasal Dayanak

### 6102 Sayılı Türk Ticaret Kanunu (TTK)

**Madde 18/3:**
> "Tacirler arasında yapılacak ihbarlar ve ihtarların noter aracılığıyla veya taahhütlü mektupla ya da telgrafla ya da güvenli elektronik imzalı yazıyla — **KEP dahil** — yapılması gerektiğinde bu yükümlülük yerine getirilmiş sayılır."

**Madde 1525:**
> Ticaret siciline tescil zorunluluğu bulunan anonim ve limited şirketlerin, kooperatiflerin ve ticari işletmelerin MERSİS kaydında KEP adresi bildirmesi zorunludur.

### 7201 Sayılı Tebligat Kanunu

**Ek Madde 1:**
> Elektronik yolla tebligat zorunluluğu: Tüzel kişiler ve belirli gerçek kişiler (avukatlar, noterler) için elektronik tebligat (e-tebligat veya KEP) zorunludur.

### Diğer İlgili Mevzuat

| Kanun/Yönetmelik | İçerik |
|-----------------|--------|
| 5070 Elektronik İmza Kanunu | KEP'te kullanılan e-imza standardı |
| BTK KEP Yönetmeliği (2011) | KEP hizmet sağlayıcı akreditasyonu |
| Ticaret Sicili Yönetmeliği | KEP adresi tescili zorunluluğu |
| Avukatlık Kanunu (md. 56/A) | Baro kayıtlı avukatlara KEP zorunluluğu |

---

## 3. Kimler KEP Almak Zorunda?

### Zorunlu Gruplar

| Grup | Dayanak | Açıklama |
|------|---------|---------|
| **Anonim Şirketler (AŞ)** | TTK 1525 | MERSİS kaydında KEP zorunlu |
| **Limited Şirketler (Ltd.)** | TTK 1525 | MERSİS kaydında KEP zorunlu |
| **Kooperatifler** | TTK 1525 | Ticaret siciline kayıtlılar |
| **Avukatlar** | Avukatlık Kanunu | Baro kaydı sırasında |
| **Noterler** | Tebligat Kanunu | Resmi tebligat alımı için |
| **Kamu kurumları** | e-Devlet entegrasyonu | Elektronik tebligat için |
| **İcra takipleri** | UYAP | Mahkeme süreçlerinde |

### Önerilen Gruplar (Zorunlu Olmasa da Yararlı)
- Şahıs şirketleri / ticaret sicili kaydı olanlar
- Serbest meslek erbabı (avukat dışı)
- E-ticaret yapan bireysel satıcılar
- Sık hukuki yazışma yapan KOBİ'ler

---

## 4. KEP Hizmet Sağlayıcıları

BTK tarafından akredite edilmiş KEP hizmet sağlayıcıları:

### Karşılaştırma Tablosu

| Sağlayıcı | Web Sitesi | Güçlü Yönler | Yıllık Fiyat (Tahmini) |
|-----------|-----------|-------------|----------------------|
| **Türkkep** | turkkep.com.tr | Pazar lideri, en geniş entegrasyon | ~500-1.500 TL/yıl |
| **TNB KEP** | tnbkep.com.tr | PTT altyapısı, geniş ağ | ~400-1.200 TL/yıl |
| **KEPAS** | kepas.com.tr | Kurumsal odaklı | ~600-2.000 TL/yıl |

> ⚠️ Fiyatlar 2026 yılı için tahminidir. Güncel fiyat için sağlayıcı sitelerini kontrol edin.

### Sağlayıcı Seçim Kriterleri
1. **API kalitesi:** REST API, SMTP entegrasyon
2. **Depolama:** Gelen/giden kutusu kapasitesi
3. **SLA:** Erişilebilirlik garantisi
4. **Kurumsal özellikler:** Çoklu kullanıcı, departman yönetimi
5. **Fiyat modeli:** Kota başı mı, aylık sabit mi?

---

## 5. KEP Adresi Nasıl Alınır? (Adım Adım)

### Tüzel Kişiler (Şirketler) için

**Türkkep üzerinden örnek süreç:**

**1. Adım — Hazırlık**
- Vergi levhası fotokopisi
- İmza sirküleri / yetkilendirme belgesi
- Yetkili kişinin TC kimlik kartı
- Şirket unvanı (MERSİS'e kayıtlı)

**2. Adım — Başvuru**
- https://www.turkkep.com.tr adresine git
- "KEP Başvurusu" → Kurumsal seçeneğini seç
- Online form doldur veya yetkili satıcıya git

**3. Adım — Kimlik Doğrulama**
- e-İmza veya mobil imza ile doğrulama
- ya da Türkkep yetkili satıcılarından biri üzerinden yüz yüze

**4. Adım — Aktivasyon**
- Başvuru onay süresi: 1-2 iş günü
- KEP adresi formatı: `ticaret.unvani@hs01.kep.tr` (Türkkep)
- MERSİS'e KEP adresini bildirme (TTK 1525 gereği)

**5. Adım — MERSİS Bildirimi**
- https://mersis.gtb.gov.tr adresine giriş
- Şirket bilgileri → KEP adresi güncelle
- Ticaret sicili kaydında güncelleme

### Gerçek Kişiler için
- TC kimlik kartı
- e-Devlet şifresi veya e-İmza
- Online başvuru (adımlar şirketlerle benzer)

---

## 6. KEP ile Yapılabilecekler

### Hukuki İşlemler
| İşlem | Açıklama |
|-------|---------|
| **Tebligat** | Mahkeme, icra, vergi tebligatı alma |
| **İhtar/ihbar** | Hukuki geçerli ihtar gönderme |
| **Sözleşme** | e-İmzalı sözleşme iletimi |
| **İtiraz** | İdari itiraz süreçleri |
| **Bildirim** | SGK, vergi dairesi bildirimleri |

### Ticari İşlemler
| İşlem | Açıklama |
|-------|---------|
| **Sipariş/teklif** | Bağlayıcı ticari yazışmalar |
| **Fatura gönderimi** | E-arşiv fatura iletimi |
| **Sözleşme** | Tedarik sözleşmeleri |
| **İş akdi** | İşe alım ve fesih bildirimleri |

### Kamu İşlemleri
| İşlem | Açıklama |
|-------|---------|
| **e-Tebligat** | Tüm resmi devlet tebligatları |
| **UYAP** | Mahkeme süreçleri |
| **e-Devlet** | Resmi başvuru yanıtları |

---

## 7. KEP API Entegrasyonu

### API Özellikleri (Türkkep örneği)
Türkkep, geliştiriciler için REST API ve SMTP entegrasyonu sunar.

**Desteklenen Protokoller:**
- REST API (JSON/XML)
- SMTP (port 587, STARTTLS)
- IMAP (gelen kutusu okuma)
- SOAP Web Servisleri (kurumsal)

### Temel API İşlemleri
```bash
# Türkkep API - KEP Gönderme (örnek)
curl -X POST https://api.turkkep.com.tr/v1/send \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "alici@hs01.kep.tr",
    "subject": "Hukuki Bildirim",
    "body": "...",
    "attachments": []
  }'
```

**API Yanıtı Bileşenleri:**
- `messageId` — Benzersiz KEP mesaj kimliği
- `timestamp` — Gönderim zaman damgası
- `deliveryProof` — Teslimat kanıtı belgesi
- `contentHash` — İçerik bütünlüğü hash'i

### Python ile KEP Entegrasyonu
```python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def kep_gonder(gonderen, sifre, alici, konu, icerik):
    """Türkkep SMTP üzerinden KEP gönder"""
    msg = MIMEMultipart()
    msg['From'] = gonderen
    msg['To'] = alici
    msg['Subject'] = konu
    msg.attach(MIMEText(icerik, 'plain', 'utf-8'))
    
    with smtplib.SMTP('smtp.turkkep.com.tr', 587) as server:
        server.starttls()
        server.login(gonderen, sifre)
        server.send_message(msg)
    
    return True

# Kullanım
kep_gonder(
    'sirket@hs01.kep.tr',
    'kep_sifreniz',
    'alici@hs02.kep.tr',
    'Ödeme İhtarı',
    '30 gün içinde ödeme yapılması hususunda...'
)
```

### Entegrasyon Kaynakları
- **Türkkep API Docs:** https://www.turkkep.com.tr/api
- **TNB KEP Teknik Döküman:** https://www.tnbkep.com.tr/entegrasyon

---

## 8. E-Tebligat vs. KEP Farkı

Sık karıştırılan iki kavram:

| Özellik | KEP | E-Tebligat |
|---------|-----|-----------|
| Sistem | Özel KEP sağlayıcıları | Posta ve Telgraf Teşkilatı (PTT) |
| Kapsam | Tüm hukuki ve ticari yazışmalar | Resmi devlet tebligatları |
| Kullanım | B2B, B2C, kamu | Sadece resmi tebligat |
| Adres | @hs01.kep.tr, @kep.tr | e-tebligat.gov.tr üzerinden |
| Zorunluluk | TTK kapsamındaki şirketler | Tüzel kişiler (ayrı mevzuat) |

**Öneri:** İki sistemi birlikte kullanın. KEP ticari yazışmalar için, e-Tebligat sistemi ise devlet tebligatları için ayrı portaldır.

---

## 9. Sık Sorulan Sorular

**S: KEP adresi değişebilir mi?**  
A: KEP adresi değiştirilemez; ancak farklı bir sağlayıcıdan yeni KEP adresi alınabilir. İki adres birden aktif olabilir.

**S: KEP gelen kutusunu ne kadar süre saklamamız gerekir?**  
A: Hukuki yazışmalar TTK kapsamında en az 10 yıl saklanmalıdır. Sağlayıcılar genellikle arşiv hizmeti sunar.

**S: KEP ile yurt dışına yazışma yapabilir miyim?**  
A: KEP Türkiye'ye özgü bir sistemdir. Uluslararası eşdeğeri için "REM (Registered Electronic Mail)" kullanılır, Türkiye henüz REM'e tam entegre değildir.

**S: KEP hesabını şirket içinde birden fazla kişi kullanabilir mi?**  
A: Evet, kurumsal planlarda departman/kullanıcı yönetimi sunan sağlayıcılar var (Türkkep Kurumsal gibi).

**S: KEP süresi dolunca ne olur?**  
A: Yenilenmezse gelen mesajlar düşer, gönderim yapılamaz. Önemli tebligatlar kaçırılabilir.

---

## 10. Fiyatlandırma (2026 Tahmini)

### Bireysel / Küçük Şirket
- Türkkep Bireysel: ~500-800 TL/yıl
- TNB KEP Bireysel: ~400-700 TL/yıl

### KOBİ
- Türkkep KOBİ: ~800-1.500 TL/yıl (artan kota, öncelikli destek)
- TNB KEP KOBİ: ~700-1.200 TL/yıl

### Kurumsal
- Çoklu kullanıcı, API erişimi, arşivleme
- ~2.000-10.000+ TL/yıl (kuruma özel fiyatlandırma)

---

*Bu rehber Finhouse (finhouse.ai) tarafından hazırlanmıştır. KEP entegrasyonu için danışmanlık: info@finhouse.ai*
