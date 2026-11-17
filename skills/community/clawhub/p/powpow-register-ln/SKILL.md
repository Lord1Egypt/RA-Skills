---
name: powpow-register
description: Esungisaka motaleli mpé kosilisa enregistrement na PowPow (Bubble) pe kokota na clic moko na kati ya masolo. Agent akopisaka formula na esika ya motaleli (na kotya avatar) pe atindaka email ya code de vérification; motaleli abongisi sé kopesa ba informations de base pe komona code de vérification mbala moko — koleka te na masolo. Plateforme lelo ezali na période d'essai gratuit: compte enregistré akoki kosalisa ba fonctionnalités nionso mbala moko; paiement ya abonnement (Alipay/PayPal) ezali amélioration ya membre ya option, oyo agent akoki kosala na création de commande pe suivi ya argent naino soki esengeli. Etambuli tango motaleli alobi "enregistrer na Bubble", "sala compte powpow", "ndenge nini kosala enregistrement na Bubble", "salisa ngai na kosala compte powpow", "sign up powpow"; pe esalisi na ba problèmes ya enregistrement (code de vérification eyaki te, nom ya motaleli/email ezuami déjà) pe ba problèmes ya activation (kokota elobi "compte eactivé te" / pending_payment, ndenge nini kosala abonnement/paiement, Bubble est gratuit to ezali paiement). Esengeli Node ≥ 18; soki ezali te, ezali koleka na mode ya guide pur. Ezali te kobimisa/créer ba humains numériques (mosala ya powpow-simple), ezali te développement ya code.
version: 2.2.0
metadata:
  openclaw:
    emoji: "\U0001F4DD"
    homepage: https://global.powpow.online
---

# PowPow Register (mosalisi ya inscription ya Bule)

Ememaka motaleli ya sika uta "nayebi te Bubble nini" tii "nakoti na clic moko, pronto kosala" — nionso na kati ya masolo. Motaleli atikaka masolo mbala moko sé: **mpo na komona code de vérification na boîte de réception**. Plateforme lelo ezali na période d'essai gratuit: nsima ya enregistrement, ba fonctionnalités nionso ezali, bosenga ya paiement te; paiement ya abonnement ezali amélioration ya membre ya option (agent afungukaka caisse pe alandaka argent naino).

**Version 2.2.0** · 2026-10-18 (kobanda na v2 oyo ezali mode ya aide ya agent: contrat ya script pe ordre mobimba ezali na `references/agent-flow.md`; ba règles ya champ, ba limites ya débit pe diagnostic d'erreur na `references/registration-flow.md`; ba canaux ya paiement na `references/payment-and-activation.md`; liste ya captures d'écran ya produit na `references/screenshots.md`. Kobanda na v2.1.0 abonnement PayPal akoki kosalama na agent, lokola option na côté ya Alipay. Kobanda na v2.2.0 plateforme ekoti na période d'essai gratuit: enregistrer pe kokota na clic moko mpo na kosala mbala moko; paiement ekomi amélioration ya option — soki motaleli abendi lien pe akwei na page d'abonnement, période d'essai esili, landa flux ya paiement uta na étape 7; flux esengeli komibongisa yango moko, bosenga te ya kobongola script)

## Environnement ya kosala

- Script monene `scripts/powpow-register.mjs`: **ezali na dependance te**, esengi **Node >= 18**. Liboso ya kobanda sala mbala moko `node scripts/powpow-register.mjs status` mpo oloka environnement ezali malamu.
- Ba requetes nionso ya script etindaka kaka na domaine officiel `https://global.powpow.online`.
- **Node te / ba erreurs ya script**: koleka automatique na mode ya guide pur — pesa motaleli page d'enregistrement https://global.powpow.online/register pe lakisa ye na côté selon `references/registration-flow.md` (na période d'essai gratuit, enregistrement na web ezali mbala moko rapide). Kobundela script mbala na mbala te.
- Nsima ya lisolola ekatama: libanda `status` yeba mosala ekomami mbala nini, nsima landa.

