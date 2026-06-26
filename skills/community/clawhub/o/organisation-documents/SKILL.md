---
name: organisation-documents
description: Skill central de l'assistant comptable. Réceptionne, classe et nomme automatiquement les documents comptables (factures, relevés bancaires) par client / année / mois / nature, et déduit clients.json depuis les relevés bancaires. À INVOQUER SYSTÉMATIQUEMENT et SANS DEMANDER L'AUTORISATION dès que (a) un e-mail arrive avec une PJ PDF/image, (b) un e-mail contient un mot-clé comptable (facture, invoice, reçu, paiement, TVA, total, acompte, avoir, relevé), (c) le comptable demande de traiter / classer / organiser un document, (d) un fichier est déposé dans l'inbox, (e) le comptable répond à une question d'identification de client. L'extraction et le classement sont faits par scripts/main.py + scripts/extract.py — aucun champ n'est jamais deviné à l'œil.
license: Interne — usage privé OpenClaw
---

# Skill `organisation-documents`

> Moteur d'entrée du domaine comptable. Réception → identification du client → classement → indexation → rapport.
> **Le travail réel est fait par `scripts/main.py`** (qui appelle `scripts/extract.py`). Ce skill = quand le lancer + comment dialoguer avec le comptable.

---

## ⚠️ Règle absolue — EXÉCUTION DU SCRIPT (non négociable)

**Pour chaque invocation, la SEULE action de classement correcte est d'exécuter la commande :**

```bash
python3 scripts/main.py <dossier_inbox> <racine_clients>
```

puis de lire `<racine_clients>/_report.json` et de le relayer au comptable.

### ❌ INTERDIT

- **Lire les PDFs un par un et classer à la main.** L'agent extrait les champs à l'œil de façon inconsistante (cas réels déjà observés : `invoice_id` = `"N"`, `"des"`, `"um-rix"` au lieu de `F1-2026-0001` ; `total_ttc` = `0.00` au lieu du vrai montant). Ces erreurs cassent ensuite tout le rapprochement de `rapprochement-bancaire`.
- **Dupliquer la logique du script en Python ad-hoc** dans une cellule / un sous-process inline. Le script EST la logique, il est déterministe, déjà testé. Le réimplémenter à chaque invocation est garanti de diverger.
- **Créer ou déplacer des fichiers dans `<racine_clients>/` à la main** (move, copy, write). C'est le script qui le fait.
- **Inventer un `invoice_id`** quand le PDF n'en contient pas de lisible. Si `extract.py` ne le trouve pas, le script écrit `SANS-NUM` ; n'essaie PAS de fabriquer mieux à partir du nom de l'émetteur ou de la description.

### ✅ OBLIGATOIRE

1. Exécuter la commande shell ci-dessus (et UNIQUEMENT ça pour la partie classement).
2. Lire le `_report.json` produit.
3. Relayer au comptable un résumé court + les questions d'onboarding si la section `questions` n'est pas vide.

### Si le script échoue

Signale l'erreur exacte (stderr) au comptable. **NE PAS** "rattraper" en classant manuellement — c'est précisément ce qui produit les filenames cassés. Si le binaire `pdftotext` manque (`poppler-utils` non installé), demande-le et stoppe.

> Pourquoi cette règle est aussi stricte : on a déjà eu plusieurs runs où l'agent a improvisé le classement et produit des `invoice_id` bidons (`N`, `des`, `um-rix`). À chaque fois, `rapprochement-bancaire` flagge ensuite des `facture_manquante` qui n'en sont pas, le comptable perd du temps à investiguer. Le script ne fait pas ces erreurs.

---

## Quand utiliser ce skill

Réflexe par défaut face à tout document entrant :

1. E-mail avec PJ → traitement immédiat.
2. Dépôt manuel dans l'inbox → idem.
3. Import en masse (ZIP, dossier) → idem.
4. Réponse du comptable à une question d'identification → reprise (étape 2 de l'onboarding).
5. Reclassement / correction → relancer le script.

Ne **pas** utiliser pour : FEC (→ `fec-parser`), relances (→ `relances`), rapprochement bancaire (→ `rapprochement-bancaire`).

---

## Exécution

```bash
python3 scripts/main.py <dossier_inbox> [<racine_clients>]
# racine_clients par défaut : ~/.openclaw/workspace/clients
```

Le script :

