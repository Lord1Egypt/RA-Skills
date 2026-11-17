# Flux de prise en charge par l'agent et contrat du script — powpow-register

Détails d'exécution de chaque étape de SKILL.md. Toutes les commandes sont de la forme `node scripts/powpow-register.mjs <sous-commande> [paramètres]`,
le script est **zéro dépendance** et requiert **Node ≥ 18** ; toutes les requêtes ne partent que vers `https://global.powpow.online`.

## Conception sécurité (pourquoi c'est conçu ainsi)

| Conception | Raison |
|---|---|
| Le mot de passe ne passe que par la variable d'environnement `POWPOW_REGISTER_PASSWORD` | Les arguments de ligne de commande d'un processus sont visibles des autres processus de la même machine (surface de fuite argv) ; la variable d'environnement est lue dans le script et utilisée immédiatement |
| Le mot de passe n'est **jamais écrit dans le fichier d'état**, n'apparaît jamais dans les logs | Le fichier d'état peut rester sur le disque ; en mode génération, on ne l'affiche qu'une fois pour que l'utilisateur le sauvegarde |
| Le fichier d'état est dans le répertoire temporaire système (`os.tmpdir()/powpow-register-state.json`, 0600) | Il ne contient que les cinq champs email / username / nickname / token / outTradeNo ; `cleanup` l'efface d'un coup |
| Le JWT reçu par l'agent est échangé contre un cookie de navigateur via l'endpoint officiel `me?token=` | C'est le pont officiel conçu par la plateforme pour le WebView HarmonyOS ; la vérification ne contrôle que signature + validité, sans attache à l'empreinte de l'appareil, donc le navigateur de l'utilisateur convient |
| Le paiement ne fait que create-order / query / ouvrir la caisse | L'acte de payer et les moyens de paiement restent toujours entre l'utilisateur et la caisse officielle Alipay ; l'agent ne les manipule pas |

## Référence des commandes

| Commande | Paramètres clés | Rôle / quand |
|---|---|---|
| `status` | —— | Voir la progression du flux (lit le fichier d'état) ; après une interruption de conversation, lance d'abord ceci |
| `gen-password` | —— | Génère un mot de passe fort de 24 caractères (majuscules + minuscules + chiffres) ; stdout l'affiche **une seule fois** |
| `prepare-suggest` | `--username --nickname --email` | Note dans le fichier d'état les informations confirmées (ensuite register n'a plus à les redemander) |
| `send-code` | `--email` | Déclenche l'envoi par la plateforme du code de vérification à 6 chiffres (valable 10 minutes, refroidissement 60s) |
| `register` | `--code` (obligatoire) ; `--username --nickname --avatar --phone` (optionnels, omis s'ils sont déjà dans le fichier d'état) | Crée le compte pending ; le mot de passe passe par la variable d'environnement `POWPOW_REGISTER_PASSWORD` ; en cas de succès, le JWT est automatiquement stocké dans le fichier d'état |
| `login-link` | `--target pending` ou `--target home` | Génère un lien de connexion en un clic (conception à double lien, voir plus bas) |
| `create-order` | `--package monthly\|quarterly\|yearly` (Alipay par défaut)<br>`--provider alipay\|paypal` | Crée la commande de paiement ; Alipay renvoie le chemin du fichier de la page de paiement + outTradeNo ; PayPal renvoie le chemin du fichier de la page d'autorisation + subscriptionId (noté automatiquement dans le fichier d'état) |
| `query` | —— | Consulte l'état de la commande / de l'abonnement. Alipay : `paid / pending / closed / unknown` ; PayPal : `ACTIVE / PENDING` ; interrogation toutes les 10–15s |
| `refresh-login` | Mot de passe par variable d'environnement | Reconnexion pour un **JWT neuf** (la déclaration d'abonnement passe de NONE à ACTIVE) ; obligatoire après encaissement |
| `whoami` | —— | Consulte avec le token du fichier d'état l'état du compte et de l'abonnement (vérifier si l'activation a pris effet) |
| `cleanup` | —— | Supprime le fichier d'état (obligatoire à la clôture) |

**Passage de la variable d'environnement** (le mot de passe ne va jamais sur la ligne de commande) :

