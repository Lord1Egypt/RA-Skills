/**
 * @module tools/search-text
 * @description Busca full-text em todas as notas do vault
 */

import { CONFIG, getDefaultHeaders, buildUrl, successResponse, errorResponse } from '../config/defaults.js';

/**
 * Realiza busca full-text no vault
 * @param {Object} options - Opções de busca
 * @param {string} options.query - Termo de busca
 * @param {boolean} [options.caseSensitive=false] - Diferenciar maiúsculas/minúsculas
 * @param {boolean} [options.regex=false] - Usar expressão regular
 * @param {string} [options.folder] - Limitar busca a uma pasta
 * @param {number} [options.limit=50] - Limite de resultados
 * @param {boolean} [options.includeContext=true] - Incluir contexto ao redor do match
 * @param {number} [options.contextLines=2] - Linhas de contexto
 * @returns {Promise<Object>} Resultados da busca
 */
export async function searchText(options) {
  try {
    const {
      query,
      caseSensitive = false,
      regex = false,
      folder,
      limit = 50,
      includeContext = true,
      contextLines = 2,
    } = options;

    // Validações
    if (!query) {
      return errorResponse('Termo de busca é obrigatório');
    }

    if (!CONFIG.apiKey) {
      return errorResponse('OBSIDIAN_API_KEY não configurada');
    }

    // Usa a API de busca do Obsidian
    const searchBody = {
      query: regex ? query : escapeRegex(query),
    };

    if (folder) {
      searchBody.path = folder;
    }

    const response = await fetch(buildUrl('/search/simple/'), {
      method: 'POST',
      headers: getDefaultHeaders(),
      body: JSON.stringify(searchBody),
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Erro ${response.status}: ${errorText}`);
    }

    const results = await response.json();

    // Processa resultados
    const processedResults = [];
    let total = 0;

    for (const result of results.slice(0, limit)) {
      total++;

      const matchInfo = {
        file: result.file,
        path: result.path,
        matches: result.matches || [],
      };

      // Busca contexto se solicitado
      if (includeContext) {
        try {
          const context = await fetchMatchContext(result.path, result.matches, contextLines, query, caseSensitive);
          matchInfo.context = context;
        } catch {
          matchInfo.context = null;
        }
      }

      processedResults.push(matchInfo);
    }

    return successResponse(
      `🔍 ${total} resultado(s) para "${query}"`,
      {
        query,
        totalResults: total,
        hasMore: results.length > limit,
        results: processedResults,
        searchOptions: {
          caseSensitive,
          regex,
          folder,
        },
      },
      '🔍'
    );

  } catch (error) {
    return errorResponse(`Falha na busca: ${error.message}`, error);
  }
}

/**
 * Busca contexto ao redor de matches
 * @param {string} path - Caminho do arquivo
 * @param {Array} matches - Matches encontrados
 * @param {number} contextLines - Linhas de contexto
 * @param {string} query - Query original
 * @param {boolean} caseSensitive - Case sensitivity
 * @returns {Promise<Array>} Contextos
 */
async function fetchMatchContext(path, matches, contextLines, query, caseSensitive) {
  try {
    const response = await fetch(buildUrl(`/vault/${path}`), {
      method: 'GET',
      headers: getDefaultHeaders(),
    });

    if (!response.ok) return [];

    const content = await response.text();
    const lines = content.split('\n');
    const contexts = [];

    const flags = caseSensitive ? 'g' : 'gi';
    const searchPattern = new RegExp(query, flags);

    for (let i = 0; i < lines.length; i++) {
      if (searchPattern.test(lines[i])) {
        const start = Math.max(0, i - contextLines);
        const end = Math.min(lines.length, i + contextLines + 1);

        contexts.push({
          lineNumber: i + 1,
          before: lines.slice(start, i),
          match: lines[i],
          after: lines.slice(i + 1, end),
        });
      }
    }

    return contexts;

  } catch {
    return [];
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
export default searchText;
