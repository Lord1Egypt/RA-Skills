# Advanced Human Writing & AI Humanizer

<p align="center"><img src="assets/logo.png" width="320" alt="Human Writing : écriture à la plume et code de terminal sur fond blanc chaud"></p>

> Une écriture assistée par IA plus naturelle : révision multilingue, travail par sections et contrôle de la cohérence des textes longs, avec des Skills et un plugin DSH.

**Recherches :** humaniser un texte IA, enlever le ton IA, écriture naturelle, révision de roman, cohérence narrative, audit de chapitres, cohérence des personnages, dialogues naturels, éviter le style de traduction, rédaction journalistique, relecture académique.

Ce dépôt fournit des instructions réutilisables et un compilateur léger de prompts. Il ne prétend ni déterminer l'auteur d'un texte ni contourner des détecteurs. Il sert à améliorer la précision, la continuité, la voix et la qualité éditoriale.

## Ce que le projet couvre

- Romans et fiction sérielle : personnages, relations, positions, objets, tenue, chronologie, dette d'interaction et voix de dialogue.
- Actualités, rapports, documents administratifs et textes scientifiques : attribution, terminologie, chiffres, citations, sources et portée des conclusions.
- Écriture multilingue : français, espagnol, portugais, anglais, chinois, japonais, arabe, latin et autres langues prises en charge par le modèle.
- Traduction et localisation : repère les calques, l'ordre syntaxique importé, les faux amis et la voix de traduction uniforme sans supprimer les références culturelles.
- Textes longs : découpe les romans, séries d'articles et rapports en blocs auditables puis réconcilie style, voix et faits entre sections.

Pour un roman d'au moins trois chapitres, `chunk-audit --book-level` ajoute une seule lecture de l'architecture d'ensemble après les blocs : choix, conséquences, évolution du conflit et déplacements temporels. Cette option ne s'active ni pour les rapports ni pour un chapitre isolé.

`verify` contrôle littéralement chiffres et citations ; `verify-fidelity --source original.md --candidate revision.md` localise les affirmations modifiées et demande une vérification du sens. La détection automatique des documents sérieux utilise plusieurs indices selon la langue ; précisez `--document-type` si le texte est trop court. Les exemples fournis ne constituent pas une validation indépendante par des locuteurs natifs.

## Démarrage rapide

```powershell
python -m humanwriting.cli humanize `
  --draft brouillon.md `
  --style fiction `
  --mode deep `
  --task "Révise le rythme sans lisser la voix établie des personnages."

python -m humanwriting.cli audit `
  --draft chapitre.md `
  --context bible-du-roman.md `
  --profile voice
```

Utilisez `--reference extrait-approuve.md` ou `--reference-style` seulement lorsqu'une référence explicite est fournie. Une référence apporte des traits de style, jamais des faits, des personnages ou des formulations à reproduire.

## Audit long et agents indépendants

Sur un long manuscrit, un modèle peut traiter certaines sections superficiellement. `chunk-audit` produit un paquet contrôlable : chaque bloc possède un corps unique, une courte entrée précédente en lecture seule et une ligne de base commune.

```powershell
python -m humanwriting.cli chunk-audit `
  --draft roman-complet.md `
  --style fiction `
  --outline bible-du-roman.md `
  --reference chapitres-approuves.md `
  --agent-mode deep `
  --output-dir audit-roman
```

Exécutez d'abord `00-baseline-prompt.md`. Les tâches ne dépendant que de `baseline` peuvent ensuite être distribuées en parallèle dans des conversations neuves ou des requêtes API séparées. Enregistrez chaque réponse à l'emplacement prévu sous `reports/`, décrit dans `agent-plan.json`.

```powershell
python -m humanwriting.cli verify-chunk-audit `
  --package-dir audit-roman
```

Chaque rapport doit contenir un **Coverage Receipt** indiquant le bloc, les unités relues, les constats et les parties non examinées. La réconciliation finale ne doit commencer que lorsque toutes les tâches requises sont complètes. Le mode `standard` fournit une revue complète par bloc ; `deep` ajoute une revue de prose paragraphe par paragraphe, une revue de dialogue lorsqu'il y en a, et une revue des preuves pour les documents sérieux avec sources explicites.

## Traduction naturelle et localisation

Activez `--translationese` uniquement pour une traduction ou une localisation explicitement demandée :

```powershell
python -m humanwriting.cli chunk-audit `
  --draft rapport-fr.md `
  --style news-report `
  --context plan-redactionnel.md `
  --source sources.md `
  --translationese `
  --agent-mode deep `
  --output-dir audit-rapport
```

Le module protège les noms, chiffres, citations, termes, attributions et degrés d'incertitude. Il n'invente ni accent, ni argot, ni mot étranger, ni stéréotype national.

## Chargement ciblé

Les modules ne sont pas tous chargés ensemble. Voix, registre, relations, continuité sérielle et espace physique nécessitent une preuve dans la demande ou le contexte. La protection des contenus factuels ne s'active automatiquement que pour les nouvelles, documents formels et textes académiques, juridiques ou techniques. Le mode profond est toujours explicite afin de maîtriser les tokens.

## Documentation principale

- [README in English](README.md)
- [README 中文](README.zh-CN.md)
- [README en español](README.es.md)
- [README em português](README.pt-BR.md)
- [Guide de cohérence des textes longs](docs/long-form-consistency.md)
- [Guide d'audit par étapes](docs/audit-pipeline.md)

## Licence

MIT. Voir [LICENSE](LICENSE).
