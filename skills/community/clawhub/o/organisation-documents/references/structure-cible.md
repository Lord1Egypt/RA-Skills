# Référence — Structure cible & conventions de nommage

> Référence chargée à la demande par `organisation-documents`. Spec exhaustive du classement.
> Source de vérité pour les autres skills qui écrivent dans le même arbre (`relances`, `facturation`, `rapprochement-bancaire`).

---

## Arborescence complète

```
~/.openclaw/workspace/
├── clients/
│   ├── <slug>/                                # un dossier = un client réel (existant ou auto-créé)
│   │   ├── contrats/                          # niveau client — contrats pluriannuels
│   │   │   └── <AAAA-MM-JJ>_<Type>_<Contrepartie>.<ext>
│   │   ├── <AAAA>/
│   │   │   └── <MM>/
│   │   │       ├── bank-statements/           # toujours un dossier (multi-comptes possibles)
│   │   │       │   └── <AAAA-MM>_<BanqueOuCompte>.<ext>
│   │   │       ├── invoices/
│   │   │       │   ├── in/                    # factures reçues (achats)
│   │   │       │   │   └── <AAAA-MM-JJ>_<Émetteur>_<MontantTTC>.<ext>
│   │   │       │   └── out/                   # factures émises (ventes)
│   │   │       │       └── <AAAA-MM-JJ>_<Destinataire>_<MontantTTC>.<ext>
│   │   │       ├── notes-de-frais/
│   │   │       │   └── <AAAA-MM-JJ>_<Collaborateur>_<Émetteur>_<MontantTTC>.<ext>
│   │   │       ├── autres/
│   │   │       │   └── <AAAA-MM-JJ>_<Description>.<ext>
│   │   │       ├── relances.md                # maintenu par skill `relances`
│   │   │       └── followup.md                # maintenu par skill `facturation`
│   │   ├── _archive-suppression/              # RGPD soft-delete (grâce 30 j)
│   │   ├── index.json                         # index par client
│   │   └── audit.log                          # déplacements / renommages
│   └── index-global.json
├── .pending-attribution/                      # parking technique HORS clients/
│   ├── <AAAA-MM-JJ-réception>_<hash-court>.<ext>
│   └── pending-attribution.json
└── clients.json
```

### Pas de slug réservé dans `clients/`

Tout dossier sous `clients/` correspond à un client réel — existant ou auto-créé en `draft-auto-created`. Aucune entité technique (`_cabinet`, `_non-attribue`, etc.) ne pollue cet arbre.

### `.pending-attribution/`

Parking technique pour les documents que la cascade d'identification n'a pas su attribuer (expéditeur générique sans signal exploitable). Vit à la racine du workspace, **hors** `clients/`.

