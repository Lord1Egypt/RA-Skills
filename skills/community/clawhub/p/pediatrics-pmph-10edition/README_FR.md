# Pédiatrie Pediatrics-PMPH-10edition
<div align="center">

> *« Guide de l'étudiant en médecine du 21e siècle »*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![Skills](https://img.shields.io/badge/skills.sh-Compatible-green)](https://skills.sh)

<br>
> Un manuel de compétences cliniques basé sur la 10e édition de « Pédiatrie » (PMPH) — 184 compétences cliniques pédiatriques essentielles
<br>
<br>

Pourquoi peiner à lire un manuel entier ?<br>
Posez simplement une question et trouvez instantanément la solution dans le manuel.

<br>

**Autres langues / Other Languages:**

[中文](README.md) · [English](README_EN.md) · [日本語](README_JP.md) · [Русский](README_RU.md)

</div>

---

## À propos du projet

Ce projet intègre systématiquement les domaines fondamentaux de la pédiatrie, notamment la néonatologie, la croissance et le développement de l'enfant, la prévention et le contrôle des maladies infectieuses, le diagnostic et le traitement des maladies génétiques et métaboliques, ainsi que les soins d'urgence et de réanimation. Il couvre **184 compétences cliniques clés** réparties en **15 catégories**.

**Public cible** : Pédiatres, Étudiants en médecine, Équipes de soins néonatals, Professionnels de santé publique, Internes en formation

