# የደንበኝነት ማንቃትና ክፍያ — powpow-register

## ማጠቃለያ (መልሱ ቀደም ብሎ)
> **ነጻ የሙከራ ወቅት (ከ 2026-10-18 ጀምሮ፤ የመድረኩ ትክክለኛ ባህሪይ ይቀዳል)**፦ በዚህ ወቅት የተመዘገበ መለያ ሁሉንም ባህሪያት በቀጥታ መጠቀም ይችላል፣ እና **መደነቅ አማራጽ ማሻሻያ ነው አይደለም ግዴታ** — ተጠቃሚው ራሱ አባልነት ሲፈልግ ብቻ የዚህን ፋይል ፍሰት ተከተል። የሙከራ ወቅቱ ሲያልቅ፣ ያልተመዘገቡ መለያዎች የሚጨርሱበትን ጊዜ ወደ ደንበኝነት ገጽ ይመለሳሉ፤ በዚህ ፋይል መሠረት ደንበኝነቱን ጨርስ።


**አሊፓይና PayPal ደንበኝነት ሁለቱም አሁን በወኪሉ ሊስተናገዱ ይችላሉ — ትዕዛዝ መፍጠርና ገንዘብ መግባት መከታተልን ጨምሮ።**
አሊፓይ ለቻይና ሀገር ውስጥ ተጠቃሚዎችና አሊፓይ ላላቸው ተጠቃሚዎች አንዴ በመክፈል ሲሆን በራስ አይታደስም፤ PayPal በየወሩ በራስ ያድሳልና በማንኛውም ጊዜ ሊሰረዝ ይችላል፣
ለውጭ አገር ተጠቃሚዎችና አሊፓይ ለሌላቸው ተጠቃሚዎች ነው። የ WeChat QR ኮድ (በእጅ ማረጋገጥ) እና የሃዋዌ IAP አሁንም አሉ፣ ግን በ skill አይተይዙም።

የክፍያ ክፍሉ የኃላፊነት ገደብ፦ ወኪሉ **ትዕዛዝ መፍጠር፣ የክፍያ ገጽ መክፈት፣ ገንዘብ መግባቱን መፈተሽ** ይችላል፤ የተጠቃሚውን የአሊፓይ/PayPal
መለያ/የክፍያ ማረጋገጫ **በጭራሽ** አያነካም፣ በጭራሽም «በምትሆን እከፍላለሁ» አይልም። የክፍያ ተግባሩ ለዘላለም በተጠቃሚው ራሱ በይፋዊ የክፍያ ገጽ ይከናወናል።

## የአሊፓይ መስመር (vibepay፣ ዋና)

የአንድ ጊዜ ግዥ-ሙሉ፦ አንዴ በመክፈል ለተጠቀሰው ጊዜ ይከፈታል፣ **በራስ አይታደስም**። ጥቅሎቹ በ
`src/lib/alipay-vibepay.ts` (በ `ALIPAY_PACKAGES`) ተጽፈዋል፦

| key | planId | ስም | ዋጋ | ቆይታ |
|---|---|---|---|---|
| `monthly` | alipay-monthly | ወርሃዊ አባልነት | ¥6.99 | 30 ቀናት |
| `quarterly` | alipay-quarterly | ሩብ-ዓመት አባልነት | ¥19.99 | 90 ቀናት |
| `yearly` | alipay-yearly | ዓመታዊ አባልነት | ¥69.99 | 365 ቀናት |

### የበር ውል (የ skill ስክሪፕቱ አስቀድሞ አስተናግዷል፣ ወኪሉ ጥያቄን በቀጥታ አይሰራም)

| በር | መንገድ | ማብራሪያ |
|---|---|---|
| `/api/payment/alipay/create-order` | POST | `Authorization: Bearer <JWT>` ያስፈልገዋል (pending ተጠቃሚ በቂ ነው)። body `{package}` → `{paymentHtml, outTradeNo, amount, planName}` ይመልሳል፤ `paymentHtml` ወደ አሊፓይ በር በራስ-ሰር የሚገባ የቅጽ ገጽ ነው |
| `/api/payment/alipay/query` | GET `?outTradeNo=` | ተመሳሳይ Bearer ማረጋገጫ። `paid` / `pending` / `closed` / `unknown` ይመልሳል |
| `/api/payment/alipay/notify` | POST (የአሊፓይ ሰርቨር ጥሪ) | የፊርማ ማረጋገጫ አምስት ጉዳዮች (ፊርማ፣ app_id፣ የመጠን ተመሳሳይነት፣ TRADE_SUCCESS/TRADE_FINISHED፣ የነጋዴ ብቸኝነት) → **መደገም-ተከላካይ** የትዕዛዝ ማዘመን + ደንበኝነት መፍጠር + መለያ ማንቃት። skill ይህንን በር ለዘላለም አያነካም |
| `/payment/alipay/return` | የአሳሽ መመለሻ ገጽ | ክፍት መንገድ፤ ከክፍያ በኋላ «ክፍያ ተሳክቷል» ማረጋገጫ ያሳያል፤ ገጹ በውስጡ የጀርባውን ትክክለኛ ሁኔታ መጠየቅ ይቀጥላል |

