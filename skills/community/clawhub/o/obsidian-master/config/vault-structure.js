/**
 * Estrutura esperada do vault e templates padrão
 * Define a hierarquia de pastas e conteúdos iniciais
 * @module config/vault-structure
 */

import { CONFIG } from './defaults.js';

/**
 * Estrutura completa de pastas do sistema PARA + Zettelkasten
 * @type {Array<Object>}
 */
export const VAULT_STRUCTURE = [
  {
    name: CONFIG.folders.inbox,
    description: 'Capturas rápidas sem processamento',
    readme: `# 📥 ${CONFIG.folders.inbox}

Pasta para capturas rápidas e notas não processadas.

## Regras
- Notas aqui são temporárias
- Devem ser processadas e movidas em até 24h
- Use para notas rápidas do celular ou ideias de emergência

## Processamento
Use o comando ".processar inbox" para analisar e mover notas automaticamente.`,
  },
  {
    name: CONFIG.folders.projects,
    description: 'Projetos ativos com deadline',
    readme: `# 📁 ${CONFIG.folders.projects}

Projetos são iniciativas com:
- **Início e fim definidos**
- **Objetivo claro**
- **Resultado esperado específico**

## Exemplos
- Escrever artigo sobre X
- Organizar festa de aniversário
- Implementar feature Y no sistema
- Reformar o escritório

## Template
Cada projeto deve usar o template de projeto.`,
  },
  {
    name: CONFIG.folders.areas,
    description: 'Responsabilidades contínuas sem deadline',
    readme: `# 🎯 ${CONFIG.folders.areas}

Áreas são responsabilidades contínuas que exigem atenção regular:
- **Sem data de término definida**
- **Necessita manutenção contínua**
- **Padrões a serem mantidos**

## Exemplos
- Saúde
- Finanças Pessoais
- Carreira
- Relacionamentos
- Desenvolvimento Pessoal

## Notas
Cada área pode ter MOCs (Maps of Content) associados.`,
  },
  {
    name: CONFIG.folders.resources,
    description: 'Material de referência e estudo',
    readme: `# 📚 ${CONFIG.folders.resources}

Recursos são materiais de referência que podem ser úteis no futuro:
- Artigos salvos
- Tutoriais
- Livros lidos
- Cursos
- Referências técnicas

## Organização
Organize por tema ou tipo de conteúdo.`,
  },
  {
    name: CONFIG.folders.archive,
    description: 'Projetos concluídos e notas inativas',
    readme: `# 🗃️ ${CONFIG.folders.archive}

Arquivo de projetos concluídos e notas inativas.

## O que arquivar
- Projetos finalizados
- Tarefas canceladas
- Notas que não são mais relevantes
- Versões antigas de documentos

## Busca
Notas arquivadas ainda são pesquisáveis via busca full-text.`,
  },
  {
    name: CONFIG.folders.daily,
    description: 'Diário estruturado',
    readme: `# 📅 ${CONFIG.folders.daily}

Daily Notes - Registro diário estruturado.

## Estrutura
Cada dia contém:
- Intenção do dia
- Tasks do dia
- Notas rápidas
- Review da noite

## Integração
Usa queries Dataview para mostrar tasks de projetos ativos.`,
  },
  {
    name: CONFIG.folders.canvas,
    description: 'Mapas visuais e brainstorms',
    readme: `# 🎨 ${CONFIG.folders.canvas}

Canvas - Mapas visuais e brainstorms.

## Tipos
- Brainstorms
- Mapas mentais
- Diagramas de projeto
- Fluxos de trabalho
- Boards de planejamento`,
  },
  {
    name: CONFIG.folders.zettelkasten,
    description: 'Notas atômicas interconectadas',
    readme: `# 🧠 ${CONFIG.folders.zettelkasten}

Zettelkasten - Sistema de notas atômicas.

## Princípios
1. **Atômica**: uma ideia por nota
2. **Autônoma**: compreensível isoladamente
3. **Conectada**: links para notas relacionadas
4. **Numerada**: ID único baseado em data/hora

## IDs
Formato: YYYYMMDDHHmm (ex: 202603201430)`,
  },
  {
    name: CONFIG.folders.mocs,
    description: 'Maps of Content por tema',
    readme: `# 🗺️ ${CONFIG.folders.mocs}

Maps of Content (MOCs) - Índices temáticos.

## Função
Um MOC organiza e conecta notas sobre um tema específico.
Serve como "mesa de trabalho" para explorar um tópico.

## Estrutura
- Visão geral do tema
- Links para notas relacionadas
- Agrupamentos por subtema
- Espaço para desenvolvimento`,
  },
  {
    name: CONFIG.folders.templates,
    description: 'Templates do sistema',
    readme: `# 📝 ${CONFIG.folders.templates}

Templates para criação padronizada de notas.

## Disponíveis
- project-template.md
- daily-template.md
- zettel-template.md
- moc-template.md`,
  },
];

/**
 * Templates padrão do sistema
 * @type {Object<string, string>}
 */
