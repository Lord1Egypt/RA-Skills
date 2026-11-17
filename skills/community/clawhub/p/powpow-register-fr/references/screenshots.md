# Captures d'écran du produit — powpow-register

À utiliser au besoin à l'exécution. Si l'utilisateur ne connaît pas du tout Bulle, ou s'il a besoin de
« voir » à quoi ressemble le produit, envoie directement la capture correspondante.

## Emplacement des images

- Les six captures sont **embarquées avec la compétence**, dans `assets/screenshots/powpow-0N.jpg` (N de 1 à 6).
  Envoie-les directement comme fichiers image locaux — aucune connexion requise, utilisable dans n'importe
  quel environnement (y compris ceux qui n'atteignent pas GitHub).
- Uniquement en secours si des fichiers du paquet manquent par accident : copie hébergée sur
  `https://raw.githubusercontent.com/durenzidu/durenzidu/main/screenshots/powpow-0N.jpg` ou miroir
  `https://cdn.jsdelivr.net/gh/durenzidu/durenzidu@main/screenshots/powpow-0N.jpg` (attention : les deux
  peuvent ne pas s'ouvrir depuis la Chine continentale — privilégie les fichiers du paquet).
- N'envoie que 1–3 images en rapport avec le sujet du moment.

## Inventaire

### powpow-01.jpg — Page de détail d'un humain numérique

![Page de détail d'un humain numérique](../assets/screenshots/powpow-01.jpg)

Fiche d'une personne réelle ou historique devenue humain numérique : statut en ligne, localisation,
biographie, « lancer une conversation », etc.
**Sert à** : présenter que « une fois inscrit, tu pourras discuter avec les humains numériques de la carte ».

### powpow-02.jpg — Page d'édition des posts

![Page d'édition des posts](../assets/screenshots/powpow-02.jpg)

Interface d'édition pour écrire des posts ou des journaux de voyage, avec un groupe de boutons flottants en bas à droite.
**Sert à** : quand l'utilisateur demande « qu'est-ce que je peux faire une fois inscrit ? » ou « où est-ce qu'on écrit ? ».

### powpow-03.jpg — Page de la carte (bulles + humains numériques)

![Page de la carte](../assets/screenshots/powpow-03.jpg)

Vue d'ensemble de la carte publique : les posts localisés s'agglomèrent en « bulles » sur la carte, et les
humains numériques sont épinglés avec leur avatar à des lieux réels.
**Sert à** : **image privilégiée pour présenter le produit à l'ouverture** — « le journal de voyage que tu publies devient une bulle sur la carte ».

### powpow-04.jpg — Profil personnel (actifs numériques)

![Profil personnel](../assets/screenshots/powpow-04.jpg)

La page propre de l'utilisateur : amis/abonnements/abonnés, et les « actifs numériques » — solde de badges,
mes bulles, mes humains numériques.
**Sert à** : montrer où vivent les badges quand on dit « à l'inscription on t'offre 3 badges » ; quand
l'utilisateur demande « quels actifs est-ce que j'ai ? ».

### powpow-05.jpg — Page de progression des histoires

![Page de progression des histoires](../assets/screenshots/powpow-05.jpg)

Le jeu d'histoires dans la plateforme (exemple « Yongle · 1421 ») : progression par chapitres, gains de
badges, jeu de rôle.
**Sert à** : quand l'utilisateur demande « à part publier, on peut jouer à quoi d'autre ? » ou « comment on gagne des badges ? ».

### powpow-06.jpg — Page de détail d'un post (exemple abouti)

![Page de détail d'un post](../assets/screenshots/powpow-06.jpg)

Un journal de voyage déjà publié : auteur, étiquettes de lieu, texte, photos ; en bas, j'aime /
commentaires / partage / enregistrement.
**Sert à** : **deuxième image d'ouverture** — « voilà ce que voient les autres quand ils ouvrent ta bulle sur la carte ».

## Consultation rapide par scène

| Ce que dit l'utilisateur / moment | Quelle capture envoyer |
|---|---|
| Ouverture, « qu'est-ce que Bulle ? » | powpow-03 + powpow-06 |
| « Qu'est-ce que je peux faire une fois inscrit ? » | powpow-02 + powpow-01 |
| « Qu'est-ce que c'est les badges / qu'est-ce que j'ai ? » | powpow-04 |
| « À part publier, quoi d'autre ? » | powpow-05 |
| Dépannage inscription/abonnement | En général pas besoin d'image ; ne l'envoie que s'il faut expliquer où se trouve un élément dans la page |

## Note de maintenance

- Les images de `assets/screenshots/` sont la copie de référence publiée avec le paquet. Quand une capture
  doit être mise à jour, remplace le fichier homonyme dans `assets/screenshots/` (en gardant le nom
  `powpow-0N.jpg`) et publie une nouvelle version.
- La copie hébergée du dépôt public `durenzidu/durenzidu` (répertoire `screenshots/`) est conservée comme
  miroir de secours, synchronisée avec les fichiers du paquet.
- La galerie actuelle n'a pas de capture de la **page d'inscription** ni de la **page d'abonnement**. Si un
  jour elles s'ajoutent (par exemple `powpow-07.jpg` pour l'inscription et `powpow-08.jpg` pour
  l'abonnement), place les fichiers dans `assets/screenshots/` et ajoute une section au même format ; le
  texte guide de SKILL.md peut les référencer au passage.
