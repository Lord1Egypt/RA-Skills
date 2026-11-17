# Activation de l'abonnement et paiement — powpow-register

## Conclusion (la réponse d'abord)
> **Période d'essai gratuit (à partir du 2026-10-18 ; le comportement réel de la plateforme prévaut)** : pendant cette période, un compte inscrit peut utiliser toutes les fonctions directement, et **s'abonner est une amélioration facultative plutôt qu'une exigence** — suis le flux de ce fichier seulement quand l'utilisateur veut activement l'adhésion. Quand la période d'essai se terminera, les comptes non abonnés visitant les pages de contenu seront redirigés vers la page d'abonnement ; il suffit de finaliser l'abonnement selon ce fichier.


**Les abonnements par Alipay comme par PayPal peuvent désormais être pris en charge par l'agent — création de la commande et suivi de l'encaissement compris.**
Alipay est un achat unique sans renouvellement automatique, pour les utilisateurs en Chine continentale et ceux qui ont Alipay ; PayPal se renouvelle automatiquement chaque mois et s'annule à tout moment,
pour les utilisateurs à l'étranger et sans Alipay. Le QR code WeChat (confirmation manuelle) et Huawei IAP restent disponibles, mais la compétence ne les prend pas en charge.

Répartition des responsabilités dans le paiement : l'agent peut **créer la commande, ouvrir la caisse,
consulter l'encaissement** ; il ne touche **jamais** au compte Alipay/PayPal de l'utilisateur ni à ses moyens de
paiement, et ne promet jamais de « payer à sa place ». L'acte de paiement est toujours accompli par
l'utilisateur lui-même à la caisse officielle.

## Canal Alipay (vibepay, voie principale)

Achat unique sans abonnement : on paie une fois pour activer la durée correspondante, **sans
renouvellement automatique**. Les formules sont figées dans `src/lib/alipay-vibepay.ts`
(`ALIPAY_PACKAGES`) :

| key | planId | Nom | Prix | Durée |
|---|---|---|---|---|
| `monthly` | alipay-monthly | Membre mensuel | ¥6.99 | 30 jours |
| `quarterly` | alipay-quarterly | Membre trimestriel | ¥19.99 | 90 jours |
| `yearly` | alipay-yearly | Membre annuel | ¥69.99 | 365 jours |

### Contrat des interfaces (déjà encapsulées par le script de la compétence, l'agent n'assemble pas les requêtes à la main)

| Interface | Méthode | Description |
|---|---|---|
| `/api/payment/alipay/create-order` | POST | Nécessite `Authorization: Bearer <JWT>` (un utilisateur pending suffit). body `{package}` → renvoie `{paymentHtml, outTradeNo, amount, planName}` ; `paymentHtml` est une page de formulaire s'auto-soumettant vers la passerelle Alipay |
| `/api/payment/alipay/query` | GET `?outTradeNo=` | Même authentification Bearer. Renvoie `paid` / `pending` / `closed` / `unknown` |
| `/api/payment/alipay/notify` | POST (callback du serveur Alipay) | Vérification de signature en cinq points (signature, app_id, concordance du montant, TRADE_SUCCESS/TRADE_FINISHED, unicité du marchand) → mise à jour **idempotente** de la commande + création de l'abonnement + activation du compte. La compétence ne touche jamais à cette interface |
| `/payment/alipay/return` | Page de retour navigateur | Chemin public ; après paiement, affiche la confirmation 「支付成功」 et interroge en boucle dans la page l'état réel du backend |

- Une commande impayée se **ferme automatiquement au bout de 2 heures** ; si l'utilisateur abandonne en
  chemin → relancer directement `create-order`, on ne s'occupe pas de l'ancienne commande.
- Le script écrit le `paymentHtml` dans un fichier HTML temporaire ; l'agent l'ouvre avec une commande
  système et l'on entre ainsi à la caisse Alipay (scan du QR code ou connexion à Alipay pour payer).

