/**
 * @module tools/canvas-create
 * @description Cria um novo arquivo Canvas do zero
 */

import { CONFIG, getDefaultHeaders, buildUrl, successResponse, errorResponse, formatDailyDate } from '../config/defaults.js';

/**
 * Cria um novo canvas
 * @param {Object} options - Opções
 * @param {string} options.name - Nome do canvas
 * @param {string} [options.folder] - Pasta (padrão: 60 - Canvas)
 * @param {Object} [options.initialNodes] - Nós iniciais
 * @param {boolean} [options.open=false] - Abrir após criar
 * @returns {Promise<Object>} Canvas criado
 */
export async function canvasCreate(options) {
  try {
    const {
      name,
      folder = CONFIG.folders.canvas,
      initialNodes = [],
      open = false,
    } = options;

    if (!name) {
      return errorResponse('Nome do canvas é obrigatório');
    }

    if (!CONFIG.apiKey) {
      return errorResponse('OBSIDIAN_API_KEY não configurada');
    }

    const fileName = name.endsWith('.canvas') ? name : `${name}.canvas`;
    const filePath = folder ? `${folder}/${fileName}` : fileName;

    // Estrutura básica do canvas
    const canvasData = {
      nodes: initialNodes.length > 0 ? initialNodes : [],
      edges: [],
    };

    // Cria o arquivo
    const response = await fetch(buildUrl(`/vault/${filePath}`), {
      method: 'PUT',
      headers: getDefaultHeaders(),
      body: JSON.stringify(canvasData, null, 2),
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Erro ${response.status}: ${errorText}`);
    }

    // Abre se solicitado
    if (open) {
      await fetch(buildUrl(`/open/${filePath}`), {
        method: 'POST',
        headers: getDefaultHeaders(),
      });
    }

    return successResponse(
      `🎨 Canvas '${name}' criado`,
      {
        path: filePath,
        name: fileName.replace('.canvas', ''),
        nodeCount: canvasData.nodes.length,
        edgeCount: canvasData.edges.length,
      },
      '🎨'
    );

  } catch (error) {
    return errorResponse(`Falha ao criar canvas: ${error.message}`, error);
  }
}

// Exporta também como default
export default canvasCreate;
