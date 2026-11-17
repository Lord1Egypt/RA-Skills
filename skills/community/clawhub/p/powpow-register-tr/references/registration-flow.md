# Kayıt akışı ayrıntıları — powpow-register

Sorun giderirken başvurmak içindir. Tüm kurallar platform kaynak kodundan gelir (Next.js ön-arka uç tutarlılık
denetimi), kaynakları belirtilmiştir. Platform güncellendiğinde çevrimiçi fiilî davranış esas alınır.

## Giriş noktaları

- Kayıt sayfası: https://global.powpow.online/register
- Giriş sayfası: https://global.powpow.online/login
- Abonelik sayfası: https://global.powpow.online/subscription
- `?next=...` taşılı bir paylaşım bağlantısından gelinmişse, kayıt + ödeme tamamlanınca otomatik olarak orijinal
  sayfaya geri dönülür.

## Form alanları ve kuralları

| Alan | Zorunlu | Kural | Kaynak kod |
|---|---|---|---|
| Profil fotoğrafı | İsteğe bağlı | Görsel ≤5MB, SVG desteklenmez; sunucu otomatik sıkıştırır (>100KB ise 400×400 / kalite 90'a) | `src/app/api/auth/register/route.ts` |
| Kullanıcı adı | Zorunlu | 2~50 karakter, trim sonrası **küçük harfe** çevrilerek saklanır (Tom ile tom aynı kullanıcı adı sayılır; kayıt ve giriş tarafında da büyük/küçük harf duyarsızdır) | Aynı (zod şeması) |
| Şifre | Zorunlu | 8~100 karakter; büyük harf, küçük harf ve rakamın üçünü birden içermeli | Aynı |
| Şifre tekrarı | Zorunlu | Şifreyle aynı olmalı (yalnızca ön uç denetimi) | `src/app/(public)/register/page.tsx` |
| Takma ad | İsteğe bağlı | ≤100 karakter; boşsa kullanıcı adı alınır | register route |
| E-posta | **Zorunlu** | Geçerli e-posta biçimi, ≤255 karakter; bir e-posta yalnızca bir hesap açabilir | register route |
| E-posta doğrulama kodu | **Zorunlu** | 6 hane; **10 dakika geçerli**; doğrulama başarılı olunca geçersizleşir; yeniden gönderim eski kodu kullanılmış işaretler | `src/lib/email-verification.ts` |
| Telefon numarası | İsteğe bağlı | Çin anakarası numarası, `1[3-9]` ile başlayan 11 hane; bir numara yalnızca bir hesaba bağlanır | register route |

Sayfada ayrıca üç üçüncü taraf giriş düğmesi sunulur: **Google, Watcha, Huawei hesabı**
(`GoogleSignInButton` / `WatchaLoginButton` / `HuaweiLoginButton`). Üçüncü taraf hesapların yerel şifresi
yoktur; sonradan şifreyle giriş denenince «bu hesapta şifre tanımlı değil, başka bir yöntemle giriş yapın» yanıtı
alınır.

## Hız sınırları ve kaba kuvvet koruması parametreleri

| Davranış | Sınır | Kaynak |
|---|---|---|
| Kayıt gönderimi | **3 kez/dakika/IP**, aşılırsa 429 | `src/lib/rate-limit.ts` `REGISTER_RATE_LIMIT` |
| Doğrulama kodu gönderimi | Aynı IP'de 1 kez/dakika **ve** aynı e-postada 1 kez/dakika, aşılırsa 429; ön uçta düğme 60 saniye geri sayar | `src/app/api/auth/register/send-code/route.ts` |
| Doğrulama kodu denetimi | E-posta başına 10 dakikada en fazla **5 deneme**; tavana vurulunca kod doğru olsa bile reddedilir, kodun yeniden gönderilmesi gerekir | `src/lib/email-verification.ts` |
| Şifremi unuttum kodu | 1 kez/dakika/IP | `src/app/api/auth/forgot-password/route.ts` |
| Giriş | 5 kez/dakika/IP; aynı hesapta art arda **5 başarısız denemede 30 dakika kilitlenir** (423), bu sürede kalan deneme sayısı azalarak bildirilir | `src/app/api/auth/login/route.ts`, `rate-limit.ts` |

**Gizlilik koruma davranışı**: doğrulama kodu / şifremi unuttum gönderiminde, e-posta zaten kayıtlı olsa da olmasa
da arayüz aynı başarı metnini döndürür; e-postanın kayıtlı olup olmadığını ele vermez.

## Agent vekâlet modu ile web kaydının eşdeğerliği

Skill scripti **aynı kamuya açık API'leri** çağırır (`/api/auth/register`, `send-code`, `login`,
`/api/auth/me`); kayıt sayfası formunun gönderimiyle birebir aynı doğrulama, hız sınırı ve hata yollarından geçer —
bu dosyadaki tüm kurallar iki mod için de eşittir. Script sıralaması ve komut sözleşmesi
`references/agent-flow.md` içindedir.

## Başarılı Kayıttan Sonraki Durum Akışı

