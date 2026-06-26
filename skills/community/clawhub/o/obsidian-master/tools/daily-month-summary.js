/"
 * @module tools/daily-month-summary
 * @description Gera resumo do mês
 */

import { CONFIG, getDefaultHeaders, buildUrl, successResponse, errorResponse } from '../config/defaults.js';

/**
 * Gera resumo do mês
 * @param {Object} options - Opções
 * @param {number} [options.year] - Ano (padrão: atual)
 * @param {number} [options.month] - Mês (1-12, padrão: atual)
 * @returns {Promise<Object>} Resumo
 */
export async function dailyMonthSummary(options = {}) {
  try {
    const now = new Date();
    const year = options.year || now.getFullYear();
    const month = options.month || now.getMonth() + 1;

    if (!CONFIG.apiKey) {
      return errorResponse('OBSIDIAN_API_KEY não configurada');
    }

    const daysInMonth = new Date(year, month, 0).getDate();
    const summaries = [];
    let totalTasks = { open: 0, completed: 0 };
    let totalWords = 0;

    for (let day = 1; day <= daysInMonth; day++) {
      const date = `${year}-${String(month).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
      const filePath = `${CONFIG.folders.daily}/${date}.md`;

      try {
        const response = await fetch(buildUrl(`/vault/${filePath}`), {
          method: 'GET',
          headers: getDefaultHeaders(),
        });

        if (response.ok) {
          const content = await response.text();
          const open = (content.match(/- \[ \]/g) || []).length;
          const completed = (content.match(/- \[x\]/gi) || []).length;
          const words = content.split(/\s+/).filter(w => w.length > 0).length;

          summaries.push({
            date,
            exists: true,
            tasks: { open, completed },
            words,
          });

          totalTasks.open += open;
          totalTasks.completed += completed;
          totalWords += words;
        } else {
          summaries.push({ date, exists: false });
        }
      } catch {
        summaries.push({ date, exists: false });
      }
    }

    const monthName = new Date(year, month - 1).toLocaleString('pt-BR', { month: 'long', year: 'numeric' });

    return successResponse(
      `📊 Resumo de ${monthName}`,
      {
        month: monthName,
        year,
        monthNumber: month,
        days: summaries,
        stats: {
          daysWithNotes: summaries.filter(s => s.exists).length,
          totalTasks,
          totalWords,
          completion: totalTasks.completed + totalTasks.open > 0
            ? Math.round((totalTasks.completed / (totalTasks.completed + totalTasks.open)) * 100)
            : 0,
          averageWordsPerDay: Math.round(totalWords / daysInMonth),
        },
      },
      '📊'
    );

  } catch (error) {
    return errorResponse(`Falha ao gerar resumo: ${error.message}`, error);
  }
}

// Exporta também como default
export default dailyMonthSummary;
