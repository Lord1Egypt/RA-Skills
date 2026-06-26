/"
 * @module tools/task-list-open
 * @description Lista todas as tasks abertas do vault
 */

import { dataviewListTasks } from './dataview-list-tasks.js';

/**
 * Lista tasks abertas
 * @param {Object} options - Opções
 * @returns {Promise<Object>} Tasks
 */
export async function taskListOpen(options = {}) {
  return await dataviewListTasks({ ...options, completed: false });
}

export default taskListOpen;
