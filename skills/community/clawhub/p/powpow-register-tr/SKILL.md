---
name: powpow-register
description: Kullanıcının PowPow (Bubble) kaydını ve tek tıkla girişini sohbet içinde baştan sona tamamlamasına yardımcı olur. Agent kullanıcı adına formu doldurur (avatar yükleme dahil) ve e-posta doğrulama kodunu gönderir; kullanıcı yalnızca temel bilgileri verir ve doğrulama kodunu bir kez kontrol eder — sohbetten hiç çıkmaz. Platform şu anda ücretsiz test döneminde: kayıtlı hesap tüm özellikleri hemen kullanabilir; abonelik ödemesi (Alipay/PayPal) isteğe bağlı bir üyelik yükseltmesidir, gerekirse agent sipariş oluşturma ve tahsilat takibi de yapar. Kullanıcı „Bubble'a kayıt ol”, „powpow hesabı aç”, „Bubble nasıl kayıt olunur”, „bana powpow hesabı oluştur”, „sign up powpow” dediğinde tetiklenir; kayıt sorunlarını (doğrulama kodu gelmiyor, kullanıcı adı/e-posta alınmış) ve etkinleştirme sorunlarını (girişte „hesap etkin değil” / pending_payment, nasıl abone olunur/ödenir, Bubble ücretsiz mi/ücretli mi) de ele alır. Node ≥ 18 gerektirir; yoksa otomatik olarak saf rehberlik moduna düşer. Gönderi yapmayı/dijital insan oluşturmayı kapsamaz (o powpow-simple'in işi), kod geliştirmeyi de kapsamaz.
version: 2.2.0
metadata:
  openclaw:
    emoji: "\U0001F4DD"
    homepage: https://global.powpow.online
---

# PowPow Register (Kabarcık kayıt asistanı)

Yeni kullanıcıyı „Bubble'ın ne olduğunu bilmiyorum” durumundan „tek tıkla giriş yaptım, oynamaya hazırım” noktasına götürür — tamamı sohbet içinde. Kullanıcı sohbetten yalnızca bir kez çıkar: **gelen kutudaki doğrulama kodunu kontrol etmek için**. Platform şu anda ücretsiz test döneminde: kayıt olduktan sonra tüm özellikler kullanılabilir, ödeme gerekmez; abonelik ödemesi isteğe bağlı bir üyelik yükseltmesidir (agent kasayı da açar ve tahsilatı takip eder).

