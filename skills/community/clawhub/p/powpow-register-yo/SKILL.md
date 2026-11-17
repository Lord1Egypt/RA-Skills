---
name: powpow-register
description: Firanran awọn olumulo lati pari iforukọsilẹ PowPop (Bubble) ati iwọle ẹyọkan ni abala iwiregba gbogbo rẹ. Ajanṣan kun fọọmu fun wọn (pẹlu gbigbe aworan) o si fi koodu ifẹsẹmulẹ imeeli ranṣẹ; olumulo kan n pese alaye ipilẹ ati wo koodu ifẹsẹmulẹ lẹẹkan — ko jade kuro ninu iwiregba. Ni akoko idanwo ọfẹ lọwọlọwọ, akanti ti o forukọsilẹ le lo gbogbo ẹya lẹsẹkẹsẹ; owo sập (Alipay/PayPal) jẹ ilọsi ọmọ-ẹyọn aṣayan, ti ajanṣan le tọju pẹlu pipin iwe ati ibẹwo ọwọn pẹlu. O ṣiṣẹ nigbati olumulo ba sọ "forukọsilẹ fun Bubble", "ṣẹda akanti powpow", "bawo ni mo ṣe le forukọsilẹ fun Bubble", "ran mi lọwọ lati ṣẹda akanti powpow", "forukọsilẹ powpow"; o tun ṣe iṣẹ pẹlu awọn iṣoro iforukọsilẹ (koodu ifẹsẹmulẹ ko gba, orukọ/imeeli ti gba) ati awọn iṣoro imuṣiṣẹ (iwọle sọ "akanti ko ṣiṣẹ" / pending_payment, bawo ni o ṣe le sanwọ/sập, Bubble jẹ ọfẹ tabi owo). O nilo Node ≥ 18; pada si ipo itọsọna pipẹ laifọwọyi nigbati ko ba si. Ko ṣe iṣẹ pẹlu ifiweranṣẹ/ṣẹda ẹda oni-nọmba (iṣẹ powpow-simple ni iyẹn), tabi idagbasoke koodu.
version: 2.2.0
metadata:
  openclaw:
    emoji: "\U0001F4DD"
    homepage: https://global.powpow.online
---

# PowPow Register (oluranlọwọ iforukosile Bubble)

O gbe olumulo tuntun lati "emi ko mọ kini Bubble jẹ" si "ti wọle pẹlu ẹyọkan, ṣetan lati ṣere" — gbogbo rẹ ni abala iwiregba. Olumulo jade kuro ninu iwiregba lẹẹkan kan: **lati wo koodu ifẹsẹmulẹ ninu apoti-ìwé rẹ**. Sajoo ni akoko idanwo ọfẹ: nigbati o forukọsilẹ, gbogbo ẹya wa, ko nilo owo; owo sập jẹ ilọsi ọmọ-ẹyọn aṣayan (ajanṣan tun ṣiṣi ati tọju ọwọn pẹlu).

**Ẹya 2.2.0** · 2026-10-18 (lati v2 eyi jẹ ipo iranlọwọ-ajanṣan: adehun iwe ati gbogbo ilana ni `references/agent-flow.md`; awọn ofin aaye, idinwo iṣẹ ati itọju aṣiṣe ni `references/registration-flow.md`; awọn ọna owo ni `references/payment-and-activation.md`; atokọ aworan ọja ni `references/screenshots.md`. Lati v2.1.0 ajanṣan le tọju sập PayPal pẹlu, gẹgẹbi aṣayan lẹgbẹẹ Alipay. Lati v2.2.0 sajoo wà ninu akoko idanwo ọfẹ: forukọsilẹ ki o wọle pẹlu ẹyọkan lati bẹrẹ lilo; owo di ilọsi aṣayan — ti olumulo ba tẹ ọna asopọ ki o si gbalẹ lori ojú-iwe sập, akoko idanwo ti pari, tẹle ilana owo igba 7; ilana ṣe atunṣa funrarẹ, ko nilo iyipada iwe)

## Agbegbe ṣiṣe