> **Ücretsiz test dönemi (2026-10-18'den başlayarak; platformun gerçek davranışı esastır)**: yeni kayıtlı hesap ödeme gerektirmeden **tüm özellikleri doğrudan kullanabilir**
> (akış, harita, dijital insanlar, check-in'ler vb.). Abonesi olmayan hesaplar artık içerik sayfalarından kesilmez. Bu bölümde anlatılan „pending yakalama”,
> test dönemi bittikten sonraki normal durumdur — o zaman geldiğinde gerçek çevrimiçi davranış esastır.

1. Kullanıcı `accountStatus: 'pending'` ve **3 başlangıç rozetiyle** kaydedilir (register rotası).
2. Sunucu ayrıca iki HttpOnly çerez bırakır: JWT (sayfalara doğrudan erişilebilir) ve pendingUserToken (abonelik akışı için kimlik kanıtı).
3. Normal durumda (test dönemi bitti / ücretsiz dönem yok) kayıt sayfası `pending_payment` algılar → `/subscription` sayfasına yönlendirir
   (`next` dönüş parametresini koruyarak); agent vekil modunda `me?token=…&redirect=/subscription` aynı etkiyi sağlar.
   **Ücretsiz test döneminde bu adım tetiklenmez** — kayıttan sonra doğrudan ana sayfaya git ve kullanmaya başla.
4. Ödeme tamamlandı → `accountStatus` `active` olur (**Alipay sunucu tarafında notify ile otomatik etkinleştirir**;
   PayPal Webhook ile etkinleştirir; WeChat QR kodu elle onaylanır; Huawei IAP `activate-huawei` üzerinden geçer).
   Ayrıntılar `payment-and-activation.md` içinde.

Normal durumda etkin olmayan (pending) hesapların temel API'leri (akış, harita, dijital insan sohbeti, check-in'ler vb.) çağırmaları 403 alır;
paylaşılan gönderi linkleri istisnadır (herkese açık kalır). Ücretsiz test döneminde bu yakalama askıya alınır ve her şey açıktır.
## Sık hataların giderme tablosu

| Belirti | Neden | Ne yapmalı |
|---|---|---|
| 「用户名已存在」 (kullanıcı adı zaten var) | Kullanıcı adı alınmış (büyük/küçük harf duyarsız) | Başka bir kullanıcı adı seçilmeli |
| 「邮箱已被使用」 (e-posta kullanılmış) | E-posta daha önce kaydedilmiş | E-posta değiştirilmeli; ya da girişe geçip «şifremi unuttum» ile eski hesap geri alınmalı |
| 「邮箱验证码错误或已过期」 (doğrulama kodu hatalı veya süresi geçmiş) | Kod yanlış / 10 dakika aşımı / 5 başarısız denemeden sonra reddedildi | «Yeniden gönder»e basılmalı, **en son gelen** e-postadaki kod kullanılmalı |
| Doğrulama kodu gelmiyor | 60 saniyelik hız sınırı; ya da spam/reklam klasörüne düşmüş | Geri sayım bitince tekrar gönderilmeli; spam klasörü karıştırılmalı |
| 「手机号已被使用」 (telefon numarası kullanılmış) | Numara başka hesaba bağlı | Numara çıkarılmalı (isteğe bağlı alan) ya da değiştirilmeli |
| 「注册请求过于频繁」 (kayıt istekleri çok sık) / 429 | Kayıtta 3 kez/dakika/IP tavanına vuruldu | Birkaç dakika bekleyip tekrar denenmeli |
| 409 「用户名或邮箱已被注册」 (kullanıcı adı veya e-posta zaten kayıtlı) | Gönderim anında başkasıyla çakışma (eşzamanlılık güvencesi) | Kullanıcı adı ya da e-posta değiştirilip tekrar denenmeli |
| 「图片大小不能超过5MB」 (görsel boyutu 5MB'ı aşamaz) / 「不支持 SVG」 (SVG desteklenmez) | Profil fotoğrafı kurallara uymuyor | Görsel değiştirilmeli ya da atlanmalı |
| Kullanıcı giriş linkine tıklıyor ama abonelik sayfasına düşüyor (ana sayfa yerine) | Ücretsiz test dönemi bitti ve platformun ödeme duvarı geri geldi | SKILL.md'deki 7. adımdaki abonelik ödeme akışını izle; abone olduktan sonra `refresh-login` çalıştır, sonra ana sayfa linkini gönder |
| Kayıt başarılı ama girişte 403 „请完成订阅以激活账户” dönüyor | Hesap hâlâ pending ve platform ücretsiz test döneminde değil (ödemeye kadar beklenen durum) | Ücretsiz test döneminde olmaz; olursa test dönemi bitmiştir — önce aboneliği tamamla; ödeme sonrası hâlâ 403 ise eski JWT kullanılmıştır — betik modunda yeni giriş durumuna takas için önce `refresh-login` çalıştır |
| Girişte 423 「账户已锁定」 (hesap kilitlendi) | Şifre 5 kez üst üste yanlış | 30 dakika beklenmeli |
| Girişte 401 「还剩 N 次尝试机会」 (N deneme hakkı kaldı) | Şifre yanlış, kilitlenmeye yakın | İyice düşünülüp denenmeli ya da doğrudan «şifremi unuttum» yoluna gidilmeli |
| 「该账号未设置密码，请使用其他方式登录」 (bu hesapta şifre tanımlı değil, başka bir yöntemle giriş yapın) | Üçüncü taraf (Google/Watcha/Huawei) hesabı | Orijinal üçüncü taraf düğmesiyle giriş yapılmalı |
| 「该账号已注销」 (bu hesap kapatılmış) | Hesap devre dışı bırakılmış | Yeniden kaydolmak gerekir |

## Giriş üzerine küçük notlar (sorun giderirken işe yarar)

Giriş, **kullanıcı adı / e-posta / telefon numarası** üçünü-bir-arada girişi destekler (üçünden herhangi biri
hesap adı sayılır).
Şifremi unuttum: giriş sayfası → «Şifremi unuttum» → kayıt e-postası girilip 6 haneli kod alınır → sıfırlanır.