**Sürüm 2.2.0** · 2026-10-18 (v2'den bu yana agent vekalet modu: betik sözleşmesi ve tam sekans `references/agent-flow.md`; alan kuralları, hız sınırları ve hata ayıklama `references/registration-flow.md`; ödeme kanalları `references/payment-and-activation.md`; ürün ekran görüntüsü listesi `references/screenshots.md`. v2.1.0'dan bu yana PayPal aboneliklerini de agent yürütebilir, Alipay ile birlikte. v2.2.0'dan bu yana platform ücretsiz test döneminde: kayıt ol ve tek tıkla giriş yap, hemen kullan; ödeme isteğe bağlı bir yükseltmeye döndü — kullanıcı linke tıklayıp abonelik sayfasına düşerse test dönemi bitmiştir, 7. adımdaki ödeme akışını izle; akış kendini uyarlar, betik değişikliği gerekmez)

## Çalışma ortamı

- Ana script `scripts/powpow-register.mjs`: **sıfır bağımlılık**, **Node ≥ 18** gerektirir. Başlamadan önce ortamın çalıştığını doğrulamak için bir kez `node scripts/powpow-register.mjs status` çalıştırın.
- Scriptin tüm istekleri yalnızca resmî alan adı `https://global.powpow.online`'a gider.
- **Node yok / betik hatası**: otomatik olarak saf rehberlik moduna düş — kullanıcıya kayıt sayfası https://global.powpow.online/register ver ve `references/registration-flow.md`'e göre yanında rehberlik et (ücretsiz test döneminde web kaydı da aynı şekilde anında çalışır). Betiği ısrarla tekrar deneme.
- Sohbet kesilirse kurtarma: önce `status` çalıştırıp akışın hangi adımda kaldığına bakın, oradan devam edin.

## Trigger Conditions

- Kayıt niyeti: «Kabarcık'a kayıt ol», «powpow hesabı aç», «Kabarcık'a nasıl kaydolunur», «sign up powpow»
- Takılan kayıt: «doğrulama kodu gelmiyor», «kullanıcı adı zaten var diyor», «şifre bir türlü kabul edilmiyor»
- Kayıt sonrası sorunlar: „girişte hesap etkin değil diyor”, „403 pending_payment”, „Bubble nasıl ödenir/abone olunur”, „Bubble ücretsiz mi/ücretli mi”

**Şunlar için devreye girmez**: gönderi yayınlama/dijital insan oluşturma (→ powpow-simple); Web tarafı kod geliştirme (geliştirme skill'lerine bakın). Kullanıcı hem kayıt olmak hem gönderi yayınlamak istiyorsa: önce bu skill'i bitirin, etkinleşince powpow-simple'a devredin.

## Akışa genel bakış

| Adım | Agent ne yapar | Kullanıcı ne yapar |
|---|---|---|
| 1 Ürün tanıtımı | Tanıtır + ekran görüntüsü gönderir | Biraz göz atar |
| 2 Bilgi onayı | Kullanıcı adını/takma adı kendiliğinden önerir, şifrede iki seçenek sunar, e-postayı sorar | Onaylar, bilgi verir |
| 3 Kod gönderimi | `send-code` | —— |
| 4 Kod okuma | —— | E-postasına gidip 6 haneli kodu okur, yazar |
| 5 Kayıt gönderimi | `register` (profil fotoğrafını da yükler), hataları kendiliğinden yönetir | —— |
| 6 Tek tıkla giriş | `login-link(home)` doğrudan ana sayfaya; abonelik sayfasına düşerse 7. adıma git | Linke tıkla ve oynamaya başla |
| 7 Abonelik yükseltmesi (isteğe bağlı) | Yalnızca kullanıcı üyelik istediğinde / ücretsiz dönem bittiğinde: tam ödeme akışı yürütülür | Yöntem seç, öde |
| 8 Kapanış | `cleanup` + hesap bilgisi teslimi + deneyim rehberi + eklenti önerisi | Oynamaya başlar |

## Adım 1: ürün tanıtımı + ekran görüntüleri (atlanmaz)

Kullanıcıların çoğu Kabarcık'ı hiç görmemiştir. İlk iş akışı anlatmak değil, ürünü **göstermektir**:

1. Kabarcık'ı ~120 karakterle tanıtın: anlık fotoğrafları birer seyahat günlüğüne dönüştürür, kamuya açık haritada bir «kabarcık» olarak iliştirir; kabarcık zamanla soğur, başkalarının «beğen»leri onu yeniden canlandırabilir; haritada ayrıca sohbet edilebilen «dijital insanlar» vardır. Platform adresi: https://global.powpow.online ; önce video görmek isterse: https://www.bilibili.com/video/BV1Wu826UEVz/
2. **Ekran görüntülerini gönderin**. Görüntüler skill ile paketli halde `assets/screenshots/powpow-0N.jpg` konumundadır — yerel görsel dosyası olarak doğrudan gönderin, ağ gerekmez. Liste, her görüntünün içeriği ve kullanım anları `references/screenshots.md` içinde. Açılışta en çok kullanılan ikili: harita sayfası (powpow-03) + gönderi detay sayfası (powpow-06).

Ekran görüntüsü kuralları (sert kurallar):

- Görüntüler skill ile **paket halinde** `assets/screenshots/` içindedir (`powpow-0N.jpg`) — yerel görsel dosyası olarak doğrudan gönderin; GitHub'a ulaşılamayan ortamlar dahil her ortamda çalışır.
- Her seferinde yalnızca güncel konuyla ilgili 1–3 görüntü gönderin, hepsini birden yığmayın.
- Paketteki dosya yanlışlıkla eksikse, `references/screenshots.md`'de listelenen barındırma bağlantılarına dönün (dikkat: Çin anakarasında açılmayabilir).

Tanıtım bitince seçimi kullanıcıya iade edin: **«Kayıt olmak istersen, üç dakika içinde hesabını bu sohbette açarım; tek yapman gereken e-postandaki doğrulama kodunu bir kez okumak.»**

## Adım 2: kayıt bilgilerinin onayı (tur başına tek soru, hepsini birden sormayın)

- **Kullanıcı adı** (zorunlu): sohbet bağlamından/sistem kullanıcı adından yola çıkarak **kendiliğinden bir tane önerin** (2~50 karakter, büyük/küçük harf duyarsız); kullanıcı onaylarsa o kullanılır, değiştirmek isterse değiştirilir.
- **Şifre** (zorunlu; önce iki seçenekten birini seçtirin):
  - Kullanıcı kendisi verir → sonra scripte ortam değişkeniyle geçirin, **asla komut satırı parametresine koymayın**;
  - agent üretir → `node scripts/powpow-register.mjs gen-password` çalıştırın ve üretilen şifreyi **hemen kullanıcıya kaydetmesi için gönderin** (yalnızca bir kez gösterilir, sonra bir daha görünmez).
- **E-posta** (zorunlu): kullanıcı kendisi vermeli — bu hesabın kimlik çapasıdır, **tahmin etmeye kalkmayın**.
- **Takma ad** (isteğe bağlı): varsayılan olarak kullanıcı adıyla aynı önerin.
- **Profil fotoğrafı** (isteğe bağlı): kullanıcı yerel bir görsel yolu verirse (≤5MB, SVG değil) script doğrudan yükler; yoksa atlanır (platform varsayılan logoyu kullanır); görsel üretme yeteneğiniz varsa kendiliğinden bir tane yapmayı önerabilirsiniz.
- **Telefon numarası** (isteğe bağlı, Çin anakarası numarası): varsayılan olarak atlanır; yalnızca kullanıcı açıkça bağlamak isterse sorulur.

Onaydan sonra `prepare-suggest --username U --nickname N --email E` çalıştırıp durum dosyasına işleyebilirsiniz (sonrasında register'da tekrar geçmeye gerek kalmaz).

## Adım 3–4: e-posta doğrulama kodu (sohbetten ayrılmayı gerektiren tek nokta)

```
node scripts/powpow-register.mjs send-code --email <e-posta>
```

Sonra kullanıcıya net söyleyin: **e-postana git, 6 haneli doğrulama kodunu bul; 10 dakika geçerli; spam/reklam klasörlerine de bak**; bulunca gelip kodu bana yaz. Gönderimin 60 saniyelik bekleme süresi var, üst üste tıklamayın.

## Adım 5: kaydın gönderilmesi (agent vekâlet eder)

```
POWPOW_REGISTER_PASSWORD=<şifre> node scripts/powpow-register.mjs register --code <kod> [--username U] [--nickname N] [--avatar <yerel görsel yolu>] [--phone P]
```

Başarılı olursa hesap oluşur (pending durumu, 3 açılış rozetiyle birlikte). Sık hatalar otomatik yönetilir, kullanıcıyı bölmez:

| Hata | Yönetim |
|---|---|
| 「用户名已存在」 (kullanıcı adı zaten var) | Kendiliğinden bir varyant öner (kullanıcı adı + sayı), kullanıcı onaylayınca hemen tekrar dene (kod hâlâ geçerli, yeniden göndermek gerekmez) |
| 「邮箱已被使用」 (e-posta kullanılmış) | kullanıcıya sor: e-posta mı değişir, yoksa zaten hesabı mı var? (giriş/şifremi unuttum'a geç) |
| 「邮箱验证码错误或已过期」 (doğrulama kodu hatalı veya süresi geçmiş) | 10 dakikayı aşmışsa → `send-code`'u tekrar çalıştır |
| Gönderim/kayıt çok sık (429) | 1 dakika bekle ve tekrar dene; kullanıcıya tek cümleyle haber vermek yeter |

## Adım 6: Tek Tıkla Giriş (kayıttan sonra doğrudan ana sayfaya)

1. Kayıt başarılı olduktan hemen sonra:
   ```
   node scripts/powpow-register.mjs login-link --target home
   ```
2. Linki kullanıcıya gönder: **tıkladığında doğrudan ana sayfada, giriş yapılmış olarak açılır**. Platform şu anda ücretsiz test döneminde — kayıt olduktan sonra tüm özellikler (akış, harita, dijital insanlar, check-in'ler vb.) kullanılabilir, **ödeme gerekmez**.
3. Kullanıcıdan içeri girdiğini onaylamasını iste; iki durum var:
   - **Ana sayfaya düştü** → doğrudan 8. adıma geçip sar; kayıt tamamdır;
   - **Abonelik sayfasına düştü** → platformun ücretsiz test dönemi bitmiştir; kullanıcıya „ücretsiz deneme süresi bitti, şimdi üyelik aboneliği gerekiyor” de, sonra aboneliği tamamlamak için 7. adımı izle ve abone olduktan sonra 8. adıma dön.
4. Kullanıcı kendiliğinden yükseltmek veya platformu desteklemek isterse → yine 7. adıma git (abonelik gönüllüdür; ısrarcı olma).
## Adım 7: Abonelik Yükseltmesi (isteğe bağlı — yalnızca 6. adım gerektirdiğinde)

1. Ödeme dönüş sayfasının „Ödeme başarılı” yazısını doğru gösterebilmesi için önce yarı-giriş linkini gönder:
   ```
   node scripts/powpow-register.mjs login-link --target pending
   ```
   Linki kullanıcıya gönder: tıkladığında tarayıcı doğrudan abonelik sayfasında, giriş yapılmış olarak açılır.
2. **Kullanıcıdan bir ödeme yöntemi seçmesini iste** — iki kanalı da göster:
   - **Alipay (Çin ana karası / Alipay'i olan kullanıcılar)**: ilgili sürenin tek seferlik satın alımı, **otomatik yenileme yok**
     - Aylık **¥6.99** (denemek için önerilir) / Üç Aylık **¥19.99** / Yıllık **¥69.99**
   - **PayPal (yurt dışı / Alipay'i olmayanlar)**: ayda bir otomatik yenilenir, istendiğinde iptal edilir
     - Premium Monthly, yaklaşık **$1/ay** (abonelik sayfasındaki gibi; otomatik yenilemeli)
3. Kullanıcı birini seçtiğinde:
   - **Alipay**:
     ```
     node scripts/powpow-register.mjs create-order --package monthly
     ```
   - **PayPal**:
     ```
     node scripts/powpow-register.mjs create-order --provider paypal
     ```
   Betik ödeme sayfası dosyasının yolunu döndürür; **doğrudan bir sistem komutuyla aç** (Windows: `start <dosya>`; macOS: `open <dosya>`; Linux: `xdg-open <dosya>`). Tarayıcı otomatik olarak resmi Alipay/PayPal kasasına geçer, kullanıcı ödemeyi veya tahsilat yetkisini orada tamamlar.
4. `paid` veya `ACTIVE` dönene kadar her 10–15 saniyede bir `query` çalıştır (ödeme/yetki genelde birkaç saniye ile bir dakika arasında iner). Kullanıcı ödeme sayfasını yarıda kapatırsa → doğrudan `create-order` komutunu yeniden çalıştır (eski siparişler ve bekleyen abonelikler 2 saatte kendiliğinden kapanır veya düşer; aldırma).
5. WeChat QR kod kanalı elle onaylanır, tahsilat gecikebilir; Huawei IAP yalnızca HarmonyOS uygulaması içinde kullanılabilir. Skill bu ikisini yürütmez — ödeme yaptıktan sonra kullanıcı dönüp agenta bildirir, agent önce `whoami` çalıştırıp tahsilatı onaylar, sonra aşağıdaki 6. maddedeki gibi ana sayfa linkini gönderir.
6. Tahsilat onaylandıktan sonra en güncel abonelik claim'iyle yeni bir giriş durumuna takas et, sonra linki doğrudan ana sayfaya gönder:
   ```
   POWPOW_REGISTER_PASSWORD=<şifre> node scripts/powpow-register.mjs refresh-login
   node scripts/powpow-register.mjs login-link --target home
   ```
   Linki kullanıcıya gönder: **tıkladığında doğrudan ana sayfada, tam üyelik durumuyla açılır**.
## Adım 8: Sarma

1. Yerel geçici durum dosyalarını (oturum kimlik bilgilerini) temizlemek için `node scripts/powpow-register.mjs cleanup` çalıştır.
2. Kullanıcıya bir „hesap kartı” ver: kullanıcı adı, e-posta (şifre bir daha gösterilmez — üretim modunda kullanıcıdan üretildiğinde kaydetmesi istenmiştir; kullanıcı kendisi belirlediyse zaten bilir).
3. Üyelik hatırlatması (bir kez söyle, ısrarcı olma): şu anda ücretsiz test dönemi ve hesap hemen kullanılabilir; test dönemi bittiğinde abonesi olmayan hesaplar içerik sayfalarına girdiğinde abonelik sayfasına yönlendirilir — uzun süreli kullanım için dilediğinde gel ve abone ol.
4. İlk adımları yönlendir: haritaya göz at, ilk seyahat günlüğünü paylaş (→ powpow-simple'e devret).
5. Eklentileri öner: `@durenzidu/powpow-integration` skill'i ve `@durenzidu/openclaw-channel-powpow` eklentisi — Bubble'ı kullanıcının kendi agentına bağla; isterse kurulum komutunu ver.
6. Bir „sonraki adım” bloğuyla bitir.
## Conversation UX

powpow'un alışılmış hizmet tonunu koruyun:

- **Cümlelerin öznesi kullanıcıdır**; «şunu yapabilirsin…» «senden şunu yapmamı istiyorum»dan iyidir; nutuk çekmeyin, tepeden bakmayın.
- **Tur başına yalnızca bir karar ilerletin**; bilgi istemeden önce gerekçesini söyleyin.
- **Her yanıtın sonunda** sabit bir «sonraki adım» bloğu (ayraç + 👉 + tek eylem + «yaptığında ben … yapacağım» cümlesi), örneğin:
  ```
  ────────────────────
  👉 Sıra sende: e-postana git, 6 haneli kodu bul ve bana yaz
     (kod elime geçince hesabını açıyorum)
  ```
- **Şifre konusunda kendiliğinden güvenlik dersi vermeyin**; kullanıcı sormadıkça iç mekanizmaları, hız sınırlarını ve güvenlik tasarımını açıklamayın.
- Agent vekâlet ettikçe ilerlemeyi bildirsin: scriptin her adımından sonra kullanıcıya tek cümleyle ne olduğunu söyleyin («hesabın açıldı», «ödeme sayfasını sana açtım»).

## Sert kurallar

- **Kimlik bilgisi güvenliği**: şifre scripte yalnızca `POWPOW_REGISTER_PASSWORD` ortam değişkeniyle geçirilir, **asla** komut satırı parametresine konmaz (süreç listesinde görünür), hiçbir dosyaya yazılmaz (üretim modunda kullanıcı kaydetsin diye bir kez gösterilir, sonra bir daha anılmaz). Doğrulama kodu yalnızca resmî kayıt arayüzünde kullanılır ve işi bitince atılır.
- **Resmîlik sınırı**: tüm istekler yalnızca `https://global.powpow.online`'a gider (scripte yerleşiktir); kullanıcı bilgilerini asla üçüncü taraf adreslere göndermeyin.
- **Ödeme sınırı**: agent yalnızca sipariş açar, kasayı açar, para geçişini sorgular; kullanıcının Alipay/PayPal hesabına/ödeme belgelerine **asla** dokunmaz, «ben öderim» diye söz de vermez.
- **Ödeme duvarı bir hata değil**: mevcut ücretsiz test döneminde tüm içerik sayfaları açık; kullanıcı ana sayfa linkine tıklayıp abonelik sayfasına düşerse test dönemi bitmiştir — 7. adım üzerinden aboneliğe yönlendir. Ödeme duvarını aşmaya çalışma ve kullanıcıya içsel mekanizmaları açma.
- **Geri dönme özgürlüğü**: herhangi bir adımda kullanıcı kendi yapmak isterse ya da ortam scripti çalıştıramıyorsa, istediğiniz an salt yol gösterme moduna dönün — bağlantıları verin, kuralları anlatın, hataları birlikte çözün.
- Platform kuralı uydurmayın: alan kuralları, hata metinleri ve hız sınırı parametrelerinin tamamı platform kodundan gelir (`references/registration-flow.md` kaynağı gösterir); platform güncellenirse fiilî davranış esas alınır.
- Görsel gösterirken yalnızca paketteki `assets/screenshots/` ekran görüntülerini kullanın (her birinin kullanımı `references/screenshots.md`'de).
- Her turu «sonraki adım» bloğuyla kapatın; kullanıcı şu anda ne yapması gerektiğini her zaman bilsin.
