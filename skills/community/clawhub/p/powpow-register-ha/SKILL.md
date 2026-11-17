---
name: powpow-register
description: Yana taimaka wa mai amfani kammala rajistar PowPow (Bubble) da shiga da danna daya cikin hirar. Magidiman yana cika fom madadin mai amfani (har da dora hoton bayan gida) kuma yana aika da lambar tabbatar da imel; mai amfani kawai yana bayar da bayanan asali da kuma duban lambar tabbatar da sau daya — ba tare da ya bar tattaunawar ba. Yanar gizo a yanzu yana cikin lokacin gwaji kyauta: asusu da aka yi rajista zai iya amfani da dukkan fannoni nan take; biyan kudi na biya (Alipay/PayPal) karin mamba ne na zabi, wanda magidiman zai iya sarrafawa da kirkirar oda da bin diddigin kudin shiga in da akace. Yana kunna sa'oi da masu amfani na cewa "yi rajista a Bubble", "kirkiro asusu powpow", "yaya zan yi rajista a Bubble", "taimaka mini kirkirar asusu powpow", "sign up powpow"; kuma yana sarrafa matsalolin rajista (lambar tabbatar da bata zo, sunan mai amfani/imel an riga an rike) da matsalolin kunna (shiga yana cewa "ba a kunna asusu ba" / pending_payment, yaya zan biya/yi rajista, Bubble kyauta ne ko kudi). Yana bukatar Node ≥ 18; idan babu shi, ya koma da kansa zuwa yanayin jagorar tsantsa. Ba ya hada buga/kirkirar mutum na dijital (aikin powpow-simple ne), kuma ba ya hada habaka lamba.
version: 2.2.0
metadata:
  openclaw:
    emoji: "\U0001F4DD"
    homepage: https://global.powpow.online
---

# PowPow Register (mai taimakon rijistar kumfa)

Yana daukar sabon mai amfani daga "ban san menene Bubble ba" zuwa "na shiga da danna daya, a shirye don fara" — duka a cikin tattaunawar. Mai amfani yana barin tattaunawa sau daya kawai: **don duban lambar tabbatar da a akwatin sakonni**. Yanar gizo a yanzu yana cikin lokacin gwaji kyauta: bayan rajista, dukkan fannoni suna samuwa, babu bukatar biya; biyan kudi na biya karin mamba ne na zabi (magidiman yana bude karfat kudi kuma yana bin diddigin kudin shiga).

