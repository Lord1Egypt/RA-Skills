# Agent vekâlet akışı ve script sözleşmesi — powpow-register

SKILL.md'deki adımların yürütme ayrıntıları. Tüm komutlar `node scripts/powpow-register.mjs <alt komut> [parametreler]`
biçimindedir; script **sıfır bağımlılıktır**, **Node ≥ 18** gerektirir, tüm istekler yalnızca
`https://global.powpow.online`'a gider.

## Güvenlik tasarımı (neden böyle tasarlandı)

| Tasarım | Gerekçe |
|---|---|
| Şifre yalnızca `POWPOW_REGISTER_PASSWORD` ortam değişkeniyle geçer | Sürecin komut satırı parametreleri aynı makinedeki diğer süreçlere görünür (argv sızıntı yüzeyi); ortam değişkeni script içinde okunur okunmaz kullanılır |
| Şifre **asla durum dosyasına yazılmaz**, asla loglarda görünmez | Durum dosyası diskte kalabilir; sohbetteki üretim modunda bir kez gösterilmesinin nedeni kullanıcının kaydetmesidir |
| Durum dosyası sistem geçici dizininde (`os.tmpdir()/powpow-register-state.json`, 0600) | Yalnızca email / username / nickname / token / outTradeNo alanlarını içerir, `cleanup` tek komutla temizler |
| Agent'ın elindeki JWT, resmî `me?token=` uç noktasından tarayıcı cookie'sine dönüştürülür | Platformun HarmonyOS WebView için tasarlanmış resmî köprüsüdür; imza doğrulaması yalnızca imza + geçerlilik süresine bakar, cihaz parmak izine bağlamaz, kullanıcının tarayıcısı kullanabilir |
| Ödemede yalnızca create-order / query / kasa açma yapılır | Ödeme eylemi ve ödeme belgeleri her zaman kullanıcı ile Alipay'in resmî kasası arasındadır, agent araya girmez |

## Komut başvurusu

