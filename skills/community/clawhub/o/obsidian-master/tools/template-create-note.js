/"
 * @module tools/template-create-note
 * @description Cria nota a partir de template
 */

import { CONFIG, getDefaultHeaders, buildUrl, successResponse, errorResponse, formatDailyDate } from '../config/defaults.js';
import { noteCreate } from './note-create.js';

/**
 * Cria nota a partir de template
 * @param {Object} options - Opções
 * @param {string} options.title - Título da nota
 * @param {string} options.templatePath - Caminho do template
 * @param {string} [options.folder] - Pasta destino
 * @param {Object} [options.variables] - Variáveis adicionais
 * @returns {Promise<Object>} Nota criada
 */
export async function templateCreateNote(options) {
  try {
    const {
      title,
      templatePath,
      folder = CONFIG.folders.inbox,
      variables = {},
    } = options;

    if (!title || !templatePath) {
      return errorResponse('Título e caminho do template são obrigatórios');
    }

    if (!CONFIG.apiKey) {
      return errorResponse('OBSIDIAN_API_KEY não configurada');
    }

    // Lê template
    const response = await fetch(buildUrl(`/vault/${templatePath}`), {
      method: 'GET',
      headers: getDefaultHeaders(),
    });

    if (!response.ok) {
      return errorResponse(`Template não encontrado: ${templatePath}`);
    }

    let content = await response.text();

    // Substitui variáveis
    const now = new Date();
    const vars = {
      title,
      date: formatDailyDate(now),
      datetime: now.toISOString(),
      ...variables,
    };

    for (const [key, value] of Object.entries(vars)) {
      content = content.replace(new RegExp(`{{${key}}}`, 'g'), value);
    }

    // Cria nota com conteúdo do template
    return await noteCreate({
      title,
      content,
      folder,
      type: 'note',
    });

  } catch (error) {
    return errorResponse(`Falha ao criar nota do template: ${error.message}`, error);
  }
}

// Exporta também como default
export default templateCreateNote;