```bash
# bash / zsh / WSL
POWPOW_REGISTER_PASSWORD='<mot de passe>' node scripts/powpow-register.mjs register --code 123456
# PowerShell
$env:POWPOW_REGISTER_PASSWORD = '<mot de passe>'; node scripts/powpow-register.mjs register --code 123456
# cmd
set POWPOW_REGISTER_PASSWORD=<mot de passe> && node scripts/powpow-register.mjs register --code 123456
```

## Mécanisme à double lien (conception centrale)

L'état de session de la plateforme est un cookie HttpOnly, que l'agent ne peut pas planter directement dans le navigateur ; le pont est l'endpoint officiel
`/api/auth/me?token=<JWT>&redirect=<chemin interne>` : vérifier la signature → créer la session automatiquement
→ `Set-Cookie: powpow_token` (HttpOnly / SameSite=Lax / 7 jours) → valider
la redirection (doit commencer par une seule barre, `//` et barres obliques inverses interdits, même origine après analyse) → 307 redirection temporaire vers la page cible.

Il y a deux cibles de lien, **génère d'abord home, puis décide s'il faut passer par pending selon où atterrit l'utilisateur** :

- **lien home (envoyé par défaut en premier, `--target home` → atterrit sur `/`)** : généré et envoyé à l'utilisateur immédiatement après l'inscription réussie.
  Pendant la période d'essai gratuit, l'utilisateur entre directement sur la page d'accueil, tout est utilisable ; **si l'utilisateur l'ouvre mais atterrit sur la page d'abonnement, la période d'essai gratuit est terminée** — bascule alors sur le chemin de paiement (voir plus bas) ; aucun changement de script ni réinscription nécessaire.
- **lien pending (utilisé dans le chemin de paiement, `--target pending` → atterrit sur `/subscription`)** :
  le navigateur de l'utilisateur entre en état de « demi-connexion » : la page d'abonnement et la page de retour du paiement sont visibles et utilisables. Après l'encaissement,
  lance `refresh-login` pour échanger contre un nouveau JWT portant la déclaration ACTIVE, puis renvoie le lien home une fois de plus pour l'adhésion complète.

## Séquence complète

### Chemin rapide (pendant la période d'essai gratuit — la grande majorité des cas)

```
1.  status                          # auto-vérification de l'environnement
2.  (étape 2 conversation pour confirmer les infos, mot de passe au choix ; mode généré : gen-password → faire sauvegarder immédiatement par l'utilisateur)
3.  prepare-suggest --username U --nickname N --email E
4.  send-code --email E             # → l'utilisateur consulte le code dans sa boîte mail (seule sortie de la conversation)
5.  POWPOW_REGISTER_PASSWORD=*** register --code 123456 [--avatar pic.jpg]
6.  login-link --target home        # → envoie le lien à l'utilisateur ; un clic et il est sur la page d'accueil
7.  (l'utilisateur confirme qu'il est entré) → conclus directement : cleanup + fiche de compte + guide des premiers pas
```

### Chemin de paiement (quand l'utilisateur veut l'adhésion, ou que la période d'essai gratuit est terminée)

```
1–5. Identique au chemin rapide (le state contient déjà le token après un register réussi)
6.  login-link --target pending     # → lien de demi-connexion, garde la page de retour du paiement fonctionnelle
7.  (l'utilisateur choisit le moyen de paiement)
    # Alipay : create-order --package monthly|quarterly|yearly
    # PayPal : create-order --provider paypal
8.  start <fichier de page de paiement>   # Windows ; macOS utilise open, Linux utilise xdg-open
    # → l'utilisateur finalise le paiement/l'autorisation à la caisse Alipay/PayPal (sort de la conversation)
9.  query (toutes les 10–15 s) jusqu'à paid / ACTIVE
10. refresh-login                   # échange contre un nouveau JWT portant la déclaration ACTIVE
11. login-link --target home        # → envoie le lien d'adhésion complète à l'utilisateur
12. whoami                          # confirme subscriptionStatus: ACTIVE (facultatif)
13. cleanup                         # nettoie le fichier d'état
```
## Correspondance commande → API de la plateforme

