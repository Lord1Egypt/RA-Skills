/"
 * @module tools/daily-read
 * @description Lê a daily note de uma data específica
 */

import { CONFIG, getDefaultHeaders, buildUrl, successResponse, errorResponse, formatDailyDate } from '../config/defaults.js';

/**
 * Lê uma daily note
 * @param {Object} options - Opções
 * @param {string} [options.date] - Data (padrão: hoje)
 * @param {string} [options.format='raw'] - Formato: 'raw' ou 'parsed'
 * @returns {Promise<Object>} Conteúdo
 */
export async function dailyRead(options = {}) {
  try {
    const {
      date = formatDailyDate(new Date()),
      format = 'raw',
    } = options;

    if (!CONFIG.apiKey) {
      return errorResponse('OBSIDIAN_API_KEY não configurada');
    }

    const dailyFolder = CONFIG.folders.daily;
    const fileName = `${date}.md`;
    const filePath = `${dailyFolder}/${fileName}`;

    const response = await fetch(buildUrl(`/vault/${filePath}`), {
      method: 'GET',
      headers: getDefaultHeaders(),
    });

    if (!response.ok) {
      if (response.status === 404) {
        return errorResponse(`Daily note não encontrada: ${date}`);
      }
      throw new Error(`Erro ${response.status}`);
    }

    const content = await response.text();

    let result = { content };

    if (format === 'parsed') {
      result = {
        ...result,
        ...parseDaily(content),
      };
    }

    return successResponse(
      `📅 Daily de ${date}`,
      {
        path: filePath,
        date,
        ...result,
      },
      '📅'
    );

  } catch (error) {
    return errorResponse(`Falha ao ler daily: ${error.message}`, error);
  }
}

/**
 * Parseia conteúdo da daily
 * @param {string} content - Conteúdo
 * @returns {Object} Seções
 */
function parseDaily(content) {
  const sections = {};
  const lines = content.split('\n');
  let currentSection = null;

  for (const line of lines) {
    // Detecta headers
    const headerMatch = line.match(/^(#{1,3})\s+(.+)$/);
    if (headerMatch) {
      currentSection = headerMatch[2].trim();
      sections[currentSection] = [];
    } else if (currentSection && line.trim()) {
      sections[currentSection].push(line);
    }
  }

  // Extrai tasks
  const tasks = {
    open: (content.match(/- \[ \] (.+)/g) || []).map(m => m.replace(/- \[ \] /, '')),
    completed: (content.match(/- \[x\] (.+)/gi) || []).map(m => m.replace(/- \[x\] /i, '')),
  };

  return {
    sections,
    tasks,
    lineCount: lines.length,
    wordCount: content.split(/\s+/).filter(w => w.length > 0).length,
  };
}

// Exporta também como default
export default dailyRead;
