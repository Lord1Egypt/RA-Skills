# li-bid-document-maker — Guide d'utilisation

> **Expert en appels d'offres** — Convertit automatiquement les documents d'appel d'offres en réponses professionnelles orientées selon les critères de notation

## Installation

```bash
clawhub install li-bid-document-maker
```

## Démarrage rapide

Après l'installation, déclenchez la compétence en disant l'une des phrases suivantes à votre assistant IA :

- "Créer une réponse à un appel d'offres"
- "Analyser cet appel d'offres et générer une soumission"
- "Préparer une offre"
- "Générer une réponse à cette RFP"

L'IA exécutera automatiquement un flux de travail en 6 étapes : **Analyser l'appel d'offres → Analyse stratégique → Générer le plan → Rédiger les chapitres → Contrôle qualité → Amélioration PDCA**

## Utilisation

### Méthode 1 : Télécharger un fichier

Glissez-déposez le document d'appel d'offres (PDF ou Word) dans le chat, puis dites :
> "Utilise li-bid-document-maker pour analyser ce document"

### Méthode 2 : Spécifier le chemin du fichier

> "Utilise li-bid-document-maker, le fichier d'appel d'offres est dans /projects/tender.pdf"

## Configuration requise

| Élément | Configuration |
|---------|--------------|
| OS | Windows 10/11, macOS, Ubuntu 20.04+ |
| Plateforme IA | Claude, OpenClaw, Hermes, ou tout LLM Agent prenant en charge les E/S de fichiers |
| Format de fichier | PDF (recherchable de préférence) ou Word (.docx) |
| Dépendances | `python-docx`, `PyPDF2` (pour le traitement des fichiers, optionnel) |

## Résultat

- Document de soumission complet (structure standard de 16 chapitres)
- Rapport d'amélioration de la qualité PDCA
- Correspondance des critères de notation avec les points attribués

## Flux de travail

```
Étape 1: Analyser l'appel d'offres  → Extraire les informations projet, spécifications techniques, critères
Étape 2: Analyse stratégique        → Analyse des pondérations, stratégie concurrentielle
Étape 3: Générer le plan           → Plan orienté notation (confirmation utilisateur requise)
Étape 4: Rédiger les chapitres     → Rédaction section par section
Étape 5: Contrôle qualité          → Vérification complète sur 6 dimensions
Étape 6: Amélioration PDCA         → 3 cycles d'amélioration automatique, puis livraison
```

## Licence

MIT-0
