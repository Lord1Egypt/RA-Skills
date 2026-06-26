---
name: pipeline-comptable
description: Chef d'orchestre du traitement des pièces comptables entrantes. Enchaîne automatiquement les quatre étapes — tri du mail ①, analyse de la pièce ②, identification du client ③, classement ④ — comme une assistante qui traite son courrier du matin. À utiliser dès qu'il faut traiter du courrier entrant ou un lot de pièces de bout en bout : « traite les mails reçus », « range tout ce qui est arrivé », « classe ces factures », « traite cette note de frais », un mail avec pièce jointe comptable arrive, ou un dépôt de documents à traiter. Gère factures, relevés bancaires ET notes de frais. Délègue tout aux petites briques mono-tâche (tri-courrier-entrant, analyse-piece-comptable, identification-client, classement-document) et fait remonter un compte-rendu unique + les questions à poser au comptable.
license: Interne — usage privé OpenClaw
---

# Skill `pipeline-comptable` — orchestrateur

> Action humaine : **traiter son courrier du matin de bout en bout.**
> N'invente aucune logique : il appelle les quatre briques dans l'ordre et passe
> le « dossier » de l'une à l'autre. Toute l'intelligence est dans les briques.

```
   📬 mail / dépôt de pièces
        │
   ① tri-courrier-entrant     ce mail me concerne ? quelles pièces ?
        ▼
   ② analyse-piece-comptable  qu'est-ce que c'est ? quels montants ?
        ▼
   ③ identification-client    à quel client ça appartient ? achat ou vente ?
        ▼
   ④ classement-document      je range au bon endroit.
        ▼
   ⑤ rapprochement-paiements  je pointe les relevés avec les factures.
```

L'étape ⑤ se lance automatiquement une fois les pièces classées (le moteur
retraite tout le dossier client, c'est un cache reconstructible). Pour la sauter
ponctuellement : `--no-rapprochement`.

---

## Comment l'utiliser

```bash
# Depuis un mail (tri ① inclus, puis ②③④ par pièce) :
python3 scripts/pipeline.py --email <mail.json> --clients-root <chemin/clients>

# Depuis un lot de pièces déjà déposées (②③④, pas de mail donc pas d'étape ①) :
python3 scripts/pipeline.py --inbox <dossier> --clients-root <chemin/clients>
```

Sortie : un **rapport JSON consolidé** sur la sortie standard (un « dossier »
complet par pièce, avec chaque bloc rempli par son étape) + un **résumé lisible**
sur la sortie d'erreur (pièces rangées, doublons, en attente, questions).

---

## Comment en rendre compte au comptable

Lis le résumé et restitue-le simplement, dans le ton habituel :

1. **Ce qui a été fait** — « 5 pièces traitées : 4 factures rangées, 1 relevé. »
2. **Ce qui attend une décision** — pose les questions d'identification telles
   quelles, une par pièce ambiguë. Ne tranche jamais à la place du comptable.
3. **Ce qui mérite attention** — pièces incomplètes, doublons écartés.

Jamais de chemin technique, de nom de script, de « JSON » ou d'« index ».

Quand des pièces ont été rangées, la suite naturelle est le rapprochement des
paiements (`rapprochement-paiements`) — propose-le.

---

## Pourquoi un orchestrateur séparé

Chaque brique reste utilisable seule (analyser une pièce isolée, reconnaître un
client, ranger un document). L'orchestrateur ne fait que les **enchaîner** pour le
cas courant « du courrier arrive, traite-le ». Si une brique évolue, l'orchestrateur
n'a rien à changer : il parle le même « dossier » JSON d'un bout à l'autre.

---

## Limites assumées

- Les questions d'identification s'adressent au comptable : l'orchestrateur les
  remonte, il ne décide pas à sa place.
- Il traite, range et rapproche (étapes ① → ⑤). Il ne rédige pas les relances
  lui-même : il les fait remonter (workflow e-mail) pour validation du comptable.
- Le tri ① ne s'applique qu'au mode mail ; un dépôt direct de pièces commence à ②.