### Chaîne d'activation (automatique, sans intervention humaine)

Vérification de signature du notify passée → `paymentOrders` marquée payée → `user_subscriptions`
créée/prorogée (`planId`, `currentPeriodEnd` calculés selon durationDays ; les renouvellements se
prorogent sur la date d'expiration d'origine) → `users.accountStatus: active` +
`subscriptionStatus: ACTIVE` → la page de retour constate le paid et affiche le succès.

## Après le paiement, il faut impérativement renouveler l'état de connexion (important)

Le JWT embarque la déclaration d'abonnement (pour un compte pending, c'est `NONE`). **L'encaissement ne
met à jour que la base de données, il ne modifie pas un JWT déjà émis** — la déclaration de l'ancien
token reste NONE ; l'utiliser directement pour générer un lien de connexion se manifeste en « pas de
membership ». C'est pourquoi la compétence, après confirmation du `paid` / du `ACTIVE` PayPal, lance d'abord `refresh-login`
(reconnexion contre un JWT neuf, déclaration ACTIVE), puis génère le lien 2. C'est un comportement voulu
par la conception, pas un correctif de bug.

## Canal d'abonnement PayPal (pris en charge par la compétence ; web, hors HarmonyOS)

Il n'existe qu'une seule formule, Premium Monthly (environ $1/mois, selon ce que renvoie `/api/subscription/plans`) ; **elle se renouvelle automatiquement chaque mois**
et l'utilisateur peut l'annuler quand il veut depuis son compte PayPal.

### Contrat d'interface (déjà encapsulé par le script de la compétence ; l'agent n'assemble pas les requêtes à la main)

| Interface | Méthode | Description |
|---|---|---|
| `/api/subscription/plans` | GET | Auth Bearer ; renvoie la liste des formules disponibles (actuellement une seule) |
| `/api/subscription/create` | POST | body `{planId}` → renvoie `{subscriptionId, approveUrl, status}` ; `status` vaut généralement `APPROVAL_PENDING` |
| `/api/subscription/create` | GET | Auth Bearer ; renvoie `{activeSubscription, allSubscriptions}` ; l'agent sonde `activeSubscription.subscription.status === 'ACTIVE'` |
| `/api/subscription/verify` | POST | Appelée automatiquement par la page de succès (avec le cookie) ; active directement via l'API PayPal si le webhook n'est pas arrivé |
| `/subscription/success` | Page de retour navigateur | Page d'atterrissage après l'autorisation PayPal ; sonde verify automatiquement, puis revient à l'accueil / à la page d'origine |
| `/subscription/cancel` | Page navigateur | Page d'atterrissage en cas d'annulation ou d'échec ; on peut relancer |

### Déroulé délégué

```
create-order --provider paypal  # → renvoie approveUrl, écrit dans un fichier HTML local
ouvrir le fichier HTML          # → le navigateur saute vers la page d'autorisation PayPal
query (toutes les 10–15 s)      # → sonder jusqu'à ACTIVE
refresh-login                   # → échanger contre un JWT neuf (déclaration d'abonnement ACTIVE)
login-link --target home        # → générer le lien de connexion définitif
```

- Les abonnements PENDING non finalisés dans l'heure sont nettoyés automatiquement par le backend ; il suffit de relancer.
- Si l'utilisateur relance `create-order`, le backend réutilise l'abonnement `APPROVAL_PENDING` encore valide, ce qui évite un 409.
- Comme avec Alipay : l'encaissement ne met à jour que la base de données, un ancien JWT ne se rafraîchit pas tout seul — il **faut** lancer `refresh-login` avant d'envoyer le lien vers l'accueil.

## Les quatre canaux de la page d'abonnement

La page d'abonnement `src/app/(public)/subscription/page.tsx` affiche selon l'environnement d'exécution :