- Iwe pataki `scripts/powpow-register.mjs`: **laisi awọn igbẹkẹle**, o nilo **Node >= 18**. Ṣaaju ki o to bẹrẹ, ṣiṣẹ lẹẹkan `node scripts/powpow-register.mjs status` lati ni idaniloju agbegbe ṣiṣe.
- Gbogbo awọn ibeere iwe n lọ si ibugbe osise nikan `https://global.powpow.online`.
- **Ko si Node / aṣiṣe iwe**: pada si ipo itọsọna pipẹ laifọwọyi — fun olumulo ni ojú-iwe iforukọsilẹ https://global.powpow.online/register ki o si ṣe itọsọna pẹlu gẹgẹbi `references/registration-flow.md` (ni akoko idanwo ọfẹ, iforukọsilẹ wẹẹbu jẹ iyara kan). Maṣe tubọ lu iwe.
- Ipadabọ lẹhin ti ibaraẹnisọrọ naa ti ge: kọkọ `status` lati wo iru ipe ti ilana naa ti de, lẹhinna tẹsiwaju.

## Trigger Conditions

- Ète iforukosile: "foruko Bubble", "foruko akọọlẹ powpow kan", "bawo ni a ṣe foruko powpow", "sign up powpow"
- Iforukosile ti di duro: "gbigba nọmba ijẹrisi imeeli", "oruko olumulo ni a sọ pe o ti wa tẹlẹ", "ọrọ igbaniwọle ko dara nigbagbogbo"
- Awọn iṣoro lẹhin iforukọsilẹ: "iwọle sọ akanti ko ṣiṣẹ", "403 pending_payment", "bawo ni mo ṣe sanwọ/sập fun Bubble", "Bubble jẹ ọfẹ tabi owo"

**Ko ṣe nkan**: gbigbe ifiweranṣẹ/ẹda eniyan oni-nọmba (→ powpow-simple); idagbasoke koodu oju opo wẹẹbu (wo skill idagbasoke). Nigbati olumulo ba fẹ iforukosile ati tun fẹ gbe ifiweranṣẹ: kọkọ pari skill yii, lẹhin imuyipada fi si ọwọ powpow-simple.

## Akopọ ṣiṣan

| Ipe | Ohun ti agent ṣe | Ohun ti olumulo ṣe |
|---|---|---|
| 1 Ifihan ọja | Ṣalaye + firanṣẹ aworan | Wo |
| 2 Imudaniloju alaye | Dabanọ oruko olumulo/oruko ọrẹ, yan ọrọ igbaniwọle, beere imeeli | Imudaniloju, pese |
| 3 Firanṣẹ koodu ijẹrisi | `send-code` | —— |
| 4 Ka nọmba ijẹrisi | —— | Lọ si imeeli wo nọmba oni-nọmba 6, pada fi ranṣẹ |
| 5 Fi iforukosile silẹ | `register` (pẹlu ikojade aworan profaili taara), ṣetọju aṣiṣe laifọwọyi | —— |
| 6 Iwọle ẹyọkan | `login-link(home)` taara si ojú-iwe ile; ti o ba gbalẹ lori ojú-iwe sập, lọ si Igba 7 | Tẹ ọna ki o bẹrẹ ṣere |
| 7 Ilọsi ọmọ-ẹyọn (aṣayan) | Nigbati olumulo fẹ ọmọ-ẹyọn / akoko ọfẹ ti pari: gbogbo ilana owo ni a tọju | Yan ọna, san owo |
| 8 Ipari | `cleanup` + fi iwe-ẹri fun + ṣe itọsọna iriri + daba afikun | Bẹrẹ ere |

## Ipe 1: Ifihan ọja + aworan (maṣe fo)

Ọpọlọpọ awọn olumulo ko tii ri Bubble rara. Ohun akọkọ kii ṣe alaye ilana, ṣugbọn jẹ ki wọn **ri** ọja naa:

