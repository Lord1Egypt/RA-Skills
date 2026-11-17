# powpow-register

Msaidizi wa usajili wa PowPow Povu (toleo la OpenClaw): kuleta mtumiaji mpya kutoka "hajui Povu ni nini" hadi "akaunti imewezeshwa, ingia kwa kubofya mara moja, anze kucheza" — utangulizi wa bidhaa (pamoja na picha za kiolesura), usajili unaosaidiwa na agent (pamoja na upakiaji wa picha ya wasifu moja kwa moja), agizo la usajili wa Alipay/PayPal na ufuatiliaji wa malipo, ingia kwa kubofya mara moja kupitia viungo viwili, utatuzi wa makosa.

**Tangu v2.0.0 hii ni hali ya wakala-msaidizi, na tangu v2.2.0 inajirekebisha kwa kipindi cha majaribio bila malipo cha jukwaa**: hati kuu `scripts/powpow-register.mjs` ni zero-dependency
(Node ≥ 18); mtumiaji anaacha mazungumzo mara moja tu: kukagua msimbo wa uthibitishaji kwenye kikasha chake. Katika kipindi cha sasa cha majaribio bila malipo, akaunti iliyosajiliwa inaweza kutumia kila kipengele mara moja — malipo ya sasiri ni uboreshaji wa hiari; kama kipindi cha majaribio kinaisha na mtumiaji anatua kwenye ukurasa wa sasiri, mtiririko unabadilika kwenye njia ya malipo kiotomatiki. Bila Node, au wakati mtumiaji anaenda kufanya mwenyewe, hurejea kiotomatiki kwenye hali ya mwongozo safi.

## Usakinishaji

```
openclaw skills install @durenzidu/powpow-register
```

## Vipengele

1. **Utangulizi wa bidhaa**: utangulizi wa maneno ~120 + picha za kiolesura zilizofungwa pamoja na skill (`assets/screenshots/` chini yake picha 6: ukurasa wa ramani, ukurasa wa maelezo ya chapisho, n.k., chagua tuma 1–3 kulingana na hali; hahitaji hifadhi ya picha ya nje, inafaa nje ya mtandao).
2. **Usajili unaosaidiwa**: agent inapendekeza jina la mtumiaji/jina la kirafiki, nenosiri uchague moja (mtumiaji atoe au agent itengeneze), kutuma na kuwasilisha nambari ya uthibitisho, upakiaji wa picha ya wasifu moja kwa moja (<=5MB sio SVG), kushughulikia makosa ya kawaida kiotomatiki (kuchukuliwa/kuisha/mzigo wa kizuizi).
3. **Kuingia kwa bonyezo moja (viungo viwili)**: mara baada ya usajili kufanikiwa, kiungo cha kuingia kinamweka mtumiaji moja kwa moja kwenye ukurasa wa nyumbani (katika kipindi cha majaribio bila malipo, bonyezo moja na kinapatikana);
   kama kinatua kwenye ukurasa wa sasiri (kipindi cha majaribio kimeisha) au mtumiaji anataka kuboresha, fuata mtiririko wa sasiri — baada ya malipo kufika, hali mpya ya kuingia inabadilishwa na kiungo cha uanachama kamili kinamweka kwenye ukurasa wa nyumbani
   (kupitia daraja rasmi la `me?token=` la jukwaa, linalozalisha kuki ya HttpOnly kiotomatiki).
4. **Usajili wa malipo**: njia zote mbili za Alipay (mwezi ¥6.99 / robo mwaka ¥19.99 / mwaka ¥69.99, ununuzi wa mara moja hauna ushamiri otomatiki) na PayPal (Premium Monthly, takriban $1/mwezi, inashamiri otomatiki, batilisha wakati wowote) zinashughulikiwa na agent kwa kuunda agizo + ufuatiliaji wa malipo; mtumiaji wa nje anarudi PayPal; mwongozo wa usome msimbo wa WeChat / Huawei IAP.
5. **Utatuzi wa makosa**: kutopokea nambari ya uthibitisho, jina la mtumiaji/barua pepe imechukuliwa, 403 haijawa hiyari, akaunti imefungwa, n.k. masuala ya kawaida, yote yanatoka kwenye msimbo wa jukwaa na yana chanzo kilichotajwa.

## Muundo wa faili

```
powpow-register/
├── SKILL.md                            # Mwongozo mkuu (masharti ya trigger, mtiririko wa hatua 8, kanuni za sauti, kanuni ngumu)
├── README.md
├── .clawhubignore
├── assets/
│   └── screenshots/                    # Picha za bidhaa zilizofungwa pamoja na skill (powpow-01~06.jpg)
├── scripts/
│   └── powpow-register.mjs             # Hati kuu (haina tegemezi Node>=18, amri 11 za kifaa)
└── references/
    ├── agent-flow.md                   # Mkataba wa hati, mlolongo kamili, utaratibu wa viungo viwili, muundo wa usalama
    ├── registration-flow.md            # Sheria za sehemu, vizuizi, jedwali la utatuzi wa makosa (pamoja na chanzo la msimbo)
    ├── payment-and-activation.md       # Mkataba wa vibepay ya Alipay, mlolongo wa uwezeshaji, utatuzi wa njia
    └── screenshots.md                  # Orodha ya picha zilizofungwa pamoja na skill + utafutaji wa haraka wa hali
```

## Usalama

- **Nenosiri** hutumiwa tu kupitia kigezo cha mazingira kuingia kwenye mchakato wa hati, kamwe usiiandike kwenye vigezo vya amri, usiihifadhi kwenye diski, usiiingize kwenye faili ya hali; nenosiri lililotengenezwa na agent linaonyeshwa mara moja tu ili mtumiaji ahifadhi.
- **Nambari ya uthibitisho** hutumiwa tu kwa kiolesura rasmi cha usajili, inapotumika inaachwa; faili ya hali (barua pepe / jina la mtumiaji / token / nambari ya agizo) imehifadhiwa katika saraka ya muda ya mfumo, mwisho wa mtiririko `cleanup` inafuta kiotomatiki.
- **Malipo**: agent huunda agizo, hufungua cashier, hufuatilia malipo; kamwe haigusi akaunti ya Alipay/PayPal ya mtumiaji au kitambulisho cha malipo, kamwe hailipi badala yake. Malipo yanafanyika kila wakati kati ya mtumiaji na cashier rasmi.
- Maombi yote yanaenda tu kwenye kikoa rasmi `https://global.powpow.online`; hayana funguo yoyote.

## Leseni

MIT-0 (leseni ya ClawHub iliyo umoja).

## Viungo

- Tovuti rasmi: https://global.powpow.online
- Usajili: https://global.powpow.online/register
- Jua Povu (video): https://www.bilibili.com/video/BV1Wu826UEVz/
