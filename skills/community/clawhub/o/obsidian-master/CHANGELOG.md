# Changelog

Todas as mudanças notáveis deste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-03-20

### Adicionado
- Skill completa para Obsidian com 66+ tools
- Sistema de notas básico: create, read, update, delete, move, rename, duplicate, merge
- Gerenciamento de frontmatter: get, set, add-tag, remove-tag
- Organização de pastas: create, list, move, delete, stats
- Sistema completo de Canvas: create, read, add-card, add-note, add-group, connect, auto-map
- Busca avançada: text, by-tag, by-date, backlinks, orphans, broken-links, by-frontmatter
- Daily Notes: open, append, read, week-summary, month-summary
- Templates: list, apply, create-note, create
- Integração com Dataview: query, list-tasks
- Sistema de tasks: create, complete
- Links e grafos: create
- Vault Intelligence: stats, health
- MOC (Map of Content): create
- Zettelkasten: create
- Utilitários: obsidian-command
- Documentação completa em SKILL.md (400+ linhas)
- README.md com guia de instalação e uso
- Sistema de resposta padronizado (success/error/warning)
- Suporte a variáveis de ambiente para configuração
- Zero dependências externas

### Recursos
- Integração completa com Obsidian Local REST API
- Padrão de nomenclatura PARA + Zettelkasten
- Frontmatter padronizado com metadados
- Tratamento de erros completo
- Validação de inputs
- Backup automático antes de deleções
- Suporte a operações bidirecionais

## Próximas Versões

### [1.1.0] - Planejado
- Plugin-list: Listar plugins instalados
- Templater-run: Executar scripts Templater
- Zettel-link-suggest: Sugerir conexões entre zettels
- Zettel-cluster: Identificar clusters de conhecimento
- Moc-update: Atualizar MOC existente
- Task-list-open: Listar tasks abertas
- Task-list-by-project: Tasks por projeto
- Task-daily-review: Review de tasks

### [1.2.0] - Planejado
- Link-scan-all: Mapear rede de links
- Link-suggest: Sugerir links baseado em conteúdo
- Vault-export-topic: Exportar tema como markdown
- Vault-recent: Notas modificadas recentemente
- Vault-structure-map: Mapa completo da estrutura
- Dataview-inline: Avaliar expressões inline
- Dataview-by-tag: Tabela de notas por tag
- Dataview-calendar: Gerar view de calendário
- Templater-create-template: Criar template Templater

### [2.0.0] - Planejado
- Suporte a múltiplos vaults simultâneos
- Sincronização bidirecional
- Cache inteligente de queries
- Dashboard em tempo real
- Análise de sentimento de notas
- Sugestões automáticas de tags com ML
- Exportação para formatos diversos (PDF, HTML, etc)
- Integração com Git para versionamento