**Manuel de référence** : « Pédiatrie » (People's Medical Publishing House, 10e édition)

**⚠️Risque⚠️** : Les traitements cliniques, procédures et conseils posologiques à haut risque peuvent ne pas convenir à une installation générale ou à une utilisation non supervisée.

**Atténuation** : Réservé aux pédiatres qualifiés, néonatologistes, réanimateurs pédiatriques ou environnements de formation médicale supervisée. Exiger un examen clinique avant d'appliquer les résultats.

**⚠️Risque⚠️** : Les recommandations peuvent entrer en conflit avec les directives locales actuelles, les protocoles institutionnels ou les contre-indications spécifiques au patient.

**Atténuation** : Vérifier que les plans, procédures, seuils et suivis sont conformes aux normes locales et politiques institutionnelles avant utilisation.

**⚠️Risque⚠️** : Les procédures d'urgence, interventions invasives, réanimation néonatale, calculs posologiques pédiatriques et sujets sensibles liés au développement/comportement peuvent compromettre la sécurité ou la vie privée du patient s'ils sont traités avec légèreté.

**Atténuation** : Ajouter des avertissements explicites pour ces scénarios, rediriger les urgences vers les soins d'urgence/réanimation et limiter l'accès aux utilisateurs ayant des besoins cliniques ou éducatifs supervisés appropriés.

## Structure du projet

```
Pediatrics-PMPH-10edition/
├── SKILL.md                  # Configuration centrale — registre des 184 compétences
├── README.md                 # Ce document — présentation et guide d'utilisation
├── <skill-name>/             # Définitions détaillées des compétences
│   └── SKILL.md              #   Détails de la compétence (quand l'utiliser, étapes, références)
├── scripts/                  # Scripts exécutables
│   └── .gitkeep
├── config/                   # Fichiers de configuration
│   └── .gitkeep
└── tests/                    # Validation et tests
    └── .gitkeep
```

## Catégories de compétences

| Catégorie | Compétences | Description |
|-----------|-------------|-------------|
| 👶 Néonatologie & Médecine périnatale | 18 | Ictère, SDR, hémolyse, hémorragie, ENN, ROP, DBP |
| 📏 Croissance, Développement & Nutrition | 18 | Évaluation de la croissance, diversification alimentaire, sommeil, micronutriments |
| 💉 Immunisation & Lutte anti-infectieuse | 20 | Calendrier vaccinal, rougeole, HFMD, tuberculose, Kawasaki |
| 🫁 Maladies respiratoires | 12 | Pneumonie, asthme, mycoplasme, bronchoscopie, gaz du sang |
| ❤️ Maladies cardiovasculaires | 10 | Classification des cardiopathies congénitales, insuffisance cardiaque, myocardite, critères de Duke |
| 🫃 Maladies digestives & hépatobiliaires | 12 | Invagination intestinale, Hirschsprung, MII, atrésie biliaire, RGO |
| 🫘 Maladies urinaires & rénales | 10 | Hématurie, néphrite, syndrome néphrotique, IRA, ART |
| ⚖️ Maladies endocriniennes & métaboliques | 13 | GHD, puberté précoce, hypothyroïdie, diabète, ACD |
| 🩸 Hématologie & Oncologie | 9 | PTI, AHAI, hémophilie, thalassémie, LCH |
| 🧠 Neurologie & Troubles du comportement | 12 | Épilepsie, convulsions fébriles, TDAH, SGB, myasthénie grave |
| 🚑 Urgences & Soins intensifs | 10 | RCP, traumatisme, noyade, insuffisance respiratoire, déshydratation |
| 🧬 Maladies génétiques & congénitales | 7 | Prévention à trois niveaux, classification génétique, CHARGE, DMD/BMD |
| 🔬 Examens complémentaires & Imagerie | 11 | LCR, PCU, HCS, rachitisme, IRM, échographie |
| 📚 Manuels & Médecine factuelle | 7 | Évaluation de l'autorité des manuels, principes de révision, littérature |
| 🏋️ Gestion globale de la santé | 9 | Exercice, alimentation, système immunitaire, posologie, examen physique |

## Démarrage rapide

### Installation

CLI :
```bash
openclaw skills install pediatrics-pmph-10edition
```

Prompt :
```bash
Before installing anything, inspect the ClawHub skill metadata and setup requirements.
If the skill asks you to install a third-party package or CLI, verify its source, maintainer, and package contents before running the install command.
Install the skill "Pediatrics-PMPH-10edition" from ClawHub only after those checks pass.
Keep the work scoped to this skill only.
After install, help me finish setup from verified skill metadata.
Use only the metadata you can verify from ClawHub; do not invent missing requirements.
Ask before making any broader environment changes.
```

### Rechercher une compétence

```bash
# Recherche par mot-clé
bash scripts/skill-search.sh ictère néonatal

# Générer un rapport des compétences
bash scripts/skill-report.sh
```

### Utilisation

Chaque compétence se compose de quatre sections :
1. **Quand l'utiliser** — Situations cliniques déclenchant cette compétence
2. **Étapes d'exécution** — Procédure opératoire standardisée
3. **Précautions** — Contre-indications et avertissements
4. **Références** — Documents complémentaires

### Stratégies de questionnement

#### 1. **Concept**

Question :
```bash
Concept de l'ictère physiologique du nouveau-né
```

Réponse :
```bash
## Concept de l'ictère physiologique du nouveau-né

**L'ictère physiologique du nouveau-né** est une élévation transitoire de la bilirubine sérique non conjuguée chez le nouveau-né, due aux caractéristiques uniques du métabolisme de la bilirubine. Il s'agit d'un processus bénin et auto-limitant qui se résout généralement sans intervention.

### Critères diagnostiques

| Paramètre | Nouveau-né à terme | Prématuré |
|-----------|-------------------|-----------|
| Apparition | J2–3 après la naissance | J3–5 après la naissance |
| Pic | J4–5 après la naissance | J5–7 après la naissance |
| Résolution | J5–7 après la naissance | J7–9 après la naissance |
| Bilirubine sérique maximale | < 221 μmol/L (12,9 mg/dL) | < 256 μmol/L (15 mg/dL) |
| Augmentation quotidienne | < 85 μmol/L (5 mg/dL) | < 85 μmol/L (5 mg/dL) |

### Diagnostic différentiel clé

- **Ictère physiologique** : Respecte la fenêtre temporelle et les seuils ; enfant en bonne santé apparente
- **Ictère pathologique** : Apparition < 24 h, taux excessifs, évolution prolongée, augmentation rapide, ou bilirubine directe élevée
- **Ictère au lait maternel** : Apparition à 1 semaine, pic à 2–3 semaines ; diminution significative après 3 jours d'arrêt de l'allaitement

### Prise en charge

Aucun traitement spécifique requis. Assurer une alimentation adéquate pour favoriser l'élimination du méconium. Si la BST approche le seuil d'intervention, évaluer la nécessité d'une photothérapie.

---

**Compétence associée :** [Évaluation du risque d'ictère néonatal et diagnostic d'ictère physiologique](neonatal-jaundice-risk-assessment-diagnosis/SKILL.md)
```

#### 2. **Analyse de cas clinique**

Question :
```bash
Nouveau-né à terme, 38 semaines d'âge gestationnel, accouchement par voie basse, poids de naissance 3,2 kg. Ictère cutané apparaissant dans les 24 heures suivant la naissance, s'aggravant rapidement. À 36 heures de vie, BST à 15 mg/dL, prédominance de bilirubine non conjuguée. Groupe sanguin maternel : O Rh(+) ; groupe sanguin du nouveau-né : A Rh(+). Quel est le diagnostic le plus probable ?
```

Réponse :
```bash
## Analyse du cas

**Diagnostic le plus probable : Maladie hémolytique du nouveau-né par incompatibilité ABO (MHN-ABO)**

### Éléments diagnostiques

| Caractéristique clinique | Signification |
|-------------------------|---------------|
| **Ictère dans les 24 heures** | Ictère pathologique — apparition trop précoce |
| **BST 15 mg/dL (257 μmol/L)** | Nettement au-dessus des valeurs physiologiques (pic < 12,9 mg/dL) |
| **Prédominance de bilirubine non conjuguée** | Compatible avec un ictère hémolytique |
| **Mère O + Enfant A** | Combinaison MHN-ABO la plus fréquente (IgG anti-A maternel traverse le placenta) |
| **Test de Coombs positif** | Preuve définitive d'hémolyse immunologique |

### Prise en charge

1. **Instaurer une photothérapie immédiatement** — lumière bleue à haute intensité (425–475 nm)
2. **Surveiller la BST q4–6h** — évaluer le besoin d'exsanguino-transfusion
3. **NFS + réticulocytes** — évaluer la sévérité de l'anémie
4. **IVIG 0,5–1 g/kg** — interrompre l'hémolyse
5. **Exsanguino-transfusion** — si BST ≥ seuil d'exsanguino-transfusion ou échec de la photothérapie

---

**Compétences associées :** [Évaluation du risque d'ictère néonatal et diagnostic](neonatal-jaundice-risk-assessment-diagnosis/SKILL.md) · [Stadification et diagnostic de l'encéphalopathie bilirubinique](bilirubin-encephalopathy-staging-and-diagnosis/SKILL.md)
```

#### 3. **Question d'examen**

Question :
```bash
Nourrisson de 8 mois, fièvre depuis 3 jours. Une éruption cutanée apparaît après la défervescence. Le diagnostic le plus probable est :
A. Rougeole
B. Rubéole
C. Exanthème subit (Roséole)
D. Scarlatine
E. Varicelle
```

Réponse :
```bash
**Réponse : C. Exanthème subit (Roséole)**

### Diagnostic différentiel

| Maladie | Relation fièvre-éruption | Caractéristiques de l'éruption | Autres signes |
|---------|------------------------|-------------------------------|---------------|
| A. Rougeole | Éruption **pendant** la fièvre | Maculopapules rouge foncé, extension céphalo-caudale | Taches de Koplik, coryza |
| B. Rubéole | Éruption **pendant** la fièvre | Maculopapules roses, visage → corps rapidement | Adénopathies rétro-auriculaires/occipitales |
| **✅ C. Roséole** | Éruption **après** défervescence | Maculopapules rosées, tronc → visage → membres, disparaît en 1–2 jours | Fièvre élevée (39–40°C), bon état général |
| D. Scarlatine | Éruption **pendant** la fièvre | Éruption érythémateuse punctiforme, lignes de Pastia | Langue framboisée, pharyngite |
| E. Varicelle | Éruption **pendant** la fièvre | Lésions centrifuges « quatre générations » : macule → papule → vésicule → croûte | Prurit intense |

### Pourquoi C ?

Indices clés dans la question :
- **8 mois** → âge le plus fréquent pour la roséole (6–18 mois)
- **Fièvre 3 jours, éruption après défervescence** → **« L'éruption apparaît après la disparition de la fièvre » est la caractéristique classique de la roséole**, distincte des autres maladies exanthémateuses
- Éruption rosée maculopapuleuse, débutant sur le tronc puis s'étendant → compatible avec le mode d'éruption de la roséole

### Prise en charge

Auto-limitante ; aucun traitement antiviral spécifique. Soins de support :
- Antipyrétiques pour la fièvre élevée (refroidissement physique, acétaminophène/ibuprofène)
- Assurer un apport hydrique adéquat
- Surveiller les convulsions fébriles

---

**Compétence associée :** [Diagnostic et prévention des maladies infectieuses pédiatriques](er-tong-chuan-ran-bing-zhen-duan-yu-fang-zhi/SKILL.md)
```

## À propos de l'auteur

**Xiaolvlyu (https://xllgreen.github.io)** — Étudiant en médecine au Jiujiang University College of Clinical Medicine · Passionné de technologie

## Support technique
<br>
Projet PDF2App : https://pdf2app.cn
<br>
Microsoft Visual Studio Code : https://code.visualstudio.com/
<br>
Claude Code for VS Code : https://claude.com/
© 2026 Anthropic PBC
<br>
<br>
<img src="https://cdn.deepseek.com/logo.png?x-image-process=image%2Fresize%2Cw_1920" width="130px">
<br>DeepSeek API : https://platform.deepseek.com/
© 2026 Hangzhou DeepSeek Artificial Intelligence Basic Technology Research Co., Ltd. Tous droits réservés
<br>
<br>
<img src="https://cdn.cnbj1.fds.api.mi-img.com/aife/mimo-blog-fe/doc_build/static/image/logo.99baaffe.png" width="130px">
<br>Xiaomi Mimo API : https://platform.xiaomimimo.com/
Copyright © 2010 - 2026 Xiaomi. All Rights Reserved
<br>

## Licence

Le contenu de ce projet est basé sur la 10e édition de « Pédiatrie » (PMPH) et est fourni à des fins de référence éducative uniquement.

## Star History

<a href="https://www.star-history.com/#">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=&type=date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=&type=date" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=&type=date" />
 </picture>
</a>