1. Lo ọrọ bii 120 lati ṣalaye Bubble: awọn aworan ti o ya ni irọrun yipada si irin-ajo irin-ajo, wọn fi si maapu gbangba bi "bebula" kan; bebula naa n rẹwẹsi pẹlu akoko, awọn miiran ti o ba fẹran a o sọji; lori maapu tun wa awọn "eniyan oni-nọmba" ti o le ba sọrọ. Adirẹsi pẹpẹ https://global.powpow.online, ti o ba fẹ wo fidio kọkọ: https://www.bilibili.com/video/BV1Wu826UEVz/
2. **Firanṣẹ aworan**. Awọn aworan ti dahun pọ pẹlu skill ninu `assets/screenshots/powpow-0N.jpg` — fi ranṣẹ taara bi faili aworan agbegbe, ko nilo nẹtiwọọki. Atokọ, ohun ti o wa ninu aworan kọọkan ati igba lati lo wọn wo `references/screenshots.md`. Apapọ ti a lo julọ ni ibẹrẹ: oju-iwe maapu (powpow-03) + oju-iwe alaye ifiweranṣẹ (powpow-06).

Awọn ofin aworan (ofin lile):

- Aworan **ti dahun pọ pẹlu skill** ninu `assets/screenshots/` (`powpow-0N.jpg`) — fi ranṣẹ faili aworan agbegbe nikan; o ṣiṣẹ ni gbogbo agbegbe, pẹlu awọn agbegbe nibiti GitHub ko ṣii.
- Firanṣẹ awọn aworan 1–3 ti o jọmọ koko-ọrọ lọwọlọwọ nikan ni igba kan, maṣe fi gbogbo wọn ranṣẹ ni ẹẹkan.
- Ti awọn faili inu ba padanu lairotẹlẹ, pada si awọn ọna asopọ ibi ipamọ ti a ṣe akojọ ninu `references/screenshots.md` (akiyesi: o le ma ṣii ni Ilu China).

Lẹhin alaye, fi yiyan fun olumulo: **"Ti o ba fẹ foruko, a o kọ akọọlẹ sinu ibaraẹnisọrọ ni iṣẹju mẹta, o nilo nikan lati wo nọmba ijẹrisi imeeli lẹẹkan."**

## Ipe 2: Imudaniloju alaye iforukosile (beere ibeere kan fun ipe kan, maṣe beere gbogbo wọn ni ẹẹkan)

- **Oruko olumulo** (dandan): lati agbegbe ibaraẹnisọrọ/oruko olumulo eto **daba ọkan** (awọn ohun kikọ 2~50, laibikita nla-kekere), ti olumulo ba fọwọsi lo, ti o ba fẹ yi padà yipada.
- **Ọrọ igbaniwọle** (dandan, kọkọ beere olumulo yan ọkan):
  - Olumulo funra rẹ pese → lẹhinna fi via oniyipada ayika si iwe, **maṣe kọ sinu awọn ariyanjiyan aṣẹ rara**;
  - agent ṣe ipilẹṣẹ → ṣiṣẹ `node scripts/powpow-register.mjs gen-password`, fi ọrọ igbaniwọle ti a ṣipilẹṣẹ **ranṣẹ si olumulo lẹẹkan ki o tọju** (a fi han lẹẹkan nikan, ko tun farahan lẹhinna).
- **Imeeli** (dandan): olumulo gbọdọ pese — eyi ni oran idanimọ ti akọọlẹ, **maṣe gboju boya fun olumulo**.
- **Oruko ọrẹ** (iyanjiyan): daba aiyipada kanna bi oruko olumulo.
- **Aworan profaili** (iyanjiyan): olumulo fun ọna faili aworan agbegbe kan (<=5MB, kii ṣe SVG) jẹ ki iwe gbe taara; ti ko ba si fo (pẹpẹ lo aami aiyipada); ti o ba ni agbara ṣiṣẹda aworan, o le daba lati ran olumulo lọwọ ṣe ọkan.
- **Nọmba foonu** (iyanjiyan, nọmba oluile): aiyipada fo, ti olumulo ba fẹ dipọ beere.

Lẹhin imudaniloju o le ṣiṣẹ `prepare-suggest --username U --nickname N --email E` lati kọ si faili ipo (lẹhinna register ko nilo tun ranṣẹ).

## Ipe 3–4: Nọmba ijẹrisi imeeli (ipin kan ṣoṣo ti o nilo jade kuro ninu ibaraẹnisọrọ)

```
node scripts/powpow-register.mjs send-code --email <imeeli>
```

