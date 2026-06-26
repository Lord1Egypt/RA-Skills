# HackerNews Skill

Monitora e busca stories do HackerNews via API oficial.

## Gatilhos

Ative a skill usando palavras-chave:
- `"hackernews"`, `"hn"` — listar top stories
- `"top stories"`, `"front page"` — top stories
- `"new"`, `"latest"`, `"novas"` — stories recentes  
- `"ask hn"`, `"askstories"` — Ask HN
- `"show hn"`, `"showstories"` — Show HN
- `"jobs"`, `"vagas"` — Jobs
- `"best"`, `"melhores"` — Melhores stories
- `"buscar no hn"`, `"pesquisar hn"` — buscar por termo

## Como Usar

```bash
# Listar top stories (padrão: 10)
node index.js top
node index.js top 20

# Stories recentes
node index.js new
node index.js new 15

# Melhores stories
node index.js best

# Ask HN
node index.js ask
node index.js show

# Jobs
node index.js jobs

# Ver detalhes de uma story por ID
node index.js item 12345678

# Ver perfil de usuário
node index.js user pg

# Buscar stories por termo
node index.js search rust
node index.js search "machine learning"
```

##API

- **URL Base:** `https://hacker-news.firebaseio.com/v0/`
- **Rate Limit:** Nenhum (API pública)
- **Autenticação:** Não requerida
