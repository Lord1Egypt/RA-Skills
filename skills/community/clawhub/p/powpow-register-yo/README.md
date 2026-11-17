# powpow-register

Oluranlọwọ iforukosile PowPow Bubble (ẹ̀dà OpenClaw): mu olumulo tuntun lati "ko mọ ohun ti Bubble jẹ" de "akọọlẹ ti mu ṣiṣẹ, wiwọle ọkan-tẹ, bẹrẹ ere" — ifihan ọja (pẹlu awọn aworan akojade), iforukosile ti agent ṣe iranlọwọ (pẹlu ikojade aworan profaili taara), ṣiṣe aṣẹ ṣiṣe alaisanfarasin Alipay/PayPal ati tọpa isanwo, wiwọle ọkan-tẹ nipasẹ awọn ọna asopọ meji, ṣiṣayẹwo aṣiṣe.

**Lati v2.0.0 eyi jẹ ipo iranlọwọ-ajanṣan, ati lati v2.2.0 o baamu akoko idanwo ọfẹ sajoo**: iwe ipilẹ `scripts/powpow-register.mjs` jẹ kini-ṣi-ẹrọ-orisun
(Node ≥ 18); olumulo jade kuro ninu iwiregba lẹẹkan kan: lati wo koodu ifẹsẹmulẹ ni apoti-ìwé rẹ. Ni akoko idanwo ọfẹ lọwọlọwọ, akanti ti o forukọsilẹ le lo gbogbo ẹya lẹsẹkẹsẹ — owo sập jẹ ilọsi aṣayan; ti akoko idanwo pari ati olumulo gbalẹ lori ojú-iwe sập, ilana pada si ọna owo laifọwọyi. Laisi Node, tabi nigbati olumulo fẹ ṣe funrarẹ, o pada si ipo itọsọna pipẹ laifọwọyi.

## Fifi sori ẹrọ

```
openclaw skills install @durenzidu/powpow-register
```

## Awọn ẹya

1. **Ifihan ọja**: ifihan ọrọ bii 120 + awọn aworan akojade ti a dahun pọ pẹlu skill (`assets/screenshots/` labẹ rẹ aworan 6: oju-iwe maapu, oju-iwe alaye ifiweranṣẹ, ati bẹbẹ, yan firanṣẹ 1–3 ni ibamu si ipo; ko nilo ibi ipamọ aworan ita, ṣiṣẹ lainẹtiwọọki).
2. **Iforukosile ti a ṣe iranlọwọ**: agent n daba oruko olumulo/oruko ọrẹ, yan ọrọ igbaniwọle (olumulo pese tabi agent ṣe ipilẹṣẹ), firanṣẹ ati fi silẹ nọmba ijẹrisi, ikojade aworan profaili taara (<=5MB kii ṣe SVG), ṣetọju awọn aṣiṣe ti o wọpọ laifọwọyi (ti a lo / ti di ofo / ihamọ).
3. **Iwọle ẹyọkan (awọn ọna meji)**: lẹyin iforukọsilẹ to ṣaṣeyọri, ọna iwọle gbe olumulo taara si ojú-iwe ile (ni akoko idanwo ọfẹ, ẹyọkan ki o wa);
   ti o gbalẹ lori ojú-iwe sập (akoko idanwo pari) tabi olumulo fẹ ilọsi, tẹle ilana sập — lẹhin owo de, ipo iwọle tuntun paṣiparọ ati ọna ọmọ-ẹyọn kikun gbe wọn si ojú-iwe ile
   (nipasẹ ọfa `me?token=` ofeefee sajoo, ti o gbin kuki HttpOnly laifọwọyi).
4. **Ṣiṣe alaisanfarasin**: ọna Alipay (osu ¥6.99 / mẹẹdogun ¥19.99 / ọdun ¥69.99, rira lẹẹkan laisi isọdọtun laifọwọyi) ati PayPal (Premium Monthly, bii $1/oṣu, isọdọtun laifọwọyi, a le fagilee nigbakugba) mejeeji jẹ ti agent ṣe iranlọwọ lati ṣẹda aṣẹ + tọpa isanwo; olumulo okeere pada si PayPal; itọsọna iwo-koodu WeChat / Huawei IAP.
5. **Ṣiṣayẹwo aṣiṣe**: gbigba nọmba ijẹrisi, oruko olumulo/imeeli ti a ti lo, 403 ko tii mu ṣiṣẹ, akọọlẹ ti dii pa, ati bẹbẹ, awọn ọran ti o wọpọ, gbogbo wa lati inu koodu pẹpẹ pẹlu orisun ti a darukọ.

## Eto faili

```
powpow-register/
├── SKILL.md                            # Itọsọna akọkọ (awọn ipo trigger, ilana ipe 8, awọn ofin ohun orin, awọn ofin lile)
├── README.md
├── .clawhubignore
├── assets/
│   └── screenshots/                    # Awọn aworan ọja ti a dahun pọ pẹlu skill (powpow-01~06.jpg)
├── scripts/
│   └── powpow-register.mjs             # Iwe pataki (laisi igbẹkẹle Node>=18, awọn aṣẹ 11)
└── references/
    ├── agent-flow.md                   # Adrhun iwe, ṣiṣan akoko pipe, ero ọna asopọ meji, apẹrẹ aabo
    ├── registration-flow.md            # Awọn ofin aaye, ihamọ, tabili ṣiṣayẹwo aṣiṣe (pẹlu orisun koodu)
    ├── payment-and-activation.md       # Adrhun vibepay Alipay, ṣiṣan imuyipada, ṣiṣayẹwo ọna
    └── screenshots.md                  # Atokọ awọn aworan ti a dahun pọ pẹlu skill + wiwa iyara ipo
```

## Aabo

- **Ọrọ igbaniwọle** n lọ nipasẹ oniyipada ayika nikan sinu ilana iwe, rara kọ si awọn ariyanjiyan aṣẹ, rara tọju si disk, rara wọle si faili ipo; ọrọ igbaniwọle ti agent ṣe ipilẹṣẹ han lẹẹkan nikan ki olumulo to tọju.
- **Nọmba ijẹrisi** n lo fun akojọpọ iforukosile osise nikan, lẹhin lilo jẹ abojuto; faili ipo (imeeli / oruko olumulo / token / nọmba aṣẹ) ti wa ni ipamọ ni folda igba-die eto, ni ipari ṣiṣan `cleanup` nu laifọwọyi.
- **Isanwo**: agent n ṣẹda aṣẹ, ṣii alagbata, ṣe ibeere isanwo; rara fọwọkan akọọlẹ Alipay/PayPal olumulo tabi ẹri isanwo, rara sanwo ni ipo rẹ. Isanwo n ṣẹlẹ nigbagbogbo laarin olumulo ati alagbata osise.
- Gbogbo awọn ibeere n lọ si ibugbe osise `https://global.powpow.online` nikan; ko ni awọn bọtini ikoko.

## Iwe-aṣẹ

MIT-0 (iwé-àṣẹ ClawHub ti iṣọkan).

## Awọn ọna asopọ

- Oju opo osise: https://global.powpow.online
- Iforukosile: https://global.powpow.online/register
- Mọ Bubble (fidio): https://www.bilibili.com/video/BV1Wu826UEVz/
