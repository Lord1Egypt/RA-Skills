# የወኪል ተይዞ የሚሠራ ሂደትና የስክሪፕት ውል — powpow-register

የ SKILL.md እያንዳንዱ ደረጃ የአፈጻጸም ዝርዝር። ሁሉም ትዕዛዞች `node scripts/powpow-register.mjs <ንዑስ-ትዕዛዝ> [ክርክሮች]` ቅርጸት አላቸው፣ ስክሪፕቱ **ዜሮ ጥገኛነት** አለው፣ **Node ≥ 18** ያስፈልገዋል፣ ሁሉም ጥሪዎች ወደ `https://global.powpow.online` ብቻ ይሄዳሉ።

## የደህንነት ንድፍ (ለምን እንዲህ እንደተነደፈ)

| ንድፍ | ምክንያት |
|---|---|
| የመግቢያ ቃል በአካባቢ ተለዋዋጭ `POWPOW_REGISTER_PASSWORD` በኩል ብቻ ይገባል | የሂደቱ ትዕዛዝ መስመር ክርክሮች ለተመሳሳይ ማሽን ሌሎች ሂደቶች ይታያሉ (የ argv የፍልሰት ገጽታ)፤ የአካባቢ ተለዋዋጭ ስክሪፕቱ ካነበው ወዲያውኑ ይጠቀምበታል |
| የመግቢያ ቃል **በጭራሽ ወደ ሁኔታ ፋይል አይጻፍም**፣ በሎግ አይታይም | የሁኔታ ፋይል በዲስክ ላይ ሊቀር ይችላል፤ በውይይቱ ውስጥ በመፍጠሪያ ሁነታ አንዴ ብቻ መታየቱ ተጠቃሚው እንዲያስቀምጥ ነው |
| የሁኔታ ፋይል በስርዓቱ ጊዜያዊ ማውጫ (`os.tmpdir()/powpow-register-state.json`፣ 0600) | አምስቱን መስኮች ብቻ ይዟል email / username / nickname / token / outTradeNo፤ `cleanup` በአንድ ጠቅታ ያጽዳቸዋል |
| ወኪሉ የተቀበለው JWT በብዙሃን `me?token=` በር በኩል ወደ አሳሽ cookie ይቀየራል | መድረኩ ለሃርሞኒየስ (HarmonyOS) WebView ያዘጋጀው ይፋዊ ድልድይ ነው፤ የፊርማ ማረጋገጫው ፊርማ + የኃይል ጊዜ ብቻ ያረጋግጣል፣ የመሣሪያ አሻራ አያስተሳስርም፣ ስለዚህ የተጠቃሚው አሳሽ መጠቀም ይችላል |
| ክፍያ create-order / query / የክፍያ ገጽ መክፈት ብቻ ነው | የክፍያ ተግባርና የክፍያ ማረጋገጫ ለዘላለም በተጠቃሚውና በአሊፓይ ይፋዊ የክፍያ ገጽ መካከል ብቻ ናቸው፤ ወኪል አያነካቸውም |

## የትዕዛዞች ማጣቀሻ

