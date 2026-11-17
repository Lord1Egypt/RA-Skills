# Molongo ya agent esalaka na contract ya script — powpow-register

Detail ya execution ya etapes nionso ya SKILL.md. Commandes nionso ezali `node scripts/powpow-register.mjs <commande> [params]`, script **ezali na dependance te**, esengi **Node >= 18**, ba requetes nionso etindaka kaka `https://global.powpow.online`.

## Design ya securite (mbala nini esali ndenge wana)

| Design | Tina |
|---|---|
| Password etindaka kaka na variable d'environnement `POWPOW_REGISTER_PASSWORD` | parametres ya commande ya processus emonana na processus mosusu ya machine oyo (surface ya fuite argv), variable d'environnement na kati ya script esomaka mpe esalelama mbala moko |
| Password **jamais ekoma na fichier etat**, jamais emonana na logs | fichier etat ekoki kofanda na disque; mode generation elakisa mbala moko kaka mpo mosaleli abomba |
| Fichier etat ezali na repertoire temporaire ya systeme (`os.tmpdir()/powpow-register-state.json`, 0600) | ezali na champs tano kaka: email / username / nickname / token / outTradeNo, `cleanup` efaceraka mbala moko |
| JWT oyo agent azwa echangama na cookie ya navigateur na pont officiel `me?token=` | pont officiel oyo plateforme esali mpo na WebView ya Harmony; verification ya signature etala kaka signature + validite, ekanga empreinte ya appareil te, navigateur ya mosaleli ekoki kosalela |
| Kofuta esala kaka create-order / query / kofungola caisse | action ya kofuta na identite ya kofuta mbala nionso ezali na kati ya mosaleli na caisse officielle ya Alipay, agent apasi te |

## Reference ya commandes

| Commande | Params monene | Mosala / ntango |
|---|---|---|
| `status` | —— | Tala progres ya mosala (soma fichier etat); nsima lisolola ekatama sala yango liboso |
| `gen-password` | —— | Sala password ya makasi ya caracteres 24 (MAJUSCULE+minuscule+nombo), emonana na stdout **mbala moko kaka** |
| `prepare-suggest` | `--username --nickname --email` | Koma bansongo oyo epanzani na fichier etat (nsima register esengi kotinda lisusu te) |
| `send-code` | `--email` | Peser plateforme etinda kodi ya nombo 6 (valide miniti 10, cooldown secondes 60) |
| `register` | `--code` (obligatoire); `--username --nickname --avatar --phone` (optionnel, soki fichier etat ezali na yango esengi te) | Sala kompte pending; password na variable d'environnement `POWPOW_REGISTER_PASSWORD`; nsima succes JWT ekanda automatiquement na fichier etat |
| `login-link` | `--target pending` to `--target home` | Esalaka lien ya kokota na clic moko (design ya ba liens mibale, tala awa na se) |
| `create-order` | `--package monthly\|quarterly\|yearly` (défaut Alipay)<br>`--provider alipay\|paypal` | Sala commande ya kofuta; Alipay ezongisa chemin ya fichier ya lokasa ya kofuta + outTradeNo; PayPal ezongisa chemin ya fichier ya lokasa ya ndingisa + subscriptionId (ekanda automatiquement na fichier etat) |
| `query` | —— | Tuna etat ya commande/abonnement. Alipay: `paid / pending / closed / unknown`; PayPal: `ACTIVE / PENDING`; poller chaque secondes 10–15 |
| `refresh-login` | Password na variable d'environnement | Koneksione lisusu mpo azwa **JWT sika** (declaration ya abonnement echangaka uta NONE kino ACTIVE), obligatoire nsima mbongo ekota |
| `whoami` | —— | Salela token ya fichier etat tona etat ya kompte na abonnement (verifier activation esalaka) |
| `cleanup` | —— | Facera fichier etat (obligatoire na nsila) |

**Etinda variable d'environnement** (password jamais na commande):

