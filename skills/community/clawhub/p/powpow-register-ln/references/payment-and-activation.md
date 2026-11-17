# Activation ya abonnement na kofuta — powpow-register

## Conclusion (reponse liboso)
> **Période d'essai gratuit (kobanda 2026-10-18; comportement réel ya plateforme ezali oyo eleki)**: na période oyo compte enregistré akoki kosalisa ba fonctionnalités nionso directement, pe **sala abonnement ezali amélioration ya option te exigence** — landa flux ya fichier oyo sé tango motaleli moko alingi membre. Tango période d'essai esili, ba comptes sans abonnement tango bakokota na ba pages ya contenu bakozwa redirection na page d'abonnement; silisa abonnement selon fichier oyo.


**Nzela ya Alipay na PayPal nyonso mibale sikoyo ekoki kosalema na agent — kosala commande na kolandela mbongo ekota.**
Alipay ezali achat mbala moko, e-renouveler automatiquement te, mpo na ba mosaleli ya Chine na ba oyo bazali na Alipay; PayPal e-renouveler automatiquement chaque mois mpe ekoki ko-annuler ntango nionso,
mpo na ba mosaleli ya mboka mosusu na ba oyo bazali na Alipay te. Scan WeChat (confirmation ya moto) na Huawei IAP ezali naino, kasi skill esala yango te.

Ndelo ya responsabilité na se ya kofuta: agent ekoki **sala commande, fungola caisse, tuna mbongo**; **jamais** ekanga compte ya Alipay/PayPal ya mosaleli / identite ya kofuta, jamais epromettre «kofuta na esika ya mosaleli». Action ya kofuta mbala nionso esalaka na mosaleli moko moko na caisse officielle.

## Nzela ya Alipay (vibepay, monene)

Systeme ya achat mbala moko: futa mbala moko mpo ofungola duree ekokani, **ko-renouveler automatiquement te**. Plans ekangami na
`src/lib/alipay-vibepay.ts` (`ALIPAY_PACKAGES`):

| key | planId | Nkomba | Motango | Duree |
|---|---|---|---|---|
| `monthly` | alipay-monthly | Membre ya mois | ¥6.99 | jours 30 |
| `quarterly` | alipay-quarterly | Membre ya trimestre | ¥19.99 | jours 90 |
| `yearly` | alipay-yearly | Membre ya annee | ¥69.99 | jours 365 |

### Contract ya interfaces (script ya skill ekanga deja, agent assembla requete directement te)

| Interface | Methode | Explication |
|---|---|---|
| `/api/payment/alipay/create-order` | POST | Esengi `Authorization: Bearer <JWT>` (mosaleli pending ekoki). body `{package}` → ezongisa `{paymentHtml, outTradeNo, amount, planName}`; `paymentHtml` ezali lokasa ya fome etindaka automatiquement na passerelle ya Alipay |
| `/api/payment/alipay/query` | GET `?outTradeNo=` | Ndenge moko auth ya Bearer. Ezongisa `paid` / `pending` / `closed` / `unknown` |
| `/api/payment/alipay/notify` | POST (callback ya serveur Alipay) | Verification ya signature ya elements misato (signature, app_id, montant ekokana, TRADE_SUCCESS/TRADE_FINISHED, unicite ya marchand) → **idempotent** mise a jour ya commande + kosala abonnement + ko-activer kompte. Skill jamais etuna interface oyo |
| `/payment/alipay/return` | Lokasa ya retour ya navigateur | Chemin public, nsima ya kofuta elakisa confirmation «支付成功» (kofuta esilama), lokasa epoller etat reel ya backend |

- Commande non payée **efungwama automatiquement nsima ya heures 2**; mosaleli abwaka na katikati → directement sala lisusu `create-order`, commande ya kala likambo te.
- Script ekoma `paymentHtml` na fichier HTML temporaire, agent esalela commande ya systeme mpo efungola na caisse ya Alipay (scan to akota na Alipay afuta).

