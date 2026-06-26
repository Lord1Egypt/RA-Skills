/"
 * @module tools/task-list-by-project
 * @description Lista tasks de um projeto específico
 */

import { CONFIG, successResponse, errorResponse } from '../config/defaults.js';
import { dataviewListTasks } from './dataview-list-tasks.js';

/**
 * Lista tasks de um projeto
 * @param {Object} options - Opções
 * @param {string} options.project - Nome do projeto
 * @returns {Promise<Object>} Tasks
 */
export async function taskListByProject(options) {
  try {
    const { project } = options;

    if (!project) {
      return errorResponse('Nome do projeto é obrigatório');
    }

    const folder = `${CONFIG.folders.projects}/${project}`;

    return await dataviewListTasks({ from: `"${folder}"`, completed: false });

  } catch (error) {
    return errorResponse(`Falha ao listar tasks: ${error.message}`, error);
  }
}

export default taskListByProject;
