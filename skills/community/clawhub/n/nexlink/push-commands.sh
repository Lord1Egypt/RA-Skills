#!/bin/bash
# Comenzi pentru a face push la repository-ul NexLink
# Rulează aceste comenzi pe mașina ta locală

# 1. Clonează repository-ul
git clone https://github.com/asistent-alex/openclaw-nexlink.git
cd openclaw-nexlink

# 2. Copiază fișierele din skill-ul local
# Înlocuiește cu calea ta locală
SKILL_DIR="/home/adminul/.openclaw/skills/nexlink"
cp -r "$SKILL_DIR"/* .

# 3. Adaugă .gitignore dacă nu există
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class

# Environment variables (NEVER commit these!)
.env
.env.local
config.yaml
credentials.json

# IDE
.idea/
.vscode/
*.swp
EOF

# 4. Commit și push
git add .
git commit -m "Initial commit: NexLink Exchange skill"
git branch -M main
git push -u origin main

echo "Done! Repository: https://github.com/asistent-alex/openclaw-nexlink"