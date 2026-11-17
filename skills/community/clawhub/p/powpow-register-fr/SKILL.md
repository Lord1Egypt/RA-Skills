---
name: powpow-register
description: Aide les utilisateurs à terminer l'inscription à PowPow (Bulle) et la connexion en un clic, entièrement dans la conversation. L'agent remplit le formulaire à leur place (y compris le téléversement de l'avatar) et envoie le code de vérification par e-mail ; l'utilisateur ne fournit que les informations de base et consulte le code une fois, sans quitter la conversation. Pendant la période actuelle d'essai gratuit de la plateforme, un compte inscrit peut utiliser toutes les fonctions immédiatement ; le paiement de l'abonnement (Alipay/PayPal) est une amélioration d'adhésion facultative, que l'agent peut aussi prendre en charge avec création de commande et suivi de l'encaissement si besoin. Se déclenche quand l'utilisateur dit « s'inscrire à Bulle », « créer un compte powpow », « comment s'inscrire à Bulle », « aide-moi à créer un compte powpow », « sign up powpow » ; gère aussi les blocages d'inscription (code de vérification non reçu, nom d'utilisateur/e-mail déjà pris) et les problèmes d'activation (la connexion dit « compte non activé » / pending_payment, comment s'abonner/payer, Bulle est-ce gratuit ?). Nécessite Node ≥ 18 ; replie automatiquement en mode guidage pur si indisponible. Ne couvre pas la publication/la création d'humains numériques (c'est le domaine de powpow-simple), ni le développement code.
version: 2.2.0
metadata:
  openclaw:
    emoji: "\U0001F4DD"
    homepage: https://global.powpow.online
---

# PowPow Register (assistant d'inscription à Bulle)

Emmène un nouvel utilisateur de « je ne sais pas ce qu'est Bulle » à « connexion en un clic, prêt à jouer » — entièrement dans la conversation. L'utilisateur ne quitte la conversation qu'une seule fois : **pour consulter le code de vérification dans sa boîte mail**. La plateforme est actuellement en période d'essai gratuit : une fois inscrit, toutes les fonctions sont utilisables, aucun paiement requis ; le paiement de l'abonnement est une amélioration d'adhésion facultative (l'agent ouvre aussi la caisse et suit l'encaissement).

**Version 2.2.0** · 2026-10-18 (depuis la v2, mode assisté par agent : contrat du script et séquence complète dans `references/agent-flow.md` ; règles de champs, limites de débit et dépannage des erreurs dans `references/registration-flow.md` ; canaux de paiement dans `references/payment-and-activation.md` ; liste des captures produit dans `references/screenshots.md`. Depuis la v2.1.0, les abonnements PayPal peuvent aussi être gérés par l'agent, en option aux côtés d'Alipay. Depuis la v2.2.0, la plateforme entre en période d'essai gratuit : inscris-toi et connecte-toi en un clic pour commencer ; le paiement devient une amélioration facultative — si l'utilisateur ouvre le lien et atterrit sur la page d'abonnement, la période d'essai est terminée, suis alors le flux de paiement de l'étape 7 ; le flux s'adapte tout seul, aucune modification du script)

## Environnement d'exécution

- Script principal `scripts/powpow-register.mjs` : **zéro dépendance**, requiert **Node ≥ 18**. Avant de commencer, lance une fois `node scripts/powpow-register.mjs status` pour vérifier que l'environnement fonctionne.
- Toutes les requêtes du script ne partent que vers le domaine officiel `https://global.powpow.online`.
- **Pas de Node / erreurs du script** : replie automatiquement en mode guidage pur — donne à l'utilisateur la page d'inscription https://global.powpow.online/register et accompagne-le selon `references/registration-flow.md` (pendant la période d'essai gratuit, l'inscription web est tout aussi immédiate). N'insiste pas avec le script.
- Reprise après une interruption de conversation : lance d'abord `status` pour voir où en est le flux, puis continue.

## Trigger Conditions

