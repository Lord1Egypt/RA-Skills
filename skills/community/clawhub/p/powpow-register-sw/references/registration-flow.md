# Maelezo ya kina ya mtiririko wa usajili — powpow-register

Kwa kuangalia wakati wa utatuzi wa matatizo. Sheria zote zinatoka kwenye msimbo wa jukwaa (ukaguzi wa ufanisi wa Next.js ya mbele na nyuma), zimeweka chanzo. Wakati jukwaa linaposasisha, fuata tabia halisi ya mtandaoni.

## Ingia

- Ukurasa wa usajili: https://global.powpow.online/register
- Ukurasa wa ingia: https://global.powpow.online/login
- Ukurasa wa usajili wa malipo: https://global.powpow.online/subscription
- Ikiwa unaingia kutoka kiungo cha kushiriki chenye `?next=...`, baada ya usajili + malipo kukamilika utaelekezwa kurudi kwenye ukurasa wa awali.

## Sehemu za fomu na sheria

| Sehemu | Inahitajika | Sheria | Chanzo la msimbo |
|---|---|---|---|
| Picha ya wasifu | Hiari | Picha <=5MB, haiauni SVG; seva inabanaa kiotomatiki (ikibaki >100KB inabanaa hadi 400×400 / ubora 90) | `src/app/api/auth/register/route.ts` |
| Jina la mtumiaji | Inahitajika | Herufi 2~50, baada ya kukata na kupunguza nafasi hubadilishwa kuwa **herufi ndogo** kuhifadhiwa (Tom na tom zinaongewa jina moja la mtumiaji, upande wa usajili na upande wa ingia havijali herufi kubwa ndogo) | sawa (zod schema) |
| Nenosiri | Inahitajika | Vipimo 8~100, lazima iwe na herufi kubwa, herufi ndogo, na tarakimu kwa pamoja | sawa |
| Thibitisha nenosiri | Inahitajika | Inafanana na nenosiri (ukaguzi wa upande wa mbele tu) | `src/app/(public)/register/page.tsx` |
| Jina la kirafiki | Hiari | <=100 herufi; usipojaza chaguo-msingi huchukua jina la mtumiaji | register route |
| Barua pepe | **Inahitajika** | Fomati ya barua pepe halali, <=255 herufi; barua pepe moja inaweza kusajili akaunti moja tu | register route |
| Nambari ya uthibitisho ya barua pepe | **Inahitajika** | Tarakimu 6; **inayofaa kwa dakika 10**; baada ya kuthibitishwa kwa mafanikio inaachwa; kutuma tena kutaalamu nambari ya zamani kuwa imekuwa matumizi | `src/lib/email-verification.ts` |
| Nambari ya simu | Hiari | Nambari ya simu ya bara `1[3-9]` inaanza jumla ya tarakimu 11; nambari ya simu moja inaweza kufunga akaunti moja tu | register route |

Ukurasa pia una vitufe vitatu vya ingia ya watu wa tatu: **Google, Watcha, Huawei** (`GoogleSignInButton` /
`WatchaLoginButton` / `HuaweiLoginButton`). Akaunti za watu wa tatu hazina nenosiri ya ndani, baadaye kutumia nenosiri ya ingia kutatoa
`该账号未设置密码，请使用其他方式登录` (akaunti hii haijaweka nenosiri, tafadhali tumia njia nyingine ya kuingia).

## Vizuizi na vipingamizi vya uchambuzi

| Kitendo | Kizuizi | Chanzo |
|---|---|---|
| Kuwasilisha usajili | **mara 3 kwa dakika/IP**, ikipita 429 | `src/lib/rate-limit.ts` `REGISTER_RATE_LIMIT` |
| Kutuma nambari ya uthibitisho | IP moja mara 1 kwa dakika **na** barua pepe moja mara 1 kwa dakika, ikipita 429; kitufe cha mbele kuhesabu nyuma sekunde 60 | `src/app/api/auth/register/send-code/route.ts` |
| Uchunguzi wa nambari ya uthibitisho | Kila barua pepe ndani ya dakika 10 majaribio hadi **mara 5**, kufikia kikomo hata nambari ikiwa sahihi itakataliwa, inahitaji kutuma nambari mpya | `src/lib/email-verification.ts` |
| Kutuma nambari ya kusahau nenosiri | Mara 1 kwa dakika/IP | `src/app/api/auth/forgot-password/route.ts` |
| Ingia | Mara 5 kwa dakika/IP; akaunti moja ikishindwa mfululizo **mara 5 itafungwa kwa dakika 30** (423), wakati huo idadi iliyobaki inapungua kuonyesha | `src/app/api/auth/login/route.ts`, `rate-limit.ts` |

