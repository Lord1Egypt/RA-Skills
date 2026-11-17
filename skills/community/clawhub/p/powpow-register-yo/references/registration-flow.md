# Ẹ̀kọ́ jinlẹ̀ ti ṣiṣan iforukosile — powpow-register

Fun lilo nigbati a ba n ṣayẹwo awọn iṣoro. Gbogbo awọn ofin wa lati inu koodu pẹpẹ (ayẹwo ibaramu iwaju ati ẹhin Next.js), pẹlu orisun ti a darukọ. Nigbati pẹpẹ ba ṣe imudojuiwọn, tẹle ihuwasi gangan lori ayelujara.

## Ẹnu-ọna

- Oju-iwe iforukosile: https://global.powpow.online/register
- Oju-iwe wiwọle: https://global.powpow.online/login
- Oju-iwe ṣiṣe alaisanfarasin: https://global.powpow.online/subscription
- Ti o ba wọle lati ọna asopọ pinpin ti o ni `?next=...`, lẹhin iforukosile + isanwo ti pari yoo darí pada si oju-iwe atilẹba laifọwọyi.

## Awọn aaye fọọmu ati awọn ofin

| Aaye | Dandan | Ofin | Orisun koodu |
|---|---|---|---|
| Aworan profaili | Iyanjiyan | Aworan <=5MB, ko ṣe atilẹyin SVG; olupin n ko pẹpẹ laifọwọyi (ti o ba ku ju >100KB ko si 400×400 / didara 90) | `src/app/api/auth/register/route.ts` |
| Oruko olumulo | Dandan | Awọn ohun kikọ 2~50, lẹhin gige ati yọ aaye kuro yipada si **kekere** lati tọju (Tom ati tom jẹ oruko olumulo kanna, ẹgbẹ iforukosile ati wiwọle ko ṣe akiyesi nla-kekere) | bakanna (zod schema) |
| Ọrọ igbaniwọle | Dandan | Iwọn 8~100, gbọdọ ni nla-kekere ati nọmba ni apapọ | bakanna |
| Jẹri ọrọ igbaniwọle | Dandan | Baraamu pẹlu ọrọ igbaniwọle (ayẹwo iwaju nikan) | `src/app/(public)/register/page.tsx` |
| Oruko ọrẹ | Iyanjiyan | <=100 ohun kikọ; ti ko ba kun aiyipada gba oruko olumulo | register route |
| Imeeli | **Dandan** | Fọọmu imeeli to tọ, <=255 ohun kikọ; imeeli kan le forukosile akọọlẹ kan nikan | register route |
| Koodu ijẹrisi imeeli | **Dandan** | Oni-nọmba 6; **wulo fun iṣẹju 10**; lẹhin ijẹrisi aṣeyọri ni a sọnù; atunfiranṣẹ yoo samisi atijọ bi a ti lo | `src/lib/email-verification.ts` |
| Nọmba foonu | Iyanjiyan | Nọmba foonu oluile `1[3-9]` bẹrẹ pẹlu lapapọ awọn nọmba 11; nọmba foonu kan le so akọọlẹ kan nikan | register route |

Oju-iwe naa tun pese awọn bọtini wiwọle ẹnikẹta mẹta: **Google, Watcha, Huawei** (`GoogleSignInButton` /
`WatchaLoginButton` / `HuaweiLoginButton`). Awọn akọọlẹ ẹnikẹta ko ni ọrọ igbaniwọle agbegbe, nigbamii nigba lilo wiwọle ọrọ igbaniwọle yoo
gba `该账号未设置密码，请使用其他方式登录` (akọọlẹ yii ko ṣe eto ọrọ igbaniwọle, jọwọ lo ọna wiwọle miiran).

## Ihamọ ati awọn ariyanjiyan idena

