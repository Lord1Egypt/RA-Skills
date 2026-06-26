/**
 * @module tools/search-backlinks
 * @description Encontra todas as notas que linkam para uma nota específica
 */

import { CONFIG, getDefaultHeaders, buildUrl, successResponse, errorResponse } from '../config/defaults.js';

/**
 * Busca backlinks para uma nota específica
 * @param {Object} options - Opções de busca
 * @param {string} options.note - Nome ou caminho da nota (ex: "Minha Nota" ou "Projetos/Minha Nota")
 * @param {boolean} [options.includeAliases=true] - Incluir links com aliases [[Nota|Texto]]
 * @param {boolean} [options.includeEmbedded=true] - Incluir embeds ![[Nota]]
 * @param {number} [options.limit=100] - Limite de resultados
 * @returns {Promise<Object>} Backlinks encontrados
 */
export async function searchBacklinks(options) {
  try {
    const {
      note,
      includeAliases = true,
      includeEmbedded = true,
      limit = 100,
    } = options;

    // Validações
    if (!note) {
      return errorResponse('Nome da nota é obrigatório');
    }

    if (!CONFIG.apiKey) {
      return errorResponse('OBSIDIAN_API_KEY não configurada');
    }

    // Extrai o nome da nota (sem caminho e sem extensão)
    const noteName = note.split('/').pop().replace(/\.md$/, '');

    // Busca todos os arquivos
    const response = await fetch(buildUrl('/vault/'), {
      method: 'GET',
      headers: getDefaultHeaders(),
    });

    if (!response.ok) {
      throw new Error('Não foi possível listar o vault');
    }

    const items = await response.json();
    const mdFiles = items.filter(i => i.endsWith('.md'));

    const backlinks = [];

    // Padrões de busca
    const patterns = [
      `\\[\\[${escapeRegex(noteName)}\\]\\]`, // [[Nota]]
    ];

    if (includeAliases) {
      patterns.push(`\\[\\[${escapeRegex(noteName)}\\|[^\\]]+\\]\\]`); // [[Nota|Texto]]
    }

    if (includeEmbedded) {
      patterns.push(`!\\[\\[${escapeRegex(noteName)}[^\\]]*\\]\\]`); // ![[Nota]]
    }

    const searchRegex = new RegExp(patterns.join('|'), 'g');

    for (const file of mdFiles) {
      try {
        const fileResponse = await fetch(buildUrl(`/vault/${file}`), {
          method: 'GET',
          headers: getDefaultHeaders(),
        });

        if (!fileResponse.ok) continue;

        const content = await fileResponse.text();

        // Busca links
        const matches = content.match(searchRegex);

        if (matches) {
          // Extrai contexto
          const contexts = [];
          const lines = content.split('\n');

          for (let i = 0; i < lines.length; i++) {
            if (lines[i].includes(`[[${noteName}`)) {
              contexts.push({
                line: i + 1,
                text: lines[i].trim(),
                surrounding: lines.slice(Math.max(0, i - 1), Math.min(lines.length, i + 2)),
              });
            }
          }

          backlinks.push({
            file,
            path: file,
            linkCount: matches.length,
            contexts: contexts.slice(0, 3), // Limita contextos
          });
        }

        if (backlinks.length >= limit) break;

      } catch {
        // Ignora erro individual
      }
    }

    // Organiza por número de links
    backlinks.sort((a, b) => b.linkCount - a.linkCount);

    return successResponse(
      `🔗 ${backlinks.length} nota(s) linkam para "${noteName}"`,
      {
        targetNote: noteName,
        totalBacklinks: backlinks.length,
        totalReferences: backlinks.reduce((sum, b) => sum + b.linkCount, 0),
        backlinks,
      },
      '🔗'
    );

  } catch (error) {
    return errorResponse(`Falha ao buscar backlinks: ${error.message}`, error);
  }
}

/**
 * Escapa caracteres especiais para regex
 * @param {string} string - String original
 * @returns {string} String escapada
 */
function escapeRegex(string) {
  return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

// Exporta também como default
export default searchBacklinks;
