# Référence — Contrat d'invocation & sources

> Référence chargée à la demande par `organisation-documents`. Schémas JSON, sources acceptées, enum d'alertes, schéma de l'index.

---

## Sources acceptées

| Source             | Détection                                                 | Pré-traitement                                |
| ------------------ | --------------------------------------------------------- | --------------------------------------------- |
| Pièce jointe Gmail | Skill `gog` → push d'événement                            | Extraction de la PJ + métadonnées de l'e-mail |
| Adresse AgentMail  | Skill `agentmail` → webhook                               | Idem                                          |
| Lien Drive         | URL `https://drive.google.com/file/d/...` dans un message | Téléchargement via `gog`                      |
| Dépôt FS local     | Surveillance `~/.openclaw/workspace/inbox/`               | Lecture directe                               |
| Upload manuel UI   | API REST de l'agent                                       | Idem                                          |

### Formats de fichiers

PDF (texte ou scanné), JPG, PNG, HEIC, TIFF, e-mail `.eml` complet, Factur-X (PDF/A-3 + XML embarqué), UBL XML, CSV/OFX (relevés bancaires).

### Métadonnées de l'e-mail (si applicable)

Adresse expéditeur, sujet, date d'envoi, corps HTML. Utilisées pour deviner le client si non détectable depuis la pièce.

---

## Contrat JSON

### Input

```jsonc
{
  "email": {
    // optionnel : absent si dépôt FS / upload manuel
    "from": "compta@orange-pro.fr",
    "subject": "Facture F-2026-04-1287",
    "date": "2026-04-15T09:12:00Z",
    "body": "Bonjour, veuillez trouver ci-joint…",
    "messageId": "<abc@gmail>",
  },
  "attachments": [
    {
      "filename": "facture_orange_avril.pdf",
      "mimeType": "application/pdf",
      "path": "/var/lib/openclaw/inbox/staging/abc.pdf",
      "sizeBytes": 184320,
    },
  ],
  "source": "gmail|agentmail|drive|fs|upload",
  "mode": "draft|auto", // override explicite ; sinon dérivé du calendrier post-onboarding
  "clientHint": "acme-sa", // optionnel : déjà connu par l'appelant (ex : reclassement)
}
```

### Output

```jsonc
{
  "status": "processed",
  "documents": [
    {
      "filename": "facture_orange_avril.pdf",
      "decision": "auto_classify|needs_review|ignore",
      "reason": "client identifié + extraction 0.92 + conforme",
      "client": "acme-sa",
      "categorie": "achat", // enum : achat | vente | bank-statement | note-de-frais | contrat | autre
      "cheminCible": "clients/acme-sa/2026/04/invoices/in/2026-04-15_OrangePro_348.50.pdf",
      "metadata": {
        "emetteur": "Orange Pro",
        "destinataire": "ACME SA", // optionnel : peuplé pour categorie = vente
        "numeroFacture": "F-2026-04-1287",
        "dateEmission": "2026-04-15",
        "montantTTC": 348.5,
      },
      "confidence": 0.92, // 0–1, agrégat OCR + matching client
      "alerts": [],
    },
  ],
  "alerts": [], // alertes batch-level
}
```

---

## Enum `alerts[]`

Valeurs possibles (par document ou batch-level) :

- `email_non_pertinent` — pas de PJ ET pas de mots-clés comptables → ignoré dès le pré-filtre
- `client_inconnu` — aucune correspondance dans `clients.json`
- `extraction_incomplete` — un ou plusieurs champs obligatoires manquants
- `low_confidence_extraction` — `confidence < 0.7`
- `siren_client_manquant` — facture B2B post-2026-09-01 sans SIREN destinataire
- `tva_incoherente` — `HT × taux ≠ TVA` au-delà de la tolérance
- `duplicate_fichier` — hash identique déjà indexé
- `duplicate_metier` — même `numeroFacture` + `emetteur` + `montantTTC`
- `duplicate_probable` — même `emetteur` + `montantTTC` + écart date < 7j
- `mention_obligatoire_manquante` — au moins une mention légale FR absente
- `iban_invalide` — IBAN présent mais mod 97 KO
- `montant_aberrant` — TTC ≠ HT + TVA hors tolérance
- `date_future` — date d'émission postérieure à aujourd'hui
- `multi_clients_possibles` — plusieurs candidats clients à confiance proche

---

## Schéma d'une entrée d'index

Index par client (`~/.openclaw/workspace/clients/<slug>/index.json`) et global (`~/.openclaw/workspace/index-global.json`).

```jsonc
{
  "id": "uuid",
  "hashFichier": "sha256:...",
  "clientId": "acme-sa",
  "categorie": "achat", // enum : achat | vente | bank-statement | note-de-frais | contrat | autre
  "emetteur": "Orange Pro",
  "sirenEmetteur": "380129866",
  "destinataire": "ACME SA", // optionnel : peuplé pour categorie = vente | note-de-frais
  "numeroFacture": "F-2026-04-1287",
  "dateEmission": "2026-04-15",
  "montantHT": 290.42,
  "tva": [{ "taux": 20, "montant": 58.08 }],
  "montantTTC": 348.5,
  "cheminDrive": "clients/acme-sa/2026/04/invoices/in/2026-04-15_OrangePro_348.50.pdf",
  "cheminLocal": "/var/lib/openclaw/.../clients/acme-sa/2026/04/invoices/in/...",
  "statutConformite": "conforme",
  "manquements": [],
  "modeTraitement": "auto-validé",
  "validePar": null,
  "dateClassement": "2026-04-28T14:23:11Z",
  "sourceReception": "gmail|agentmail|drive|fs|upload",
  "messageIdSource": "...",
}
```