1. **Dédoublonne** par SHA-256 (ignore les fichiers déjà classés via `_index.json`).
2. **Extrait** chaque PDF avec `scripts/extract.py` (`pdftotext -layout` + règles déterministes). Aucun montant, numéro ou nom n'est inventé.
3. **Phase 1 — relevés bancaires d'abord** : le titulaire affiché en en-tête du relevé EST le client du cabinet (identité certaine) → crée/complète l'entrée `clients.json` (`statut: auto-from-bank-statement`), classe le relevé dans `<slug>/<AAAA>/<MM>/bank-statements/`.
4. **Phase 2 — factures** : pour chaque facture, compare émetteur et destinataire à `clients.json` (exact puis fuzzy ≥ 0.82).
   - un seul côté matche → c'est le client ; émetteur ≈ client → `invoices/out/`, destinataire ≈ client → `invoices/in/`.
   - aucun côté ne matche → `_a-identifier/` + une **question** dans le rapport (cf. onboarding ci-dessous).
   - les deux matchent → `_a-identifier/` + question (cas rare).
   - extraction incomplète (date ou montant TTC introuvable) → `_incomplet/` + ligne dans le rapport.
5. **Phase 3 — autres** : ni facture ni relevé reconnaissable → `_non-attribue/`.
6. Écrit `clients/clients.json`, `clients/_index.json`, `clients/_report.json`, et imprime un résumé.

**Après l'exécution**, lire `clients/_report.json` et :

- relayer au comptable un résumé court (nb de factures classées, nb de relevés, clients créés) ;
- si `_report.json → questions` n'est pas vide → poser ces questions au comptable (cf. format) ;
- si `_report.json → incomplete` n'est pas vide → signaler ces pièces ;
- pour chaque facture classée (hors `_a-identifier`/`_incomplet`), considérer le post-traitement `rapprochement-bancaire` déclenché (le batch repassera de toute façon).

---

## Identification du client — règle absolue

Trois signaux **fiables**, dans l'ordre (gérés par le script) :

1. **Relevé bancaire** : titulaire du compte → certitude.
2. **Mapping confirmé** : e-mail expéditeur ∈ `contacts[].email`, domaine ∈ `domains`, ou SIREN du document ∈ `siren` d'un client.
3. **Raison sociale fuzzy** ≥ 0.82 contre `clients.json` — seulement si **un seul** des deux côtés matche.

Si aucun signal fiable → **on ne devine pas**. Le document part en `_a-identifier/` et le comptable tranche une fois.

### Onboarding d'un expéditeur ambigu (le cas « Corse Plomberie »)

Une facture contient toujours deux entreprises (émetteur, destinataire). Quand aucune n'est connue — et qu'aucun relevé ne couvre l'une d'elles — le script ne choisit pas : il met la pièce dans `_a-identifier/` et ajoute une question.

**Étape 1 (automatique)** — la question apparaît dans `_report.json → questions` :

> « Document : facture `TUYO-2024-087` (348,50 € TTC). Émetteur « TUYO SARL », destinataire « Corse Plomberie ». Lequel est votre client ? »

L'agent la relaie au comptable. **Aucune écriture dans `clients.json`** à ce stade.

**Étape 2 (à la réponse du comptable)** — quand le comptable répond « c'est **X** » :

1. Ajouter/compléter l'entrée `clients.json` de X :
   ```json
   { "slug": "<slug X>", "raisonSociale": "X", "statut": "confirmed",
     "confiance": 1.0, "aValider": false,
     "siren": ["<si lisible sur la pièce>"], "contacts": [{"email": "<expéditeur>"}],
     "domains": ["<si e-mail pro>"], "sources": ["accountant-confirmation"] }
   ```
2. Relancer `python3 scripts/main.py clients/_a-identifier <racine_clients>` : avec X désormais dans `clients.json`, les pièces de `_a-identifier/` liées sont classées (sens in/out déterminé) et sortent du dossier.
3. Relayer le résultat.

À partir de là, tout document futur du même expéditeur (même e-mail) est attribué automatiquement.

### Si le comptable répond « aucune des deux »

Déplacer la pièce de `_a-identifier/` vers `_non-attribue/`. Pas de suivi comptable.

---

## `clients.json` — structure

```json
[
  {
    "slug": "corse-plomberie",
    "raisonSociale": "Corse Plomberie",
    "statut": "auto-from-bank-statement | confirmed",
    "confiance": 0.9,
    "aValider": false,
    "siren": ["812345678"],
    "contacts": [{ "email": "jeanmichel@gmail.com" }],
    "domains": ["corseplomberie.fr"],
    "sources": ["bank-statement"]
  }
]
```

