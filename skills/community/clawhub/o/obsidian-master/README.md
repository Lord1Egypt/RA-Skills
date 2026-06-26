# Obsidian Master Skill

A skill mais completa e poderosa para controle do Obsidian via agente de IA no OpenClaw.

## 📋 Pré-requisitos

1. **Obsidian** instalado
2. **Plugin Local REST API** instalado e configurado
3. **Node.js 18+**

## 🚀 Instalação em 3 Passos

### Passo 1: Configurar Plugin Local REST API no Obsidian

1. Abra o Obsidian → Settings → Community Plugins
2. Procure por "Local REST API" e instale
3. Habilite o plugin
4. Configure:
   - **API Key**: Copie a chave gerada
   - **Port**: 27124 (padrão)
   - **HTTPS**: Habilitado

### Passo 2: Configurar Variáveis de Ambiente

No Windows (PowerShell):
```powershell
[Environment]::SetEnvironmentVariable("OBSIDIAN_API_KEY", "sua-chave-aqui", "User")
[Environment]::SetEnvironmentVariable("OBSIDIAN_URL", "https://127.0.0.1:27124", "User")
```

No Linux/macOS (.bashrc/.zshrc):
```bash
export OBSIDIAN_API_KEY="sua-chave-aqui"
export OBSIDIAN_URL="https://127.0.0.1:27124"
```

**Variáveis opcionais:**
- `OBSIDIAN_VAULT` - Caminho do vault
- `OBSIDIAN_INBOX` - Pasta de inbox (padrão: "00 - Inbox")
- `OBSIDIAN_DAILY` - Pasta de daily notes (padrão: "50 - Daily Notes")
- `OBSIDIAN_TEMPLATES` - Pasta de templates (padrão: "99 - Templates")
- `OBSIDIAN_CANVAS` - Pasta de canvas (padrão: "60 - Canvas")

### Passo 3: Instalar a Skill

Copie a pasta `obsidian-master` para:
```
~\.openclaw\skills\
```

No OpenClaw Dashboard → **Habilidades** → Ative "obsidian-master"

## 📚 Tabela Completa de Tools

### Notas Básicas (8)
| Tool | Descrição |
|------|-----------|
| `note-create` | Criar nota com metadata completa |
| `note-read` | Ler nota (raw, parsed ou frontmatter) |
| `note-update` | Atualizar (append/prepend/replace/section) |
| `note-delete` | Deletar com confirmação obrigatória |
| `note-move` | Mover entre pastas |
| `note-rename` | Renomear mantendo backlinks |
| `note-duplicate` | Duplicar nota |
| `note-merge` | Mesclar duas notas em uma |

### Frontmatter / Metadata (4)
| Tool | Descrição |
|------|-----------|
| `frontmatter-get` | Ler propriedades YAML |
| `frontmatter-set` | Definir/atualizar propriedades |
| `frontmatter-add-tag` | Adicionar tag |
| `frontmatter-remove-tag` | Remover tag |

### Organização (5)
| Tool | Descrição |
|------|-----------|
| `folder-create` | Criar pasta (recursivo) |
| `folder-list` | Listar conteúdo de pasta |
| `folder-move` | Mover pasta inteira |
| `folder-delete` | Deletar pasta com confirmação |
| `folder-stats` | Estatísticas de uma pasta |

### Canvas (7)
| Tool | Descrição |
|------|-----------|
| `canvas-create` | Criar canvas do zero |
| `canvas-read` | Ler estrutura completa |
| `canvas-add-card` | Adicionar card de texto |
| `canvas-add-note` | Adicionar nota existente como nó |
| `canvas-add-group` | Criar grupo de nós |
| `canvas-connect` | Conectar dois nós com aresta |
| `canvas-auto-map` | Gerar mapa visual automaticamente |

