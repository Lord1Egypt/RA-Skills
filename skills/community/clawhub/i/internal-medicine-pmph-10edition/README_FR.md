# Internal Medicine — PMPH 10e édition
<div align="center">

> *« Guide de l'étudiant en médecine du XXIe siècle »*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![Skills](https://img.shields.io/badge/skills.sh-Compatible-green)](https://skills.sh)

<br>
> Un manuel de compétences cliniques basé sur *Médecine Interne*, 10e édition, People's Medical Publishing House — 423 compétences cliniques fondamentales en médecine interne
<br>
<br>
<img src="assets/Internal-Medicine.jpg" width="260px">
<br>

Pourquoi peiner à lire un manuel entier ?<br>
Il suffit de poser une question pour obtenir une solution directement tirée du manuel.

<br>

**Autres langues / Other Languages:**

[English](README_EN.md) · [简体中文](README.md) · [日本語](README_JA.md) · [Русский](README_RU.md)

</div>

---

## Présentation du projet

Ce projet intègre systématiquement les connaissances fondamentales de la médecine interne, couvrant **15 grandes catégories** — Maladies cardiovasculaires, Maladies respiratoires, Maladies digestives, Maladies endocriniennes et métaboliques, Maladies rénales, Maladies hématologiques, Maladies rhumatismales et immunitaires, Maladies infectieuses et tuberculose, Intoxications et lésions physico-chimiques, Oncologie et soins globaux, Gestion des maladies chroniques et soins hiérarchisés, Compétences et procédures cliniques, Pharmacothérapie et sécurité, Interprétation des examens de laboratoire et d'imagerie, et Ressources pédagogiques et contrôle qualité — pour un total de **423 compétences cliniques clés**.

**Public cible** : Médecins internistes, généralistes, urgentistes, étudiants en médecine, résidents en formation standardisée

**Manuel de référence** : *Médecine Interne*, 10e édition, People's Medical Publishing House

**⚠️ Risque ⚠️** : Les traitements, procédures et posologies à haut risque peuvent ne pas convenir à une installation générale ou à une utilisation non supervisée.

**Mesure d'atténuation** : Destiné aux cliniciens qualifiés, aux environnements d'enseignement médical supervisé ; nécessite une révision par un clinicien avant d'appliquer toute sortie.

**⚠️ Risque ⚠️** : Les recommandations peuvent entrer en conflit avec les directives locales en vigueur, les protocoles institutionnels ou les contre-indications spécifiques au patient.

**Mesure d'atténuation** : Vérifier que les plans, procédures, seuils et plans de suivi sont conformes aux dernières normes locales et politiques institutionnelles avant utilisation.

**⚠️ Risque ⚠️** : Les procédures invasives en situation d'urgence, les ajustements de protocoles de chimiothérapie et les décisions sensibles de fin de vie peuvent compromettre la sécurité ou la vie privée du patient si elles sont traitées trop cavalièrement.

**Mesure d'atténuation** : Ajouter des avertissements explicites pour ces scénarios, orienter les urgences vers les soins aigus, et limiter l'accès aux utilisateurs ayant des besoins cliniques ou éducatifs supervisés appropriés.

## Structure du projet

```
Internal-Medicine-PMPH-10edition/
├── SKILL.md                  # Configuration centrale — registre des 423 compétences
├── README.md                 # Ce document — description du projet et guide d'utilisation
├── <skill-name>/             # Définitions détaillées de chaque compétence
│   └── SKILL.md              #   Détails de la compétence (indications, procédure, références)
├── scripts/                  # Scripts utilitaires exécutables
│   ├── list-skills.sh        #   Recherche par mot-clé de compétence
│   └── build-index.py        #   Générateur d'index de compétences
├── config/                   # Fichiers de configuration
│   └── skills-index.json     #   Index JSON des 423 compétences
└── tests/                    # Validation et tests
```

## Aperçu des catégories de compétences

