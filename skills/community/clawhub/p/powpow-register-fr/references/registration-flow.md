# Détail du flux d'inscription — powpow-register

Pour consultation lors du dépannage. Toutes les règles viennent du code source de la plateforme
(validation cohérente frontend/backend Next.js), sources citées. Si la plateforme évolue, le comportement
réel en ligne prime.

## Points d'entrée

- Page d'inscription : https://global.powpow.online/register
- Page de connexion : https://global.powpow.online/login
- Page d'abonnement : https://global.powpow.online/subscription
- Si l'on entre depuis un lien de partage avec `?next=...`, après inscription + paiement, retour
  automatique à la page d'origine.

## Champs du formulaire et règles

| Champ | Obligatoire | Règle | Source dans le code |
|---|---|---|---|
| Avatar | Optionnel | Image ≤5Mo, SVG non pris en charge ; compression automatique côté serveur (>100Ko compressé en 400×400 / qualité 90) | `src/app/api/auth/register/route.ts` |
| Nom d'utilisateur | Obligatoire | 2~50 caractères, après trim stockage en **minuscules** (Tom et tom comptent comme le même nom d'utilisateur ; insensible à la casse à l'inscription comme à la connexion) | Idem (zod schema) |
| Mot de passe | Obligatoire | 8~100 caractères, doit contenir à la fois majuscule, minuscule et chiffre | Idem |
| Confirmation du mot de passe | Obligatoire | Identique au mot de passe (validation frontend uniquement) | `src/app/(public)/register/page.tsx` |
| Pseudo | Optionnel | ≤100 caractères ; si vide, prend par défaut le nom d'utilisateur | register route |
| E-mail | **Obligatoire** | Format d'e-mail valide, ≤255 caractères ; un e-mail ne peut être inscrit que sur un seul compte | register route |
| Code de vérification par e-mail | **Obligatoire** | 6 chiffres ; **valable 10 minutes** ; annulé dès validation réussie ; un renvoi marque l'ancien code comme utilisé | `src/lib/email-verification.ts` |
| Téléphone | Optionnel | Numéro de Chine continentale, 11 chiffres commençant par `1[3-9]` ; un numéro ne peut être lié qu'à un seul compte | register route |

La page propose en outre trois boutons de connexion tierce : **Google, Watcha, compte Huawei**
(`GoogleSignInButton` / `WatchaLoginButton` / `HuaweiLoginButton`). Les comptes tiers n'ont pas de mot de
passe local ; une connexion par mot de passe ensuite renvoie
「该账号未设置密码，请使用其他方式登录」 (ce compte n'a pas de mot de passe défini, connectez-vous autrement).

## Limitation de fréquence et protection anti-force brute

| Action | Limite | Source |
|---|---|---|
| Soumission de l'inscription | **3 fois/minute/IP**, dépassement → 429 | `src/lib/rate-limit.ts` `REGISTER_RATE_LIMIT` |
| Envoi du code de vérification | Même IP 1 fois/minute **et** même e-mail 1 fois/minute, dépassement → 429 ; bouton frontend avec compte à rebours de 60 secondes | `src/app/api/auth/register/send-code/route.ts` |
| Validation du code | Par e-mail, au plus **5 tentatives** en 10 minutes ; à la limite, refus même si le code est juste ; il faut redemander un code | `src/lib/email-verification.ts` |
| Envoi du code « mot de passe oublié » | 1 fois/minute/IP | `src/app/api/auth/forgot-password/route.ts` |
| Connexion | 5 fois/minute/IP ; un même compte avec **5 échecs** consécutifs est **verrouillé 30 minutes** (423), avec décompte des tentatives restantes pendant le verrouillage | `src/app/api/auth/login/route.ts`, `rate-limit.ts` |

**Comportement de protection de la vie privée** : lors de l'envoi du code de vérification / du mot de passe
oublié, si l'e-mail est déjà inscrit ou inexistant, l'interface renvoie dans tous les cas un message de
succès uniforme, sans divulguer si l'e-mail est inscrit.

## Équivalence entre le mode délégué à l'agent et l'inscription Web

Le script de la compétence appelle **le même lot d'API publiques** (`/api/auth/register`, `send-code`,
`login`, `/api/auth/me`), et passe exactement par les mêmes validations, limitations et chemins d'erreur
que la soumission du formulaire de la page d'inscription — toutes les règles de ce fichier s'appliquent à
l'identique aux deux modes. La séquence du script et le contrat des commandes sont dans
`references/agent-flow.md`.

## Flux d'état après une inscription réussie

> **Période d'essai gratuit (à partir du 2026-10-18 ; le comportement réel de la plateforme prévaut)** : un compte nouvellement inscrit peut **utiliser toutes les fonctions directement**
> (fil, carte, humains numériques, check-ins, etc.) sans paiement requis ; les comptes non abonnés ne sont plus bloqués des pages de contenu. La description du
> « blocage pending » de cette section est l'état normal après la fin de la période d'essai — le moment venu, le comportement réel en ligne prévaut.