Lẹhinna sọ fun olumulo ni gbangba: **lọ si imeeli wa nọmba oni-nọmba 6, wulo fun iṣẹju 10, ranti wo folda idọti/ifilọle**, ti o ba ri pada fi ranṣẹ. Firanṣẹ ni ihamọ iṣẹju 60, maṣe tẹ leralera.

## Ipe 5: Fi iforukosile silẹ (agent n ṣe iranlọwọ)

```
POWPOW_REGISTER_PASSWORD=<ọrọigbaniwọle> node scripts/powpow-register.mjs register --code <nọmba ijẹrisi> [--username U] [--nickname N] [--avatar <ọna faili aworan agbegbe>] [--phone P]
```

Aṣeyọri ṣẹda akọọlẹ (ipo pending, pẹlu baaji 3 ibẹrẹ). Awọn aṣiṣe ti o wọpọ ni a ṣetọju laifọwọyi, laisi idilọwọ olumulo:

| Aṣiṣe | Ṣetọju |
|---|---|
| 用户名已存在 (oruko olumulo ti wa tẹlẹ) | Daba iyatọ laifọwọyi (oruko olumulo + nọmba), olumulo fọwọsi lẹhinna tun gbiyanju taara (koodu ijẹrisi tun wulo, ko nilo atunfiranṣẹ) |
| 邮箱已被使用 (imeeli ti a ti lo) | Beere olumulo: paṣẹ imeeli miiran, tabi boya o ti ni akọọlẹ (yi lọ si wiwọle/iranti ọrọ igbaniwọle) |
| 邮箱验证码错误或已过期 (koodu ijẹrisi imeeli jẹ aṣiṣe tabi ti di ofo) | Ti o ba kọja iṣẹju 10 → tun `send-code` |
| 发送/注册过于频繁（429） (firanṣẹ/iforukosile pupọ ju (429)) | Duro iṣẹju 1 lẹhinna tun gbiyanju, sọ fun olumulo nikan |

## Igba 6: Iwọle Ẹyọkan (taara si ojú-iwe ile lẹhin iforukọsilẹ)

1. Lẹyin iforukọsilẹ to ṣaṣeyọri:
   ```
   node scripts/powpow-register.mjs login-link --target home
   ```
2. Fi ọna ranṣẹ si olumulo: **tẹ e ki o si gbalẹ taara lori ojú-iwe ile, ti wọle tẹlẹ**. Sajoo wà ninu akoko idanwo ọfẹ — lẹhin iforukọsilẹ, gbogbo ẹya wa (ifeede, maapu, ẹda oni-nọmba, awọn abẹwo, ati bẹbẹ), **ko nilo owo**.
3. Beere olumulo lati jẹrisi pe o wọle; ipo meji wa:
   - **Gbalẹ lori ojú-iwe ile** → fo taara si Igba 8 lati pari; iforukọsilẹ ti pari;
   - **Gbalẹ lori ojú-iwe sập** → akoko idanwo ọfẹ sajoo ti pari; sọ fun olumulo "akoko idanwo ọfẹ ti pari, sập ọmọ-ẹyọn nilo bayi", lẹhinna tẹle Igba 7 lati pari sập, ki o si pada si Igba 8 lẹhin sập.
4. Ti olumulo ba fẹ ilọsi tabi ṣe atilẹyin sajoo → lọ si Igba 8 pẹlu (sập jẹ ifẹ; maṣe fi ipá).
## Igba 7: Ilọsi Ọmọ-ẹyọn (aṣayan — nigbati Igba 6 n beere)

1. Kọọkan fi ọna idaji-iwọle ranṣẹ ki oju-iwe ipadabọ owo le ṣafihan "Owo ṣaṣeyọri" daradara:
   ```
   node scripts/powpow-register.mjs login-link --target pending
   ```
   Fi ọna ranṣẹ si olumulo: titẹ e jẹ ki aṣawakiri gbalẹ taara lori ojú-iwe sập, ti wọle tẹlẹ.