| Iṣe | Ihamọ | Orisun |
|---|---|---|
| Ifisilẹ iforukosile | **3 igba/iṣẹju/IP**, ti o ba ju 429 | `src/lib/rate-limit.ts` `REGISTER_RATE_LIMIT` |
| Firanṣẹ koodu ijẹrisi | IP kanna 1 igba/iṣẹmu **ati** imeeli kanna 1 igba/iṣẹmu, ti o ba ju 429; bọtini iwaju iṣẹju 60 | `src/app/api/auth/register/send-code/route.ts` |
| Ayẹwo koodu ijẹrisi | Fun imeeli kọọkan laarin iṣẹju 10 awọn igbiyanju to **5**, ti o ba de opin paapaa ti nọmba ba tọ yoo kọ, o nilo atunfiranṣẹ | `src/lib/email-verification.ts` |
| Firanṣẹ koodu igbagbe ọrọ igbaniwọle | 1 igba/iṣẹmu/IP | `src/app/api/auth/forgot-password/route.ts` |
| Wiwọle | 5 igba/iṣẹmu/IP; akọọlẹ kanna ti o ba kuna ni itẹlera **5 yoo dii pa fun iṣẹju 30** (423), lakoko iye ti o ku n dinku lati ṣafihan | `src/app/api/auth/login/route.ts`, `rate-limit.ts` |

**Ihuwasi aabo ikọkọ**: nigbati a ba n firanṣẹ koodu ijẹrisi / igbagbe ọrọ igbaniwọle, ti imeeli ba ti forukosile tabi ko si, aaye naa da idahun aṣeyọri kanna pada, ko ṣafihan boya imeeli ti forukosile.

## Ibamu ti ipo agent-oluranlọwọ ati iforukosile oju-iwe

Iwe skill n pe **ṣeto kanna ti awọn API gbangba** (`/api/auth/register`, `send-code`, `login`,
`/api/auth/me`), ati pe ifisilẹ fọọmu oju-iwe n lọ nipasẹ awọn ayẹwo, ihamọ, ati ọna aṣiṣe kanna — gbogbo
awọn ofin faili yii ko ṣe iyatọ si awọn ọna mejeeji. Ṣiṣan akoko ati adehun aṣẹ iwe wo `references/agent-flow.md`.

## Ilana Ipo Lẹhin Iforukọsilẹ Ṣaṣeyọri

> **Akoko idanwo ọfẹ (bẹrẹ 2026-10-18; ihuwasi sajoo gidi ni o ṣe): akanti tuntun ti o forukọsilẹ le **lo gbogbo ẹya taara**
> (ifeede, maapu, ẹda oni-nọmba, awọn abẹwo, ati bẹbẹ) laisi owo; awọn akanti ti ko sập ko ni idi mọ lori ojú-iwe akoonu. "Idinamọ pending"
> ti a ṣalaye ni abala yii jẹ ipo deede lẹhin akoko idanwo pari — nigbati akoko na de, ihuwasi ori-ayelujara gidi ni o ṣe.

1. Olumulo fi pamọ pẹlu `accountStatus: 'pending'` ati **aami ipilẹ 3** (ọna forukọsilẹ).
2. Olupin gbin kuki HttpOnly meji pẹlu: JWT (le wọle ojú-iwe taara) ati pendingUserToken (ẹri idanimọ fun ilana sập).
3. Ni ipo deede (akoko idanwo pari / ko si akoko ọfẹ), ojú-iwe iforukọsilẹ ri `pending_payment` → pada si `/subscription`
   (ti ipadabọ `next`); ni ipo iranlọwọ-ajanṣan, `me?token=…&redirect=/subscription` gba ipa kan.
   **Ni akoko idanwo ọfẹ igba yii ko ṣiṣẹ** — lẹhin forukọsilẹ, lọ taara si ojú-iwe ile ki o bẹrẹ lilo.
4. Owo pari → `accountStatus` di `active` (**Alipay ṣiṣẹ laifọwọyi ẹgbẹ olupin nipasẹ notify**;
   PayPal ṣiṣẹ nipasẹ Webhook; koodu WeChat QR jẹrisi ni ọwọ; Huawei IAP kọja nipasẹ `activate-huawei`).
   Wo `payment-and-activation.md` fun alaye.

Ni ipo deede, awọn olumulo ti ko ṣiṣẹ (pending) ti n pe API ipilẹ (ifeede, maapu, iwiregba ẹda oni-nọmba, awọn abẹwo, ati bẹbẹ) gba 403;
awọn ọna ifiweranṣẹ pinyẹẹ jẹ aṣẹ (jẹ gbangba). Ni akoko idanwo ọfẹ idinamọ yii duro ati gbogbo rẹ ṣi.
## Tabili ṣiṣayẹwo awọn aṣiṣe ti o wọpọ