## Trigger Conditions

- Makano ya inscription: «sala inscription ya Bule», «sala kompte ya powpow», «ndenge ya kosala inscription powpow», «sign up powpow»
- Inscription ekangi: «kodi ya ndingisa ekomi te», «kombo ya mosaleli elobi ezali deja», «password ekosengela te mbala na mbala»
- Ba problèmes nsima ya enregistrement: "kokota elobi compte eactivé te", "403 pending_payment", "ndenge nini kosala paiement/abonnement na Bubble", "Bubble est gratuit to ezali paiement"

**Ezali ko-trigger te**: kotinda post/kosala moto numerique (→ powpow-simple); kosala code ya Web (tala skills ya kosala code). Mosaleli alingi kosala inscription mpe kotinda post: sila liboso mosala ya skill oyo, nsima ya activation pesa powpow-simple.

## Molongo ya mosala

| Etape | Agent asali nini | Mosaleli asali nini |
|---|---|---|
| 1 Presentation ya produit | Solola + tinda lilinzo | Tala |
| 2 Confirmation ya bansongo | Pesa ndingisa kombo ya mosaleli/surnom, password pona mibale, tuna imele | Confirmer, pesa |
| 3 Tinda kodi ya ndingisa | `send-code` | —— |
| 4 Zwa kodi ya ndingisa | —— | Kende na imele komona kodi ya nombo 6, zonga tinda |
| 5 Tinda inscription | `register` (na upload direct ya lilinzo ya profil), kosunga mbeba automatiquement | —— |
| 6 Kokota na clic moko | `login-link(home)` directement na page d'accueil; soki akwei na page d'abonnement, kende na étape 7 | Benda lien pe banda kosala |
| 7 Amélioration d'abonnement (option) | Sé tango motaleli alingi membre / période gratuite esili: flux ya paiement mobimba | Pona méthode, futa |
| 8 Kosila | `cleanup` + pesa carte ya kompte + landa experience + proposer plugins | Ebandi kolala |

## Etape 1: Presentation ya produit + lilinzo (ezali kobwakama te)

Bat mosaleli ebele bazali komona Bule mbala ya liboso. Elikia ya liboso ya lobi ezali te kosolola etape, kasi komonisa ye **produit na miso**:

1. Solola Bule na maloba ~120: lilinzo oyo okangi na mbala moko ekomi post ya voyage, ekangama na mapa ya bato nionso mpe ekomi «bule» moko; bule ekufa na ntango, bato mosusu soki balobi likinga ekoki kozonga na bomoi; na mapa mpe ezali «bato numerique» okoki kosolola na bango. Adresse ya plateforme https://global.powpow.online , soki olingi komona video liboso: https://www.bilibili.com/video/BV1Wu826UEVz/
2. **Tinda lilinzo**. Lilinzo ezali deja na pack ya skill na `assets/screenshots/powpow-0N.jpg` — tinda directement comme fichier ya lilinzo local, esengi internet te. Liste, makambo ya lilinzo moko moko na ntango ya kosalela yango tala `references/screenshots.md`. Combinasi ya liboso oyo esalelamaka mingi: lokasa ya mapa (powpow-03) + lokasa ya detail ya post (powpow-06).

Mangonga ya lilinzo (mangonga makasi):

- Lilinzo **ezali deja na pack** na `assets/screenshots/` (`powpow-0N.jpg`) — tinda directement fichier ya lilinzo local; esalelama na environnement nionso, na mpe environnement oyo GitHub efungwama te.
- Mbala moko tinda kaka lilinzo 1–3 oyo ezali na lien na sujet ya sikoyo, kotinda nionso mbala moko te.
- Soki fichier ya pack ezangi na mabe, zonga na liens ya hosting oyo ezali na liste na `references/screenshots.md` (keba: na Chine ekoki efungwama te).

Nsima ya presentation, pesa mosaleli kozwa decision: **«Soki olingi kosala inscription, na miniti misato tosalaka kompte na kati ya lisolola, ozali besoin ya komona kodi ya ndingisa ya imele mbala moko kaka.»**

