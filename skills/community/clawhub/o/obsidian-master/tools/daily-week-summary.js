/"
 * @module tools/daily-week-summary
 * @description Gera resumo da semana atual
 */

import { CONFIG, getDefaultHeaders, buildUrl, successResponse, errorResponse, formatDailyDate } from '../config/defaults.js';

/**
 * Gera resumo da semana
 * @param {Object} options - Opções
 * @param {number} [options.offset=0] - Offset em semanas (0 = atual, -1 = passada)
 * @returns {Promise<Object>} Resumo
 */
export async function dailyWeekSummary(options = {}) {
  try {
    const { offset = 0 } = options;

    if (!CONFIG.apiKey) {
      return errorResponse('OBSIDIAN_API_KEY não configurada');
    }

    const today = new Date();
    const currentWeek = getWeekDates(today, offset);

    const summaries = [];
    let totalTasks = { open: 0, completed: 0 };

    for (const date of currentWeek) {
      const filePath = `${CONFIG.folders.daily}/${date}.md`;

      try {
        const response = await fetch(buildUrl(`/vault/${filePath}`), {
          method: 'GET',
          headers: getDefaultHeaders(),
        });

        if (response.ok) {
          const content = await response.text();
          const daySummary = summarizeDay(content, date);
          summaries.push(daySummary);

          totalTasks.open += daySummary.tasks.open.length;
          totalTasks.completed += daySummary.tasks.completed.length;
        }
      } catch {
        // Dia sem daily
        summaries.push({
          date,
          exists: false,
          tasks: { open: [], completed: [] },
        });
      }
    }

    const weekRange = `${currentWeek[0]} a ${currentWeek[6]}`;

    return successResponse(
      `📊 Resumo da semana ${weekRange}`,
      {
        weekRange,
        days: summaries,
        totalTasks,
        completion: totalTasks.completed + totalTasks.open > 0
          ? Math.round((totalTasks.completed / (totalTasks.completed + totalTasks.open)) * 100)
          : 0,
      },
      '📊'
    );

  } catch (error) {
    return errorResponse(`Falha ao gerar resumo: ${error.message}`, error);
  }
}

/**
 * Retorna datas da semana
 * @param {Date} date - Data de referência
 * @param {number} offset - Offset em semanas
 * @returns {Array<string>} Datas YYYY-MM-DD
 */
function getWeekDates(date, offset) {
  const d = new Date(date);
  const day = d.getDay();
  const diff = d.getDate() - day + (day === 0 ? -6 : 1); // Ajusta para segunda

  const monday = new Date(d.setDate(diff + (offset * 7)));

  const dates = [];
  for (let i = 0; i < 7; i++) {
    const day = new Date(monday);
    day.setDate(monday.getDate() + i);
    dates.push(formatDailyDate(day));
  }

  return dates;
}

/**
 * Resume um dia
 * @param {string} content - Conteúdo
 * @param {string} date - Data
 * @returns {Object} Resumo
 */
function summarizeDay(content, date) {
  const tasks = {
    open: (content.match(/- \[ \] (.+)/g) || []).map(m => m.replace(/- \[ \] /, '')),
    completed: (content.match(/- \[x\] (.+)/gi) || []).map(m => m.replace(/- \[x\] /i, '')),
  };

  return {
    date,
    exists: true,
    tasks,
    hasContent: content.length > 500,
    wordCount: content.split(/\s+/).filter(w => w.length > 0).length,
  };
}

// Exporta também como default
export default dailyWeekSummary;
