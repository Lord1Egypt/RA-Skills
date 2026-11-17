# powpow-register

Mosalisi ya inscription ya PowPow Bule (version OpenClaw): koyekemela mosaleli ya sika uta «ayebi te Bule ezali nini» kino «kompte ezali active, koneksione ya kubeta mbala moko, ebandi kolala» — presentation ya produit (na lilinzo ya interface), inscription na agent esalaka (na upload ya lilinzo ya profil), commande ya abonnement Alipay/PayPal na kolandela mbongo ekota, koneksione ya kubeta mbala moko na liens mibale, kotunga mbeba.

**Kobanda na v2.0.0 oyo ezali mode ya aide ya agent, pe kobanda na v2.2.0 ebongisami na période d'essai gratuit ya plateforme**: script central `scripts/powpow-register.mjs` azali na dépendances zéro
(Node ≥ 18); motaleli atikaka masolo mbala moko sé: mpo na komona code de vérification na boîte de réception. Na période d'essai gratuit lelo, compte enregistré akoki kosalisa ba fonctionnalités nionso mbala moko — paiement ya abonnement ezali amélioration ya option; soki période d'essai esili pe motaleli akwei na page d'abonnement, flux ebongolaka yango moko na chemin ya paiement. Soki Node te, to tango motaleli alingi kosala yango moko, ezali koleka automatique na mode ya guide pur.

## Installation

```
openclaw skills install @durenzidu/powpow-register
```

## Makambo ya kosala

1. **Presentation ya produit**: presentation ya maloba ~120 + lilinzo ya interface ezali deja na pack (`assets/screenshots/` na se yango lilinzo 6: lokasa ya mapa, lokasa ya detail ya post, nsn., pona situation tinda 1–3; esengi image host ya libanda te, esalelama hors ligne).
2. **Inscription na agent**: agent epesa ndingisa kombo ya mosaleli/surnom, password pona mibale (mosaleli apesa to agent esali), kotinda na kutinda kodi ya ndingisa, upload direct ya lilinzo ya profil (<=5MB te SVG), kosunga automatiquement mbeba ya mbala mingi (deja pris/ekufi/limite).
3. **Kokota na clic moko (ba liens mibale)**: mbala moko nsima ya enregistrement elongi, lien ya kokota ememaka motaleli directement na page d'accueil (na période d'essai gratuit, clic moko pe esalaka);
   soki akwei na page d'abonnement (période d'essai esili) to motaleli alingi amélioration, landa flux d'abonnement — nsima ya argent ekwei, état ya kokota ya sika ebongolami pe lien ya membre mobimba ememaka ye na page d'accueil
   (via pont officiel `me?token=` ya plateforme, oyo atiaka cookie HttpOnly automatique).
4. **Abonnement na kofuta**: Alipay (mois ¥6.99 / trimestre ¥19.99 / annee ¥69.99, achat mbala moko ko-renouveler automatiquement te) na PayPal (Premium Monthly, soki $1/mois, e-renouveler automatiquement, ko-annuler ntango nionso) nyonso mibale agent esala commande + kolandela mbongo ekota; scan WeChat / Huawei IAP lakisa nzela.
5. **Kotunga mbeba**: kodi ya ndingisa ekomi te, kombo ya mosaleli/imele deja pris, 403 ezali active te, kompte efungami, nsn. makambo ya mbala mingi, nionso ewuti na code ya plateforme mpe ezali na source.

## Structure ya fichiers

```
powpow-register/
├── SKILL.md                            # Guide monene (conditions ya trigger, mosala ya etapes 8, mangonga ya voix, mangonga makasi)
├── README.md
├── .clawhubignore
├── assets/
│   └── screenshots/                    # Lilinzo ya produit ezali na pack (powpow-01~06.jpg)
├── scripts/
│   └── powpow-register.mjs             # Script monene (dependance te Node>=18, commandes 11)
└── references/
    ├── agent-flow.md                   # Contract ya script, molongo mobimba, mecanisme ya liens mibale, design ya securite
    ├── registration-flow.md            # Mangonga ya champs, limites, table ya kotunga mbeba (na source ya code)
    ├── payment-and-activation.md       # Contract ya vibepay Alipay, molongo ya activation, kotunga nzela
    └── screenshots.md                  # Liste ya lilinzo ya pack + koluka mbala moko ya situation
```

## Securite

- **Password** etindama kaka na variable d'environnement na processus ya script, jamais na parametre ya commande, jamais na disque, jamais na fichier etat; password oyo agent esali emonana mbala moko kaka mpo mosaleli abomba.
- **Kodi ya ndingisa** esalelaka kaka API officielle ya inscription, esila esalema ebwakama; fichier etat (imele/kombo ya mosaleli/token/nombo ya commande) ezali na repertoire temporaire ya systeme, nsila ya mosala `cleanup` efaceraka automatiquement.
- **Kofuta**: agent esala kaka commande, efungola caisse, etuna mbongo; jamais ekanga compte ya Alipay/PayPal ya mosaleli to identite ya kofuta, jamais efuta na esika ya mosaleli. Kofuta esalaka mbala nionso na kati ya mosaleli na caisse officielle.
- Ba requetes nionso etindaka kaka domaine officiel `https://global.powpow.online`; ezali na cle te.

## Licence

MIT-0 (licence ya ClawHub, moko moko).

## Liens

- Site officiel: https://global.powpow.online
- Inscription: https://global.powpow.online/register
- Yeba Bule (video): https://www.bilibili.com/video/BV1Wu826UEVz/
