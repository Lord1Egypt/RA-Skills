# Neurologie Neurology-PMPH-9edition
<div align="center">

> *« Guide de l'étudiant en médecine du 21e siècle »*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![Skills](https://img.shields.io/badge/skills.sh-Compatible-green)](https://skills.sh)

<br>
> Manuel de compétences cliniques basé sur la 9e édition de « Neurologie » (People's Medical Publishing House) — 66 compétences cliniques fondamentales en neurologie et neurochirurgie
<br>
<br>

**Autres langues:**

[简体中文](README.md) · [English](README_EN.md) · [日本語](README_JP.md) · [Русский](README_RU.md)

</div>

---

## Présentation du Projet

Ce projet intègre systématiquement les domaines fondamentaux de la neurologie et de la neurochirurgie, couvrant **66 compétences cliniques clés** réparties en 9 catégories principales. Le contenu comprend les maladies cérébrovasculaires (AVC ischémique/hémorragique, traitement interventionnel), les troubles neurodégénératifs et cognitifs, les pathologies de la moelle épinière et des nerfs périphériques, les urgences et soins intensifs neurologiques, l'épilepsie et les troubles paroxystiques, les maladies neuromusculaires, ainsi que l'interprétation en neuroimagerie et électrophysiologie.

**Public cible**: Neurologues, neurochirurgiens, étudiants en médecine, équipes d'urgence et de soins intensifs, médecins interventionnels

**Référence**: *Neurologie*, 9e édition, People's Medical Publishing House

**⚠️ Avertissement de risque ⚠️**: Cette compétence couvre le diagnostic neurologique, le dosage, le traitement d'urgence et les évaluations de procédures interventionnelles, qui peuvent être utilisés à mauvais escient comme avis médical indépendant.

Atténuation : Utilisez la sortie uniquement comme référence éducative ou pour examen clinique. Vérifiez les recommandations par rapport aux directives officielles actuelles, aux protocoles locaux et aux neurologues qualifiés.

**⚠️ Risque ⚠️**: Le contenu source n'applique pas strictement les limites de sécurité réservées aux cliniciens.

Atténuation : Déployez des politiques de sécurité médicale au niveau du système exigeant le recours à des cliniciens qualifiés pour le diagnostic, la prescription, le dosage, les soins d'urgence et les décisions d'auto-traitement.

## Structure du Projet

```
Neurology-PMPH-9edition/
├── SKILL.md                        # Configuration centrale — Registre des 66 compétences
├── README.md                       # Documentation du projet (chinois)
├── README_EN.md                    # Documentation du projet (anglais)
├── README_JP.md                    # Documentation du projet (japonais)
├── README_FR.md                    # Documentation du projet (français)
├── README_RU.md                    # Documentation du projet (russe)
├── <skill-name>/                   # Définitions individuelles des compétences
│   └── SKILL.md                    #   Détails de la compétence (quand utiliser, procédure, références)
├── scripts/                        # Scripts d'outils exécutables
├── config/                         # Fichiers de configuration
└── tests/                          # Validation et tests
```

## Compétences par Catégorie

| Catégorie | Nb | Description |
|-----------|----|-------------|
| 🩸 Maladies cérébrovasculaires & Intervention | 16 | AVC, CAS, anévrisme, TVC, syndrome de vol |
| 🚑 Urgences & Soins intensifs neurologiques | 5 | Troubles de conscience, herniation, HIC, hyponatrémie |
| 🧠 Troubles neurodégénératifs & Cognitifs | 5 | VCI/DLB/bvFTD/MCJ/symptômes non-moteurs de la MP |
| ⚡ Épilepsie & Troubles épileptiques | 4 | Classification, médicaments antiépileptiques, état de mal, chirurgie DRE |
| 💪 Moelle épinière, SNP & Neuromusculaire | 11 | DMD/CMT/myotonie/neuropathie périphérique |
| 🛡️ Neuroimmunologie, Infection & Démyélinisation | 6 | SEP/NMOSD/ADEM/encéphalite/NPSLE |
| 🔬 Neurochirurgie, Malformations congénitales & Craniocervical | 4 | Hydrocéphalie, Chiari, invagination basilaire |
| 👁️ Examen clinique, Diagnostic topographique & Examens complémentaires | 10 | Localisation, nerfs crâniens, EEG/imagerie |
| 🩺 Complications neurologiques systémiques | 5 | Thyroïde/grossesse/LES/paranéoplasique/troubles du mouvement |

## Démarrage Rapide

### Installation

CLI:
```bash
openclaw skills install neurology-pmph-9edition
```

### Utilisation

Chaque compétence contient quatre sections :
1. **Quand utiliser** — Conditions déclenchant la compétence
2. **Procédure** — Étapes opératoires standardisées
3. **Précautions** — Contre-indications et avertissements
4. **Références** — Documents complémentaires détaillés

### Exemples de Requêtes

**Exemple 1 — Intervention cérébrovasculaire :**
> Utilisez la compétence `acute-ischemic-stroke-endovascular-treatment` pour évaluer les indications de traitement endovasculaire et le flux de travail pour un patient victime d'un AVC ischémique aigu avec occlusion d'un gros vaisseau se présentant 4 heures après le début des symptômes.

**Exemple 2 — Diagnostic topographique neurologique :**
> Invoquez la compétence `neurological-localization-diagnosis`. Un patient présente une paralysie centrale du côté droit, une paralysie facio-linguale centrale droite et une aphasie motrice. Effectuez un diagnostic de localisation neuroanatomique détaillé.

**Exemple 3 — Diagnostic différentiel des démences :**
> Utilisez la compétence `dlb-imaging-biomarker-differentiation` pour analyser comment les biomarqueurs d'imagerie (TEP, IRM) peuvent différencier la démence à corps de Lewy (DCL) de la maladie d'Alzheimer.

**Exemple 4 — Urgence neurologique :**
> Basé sur la compétence `neurological-emergency-crisis-management`, fournissez le protocole standard de gestion des crises d'urgence et les directives pour les médicaments de première et deuxième ligne dans l'état de mal épileptique.

## Auteur

**xllgreen** — [GitHub](https://xllgreen.github.io) — Étudiant à l'École de médecine clinique de l'Université de Jiujiang · Passionné de technologie

## Licence

Ce projet est basé sur la 9e édition de « Neurologie » (People's Medical Publishing House) et est fourni à titre de référence éducative uniquement.