### Molongo ya activation (automatique, moto esengi te)

notify verification ya signature eleki → `paymentOrders` elakisa payé → `user_subscriptions` esala/etindaka liboso
(`planId`, `currentPeriodEnd` calculer na durationDays, renouvellement etindaka liboso na date ya expiration ya kala) →
`users.accountStatus: active` + `subscriptionStatus: ACTIVE` → lokasa ya retour epoller kino paid elakisa succes.

### Nsima ya kofuta esengi echangala etat ya koneksione sika (monene)

JWT ezali na declaration ya abonnement (kompte pending ezali `NONE`). **Kofuta ekota echangaka base de donnees kaka, echangaka JWT déjà signe te** — declaration ya token ya kala naino NONE, osalela directement mpo sala lien ya koneksione ekomonana «membre te».
Ndenge wana skill nsima ya confirmation `paid` / PayPal `ACTIVE` liboso esala `refresh-login` (koneksione lisusu echangala JWT sika, declaration ekomi ACTIVE), nsima sala lien 2. Yango ezali comportement ya design, ezali correction ya bug te.

## Nzela ya abonnement PayPal (agent esalaka yango; web, HarmonyOS te)

Plan moko kaka ezali, Premium Monthly (soki $1/mois, ndenge `/api/subscription/plans` ezongisaka); **e-renouveler automatiquement chaque mois**
mpo mosaleli akoki ko-annuler ntango nionso na compte na ye ya PayPal.

### Contract ya API (esili ko-emballer na script ya skill; agent asangisaka requête moko moko te)

| Endpoint | Methode | Note |
|---|---|---|
| `/api/subscription/plans` | GET | Auth Bearer; ezongisaka liste ya ba plans ezali (sikoyo moko kaka) |
| `/api/subscription/create` | POST | Corps `{planId}` → ezongisaka `{subscriptionId, approveUrl, status}`; `status` mingi ezali `APPROVAL_PENDING` |
| `/api/subscription/create` | GET | Auth Bearer; ezongisaka `{activeSubscription, allSubscriptions}`; agent atunaka `activeSubscription.subscription.status === 'ACTIVE'` |
| `/api/subscription/verify` | POST | Lokasa ya succès ebengaka yango automatiquement (na cookie); e-activer na API ya PayPal directement soki webhook ekomi naino te |
| `/subscription/success` | Lokasa ya retour ya navigateur | Lokasa ya kokita nsima ya ndingisa PayPal; e-poller verify automatiquement, nsima ezonga na lokasa ya ndako / lokasa ya kala |
| `/subscription/cancel` | Lokasa ya navigateur | Lokasa ya kokita ntango mosaleli a-annuler to esali échec; essai ya sika ekoki kobanda |

### Molongo ya agent

```
create-order --provider paypal   # → ezongisaka approveUrl, ekomama na fichier HTML local
open the HTML file               # → navigateur ezo zwa nzela na lokasa ya ndingisa PayPal
query (chaque secondes 10–15)    # → poller kino ACTIVE
refresh-login                    # → echanger JWT sika (declaration ya abonnement ACTIVE)
login-link --target home         # → sala lien officiel ya koneksione
```

- Ba abonnements PENDING oyo esilama te na kati ya heure 1, backend epetolaka yango automatiquement; banda lisusu.
- Soki mosaleli asali lisusu `create-order`, backend esalelaka lisusu abonnement `APPROVAL_PENDING` oyo ezali naino valide, eboya 409.
- Ndenge moko na Alipay: mbongo ekota ebongisaka kaka DB — JWT ya kala e-renouveler automatiquement te, yango wana **esengeli** osala `refresh-login` liboso ya kotinda lien ya lokasa ya ndako.

## Nzela nionso ya lokasa ya abonnement

Lokasa ya abonnement `src/app/(public)/subscription/page.tsx` elakisa selon environnement ya kosala:

| Nzela | Environnement | Mecanisme | Ndenge ya activation |
|---|---|---|---|
| **Alipay (monene)** | Web | `AlipayPaymentSection` na interfaces ya vibepay (table oyo na se) | notify serveur activation automatique, secondes |
| Abonnement PayPal | Web (te Harmony) | `/api/subscription/create` → kende na autorisation ya PayPal; renouvellement ya chaque mois ekoki annuler mbala nionso (`/api/subscription/manage`) | PayPal Webhook (`BILLING.SUBSCRIPTION.*`) ekoma active automatiquement |
| Abonnement «微信扫码订阅» (scan WeChat) | Web (te Harmony) | na se ya lokasa: scan transfert ya mbongo | **confirmation ya moto**, mbongo ekoki kuchelewa; nsima ya kofuta juger echec mbala moko te |
| Achat na kati ya app Huawei | Na kati ya app Harmony | Natif `NativeBridge.purchaseSubscription()` | `/api/subscription/activate-huawei` everifier commande ya Huawei nsima activer |

Plans na motango ya PayPal ewuti dynamique na `/api/subscription/plans`; texte fixe ya lokasa: Auto-renews. Cancel anytime.

## Etat na redirection

- Alipay nsima ya kofuta → lokasa ya retour elakisa succes; PayPal succes → `/subscription/success` → kompte active →
  redirection automatique na lokasa ya libanda oyo parametre `next` elobi (ezali te lokasa ya libanda).
- Mosaleli déjà abonné afika lokasa ya abonnement → elakisa "You're All Set!", nsima ya secondes 3 ezonga lokasa ya libanda automatiquement.
- Kofuta echec/annulé (PayPal) → `/subscription/cancel`, ekoki lancer lisusu.

## Kotunga

| Tukio | Kosunga |
|---|---|
| Alipay nsima ya kofuta `query` naino pending | notify kuchelewa mingi mingi te; zela secondes 30 nsima tuna lisusu. Bado ezali te pesa mosaleli ezonga navigateur komona etat ya lokasa ya retour, bado ezali te contacter support ya plateforme (dongtao@outlook.com), pesa `outTradeNo` |
| Alipay nsima ya kofuta, lien 2 ekota naino ebombama | elibi `refresh-login` (declaration ya JWT ya kala misajour te) — liboso `refresh-login` nsima `login-link` |
| PayPal `query` etikali PENDING | Mosaleli asilisi ndingisa na PayPal te; tala soki lien ya ndingisa efungwama na navigateur. Soki ezali naino PENDING nsima ya ndingisa, webhook ekoki kochelewa — tika mosaleli azela secondes moke na lokasa ya succès to a-refresh |
| PayPal `query` ezongisi 409 | Abonnement PENDING moko esilama naino te; zela heure 1 esila, to silisa ndingisa ya lien ya kala na navigateur |
| PayPal nsima ya kofuta, lien 2 ekota naino ebombama | Ndenge moko na Alipay: liboso `refresh-login` nsima `login-link` |
| Nsima ya kofuta naino 403 (PayPal) | Webhook mbala mosusu kuchelewa, koneksione lisusu mpo refresh etat |
| WeChat efuti kasi efungolami te | confirmation ya moto ezali asynchrone, na kati ya heures ebele efungolami te contacter support ya plateforme |
| Lokasa ya abonnement elakisa "No subscription plans available" | `/api/subscription/plans` ezali na plan PayPal disponible te, likambo ya configuration ya plateforme; mosaleli ya Chine abadila na Alipay kaka |

## Note ya histoire

Na code ezali na ensemble **ya kala** ya paiement web Alipay (`src/lib/alipay.ts`, `/api/payment/create-order`,
¥9.90/¥99 achat mbala moko, sandbox na cle te ekita na paiement ya simulation), jamais ekangami na UI ya lokasa ya abonnement, ezali na lien na vibepay te. Skill jamais etuna yango; `alipay-vibepay.ts` nde nzela oyo ezali kosalelama sikoyo.
