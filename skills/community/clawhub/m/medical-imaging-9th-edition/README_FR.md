# Medical Imaging-9thEdition (Imagerie Médicale)
<div align="center">

> *「Guide d'Imagerie Médicale du 21e Siècle」*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![Skills](https://img.shields.io/badge/skills.sh-Compatible-green)](https://skills.sh)

<br>
> Un manuel de compétences cliniques basé sur la 9e édition d'Imagerie Médicale (Maison d'Édition Populaire de la Santé) — 136 compétences essentielles en diagnostic par imagerie et thérapie interventionnelle
<br>
<br>

Pourquoi lire tout un manuel ?<br>
Posez une question et obtenez automatiquement une solution tirée du manuel

<br>

**Autres langues / Other Languages:**

[中文](README.md) · [English](README_EN.md) · [日本語](README_JP.md) · [Русский](README_RU.md)

</div>

---

## Présentation du Projet

Ce projet intègre systématiquement les domaines fondamentaux du diagnostic par imagerie médicale, de la radiologie interventionnelle, de l'analyse assistée par IA et de la sélection de techniques d'imagerie multimodale, couvrant **136 compétences cliniques clés** organisées en 13 catégories.

**Public cible** : Radiologues, cliniciens de toutes spécialités, étudiants en médecine, équipes de radiologie interventionnelle, éducateurs médicaux

**Manuel de référence** : *Imagerie Médicale*, 9e édition, Maison d'Édition Populaire de la Santé

**⚠️ Risque ⚠️** : Cet ensemble de compétences couvre le diagnostic par imagerie, l'utilisation des produits de contraste, les indications thérapeutiques interventionnelles et l'interprétation des rapports, qui pourraient être utilisés à mauvais escient comme décisions diagnostiques ou thérapeutiques indépendantes.

Atténuation : Utilisez les résultats uniquement comme référence éducative ou pour examen par un clinicien, et vérifiez les recommandations par rapport aux directives officielles, protocoles locaux et spécialistes en radiologie qualifiés.

## Structure du Projet

```
Medical-Imaging-9thEdition/
├── SKILL.md              # Configuration centrale — registre des 136 compétences
├── README.md             # Documentation du projet
├── README_FR.md          # Documentation en français
├── <skill-name>/         # Définitions détaillées de chaque compétence
│   └── SKILL.md          #   Détails (quand utiliser, procédures, notes)
├── scripts/              # Scripts d'outils exécutables
├── config/               # Fichiers de configuration
├── tests/                # Vérification et tests
└── assets/               # Ressources statiques
```

## Aperçu des Compétences

| Catégorie | Nb | Description |
|-----------|----|-------------|
| 🏗️ Fondamentaux & Technologie | 9 | Principes RX, CT, IRM, écho, post-traitement, sécurité |
| 🤖 IA & Ressources Numériques | 5 | Analyse assistée par IA, workflows intelligents |
| 📚 Manuels & Programme | 3 | Vérification, révision, réforme curriculaire |
| 🧠 Système Nerveux Central | 7 | Traumatisme crânien, IRM médullaire, maladies démyélinisantes |
| 👁️ Tête & Cou | 4 | Orbite, parotide, mandibule |
| 🫁 Thorax & Cardiovasculaire | 18 | Poumon, plèvre, médiastin, imagerie cardiaque |
| 🫄 Sein & Gynécologie | 8 | Mammographie, tumeurs ovariennes, placenta praevia, UAE |
| 🫃 Système Digestif | 19 | Imagerie multimodale du tube digestif et hépatobiliaire |
| 🫘 Urinaire & Surrénales | 8 | Tumeurs rénales, classification kystique, lithiase |
| 🦴 Musculosquelettique | 10 | Fractures, tumeurs osseuses, ostéomyélite, articulations |
| 👶 Pédiatrie & Congénital | 4 | NRDS, LCH, invagination intestinale, rachitisme |
| 💉 Radiologie Interventionnelle | 19 | Voie vasculaire, embolisation, stents, ablation, TIPS |
| 📋 Diagnostic Intégré | 14 | Raisonnement diagnostique, interprétation, fusion multimodale |

## Guide de Démarrage Rapide

### Installation

CLI :
```bash
openclaw skills install medical-imaging-9th-edition
```

### Exemples d'Utilisation

**Question :**
```bash
Critères de la classification de Bosniak 2019 pour les kystes rénaux
```

**Réponse :**
```bash
## Classification de Bosniak des Kystes Rénaux (2019)

| Type | Caractéristiques | Risque Malin | Prise en charge |
|------|-----------------|--------------|-----------------|
| I | Kyste simple, paroi fine, pas de cloison | <1% | Bénin, pas de suivi |
| II | Peu (≤3) cloisons fines (≤2mm), fines calcifications | <5% | Bénin, pas de suivi |
| IIF | Multiples (≥4) cloisons fines, léger épaississement pariétal | ~10% | Surveillance |
| III | Composants solides rehaussés, paroi irrégulièrement épaisse (≥4mm) | ~55% | Résection chirurgicale |
| IV | Composants tissulaires nettement rehaussés | >90% | Résection chirurgicale |
```

## Licence

Ce projet est basé sur la 9e édition d'*Imagerie Médicale* (Maison d'Édition Populaire de la Santé) et est fourni à des fins de référence éducative uniquement.
