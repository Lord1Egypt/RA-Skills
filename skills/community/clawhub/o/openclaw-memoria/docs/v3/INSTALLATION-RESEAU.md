# Installer Memoria sur une nouvelle machine + partager la mémoire (réseau)

Guide non-technique. Objectif : installer Memoria sur l'iMac (Luna), le relier au
Mac Studio (Koda = le « hub ») et partager la mémoire d'équipe + le coffre.

## 1. Installer sur une machine neuve (l'iMac de Luna)

Sur l'iMac, ouvrir le Terminal et coller **une seule commande** :

```sh
curl -fsSL https://raw.githubusercontent.com/Primo-Studio/openclaw-memoria/memoria-v1/scripts/install-memoria.sh | sh
```

(ou, si le dépôt est déjà cloné : `sh scripts/install-memoria.sh`)

Le script fait tout : il vérifie les outils, télécharge Memoria, l'installe, le
construit, démarre le service, configure la commande `memoria` (PATH dans
`~/.zshrc`), active le **lancement automatique au démarrage du Mac** et **ouvre
l'interface tout seul** dans le navigateur.

Pour rouvrir l'interface plus tard : taper **`memoria ui`** (ou `memoria` tout
court) dans le Terminal. Pas besoin de relancer quoi que ce soit après un
redémarrage : Memoria démarre tout seul au prochain allumage.

> Pré-requis : **Node.js 22 LTS** (https://nodejs.org). Le script vérifie sa
> présence et s'arrête proprement s'il manque (il avertit aussi si une version
> non-LTS est installée). Les **outils de développement Apple** sont gérés par
> le script lui-même : s'ils manquent, il ouvre la fenêtre d'installation
> système (~5 min) et demande simplement de le relancer ensuite.

> Sécurité : si le dossier `~/openclaw-memoria` contient des modifications
> locales (machine de développement), le script **refuse** de l'écraser et
> conseille `memoria update` à la place.

## 1bis. Choisir le moteur d'intelligence

Au premier lancement, l'écran d'accueil de l'interface te guide pour brancher
le **moteur d'intelligence** — c'est lui qui transforme les conversations en
souvenirs. Trois options :

- **Ollama** (recommandé) : 100 % local et gratuit, rien ne sort de la machine.
- **LM Studio** : local aussi, si tu préfères son application.
- **Clé API** (Anthropic, OpenAI, OpenRouter) : moteur dans le cloud.

Sans moteur configuré, Memoria capture les conversations mais **n'extrait aucun
souvenir** — et te l'affiche clairement dans l'interface (rien n'échoue en
silence). Suis simplement l'onboarding : il détecte ce qui est installé et
propose la marche à suivre.

## 2. Désigner le hub (le Mac Studio de Koda)

Sur le Mac Studio (machine toujours allumée), dans l'interface :

**Réglages → Synchro entre machines → « Faire de cette machine le hub »**, puis
redémarrer le service (le bouton l'indique, ou `memoria stop && memoria start`).

En terminal, l'équivalent : `memoria sync init-hub` puis `memoria stop && memoria start`.

## 3. Inviter une machine

Sur le hub : **Réglages → Synchro → « Inviter une machine »** → un **code** s'affiche
(valable 10 min) avec l'adresse du hub. En terminal : `memoria sync invite`.

## 4. Relier l'iMac au hub

Sur l'iMac : **Réglages → Synchro → « Relier au hub »** → coller l'**adresse du hub**
(ex. `192.168.1.20:47600`) + le **code**. En terminal :

```sh
memoria sync join --hub 192.168.1.20:47600 --code XXXX-XXXX
```

L'iMac récupère alors **tout l'historique partagé** (infos sur Néto, l'entreprise,
les projets) **+ les mots de passe partagés** (coffre), et reste synchronisé.

### Ce qui se partage — et ce qui NE se partage PAS

| Partagé entre machines | JAMAIS partagé |
|---|---|
| Scope **user** (infos sur Néto) | Mémoire **privée** de chaque agent |
| Scope **org** (entreprise, lignes de commande, conventions) | Quarantaine `legacy_to_review` |
| Scopes **projet/client** | Télémétrie d'usage locale |
| **Coffre** : secrets marqués « partageables » (valeur chiffrée en transit) | Secrets `critical` (sauf opt-in explicite) |

La valeur d'un mot de passe ne circule **jamais en clair** : elle est chiffrée
(GVK) avant de quitter le hub et déchiffrée seulement sur la machine destinataire.

## 5. Mettre à jour Memoria (toutes machines)

**Réglages → Mise à jour → « Vérifier et mettre à jour »** : télécharge la dernière
version, reconstruit, redémarre le service tout seul. En terminal : `memoria update`.

## 6. Identifier l'interlocuteur

Dans **Personnes**, enregistrer qui peut parler aux agents (Néto, Badette, des
stagiaires, un client) avec leurs identifiants (Telegram, WhatsApp, e-mail). Les
agents appellent `memoria_identify_interlocutor` pour savoir à qui ils parlent et
adapter ton + contexte.

## Sécurité réseau (résumé)

- Seules les routes `/v1/sync/*` sortent du loopback, **uniquement sur le LAN**,
  derrière un **token de pair + signature HMAC** (anti-rejeu/anti-MITM). Les
  routes d'administration et de mémoire restent strictement locales (127.0.0.1).
- Les clés (coffre de groupe GVK, clé de pairing CPK, token de pair) vivent dans
  le **Trousseau** (Keychain) / coffre chiffré — **jamais** dans un fichier en clair.
- Se déconnecter : **Réglages → Synchro → « Se déconnecter »** (`memoria sync leave`).
  Les souvenirs et secrets déjà reçus restent disponibles hors-ligne.