| Élément                          | Rôle                                                                              |
| -------------------------------- | --------------------------------------------------------------------------------- |
| `<date-réception>_<hash>.<ext>`  | Le fichier physique, renommé pour la traçabilité (pas le filename d'origine)      |
| `pending-attribution.json`       | Métadonnées extraites partielles + question à poser à l'utilisateur               |

Une fois la réponse utilisateur reçue (« rattacher à `acme-sa` » ou « créer client `nouveau-client` »), le fichier est **déplacé** vers son chemin cible définitif dans `clients/<slug>/…` et l'entrée correspondante de `pending-attribution.json` est purgée.

---

## Mapping `categorie` → dossier

| `categorie`      | Dossier cible                            | Vocab comptable    | Niveau   |
| ---------------- | ---------------------------------------- | ------------------ | -------- |
| `achat`          | `<AAAA>/<MM>/invoices/in/`               | Achats             | mois     |
| `vente`          | `<AAAA>/<MM>/invoices/out/`              | Ventes             | mois     |
| `bank-statement` | `<AAAA>/<MM>/bank-statements/`           | Relevés bancaires  | mois     |
| `note-de-frais`  | `<AAAA>/<MM>/notes-de-frais/`            | Notes de frais     | mois     |
| `contrat`        | `contrats/` (racine `<slug>/`)           | Contrats           | client   |
| `autre`          | `<AAAA>/<MM>/autres/`                    | Autres             | mois     |

L'enum machine est en kebab-case singulier (`achat`, pas `Achats`). Le vocab capitalisé pluriel est réservé aux **messages affichés au comptable** ; il n'apparaît jamais dans un chemin ni un payload.

---

## Conventions de nommage

### Slug client

- lowercase
- accents retirés (`é` → `e`, `ç` → `c`, etc.)
- espaces → `-`
- caractères non alphanumériques → `-`
- pas de `-` consécutifs, pas de `-` en début/fin
- dérivé du **domaine** de l'expéditeur, pas de l'email (`trendex.tech` → `trendex-tech`)

### Composants de nom de fichier

| Token            | Règle                                                                                                  |
| ---------------- | ------------------------------------------------------------------------------------------------------ |
| `AAAA-MM-JJ`     | `dateEmission` du document (ISO 8601), pas date de réception                                          |
| `AAAA-MM`        | `dateEmission` tronquée au mois — utilisé pour les relevés bancaires (couvre généralement un mois)    |
| `Émetteur`       | Raison sociale source, 10 premiers caractères significatifs, sans accents ni espaces (`Orange Pro` → `OrangePro`) |
| `Destinataire`   | Idem, pour les factures émises (`out/`) — c'est le client final du client du cabinet                  |
| `Collaborateur`  | Prénom ou prénom+initiale, sans accents (`Thomas`, `ThomasM`)                                         |
| `MontantTTC`     | Sans séparateur de milliers, point décimal, sans symbole (`348.50`, pas `348,50 €`)                   |
| `BanqueOuCompte` | Nom court de banque + suffixe compte optionnel (`BNP-courant`, `Qonto-pro`)                           |
| `Type` (contrat) | `MSA`, `NDA`, `Bail`, `CDI`, `Avenant`, etc. — vocabulaire court figé                                 |
| `Contrepartie`   | Slug ou raison sociale courte de l'autre partie au contrat                                            |
| `Description`    | Slug court décrivant le document quand aucune catégorie ne s'applique (`Statuts`, `KBis`, `Procuration`) |

### Séparateur

`_` entre composants. `-` à l'intérieur d'un composant. Jamais d'espace.

### Extension

Préservée du document source en lowercase (`.pdf`, `.jpg`, `.png`, `.eml`, `.csv`, `.ofx`, `.xml`).

---

## Cas spéciaux

### Multi-comptes bancaires

Un client peut avoir plusieurs comptes (courant, livret pro, devises). `bank-statements/` est toujours un dossier, jamais un fichier unique :

```
clients/acme-sa/2026/04/bank-statements/
├── 2026-04_BNP-courant.pdf
├── 2026-04_BNP-livret-pro.pdf
└── 2026-04_Qonto-usd.pdf
```

### Multi-pages relevé / cas hebdomadaires

Si un relevé couvre plusieurs périodes ou est fragmenté, suffixer avec la plage :

```
clients/acme-sa/2026/04/bank-statements/2026-04-01_2026-04-15_BNP-courant.pdf
```

### Contrats pluriannuels

Les contrats vivent à `<slug>/contrats/`, indexés sur la date de signature, pas la date de réception. Un avenant garde le même `<Type>` préfixé `Avenant-` :

```
clients/acme-sa/contrats/2024-01-15_MSA_TrendexTech.pdf
clients/acme-sa/contrats/2026-03-01_Avenant-MSA_TrendexTech.pdf
```

### Notes de frais — toujours rattachées à un client

Une note de frais appartient toujours à un client (celui dont l'employé doit être remboursé). L'émetteur du document est le commerçant (SNCF, restaurant…) ; le **bénéficiaire** — identifié dans le composant `<Collaborateur>` du nom — est l'employé d'un client.

```
clients/<client>/<AAAA>/<MM>/notes-de-frais/<AAAA-MM-JJ>_<Collaborateur>_<Émetteur>_<MontantTTC>.<ext>
```

Les frais perso de l'utilisateur lui-même **ne sont pas dans le scope** de ce skill. Si un document de ce type est détecté (typiquement : ticket envoyé depuis l'adresse perso de l'utilisateur, sans contexte client) → traité comme `non attribuable` → `.pending-attribution/`.

### Documents non datables

Si `dateEmission` est introuvable ET non déductible (carte de visite, capture d'écran, etc.) → date de réception en fallback, et alerte `extraction_incomplete`. Décision auto-rétrogradée à `needs_review`.

### Reclassement (correction d'un mauvais classement)

Quand le comptable corrige une attribution (mauvais client, mauvaise catégorie), le skill :

1. Déplace le fichier vers le nouveau chemin (sans renommage si le nouveau nom est identique).
2. Met à jour `index.json` des deux clients concernés (ancien + nouveau).
3. Logue l'opération dans `audit.log` du nouveau client avec `motif: reclassement-manuel`.
4. Ne touche jamais à `_archive-suppression/` (la suppression est un autre flux).

---

## `relances.md` — schéma

> Maintenu par le skill `relances`. Lu par `organisation-documents` en cas de classement d'une réponse à relance.

Un fichier par mois et par client : `clients/<slug>/<AAAA>/<MM>/relances.md`.

**Contenu** — un fichier = deux tableaux markdown :

```markdown
# Relances — <Raison sociale client> — <AAAA>/<MM>

> Maintenu par le skill `relances`. Toute modification manuelle est tolérée mais peut être écrasée à la prochaine exécution.

## À envoyer

| Date prévue | Facture       | Destinataire | Montant TTC | Échéance dépassée | Canal | Type   | Statut    |
| ----------- | ------------- | ------------ | ----------- | ----------------- | ----- | ------ | --------- |
| 2026-05-15  | F-2026-04-012 | TrendexTech  | 2 400,00 €  | 15 j              | email | R1     | planifiée |
| 2026-05-30  | F-2026-04-012 | TrendexTech  | 2 400,00 €  | 30 j              | email | R2     | planifiée |

## Effectuées

| Date envoi | Facture       | Destinataire | Montant TTC | Canal   | Type | Réponse client | Suite             |
| ---------- | ------------- | ------------ | ----------- | ------- | ---- | -------------- | ----------------- |
| 2026-04-15 | F-2026-03-008 | ACME Corp    | 1 248,00 €  | email   | R1   | promesse 15/05 | R2 planifié 30/05 |
| 2026-04-30 | F-2026-03-005 | Foo SAS      | 850,00 €    | courrier | R3   | aucune         | escalade huissier |
```

**Colonnes obligatoires** — toute autre colonne est facultative.

**Règles d'écriture** :

- Le skill `relances` est seul autorisé à modifier ces fichiers. `organisation-documents` les lit uniquement.
- L'ordre des lignes dans `À envoyer` : chronologique croissant (la prochaine en haut).
- L'ordre des lignes dans `Effectuées` : chronologique décroissant (la plus récente en haut).
- Quand une relance planifiée est envoyée, le skill `relances` la migre de `À envoyer` vers `Effectuées` dans le fichier du mois courant (pas du mois de la facture).

---

## `followup.md` — schéma

> Maintenu par le skill `facturation`. Lu par `organisation-documents` en cas de classement d'une facture entrante (paiement) ou sortante (émise).

Un fichier par mois et par client : `clients/<slug>/<AAAA>/<MM>/followup.md`.

```markdown
# Followup factures — <Raison sociale client> — <AAAA>/<MM>

> Maintenu par le skill `facturation`. Vue mois en cours.

## À émettre

| Date prévue | Destinataire | Description        | Montant TTC prévu | Statut         |
| ----------- | ------------ | ------------------ | ----------------- | -------------- |
| 2026-04-01  | TrendexTech  | Forfait avril      | 2 400,00 €        | à préparer     |
| 2026-04-15  | ACME Corp    | Prestation projet X | 5 800,00 €        | brouillon prêt |

## Émises ce mois

| Date émission | N° facture    | Destinataire | Montant TTC | Échéance   | Statut paiement | Prochaine relance |
| ------------- | ------------- | ------------ | ----------- | ---------- | --------------- | ----------------- |
| 2026-04-01    | F-2026-04-012 | TrendexTech  | 2 400,00 €  | 2026-04-30 | non payée       | R1 le 2026-05-15  |
| 2026-04-15    | F-2026-04-013 | ACME Corp    | 5 800,00 €  | 2026-05-15 | partielle (50%) | suivi 2026-05-15  |
| 2026-04-22    | F-2026-04-014 | Foo SAS      | 720,00 €    | 2026-05-22 | payée 2026-04-28 | —                |
```

**Statut paiement** — enum : `non payée` | `partielle` | `payée` | `litige` | `irrécouvrable`.

**Mise à jour automatique** — quand `organisation-documents` classe un relevé bancaire dans `bank-statements/`, il devrait théoriquement déclencher un rapprochement (`rapprochement-bancaire` skill) qui mettra à jour `followup.md` avec les paiements détectés. Hors scope de ce skill, mais le contrat de chemin est figé ici pour permettre l'intégration.

---

## Pourquoi cette structure

| Décision                                    | Alternative rejetée                          | Raison                                                                                  |
| ------------------------------------------- | -------------------------------------------- | --------------------------------------------------------------------------------------- |
| `<AAAA>/<MM>/` (deux niveaux)               | `<AAAA-MM>/` (un niveau)                     | Conservation 10 ans = 120 dossiers à plat ingérables sur Drive/Finder                   |
| `invoices/in` + `invoices/out` séparés      | `invoices/` unique                           | TVA et PCG différents — un compta ne mélange jamais                                     |
| `contrats/` à la racine client              | `contrats/` au mois                          | Contrats pluriannuels — les enterrer dans un mois rend la lecture impossible            |
| `bank-statements/` toujours un dossier      | Fichier `bank-statement.pdf` direct          | Multi-comptes très courant, dossier dès le départ évite la migration                    |
| `relances.md` + `followup.md` au mois       | Fichier rolling à la racine client           | Le comptable raisonne par mois (clôtures) — état mensuel plus utile que log global      |
| Slug dérivé du domaine                      | Slug dérivé de l'email                       | 1 client = N employés = N emails — mais 1 dossier client                                |
| Aucun slug réservé dans `clients/`          | `_cabinet` + `_non-attribue` pseudo-clients   | Un slug = un client réel. Le reste vit dans `.pending-attribution/` hors `clients/`.   |
| Auto-création par défaut                    | Toujours demander à l'utilisateur            | Trop interruptif au quotidien. Confirmation opt-in via `clientCreation: "confirm"`.    |
| Enum `categorie` kebab-case singulier       | Capitalisé pluriel                           | Aligné sur les noms de dossiers (`invoices/in` etc.) — pas de mismatch machine/affiché |