| Catégorie | Compétences | Description |
|-----------|-------------|-------------|
| ❤️ Maladies cardiovasculaires | 56 | Coronaropathie, insuffisance cardiaque, arythmies, cardiomyopathie, HTA, valvulopathies, etc. |
| 🫁 Maladies respiratoires | 45 | Pneumonie, BPCO, asthme, embolie pulmonaire, pneumopathie interstitielle, pleurésie, etc. |
| 🫃 Maladies digestives | 50 | Gastrite, ulcère, MICI, cirrhose, pancréatite, ascite, etc. |
| 🧬 Maladies endocriniennes et métaboliques | 46 | Diabète, thyroïdopathies, maladies hypophyso-surrénaliennes, goutte, troubles électrolytiques, etc. |
| 🫘 Maladies rénales | 29 | Glomérulonéphrite, insuffisance rénale, dialyse, protéinurie, IRA, etc. |
| 🩸 Maladies hématologiques | 37 | Leucémie, anémie, troubles de la coagulation, myélome multiple, lymphome, SMD, etc. |
| 🦿 Maladies rhumatismales et immunitaires | 12 | PR, LED, syndrome de Gougerot-Sjögren, sclérose systémique, vascularite, etc. |
| 🦠 Maladies infectieuses et tuberculose | 20 | Infections communautaires, infections nosocomiales, tuberculose, infections fongiques, hépatites virales, etc. |
| 💊 Intoxications et lésions physico-chimiques | 15 | Intoxication médicamenteuse, solvants organiques, CO, coup de chaleur, noyade, etc. |
| 🎗️ Oncologie et soins globaux | 18 | Cancer du poumon, gastrique, colorectal, pancréatique, marqueurs tumoraux & thérapie ciblée, etc. |
| 📋 Gestion des maladies chroniques et soins hiérarchisés | 20 | Gestion hiérarchisée de l'HTA, suivi du diabète, gestion de la dyslipidémie, etc. |
| 🔬 Compétences et procédures cliniques | 25 | Ponction pleurale, ponction abdominale, ponction médullaire, RCP, défibrillation, etc. |
| 💉 Pharmacothérapie et sécurité | 20 | Gestion des anticoagulants, usage rationnel des antibiotiques, usage standardisé des glucocorticoïdes, etc. |
| 📡 Interprétation des examens de laboratoire et d'imagerie | 15 | Analyse ECG, échocardiographie, gaz du sang, interprétation des examens biologiques, etc. |
| 📚 Ressources pédagogiques et contrôle qualité | 15 | Structure du manuel, révision du programme, points d'examen essentiels, raisonnement clinique, etc. |

## Démarrage rapide

### Installation

CLI :
```bash
openclaw skills install internal-medicine-pmph-10edition
```

Prompt :
```bash
Avant d'installer quoi que ce soit, inspectez les métadonnées et les exigences de configuration de la compétence sur ClawHub.
Si la compétence vous demande d'installer un package ou un CLI tiers, vérifiez sa source, son mainteneur et le contenu du package avant d'exécuter la commande d'installation.
N'installez la compétence "Internal-Medicine-PMPH-10edition" (xllgreen/internal-medicine-pmph-10edition) depuis ClawHub qu'après ces vérifications.
Page de la compétence : https://clawhub.ai/xllgreen/internal-medicine-pmph-10edition
Limitez votre travail à cette seule compétence.
Après l'installation, aidez-moi à terminer la configuration à partir des métadonnées vérifiées de la compétence.
Utilisez uniquement les métadonnées que vous pouvez vérifier depuis ClawHub ; n'inventez pas d'exigences manquantes.
Demandez avant d'apporter des modifications plus larges à l'environnement.
```

### Utilisation après installation
Donnez les instructions suivantes à l'agent :
```bash
Avant chaque réponse, veuillez consulter la compétence médicale correspondante pour vérifier les informations.
```

### Recherche de compétences

```bash
# Recherche par mot-clé
bash scripts/list-skills.sh search insuffisance cardiaque

# Liste des compétences
bash scripts/list-skills.sh list
```

### Mode d'emploi

Chaque compétence comprend quatre parties :
1. **Indications** — Quand déclencher cette compétence
2. **Procédure** — Étapes opérationnelles standardisées
3. **Précautions** — Contre-indications et avertissements
4. **Références** — Documents complémentaires détaillés

### Stratégies de questionnement

#### 1. **Concept**
Question :
```bash
Quelle est la définition de l'endocardite infectieuse en médecine interne ?
```
Réponse :
```bash
Définition selon Médecine Interne (10e édition) :
**L'endocardite infectieuse (EI)** est un syndrome clinique caractérisé par la formation de **végétations** sur l'endocarde, les valves cardiaques ou l'intima des grosses artères adjacentes, causée par l'invasion hématogène directe de micro-organismes pathogènes (bactéries, champignons, etc.). Les végétations sont composées de plaquettes, de fibrine, de micro-organismes pathogènes et de cellules inflammatoires.
Points clés :
- **Physiopathologie centrale** : Fixation des micro-organismes sur les surfaces valvulaires ou endocardiques lésées → formation de végétations
- **Sites de prédilection** : Valve mitrale > Valve aortique (prédominance gauche)
- **Triade clinique** : Fièvre + Souffle cardiaque + Phénomènes emboliques/vasculaires
- **Classification** : Aiguë vs subaiguë selon l'évolution ; EI sur valve native, prothétique, et droite selon le type de valve
```