| Komut | Temel parametreler | İşlev / zamanı |
|---|---|---|
| `status` | —— | Akış ilerlemesini görür (durum dosyasını okur); sohbet kesildikten sonra önce bunu çalıştırın |
| `gen-password` | —— | 24 karakterlik güçlü şifre üretir (büyük + küçük harf ve rakam içerir), stdout'da **yalnızca bu kez** gösterilir |
| `prepare-suggest` | `--username --nickname --email` | Onaylanmış bilgileri durum dosyasına işler (sonrasında register'da tekrar geçmeye gerek yok) |
| `send-code` | `--email` | Platformun 6 haneli doğrulama kodu göndermesini tetikler (10 dakika geçerli, 60s bekleme) |
| `register` | `--code` (zorunlu); `--username --nickname --avatar --phone` (isteğe bağlı, durum dosyasında varsa geçilmez) | pending hesap oluşturur; şifre `POWPOW_REGISTER_PASSWORD` ortam değişkeniyle; başarılı olunca JWT otomatik olarak durum dosyasına yazılır |
| `login-link` | `--target pending` veya `--target home` | Tek tıkla giriş linki üretir (çift link tasarımı, aşağıya bak) |
| `create-order` | `--package monthly\|quarterly\|yearly` (varsayılan Alipay)<br>`--provider alipay\|paypal` | Ödeme siparişini oluşturur; Alipay ödeme sayfası dosya yolunu + outTradeNo döndürür, PayPal onay sayfası dosya yolunu + subscriptionId döndürür (otomatik olarak durum dosyasına yazılır) |
| `query` | —— | Sipariş/abonelik durumunu sorar. Alipay: `paid / pending / closed / unknown`; PayPal: `ACTIVE / PENDING`; 10–15s arayla yoklanır |
| `refresh-login` | şifre ortam değişkeniyle | Yeniden giriş yapıp **yeni JWT** alır (abonelik beyanı NONE'dan ACTIVE'e döner), para geçtikten sonra mutlaka çalıştırılır |
| `whoami` | —— | Durum dosyasındaki token ile hesabı ve abonelik durumunu sorgular (etkinleşmenin tutup tutmadığını doğrular) |
| `cleanup` | —— | Durum dosyasını siler (kapanışta mutlaka çalıştırılır) |

**Ortam değişkeni geçişi** (şifre asla komut satırına çıkmaz):

```bash
# bash / zsh / WSL
POWPOW_REGISTER_PASSWORD='<şifre>' node scripts/powpow-register.mjs register --code 123456
# PowerShell
$env:POWPOW_REGISTER_PASSWORD = '<şifre>'; node scripts/powpow-register.mjs register --code 123456
# cmd
set POWPOW_REGISTER_PASSWORD=<şifre> && node scripts/powpow-register.mjs register --code 123456
```

## Çift Link Mekanizması (temel tasarım)

Platformun giriş durumu HttpOnly çerezidir, agent'ın doğrudan tarayıcıya ekleyemeyeceği; köprü resmi
`/api/auth/me?token=<JWT>&redirect=<site içi yol>` uç noktasıdır: imzayı doğrula → otomatik olarak
oturum oluştur → `Set-Cookie: powpow_token` (HttpOnly / SameSite=Lax / 7 gün) → yönlendirmeyi
doğrula (tek eğik çizgiyle başlamalı, `//` ve ters eğik çizgiler yasak, çözüldükten sonra aynı kaynak olmalı) → hedef sayfaya 307 geçici yönlendirme.

İki link hedefi vardır, **önce home üret, pending'den geçilip geçilmeyeceğine kullanıcı nereye düştüyse karar ver**:

- **home linki (varsayılan olarak gönderilir, `--target home` → `/` sayfasına iner)**: kayıt başarılı olduktan hemen sonra üretilip kullanıcıya gönderilir.
  Ücretsiz test döneminde kullanıcı doğrudan ana sayfaya gider, her şey kullanılabilir; **linke tıklayıp abonelik sayfasına düşerse ücretsiz test dönemi bitmiştir** — ödeme akışına geç (aşağıya bak); betik değişikliği ve yeniden kayıt gerekmez.
- **pending linki (ödeme akışında kullanılır, `--target pending` → `/subscription` sayfasına iner)**:
  kullanıcının tarayıcısı „yarı giriş” durumuna girer: abonelik sayfası ve ödeme dönüş sayfası görünür ve kullanılabilir. Ödeme indikten sonra
  ACTIVE claim'li yeni bir JWT'ye takas etmek için `refresh-login` çalıştır, sonra tam üyelik durumu için home linkini bir kez daha gönder.

## Tam Sekans

### Hızlı Yol (ücretsiz test döneminde — durumların büyük çoğunluğu)

```
1.  status                          # ortam öz-kontrolü
2.  (2. adım: bilgiyi teyit için sohbet, şifre istediğin gibi; üretim modu: gen-password → kullanıcıdan hemen kaydetmesini iste)
3.  prepare-suggest --username U --nickname N --email E
4.  send-code --email E             # → kullanıcı kodu gelen kutuda kontrol eder (sohbetten tek çıkış)
5.  POWPOW_REGISTER_PASSWORD=*** register --code 123456 [--avatar pic.jpg]
6.  login-link --target home        # → linki kullanıcıya gönder; tek tıkla ana sayfada
7.  (kullanıcı içeri girdiğini teyit eder) → doğrudan sar: cleanup + hesap kartı + ilk adımları yönlendir
```

### Ödeme Yolu (kullanıcı üyelik istediğinde veya ücretsiz dönem bittiğinde)

```
1–5. Hızlı Yol ile aynı (register başarılı olduktan sonra durumda token zaten var)
6.  login-link --target pending     # → yarı-giriş linki, ödeme dönüş sayfası çalışmaya devam eder
7.  (kullanıcı bir ödeme yöntemi seçer)
    # Alipay: create-order --package monthly|quarterly|yearly
    # PayPal: create-order --provider paypal
8.  start <ödeme sayfası dosyası>   # Windows; macOS open, Linux xdg-open
    # → kullanıcı Alipay/PayPal kasasında ödemeyi/yetkiyi tamamlar (sohbetten çıkar)
9.  query (her 10–15 s) paid / ACTIVE olana kadar
10. refresh-login                   # ACTIVE claim'li yeni JWT'ye takas
11. login-link --target home        # → kullanıcıya tam üyelik linkini gönder
12. whoami                          # subscriptionStatus: ACTIVE olduğunu teyit et (isteğe bağlı)
13. cleanup                         # durum dosyasını temizle
```
## Komut → platform API eşlemesi

| Script komutu | Platform arayüzü |
|---|---|
| `send-code` | `POST /api/auth/register/send-code` |
| `register` | `POST /api/auth/register` (multipart, profil fotoğrafı doğrudan yüklenir) |
| `login-link` | `GET /api/auth/me?token=…&redirect=…` (bağlantının kendisi, tarayıcı tıkladığında etkili olur) |
| `create-order` | `POST /api/payment/alipay/create-order` (Bearer, Alipay)<br>`GET /api/subscription/plans` + `POST /api/subscription/create` (Bearer, PayPal) |
| `query` | `GET /api/payment/alipay/query?outTradeNo=…` (Bearer, Alipay)<br>`GET /api/subscription/create` (Bearer, PayPal) |
| `refresh-login` | `POST /api/auth/login` (`{step:1, username, password}`) |
| `whoami` | `GET /api/auth/me?token=…` |

Kural kaynakları: kayıt alanları ve hız sınırları için `registration-flow.md`; paketler ve etkinleştirme zinciri
için `payment-and-activation.md` (ikisinde de platform kaynak dosyaları belirtilidir).

## Script düzeyinde hata yönetimi

| Belirti | Yönetim |
|---|---|
| `Node sürümü çok düşük` | Salt yol gösterme moduna dönün, inatla denemeyin |
| Ağ hatası / zaman aşımı | Bir kez tekrar deneyin; yine başarısızsa kullanıcı ağı kontrol etsin, sonra devam (durum dosyası duruyor, baştan `status` ile kurtarılır) |
| register iş hatası verir (kullanıcı adı var vb.) | SKILL.md Adım 5'teki tabloya göre yönetilir, **doğrulama kodu yeniden gönderilmez** (10 dakika içinde hâlâ geçerlidir) |
| register 「邮箱验证码错误或已过期」 (doğrulama kodu hatalı ya da süresi geçmiş) der | Süre aşımı → `send-code` yeniden |
| `create-order`'dan sonra kullanıcı ödeme sayfasını kapattı | Doğrudan `create-order` yeniden (eski sipariş 2 saatte otomatik kapanır; PayPal PENDING abonelikler 1 saatte sona erer) |
| `create-order --provider paypal` 409 döndürüyor | Hâlihazırda tamamlanmamış bir PayPal aboneliği var; 1 saat bekleyip sona ermesini bekleyin ya da eski onayı tarayıcıda tamamlayın |
| `query` sürekli pending / PENDING | Kullanıcı ödememiş olabilir; bir cümle sorun. Gerçekten ödediyse → payment-and-activation.md'deki teşhis tablosunu izleyin |
| Kullanıcı home linkine tıklıyor ama abonelik sayfasına düşüyor | Ücretsiz test dönemi bitti → ödeme akışına geç: `login-link --target pending` → ödeme yöntemi seç → `create-order` |
| `refresh-login` 403 `pending_payment` | Ücretsiz test dönemi bitti ve ödeme inmedi; sorgulamaya devam etmek için 9. adıma dön ya da kullanıcının ödemeyi tamamlayıp tamamlamadığını teyit et |
| Durum dosyası kayboldu (yanlışlıkla silindi / makine değişti) | `whoami`/`refresh-login` kullanılamaz; kullanıcıya, bağlantı 1'i açtığı tarayıcıda abonelik sayfasını yenileterek durumu doğrulatın ya da yeniden giriş yaptırın (web modu) |

## Geri dönüş modu (salt yol gösterme)

Aşağıdaki durumlardan herhangi biri olursa hemen v1 tarzı salt yol göstermeye dönülür, script daha fazla
uğraştırılmaz:

- Node ≥ 18 yok ya da script art arda iki kez aynı tür hatayı verdi;
- Kullanıcı açıkça «ben web'de kendim yaparım» dedi;
- Şirket/cihaz politikası scriptin ağa çıkmasını kısıtlıyor.

Geri düştükten sonra: kayıt sayfası https://global.powpow.online/register ver (ücretsiz test döneminde web kaydı da aynı şekilde anında çalışır; abonelik gerektiğinde abonelik sayfası https://global.powpow.online/subscription de ver ), `registration-flow.md`'deki kurallara göre yanında sorunu çöz, aynı tonu koru ve her turu yine bir „sonraki adım” bloğuyla bitir.
https://global.powpow.online/subscription verilir, `registration-flow.md` kurallarına göre eşlik edilir, ton
değişmez, her tur yine «sonraki adım» bloğuyla kapanır.