| ትዕዛዝ | ቁልፍ ክርክሮች | ተግባር / ጊዜ |
|---|---|---|
| `status` | —— | የሂደቱን እድገት ማየት (የሁኔታ ፋይልን ማንበብ)፤ ውይይቱ ከተቋረጠ በኋላ መጀመሪያ ይህን ያሂዱ |
| `gen-password` | —— | 24 ፊደላት ጠንካራ የመግቢያ ቃል ይፈጥራል (ትላልቅ + ትንሽ ፊደላት + ቁጥሮች)፤ stdout **ይህን አንዴ ብቻ** ያሳያል |
| `prepare-suggest` | `--username --nickname --email` | የተረጋገጠውን መረጃ ወደ ሁኔታ ፋይል ያስገባል (ከዚያ በኋላ register ዳግም መላክ አያስፈልገውም) |
| `send-code` | `--email` | መድረኩ 6-አሃያ የማረጋጋጫ ኮድ እንዲልክ ያነቃቃል (10 ደቂቃ ይጸናል፣ 60s ቀዝቃዛ ጊዜ) |
| `register` | `--code` (ግዴታ)፤ `--username --nickname --avatar --phone` (አማራጭ፤ በሁኔታ ፋይል ላይ ካሉ መላክ አያስፈልግም) | pending መለያ ይፈጥራል፤ የመግቢያ ቃል በ `POWPOW_REGISTER_PASSWORD` የአካባቢ ተለዋዋጭ በኩል፤ ሲሳክ JWT በራስ-ሰር ወደ ሁኔታ ፋይል ይቀመጣል |
| `login-link` | `--target pending` ወይም `--target home` | በአንድ ጠቅታ የመግቢያ ማለግጠፊያ ይፈጥራል (የሁለት ማለግጠፊያ ንድፍ፣ ከታች ተመልከት) |
| `create-order` | `--package monthly\|quarterly\|yearly` (የአሊፓይ ነባሪ)<br>`--provider alipay\|paypal` | የክፍያ ትዕዛዝ ይፈጥራል፤ አሊፓይ የክፍያ ገጽ ፋይል መንገድ + outTradeNo ይመልሳል፤ PayPal የፍቃድ ገጽ ፋይል መንገድ + subscriptionId ይመልሳል (በራስ-ሰር ወደ ሁኔታ ፋይል ይገባል) |
| `query` | —— | የትዕዛዝ/ደንበኝነት ሁኔታ ያረጋግጣል። አሊፓይ፦ `paid / pending / closed / unknown`፤ PayPal፦ `ACTIVE / PENDING`፤ በየ 10–15s ይጠይቁ |
| `refresh-login` | የመግቢያ ቃል በአካባቢ ተለዋዋጭ በኩል | ዳግም መግባት **አዲስ JWT** ለመቀየር (የደንበኝነት አባልነት ከ NONE ወደ ACTIVE ይቀየራል)፤ ገንዘብ ከገባ በኋላ መሮጥ አለበት |
| `whoami` | —— | በሁኔታ ፋይሉ ያለውን ቶከን በመጠቀም መለያና የደንበኝነት ሁኔታ ያረጋግጣል (ማንቃቱ እንደተሳካ ማረጋገጥ) |
| `cleanup` | —— | የሁኔታ ፋይል መሰረዝ (ሲዘጋ መሮጥ አለበት) |

**የአካባቢ ተለዋዋጭ ማስተላለፍ** (የመግቢያ ቃል በጭራሽ ወደ ትዕዛዝ መስመር አይደርስም)፦

```bash
# bash / zsh / WSL
POWPOW_REGISTER_PASSWORD='<የመግቢያ ቃል>' node scripts/powpow-register.mjs register --code 123456
# PowerShell
$env:POWPOW_REGISTER_PASSWORD = '<የመግቢያ ቃል>'; node scripts/powpow-register.mjs register --code 123456
# cmd
set POWPOW_REGISTER_PASSWORD=<የመግቢያ ቃል> && node scripts/powpow-register.mjs register --code 123456
```

## የሁለት ማለግጠፊያ ሥርዓተ ነገሮች (ዋና ንድፍ)

የመድረኩ የመግቢያ ሁኔታ HttpOnly ኩኪ ነው፣ ወኪሉ በቀጥታ ለአሳሹ ማስገባት አይችልም፤ ድልድዩ ብቁ
`/api/auth/me?token=<JWT>&redirect=<በሣይት ውስጥ መንገድ>` የመጨረሻ ነጥብ ነው፦ ፊርማ አረጋግጥ → ራስ-ሰር ፍጠር
ክፍለ ጊዜ → `Set-Cookie: powpow_token` (HttpOnly / SameSite=Lax / 7 ቀናት) → ተመላላሽ
አረጋግጥ (በአንድ ብቸኛ ሰላይ መጀመር አለበት፣ `//` እና የኋሊት ሰላዮች የተከለከሉ ናቸው፣ ከተተነተነ በኋላ same-origin መሆን አለበት) → ወደ ግቡ ገጽ 307 ጊዜያዊ ተመላላሽ።

የማለግጠፊያ ሁለት ግቦች አሉ፣ **በመጀመሪያ home ፍጠር፣ ከዚያ ተጠቃሚው ወዴት እንደወረደ በመመስረት pending ላይ መሄድ ወስን**፦

- **home ማለግጠፊያ (በነባሪ ይላካል፣ `--target home` → `/` ላይ ይወርዳል)**፦ ምዝገባው ከተሳካ ወዲያውኑ ይፈጠራል እና ለተጠቃሚው ይላካል።
  በነጻ የሙከራ ወቅት ተጠቃሚው ቀጥታ ወደ መነሻ ገጽ ይሄዳል፣ ሙሉ ተጠቃሚ፤ **ማለግጠፊያውን ጫኖ ወደ ደንበኝነት ገጽ ከወረደ — ነጻ የሙከራ ወቅቱ አልቋል** — ወደ የክፍያ ፍሰት ቀይር (ከታች ተመልከት)፤ ስክሪፕት መቀየር እና እንደገና መመዝገብ አያስፈልግም።
