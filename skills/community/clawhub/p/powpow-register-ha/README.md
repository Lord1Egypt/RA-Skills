# powpow-register

Mai taimakon rijistar PowPow kumfa (bugu na OpenClaw): yana kai sabon mai amfani daga "ba ya san kumfa abin da yake" zuwa "akaunti ta kunno, shiga da danna sau ɗaya, fara wasa" — gabatarwar samfur (tare da hotunan allo), rijista agent tana taimakawa (tare da ɗora avatar), oda membanci ta Alipay/PayPal da bin diddigin shigar kuɗi, shiga da danna sau ɗaya da mahadi biyu, bincike da gyaran kuskure.

**Tun daga v2.0.0 wannan yanayin magidiman ne, kuma tun daga v2.2.0 yana daidaita da lokacin gwaji kyauta na yanar gizo**: rubutu na asali `scripts/powpow-register.mjs` ba shi da bukatar abun biya
(Node ≥ 18); mai amfani yana barin tattaunawa sau daya kawai: don duban lambar tabbatar da a akwatin sakonni. A cikin lokacin gwaji kyauta na yanzu, asusu da aka yi rajista zai iya amfani da dukkan fannoni nan take — biyan kudi na biya kari ne na zabi; in lokacin gwaji ya kare kuma mai amfani ya sauka a shafin biya, jawardar tana sauya kanta zuwa hanyar biya. Ba tare da Node, ko sa'adda mai amfani ya fi son yin shi da kansa, yana koma kai tsaye zuwa yanayin jagorar tsantsa.

## Shigarwa

```
openclaw skills install @durenzidu/powpow-register
```

## Ayyuka

1. **Gabatarwar samfur**: gabatarwa da kalmomi ~120 + hotunan allo da aka haɗe da kunshin (a ƙarƙashin `assets/screenshots/` hotuna 6: shafin taswira, shafin cikakken bayanin sako, da sauransu, a zaɓa a aika 1–3 bisa yanayi; ba buƙatar mashigar hoto ta waje, tana aiki ba tare da intanet ba).
2. **Rijistar agent tana taimakawa**: agent na ba da shawarar sunan mai amfani/laƙabi, kalmar sirri zaɓi ɗaya (mai amfani ya kawo ko agent ta ƙirƙira), aikawa da ƙaddamar da lambar tabbatarwa, ɗora avatar kai tsaye (≤5MB ba SVG ba), kula da kuskuren da aka saba ta kai (ma'amala/ƙarewa/iyakancewa).
3. **Shiga da danna daya (hanyoyi biyu)**: nan take bayan rajista ta samu nasara, hanyar shiga tana kai mai amfani kai tsaye zuwa shafin gida (a lokacin gwaji kyauta, danna daya kuma yana amfani);
   in ya sauka a shafin biya (lokacin gwaji ya kare) ko mai amfani ya so kari, bi jawardar rajista — bayan saukar kudi, ana musanya sabon yanayin shiga kuma hanyar cikakken mamba tana kai shi zuwa shafin gida
   (ta hanyar gada `me?token=` na yanar gizo na hukuma, wanda ke dasa kuki na HttpOnly kai tsaye).
4. **Membanci da biya**: Alipay (wata ¥6.99 / kwata ¥19.99 / shekara ¥69.99, biya sau ɗaya ba ya sabunta kansa) da PayPal (Premium Monthly, kusan $1/wata, yana sabunta kansa, ana iya soke shi kowane lokaci) duka agent tana taimakawa ƙirƙirar oda + bin diddigin shigar kuɗi; nuna hanyar siffanta lambar QR ta WeChat / Huawei IAP.
5. **Bincike da gyaran kuskure**: karɓar lambar tabbatarwa, sunan mai amfani/imel an yi amfani da su, 403 ba ta a kunna ba, asusu an kulle da sauran matsalolin da aka saba, duka sun fito daga code ɗin dandalin kuma an ambaci inda aka samo su.

## Tsarin fayil

```
powpow-register/
├── SKILL.md                            # Babban jagora (ka'idojin kunna, tsarin matakan 8, dokokin salo, ka'idojin ƙarfi)
├── README.md
├── .clawhubignore
├── assets/
│   └── screenshots/                    # Hotunan samfur da aka haɗe da kunshin (powpow-01~06.jpg)
├── scripts/
│   └── powpow-register.mjs             # Babban script (ba dogaro Node>=18, umarnin 11 na ciki)
└── references/
    ├── agent-flow.md                   # Kwangilar script, cikakken tsarin lokaci, tsarin mahadi biyu, zanen tsaro
    ├── registration-flow.md            # Dokokin filaye, iyakancewa, teburin gyaran kuskure (tare da inda aka samo su)
    ├── payment-and-activation.md       # Kwangilar vibepay ta Alipay, hanyar kunnawa, binciken hanyoyi
    └── screenshots.md                  # Jerin hotunan kunshin + bincike mai sauri na yanayi
```

## Tsaro

- **Kalmar sirri** tana wucewa ga aiwatar da script ɗin ta canjin muhalli kawai, kada ta rubuta a cikin mahawarin umarni, kada ta sauka a kan diski, kada ta shiga fayil ɗin hali; kalmar sirrin da agent ta ƙirƙira ana nunta sau ɗaya kawai domin mai amfani ya adana.
- **Lambar tabbatarwa** ana amfani da ita da tashar hukuma ta rijista kawai, bayan amfani a jefar da ita; fayil ɗin hali (imel/sunan mai amfani/token/lambar oda) yana cikin babban fayil ɗin wucin gadi na tsarin, a ƙarshen tsarin `cleanup` yana sharewa da danna ɗaya.
- **Biya**: agent ɗin ƙirƙirar oda kawai take yi, buɗe cashier, duba shigar kuɗi; kada ta taba asusun Alipay/PayPal na mai amfani ko takaddun biya, kada ta biya a madadinsa. Biya koyaushe yana faruwa tsakanin mai amfani da cashier na hukuma.
- Duk buƙatun suna tafiya ga adireshin hukuma `https://global.powpow.online` kawai; ba sa ɗauke da wata sirri.

## Lasisi

MIT-0 (lasisin ClawHub ɗaya ga kowa).

## Mahadi

- Shafin hukuma: https://global.powpow.online
- Rijista: https://global.powpow.online/register
- Sanin kumfa (bidiyo): https://www.bilibili.com/video/BV1Wu826UEVz/
