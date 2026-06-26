# Référence — Extraction & validation comptable française

> Référence chargée à la demande par `organisation-documents`. Détail des champs, des règles FR, des seuils, des doublons et des données embarquées.

---

## Champs cibles d'extraction

| Champ                    | Format attendu                                       | Obligatoire                |
| ------------------------ | ---------------------------------------------------- | -------------------------- |
| `emetteur`               | Raison sociale + SIREN si présent                    | ✅                         |
| `numeroFacture`          | Chaîne libre (peut contenir préfixe / suffixe)       | ✅                         |
| `dateEmission`           | ISO 8601 (`YYYY-MM-DD`)                              | ✅                         |
| `dateEcheance`           | ISO 8601                                             | ⚠️ recommandé              |
| `montantHT`              | Décimal, devise                                      | ✅                         |
| `tauxTVA`                | Liste (multi-taux possible)                          | ✅                         |
| `montantTVA`             | Décimal                                              | ✅                         |
| `montantTTC`             | Décimal                                              | ✅                         |
| `iban`                   | Format normalisé (mod 97)                            | ⚠️                         |
| `bicSwift`               | Format normalisé                                     | ⚠️                         |
| `mentionAutoliquidation` | bool                                                 | ⚠️ si TVA = 0              |
| `categorieOperation`     | `biens` / `services` / `mixte`                       | ✅ depuis 2026-09-01 (B2B) |
| `sirenClient`            | Si destinataire = client du cabinet                  | ✅ depuis 2026-09-01 (B2B) |
| `confidence`             | Score 0–1 agrégeant OCR + matching champs canoniques | ✅                         |

Si plusieurs montants détectés (cas multi-pages, rappels), ne retenir que les valeurs présentes en zone « total » du document. Sinon, marquer `extraction-incertaine` et escalader.

### Seuils sur `confidence`

- `≥ 0.85` → éligible auto-classement (si autres conditions OK).
- `0.70 – 0.85` → toujours en `needs_review`, même hors mode draft.
- `< 0.70` → alerte `low_confidence_extraction`, escalade systématique.

---

## Validation des mentions obligatoires (FR)

Vérifier la conformité de la facture aux mentions légales françaises :

- Présence des **3 mentions distinctes** : « description », « quantité », « prix unitaire ».
- Numéro de facture **séquentiel** (warning si trou détecté dans la séquence pour le même émetteur).
- Date d'émission présente et cohérente (≤ aujourd'hui, ≥ 1 an avant).
- TVA cohérente (`HT × taux = TVA`, tolérance `±0.01`).
- Si TVA = 0 → mention d'autoliquidation **ou** exonération **ou** franchise présente.
- Depuis 2026-09-01 (B2B) : SIREN du client + catégorie d'opération obligatoires.
- IBAN bien-formé (mod 97) si présent.

Référentiel embarqué : `assets/mentions-obligatoires.json` (structure inspirée de Paperasse `comptable/data/facturation/mentions-obligatoires.json`).

Sortie : score de conformité + liste des manquements. Si `manquements > 0`, le document est classé mais **flaggé** dans l'index (`statut-conformite: non-conforme`), avec notification au comptable.

---

## Catégorisation (nature du document)

L'enum `categorie` est aligné sur les dossiers cibles (cf. `structure-cible.md`).

Décision en cascade — première règle qui matche s'applique :

| Indice                                                                                                   | `categorie`      | Dossier cible              | Vocab comptable  |
| -------------------------------------------------------------------------------------------------------- | ---------------- | -------------------------- | ---------------- |
| Document de type relevé (mots-clés : « relevé », « extrait de compte », IBAN en en-tête sans n° facture) | `bank-statement` | `<AAAA>/<MM>/bank-statements/` | Relevés bancaires |
| Contrat (mots-clés : « contrat », « avenant », pas de montant TTC en clair)                              | `contrat`        | `contrats/` (racine client) | Contrats         |
| Émetteur = personne physique du cabinet ou d'un client                                                   | `note-de-frais`  | `<AAAA>/<MM>/notes-de-frais/` | Notes de frais   |
| `emetteur` ∈ clients du cabinet (le client a émis la facture à l'un de ses propres clients)              | `vente`          | `<AAAA>/<MM>/invoices/out/` | Ventes           |
| `emetteur` ∉ clients ET le client est destinataire                                                       | `achat`          | `<AAAA>/<MM>/invoices/in/`  | Achats           |
| Aucune correspondance                                                                                    | `autre`          | `<AAAA>/<MM>/autres/`       | Autres           |

**Ordre important** : `bank-statement` et `contrat` sont testés AVANT `vente`/`achat` car ils peuvent être émis par un client du cabinet sans être pour autant une vente (un relevé BNP avec émetteur = client ne doit pas atterrir dans `invoices/out/`).

**Précision `note-de-frais`** : l'émetteur du document est le commerçant (SNCF, restaurant…) ; ce qui qualifie en note de frais c'est le **bénéficiaire** (l'employé qui se fait rembourser) ou le contexte de réception (mail d'un collaborateur d'un client). Le slug du dossier est toujours celui du **client** qui emploie le bénéficiaire. Pour les frais perso de l'utilisateur lui-même → escalade vers `.pending-attribution/` (hors scope du skill).

---

## Détection de doublons

Au-delà du hash fichier (étape 1 du workflow principal), vérifier les doublons **logiques** dans l'index du client cible :

| Test                                                       | Verdict                           | Action                            |
| ---------------------------------------------------------- | --------------------------------- | --------------------------------- |
| Même `numeroFacture` + même `emetteur` + même `montantTTC` | `doublon-certain`                 | Skip classement, log au comptable |
| Même `emetteur` + même `montantTTC` + écart date < 7j      | `doublon-probable`                | Classer mais flagger pour revue   |
| Même hash fichier                                          | `doublon-fichier`                 | Stop avant traitement             |
| Tolérance arrondi : `abs(TTC1 - TTC2) < 0.01`              | (s'applique aux 2 premiers tests) | —                                 |

→ Réutilise la logique du skill `factures-doublons` quand il sera buildé. Pour l'instant, implémentation locale.

---

## Données embarquées

Dans `assets/` du skill :

- `mentions-obligatoires.json` — règles de conformité FR (référentiel inspiré de Paperasse, à versionner avec dates de validité).
- `pcg-2026.json` — Plan Comptable Général (utile pour mapping catégorie → compte PCG dans une v0.2).
- `tva-taux-fr.json` — taux de TVA en vigueur (5,5 / 10 / 20 / 0 / autoliquidation).
- `regex-siren-iban-tva-intra.json` — patterns d'extraction réutilisables.
