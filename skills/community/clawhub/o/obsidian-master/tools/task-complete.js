/"
 * @module tools/task-complete
 * @description Marca uma task como concluída
 */

import { CONFIG, getDefaultHeaders, buildUrl, normalizePath, successResponse, errorResponse, formatDailyDate } from '../config/defaults.js';

/**
 * Marca task como concluída
 * @param {Object} options - Opções
 * @param {string} options.notePath - Caminho da nota
 * @param {string} [options.taskText] - Texto parcial da task
 * @param {number} [options.lineNumber] - Número da linha
 * @returns {Promise<Object>} Resultado
 */
export async function taskComplete(options) {
  try {
    const {
      notePath,
      taskText,
      lineNumber,
    } = options;

    if (!notePath) {
      return errorResponse('Caminho da nota é obrigatório');
    }

    if (!taskText && !lineNumber) {
      return errorResponse('Texto da task ou número da linha é obrigatório');
    }

    if (!CONFIG.apiKey) {
      return errorResponse('OBSIDIAN_API_KEY não configurada');
    }

    const normalizedPath = normalizePath(notePath);

    // Lê nota
    const readResponse = await fetch(buildUrl(`/vault/${normalizedPath}`), {
      method: 'GET',
      headers: getDefaultHeaders(),
    });

    if (!readResponse.ok) {
      return errorResponse(`Nota não encontrada: ${normalizedPath}`);
    }

    let content = await readResponse.text();
    const lines = content.split('\n');

    let completedTask = null;

    if (lineNumber) {
      // Por número de linha
      const idx = lineNumber - 1;
      if (idx >= 0 && idx < lines.length && lines[idx].match(/^- \[ \]/)) {
        completedTask = lines[idx].replace('- [ ]', '- [x]');
        lines[idx] = completedTask + ` ✅ ${formatDailyDate(new Date())}`;
      }
    } else {
      // Por texto
      for (let i = 0; i < lines.length; i++) {
        if (lines[i].includes(taskText) && lines[i].match(/^- \[ \]/)) {
          completedTask = lines[i].replace('- [ ]', '- [x]');
          lines[i] = completedTask + ` ✅ ${formatDailyDate(new Date())}`;
          break;
        }
      }
    }

    if (!completedTask) {
      return errorResponse('Task não encontrada ou já concluída');
    }

    // Salva
    const newContent = lines.join('\n');
    const writeResponse = await fetch(buildUrl(`/vault/${normalizedPath}`), {
      method: 'PUT',
      headers: getDefaultHeaders(),
      body: newContent,
    });

    if (!writeResponse.ok) {
      throw new Error('Erro ao salvar');
    }

    return successResponse(
      `✅ Task concluída`,
      {
        notePath: normalizedPath,
        completedTask: completedTask.replace(/^- \[x\] /, ''),
      },
      '✅'
    );

  } catch (error) {
    return errorResponse(`Falha ao completar task: ${error.message}`, error);
  }
}

// Exporta também como default
export default taskComplete;