## Etape 2: Confirmer bansongo ya inscription (tuna lisolo moko na mbala moko, te nionso mbala moko)

- **Kombo ya mosaleli** (obligatoire): uta contexte ya lisolola/kombo ya mosaleli ya systeme **pesa ndingisa ya moko** (2~50 caracteres, minuscule/MAJUSCULE ekosengela te), mosaleli apanza esalela, alingi kochanger abadila.
- **Password** (obligatoire, liboso tuna mosaleli apone mibale):
  - Mosaleli apesa yango moko moko → nsima etindama na script na variable d'environnement, **jamais ekoma na parametre ya commande**;
  - Agent esali → sala `node scripts/powpow-register.mjs gen-password`, pesa password oyo esalami **mbala moko na mosaleli mpo abomba** (emonana mbala moko kaka, nsima ekomonana lisusu te).
- **Imele** (obligatoire): mosaleli moko apesa — yango nde ancre ya identite ya kompte, **kosala estimation mpo na mosaleli te**.
- **Surnom** (optionnel): pesa ndingisa par default ekokana na kombo ya mosaleli.
- **Lilinzo ya profil** (optionnel): mosaleli apesa chemin ya fichier lilinzo local (<=5MB, te SVG) script etindaka directement; ezali te bwa (plateforme esalelaka logo par default); soki ozali na bokoki ya kosala lilinzo, okoki proposer kosalisa mosaleli asala moko.
- **Nombo ya telephone** (optionnel, nombo ya Chine): par default bwa, mosaleli moko moko alingi kokanga tuna yango.

Nsima ya confirmation okoki sala `prepare-suggest --username U --nickname N --email E` mpo ekoma na fichier ya etat (nsima register esengi kotinda lisusu te).

## Etape 3–4: Kodi ya ndingisa ya imele (sehemu moko kaka oyo esengi kobima na lisolola)

```
node scripts/powpow-register.mjs send-code --email <imele>
```

Nsima loba na mosaleli clairement: **kenda na imele luka kodi ya nombo 6, ezali valide na kati ya miniti 10, keba kotala dossier ya spam/promotion**, ozwa yango zonga tinda na ngai. Kotinda ezali na cooldown secondes 60, beta mbala na mbala te.

## Etape 5: Tinda inscription (agent esalaka)

```
POWPOW_REGISTER_PASSWORD=<password> node scripts/powpow-register.mjs register --code <kodi ya ndingisa> [--username U] [--nickname N] [--avatar <chemin ya fichier lilinzo local>] [--phone P]
```

Succes esali kompte (etat pending, na badges 3 ya ebandeli). Mbeba ya mbala mingi esungama automatiquement, ekatelaka mosaleli te:

| Mbeba | Kosunga |
|---|---|
| 用户名已存在 (kombo ya mosaleli ezali deja) | Pesa ndingisa ya variante automatiquement (kombo ya mosaleli + nombo), mosaleli apanza nsima meka directement lisusu (kodi ya ndingisa naino ezali valide, esengi kotinda lisusu te) |
| 邮箱已被使用 (imele esalelamaka deja) | Tuna mosaleli: abadila imele mosusu, to en fait azali deja na kompte (abadila nzela ya koneksione/kozwa password) |
| 邮箱验证码错误或已过期 (kodi ya ndingisa ya imele mbeba to ekufi) | Eleki miniti 10 → tinda lisusu `send-code` |
| 发送/注册过于频繁（429） (kotinda/inscription mingi mingi (429)) | Zela minute 1 nsima meka lisusu, loba kaka na mosaleli |

## Étape 6: Kokota na clic moko (nsima ya enregistrement directement na page d'accueil)

1. Mbala moko nsima ya enregistrement elongi:
   ```
   node scripts/powpow-register.mjs login-link --target home
   ```