**Sigar 2.2.0** · 2026-10-18 (tun daga v2 wannan yanayin magidiman ne: kwangilar rubutu da cikakken jeri suna a `references/agent-flow.md`; ka'idodin fili, iyakar kima da warware matsala a `references/registration-flow.md`; hanyoyin biya a `references/payment-and-activation.md`; jerin hotunan samfur a `references/screenshots.md`. Tun daga v2.1.0 magidiman zai iya sarrafa rajistar PayPal, azaman zabi tare da Alipay. Tun daga v2.2.0 yanar gizo ya shiga lokacin gwaji kyauta: yi rajista kuma shiga da danna daya don fara amfani; biya ya zama kari na zabi — in mai amfani ya danna hanyar hadi kuma ya sauka a shafin biya, lokacin gwaji ya kare, bi bin jawardar biya daga mataki 7; jawardar tana daidaita kanta, babu bukatar canza rubutu)

## Yanayin aiki

- Babban script ɗin `scripts/powpow-register.mjs`: **ba shi da dogaro**, yana buƙatar **Node >= 18**. Kafin ka fara, ka gudanar da `node scripts/powpow-register.mjs status` sau ɗaya domin tabbatar da yanayin yana aiki.
- Duk buƙatun script ɗin suna tafiya ga adireshin hukuma `https://global.powpow.online` kawai.
- **Babu Node / kuskuren rubutu**: koma da kanka zuwa yanayin jagorar tsantsa — ba mai amfani shafin rajista https://global.powpow.online/register kuma ka bi shi bisa ka'idodin `references/registration-flow.md` (a lokacin gwaji kyauta, rajistar yanar gizo ita ce nan take). Kada ka ci gaba da dukan rubutu.
- Bayan tattaunawa ta katse kuma ana dawowa: da farko `status` ka duba an kai mataki guda, sannan ka ci gaba.

## Trigger Conditions

- Aniyar rijista: 'rijista kumfa', 'yi min rijistar asusun powpow', 'yadda ake rijistar kumfa', 'sign up powpow'
- Rijista ta makaure: 'ba a karɓar lambar tabbatarwa', 'an ce sunan mai amfani ya riga ya wanzu', 'kalmar sirri koyaushe ba ta dace ba'
- Matsalolin bayan rajista: "shiga yana cewa ba a kunna asusu ba", "403 pending_payment", "yaya zan biya/yi rajista a Bubble", "Bubble kyauta ne ko kudi"

**Ba ya kunna**: wallafa sako/ƙirƙirar mutum na dijital (→ powpow-simple); haɓakar code na Web (duba skill ɗin haɓaka). Idan mai amfani yana son rijista kuma wallafa sako: ka fara kammala skill ɗin nan, bayan kunna ka mika wa powpow-simple.

## Taƙaitaccen tsari

| Mataki | Agent yana yi nini | Mai amfani yana yi nini |
|---|---|---|
| 1 Gabatarwar samfur | Bayyana + aika hoto | Duba |
| 2 Tabbatar da bayanai | Ka ba da shawarar sunan mai amfani/laƙabi, kalmar sirri zaɓi ɗaya, ka tambayi imel | Tabbatar, bayar |
| 3 Aika lambar tabbatarwa | `send-code` | —— |
| 4 Karɓar lambar tabbatarwa | —— | Ka je imel ka duba lambar lambobi 6, ka dawo ka tura mana |
| 5 Ƙaddamar da rijista | `register` (tare da ɗora avatar kai tsaye), kuskure ana kula da su ta kai | —— |
| 6 Shiga da danna daya | `login-link(home)` kai tsaye zuwa shafin gida; in ya sauka a shafin biya, je zuwa mataki 7 | Danna hanyar hadi kuma fara amfani |
| 7 Karin rajista (na zabi) | Kawai in mai amfani ya so mamba / lokacin kyauta ya kare: cikakken jawardar biya a sarrafa | Zabi hanya, biya |
| 8 Rufe aiki | `cleanup` + ba da takaddun + jagorar gwaji + ba da shawarar plugin | Ka fara wasa |

## Mataki na 1: Gabatarwar samfur + hotuna (ba za a iya tsallakewa ba)

Yawancin masu amfani ba su taɓa ganin kumfa ba. Abin da za a fara da shi ba bayanin tsari bane, amma a sa shi ya **gani** samfurin:

1. Ka gabatar da kumfa da kalmomi kusan 120: hotunan da mai amfani ya ɗauka bisa son zuciya suna zama rubutun tafiya, ana dasa su a kan taswirar jama'a su zama 'kumfa' guda; kumfa na ƙare rai tare da lokaci, idan wasu suka yaba (like) zai iya komawa rai; a kan taswira akwai 'mutane na dijital' da za a iya magana da su. Adireshin dandali https://global.powpow.online , idan yana son duba bidiyo da farko: https://www.bilibili.com/video/BV1Wu826UEVz/
2. **Aika hotuna**. Hotunan an haɗe su tare da skill a cikin `assets/screenshots/powpow-0N.jpg` — ka aika da su kai tsaye a matsayin fayilolin hoto na gida, ba tare da intanet ba. Jerin, abin da kowane hoto ke ƙunsa da lokacin amfani da shi duba `references/screenshots.md`. Haɗin da ake amfani da shi fiye da kowa a farko: shafin taswira (powpow-03) + shafin cikakken bayanin sako (powpow-06).

Dokokin hoto (ka'idoji masu ƙarfi):

- Hotunan **an haɗe su tare da skill** a cikin `assets/screenshots/` (`powpow-0N.jpg`) — ka aika da fayilolin hoto na gida kai tsaye; suna aiki a kowane yanayi, har ma da yanayin da GitHub ba za a iya buɗewa ba.
- A lokaci guda ka aika hotuna 1–3 kawai waɗanda suka shafi batun na yanzu, kada ka ɗora duka gaba ɗaya.
- Idan fayilolin cikin kunshin sun ɓace ba zato ba tsammani, ka koma ga mahadi da aka jera a cikin `references/screenshots.md` (a lura: a China mai yiwuwa ba za a iya buɗe su ba).

Bayan gabatarwa, ka ba mai amfani zaɓi: **'Idan kana son yin rijista, za mu gina asusun a cikin tattaunawa a cikin minti uku, kana buƙatar duba lambar tabbatarwa ta imel sau ɗaya kawai.'**

## Mataki na 2: Tabbatar da bayanin rijista (tambaya ɗaya a kowane zagaye, kada ka tambaya duka gaba ɗaya)

- **Sunan mai amfani** (wajibi): daga mahallin tattaunawa/sunan mai amfani na tsarin **ka ba da shawarar ɗaya** (haruffa 2~50, ba tare da la'akari da girma-kanana ba), idan mai amfani ya amince a yi amfani da shi, idan yana son canzawa a canza.
- **Kalmar sirri** (wajibi, ka fara tambayi mai amfani ya zaɓi ɗaya):
  - Mai amfani ya kawo nasa → daga baya a wuce ta ta canjin muhalli ga script ɗin, **kada ka taɓa rubuta ta a cikin mahawarin umarni**;
  - Agent ta ƙirƙira → ka gudanar da `node scripts/powpow-register.mjs gen-password`, ka aika da kalmar sirrin da aka ƙirƙira **da farko ga mai amfani domin ya adana** (ana nuna ta sau ɗaya kawai, daga baya ba za ta bayyana ba).
- **Imel** (wajibi): dole ne mai amfani ya kawo — wannan ita ce tushen asalin asusun, **kada ka tsinkaya wa mai amfani**.
- **Laƙabi** (na zaɓi): ka ba da shawarar ta zama daidai da sunan mai amfani da tsoho.
- **Avatar** (na zaɓi): idan mai amfani ya ba da hanyar fayil ɗin hoto na gida (≤5MB, ba SVG ba) script ɗin zai ɗora ta kai tsaye; idan ba ya kawo a tsallake ta (dandalin zai yi amfani da tambarin tsoho); idan kana da ƙarfin ƙirƙirar hoto, za ka iya ba da shawarar taimaka wa mai amfani ya ƙirƙiri ɗaya.
- **Lambar waya** (na zaɓi, lambar babban yankin China): tsoho ita ce tsallakewa; idan mai amfani da kansa yana son ɗaure, to a nemi.

Bayan an tabbatar za ka iya gudanar da `prepare-suggest --username U --nickname N --email E` domin a rubuta su a cikin fayil ɗin hali (daga baya register ba buƙatar maimaita wucewa).

## Mataki na 3–4: Lambar tabbatarwa ta imel (kadai matakin da dole ne a bar tattaunawa)

```
node scripts/powpow-register.mjs send-code --email <imel>
```

Sannan ka faɗi wa mai amfani a bayyane: **ka je imel ka nemo lambar lambobi 6, mai inganci a cikin minti 10, ka tuna ka duba babban fayil ɗin spam/junk**, idan ya samu ya dawo ya tura mana lambar. Aikawa na da lokacin jira na daƙiƙa 60, kada ka yi ta danna.

## Mataki na 5: Ƙaddamar da rijista (agent yana taimakawa)

```
POWPOW_REGISTER_PASSWORD=<kalmar sirri> node scripts/powpow-register.mjs register --code <lambar tabbatarwa> [--username U] [--nickname N] [--avatar <hanyar fayil ɗin hoto na gida>] [--phone P]
```

Nasarara tana ƙirƙirar asusu (hali pending, tare da badge 3 na farko). Kuskuren da aka saba ana kula da su ta kai, ba tare da katsewa ga mai amfani ba:

| Kuskure | Yadda ake kula |
|---|---|
| 用户名已存在 (sunan mai amfani ya riga ya wanzu) | Ka ba da shawarar saiti (sunan mai amfani + lamba) ta kai, mai amfani ya tabbatar sannan a sake gwadawa kai tsaye (lambar tabbatarwa tana da inganci har yanzu, ba buƙatar sake aikawa) |
| 邮箱已被使用 (an riga an yi amfani da imel) | Ka tambayi mai amfani: ya canza wata imel, ko kuma hakika yana da asusu a riga (a canza zuwa shiga/sake saita kalmar sirri) |
| 邮箱验证码错误或已过期 (lambar tabbatarwa ta imel ba ta daidai ko ta ƙare) | Idan ya wuce minti 10 → a sake `send-code` |
| 发送/注册过于频繁（429） (aikawa/rijista sau da yawa (429)) | Ka jira minti 1 sannan a sake gwadawa, ka faɗi wa mai amfani kawai |

## Mataki 6: Shiga da danna daya (bayan rajista kai tsaye zuwa shafin gida)

1. Nan take bayan rajista ta samu nasara:
   ```
   node scripts/powpow-register.mjs login-link --target home
   ```
2. Aika hanyar hadi zuwa ga mai amfani: **danna shi kuma ka sauka kai tsaye a shafin gida, tare da shiga**. Yanar gizo a yanzu yana cikin lokacin gwaji kyauta — bayan rajista dukkan fannoni suna amfani (beam, taswira, mutum na dijital, shaidar ziyara da sauransu), **babu bukatar biya**.
3. Tambayi mai amfani ya tabbatar da shigarsa; akwai halaye biyu:
   - **Ya sauka a shafin gida** → je kai tsaye zuwa mataki 8 don kammala; rajista ta kammala;
   - **Ya sauka a shafin biya** → lokacin gwaji kyauta na yanar gizo ya kare; faɗa wa mai amfani "lokacin gwaji kyauta ya kare, yanzu ana bukatar rajistar mamba", sannan bi mataki 7 don kammala rajista, kuma bayan rajista koma zuwa mataki 8.
4. In mai amfani da kansa ya so kari ko tallafa yanar gizo → je zuwa mataki 7 (rajista son zuciya ne; kada ka tilasta).
## Mataki 7: Karin rajista (na zabi — kawai sa'adda mataki 6 ya nuna)

1. Da fari aika hanyar shiga ta rabi don shafin dawowa bayan biya ya iya nuna "Biya ta samu nasara" daidai:
   ```
   node scripts/powpow-register.mjs login-link --target pending
   ```
   Aika hanyar hadi zuwa ga mai amfani: danna shi kuma burauza ya sauka kai tsaye a shafin biya, tare da shiga.
2. **Tambayi mai amfani ya zabi hanyar biya** — nuna dukkan hanyoyin biyu:
   - **Alipay (ƙasar Sin / masu amfani da Alipay)**: siyan daya ta wani lokaci, **ba ta sake kanta ba**
     - Na wata **¥6.99** (an shawarata don gwaji) / Na watanni uku **¥19.99** / Na shekara **¥69.99**
   - **PayPal (ketare / marasa Alipay)**: sake kanta kowane wata, soke a kowane lokaci
     - Premium Monthly, kusan **$1/wata** (kamar yadda aka nuna a shafin biya; tare da sake kanta)
3. Da zarar mai amfani ya zabi daya:
   - **Alipay**:
     ```
     node scripts/powpow-register.mjs create-order --package monthly
     ```
   - **PayPal**:
     ```
     node scripts/powpow-register.mjs create-order --provider paypal
     ```
   Rubutun zai dawo da hanyar fayil din shafin biya; **buɗe shi kai tsaye da umarnin tsarin** (Windows: `start <fayil>`; macOS: `open <fayil>`; Linux: `xdg-open <fayil>`). Burauza zai sake kansa zuwa karfat kudin Alipay/PayPal na hukuma, inda mai amfani zai kammala biya ko izinin cajin kudi.
4. Gudanar da `query` kowane 10–15 dakika har ya dawo da `paid` ko `ACTIVE` (biya/izini yana sauka a cikin yan dakika zuwa minti daya). In mai amfani ya rufe shafin biya a tsakiya → kawai `create-order` sake (tsofaffin oda / rajistar da ta tsaya suna rufe ko karewa bayan awa 2; kauce musu).
5. Hanyar kodin QR ta WeChat ana tabbatar da ita da hannu kuma kudi na iya jinkirta; Huawei IAP yana samuwa kawai a cikin manhajar HarmonyOS. Fasahar ba ta sarrafa waɗannan biyu — bayan biya, mai amfani yana komawa kuma ya faɗa wa magidiman, wanda ya fara gudanar da `whoami` don tabbatar da saukar kudi, sannan ya aika hanyar shafin gida bisa ka'ida 6 a kasa.
6. Bayan tabbatar da saukar kudi, musanya yanayin shiga da kimar rajista ta yanzu, sannan aika hanyar hadi kai tsaye zuwa shafin gida:
   ```
   POWPOW_REGISTER_PASSWORD=<kalmar sirri> node scripts/powpow-register.mjs refresh-login
   node scripts/powpow-register.mjs login-link --target home
   ```
   Aika hanyar hadi zuwa ga mai amfani: **danna shi kuma ka sauka kai tsaye a shafin gida tare da cikakken matsayin mamba**.
## Mataki 8: Kammalawa

1. `node scripts/powpow-register.mjs cleanup` don share fayilolin yanayin na wancan lokaci (takaddun zama).
2. Ba mai amfani "katin asusu": sunan mai amfani, imel (ba a sake nuna kalmar sirri — a yanayin kirkira an ce wa mai amfani ya ajiye ta sa'adda aka kirkira; in mai amfani ya saita ta da kansa, ya santa).
3. Tunatarwar mamba (faɗa sau daya, kada ka tilasta): a yanzu lokacin gwaji kyauta ne kuma asusu yana amfani nan take; sa'adda lokacin gwaji ya kare, asusun da ba su yi rajista ba za a mayar da su zuwa shafin biya sa'adda suka shiga shafukan abun ciki — don amfani na dogon lokaci, koyo kuma yi rajista a kowane lokaci.
4. Nuna matakan farko: duba taswira, buga rubutun tafiya na farko (→ mika zuwa powpow-simple).
5. Shawarar fadada: fasahar `@durenzidu/powpow-integration` da plugin din `@durenzidu/openclaw-channel-powpow` — hada Bubble zuwa magidiman mai amfani da kansa; ba da umarnin shigar da in ya so.
6. Kammala da sashin "mataki na gaba".
## Conversation UX

Ka ci gaba da salo mai taimako na PowPow:

- **Mai amfani shine jumla ta magana**: 'kana iya...' ya fi 'ina buƙatar ka...'; kada ka yi wa kai girma, kada ka koyar da shi.
- **A kowane zagaye ka ci gaba da yanke shawara ɗaya kawai**; kafin neman bayani, ka fara ba da dalili.
- **Ƙarshen kowane amsa** sashe ne na dindindin na 'mataki na gaba' (layin raba + 👉 + aiki ɗaya + jimla ɗaya 'da zarar na yi...'), misali:
  ```
  ────────────────────
  👉 Abin da ake buƙata daga kai yanzu: ka je imel ka nemo lambar lambobi 6, ka tura mana kai tsaye
     (da zarar na karɓa, nan da nan zan gina asusun)
  ```
- **Kada ka yi wa kalmar sirri lacca kan tsaro da kanka**; kada ka bayyana tsarin ciki, iyakancewa ko zanen tsaro, sai dai idan mai amfani ya tambaya.
- Lokacin agent tana taimakawa fiye da haka dole ne a ba da rahoton ci gaba: bayan kowane matakin script ɗin ka faɗi wa mai amfani da jimla ɗaya abin da ya faru ('asusun an gina shi', 'shafin biya na taimaka maka an buɗe shi').

## Ka'idojin ƙarfi

- **Tsaron takaddun shaida**: kalmar sirri tana wucewa ga script ɗin ta hanyar canjin muhalli `POWPOW_REGISTER_PASSWORD` kawai, **kada taɓa** rubuta ta a cikin mahawarin umarni (jerin aiwatarwa na iya ganonta), kada ka rubuta ta a cikin wani fayil (yanayin ƙirƙira yana nunta sau ɗaya domin mai amfani ya adana, daga baya ba a sake maimaita ta). Lambar tabbatarwa ana amfani da ita da tashar hukuma ta rijista kawai, bayan amfani a jefar da ita.
- **Iyakar hukuma**: duk buƙatun suna tafiya ga `https://global.powpow.online` kawai (script ɗin ya riga ya saka shi), kada ka taɓa aika bayanan mai amfani ga wata adireshin ɓangare na uku.
- **Iyakar biya**: agent ɗin ƙirƙirar oda kawai take yi, buɗe cashier, duba shigar kuɗi; **kada ta taba** asusun Alipay/PayPal na mai amfani/takaddun biya, kuma kada ta taɓa alƙawari 'biya a madadinsa'.
- **Katanga ba laifi ba ne**: a cikin lokacin gwaji kyauta na yanzu dukkan shafukan abun ciki suna buɗe; in mai amfani ya danna hanyar shafin gida amma ya sauka a shafin biya — lokacin gwaji ya kare, bishe shi ya yi rajista ta mataki 7. Kada ka kokari wuce katanga, kuma kada ka bayar da ginshikan cikin gida ga mai amfani.
- **'Yancin dawowa**: a kowane mataki mai amfani yana son yin shi da kansa, ko yanayin ba ta goyi bayan script ɗin ba, a koma ta kai ga yanayin jagora kawai — ka ba mahadi, ka bayyana dokoki, ka taimaka gyara kuskure.
- Kada ka ƙirƙiri dokokin dandalin: dokokin filaye, rubutun kuskure, ma'aunin iyakancewa duka sun fito daga code ɗin dandalin (`references/registration-flow.md` tana da inda aka samo su), lokacin da dandalin ya sabunta a bi halin da gaske na kan layi.
- Hotunan da ake nunawa ka yi amfani da waɗanda ke cikin kunshin `assets/screenshots/` kawai (amfanin kowane hoto duba `references/screenshots.md`).
- A ƙarshen kowane zagaye ka rufe da sashin 'mataki na gaba', domin mai amfani ya san koyaushe abin da ya kamata ya yi.