**Tabia ya ulinzi wa faragha**: wakati wa kutuma nambari ya uthibitisho / kusahau nenosiri, ikiwa barua pepe imeshajiliwa au haipo, kiolesura kinarudisha ujumbe wa mafanikio sawa, haifichui iwapo barua pepe imeshajiliwa.

## Usawa wa mtindo wa agent-kusaidia na usajili wa wavuti

Hati za skill zinapiga simu **seti ile ile ya API za wazi** (`/api/auth/register`, `send-code`, `login`,
`/api/auth/me`), na ukurasa wa usajili wa fomu unapita njia ile ile za ucahiliji, vizuizi, na makosa — yote
sheria za faili hii ni sawa kwa njia zote mbili. Mlolongo na mkataba wa amri za hati angalia `references/agent-flow.md`.

## Mtiririko wa Hali Baada ya Usajili Kufanikiwa

> **Kipindi cha majaribio bila malipo (kuanzia 2026-10-18; tabia halisi ya jukwaa ndiyo inayotawala)**: akaunti mpya iliyosajiliwa inaweza **kutumia kila kipengele moja kwa moja**
> (mlipuko, ramani, binadamu wa digitali, viingilio, n.k.) bila malipo yanayohitajika; akaunti zisizo na sasiri hazifungwi tena kwenye kurasa za maudhui. "Kuzuia kwa pending"
> kunaelezewa katika sehemu hii ni hali ya kawaida baada ya kipindi cha majaribio kukamilika — wakati huo unapofika, tabia halisi ya mtandaoni ndiyo inayotawala.

1. Mtumiaji huhifadhiwa na `accountStatus: 'pending'` na **beji 3 za mwanzo** (njia ya register).
2. Seva pia huzalisha vuki viwili vya HttpOnly: JWT (inaweza kufikia kurasa moja kwa moja) na pendingUserToken (cheti cha utambulisho cha mtiririko wa sasiri).
3. Katika hali ya kawaida (kipindi cha majaribio kimeisha / hakuna kipindi cha bila malipo), ukurasa wa usajili hugundua `pending_payment` → inaelekeza kwenye `/subscription`
   (ikihifadhi kigezo cha kurudi `next`); katika hali ya wakala-msaidizi, `me?token=…&redirect=/subscription` hupata athari sawa.
   **Katika kipindi cha majaribio bila malipo hatua hii haichochei** — baada ya kujiandikisha, nenda moja kwa moja kwenye ukurasa wa nyumbani na uanze kutumia.
4. Malipo yamekamilika → `accountStatus` inakuwa `active` (**Alipay huwasha kiotomatiki upande wa seva kupitia notify**;
   PayPal huwasha kupitia Webhook; msimbo wa QR ya WeChat huthibitishwa kwa mikono; Huawei IAP hupitia `activate-huawei`).
   Ona `payment-and-activation.md` kwa maelezo.

Katika hali ya kawaida, watumiaji wasio na shughuli (pending) wanaoitia API za msingi (mlipuko, ramani, mazungumzo ya binadamu wa digitali, viingilio, n.k.) hupata 403;
viungo vya machapisho yaliyogawanywa ni ubaguzi (vinahifadhiwa kupatikana hadharani). Katika kipindi cha majaribio bila malipo kuzuia hii kunasimamishwa na kila kitu kimefunguliwa.
## Jedwali la utatuzi wa makosa ya kawaida

