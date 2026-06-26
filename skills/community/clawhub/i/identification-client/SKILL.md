---
name: identification-client
description: Étape ③ du pipeline comptable. Reconnaît à quel client appartient une pièce déjà analysée, et pour une facture détermine le sens (achat = le client est le destinataire, vente = le client est l'émetteur). À utiliser dès qu'il faut rattacher un document à un dossier client : « à qui appartient cette facture ? », « c'est un de nos clients ? », « c'est un achat ou une vente ? », après l'analyse d'une pièce et avant de la ranger. C'est la seule brique qui tient le registre clients (clients.json) : elle le lit pour reconnaître et n'y ajoute que du certain (un nouveau client vu sur un relevé bancaire). Ne range aucun fichier (c'est classement-document).
license: Interne — usage privé OpenClaw
---

# Skill `identification-client` — étape ③

> Action humaine : **regarder une pièce analysée et reconnaître le dossier client.**
> Seule brique qui connaît et tient `clients.json`. Ne range aucun fichier.

---

## Comment l'utiliser

```bash
echo '<dossier.json>' | python3 scripts/identifier.py --clients <chemin/clients.json>
```

Entrée : un dossier contenant l'analyse de la pièce (étape ②) et, si disponible,
l'en-tête du mail (étape ①). Sortie : le même dossier + un bloc `client`.

```jsonc
{ "client": {
    "slug": "numerix-studio" | null,
    "role": "out" | "in" | "holder" | null,   // out = vente, in = achat
    "counterparty": "Auberge du Vieux Port" | null,
    "method": "relevé | raison-sociale-exacte | raison-sociale | null",
    "confidence": "haute | moyenne | faible",
    "needs_review": false,
    "question": null                            // posée au comptable si à confirmer
}}
```

---

## Comment elle reconnaît (du plus sûr au moins sûr)

1. **Relevé bancaire** → le titulaire EST le client : certitude. Si le client est
   nouveau, sa fiche est créée dans `clients.json` (`auto-from-bank-statement`).
2. **Facture** → on compare l'émetteur et le destinataire aux raisons sociales
   connues (égalité, puis ressemblance ≥ 0,82).
   - un seul côté reconnu → c'est le client ; émetteur reconnu → **vente** (`out`),
     destinataire reconnu → **achat** (`in`) ;
   - les deux reconnus, ou aucun → on **ne devine pas** : `needs_review` + une
     question claire pour le comptable.

Le SIREN sert seulement à **renforcer la confiance** quand il confirme le client
trouvé par le nom — jamais à choisir le côté. Raison : l'analyse renvoie tous les
SIREN de la pièce (vendeur ET acheteur) en vrac ; s'en servir des deux côtés
ferait correspondre les deux à la fois. C'est exactement ce qui, par le passé,
remplissait les fiches de SIREN parasites — donc on ne réinjecte aucun SIREN
automatiquement ici.

---

## Comment en rendre compte au comptable

Sans jargon : « Cette facture est une vente de Numérix Studio à l'Auberge du Vieux
Port » ou « Je n'arrive pas à rattacher cette facture : … ». Si `question` est
renseignée, **pose-la telle quelle** et attends la réponse — ne tranche jamais à
la place du comptable. Une fois sa réponse connue, complète la fiche client et
relance.

---

## Limites assumées

- Ne range rien : une fois le client connu, c'est `classement-document` (étape ④).
- N'écrit dans `clients.json` que du sûr (titulaire de relevé). Apprendre les
  domaines mail / SIREN d'un client se fait via une confirmation explicite, pas en
  devinant sur une facture — pour garder le registre propre.
- Ne juge ni doublon, ni paiement, ni rapprochement : ça se voit au niveau du
  dossier, pas sur une pièce isolée.