- Intention d'inscription : « m'inscrire sur Bulle », « créer un compte powpow », « comment s'inscrire sur Bulle », « sign up powpow »
- Inscription bloquée : « je ne reçois pas le code de vérification », « il dit que le nom d'utilisateur existe déjà », « mon mot de passe ne passe jamais la validation »
- Problèmes après inscription : « la connexion dit que le compte n'est pas activé », « 403 pending_payment », « comment payer/s'abonner à Bulle », « Bulle c'est gratuit ou payant ? »

**Ne se déclenche pas pour** : publier des posts / créer des humains numériques (→ powpow-simple) ; le développement de code côté Web (voir les compétences de développement). Si l'utilisateur veut à la fois s'inscrire et publier : termine d'abord cette compétence, puis après activation, passe-le à powpow-simple.

## Vue d'ensemble du flux

| Étape | Ce que fait l'agent | Ce que fait l'utilisateur |
|---|---|---|
| 1 Présentation du produit | Présente + envoie des captures | Jette un œil |
| 2 Confirmation des infos | Propose proactivement nom d'utilisateur/pseudo, mot de passe au choix entre deux options, demande l'e-mail | Confirme, fournit |
| 3 Envoi du code | `send-code` | —— |
| 4 Lecture du code | —— | Va dans sa boîte mail, relève le code à 6 chiffres, le renvoie |
| 5 Envoi de l'inscription | `register` (upload direct de l'avatar inclus), gère les erreurs automatiquement | —— |
| 6 Connexion en un clic | `login-link(home)` directement sur la page d'accueil ; si ça atterrit sur la page d'abonnement, passe à l'étape 7 | Clique le lien et commence à jouer |
| 7 Amélioration d'abonnement (facultative) | Seulement si l'utilisateur veut l'adhésion / la période gratuite est terminée : flux de paiement complet géré | Choisis un moyen, paie |
| 8 Clôture | `cleanup` + remise des identifiants + guide de prise en main + recommandation de plugins | Commence à jouer |

## Étape 1 : présentation du produit + captures (à ne pas sauter)

La plupart des utilisateurs n'ont jamais vu Bulle. La première chose n'est pas d'expliquer le flux, mais de lui faire **voir** le produit :

1. Présente Bulle en ~120 caractères : transforme les photos prises à la volée en un journal de voyage, épinglé sur la carte publique comme une « bulle » ; les bulles perdent de l'actualité avec le temps et les « j'aime » des autres peuvent les ressusciter ; sur la carte, il y a aussi des « humains numériques » avec qui discuter. Adresse de la plateforme : https://global.powpow.online ; pour voir d'abord une vidéo : https://www.bilibili.com/video/BV1Wu826UEVz/
2. **Envoie des captures**. Les captures sont déjà embarquées avec la compétence dans `assets/screenshots/powpow-0N.jpg` — envoie-les directement comme fichiers image locaux, sans connexion requise. L'inventaire, le contenu de chaque image et le moment de les utiliser sont dans `references/screenshots.md`. La combinaison la plus courante à l'ouverture : page de la carte (powpow-03) + page de détail d'un post (powpow-06).

Règles sur les captures (règles strictes) :