| Tukio | Sababu | Fanya nini |
|---|---|---|
| 「用户名已存在」 (jina la mtumiaji limeshakuwepo) | Jina la mtumiaji limechukuliwa (bila kujali herufi kubwa ndogo) | Badilisha jina la mtumiaji |
| 「邮箱已被使用」 (barua pepe imeshatumiwa) | Barua pepe imeshajiliwa | Badilisha barua pepe; au badili kwenda ingia + "sahau nenosiri" kurejesha akaunti ya zamani |
| 「邮箱验证码错误或已过期」 (nambari ya uthibitisho ya barua pepe ni mbaya au imeisha muda) | Nambari imeingizwa vibaya / imepita dakika 10 / imejaribiwa zaidi ya mara 5 ikakataliwa | Bofya "tuma tena", tumia nambari ya barua pepe ya **tafsiri ya hivi karibuni** |
| Hauskii nambari ya uthibitisho | Kizuizi cha sekunde 60; au imeingia kwenye taka/utangazaji | Subiri muda wa kuhesabu nyuma uishe kisha tuma; angalia folda ya taka za barua pepe |
| 「手机号已被使用」 (nambari ya simu imeshatumiwa) | Nambari ya simu imeshafungwa akaunti nyingine | Futa nambari ya simu (ni hiari) au badilisha nambari |
| 「注册请求过于频繁」/ 429 (ombi la usajili mara nyingi mno / 429) | Usajili mara 3 kwa dakika/IP umefikia kilele | Subiri dakika chache kisha jaribu |
| 409「用户名或邮箱已被注册」 (409 jina la mtumiaji au barua pepe imeshajiliwa) | Wakati wa kuwasilisha umepigana na mwingine (ulinzi wa mshindani) | Badilisha jina la mtumiaji au barua pepe kisha jaribu tena |
| 「图片大小不能超过5MB」/「不支持 SVG」 (picha haiwezi kuwa kubwa zaidi ya 5MB / haiungi mkono SVG) | Picha ya wasifu haifai | Badilisha picha au ruka sehemu ya picha ya wasifu |
| Mtumiaji anabonyeza kiungo cha kuingia lakini anatua kwenye ukurasa wa sasiri (badala ya ukurasa wa nyumbani) | Kipindi cha majaribio bila malipo kimekamilika na ukuta wa malipo wa jukwaa umerudi | Fuata Hatua 7 ndani ya SKILL.md kwa mtiririko wa malipo ya sasiri; baada ya kusajiri, endesha `refresh-login` kisha tuma kiungo cha ukurasa wa nyumbani |
| Usajili umefanikiwa lakini kuingia inarudisha 403 "请完成订阅以激活账户" | Akaunti bado iko pending, na jukwaa haliko katika kipindi cha majaribio bila malipo (hali inayotarajiwa kabla ya malipo) | Haitatokea katika kipindi cha majaribio bila malipo; ikitokea, kipindi cha majaribio kimekamilika — kamilisha sasiri kwanza; kama bado 403 baada ya malipo, JWT ya zamani ilitumika — katika hali ya hati endesha `refresh-login` kwanza kubadilishana hali mpya ya kuingia |
| Ingia 423「账户已锁定」 (akaunti imefungwa) | Nenosiri imeshindwa mara 5 mfululizo | Subiri dakika 30 |
| Ingia 401「还剩 N 次尝试机会」 (bado N ya nafasi za majaribio) | Nenosiri si sahihi, karibu kufungwa | Fikiria vizuri kisha jaribu, au nenda moja kwa moja kwenye "sahau nenosiri" |
| 「该账号未设置密码，请使用其他方式登录」 (akaunti hii haijaweka nenosiri, tafadhali tumia njia nyingine ya kuingia) | Akaunti ya mtu wa tatu (Google/Watcha/Huawei) | Tumia kitufe cha mtu wa tatu cha awali cha kuingia |
| 「该账号已注销」 (akaunti hii imefutwa) | Akaunti imefutwa (deactivate) | Inahitaji usajili mpya |

## Ujuzi mdogo wa ingia (kusaidia utatuzi)

Ingia inaauni ingizo moja la **jina la mtumiaji / barua pepe / nambari ya simu** (yoyote kati ya tatu inaweza kutumika kama jina la akaunti).
Sahau nenosiri: ukurasa wa ingia → "sahau nenosiri" → ingiza barua pepe ya usajili upokee nambari ya tarakimu 6 → weka upya.