- **pending ማለግጠፊያ (በየክፍያ ፍሰት ይያዛል፣ `--target pending` → `/subscription` ላይ ይወርዳል)**፦
  የተጠቃሚው አሳሽ "ግማሽ-ገብቷል" ሁኔታ ይገባል፦ የደንበኝነት ገጽ እና የክፍያ ተመላላሽ ገጽ ይታያሉ እና ሊሠሩ ይችላሉ። ክፍያ ከደረሰ በኋላ፣
  ACTIVE መግለጫ ጋር አዲስ JWT ለመቀየር `refresh-login` አሂድ፣ ከዚያ ሙሉ የአባልነት ሁኔታ ለመፍጠር home ማለግጠፊያ እንደገና ላክ።

## ሙሉ ቅደም ተከተል

### ፈጣን መንገድ (በነጻ የሙከራ ወቅት — አብዛኞቹ ጉዳዮች)

```
1.  status                          # የአካባቢ ራስ-መረጋገጥ
2.  (ደረጃ 2 ውይይት መረጃውን ለማረጋገጥ፤ የይለፍ ቃል ማንኛውም፤ በመፍጠር ሁኔታ፦ gen-password → ተጠቃሚው ወዲያውኑ እንዲያስቀምጥ ጠይቅ)
3.  prepare-suggest --username U --nickname N --email E
4.  send-code --email E             # → ተጠቃሚው ኮዱን በኢንቦክስ ይመልከት (ውይይቱን የሚለቅበት ብቸኛው ጊዜ)
5.  POWPOW_REGISTER_PASSWORD=*** register --code 123456 [--avatar pic.jpg]
6.  login-link --target home        # → ማለግጠፊያውን ለተጠቃሚው ላክ፤ አንድ ጠቅታ ወደ መነሻ ገጽ
7.  (ተጠቃሚው ገብቷል ብሎ ያረጋግጣል) → ቀጥታ ጨርስ፦ cleanup + የመለያ ካርድ + የመጀመሪያ ደረጃዎችን አሳይ
```

### የክፍያ መንገድ (ተጠቃሚው አባልነት ሲፈልግ፣ ወይም ነጻ የሙከራ ወቅቱ ሲያልቅ)

```
1–5. እንደ ፈጣን መንገድ (register ከተሳካ በኋላ ሁኔታው አስቀድሞ ተከታታዩን ይይዛል)
6.  login-link --target pending     # → ግማሽ-መግቢያ ማለግጠፊያ፣ የክፍያ ተመላላሽ ገጽ እንዲሠራ ያደርጋል
7.  (ተጠቃሚው የክፍያ ዘዴ ይመርጣል)
    # Alipay: create-order --package monthly|quarterly|yearly
    # PayPal: create-order --provider paypal
8.  start <የክፍያ ገጽ ፋይል>       # Windows፤ macOS open ይጠቀም፣ Linux xdg-open
    # → ተጠቃሚው በ Alipay/PayPal የክፍያ ገጽ ክፍያ/ፈቃድ ይጨርሳል (ውይይቱን ይለቃል)
9.  query (በየ 10–15s) እስከ paid / ACTIVE
10. refresh-login                   # ACTIVE መግለጫ ጋር አዲስ JWT ቀይር
11. login-link --target home        # → ሙሉ-አባልነት ማለግጠፊያ ለተጠቃሚው ላክ
12. whoami                          # አረጋግጥ subscriptionStatus: ACTIVE (አማራጽ)
13. cleanup                         # የሁኔታ ፋይል አጽዳ
```
## ትዕዛዝ → የመድረክ API ካርታ

| የስክሪፕት ትዕዛዝ | የመድረክ በር |
|---|---|
| `send-code` | `POST /api/auth/register/send-code` |
| `register` | `POST /api/auth/register` (multipart፣ የመገለጫ ምስል ቀጥታ ማስገባት) |
| `login-link` | `GET /api/auth/me?token=…&redirect=…` (አገናኙ ራሱ፤ በአሳሽ ሲነካ ይሠራል) |
| `create-order` | `POST /api/payment/alipay/create-order` (Bearer, አሊፓይ)<br>`GET /api/subscription/plans` + `POST /api/subscription/create` (Bearer, PayPal) |
| `query` | `GET /api/payment/alipay/query?outTradeNo=…` (Bearer, አሊፓይ)<br>`GET /api/subscription/create` (Bearer, PayPal) |
| `refresh-login` | `POST /api/auth/login` (`{step:1, username, password}`) |
| `whoami` | `GET /api/auth/me?token=…` |

የሕጎች ምንጭ፦ የምዝገባ መስኮችና ገደቦች `registration-flow.md` ውስጥ፤ ጥቅሎችና የማንቃት ሰንሰለት `payment-and-activation.md` ውስጥ (ሁለቱም የመድረኩን የኮድ ፋይሎች ይጠቅሳሉ)።

## በስክሪፕት ደረጃ ስህተት አፈታት

