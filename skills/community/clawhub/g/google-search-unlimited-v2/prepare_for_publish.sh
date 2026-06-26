#!/bin/bash
# Script pour préparer la publication du skill sur ClawHub

echo "=== Préparation de google-search-unlimited-v2 pour publication ==="
echo ""

# Vérifier la structure
echo "1. Vérification de la structure du skill..."
if [ ! -f "SKILL.md" ]; then
    echo "❌ Fichier SKILL.md manquant"
    exit 1
fi

if [ ! -f "_meta.json" ]; then
    echo "❌ Fichier _meta.json manquant"
    exit 1
fi

if [ ! -f "search.py" ]; then
    echo "❌ Fichier search.py manquant"
    exit 1
fi

echo "✅ Structure valide"
echo ""

# Vérifier les métadonnées
echo "2. Vérification des métadonnées..."
python3 -c "
import json
import sys

try:
    with open('_meta.json', 'r') as f:
        meta = json.load(f)
    
    required = ['name', 'version', 'description', 'author', 'license']
    for field in required:
        if field not in meta:
            print(f'❌ Champ {field} manquant dans _meta.json')
            sys.exit(1)
    
    print('✅ Métadonnées valides:')
    print(f'   Nom: {meta[\"name\"]}')
    print(f'   Version: {meta[\"version\"]}')
    print(f'   Description: {meta[\"description\"][:50]}...')
    print(f'   Auteur: {meta[\"author\"]}')
    print(f'   Licence: {meta[\"license\"]}')
    
except Exception as e:
    print(f'❌ Erreur: {e}')
    sys.exit(1)
"
echo ""

# Vérifier les dépendances
echo "3. Vérification des dépendances..."
if [ -f "requirements.txt" ]; then
    echo "✅ Fichier requirements.txt présent"
    echo "   Dépendances:"
    cat requirements.txt | while read line; do
        echo "   - $line"
    done
else
    echo "⚠️  Fichier requirements.txt manquant"
fi
echo ""

# Vérifier la documentation
echo "4. Vérification de la documentation..."
if [ -f "README.md" ]; then
    readme_lines=$(wc -l < README.md)
    echo "✅ README.md présent ($readme_lines lignes)"
else
    echo "⚠️  README.md manquant"
fi

if [ -f "SKILL.md" ]; then
    skill_lines=$(wc -l < SKILL.md)
    echo "✅ SKILL.md présent ($skill_lines lignes)"
    
    # Vérifier le frontmatter
    if head -1 SKILL.md | grep -q "---"; then
        echo "✅ Frontmatter détecté dans SKILL.md"
    else
        echo "⚠️  Frontmatter manquant dans SKILL.md"
    fi
fi
echo ""

# Vérifier les fichiers Python
echo "5. Vérification des fichiers Python..."
py_files=$(find . -name "*.py" -not -path "./__pycache__/*" | wc -l)
echo "✅ $py_files fichiers Python trouvés:"
find . -name "*.py" -not -path "./__pycache__/*" | while read file; do
    size=$(wc -l < "$file")
    echo "   - $(basename "$file") ($size lignes)"
done
echo ""

# Vérifier les tests
echo "6. Vérification des tests..."
if [ -f "quick_test.py" ]; then
    echo "✅ Suite de tests présente"
    echo "   Pour exécuter: python3 quick_test.py"
fi

if [ -f "test_real_search.py" ]; then
    echo "✅ Test d'intégration présent"
fi
echo ""

# Instructions pour la publication
echo "=== INSTRUCTIONS POUR LA PUBLICATION ==="
echo ""
echo "1. Se connecter à ClawHub:"
echo "   clawhub login"
echo ""
echo "2. Publier le skill:"
echo "   clawhub publish . --slug google-search-unlimited-v2 --name \"Google Search Unlimited v2\" --version 2.0.0"
echo ""
echo "3. Vérifier la publication:"
echo "   clawhub inspect google-search-unlimited-v2"
echo ""
echo "4. Optionnel - Ajouter des tags:"
echo "   clawhub publish . --slug google-search-unlimited-v2 --tags \"search,optimization,caching\""
echo ""
echo "=== PRÊT POUR LA PUBLICATION ==="
echo "Le skill est correctement structuré et prêt à être publié sur ClawHub."