- ያልተከፈለ ትዕዛዝ **በ 2 ሰዓት በራስ ይዘጋል**፤ ተጠቃሚው በመካከል ሲተው → በቀጥታ ዳግም `create-order`፣ አሮጌውን ማስተካከል አያስፈልግም።
- ስክሪፕቱ `paymentHtml` ን ወደ ጊዜያዊ HTML ፋይል ጽፎ ወኪሉ በስርዓት ትዕዛዝ በመክፈት ወደ አሊፓይ የክፍያ ገጽ መግባት ይችላል
  (QR በማሰር ወይም በአሊፓይ ውስጥ ገብቶ በመክፈል)።

### የማንቃት ሰንሰለት (በራስ-ሰር፣ በእጅ ማድረግ አያስፈልግም)

የ notify ፊርማ ሲያልፍ → `paymentOrders` የተከፈለ ማለት ይሰበሰባል → `user_subscriptions` ይፈጠራል/ይራዘማል
(`planId`፣ `currentPeriodEnd` በ durationDays የሚሰላ፤ ማደስ በዐመታዊው ማበቂያ ቀን ላይ ይራዘማል) →
`users.accountStatus: active` + `subscriptionStatus: ACTIVE` → መመለሻ ገጹ paid ሲሆን ስኬት ያሳያል።

### ከክፍያ በኋላ አዲስ የመግቢያ ሁኔታ መቀየር ግዴታ ነው (አስፈላጊ)

JWT ውስጡ የደንበኝነት አባልነት አለው (pending መለያ `NONE` ነው)። **የክፍያ ገንዘብ መግባት የመረጃ ቋቱን ብቻ ያዘምናል፣ አስቀድሞ
የተሰጠውን JWT አይቀይርም** — የአሮጌው ቶከን አባልነት አሁንም NONE ነው፤ በቀጥታ በእሱ የመግቢያ አገናኝ ማዘጋጀት «አባል አይደለም» ይመስላል።
ስለዚህ skill ው `paid` / PayPal `ACTIVE` ከተረጋገጠ በኋላ መጀመሪያ `refresh-login` ያሂዳል (ዳግም መግባት አዲስ JWT፣ አባልነቱ ACTIVE ይሆናል)፣
ከዚያ አገናኝ 2 ይፈጥራል። ይህ የንድፍ ባህርይ ነው፣ የችግር ማስተካከያ አይደለም።

## የ PayPal ደንበኝነት መስመር (በወኪሉ የሚስተናገድ፤ ዌብ፣ ሃርሞኒየስ አልባ)

አንድ እቅድ ብቻ ነው ያለው፣ Premium Monthly (በግምት $1/ወር፣ `/api/subscription/plans` እንደሚመልሰው)፤ **በየወሩ በራስ ያድሳል**
ተጠቃሚውም በ PayPal መለያው ውስጥ በማንኛውም ጊዜ ሊሰርዘው ይችላል።

### የ API ውል (በስኪሉ ስክሪፕት ተጠቅሏል፤ ወኪሉ በቀጥታ ጥያቄ አያሰባስብም)

