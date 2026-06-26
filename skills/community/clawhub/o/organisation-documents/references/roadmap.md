# Référence — Tools, critères de succès, roadmap, questions ouvertes

> Référence chargée à la demande. Pas nécessaire à l'exécution courante du skill.

---

## Tools (sous-skills appelés)

| Tool                         | Skill source        | Rôle                                     |
| ---------------------------- | ------------------- | ---------------------------------------- |
| `nano_pdf.extract`           | `nano-pdf`          | OCR + extraction structurée des champs   |
| `gog.drive.upload`           | `gog`               | Dépôt du fichier au chemin cible         |
| `gog.drive.search`           | `gog`               | Vérification existence fichier           |
| `gog.gmail.fetch_attachment` | `gog`               | Récupération PJ depuis un message Gmail  |
| `agentmail.fetch_message`    | `agentmail`         | Idem côté AgentMail                      |
| `factures_doublons.check`    | `factures-doublons` | Test de doublons logiques                |
| `taskflow.schedule`          | `taskflow`          | Replanification si extraction incertaine |
| `1password.read`             | `1password`         | Récupération des creds Drive si besoin   |

---

## Critères de succès (à mesurer)

- **Taux de classement automatique** ≥ 85 % après 30 jours (hors documents non conformes / non attribuables).
- **Taux de doublon manqué** = 0 % (doublons certains détectés à 100 %).
- **Taux de mauvais classement** ≤ 2 % (correction manuelle par le comptable).
- **Délai de classement** < 60 s entre réception e-mail et fichier classé.

→ Métriques exposées par le skill via une commande `organisation-documents.stats` consommable par le dashboard mensuel.

---

## Roadmap d'implémentation

### v0.1 (MVP)

- Réception Gmail + AgentMail.
- Extraction `nano-pdf` (pas encore de Factur-X / UBL).
- Identification client par e-mail expéditeur uniquement.
- Classement `achat` / `vente` / `autre` dans la structure cible complète (`invoices/in`, `invoices/out`, `autres`).
- Création des dossiers `bank-statements/`, `notes-de-frais/`, `contrats/` vides au moment où ils deviennent pertinents (pas pré-créés).
- Lecture de `relances.md` / `followup.md` s'ils existent (pour rattacher paiements aux factures), pas d'écriture (hors scope).
- Mode draft pur.

### v0.2

- Validation des mentions obligatoires + référentiel embarqué.
- Détection client par SIREN et fuzzy raison sociale.
- Bascule auto post-14 jours.
- CSV consolidé.

### v0.3

- Support Factur-X (XML embarqué) + UBL.
- Mapping catégorie → compte PCG.
- Détection séquentialité numéros de facture (anti-fraude).
- Détection automatique `bank-statement` et `contrat` (mots-clés + structure), au-delà de la simple cascade émetteur ∈ clients.

### v0.4

- Notes de frais (OCR de tickets photo, classement par collaborateur).
- Relevés bancaires (CSV / OFX) → préparation rapprochement (`rapprochement-bancaire`).
- Reclassement bulk (correction comptable propage à toutes les pièces similaires).

---

## Questions ouvertes

1. **Reverse OCR sur les images natives** (ticket photo) : `nano-pdf` couvre-t-il, ou faut-il un fallback Tesseract local ?
2. **Multi-cabinet sur un même container** : confirmé hors scope (cf. `context.md` Q3) — on suppose 1 user = 1 cabinet.
3. **Migration existant** : si le comptable a déjà un Drive structuré différemment, on importe en l'état ou on re-classe ? → laisser le choix au comptable à l'onboarding.
4. **Stockage local vs Drive** : doublure complète sur disque LXD pour requêtes rapides, ou tout dans Drive et cache opportuniste ? Impact perf vs coût stockage.
5. **Format de l'index** : JSON suffit pour < 5 000 pièces / cabinet. Au-delà, basculer SQLite. Quel volume cible ?
