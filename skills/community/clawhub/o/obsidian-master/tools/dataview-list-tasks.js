/"
 * @module tools/dataview-list-tasks
 * @description Lista tasks abertas via Dataview
 */

import { CONFIG, getDataviewHeaders, buildUrl, successResponse, errorResponse } from '../config/defaults.js';

/**
 * Lista tasks via Dataview
 * @param {Object} options - Opções
 * @param {string} [options.from] - Fonte (ex: '"Projetos"')
 * @param {boolean} [options.completed=false] - Incluir concluídas
 * @param {string} [options.sortBy='file.name'] - Ordenar por
 * @returns {Promise<Object>} Tasks
 */
export async function dataviewListTasks(options = {}) {
  try {
    const {
      from = '""',
      completed = false,
      sortBy = 'file.name',
    } = options;

    if (!CONFIG.apiKey) {
      return errorResponse('OBSIDIAN_API_KEY não configurada');
    }

    const whereClause = completed ? '' : 'WHERE !completed';
    const query = `TASK FROM ${from} ${whereClause} SORT ${sortBy}`;

    const response = await fetch(buildUrl('/search/'), {
      method: 'POST',
      headers: getDataviewHeaders(),
      body: query,
    });

    if (!response.ok) {
      throw new Error('Erro na query');
    }

    const results = await response.json();

    return successResponse(
      `✅ ${results.length} task(s) encontrada(s)`,
      {
        query,
        tasks: results,
        count: results.length,
      },
      '✅'
    );

  } catch (error) {
    return errorResponse(`Falha ao listar tasks: ${error.message}`, error);
  }
}

// Exporta também como default
export default dataviewListTasks;