| Commande du script | Interface de la plateforme |
|---|---|
| `send-code` | `POST /api/auth/register/send-code` |
| `register` | `POST /api/auth/register` (multipart, upload direct de l'avatar) |
| `login-link` | `GET /api/auth/me?token=…&redirect=…` (le lien lui-même, prend effet au clic dans le navigateur) |
| `create-order` | `POST /api/payment/alipay/create-order` (Bearer, Alipay)<br>`GET /api/subscription/plans` + `POST /api/subscription/create` (Bearer, PayPal) |
| `query` | `GET /api/payment/alipay/query?outTradeNo=…` (Bearer, Alipay)<br>`GET /api/subscription/create` (Bearer, PayPal) |
| `refresh-login` | `POST /api/auth/login` (`{step:1, username, password}`) |
| `whoami` | `GET /api/auth/me?token=…` |

Source des règles : champs d'inscription et limites de fréquence dans `registration-flow.md` ; formules et
chaîne d'activation dans `payment-and-activation.md` (les deux citent les fichiers du code source de la
plateforme).

## Gestion des erreurs au niveau du script

| Symptôme | Gestion |
|---|---|
| `Version de Node trop basse` | Repli en mode guide pure, ne force pas |
| Erreur réseau / timeout | Réessaie une fois ; si ça échoue encore, l'utilisateur vérifie son réseau puis on continue (le fichier d'état est toujours là ; relance `status` depuis le début pour reprendre) |
| register renvoie une erreur métier (nom d'utilisateur déjà existant, etc.) | Traite selon le tableau de l'étape 5 de SKILL.md, **pas besoin de renvoyer le code de vérification** (encore valable pendant 10 minutes) |
| register renvoie 「邮箱验证码错误或已过期」 (code de vérification erroné ou expiré) | Délai dépassé → relancer `send-code` |
| L'utilisateur a fermé la page de paiement après `create-order` | Relance directement `create-order` (l'ancienne commande se ferme seule au bout de 2h ; les abonnements PENDING PayPal expirent au bout de 1h) |
| `create-order --provider paypal` renvoie 409 | Il existe déjà un abonnement PayPal non finalisé ; attends 1h qu'il expire, ou finalise l'ancienne autorisation dans le navigateur |
| `query` reste en pending / PENDING | L'utilisateur n'a peut-être pas payé ; pose la question. S'il a vraiment payé → suis le tableau de diagnostic de payment-and-activation.md |
| L'utilisateur ouvre le lien home mais atterrit sur la page d'abonnement | La période d'essai gratuit est terminée → bascule sur le chemin de paiement : `login-link --target pending` → choisis un moyen de paiement → `create-order` |
| `refresh-login` 403 `pending_payment` | La période d'essai gratuit est terminée et le paiement n'est pas encore arrivé ; retourne à l'étape 9 pour continuer à sonder, ou confirme si l'utilisateur a finalisé le paiement |
| Fichier d'état perdu (supprimé par erreur / changement de machine) | `whoami`/`refresh-login` inutilisables ; l'utilisateur actualise directement la page d'abonnement dans le navigateur où il a ouvert le lien 1 pour vérifier l'état, ou se reconnecte (mode Web) |

## Mode de repli (guide pure)

Dans l'un quelconque de ces cas, repasse immédiatement au guide pure façon v1, sans continuer à batailler avec le script :

- Pas de Node ≥ 18, ou le script échoue deux fois de suite sur le même point ;
- L'utilisateur dit clairement « je le fais moi-même sur le Web » ;
- Les politiques de l'entreprise / de l'appareil restreignent les scripts réseau.

Après repli : donne la page d'inscription https://global.powpow.online/register (pendant la période d'essai gratuit, l'inscription web est tout aussi immédiate ; quand un abonnement est nécessaire, donne aussi la page d'abonnement https://global.powpow.online/subscription ), accompagne le dépannage selon les règles de `registration-flow.md`, garde le même ton et termine chaque tour par un bloc « prochaine étape ».
https://global.powpow.online/subscription, accompagne le dépannage selon les règles de
`registration-flow.md`, garde le même ton, et termine chaque tour par le bloc « prochaine étape ».