1. L'utilisateur est enregistré avec `accountStatus: 'pending'` et **3 badges initiaux** (register route).
2. Le serveur plante aussi deux cookies HttpOnly : le JWT (peut accéder aux pages directement) et
   le pendingUserToken (identifiant d'identité pour le flux d'abonnement).
3. Dans l'état normal (période d'essai terminée / pas de période gratuite), la page d'inscription détecte `pending_payment` → redirige vers `/subscription`
   (en conservant le paramètre de retour `next`) ; en mode assisté par agent, `me?token=…&redirect=/subscription` produit le même effet.
   **Pendant la période d'essai gratuit, cette étape ne se déclenche pas** — après l'inscription, entre directement sur la page d'accueil et commence à utiliser.
4. Paiement finalisé → `accountStatus` devient `active` (**Alipay active automatiquement côté serveur via notify** ;
   PayPal active via Webhook ; le code QR WeChat est confirmé manuellement ; Huawei IAP passe par `activate-huawei`).
   Détails dans `payment-and-activation.md`.

Dans l'état normal, les utilisateurs inactifs (pending) appelant les API cœur (fil, carte, chat d'humains numériques, check-ins, etc.) reçoivent 403 ;
les liens de posts partagés sont l'exception (restent accessibles publiquement). Pendant la période d'essai gratuit, ce blocage est suspendu et tout est ouvert.
## Tableau de diagnostic des erreurs courantes

| Symptôme | Cause | Que faire |
|---|---|---|
| 「用户名已存在」 (le nom d'utilisateur existe déjà) | Nom d'utilisateur pris (insensible à la casse) | Essayer un autre nom d'utilisateur |
| 「邮箱已被使用」 (l'e-mail est déjà utilisé) | E-mail déjà inscrit | Changer d'e-mail ; ou passer par connexion +「忘记密码」(mot de passe oublié) pour retrouver l'ancien compte |
| 「邮箱验证码错误或已过期」 (code de vérification erroné ou expiré) | Code mal saisi / plus de 10 minutes / refusé après plus de 5 tentatives | Cliquer 「重新发送」(renvoyer) et utiliser le code du **dernier e-mail reçu** |
| Code de vérification non reçu | Limitation de 60 secondes ; ou classé en spam / courriers publicitaires | Attendre la fin du compte à rebours avant de renvoyer ; fouiller le dossier spam |
| 「手机号已被使用」 (le téléphone est déjà utilisé) | Numéro déjà lié à un autre compte | Retirer le téléphone (facultatif) ou changer de numéro |
| 「注册请求过于频繁」 (demande d'inscription trop fréquente) / 429 | Plafond de 3 inscriptions/minute/IP atteint | Attendre quelques minutes et réessayer |
| 409 「用户名或邮箱已被注册」 (nom d'utilisateur ou e-mail déjà enregistré) | Collision avec quelqu'un d'autre à l'instant de la soumission (filet de sécurité contre la concurrence) | Changer de nom d'utilisateur ou d'e-mail puis réessayer |
| 「图片大小不能超过5MB」 (l'image ne peut pas dépasser 5Mo) / 「不支持 SVG」 (SVG non pris en charge) | Avatar hors norme | Changer d'image ou passer l'avatar |
| L'utilisateur ouvre le lien de connexion mais atterrit sur la page d'abonnement (au lieu de la page d'accueil) | La période d'essai gratuit est terminée et le mur de paiement de la plateforme est revenu | Suis le flux de paiement par abonnement de l'étape 7 de SKILL.md ; après l'abonnement, lance `refresh-login` puis envoie le lien vers la page d'accueil |
| Inscription réussie mais la connexion renvoie 403 « 请完成订阅以激活账户 » | Le compte est encore pending, et la plateforme n'est pas en période d'essai gratuit (état attendu avant paiement) | Ne se produit pas pendant la période d'essai gratuit ; si ça arrive, la période d'essai est terminée — finalise d'abord l'abonnement ; si toujours 403 après paiement, un ancien JWT a été utilisé — en mode script, lance d'abord `refresh-login` pour échanger contre un nouvel état de session |
| Connexion 423 「账户已锁定」 (compte verrouillé) | 5 mots de passe erronés d'affilée | Attendre 30 minutes |
| Connexion 401 「还剩 N 次尝试机会」 (il reste N tentatives) | Mot de passe erroné, proche du verrouillage | Réfléchir avant de réessayer, ou passer directement par 「忘记密码」(mot de passe oublié) |
| 「该账号未设置密码，请使用其他方式登录」 (ce compte n'a pas de mot de passe défini, connectez-vous autrement) | Compte tiers (Google/Watcha/Huawei) | Se connecter avec le bouton tiers d'origine |
| 「该账号已注销」 (ce compte a été supprimé) | Compte désactivé | Il faut se réinscrire |

## À savoir sur la connexion (utile au dépannage au passage)

La connexion accepte l'entrée triple **nom d'utilisateur / e-mail / téléphone** (chacun des trois sert
d'identifiant). Mot de passe oublié : page de connexion → 「忘记密码」(mot de passe oublié) → saisir
l'e-mail d'inscription pour recevoir un code à 6 chiffres → réinitialiser.