#### 2. **Analyse de cas clinique**
Question :
```bash
Femme de 60 ans présentant une toux et une expectoration récurrentes depuis 25 ans, des palpitations, une dyspnée et un œdème intermittent des membres inférieurs depuis 3 ans, avec exacerbation récente accompagnée de frissons et de fièvre depuis 1 semaine. Examen : T 38°C, tachypnée, cyanose labiale, hypersonorité bilatérale à la percussion pulmonaire, râles crépitants dans les champs pulmonaires moyens et inférieurs, FC 110/min, rythme régulier, pas de souffle, œdème bilatéral sévère des membres inférieurs. Quel est le diagnostic ?
```
Réponse :
```bash
Il s'agit d'une progression classique de **BPCO → Cœur pulmonaire chronique → Insuffisance cardiaque droite**.
**Diagnostic complet :**
1. **Exacerbation aiguë de la Bronchopneumopathie Chronique Obstructive (BPCO)**
   - Arguments : 25 ans de toux chronique et d'expectoration + signes d'emphysème (hypersonorité) + exacerbation aiguë avec fièvre et tachypnée
2. **Cœur pulmonaire chronique (décompensé)**
   - Arguments : Terrain de BPCO + 3 ans de palpitations, dyspnée et œdème des jambes (suggérant une surcharge ventriculaire droite prolongée) + œdème bilatéral sévère actuel et cyanose labiale
**Chaîne physiopathologique :**
BPCO → Vasoconstriction pulmonaire hypoxique + réduction du lit capillaire pulmonaire → Hypertension pulmonaire → Augmentation de la post-charge du VD → Hypertrophie/dilatation du VD → Insuffisance cardiaque droite → Congestion systémique (œdème des jambes, cyanose)
**Diagnostic différentiel :**
- Rythme régulier, pas de souffle → Élimine une valvulopathie rhumatismale ou une fibrillation atriale comme cause de l'insuffisance cardiaque
- Œdème symétrique → Élimine une origine rénale (cette dernière se présente typiquement avec un œdème périorbitaire/facial)
```
#### 3. **Question d'examen**
Question :
```bash
Le site le plus fréquent de la tuberculose intestinale est :
A. Duodénum
B. Jéjunum
C. Région iléo-cæcale
D. Côlon transverse
E. Côlon sigmoïde
```
Réponse :
```bash
**C. Région iléo-cæcale**
C'est le site de prédilection le plus caractéristique de la tuberculose intestinale. Raisons :
- La région iléo-cæcale possède le tissu lymphoïde le plus abondant (plaques de Peyer), favorisant la colonisation par Mycobacterium tuberculosis
- Le péristaltisme plus lent et le temps de séjour plus long du contenu facilitent l'invasion bactérienne
Le diagnostic différentiel entre tuberculose intestinale et maladie de Crohn se concentre donc sur cette même région — des ulcères circonférentiels/irréguliers, une distribution localisée et une coloration acido-résistante positive dans la région iléo-cæcale orientent vers une tuberculose intestinale ; des ulcères longitudinaux, une distribution segmentaire et des fistules orientent davantage vers une maladie de Crohn.
```

## À propos de l'auteur

**xllgreen (https://xllgreen.github.io)** — Étudiant en médecine au Collège clinique de l'Université de Jiujiang · Passionné de technologie

## Support technique
<br>
Projet PDF2App : https://pdf2app.cn
<br>
Microsoft Visual Studio Code : https://code.visualstudio.com/
<br>
Claude Code pour VS Code : https://claude.com/
© 2026 Anthropic PBC
<br>
<br>
<img src="https://cdn.deepseek.com/logo.png?x-image-process=image%2Fresize%2Cw_1920" width="130px">
<br>API DeepSeek : https://platform.deepseek.com/
© 2026 Hangzhou DeepSeek Artificial Intelligence Fundamental Technology Research Co., Ltd. Tous droits réservés
<br>
<br>
<img src="https://cdn.cnbj1.fds.api.mi-img.com/aife/mimo-blog-fe/doc_build/static/image/logo.99baaffe.png" width="130px">
<br>API Xiaomi Mimo : https://platform.xiaomimimo.com/
Copyright © 2010 - 2026 Xiaomi. Tous droits réservés
<br>

## Licence

Le contenu de ce projet est compilé d'après *Médecine Interne*, 10e édition (PMPH) et est fourni à des fins d'apprentissage et de référence uniquement.

## Star History

<a href="https://www.star-history.com/?repos=Internal-Medicine-PMPH-10edition&type=date&legend=top-left">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chart?repos=Internal-Medicine-PMPH-10edition&type=date&theme=dark&legend=top-left" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chart?repos=Internal-Medicine-PMPH-10edition&type=date&legend=top-left" />
   <img alt="Star History Chart" src="https://api.star-history.com/chart?repos=Internal-Medicine-PMPH-10edition&type=date&legend=top-left" />
 </picture>
</a>