| Canal | Environnement | Mécanisme | Mode d'activation |
|---|---|---|---|
| **Alipay (principal)** | Web | `AlipayPaymentSection` passe par les interfaces vibepay (tableau ci-dessus) | Activation automatique côté serveur via notify, en quelques secondes |
| Abonnement PayPal | Web (hors HarmonyOS) | `/api/subscription/create` → saut vers l'autorisation PayPal ; renouvellement mensuel automatique, annulable à tout moment (`/api/subscription/manage`) | Le Webhook PayPal (`BILLING.SUBSCRIPTION.*`) passe active automatiquement |
| Abonnement par QR code WeChat | Web (hors HarmonyOS) | En bas de page 「微信扫码订阅」 (scanner pour s'abonner) : transfert par QR code | **Confirmation manuelle**, l'encaissement peut être retardé ; ne conclu pas trop vite à un échec juste après le paiement |
| Achat intégré Huawei | Dans l'app HarmonyOS | `NativeBridge.purchaseSubscription()` natif | `/api/subscription/activate-huawei` valide la commande Huawei puis active |

Les plans et prix PayPal se lisent dynamiquement depuis `/api/subscription/plans` ; texte fixe de la page :
Auto-renews. Cancel anytime.

## États et redirections

- Alipay terminé → la page de retour affiche le succès ; PayPal réussi → `/subscription/success` →
  compte active → retour automatique vers la page d'origine indiquée par le paramètre `next` (à défaut,
  l'accueil).
- Un utilisateur déjà abonné qui revisite la page d'abonnement → voit "You're All Set!", retour
  automatique à l'accueil au bout de 3 secondes.
- Paiement échoué / annulé (PayPal) → `/subscription/cancel`, on peut relancer.

## Diagnostic

| Symptôme | Gestion |
|---|---|
| Alipay payé mais `query` toujours pending | Le notify a rarement du retard ; attends 30 secondes et relance. Sinon, l'utilisateur regarde dans son navigateur l'état de la page de retour ; si ça ne va toujours pas, contacter le support de la plateforme (dongtao@outlook.com) en communiquant le `outTradeNo` |
| Alipay payé, mais avec le lien 2 on est encore bloqué | Le `refresh-login` a été sauté (déclaration du vieux JWT non mise à jour) — d'abord `refresh-login` puis `login-link` |
| Le `query` PayPal reste PENDING | L'utilisateur n'a pas finalisé l'autorisation dans PayPal ; vérifie que le lien d'autorisation a bien été ouvert dans le navigateur. Si c'est toujours PENDING après autorisation, le webhook a peut-être du retard : demande à l'utilisateur d'attendre quelques secondes de plus sur la page de succès ou de la recharger |
| Le `query` PayPal renvoie 409 | Il existe déjà un abonnement PENDING non terminé ; attends 1 heure qu'il expire, ou finalise l'autorisation de l'ancien lien dans le navigateur |
| PayPal payé, mais l'accès via le lien 2 reste bloqué | Comme avec Alipay : d'abord `refresh-login`, ensuite `login-link` |
| Toujours 403 après paiement (PayPal) | Le Webhook a parfois du retard ; se reconnecter pour rafraîchir l'état |
| Payé via WeChat mais pas d'activation | La confirmation manuelle est asynchrone ; si rien en quelques heures, contacter le support de la plateforme |
| La page d'abonnement affiche "No subscription plans available" | `/api/subscription/plans` n'a aucun plan PayPal disponible, problème de configuration côté plateforme ; les utilisateurs de Chine continentale passent par Alipay |

## Note historique

Le code contient en outre **une ancienne** passerelle de paiement web Alipay (`src/lib/alipay.ts`,
`/api/payment/create-order`, ¥9.90/¥99 achat unique, dégradée en paiement simulé quand le sandbox n'a pas
de clés configurées), jamais raccordée à l'UI de la page d'abonnement, sans rapport avec vibepay. La
compétence ne la touche en aucun cas ; `alipay-vibepay.ts` est le canal en vigueur.