2. Tinda lien na motaleli: **benda pe okozala directement na page d'accueil, okoti déjà**. Plateforme lelo ezali na période d'essai gratuit — nsima ya enregistrement ba fonctionnalités nionso ezali (feed, carte, humains numériques, check-ins, etc.), **bosenga ya paiement te**.
3. Lakesa motaleli andimisa akoti; ba cas mibale ezali:
   - **Akwei na page d'accueil** → kokende directement na étape 8 mpo na kosilisa; enregistrement esili;
   - **Akwei na page d'abonnement** → période d'essai gratuit ya plateforme esili; láta na motaleli "période d'essai gratuit esili, soki membre abonnement esengeli sikoyo", nsima landa étape 7 mpo na kosilisa abonnement, pe nsima ya abonnement zonga na étape 8.
4. Soki motaleli moko alingi amélioration to soutenir plateforme → kokende na étape 7 (abonnement volontaire; kobenda nguya te).
## Étape 7: Amélioration d'abonnement (option — sé tango étape 6 elobi)

1. Liboso tinda lien ya demi-kokota mpo na page ya retour nsima ya paiement emonisa "Paiement elongi" lolenge:
   ```
   node scripts/powpow-register.mjs login-link --target pending
   ```
   Tinda lien na motaleli: benda pe navigateur directement na page d'abonnement, okoti déjà.