Fichier **construit et maintenu par ce skill seul** (via `scripts/main.py` + ajouts manuels lors de l'onboarding). Aucun autre skill ne l'écrit. Le comptable ne l'édite pas à la main : il répond aux questions.

---

## Arborescence cible

```
clients/
├── clients.json                  ← liste des clients (déduite des relevés + confirmations)
├── _index.json                   ← sha256 → chemin classé (dédup)
├── _report.json                  ← rapport de la dernière exécution
├── _a-identifier/                ← factures dont le client n'est pas confirmé (onboarding en cours)
├── _incomplet/                   ← pièces dont l'extraction a échoué (date / montant manquant)
├── _non-attribue/                ← ni facture ni relevé exploitable
├── _cabinet/                     ← documents internes du cabinet
└── <slug>/
    └── <AAAA>/<MM>/
        ├── bank-statements/
        │   └── <AAAA-MM>_<banque>.pdf
        └── invoices/
            ├── in/
            │   └── <AAAA-MM-JJ>_<N°Facture>_<Contrepartie>_<MontantTTC>.pdf
            └── out/
                └── <AAAA-MM-JJ>_<N°Facture>_<Contrepartie>_<MontantTTC>.pdf
```

Convention de nom (produite par le script, jamais à la main) :
- `N°Facture` : numéro réel extrait du PDF (ex `F1-2026-0003`), alphanumérique+tirets ; `SANS-NUM` si absent.
- `Contrepartie` : 14 premiers caractères significatifs du nom de l'autre partie, sans accents/espaces.
- `MontantTTC` : point décimal, sans séparateur de milliers, sans symbole (ex `3336.78`).
- `AAAA-MM-JJ` : date d'émission du document.

---

## Détection facture vs relevé (rappel — implémenté dans `extract.py`)

- **Relevé bancaire** si : `RELEVÉ DE COMPTE`/`EXTRAIT DE COMPTE`/`ACCOUNT STATEMENT`, ou nom de banque + `RELEVÉ`, ou `Solde d'ouverture`/`Solde de clôture`. **Exception** : si le document contient aussi (`FACTURE`/`INVOICE`) ET (`SIRET`/`TVA`) → c'est une facture.
- **Facture** si ≥ 2 signaux parmi : `FACTURE`/`INVOICE`/`BON DE FACTURATION` · bloc `SIRET`/`TVA`/`SIREN` · bloc destinataire (`FACTURÉ À`/`DESTINATAIRE`/`BILL TO`) · `TOTAL HT`/`TOTAL TTC`/`NET À PAYER`.
- Sinon → `_non-attribue/`.

---

## Communication avec le comptable

- **Silence par défaut** : une ligne au début, une ligne à la fin. Pas de narration par étape.
- **Questions d'onboarding** : regroupées en fin de message, une par expéditeur ambigu, format « Document … — Émetteur « … », destinataire « … » — lequel est votre client ? ».
- **Vocabulaire interdit** : `pdftotext`, `regex`, `SHA-256`, `pipeline`, `extract.py`, chemins absolus système.
- **Vocabulaire métier** : facture, pièce, dossier client, mois en cours, classement, doublon, mention obligatoire, contrepartie.

---

## Garde-fous

- Aucune donnée ne quitte le container LXD.
- Conservation 10 ans minimum. Jamais de suppression — `_a-identifier/`, `_incomplet/`, `_non-attribue/` conservent les pièces.
- Sources externes en lecture seule.
- Le système ne **devine jamais** un montant, un numéro ou l'identité d'un client : signal fiable, sinon question. `_incomplet/` plutôt qu'une valeur inventée.

---

## Post-traitement

Pour chaque facture / relevé classé dans un vrai dossier client (pas `_a-identifier/` ni `_incomplet/`), le moteur d'état `rapprochement-bancaire` reprendra. Émettre :

```json
{ "trigger": "rapprochement-bancaire", "client": "<slug>" }
```

(Le batch repasse de toute façon sur tous les clients ; ce trigger ne fait qu'accélérer.)

Relances : ne jamais appeler directement. Produire au plus :

```json
{ "trigger_suggestion": "relances", "reason": "invoice status may require update" }
```

---

## Philosophie

```
organisation-documents = moteur d'entrée — classe les pièces, identifie les clients (relevé ou question), maintient clients.json
rapprochement-bancaire           = moteur d'état  — rapproche, reconstruit l'état comptable
relances               = moteur de décision différée
```

Le travail mécanique est dans les scripts. Ce skill décide *quand* les lancer et *comment* en parler au comptable.