| መጨረሻ ነጥብ | ዘዴ | ማስታወሻ |
|---|---|---|
| `/api/subscription/plans` | GET | Bearer ማረጋገጫ፤ ያሉትን እቅዶች ዝርዝር ይመልሳል (አሁን 1 ብቻ) |
| `/api/subscription/create` | POST | አካል `{planId}` → `{subscriptionId, approveUrl, status}` ይመልሳል፤ `status` አብዛኛውን ጊዜ `APPROVAL_PENDING` ነው |
| `/api/subscription/create` | GET | Bearer ማረጋገጫ፤ `{activeSubscription, allSubscriptions}` ይመልሳል፤ ወኪሉ `activeSubscription.subscription.status === 'ACTIVE'` ን ይጠይቃል |
| `/api/subscription/verify` | POST | በስኬት ገጹ (ከኩኪ ጋር) በራስ ይጠራል፤ webhook ሳይደርስ በ PayPal API በቀጥታ ያነቃል |
| `/subscription/success` | የአሳሽ መመለሻ ገጽ | ከ PayPal ፍቃድ በኋላ መድረሻ ገጽ፤ verify ን በራስ ይጠይቅና ወደ መነሻ ገጽ / ወደነበረበት ገጽ ይመለሳል |
| `/subscription/cancel` | የአሳሽ ገጽ | ተጠቃሚው ሲሰርዝ ወይም ሲወድቅ መድረሻ ገጽ፤ አዲስ ሙከራ መጀመር ይቻላል |

### የወኪል ፍሰት

```
create-order --provider paypal   # → approveUrl ይመልሳል፣ በአካባቢ HTML ፋይል ውስጥ ይጻፋል
open the HTML file               # → አሳሹ ወደ PayPal ፍቃድ ገጽ ይዘላል
query (በየ 10–15s)               # → ACTIVE እስኪሆን ድረስ ይጠይቁ
refresh-login                    # → አዲስ JWT (የደንበኝነት ጥያቄ ACTIVE)
login-link --target home         # → ይፋዊ የመግቢያ አገናኝ ያመነጫል
```

- በ 1 ሰዓት ውስጥ ያልተጠናቀቁ PENDING ደንበኝነቶች በኋለኛው ክፍል በራስ ይጸዳሉ፤ እንደገና ይጀምሩ።
- ተጠቃሚው ዳግም `create-order` ካሄደ፣ ኋለኛው ክፍል አሁንም ሕጋዊ የሆነውን `APPROVAL_PENDING` ደንበኝነት እንደገና ይጠቀማል፣ 409 ን ያስወግዳል።
- ከአሊፓይ ጋር ተመሳሳይ፦ ገንዘብ መግባቱ ዳታቤዝን ብቻ ያዘምናል — አሮጌ JWT በራስ አይታደስም፣ ስለዚም የመነሻ ገጽ አገናኝ ከመላክዎ በፊት `refresh-login` ማሄድ **አስፈላጊ** ነው።

## የደንበኝነት ገጽ አራት መስመሮች

የደንበኝነት ገጹ `src/app/(public)/subscription/page.tsx` በሥራ አካባቢው መሠረት ያሳያል፦

| መስመር | አካባቢ | ሜካኒዝም | የማንቃት መንገድ |
|---|---|---|---|
| **አሊፓይ (ዋና)** | የዌብ ገጽ | `AlipayPaymentSection` የ vibepay በሮችን ይጠቀማል (ከላይ ያለው ሠንጠረዥ) | የ notify ሰርቨር በራስ-ሰር ማንቃት፣ በሰከንድ መጠን |
| PayPal ደንበኝነት | የዌብ ገጽ (ሃርሞኒየስ አልባ) | `/api/subscription/create` → ወደ PayPal ፍቃድ መሄድ፤ በየወሩ በራስ ማደስ በማንኛውም ጊዜ ሊሰረዝ ይችላል (`/api/subscription/manage`) | PayPal Webhook (`BILLING.SUBSCRIPTION.*`) በራስ active ያደርገዋል |
| የ WeChat QR ደንበኝነት | የዌብ ገጽ (ሃርሞኒየስ አልባ) | በገጹ ግርጌ «የ WeChat QR ደንበኝነት»፦ QR በማሰር ማስተላለፍ | **በእጅ ማረጋገጥ**፣ ገንዘብ መግባቱ ሊዘገይ ይችላል፤ ከክፍያ ወዲያውኑ አልተሳካም ብለው አይወስኑ |
| የሃዋዌ የመተግበሪያ ውስጥ ግዥ | በሃርሞኒየስ መተግበሪያ ውስጥ | ዐቀፉ `NativeBridge.purchaseSubscription()` | `/api/subscription/activate-huawei` የሃዋዌውን ትዕዛዝ ካረጋገጠ በኋላ ያነቃል |

የ PayPal እቅዶችና ዋጋዎች ከ `/api/subscription/plans` በተለዋዋጭ ይነበባሉ፤ የገጹ ቋላሚ ጽሑፍ፦ Auto-renews. Cancel anytime.