```bash
# bash / zsh / WSL
POWPOW_REGISTER_PASSWORD='<password>' node scripts/powpow-register.mjs register --code 123456
# PowerShell
$env:POWPOW_REGISTER_PASSWORD = '<password>'; node scripts/powpow-register.mjs register --code 123456
# cmd
set POWPOW_REGISTER_PASSWORD=<password> && node scripts/powpow-register.mjs register --code 123456
```

## Mécanisme ya ba liens mibale (design central)

État ya kokota ya plateforme ezali cookie HttpOnly, oyo agent akoki kotya yango directement na navigateur te; pont ezali endpoint officiel
`/api/auth/me?token=<JWT>&redirect=<chemin na kati ya site>`: vérifier signature → création automatique
session → `Set-Cookie: powpow_token` (HttpOnly / SameSite=Lax / 7 jours) → valider
redirect (esengeli abanda na slash moko, `//` pe ba slash ya nsima epekisami, esengeli ezala same-origin nsima ya analyse) → 307 redirection temporaire na page cible.

Ba cibles ya lien mibale ezali, **liboso créer home, nsima décider passer par to te selon epai motaleli akwei**:

- **lien home (etindami par défaut, `--target home` → akwei na `/`)**: ecreami pe etindami na motaleli mbala moko nsima ya enregistrement elongi.
  Na période d'essai gratuit motaleli akende directement na page d'accueil, utilisation mobimba; **soki abendi lien pe akwei na page d'abonnement — période d'essai gratuit esili** — bongola na flux ya paiement (tala awa na se); bosenga te ya kobongola script pe enregistrement lisusu.
- **lien pending (esalemi na flux ya paiement, `--target pending` → akwei na `/subscription`)**:
  navigateur ya motaleli ekoti na état "demi-kokota": page d'abonnement pe page ya retour nsima ya paiement emonani pe esalaka. Nsima ya argent ekwei,
  salisa `refresh-login` mpo na bongola JWT ya sika na affirmation ACTIVE, nsima tinda lien home lisusu mpo na état ya membre mobimba.

## Ordre mobimba

### Chemin rapide (na période d'essai gratuit — majorité ya ba cas)

```
1.  status                          # auto-vérification d'environnement
2.  (étape 2 masolo mpo na confirmer informations, mot de passe nionso; mode généré: gen-password → láta motaleli abomba mbala moko)
3.  prepare-suggest --username U --nickname N --email E
4.  send-code --email E             # → motaleli atala code na boîte de réception (tangoko ya kokabola masolo)
5.  POWPOW_REGISTER_PASSWORD=*** register --code 123456 [--avatar pic.jpg]
6.  login-link --target home        # → tinda lien na motaleli; clic moko pe na page d'accueil
7.  (motaleli andimisi akoti) → silisa directement: cleanup + carte de compte + lakisa ba étapes ya liboso
```

### Chemin ya paiement (tango motaleli alingi membre, to période d'essai gratuit esili)

```
1–5. Lokola chemin rapide (état ezali na token nsima ya enregistrement elongi)
6.  login-link --target pending     # → lien demi-kokota, ebombaka page ya retour ya paiement esala
7.  (motaleli apona méthode ya paiement)
    # Alipay: create-order --package monthly|quarterly|yearly
    # PayPal: create-order --provider paypal
8.  start <fichier ya page ya paiement>       # Windows; macOS esaleli open, Linux esaleli xdg-open
    # → motaleli asilisaka paiement/autorisation na caisse Alipay/PayPal (akabwaka masolo)
9.  query (na 10–15s) tii paid / ACTIVE
10. refresh-login                   # bongola JWT ya sika na affirmation ACTIVE
11. login-link --target home        # → tinda lien membre mobimba na motaleli
12. whoami                          # confirmer subscriptionStatus: ACTIVE (option)
13. cleanup                         # petola fichier ya état
```
## Commande → API ya plateforme