2. **Jẹ ki olumulo yan ọna owo** — ṣafihan mejeeji:
   - **Alipay (ilẹ China / awọn olumulo pẹlu Alipay)**: rira ẹyọkan ti akoko to baamu, **ko si imudasilẹ adaṣe**
     - Oṣù **¥6.99** (gba niyanju lati danwo) / Kọọkan **¥19.99** / Ọdún **¥69.99**
   - **PayPal (ode ọdún / awọn olumulo laisi Alipay)**: ṣe imudasilẹ adaṣe oṣù kọọkan, le fagilé nigbakigba
     - Alabọde Oṣù, nla **$1/oṣù** (gẹgẹbi a ṣe ṣafihan lori ojú-iwe sập; ṣe imudasilẹ adaṣe)
3. Nigbati olumulo ba yan ọkan:
   - **Alipay**:
     ```
     node scripts/powpow-register.mjs create-order --package monthly
     ```
   - **PayPal**:
     ```
     node scripts/powpow-register.mjs create-order --provider paypal
     ```
   Iwe na da ọna faili ojú-iwe owo pada; **ṹ ṣíi taara pẹlu aṣẹ eto** (Windows: `start <file>`; macOS: `open <file>`; Linux: `xdg-open <file>`). Aṣawakiri fo laifọwọyi si ile-owo Alipay/PayPal ofeefee, nibiti olumulo pari owo tabi aṣẹ ìdíyelé.
4. Ṣiṣe `query` gbogbo iṣẹju 10–15 titi o padà `paid` tabi `ACTIVE` (owo/aṣẹ ni gbogbọn de laarin iṣẹju diẹ si iṣẹju kan). Ti olumulo ba ti ojú-iwe owo ni aarin → ṣẹda `create-order` lẹẹkansi (iwe atijọ / sập n reti ti ipade tabi pari laifọwọyi lẹhin wakati 2; foju wọn).
5. Ọna koodu WeChat QR jẹrisi ni ọwọ ati owo le de pẹlu; Huawei IAP wa ni inu App HarmonyOS nikan. Ìmọ-jáẹẹ yi ko tọju mejeji — lẹhin sanwo, olumulo pada sọ fun ajanṣan, ti n ṣiṣẹ `whoami` kọ lati jẹrisi ọwọn, lẹhinna fi ọna ojú-iwe ile ranṣẹ gẹgẹbi aami 6 ni isalẹ.
6. Lẹhin jẹrisi ọwọn, paṣiparọ fun ipo iwọle pẹlu asẹ sập tuntun, lẹhinna fi ọna ranṣẹ taara si ojú-iwe ile:
   ```
   POWPOW_REGISTER_PASSWORD=<password> node scripts/powpow-register.mjs refresh-login
   node scripts/powpow-register.mjs login-link --target home
   ```
   Fi ọna ranṣẹ si olumulo: **tẹ e ki o si gbalẹ taara lori ojú-iwe ile pẹlu ipo ọmọ-ẹyọn kikun**.
## Igba 8: Ipari

1. `node scripts/powpow-register.mjs cleanup` lati nu awọn faili ipo akoko agbegbe (ẹri ajọ).
2. Fun olumulo ni "kaadi akanti": orukọ, imeeli (ọrọ igbaniwọle ko han mọ — ni ipo ipilẹṣẹ a beere olumulo lati fipamọ nigbati a ṣe; ti olumulo ba fi silẹ funrarẹ, wọn mọ ọ).
3. Iranti ọmọ-ẹyọn (sọ lẹẹkan, maṣe fi ipá): eleyi jẹ akoko idanwo ọfẹ ati akanti wa lẹsẹkẹsẹ; nigbati akoko idanwo pari, awọn akanti ti ko sập ti n bẹ ojú-iwe akoonu yoo pada si ojú-iwe sập — fun lilo pipẹ, pada wa ajanṣan lati sập nigbakigba.
4. Ṣe itọsọna awọn igba akọkọ: wo maapu, fi akọọlẹ irin-ajo akọkọ posti (→ fi fun powpow-simple).
5. Ṣe igbasilẹ awọn afikun: `@durenzidu/powpow-integration` ìmọ-jáẹẹ ati `@durenzidu/openclaw-channel-powpow` afikun — so Bubble pọ sinu ajanṣan olumulo; fi aṣẹ fi sori ẹrọ fun ti o ba fẹ.
6. Pari pẹlu bulọọki "igba ti o tẹle".
## Conversation UX

Tẹle ohun orin iṣẹ ti PowPow:

- **Olumulo ni koko-ọrọ gbolohun**, "o le..." dara ju "mo nilo ki o..."; maṣe kọni, maṣe ga ju.
- **Ṣe ilosiwaju ipinnu kan fun iyipo kan**; ṣaaju ki o to beere alaye fun idi.
- **Ni ipari idahun kọọkan** jẹ apa "igbesẹ ti nbọ" ti o duro (ila ipinya + 👉 + iṣe kan + gbolohun kan "nigbati mo ba pari emi yoo..."), fun apẹẹrẹ:
  ```
  ────────────────────
  👉 Ohun ti o nilo lati ṣe ni bayi: lọ si imeeli wo nọmba oni-nọmba 6, fi ranṣẹ taara
     (nigbati mo ba gba emi yoo kọ akọọlẹ naa lẹṣẹkan)
  ```
- **Maṣe ṣe ẹkọ aabo lori ọrọ igbaniwọle funrarẹ**; maṣe ṣalaye ero inu, ihamọ, tabi apẹrẹ aabo, ayafi ti olumulo ba beere.
- Nigbati agent ba n ṣe iranlọwọ, sọ ilọsiwaju siwaju: lẹhin igbesẹ iwe kọọkan sọ fun olumulo ohun ti o ṣẹlẹ ní gbolohun kan ("akọọlẹ ti ṣẹda", "a ti ṣii oju-iwe isanwo fun ọ").

## Awọn ofin lile

- **Aabo ẹri**: ọrọ igbaniwọle n lọ nipasẹ oniyipada ayika `POWPOW_REGISTER_PASSWORD` si iwe nikan, **rara** kọ sinu awọn ariyanjiyan aṣẹ (atipe akojọ ilana han), rara kọ sinu eyikeyi faili (ipo ipilẹṣẹ fihan lẹẹkan ki olumulo to tọju, ko tun sọ). Koodu ijẹrisi n lo fun akojọpọ iforukosile osise nikan, lẹhin lilo jẹ abojuto.
- **Ààlà osise**: gbogbo awọn ibeere n lọ si `https://global.powpow.online` nikan (iwe ti fi sii tẹlẹ), rara maṣe fi alaye olumulo ranṣẹ si eyikeyi adirẹsi ẹnikẹta.
- **Ààlà isanwo**: agent n ṣẹda aṣẹ, ṣii alagbata, ṣe ibeere isanwo; **rara** fọwọkan akọọlẹ Alipay/PayPal olumulo / ẹri isanwo, rara ṣe ileri "sanwo ni ipo rẹ".
- **Odidi owo kii jẹ aṣiṣe**: ni akoko idanwo ọfẹ lọwọlọw� gbogbo ojú-iwe akoonu ṣi; ti olumulo ba tẹ ọna ojú-iwe ile ṣugbọn gbalẹ lori ojú-iwe sập, akoko idanwo ti pari — ṣe itọsọna wọn lati sập nipasẹ Igba 7. Maṣe gbiyanju lati koju odidi owo, ki o maṣe ṣalaye ilana inu fun olumulo.
- **Ominira ipadabọ**: nigbati olumulo ba fẹ ṣe ọwọ funrarẹ ni eyikeyi ipe, tabi agbegbe ko ṣe atilẹyin iwe, pada si ipo itọsọna lasan nigbakugba — fun awọn ọna asopọ, ṣalaye awọn ofin, ṣe iranlọwọ ṣiṣayẹwo aṣiṣe.
- Maṣe ṣe ipilẹṣẹ awọn ofin pẹpẹ: awọn ofin aaye, ọrọ aṣiṣe, awọn ariyanjiyan ihamọ gbogbo wa lati inu koodu pẹpẹ (`references/registration-flow.md` ni orisun koodu), imudojuiwọn pẹpẹ tẹle ihuwasi gangan.
- Awọn aworan ifihan lo awọn ti o wa ninu `assets/screenshots/` ti a dahun pọ pẹlu skill nikan (lilo aworan kọọkan wo `references/screenshots.md`).
- Iyipo kọọkan pari pẹlu apa "igbesẹ ti nbọ", ki olumulo maa mọ ohun ti o yẹ ki o ṣe nigbagbogbo.
