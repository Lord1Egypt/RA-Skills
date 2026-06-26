/"
 * @module tools/dataview-query
 * @description Executa queries DQL do Dataview
 */

import { CONFIG, getDataviewHeaders, buildUrl, successResponse, errorResponse } from '../config/defaults.js';

/**
 * Executa query Dataview
 * @param {Object} options - Opções
 * @param {string} options.query - Query DQL
 * @param {string} [options.format='json'] - Formato: 'json', 'table', 'list'
 * @returns {Promise<Object>} Resultados
 */
export async function dataviewQuery(options) {
  try {
    const {
      query,
      format = 'json',
    } = options;

    if (!query) {
      return errorResponse('Query é obrigatória');
    }

    if (!CONFIG.apiKey) {
      return errorResponse('OBSIDIAN_API_KEY não configurada');
    }

    const response = await fetch(buildUrl('/search/'), {
      method: 'POST',
      headers: getDataviewHeaders(),
      body: query,
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Erro ${response.status}: ${errorText}`);
    }

    const results = await response.json();

    return successResponse(
      `📊 Query executada`,
      {
        query,
        resultCount: Array.isArray(results) ? results.length : 1,
        results,
        format,
      },
      '📊'
    );

  } catch (error) {
    return errorResponse(`Falha na query: ${error.message}`, error);
  }
}

// Exporta também como default
export default dataviewQuery;