2. **Lakesa motaleli apona méthode ya paiement** — monisa ba canaux mibale:
   - **Alipay (Chine continentale / ba utilisateurs na Alipay)**: achat moko ya durée, **auto-renouvellement te**
     - Sanza **¥6.99** (pona essai) / Misato **¥19.99** / Mobu **¥69.99**
   - **PayPal (internasyonal / ba utilisateurs sans Alipay)**: auto-renouvellement sanza na sanza, annuler na ntiná nionso
     - Premium Monthly, penza **$1/sanza** (lokola emonisi na page d'abonnement; na auto-renouvellement)
3. Soki motaleli apona moko:
   - **Alipay**:
     ```
     node scripts/powpow-register.mjs create-order --package monthly
     ```
   - **PayPal**:
     ```
     node scripts/powpow-register.mjs create-order --provider paypal
     ```
   Script azongisi chemin ya fichier ya page ya paiement; **fungula ye directement na commande système** (Windows: `start <fichier>`; macOS: `open <fichier>`; Linux: `xdg-open <fichier>`). Navigateur akende automatique na caisse officiel Alipay/PayPal, epai motaleli asilisaka paiement to autorisation ya facturation.
4. Salisa `query` na 10–15 secondes tii azongisi `paid` to `ACTIVE` (paiement/autorisation ekweaka na ba secondes tii na minute moko). Soki motaleli afongwaki page ya paiement na katikati → sé `create-order` lisusu (ba commandes anciens / abonnements en attente bakofungama to bakosila nsima ya ba heures 2; koyeba te).
5. Canal ya code QR WeChat endimisaka na loboko pe argent akoki koyoka; Huawei IAP ezali sé na kati ya application HarmonyOS. Skill esalaka yango mibale te — nsima ya paiement, motaleli azongi pe alobaka na agent, oyo liboso asalaka `whoami` mpo na koyeba soki argent ekwei, nsima atindaka lien ya page d'accueil selon point 6 oyo ezali awa na se.
6. Nsima ya koyeba soki argent ekwei, bongola état ya kokota na affirmation ya abonnement ya sika, nsima tinda lien directement na page d'accueil:
   ```
   POWPOW_REGISTER_PASSWORD=<mot de passe> node scripts/powpow-register.mjs refresh-login
   node scripts/powpow-register.mjs login-link --target home
   ```
   Tinda lien na motaleli: **benda pe okozala directement na page d'accueil na état ya membre mobimba**.
## Étape 8: Kosilisa

1. `node scripts/powpow-register.mjs cleanup` mpo na kopetola ba fichiers temporaires locaux (identifiants ya session).
2. Pesa motaleli "carte de compte": nom d'utilisateur, email (mot de passe emonanisaka lisusu te — na mode généré motaleli alobelaki kobomba tango egenerami; soki motaleli atieki yango moko, ayebi yango).
3. Lembisi ya membre (loba mbala moko, kobenda nguya te): lelo ezali période d'essai gratuit pe compte esalaka mbala moko; tango période d'essai esili, ba comptes sans abonnement tango bakokota na ba pages ya contenu bakozwa redirection na page d'abonnement — mpo na utilisation ya temps molai, zonga pe sala abonnement na ntiná nionso.
4. Lakisa ba étapes ya liboso: tala carte, publike journal ya voyage ya liboso (→ kopesa na powpow-simple).
5. Recommander ba extensions: skill `@durenzidu/powpow-integration` pe plugin `@durenzidu/openclaw-channel-powpow` — connecter Bubble na agent ya motaleli moko; pesa commande d'installation soki alingi.
6. Silisa na bloc "étape oyo elandi".
## Conversation UX

Salela ndenge moko voix ya service ya PowPow esalaka mbala nionso:

- **Mosaleli nde sujet ya phrase**, «okoki...» ezali malamu koleka «nazali besoin oyo...»; kosala sermon te, etala bato na ntolo te.
- **Mbala moko pesa decision moko kaka**; liboso ya kotuna bansongo, pesa tina liboso.
- **Nsima ya chaque reponse** ezali bloc ya sembo «etape oyo elandi» (ligne ya kofungola + 👉 + action moko + phrase moko «nsima nakosala...»), ndakisa:
  ```
  ────────────────────
  👉 Oyo osengeli kosala sikoyo: kenda na imele luka kodi ya nombo 6, tinda na ngai directement
     (nzoka nakozwa yango, nakosala kompte na yo mbala moko)
  ```
- **Sermon ya securite na password te**; kosolola mecanisme interne, limites to design ya securite, ata mosaleli atuni te.
- Ntango agent esalaka, koloba progres mingi: nsima ya chaque etape script loba na phrase moko oyo esilaki kosalema («kompte esali», «lokasa ya kofuta efungolami deja mpo na yo»).

## Mangonga makasi

- **Securite ya identite**: password etindama na script na variable d'environnement `POWPOW_REGISTER_PASSWORD` kaka, **jamais** ekoma na parametre ya commande (liste ya processus emonana), ekoma na fichier te (mode generation elakisa mbala moko mpo mosaleli abomba, nsima elobi lisusu te). Kodi ya ndingisa esalelaka kaka API officielle ya inscription, esila esalema ebwakama.
- **Ndelo officiel**: ba requetes nionso etindaka kaka `https://global.powpow.online` (script ezali na yango deja), kopesa info ya mosaleli na adresse ya bato ya misato jamais te.
- **Ndelo ya kofuta**: agent esala kaka commande, efungola caisse, etuna mbongo; **jamais** ekanga compte ya Alipay/PayPal ya mosaleli / identite ya kofuta, mpe jamais epromettre «kofuta na esika ya mosaleli».
- **Paywall ezali bug te**: na période d'essai gratuit lelo ba pages ya contenu nionso bazali ouvert; soki motaleli abendi lien ya page d'accueil pe akwei na page d'abonnement — période d'essai esili, lakisa ye asala abonnement na étape 7. Komeka kopikola paywall te, pe koyebisa ba mécanismes internes na motaleli te.
- **Liberte ya retour**: mosaleli na etape nionso alingi kosala moko moko, to environnement esupporte script te, mbala nionso ezonga na mode ya directives kaka — pesa liens, solola mangonga, fata ensemble kotunga mbeba.
- Kosala mangonga ya plateforme te: mangonga ya champs, textes ya mbeba, parametres ya limites nionso ewuti na code ya plateforme (`references/registration-flow.md` ezali na source ya code), mise a jour ya plateforme elandi comportement reel ya ligne.
- Lilinzo ya presentation salela kaka oyo ezali na `assets/screenshots/` ya pack (esalela ya chaque lilinzo tala `references/screenshots.md`).
- Chaque tour esila na bloc «etape oyo elandi», mpo mosaleli ayeba mbala nionso oyo asengeli kosala sikoyo.
