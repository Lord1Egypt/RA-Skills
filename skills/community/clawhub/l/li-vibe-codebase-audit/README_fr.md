# 🔒 Vibe Codebase Audit - Guide d'Utilisation en Français

## 📋 Aperçu

**Vibe Codebase Audit** est un outil d'audit de sécurité complet conçu pour les bases de code générées par l'IA, avec intégration native d'agent, support multiprovider et analyse de sécurité des dépendances.

> 🎉 **NOUVEAUTÉ v2.0**: Audit natif d'agent (sans clé API), support multiprovider, analyse des dépendances, audit de configuration

---

## ⚡ Démarrage Rapide

### Méthode 1: Audit Natif d'Agent (Recommandé, Sans Configuration!)

```python
# Pas de clé API nécessaire! Utiliser directement le LLM de l'agent actuel
from vibe_audit_enhanced import vibe_audit_enhanced

result = await vibe_audit_enhanced(
    project_path=".",
    primary_provider="agent_llm"  # Utiliser le LLM de l'agent actuel
)
```

### Méthode 2: Avec Votre Clé API

```python
# Utiliser votre propre API OpenAI/Claude/Autre
result = await vibe_audit_enhanced(
    project_path=".",
    primary_provider="openai",  # ou "claude", "ollama", "deepseek"
    fallback_provider="claude"
)
```

### Méthode 3: Utilisation CLI

```bash
# Utiliser le LLM de l'agent (sans clé API)
python vibe_audit_enhanced.py /chemin/vers/projet --provider agent_llm

# Utiliser OpenAI
python vibe_audit_enhanced.py /chemin/vers/projet --provider openai

# Utiliser le modèle local Ollama
python vibe_audit_enhanced.py /chemin/vers/projet --provider ollama
```

---

## 🆕 Nouveautés dans v2.0

### 1. 🤖 Intégration Native d'Agent
- **Sans configuration** - Pas de clé API nécessaire
- Utilise la connexion LLM de votre agent actuel
- Intégration transparente avec OpenCode, Hermes, OpenClaw
- Coût réduit - tire parti de l'abonnement agent existant

### 2. 🔌 Support Multiprovider
- **Agent LLM** - Utiliser l'agent actuel (recommandé)
- **OpenAI** - GPT-4, GPT-4-turbo
- **Claude** - Claude-3 Sonnet/Opus
- **DeepSeek** - Alternative économique
- **Qwen/Tongyi** - Modèles Alibaba
- **Ollama** - Exécuter des modèles locaux (gratuit!)

### 3. 📦 Analyse de Sécurité des Dépendances
- Vérifier les vulnérabilités connues (CVE)
- Détecter les dépendances obsolètes
- Vérification de conformité des licences
- Support: npm, pip, maven, cargo, go mod

### 4. ⚙️ Vérifications de Sécurité de Configuration
- Détection de fichiers .env exposés
- Détection de mauvaise configuration CORS
- Détection du mode débogage
- Vérifications SSL

---

## 📊 Comparaison des Outils

| Outil | Vitesse | Précision | Fonctions | Clé API | Meilleur Pour |
|-------|---------|-----------|-----------|---------|---------------|
| `vibe_audit_enhanced` | Moyenne-Rapide | Élevée | Toutes | Optionnel | **Production** |
| `vibe_audit_scan` | Rapide | Moyenne | Basique | Non | Vérifications rapides |
| `vibe_audit_multi_model` | Lente | Maximale | Consensus AI | Oui | Projets critiques |
| `vibe_audit_incremental` | Très Rapide | Moyenne | Git-aware | Optionnel | CI/CD |

---

## 🌐 Configuration des Providers

### Agent LLM (Recommandé)
```python
# Sans configuration! Utiliser directement:
primary_provider="agent_llm"
```

### OpenAI
```bash
export OPENAI_API_KEY="sk-..."
```

### Claude
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

### Ollama (Local, Gratuit)
```bash
# Installer Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Télécharger le modèle
ollama pull llama2

# Utiliser dans l'audit
primary_provider="ollama"
```

---

## 🚨 Niveaux de Risque

| Niveau | Score | Action |
|--------|-------|--------|
| ✅ SÛR | 0 | Prêt à publier |
| 🟢 FAIBLE | 1-19 | Problèmes mineurs, révision recommandée |
| 🟡 MOYEN | 20-49 | Réviser et corriger avant publication |
| 🟠 ÉLEVÉ | 50-79 | Problèmes significatifs, corrections requises |
| 🔴 CRITIQUE | 80-100 | **NE PAS PUBLIER** |

---

## 🤝 Agents Supportés

- **OpenCode** - Compétence native
- **Hermes** - Plugin
- **OpenClaw** - Import de module
- **Clients MCP** - Support protocole

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/csmoove530/vibe-codebase-audit/issues)
- **Documentation**: Voir SKILL.md
- **Exemples**: Voir répertoire examples/

---

**Publiez en toute confiance. Auditez avec rigueur. Codez en paix.** 🚀
