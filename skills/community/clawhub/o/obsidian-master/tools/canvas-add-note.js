/"
 * @module tools/canvas-add-note
 * @description Adiciona uma nota existente como nó no canvas
 */

import { CONFIG, getDefaultHeaders, buildUrl, normalizePath, successResponse, errorResponse } from '../config/defaults.js';
import { canvasRead } from './canvas-read.js';

/**
 * Adiciona uma nota como nó no canvas
 * @param {Object} options - Opções
 * @param {string} options.canvasPath - Caminho do canvas
 * @param {string} options.notePath - Caminho da nota
 * @param {number} [options.x=0] - Posição X
 * @param {number} [options.y=0] - Posição Y
 * @param {number} [options.width=400] - Largura
 * @param {number} [options.height=400] - Altura
 * @param {string} [options.color] - Cor
 * @returns {Promise<Object>} Resultado
 */
export async function canvasAddNote(options) {
  try {
    const {
      canvasPath,
      notePath,
      x = 0,
      y = 0,
      width = 400,
      height = 400,
      color,
    } = options;

    if (!canvasPath || !notePath) {
      return errorResponse('Caminhos do canvas e nota são obrigatórios');
    }

    if (!CONFIG.apiKey) {
      return errorResponse('OBSIDIAN_API_KEY não configurada');
    }

    const normalizedCanvasPath = normalizePath(canvasPath).replace(/\.md$/, '.canvas');
    const normalizedNotePath = normalizePath(notePath);

    // Verifica se nota existe
    const noteCheck = await fetch(buildUrl(`/vault/${normalizedNotePath}`), {
      method: 'HEAD',
      headers: getDefaultHeaders(),
    });

    if (!noteCheck.ok) {
      return errorResponse(`Nota não encontrada: ${normalizedNotePath}`);
    }

    // Lê canvas
    const readResult = await canvasRead({ path: normalizedCanvasPath });
    if (!readResult.success) {
      return readResult;
    }

    const canvas = {
      nodes: readResult.data.nodes || [],
      edges: readResult.data.edges || [],
    };

    // Cria nó do tipo file
    const id = generateId();
    const node = {
      id,
      type: 'file',
      file: normalizedNotePath,
      x,
      y,
      width,
      height,
    };

    if (color) node.color = color;

    canvas.nodes.push(node);

    // Salva
    const response = await fetch(buildUrl(`/vault/${normalizedCanvasPath}`), {
      method: 'PUT',
      headers: getDefaultHeaders(),
      body: JSON.stringify(canvas, null, 2),
    });

    if (!response.ok) {
      throw new Error('Erro ao salvar canvas');
    }

    return successResponse(
      `📄 Nota '${notePath.split('/').pop()}' adicionada ao canvas`,
      {
        canvasPath: normalizedCanvasPath,
        notePath: normalizedNotePath,
        nodeId: id,
        nodeCount: canvas.nodes.length,
      },
      '✅'
    );

  } catch (error) {
    return errorResponse(`Falha ao adicionar nota: ${error.message}`, error);
  }
}

/**
 * Gera ID único
 * @returns {string} ID
 */
function generateId() {
  return Date.now().toString(36) + Math.random().toString(36).substr(2);
}

// Exporta também como default
export default canvasAddNote;
