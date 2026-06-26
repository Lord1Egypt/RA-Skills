/"
 * @module tools/search-by-tag
 * @description Busca notas por tags específicas
 */

import { CONFIG, getDefaultHeaders, buildUrl, successResponse, errorResponse } from '../config/defaults.js';

/**
 * Busca notas que contêm uma ou mais tags
 * @param {Object} options - Opções de busca
 * @param {string|Array<string>} options.tags - Tag(s) a buscar
 * @param {boolean} [options.matchAll=false] - Requerer todas as tags (AND) vs qualquer uma (OR)
 * @param {string} [options.folder] - Limitar a uma pasta específica
 * @param {boolean} [options.includeContent=false] - Incluir conteúdo completo
 * @param {number} [options.limit=100] - Limite de resultados
 * @returns {Promise<Object>} Notas encontradas
 */
export async function searchByTag(options) {
  try {
    const {
      tags,
      matchAll = false,
      folder,
      includeContent = false,
      limit = 100,
    } = options;

    // Validações
    if (!tags) {
      return errorResponse('Tag(s) são obrigatórias');
    }

    if (!CONFIG.apiKey) {
      return errorResponse('OBSIDIAN_API_KEY não configurada');
    }

    // Normaliza tags para array
    const tagList = Array.isArray(tags) ? tags : [tags];
    const normalizedTags = tagList.map(t => t.replace(/^#/, ''));

    // Busca via tags endpoint ou query
    const searchQuery = normalizedTags.map(t => `tag:${t}`).join(matchAll ? ' AND ' : ' OR ');

    // Usa busca simples com query de tag
    const response = await fetch(buildUrl('/search/simple/'), {
      method: 'POST',
      headers: getDefaultHeaders(),
      body: JSON.stringify({
        query: normalizedTags.join('|'),
      }),
    });

    if (!response.ok) {
      // Fallback: busca manual
      const manualResults = await searchByTagManual(normalizedTags, matchAll, folder);
      return formatResults(manualResults, normalizedTags, matchAll);
    }

    const results = await response.json();

    // Filtra e processa resultados
    const processedResults = [];
    const filesToProcess = folder
      ? results.filter(r => r.path.startsWith(folder))
      : results;

    for (const result of filesToProcess.slice(0, limit)) {
      const noteInfo = {
        file: result.file,
        path: result.path,
        tags: [],
      };

      // Extrai tags se possível
      if (includeContent) {
        try {
          const contentResponse = await fetch(buildUrl(`/vault/${result.path}`), {
            method: 'GET',
            headers: getDefaultHeaders(),
          });

          if (contentResponse.ok) {
            const content = await contentResponse.text();
            const allTags = extractTags(content);
            noteInfo.tags = allTags;
            noteInfo.matchingTags = allTags.filter(t => normalizedTags.includes(t));
          }
        } catch {
          // Ignora erro
        }
      }

      processedResults.push(noteInfo);
    }

    return formatResults(processedResults, normalizedTags, matchAll);

  } catch (error) {
    return errorResponse(`Falha na busca por tag: ${error.message}`, error);
  }
}

/**
 * Busca manual de tags (fallback)
 * @param {Array<string>} tags - Tags a buscar
 * @param {boolean} matchAll - Requerer todas
 * @param {string} folder - Pasta específica
 * @returns {Promise<Array>} Resultados
 */
async function searchByTagManual(tags, matchAll, folder) {
  // Lista todos os arquivos
  const listPath = folder || '';
  const response = await fetch(buildUrl(`/vault/${listPath}`), {
    method: 'GET',
    headers: getDefaultHeaders(),
  });

  if (!response.ok) return [];

  const items = await response.json();
  const mdFiles = items.filter(i => i.endsWith('.md'));

  const results = [];

  for (const file of mdFiles) {
    try {
      const fileResponse = await fetch(
        buildUrl(`/vault/${listPath ? listPath + '/' : ''}${file}`),
        { method: 'GET', headers: getDefaultHeaders() }
      );

      if (fileResponse.ok) {
        const content = await fileResponse.text();
        const fileTags = extractTags(content);

        const matches = matchAll
          ? tags.every(t => fileTags.includes(t))
          : tags.some(t => fileTags.includes(t));

        if (matches) {
          results.push({
            file,
            path: `${listPath ? listPath + '/' : ''}${file}`,
            tags: fileTags,
            matchingTags: fileTags.filter(t => tags.includes(t)),
          });
        }
      }
    } catch {
      // Ignora erro
    }
  }

  return results;
}

/**
 * Extrai tags de conteúdo
 * @param {string} content - Conteúdo da nota
 * @returns {Array<string>} Tags encontradas
 */
function extractTags(content) {
  const tagRegex = /#[a-zA-Z0-9_\-\/]+/g;
  const matches = content.match(tagRegex);
  return matches ? matches.map(t => t.slice(1)) : [];
}

/**
 * Formata resultados da busca
 * @param {Array} results - Resultados brutos
 * @param {Array} tags - Tags buscadas
 * @param {boolean} matchAll - Modo de match
 * @returns {Object} Resposta formatada
 */
function formatResults(results, tags, matchAll) {
  const operator = matchAll ? 'E' : 'OU';
  const tagString = tags.map(t => `#${t}`).join(` ${operator} `);

  return successResponse(
    `🏷️ ${results.length} nota(s) com ${tagString}`,
    {
      tags,
      matchAll,
      totalResults: results.length,
      results,
    },
    '🏷️'
  );
}

// Exporta também como default
export default searchByTag;