- Les captures sont **déjà embarquées avec la compétence** dans `assets/screenshots/` (`powpow-0N.jpg`) — envoie-les directement comme fichiers image locaux ; utilisables dans n'importe quel environnement, y compris ceux où GitHub ne s'ouvre pas.
- N'envoie que 1–3 images en rapport avec le sujet du moment, ne colle pas tout d'un coup.
- Si des fichiers du paquet manquent par accident, replie-toi sur les liens hébergés listés dans `references/screenshots.md` (attention : peuvent ne pas s'ouvrir depuis la Chine continentale).

Après la présentation, laisse le choix à l'utilisateur : **« Si tu veux t'inscrire, en trois minutes on crée le compte ici dans la conversation ; tu n'auras qu'à aller regarder une fois le code envoyé dans ta boîte mail. »**

## Étape 2 : confirmer les informations d'inscription (une question par tour, pas tout d'un coup)

- **Nom d'utilisateur** (obligatoire) : **propose proactivement** à partir du contexte de la conversation ou du nom d'utilisateur système (2~50 caractères, insensible à la casse) ; si l'utilisateur acquiesce, on le prend ; s'il veut changer, on change.
- **Mot de passe** (obligatoire ; propose d'abord deux options) :
  - L'utilisateur le fournit → ensuite il est passé au script par variable d'environnement, **jamais en argument de ligne de commande** ;
  - L'agent le génère → lance `node scripts/powpow-register.mjs gen-password` et **envoie immédiatement le mot de passe généré à l'utilisateur pour qu'il le sauvegarde** (affiché une seule fois, puis n'apparaît plus).
- **E-mail** (obligatoire) : doit être fourni par l'utilisateur — c'est l'ancre d'identité du compte, **ne le devine pas à sa place**.
- **Pseudo** (optionnel) : propose par défaut de le laisser identique au nom d'utilisateur.
- **Avatar** (optionnel) : si l'utilisateur donne le chemin d'une image locale (≤5 Mo, pas de SVG), le script l'uploade directement ; sinon on passe (la plateforme met le logo par défaut) ; si tu as une capacité de génération d'images, tu peux proposer d'en créer une pour lui.
- **Téléphone** (optionnel, numéro de Chine continentale) : on passe par défaut ; demande-le seulement si l'utilisateur veut le lier.

Une fois confirmé, tu peux lancer `prepare-suggest --username U --nickname N --email E` pour le noter dans le fichier d'état (ainsi register n'aura pas à redemander).

## Étapes 3–4 : code de vérification par e-mail (le seul moment où il faut quitter la conversation)

```
node scripts/powpow-register.mjs send-code --email <e-mail>
```

Puis dis clairement à l'utilisateur : **va chercher dans ta boîte mail le code de vérification à 6 chiffres, valable 10 minutes ; pense aussi à regarder le dossier spam / courriers publicitaires** ; quand il l'a trouvé, qu'il revienne te l'envoyer. L'envoi a un délai de refroidissement de 60 secondes, ne martèle pas.

## Étape 5 : envoyer l'inscription (prise en charge par l'agent)

```
POWPOW_REGISTER_PASSWORD=<mot de passe> node scripts/powpow-register.mjs register --code <code> [--username U] [--nickname N] [--avatar <chemin d'image locale>] [--phone P]
```

En cas de succès, le compte est créé (statut pending, avec 3 badges initiaux). Les erreurs courantes sont gérées automatiquement, sans interrompre l'utilisateur :

