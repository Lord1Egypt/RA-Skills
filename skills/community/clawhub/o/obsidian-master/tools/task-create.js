/"
 * @module tools/task-create
 * @description Cria uma task em uma nota
 */

import { CONFIG, getDefaultHeaders, buildUrl, normalizePath, successResponse, errorResponse, formatDailyDate } from '../config/defaults.js';

/**
 * Cria uma task em uma nota
 * @param {Object} options - Opções
 * @param {string} options.notePath - Caminho da nota
 * @param {string} options.text - Texto da task
 * @param {string} [options.section] - Seção para adicionar
 * @param {string} [options.priority] - Prioridade (!, !!, !!!)
 * @param {string} [options.dueDate] - Data de vencimento
 * @returns {Promise<Object>} Task criada
 */
export async function taskCreate(options) {
  try {
    const {
      notePath,
      text,
      section = 'Tasks',
      priority,
      dueDate,
    } = options;

    if (!notePath || !text) {
      return errorResponse('Caminho da nota e texto da task são obrigatórios');
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

    let content = '';
    if (readResponse.ok) {
      content = await readResponse.text();
    } else {
      // Cria nota nova
      content = `---\ntitle: "Tasks"\ncreated: ${formatDailyDate(new Date())}\ntype: note\ntags: [tasks]\n---\n\n# Tasks\n`;
    }

    // Monta task
    let taskText = text;
    if (dueDate) taskText += ` 📅 ${dueDate}`;
    if (priority === 'high') taskText = `!! ${taskText}`;
    else if (priority === 'highest') taskText = `!!! ${taskText}`;
    else if (priority === 'low') taskText = `! ${taskText}`;

    const taskLine = `- [ ] ${taskText}`;

    // Adiciona à seção
    const sectionRegex = new RegExp(`^(## ${section}.*)$`, 'm');
    if (sectionRegex.test(content)) {
      content = content.replace(sectionRegex, `$1\n${taskLine}`);
    } else {
      content += `\n## ${section}\n${taskLine}`;
    }

    // Salva
    const writeResponse = await fetch(buildUrl(`/vault/${normalizedPath}`), {
      method: 'PUT',
      headers: getDefaultHeaders(),
      body: content,
    });

    if (!writeResponse.ok) {
      throw new Error('Erro ao salvar');
    }

    return successResponse(
      `✅ Task criada em '${normalizedPath.split('/').pop()}'`,
      {
        notePath: normalizedPath,
        taskText,
        section,
      },
      '✅'
    );

  } catch (error) {
    return errorResponse(`Falha ao criar task: ${error.message}`, error);
  }
}

// Exporta também como default
export default taskCreate;