| Iṣẹlẹ | Idi | Kí lè ṣe |
|---|---|---|
| 「用户名已存在」 (oruko olumulo ti wa tẹlẹ) | Oruko olumulo ti gba (laibikita nla-kekere) | Paṣẹ oruko olumulo miran |
| 「邮箱已被使用」 (imeeli ti a ti lo) | Imeeli ti forukosile tẹlẹ | Paṣẹ imeeli miran; tabi yi lọ si wiwọle + "igbagbe ọrọ igbaniwọle" lati gba akọọlẹ atijọ pada |
| 「邮箱验证码错误或已过期」 (koodu ijẹrisi imeeli jẹ aṣiṣe tabi ti di ofo) | Nọmba ti ko tọ / ju iṣẹju 10 / awọn igbiyanju ju 5 lọ ti kọ | Tẹ "tun ranṣẹ", lo imeeli **ti o padà julọ** |
| Gbigba koodu ijẹrisi imeeli | Ihamọ iṣẹju 60; tabi wọ inu idọti/ipolowo | Duro ki iṣiro pada ki o to ranṣẹ; wo folda idọti imeeli |
| 「手机号已被使用」 (nọmba foonu ti a ti lo) | Nọmba foonu ti so akọọlẹ miiran | Nu nọmba foonu (iyanjiyan) tabi paṣẹ miran |
| 「注册请求过于频繁」/ 429 (ibiṣẹ iforukosile pupọ ju / 429) | Iforukosile 3 igba/iṣẹmu/IP ti de | Duro iṣẹju diẹ ki o to tun gbiyanju |
| 409「用户名或邮箱已被注册」 (409 oruko olumulo tabi imeeli ti forukosile) | Ni akoko ifisilẹ o ja pẹlu ẹlomiran (aabo ifẹhinti) | Paṣẹ oruko olumulo tabi imeeli miran ki o to tun gbiyanju |
| 「图片大小不能超过5MB」/「不支持 SVG」 (aworan ko le tobi ju 5MB / ko ṣe atilẹyin SVG) | Aworan profaili ko tọ | Paṣẹ aworan miran tabi fo apakan aworan profaili |
| Olumulo tẹ ọna iwọle ṣugbọn gbalẹ lori ojú-iwe sập (dipo ojú-iwe ile) | Akoko idanwo ọfẹ ti pari ati odidi owo sajoo pada | Tẹle Igba 7 ninu SKILL.md fun ilana owo sập; lẹhin sập, ṣiṣẹ `refresh-login` lẹhinna fi ọna ojú-iwe ile ranṣẹ |
| Forukọsilẹ ṣaṣeyọri ṣugbọn iwọle pada 403 "请完成订阅以激活账户" | Akanti wa ni pending, ati sajoo ko si ni akoko idanwo ọfẹ (ipo ti a reti ṣaaju owo) | Ko ṣẹlẹ ni akoko idanwo ọfẹ; ti o ba ṣẹlẹ, akoko idanwo ti pari — pari sập kọọkan; ti 504 ba wa lẹhin owo, JWT atijọ lo — ni ipo iwe ṣiṣẹ `refresh-login` kọọkan lati paṣiparọ fun ipo iwọle titun |
| Wiwọle 423「账户已锁定」 (akọọlẹ ti dii pa) | Ọrọ igbaniwọle kuna ni itẹlera 5 | Duro iṣẹmu 30 |
| Wiwọle 401「还剩 N 次尝试机会」 (o ku N awọn aye igbiyanju) | Ọrọ igbaniwọle ko tọ, sunmọ didii pa | Ronu daradara ki o to gbiyanju, tabi lọ taara si "igbagbe ọrọ igbaniwọle" |
| 「该账号未设置密码，请使用其他方式登录」 (akọọlẹ yii ko ṣe eto ọrọ igbaniwọle, jọwọ lo ọna wiwọle miiran) | Akọọlẹ ẹnikẹta (Google/Watcha/Huawei) | Lo bọtini wiwọle ẹnikẹta atilẹba |
| 「该账号已注销」 (akọọlẹ yii ti parẹ) | Akọọlẹ ti deactivate | O nilo iforukosile tuntun |

## Imọ-wiwọle kekere ti wiwọle (iranlọwọ ṣiṣayẹwo)

Wiwọle ṣe atilẹyin igbewọle **oruko olumulo / imeeli / nọmba foonu** (eyikeyi ninu mẹta le ṣiṣẹ bi oruko akọọlẹ).
Igbagbe ọrọ igbaniwọle: oju-iwe wiwọle → "igbagbe ọrọ igbaniwọle" → tẹ imeeli iforukosile ranṣẹ nọmba oni-nọmba 6 → tun ṣeto.