| Erreur | Gestion |
|---|---|
| 「用户名已存在」 (le nom d'utilisateur existe déjà) | Propose automatiquement une variante (nom d'utilisateur + chiffres) et, une fois confirmée par l'utilisateur, réessaie directement (le code reste valide, pas besoin de le renvoyer) |
| 「邮箱已被使用」 (l'e-mail est déjà utilisé) | Demande à l'utilisateur : changer d'e-mail, ou en fait il a déjà un compte ? (bascule vers connexion / mot de passe oublié) |
| 「邮箱验证码错误或已过期」 (code de vérification erroné ou expiré) | Plus de 10 minutes écoulées → relancer `send-code` |
| Envoi/inscription trop fréquents (429) | Attends 1 minute et réessaie ; il suffit d'en avertir l'utilisateur |

## Étape 6 : Connexion en un clic (directement sur la page d'accueil après l'inscription)

1. Juste après l'inscription réussie :
   ```
   node scripts/powpow-register.mjs login-link --target home
   ```
2. Envoie le lien à l'utilisateur : **ouvre-le et tu atterris directement sur la page d'accueil, déjà connecté**. La plateforme est actuellement en période d'essai gratuit — après l'inscription, toutes les fonctions sont utilisables (fil, carte, humains numériques, check-ins, etc.), **aucun paiement requis**.
3. Demande à l'utilisateur de confirmer qu'il est bien entré ; il y a deux cas :
   - **Arrivé sur la page d'accueil** → passe directement à l'étape 8 pour conclure ; l'inscription est terminée ;
   - **Arrivé sur la page d'abonnement** → la période d'essai gratuit de la plateforme est terminée ; dis à l'utilisateur « la période d'essai gratuite est terminée, un abonnement d'adhésion est désormais requis », puis suis l'étape 7 pour finaliser l'abonnement, et reviens à l'étape 8 après.
4. Si l'utilisateur veut activement améliorer ou soutenir la plateforme → passe aussi à l'étape 7 (s'abonner est volontaire ; ne pousse pas).
## Étape 7 : Amélioration d'abonnement (facultative — seulement quand l'étape 6 l'exige)

1. Envoie d'abord le lien de demi-connexion pour que la page de retour du paiement affiche correctement « Paiement réussi » :
   ```
   node scripts/powpow-register.mjs login-link --target pending
   ```
   Envoie le lien à l'utilisateur : en l'ouvrant, le navigateur atterrit directement sur la page d'abonnement, déjà connecté.
2. **Laisse l'utilisateur choisir le moyen de paiement** — montre les deux canaux :
   - **Alipay (Chine continentale / utilisateurs avec Alipay)** : achat unique de la durée correspondante, **pas de renouvellement automatique**
     - Mensuel **6,99 ¥** (recommandé pour essayer) / Trimestriel **19,99 ¥** / Annuel **69,99 ¥**
   - **PayPal (outre-mer / utilisateurs sans Alipay)** : renouvellement mensuel automatique, annulable à tout moment
     - Premium Monthly, environ **1 $/mois** (selon l'affichage de la page d'abonnement ; renouvellement automatique)
3. Une fois le choix fait :
   - **Alipay** :
     ```
     node scripts/powpow-register.mjs create-order --package monthly
     ```
   - **PayPal** :
     ```
     node scripts/powpow-register.mjs create-order --provider paypal
     ```
   Le script renvoie le chemin du fichier de la page de paiement ; **ouvre-le directement avec une commande système** (Windows : `start <fichier>` ; macOS : `open <fichier>` ; Linux : `xdg-open <fichier>`). Le navigateur saute automatiquement à la caisse officielle Alipay/PayPal, où l'utilisateur finalise le paiement ou l'autorisation de facturation.
4. Lance `query` toutes les 10–15 secondes jusqu'à obtenir `paid` ou `ACTIVE` (l'encaissement/l'autorisation arrive généralement en quelques secondes à une minute). Si l'utilisateur ferme la page de paiement en cours de route → relance directement `create-order` (les anciennes commandes / abonnements en attente se ferment ou expirent automatiquement après 2 heures ; ignore-les).
5. Le canal code QR WeChat est confirmé manuellement et l'encaissement peut tarder ; Huawei IAP n'est disponible que dans l'app HarmonyOS. Le skill ne gère pas ces deux canaux — après avoir payé, l'utilisateur revient le dire, et l'agent lance d'abord `whoami` pour confirmer l'encaissement, puis envoie le lien vers la page d'accueil du point 6 ci-dessous.
6. Après confirmation de l'encaissement, échange contre un état de session avec la déclaration d'abonnement la plus récente, puis envoie le lien direct vers la page d'accueil :
   ```
   POWPOW_REGISTER_PASSWORD=<mot de passe> node scripts/powpow-register.mjs refresh-login
   node scripts/powpow-register.mjs login-link --target home
   ```
   Envoie le lien à l'utilisateur : **ouvre-le et tu atterris directement sur la page d'accueil avec l'adhésion complète**.
## Étape 8 : Conclusion

1. `node scripts/powpow-register.mjs cleanup` pour nettoyer les fichiers d'état temporaires locaux (identifiants de session).
2. Donne à l'utilisateur une « fiche de compte » : nom d'utilisateur, e-mail (le mot de passe n'est pas réaffiché — en mode généré, l'utilisateur a déjà été invité à le sauvegarder à la génération ; s'il l'a choisi lui-même, il le connaît).
3. Rappel d'adhésion (dis-le une fois, ne pousse pas) : actuellement c'est une période d'essai gratuit et le compte est utilisable immédiatement ; quand la période d'essai se terminera, les comptes non abonnés visitant les pages de contenu seront redirigés vers la page d'abonnement — pour un usage prolongé, reviens demander à l'agent de t'abonner quand tu veux.
4. Guide les premiers pas : parcourir la carte, publier le premier carnet de voyage (→ passe à powpow-simple).
5. Recommande des extensions : le skill `@durenzidu/powpow-integration` et le plugin `@durenzidu/openclaw-channel-powpow` — connecte Bulle à l'agent de l'utilisateur ; donne la commande d'installation s'il le souhaite.
6. Termine par un bloc « prochaine étape ».
## Conversation UX

Garde le ton de service habituel de powpow :

- **L'utilisateur est le sujet de la phrase** ; « tu peux… » vaut mieux que « j'ai besoin que tu… » ; pas de sermon, pas de ton condescendant.
- **Chaque tour ne fait avancer qu'une seule décision** ; avant de demander une information, donne la raison.
- **À la fin de chaque réponse**, un bloc fixe « prochaine étape » (séparateur + 👉 + une seule action + une phrase « quand ce sera fait, je… »), par exemple :
  ```
   ────────────────────
   👉 À toi maintenant : va chercher dans ta boîte mail le code à 6 chiffres et envoie-le-moi directement
      (dès que je le reçois, je crée le compte)
  ```
- **Pas de sermon de sécurité spontané sur le mot de passe** ; n'explique pas les mécanismes internes, les limites de fréquence ou la conception sécurité, sauf si l'utilisateur demande.
- Quand l'agent prend les choses en charge, rends compte encore plus de la progression : après chaque étape de script, dis en une phrase ce qui vient de se passer (« le compte est créé », « je t'ai ouvert la page de paiement »).

## Règles strictes

- **Sécurité des identifiants** : le mot de passe n'est passé au script que par la variable d'environnement `POWPOW_REGISTER_PASSWORD`, **jamais** en argument de ligne de commande (visible dans la liste des processus), ni écrit dans un quelconque fichier (en mode génération, il est affiché une fois pour que l'utilisateur le sauvegarde, puis n'est plus répété). Le code de vérification ne sert que pour l'interface officielle d'inscription et est jeté après usage.
- **Frontière officielle** : toutes les requêtes ne partent que vers `https://global.powpow.online` (déjà intégré dans le script) ; n'envoie jamais les informations de l'utilisateur vers une adresse tierce.
- **Frontière de paiement** : l'agent ne fait que créer la commande, ouvrir la caisse et consulter l'encaissement ; il ne touche **jamais** au compte Alipay/PayPal de l'utilisateur ni à ses moyens de paiement, et ne promet jamais de « payer à sa place ».
- **Le mur de paiement n'est pas un bug** : pendant la période d'essai gratuit actuelle, toutes les pages de contenu sont ouvertes ; si l'utilisateur ouvre le lien vers la page d'accueil mais atterrit sur la page d'abonnement, la période d'essai est terminée — guide-le vers l'abonnement via l'étape 7. N'essaie pas de contourner le mur de paiement et n'explique pas les mécanismes internes à l'utilisateur.
- **Liberté de repli** : si à n'importe quelle étape l'utilisateur veut faire lui-même, ou si l'environnement ne supporte pas le script, retrograde à tout moment en mode guide pure — donne les liens, explique les règles, accompagne le dépannage.
- N'invente pas de règles de la plateforme : les règles de champs, les messages d'erreur et les paramètres de limitation viennent tous du code de la plateforme (`references/registration-flow.md` cite les sources) ; si la plateforme se met à jour, le comportement réel prime.
- Pour montrer des images, n'utilise que les captures embarquées dans `assets/screenshots/` (l'usage de chacune est dans `references/screenshots.md`).
- Termine chaque tour par le bloc « prochaine étape », pour que l'utilisateur sache toujours ce qu'il a à faire maintenant.
