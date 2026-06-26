/"
 * @module tools/template-create
 * @description Cria um novo template
 */

import { CONFIG, getDefaultHeaders, buildUrl, successResponse, errorResponse } from '../config/defaults.js';

/**
 * Cria um novo template
 * @param {Object} options - Opções
 * @param {string} options.name - Nome do template
 * @param {string} options.content - Conteúdo do template
 * @param {string} [options.folder] - Pasta de templates
 * @returns {Promise<Object>} Template criado
 */
export async function templateCreate(options) {
  try {
    const {
      name,
      content,
      folder = CONFIG.folders.templates,
    } = options;

    if (!name || !content) {
      return errorResponse('Nome e conteúdo são obrigatórios');
    }

    if (!CONFIG.apiKey) {
      return errorResponse('OBSIDIAN_API_KEY não configurada');
    }

    const fileName = name.endsWith('.md') ? name : `${name}.md`;
    const filePath = `${folder}/${fileName}`;

    const response = await fetch(buildUrl(`/vault/${filePath}`), {
      method: 'PUT',
      headers: getDefaultHeaders(),
      body: content,
    });

    if (!response.ok) {
      throw new Error('Erro ao criar template');
    }

    return successResponse(
      `📋 Template '${name}' criado`,
      {
        path: filePath,
        name: fileName.replace('.md', ''),
      },
      '✅'
    );

  } catch (error) {
    return errorResponse(`Falha ao criar template: ${error.message}`, error);
  }
}

// Exporta também como default
export default templateCreate;
