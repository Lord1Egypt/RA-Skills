/"
 * @module tools/template-list
 * @description Lista templates disponíveis
 */

import { CONFIG, getDefaultHeaders, buildUrl, successResponse, errorResponse } from '../config/defaults.js';
import { folderList } from './folder-list.js';

/**
 * Lista templates disponíveis
 * @param {Object} options - Opções
 * @returns {Promise<Object>} Lista de templates
 */
export async function templateList(options = {}) {
  try {
    if (!CONFIG.apiKey) {
      return errorResponse('OBSIDIAN_API_KEY não configurada');
    }

    const templatesFolder = CONFIG.folders.templates;

    // Lista pasta de templates
    const listResult = await folderList({ path: templatesFolder });

    if (!listResult.success) {
      return errorResponse('Pasta de templates não encontrada');
    }

    const templates = listResult.data.files
      .filter(f => f.extension === 'md' && f.name.toLowerCase().includes('template'))
      .map(f => ({
        name: f.name,
        path: f.path,
        size: f.size,
      }));

    return successResponse(
      `📋 ${templates.length} template(s) encontrado(s)`,
      {
        folder: templatesFolder,
        templates,
        count: templates.length,
      },
      '📋'
    );

  } catch (error) {
    return errorResponse(`Falha ao listar templates: ${error.message}`, error);
  }
}

// Exporta também como default
export default templateList;