## ሁኔታና መዘዋወር

- አሊፓይ ከተከፈለ → መመለሻ ገጹ ስኬት ያሳያል፤ PayPal ሲሳክ → `/subscription/success` → መለያው active →
  በራስ-ሰር ወደ `next` ክርክሩ የጠቀሰው ዐመታዊ ገጽ ይመለሳል (ከሌለ ወደ መነሻ ገጽ)።
- ደንበኝነት ያለው ተጠቃሚ ደግሞ የደንበኝነት ገጽ ሲጎበኝ → "You're All Set!" ያሳያል፣ ከ 3 ሰከንድ በኋላ በራስ ወደ መነሻ ገጽ ይመለሳል።
- ክፍያ ሲወድቅ/ሲሰረዝ (PayPal) → `/subscription/cancel`፣ ዳግም መጀመር ይቻላል።

## አፈታት

| ምልክት | አፈታት |
|---|---|
| አሊፓይ ከተከፈለ `query` አሁንም pending | የ notify መዘግዮት በጣም አልፎ አልፎ ነው፤ 30 ሰከንድ ይጠብቀው እንደገና ይጠይቁ። እንደቀጠለ ተጠቃሚው ወደ አሳሹ ተመልሶ የመመለሻ ገጹን ሁኔታ ይመልከቱ፣ እንደቀጠለ የመድረኩን ድጋፍ ያግኙ (dongtao@outlook.com)፣ `outTradeNo` ን ይንገሩ |
| አሊፓይ ተከፍሏል፣ በአገናኝ 2 ገብተው አሁንም ተከልክለዋል | `refresh-login` አልሮጦም (የአሮጌ JWT አባልነት አልተዘመነም) — መጀመሪያ `refresh-login` ከዚያ `login-link` |
| PayPal `query` በ PENDING ላይ ቆየ | ተጠቃሚው በ PayPal ውስጥ ፍቃዱን አላጠናቀቀም፤ የፍቃድ አገናኙ በአሳሹ ተከፍቶ እንደነበር ያረጋግጡ። ከፈቀደ በኋላም PENDING ከሆነ webhook ሊዘገይ ይችላል — ተጠቃሚው በስኬት ገጹ ላይ ጥቂት ሰከንድ ይጠብቅ ወይም ያድስ |
| PayPal `query` 409 መለሰ | ያልተጠናቀቀ PENDING ደንበኝነት አለ፤ 1 ሰዓት ይጠብቁ እስኪያልቅ ድረስ፣ ወይም የአሮጌውን አገናኝ ፍቃድ በአሳሹ ያጠናቅቁ |
| PayPal ተከፍሏል፣ አገናኝ 2 ላይ ግን አሁንም ተከልክሏል | ከአሊፓይ ጋር ተመሳሳይ፦ መጀመሪያ `refresh-login` ከዚያ `login-link` |
| ተከፍሏል ግን አሁንም 403 (PayPal) | Webhook አልፎ አልፎ ይዘጋዛል፣ ዳግም ግብተው ሁኔታውን ያድሱ |
| በ WeChat ተከፍሏል ግን አልተከፈተም | በእጅ ማረጋገጡ ያልተመሳሰለ ነው፤ በጥቂት ሰዓታት ውስጥ ካልተከፈተ የመድረኩን ድጋፍ ያግኙ |
| የደንበኝነት ገጹ "No subscription plans available" ሲል | በ `/api/subscription/plans` ውስጥ የሚጠቀሙ የ PayPal እቅዶች የሉም፣ በመድረኩ በኩል የማዋቀር ችግር ነው፤ የቻይና ተጠቃሚዎች ወደ አሊፓይ ተመልሰው በቂ ነው |

## የታሪክ ማስታወሻ

በኮዱ ውስጥ ተጨማሪ **የድሮ** የአሊፓይ የዌብ ክፍያ አለ (`src/lib/alipay.ts`፣ `/api/payment/create-order`፣
¥9.90/¥99 የአንድ ጊዜ ግዥ-ሙሉ፣ ሳንድቦክስ ቁልፍ ሳይሰጥ ሲቀር ወደ ማስመሰለት ክፍያ ይወርዳል)፣ ወደ የደንበኝነት ገጹ UI ግን በጭራሽ
አልተገናኘም፣ ከ vibepay ጋር ግንኙነት የለውም። skill ይህንን ሁልጊዜ አያነካውም፤ `alipay-vibepay.ts` ነው የአሁኑ መስመር።

