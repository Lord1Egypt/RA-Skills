# powpow-register

Assistant d'inscription à PowPow Bulle (édition OpenClaw) : accompagne un nouvel utilisateur depuis « je ne
sais pas ce qu'est Bulle » jusqu'à « compte activé, connecté en un clic, on joue » — présentation du produit
(captures d'écran comprises), inscription déléguée à l'agent (upload de l'avatar compris), commande
d'abonnement Alipay/PayPal et suivi de l'encaissement, connexion en un clic à double lien, diagnostic des erreurs.

**Depuis la v2.0.0, mode assisté par agent, et depuis la v2.2.0, adaptation à la période d'essai gratuit de la plateforme** : le script cœur `scripts/powpow-register.mjs` est à zéro dépendance
(Node ≥ 18) ; l'utilisateur ne quitte la conversation qu'une seule fois : pour consulter le code de vérification dans sa boîte mail. Pendant la période d'essai gratuit actuelle, un compte inscrit peut utiliser toutes les fonctions immédiatement — le paiement de l'abonnement est une amélioration facultative ; si la période d'essai se termine et que l'utilisateur atterrit sur la page d'abonnement, le flux bascule automatiquement sur le chemin de paiement. Sans Node, ou quand l'utilisateur préfère faire lui-même, repli automatique en mode guidage pur.

## Installation

```
openclaw skills install @durenzidu/powpow-register
```

## Fonctionnalités

1. **Présentation du produit** : ouverture en ~120 caractères + captures d'écran embarquées dans le paquet
   (`assets/screenshots/`, 6 images : page de la carte, page de détail d'un post, etc. ; choisir 1–3 images
   selon la scène ; sans hébergeur externe, utilisable hors ligne).
2. **Inscription déléguée** : l'agent propose proactivement nom d'utilisateur/pseudo, mot de passe au choix
   (fourni par l'utilisateur ou généré par l'agent), envoi et soumission du code de vérification, upload
   direct de l'avatar (≤5 Mo, pas de SVG), gestion automatique des erreurs courantes (déjà pris / expiré / limite de fréquence).
3. **Connexion en un clic (double lien)** : juste après l'inscription réussie, un lien de connexion fait atterrir l'utilisateur directement sur la page d'accueil (pendant la période d'essai gratuit, un clic et c'est utilisable) ;
   si ça atterrit sur la page d'abonnement (période d'essai terminée) ou que l'utilisateur veut améliorer, suis le flux d'abonnement — après l'encaissement, échange contre un nouvel état de session et le lien d'adhésion complète le ramène à la page d'accueil
   (via le pont officiel `me?token=` de la plateforme, qui plante le cookie HttpOnly automatiquement).
4. **Paiement de l'abonnement** : Alipay (mensuel ¥6.99 / trimestriel
   ¥19.99 / annuel ¥69.99, achat unique sans renouvellement automatique) comme PayPal (Premium Monthly, environ $1/mois, renouvellement automatique, annulable à tout moment) sont gérés par l'agent : commande + interrogation en boucle jusqu'à
   l'encaissement ; QR code WeChat / Huawei IAP : on montre le chemin.
5. **Diagnostic des erreurs** : code de vérification non reçu, nom d'utilisateur/e-mail déjà pris, 403 non
   activé, compte verrouillé, etc. — tout vient du code source de la plateforme, sources citées.

## Structure des fichiers

```
powpow-register/
├── SKILL.md                            # Guide principal (conditions de déclenchement, flux en 8 étapes, ton, règles strictes)
├── README.md
├── .clawhubignore
├── assets/
│   └── screenshots/                    # Captures produit embarquées (powpow-01~06.jpg)
├── scripts/
│   └── powpow-register.mjs             # Script principal (zéro dépendance Node≥18, 11 sous-commandes)
└── references/
    ├── agent-flow.md                   # Contrat du script, séquence complète, mécanisme du double lien, conception sécurité
    ├── registration-flow.md            # Règles de champs, limites de fréquence, tableau de diagnostic (sources citées)
    ├── payment-and-activation.md       # Contrat Alipay vibepay, chaîne d'activation, diagnostic des canaux
    └── screenshots.md                  # Inventaire des captures embarquées + consultation rapide par scène
```

## Sécurité

- **Mot de passe** : passé au processus du script uniquement par variable d'environnement, jamais en
  argument de ligne de commande, jamais écrit sur disque, jamais dans le fichier d'état ; le mot de passe
  généré par l'agent n'est affiché qu'une fois, pour que l'utilisateur le sauvegarde.
- **Code de vérification** : utilisé uniquement pour l'interface officielle d'inscription, jeté après
  usage ; le fichier d'état (e-mail/nom d'utilisateur/token/numéro de commande) est stocké dans le
  répertoire temporaire système, effacé d'un coup par `cleanup` en fin de flux.
- **Paiement** : l'agent ne fait que créer la commande, ouvrir la caisse et consulter l'encaissement ; il
  ne touche jamais au compte Alipay/PayPal de l'utilisateur ni à ses moyens de paiement, et ne paie jamais à sa
  place. Le paiement se fait toujours entre l'utilisateur et la caisse officielle.
- Toutes les requêtes ne partent que vers le domaine officiel `https://global.powpow.online` ; aucune clé n'est incluse.

## Licence

MIT-0 (licence unifiée ClawHub).

## Liens

- Site officiel : https://global.powpow.online
- Inscription : https://global.powpow.online/register
- Découvrir Bulle (vidéo) : https://www.bilibili.com/video/BV1Wu826UEVz/
