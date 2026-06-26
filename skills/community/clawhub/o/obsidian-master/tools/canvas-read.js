/"
 * @module tools/canvas-read
 * @description Lê a estrutura completa de um canvas
 */

import { CONFIG, getDefaultHeaders, buildUrl, normalizePath, successResponse, errorResponse } from '../config/defaults.js';

/**
 * Lê um canvas
 * @param {Object} options - Opções
 * @param {string} options.path - Caminho do canvas
 * @returns {Promise<Object>} Estrutura do canvas
 */
export async function canvasRead(options) {
  try {
    const { path } = options;

    if (!path) {
      return errorResponse('Caminho do canvas é obrigatório');
    }

    if (!CONFIG.apiKey) {
      return errorResponse('OBSIDIAN_API_KEY não configurada');
    }

    const normalizedPath = normalizePath(path).replace(/\.md$/, '.canvas');

    const response = await fetch(buildUrl(`/vault/${normalizedPath}`), {
      method: 'GET',
      headers: getDefaultHeaders(),
    });

    if (!response.ok) {
      if (response.status === 404) {
        return errorResponse(`Canvas não encontrado: ${normalizedPath}`);
      }
      throw new Error(`Erro ${response.status}`);
    }

    const content = await response.text();
    const canvas = JSON.parse(content);

    return successResponse(
      `🎨 Canvas '${path.split('/').pop().replace('.canvas', '')}' carregado`,
      {
        path: normalizedPath,
        nodes: canvas.nodes || [],
        edges: canvas.edges || [],
        nodeCount: (canvas.nodes || []).length,
        edgeCount: (canvas.edges || []).length,
      },
      '🎨'
    );

  } catch (error) {
    return errorResponse(`Falha ao ler canvas: ${error.message}`, error);
  }
}

// Exporta também como default
export default canvasRead;
