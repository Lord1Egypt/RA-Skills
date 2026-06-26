# Browser Autonome — Guide Agent

## Deux outils disponibles

### 1. agent-browser (CLI, recommande pour la plupart des cas)
CLI Playwright complet. Navigate, click, fill, screenshot, sessions paralleles.

### 2. browser-use (Python, pour l'agent autonome avance)
Lib Python qui donne une boucle agent complete : l'agent decide quoi faire sur la page.
Venv: `/opt/browser-use/bin/python3`
CLI: `/usr/local/bin/browser-use`

## Outil principal: agent-browser (CLI Playwright)

Tu as acces a un browser headless complet via la commande `agent-browser`.

## Workflow standard

```bash
# 1. Ouvrir une page
agent-browser open "https://example.com"

# 2. Voir les elements interactifs (boutons, liens, inputs)
agent-browser snapshot -i

# 3. Cliquer sur un element (utilise les @refs du snapshot)
agent-browser click @e3

# 4. Remplir un formulaire
agent-browser fill @e2 "mon texte"

# 5. Attendre le chargement
agent-browser wait --load networkidle

# 6. Prendre un screenshot (pour analyse visuelle)
agent-browser screenshot /tmp/page.png

# 7. Extraire du texte
agent-browser get text @e1

# 8. Fermer
agent-browser close
```

## Recherche web avancee

```bash
# Ouvrir Google
agent-browser open "https://www.google.com/search?q=mon+sujet"

# Snapshot pour voir les resultats
agent-browser snapshot -i

# Cliquer sur un resultat
agent-browser click @e5

# Extraire le contenu de la page
agent-browser snapshot -c
```

## Scraping structure

```bash
# Naviguer
agent-browser open "https://site.com/products"

# Snapshot complet (pas que interactif)
agent-browser snapshot

# Extraire des donnees specifiques
agent-browser get text @e10
agent-browser get attr @e10 href

# Paginer
agent-browser click @e20  # bouton "Next"
agent-browser wait --load networkidle
agent-browser snapshot
```

## Sessions paralleles

```bash
# Deux browsers en parallele
agent-browser --session s1 open "https://site1.com"
agent-browser --session s2 open "https://site2.com"

# Travailler dans chaque session
agent-browser --session s1 snapshot -i
agent-browser --session s2 snapshot -i

# Lister les sessions actives
agent-browser session list
```

## Sauvegarder/restaurer une session (cookies, auth)

```bash
# Apres login
agent-browser state save /tmp/auth-site.json

# Restaurer plus tard
agent-browser state load /tmp/auth-site.json
agent-browser open "https://site.com/dashboard"
```

## browser-use (agent autonome Python)

Pour les cas ou tu veux un agent qui browse de maniere autonome (comme Manus) :
```python
# Script a executer via: /opt/browser-use/bin/python3 script.py
import asyncio
from browser_use import Agent, Browser
from langchain_anthropic import ChatAnthropic
import os

async def run():
    browser = Browser()
    llm = ChatAnthropic(model='claude-sonnet-4-20250514', api_key=os.environ['ANTHROPIC_API_KEY'])
    agent = Agent(
        task="Ta tache ici - ex: Trouver les prix de [produit] sur 3 sites et comparer",
        llm=llm,
        browser=browser,
    )
    result = await agent.run()
    await browser.close()
    return result

asyncio.run(run())
```

## Regles
- Toujours `snapshot -i` apres navigation pour voir les nouveaux refs
- Les @refs changent a chaque page load
- Utiliser `fill` (pas `type`) pour les inputs (efface le contenu existant)
- `wait --load networkidle` apres les clicks qui chargent une page
- Fermer le browser quand tu as fini (`agent-browser close`)
- Pour du JSON parseable: ajouter `--json`
- Google/Bing bloquent le headless (CAPTCHA) — utiliser DuckDuckGo ou web_search a la place
- Pour les sites authentifies: `agent-browser state save/load` pour persister les sessions
