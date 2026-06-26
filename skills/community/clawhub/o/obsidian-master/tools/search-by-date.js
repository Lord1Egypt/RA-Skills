/"
 * @module tools/search-by-date
 * @description Busca notas por data de criação ou modificação
 */

import { CONFIG, getDefaultHeaders, buildUrl, successResponse, errorResponse } from '../config/defaults.js';
import { folderList } from './folder-list.js';

/**
 * Busca notas por data
 * @param {Object} options - Opções de busca
 * @param {string} [options.from] - Data inicial (YYYY-MM-DD)
 * @param {string} [options.to] - Data final (YYYY-MM-DD)
 * @param {string} [options.dateType='modified'] - Tipo: 'created', 'modified'
 * @param {string} [options.folder] - Limitar a uma pasta
 * @param {boolean} [options.includeContent=false] - Incluir conteúdo
 * @returns {Promise<Object>} Notas encontradas
 */
export async function searchByDate(options = {}) {
  try {
    const {
      from,
      to,
      dateType = 'modified',
      folder,
      includeContent = false,
    } = options;

    if (!CONFIG.apiKey) {
      return errorResponse('OBSIDIAN_API_KEY não configurada');
    }

    // Normaliza datas
    const fromDate = from ? new Date(from) : new Date('2000-01-01');
    const toDate = to ? new Date(to) : new Date();
    toDate.setHours(23, 59, 59);

    // Lista arquivos
    const listResult = await folderList({ path: folder || '', recursive: true });
    if (!listResult.success) {
      return errorResponse('Não foi possível listar arquivos');
    }

    const files = listResult.data.files.filter(f => f.extension === 'md');
    const results = [];

    for (const file of files) {
      try {
        // Usa o header para obter data sem ler conteúdo
        const response = await fetch(buildUrl(`/vault/${file.path}`), {
          method: 'HEAD',
          headers: getDefaultHeaders(),
        });

        if (!response.ok) continue;

        const lastModified = response.headers.get('last-modified');
        if (!lastModified) continue;

        const fileDate = new Date(lastModified);

        if (fileDate >= fromDate && fileDate <= toDate) {
          const result = {
            name: file.name,
            path: file.path,
            modified: lastModified,
            modifiedDate: fileDate.toISOString().split('T')[0],
          };

          if (includeContent) {
            try {
              const contentResponse = await fetch(buildUrl(`/vault/${file.path}`), {
                method: 'GET',
                headers: getDefaultHeaders(),
              });

              if (contentResponse.ok) {
                const content = await contentResponse.text();
                // Extrai created do frontmatter se existir
                const createdMatch = content.match(/^---\n.*?created:\s*(\S+)/s);
                if (createdMatch) {
                  result.created = createdMatch[1];
                }
                result.preview = content.slice(0, 200).replace(/\n/g, ' ');
              }
            } catch {
              // Ignora erro
            }
          }

          results.push(result);
        }

      } catch {
        // Ignora erro individual
      }
    }

    // Ordena por data
    results.sort((a, b) => new Date(b.modified) - new Date(a.modified));

    const dateRange = from && to
      ? `entre ${from} e ${to}`
      : from
        ? `após ${from}`
        : to
          ? `até ${to}`
          : 'todos os períodos';

    return successResponse(
      `📅 ${results.length} nota(s) ${dateRange}`,
      {
        from,
        to,
        dateType,
        totalResults: results.length,
        results,
      },
      '📅'
    );

  } catch (error) {
    return errorResponse(`Falha na busca por data: ${error.message}`, error);
  }
}

/**
 * Busca notas criadas/modificadas hoje
 * @returns {Promise<Object>} Notas de hoje
 */
export async function searchToday() {
  const today = new Date().toISOString().split('T')[0];
  return searchByDate({ from: today, to: today });
}

/**
 * Busca notas da última semana
 * @returns {Promise<Object>} Notas recentes
 */
export async function searchThisWeek() {
  const today = new Date();
  const lastWeek = new Date(today.getTime() - 7 * 24 * 60 * 60 * 1000);

  return searchByDate({
    from: lastWeek.toISOString().split('T')[0],
    to: today.toISOString().split('T')[0],
  });
}

// Exporta também como default
export default searchByDate;
