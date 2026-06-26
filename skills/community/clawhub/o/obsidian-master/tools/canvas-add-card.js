/"
 * @module tools/canvas-add-card
 * @description Adiciona um card de texto a um canvas
 */

import { CONFIG, getDefaultHeaders, buildUrl, normalizePath, successResponse, errorResponse } from '../config/defaults.js';
import { canvasRead } from './canvas-read.js';

/**
 * Adiciona um card de texto ao canvas
 * @param {Object} options - Opções
 * @param {string} options.canvasPath - Caminho do canvas
 * @param {string} options.text - Texto do card
 * @param {number} [options.x=0] - Posição X
 * @param {number} [options.y=0] - Posição Y
 * @param {number} [options.width=250] - Largura
 * @param {number} [options.height] - Altura (auto se não especificado)
 * @param {string} [options.color] - Cor (1-6 ou nome)
 * @returns {Promise<Object>} Resultado
 */
export async function canvasAddCard(options) {
  try {
    const {
      canvasPath,
      text,
      x = 0,
      y = 0,
      width = 250,
      height,
      color,
    } = options;

    if (!canvasPath || !text) {
      return errorResponse('Caminho do canvas e texto são obrigatórios');
    }

    if (!CONFIG.apiKey) {
      return errorResponse('OBSIDIAN_API_KEY não configurada');
    }

    const normalizedPath = normalizePath(canvasPath).replace(/\.md$/, '.canvas');

    // Lê canvas atual
    const readResult = await canvasRead({ path: normalizedPath });
    if (!readResult.success) {
      return readResult;
    }

    const canvas = {
      nodes: readResult.data.nodes || [],
      edges: readResult.data.edges || [],
    };

    // Gera ID único
    const id = generateId();

    // Cria novo nó
    const node = {
      id,
      type: 'text',
      text,
      x,
      y,
      width,
    };

    if (height) node.height = height;
    if (color) node.color = color;

    canvas.nodes.push(node);

    // Salva
    const response = await fetch(buildUrl(`/vault/${normalizedPath}`), {
      method: 'PUT',
      headers: getDefaultHeaders(),
      body: JSON.stringify(canvas, null, 2),
    });

    if (!response.ok) {
      throw new Error('Erro ao salvar canvas');
    }

    return successResponse(
      `📝 Card adicionado ao canvas`,
      {
        canvasPath: normalizedPath,
        nodeId: id,
        nodeCount: canvas.nodes.length,
      },
      '✅'
    );

  } catch (error) {
    return errorResponse(`Falha ao adicionar card: ${error.message}`, error);
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
export default canvasAddCard;
