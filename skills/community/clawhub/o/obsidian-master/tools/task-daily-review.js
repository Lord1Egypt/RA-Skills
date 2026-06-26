/"
 * @module tools/task-daily-review
 * @description Gera review diário de tasks
 */

import { CONFIG, successResponse, errorResponse } from '../config/defaults.js';
import { dailyRead } from './daily-read.js';
import { dataviewListTasks } from './dataview-list-tasks.js';

/**
 * Gera review de tasks do dia
 * @param {Object} options - Opções
 * @returns {Promise<Object>} Review
 */
export async function taskDailyReview(options = {}) {
  try {
    // Pega tasks abertas
    const tasksResult = await dataviewListTasks({ completed: false });

    // Pega daily de hoje
    const dailyResult = await dailyRead();

    const review = {
      date: new Date().toISOString().split('T')[0],
      openTasks: tasksResult.success ? tasksResult.data.tasks : [],
      dailyTasks: dailyResult.success ? dailyResult.data.tasks?.open || [] : [],
      summary: '',
    };

    // Gera resumo
    const totalOpen = review.openTasks.length;
    const totalDaily = review.dailyTasks.length;

    review.summary = `${totalOpen} tasks abertas no vault, ${totalDaily} na daily de hoje.`;

    return successResponse(
      `📋 Review diário: ${review.summary}`,
      review,
      '📋'
    );

  } catch (error) {
    return errorResponse(`Falha no review: ${error.message}`, error);
  }
}

export default taskDailyReview;