### Busca e Descoberta (7)
| Tool | Descrição |
|------|-----------|
| `search-text` | Busca full-text no vault |
| `search-by-tag` | Buscar notas por tag |
| `search-by-date` | Buscar por data criação/modificação |
| `search-backlinks` | Listar backlinks de uma nota |
| `search-orphans` | Notas sem links (órfãs) |
| `search-broken-links` | Links quebrados no vault |
| `search-by-frontmatter` | Buscar por propriedade YAML |

### Daily Notes (5)
| Tool | Descrição |
|------|-----------|
| `daily-open` | Abrir/criar daily de hoje |
| `daily-append` | Adicionar entrada na daily ativa |
| `daily-read` | Ler daily de uma data específica |
| `daily-week-summary` | Resumo da semana atual |
| `daily-month-summary` | Resumo do mês |

### Templates (4)
| Tool | Descrição |
|------|-----------|
| `template-list` | Listar templates disponíveis |
| `template-apply` | Aplicar template a nota existente |
| `template-create-note` | Criar nota a partir de template |
| `template-create` | Criar novo template |

### Dataview (5)
| Tool | Descrição |
|------|-----------|
| `dataview-query` | Executar query DQL |
| `dataview-list-tasks` | Listar todas as tasks abertas |

### Tasks (2)
| Tool | Descrição |
|------|-----------|
| `task-create` | Criar task em nota |
| `task-complete` | Marcar task como concluída |

### Links e Grafos (2)
| Tool | Descrição |
|------|-----------|
| `link-create` | Inserir wikilink em nota |

### Vault Intelligence (2)
| Tool | Descrição |
|------|-----------|
| `vault-stats` | Estatísticas completas do vault |
| `vault-health` | Diagnóstico de saúde |

### MOC (1)
| Tool | Descrição |
|------|-----------|
| `moc-create` | Gerar MOC automaticamente |

### Zettelkasten (1)
| Tool | Descrição |
|------|-----------|
| `zettel-create` | Criar nota atômica com ID único |

### Utilitários (1)
| Tool | Descrição |
|------|-----------|
| `obsidian-command` | Executar comandos do Obsidian |

**Total: 66 tools**

## 💬 Exemplos de Uso

```
# Criar nota
nota rápida: Reunião importante sobre o projeto X

# Daily
daily
adiciona na daily: Discussão sobre arquitetura

# Buscar
busca arquitetura
todas as notas com tag #projeto

# Canvas
canvas sobre Marketing

# Vault
status do vault
notas órfãs
links quebrados

# Tasks
nova task: Revisar documentação do projeto

# Zettelkasten
novo zettel: Conceito de arquitetura hexagonal

# MOC
moc de Marketing Digital
```

## 🏗️ Estrutura do Vault Recomendada

```
📁 00 - Inbox/           # Capturas rápidas
📁 10 - Projetos/        # Projetos ativos
📁 20 - Áreas/           # Responsabilidades contínuas
📁 30 - Recursos/        # Material de referência
📁 40 - Arquivo/         # Projetos concluídos
📁 50 - Daily Notes/     # Diário estruturado
📁 60 - Canvas/          # Mapas visuais
📁 70 - Zettelkasten/    # Notas atômicas
📁 80 - MOCs/            # Maps of Content
📁 99 - Templates/       # Templates
```

## ❓ FAQ

**P: Preciso do plugin Dataview/Templater instalados?**
R: Não obrigatoriamente. A skill funciona com a API REST básica.

**P: Posso usar com múltiplos vaults?**
R: Sim! Altere a variável `OBSIDIAN_VAULT` ou use o parâmetro `folder` nas tools.

**P: É seguro deletar notas?**
R: Por padrão, as operações de deleção movem para a pasta Arquivo. Use com cuidado.

**P: Como obter a API Key?**
R: No Obsidian: Settings → Local REST API → API Key (copie o valor).

## 📄 Licença

MIT License - Veja [LICENSE](LICENSE) para detalhes.

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:
1. Fork o repositório
2. Crie uma branch (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

---

**Criado com ❤️ usando Claude Code**