| ምልክት | አፈታት |
|---|---|
| `Node 版本过低` (የ Node ስሪት በጣም ዝቅተኛ ነው) | ወደ ንጹህ መመሪያ ሁነታ ይመለሱ፣ አትገድዱ |
| የአውታረ መረብ ስህተት / ጊዜ መያዝ | አንዴ ይመንጨቱ፤ እንደቀጠለ ተጠቃሚው አውታረ መረቡን ካረጋገጠ በኋላ ይቀጥሉ (የሁኔታ ፋይሉ አለ፤ ከመጀመሪያው `status` ሮጦት ይመለሳል) |
| register የንግድ ስህተት ያሳያል (የተጠቃሚ ስም አስቀድሞ አለ ወዘተ) | በ SKILL.md ደረጃ 5 ሠንጠረዥ መሠረት ይፍቱ፣ **የማረጋጋጫ ኮዱን ዳግም መላክ አያስፈልግም** (በ 10 ደቂቃ ውስጥ አሁንም ይጸናል) |
| register 「邮箱验证码错误或已过期」 (የኢሜይል ማረጋጋጫ ኮድ ስህተት ወይም አልፏል) ያሳያል | ጊዜ ከማለፉ → ዳግም `send-code` |
| ከ `create-order` በኋላ ተጠቃሚው የክፍያ ገጹን ዘግቷል | በቀጥታ ዳግም `create-order` (አሮጌው ትዕዛዝ በ 2h በራስ ይዘጋል፤ የ PayPal PENDING ደንበኝነቶች በ 1h ያልፋሉ) |
| `create-order --provider paypal` 409 መለሰ | ያልተጠናቀቀ የ PayPal ደንበኝነት አለ፤ 1h ይጠብቁ እስኪያልቅ ድረስ፣ ወይም የአሮጌውን ፍቃድ በአሳሹ ያጠናቅቁ |
| `query` በተከታታይ pending / PENDING | ተጠቃሚው ሳይከፍል ይችላል፤ አንዴ ጠይቁት። በእውነት ከፈለክ በኋላ → በ payment-and-activation.md ያለውን የአፈታት ሠንጠረዥ ይከተሉ |
| ተጠቃሚው የመነሻ ማለግጠፊያ ጫኖ ወደ ደንበኝነት ገጽ ወረደ | ነጻ የሙከራ ወቅቱ አልቋል → ወደ የክፍያ ፍሰት ቀይር፦ `login-link --target pending` → የክፍያ ዘዴ ምረጥ → `create-order` |
| `refresh-login` 403 `pending_payment` | ነጻ የሙከራ ወቅቱ አልቋል እና ክፍያ አልደረሰም፤ ወደ ደረጃ 9 ተመለስ መጠየቅ ቀጥል፣ ወይም ተጠቃሚው ክፍያ ከፈጸመ አረጋግጥ |
| የሁኔታ ፋይል መጥፋት (በአጣቃቂ ሲሰረዝ / ማሽን ሲቀየር) | `whoami`/`refresh-login` መጠቀም አይቻልም፤ ተጠቃሚው አገናኝ 1ን የከፈተበት አሳሽ ውስጥ የደንበኝነት ገጹን በቀጥታ በማደስ ሁኔታውን እንዲያረጋግጥ ይንገሩት፣ ወይም ዳግም ይግባ (የዌብ ሁነታ) |

## የመመለሻ ሁነታ (ንጹህ መመሪያ)

ከሚከተሉት አንዱ ከተከሰተ ወዲያውኑ ወደ v1 ዓይነቱ ንጹህ መመሪያ ይመለሱ እና ስክሪፕቱን ማለቀቀት ያቁሙ፦

- Node ≥ 18 ከሌለ ወይም ስክሪፕቱ በተከታታይ ሁለት ጊዜ ተመሳሳይ ዓይነት ስህተት ካሳየ፤
- ተጠቃሚው በግልጽ «በዌብ ላይ ራሴ እሠራለሁ» ካለ፤
- የኩባንያ/የመሣሪያ ፖሊሲ ስክሪፕቱ አውታረ መረብ እንዳይጠቀም ከገደበ።

ከተመለስክ በኋላ፦ የምዝገባ ገጽ https://global.powpow.online/register ስጥ (በነጻ የሙከራ ወቅት የድር ምዝገባም አንደው ነው ወዲያውኑ የሚጠናቀቀው፤ ደንበኝነት ሲያስፈልግ የደንበኝነት ገጽም ስጥ https://global.powpow.online/subscription )፣ በ `registration-flow.md` ደንቦች መሠረት አብሮ ችግሩን ፈታ፣ ተመሳሳይ ጠባይ ጠብቅ፣ እና ሁሌም "ቀጣይ ደረጃ" ብሎክ ጨርስ።