export const TEMPLATES = {
  project: `---
title: "{{title}}"
created: {{date}}
type: project
status: active
deadline: ""
tags: [projeto]
---

# {{title}}

## 🎯 Objetivo

Descreva aqui o objetivo principal deste projeto.

## 📋 Tasks
- [ ] Task inicial

## 📎 Recursos Relacionados

## 📅 Log
### {{date}}
- Projeto iniciado
`,

  daily: `---
title: "{{date}}"
created: {{date}}
type: daily
tags: [daily]
---

# {{date:dddd, D [de] MMMM [de] YYYY}}

## 🌅 Intenção do Dia

## ✅ Tasks de Hoje
\`\`\`dataview
TASK FROM "${CONFIG.folders.projects}"
WHERE !completed
SORT file.mtime DESC
\`\`\`

## 📝 Notas Rápidas

## 🌙 Review do Dia
### O que foi feito

### Aprendizados

### Amanhã
`,

  zettel: `---
id: {{zettelId}}
title: "{{title}}"
created: {{date}}
type: zettel
tags: []
related: []
---

# {{title}}

[Ideia atômica aqui - uma ideia por nota]

## Conexões
- [[nota-relacionada-1]]
- [[nota-relacionada-2]]

## Fonte
`,

  moc: `---
title: "{{title}}"
created: {{date}}
type: moc
tags: [moc]
---

# 🗺️ {{title}}

> Map of Content para o tema: {{theme}}

## Visão Geral

Breve descrição do tema e sua importância.

## 🗂️ Seções Principais

### Categoria 1
- [[Nota 1]]
- [[Nota 2]]

### Categoria 2
- [[Nota 3]]
- [[Nota 4]]

## 🔗 Conexões com outros MOCs
- [[Outro MOC]]

## 📝 Notas em Desenvolvimento
- [[Ideia inicial]]

## 🏷️ Tags Relacionadas
#{{theme}}`,

  note: `---
title: "{{title}}"
created: {{date}}
modified: {{date}}
tags: []
type: note
status: active
related: []
source: ""
---

# {{title}}

`,

  task: `---
title: "Task: {{title}}"
created: {{date}}
type: task
status: open
tags: [task]
project: ""
priority: medium
---

# {{title}}

- [ ] {{description}}

## Detalhes
- **Criada em:** {{date}}
- **Prioridade:** {{priority}}
- **Projeto:** {{project}}
`,
};

/**
 * Padrões de busca para diferentes tipos de conteúdo
 * @type {Object<string, RegExp>}
 */
export const PATTERNS = {
  // Wikilinks: [[Nota]] ou [[Nota|Alias]]
  wikilink: /\[\[([^\]|]+)(?:\|[^\]]+)?\]\]/g,

  // Tags: #tag ou #tag/nested
  tag: /#([a-zA-Z0-9_\-\/]+)/g,

  // Tasks: - [ ] ou - [x]
  taskOpen: /- \[ \] (.+)$/gm,
  taskDone: /- \[x\] (.+)$/gm,

  // Frontmatter
  frontmatter: /^---\n([\s\S]*?)\n---/,

  // Headers
  header: /^(#{1,6})\s+(.+)$/gm,

  // Canvas nodes
  canvasNode: /"type":"(text|file|group)"/g,

  // Dataview queries
  dataviewQuery: /\`\`\`dataview\n([\s\S]*?)\n\`\`\`/g,

  // Links externos
  externalLink: /\[([^\]]+)\]\((https?:\/\/[^\)]+)\)/g,

  // IDs Zettelkasten
  zettelId: /\d{12}/,
};

/**
 * Mapeamento de emojis para tipos de nota
 * @type {Object<string, string>}
 */
export const TYPE_EMOJIS = {
  note: '📝',
  project: '📁',
  area: '🎯',
  resource: '📚',
  archive: '🗃️',
  daily: '📅',
  canvas: '🎨',
  zettel: '🧠',
  moc: '🗺️',
  template: '📋',
  task: '✅',
};

/**
 * Retorna emoji para um tipo de nota
 * @param {string} type - Tipo da nota
 * @returns {string} Emoji correspondente
 */
export function getTypeEmoji(type) {
  return TYPE_EMOJIS[type] || TYPE_EMOJIS.note;
}

/**
 * Substitui variáveis em template
 * @param {string} template - Template com placeholders {{var}}
 * @param {Object} variables - Objeto com valores a substituir
 * @returns {string} Template processado
 */
export function processTemplate(template, variables) {
  let result = template;

  for (const [key, value] of Object.entries(variables)) {
    const regex = new RegExp(`{{${key}}}`, 'g');
    result = result.replace(regex, value);
  }

  // Limpa placeholders não substituídos
  result = result.replace(/\{\{[^}]+\}\}/g, '');

  return result;
}

/**
 * Lista todas as pastas da estrutura
 * @returns {Array<string>} Nomes das pastas
 */
export function listAllFolders() {
  return VAULT_STRUCTURE.map(f => f.name);
}

/**
 * Retorna descrição de uma pasta
 * @param {string} folderName - Nome da pasta
 * @returns {string} Descrição ou string vazia
 */
export function getFolderDescription(folderName) {
  const folder = VAULT_STRUCTURE.find(f => f.name === folderName);
  return folder?.description || '';
}
