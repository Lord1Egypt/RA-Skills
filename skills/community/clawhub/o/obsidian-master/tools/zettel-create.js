/"
 * @module tools/zettel-create
 * @description Cria uma nota Zettelkasten com ID único
 */

import { CONFIG, getDefaultHeaders, buildUrl, successResponse, errorResponse, formatZettelId, formatDailyDate } from '../config/defaults.js';

/**
 * Cria nota Zettelkasten
 * @param {Object} options - Opções
 * @param {string} options.title - Título
 * @param {string} options.idea - Ideia atômica
 * @param {Array<string>} [options.related] - IDs de zettels relacionados
 * @param {string} [options.source] - Fonte
 * @returns {Promise<Object>} Zettel criado
 */
export async function zettelCreate(options) {
  try {
    const {
      title,
      idea,
      related = [],
      source = '',
    } = options;

    if (!title || !idea) {
      return errorResponse('Título e ideia são obrigatórios');
    }

    if (!CONFIG.apiKey) {
      return errorResponse('OBSIDIAN_API_KEY não configurada');
    }

    const id = formatZettelId(new Date());
    const date = formatDailyDate(new Date());
    const folder = CONFIG.folders.zettelkasten;
    const fileName = `${id} ${title}.md`;
    const filePath = `${folder}/${fileName}`;

    const content = `---
id: ${id}
title: "${title}"
created: ${date}
type: zettel
tags: []
related: [${related.join(', ')}]
---

# ${id} ${title}

${idea}

## Conexões

${related.map(r => `- [[${r}]]`).join('\n') || '- [Adicione conexões]'}

## Contexto

${source ? `**Fonte:** ${source}` : '- [Adicione contexto]'}

---

*ID: ${id}*`;

    const response = await fetch(buildUrl(`/vault/${filePath}`), {
      method: 'PUT',
      headers: getDefaultHeaders(),
      body: content,
    });

    if (!response.ok) {
      throw new Error('Erro ao criar zettel');
    }

    return successResponse(
      `🧠 Zettel '${id} ${title}' criado`,
      {
        id,
        title,
        path: filePath,
        related,
      },
      '🧠'
    );

  } catch (error) {
    return errorResponse(`Falha ao criar zettel: ${error.message}`, error);
  }
}

// Exporta também como default
export default zettelCreate;