| Commande ya script | Interface ya plateforme |
|---|---|
| `send-code` | `POST /api/auth/register/send-code` |
| `register` | `POST /api/auth/register` (multipart, upload direct ya lilinzo ya profil) |
| `login-link` | `GET /api/auth/me?token=…&redirect=…` (lien moko moko, esalaka ntango mosaleli abeta) |
| `create-order` | `POST /api/payment/alipay/create-order` (Bearer, Alipay)<br>`GET /api/subscription/plans` + `POST /api/subscription/create` (Bearer, PayPal) |
| `query` | `GET /api/payment/alipay/query?outTradeNo=…` (Bearer, Alipay)<br>`GET /api/subscription/create` (Bearer, PayPal) |
| `refresh-login` | `POST /api/auth/login` (`{step:1, username, password}`) |
| `whoami` | `GET /api/auth/me?token=…` |

Source ya mangonga: mangonga ya champs na limites ya inscription tala `registration-flow.md`; plans na molongo ya activation tala
`payment-and-activation.md` (nionso ezali na fichier source ya plateforme elakisami).

## Kotunga mbeba ya niveau script

| Tukio | Kosunga |
|---|---|
| `Node 版本过低` (Node version moke koleka) | Zonga na mode ya directives kaka, meka na makasi te |
| Mbeba ya reseau / timeout | Meka mbala moko; bado ebebi pesa mosaleli atala reseau nsima alanda (fichier etat ezali naino, sala `status` uta liboso mpo ezonga) |
| register elobi mbeba ya business (kombo ya mosaleli ezali deja, nsn.) | Landa table ya Etape 5 ya SKILL.md, **kodi ya ndingisa esengi kotinda lisusu te** (valide naino na kati ya miniti 10) |
| register elobi `邮箱验证码错误或已过期` (kodi ya ndingisa ya imele mbeba to ekufi) | Ekufi na ntango → tinda lisusu `send-code` |
| Nsima ya `create-order` mosaleli afunga lokasa ya kofuta | Sala directement lisusu `create-order` (commande ya kala efungwama automatiquement nsima heures 2; ba abonnements PENDING ya PayPal esila nsima heure 1) |
| `create-order --provider paypal` ezongisi 409 | Abonnement PayPal moko esilama naino te; zela heure 1 esila, to silisa ndingisa ya kala na navigateur |
| `query` ezali kofanda pending / PENDING | Ekoki kozala mosaleli afuti te; tuna moko. Asili afuti → landa table ya kotunga ya payment-and-activation.md |
| Motaleli abendi lien home pe akwei na page d'abonnement | Période d'essai gratuit esili → bongola na flux ya paiement: `login-link --target pending` → pona méthode ya paiement → `create-order` |
| `refresh-login` 403 `pending_payment` | Période d'essai gratuit esili pe paiement ekwei te; zonga na étape 9 kokoba interroger, to confirmer soki motaleli asilisaki paiement |
| Fichier etat etangami te (efacami na mabe / ekoti na machine mosusu) | `whoami`/`refresh-login` esalelama te; pesa mosaleli na navigateur oyo efungolaki lien 1 abandisa lokasa ya abonnement mpo aconfirmer etat, to koneksione lisusu (mode web) |

## Mode ya retour (directives kaka)

Na cas nionso oyo elandi, zonga mbala moko na mode ya directives kaka ya v1, souffrir script lisusu te:

- Node >= 18 ezali te to script ebeba mbala mibale moko moko na ndenge moko;
- Mosaleli alobi clairement «ngai moko nakosala na web»;
- Politique ya entreprise/appareil peki script ekende na internet.

Nsima ya kozonga: pesa page d'enregistrement https://global.powpow.online/register (na période d'essai gratuit, enregistrement na web ezali mbala moko rapide; tango abonnement esengeli, pesa page d'abonnement pe https://global.powpow.online/subscription ), silisa problème na côté selon ba règles na `registration-flow.md`, bombaka ton moko, pe silisa na tour nionso na bloc "étape oyo elandi".
https://global.powpow.online/subscription, landa mangonga ya `registration-flow.md` mpo kosunga na ye, voix
echangama te, chaque tour esila na bloc «etape oyo elandi».
