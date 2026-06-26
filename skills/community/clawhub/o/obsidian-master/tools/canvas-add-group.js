/"
 * @module tools/canvas-add-group
 * @description Cria um grupo de nós no canvas
 */

import { CONFIG, getDefaultHeaders, buildUrl, normalizePath, successResponse, errorResponse } from '../config/defaults.js';
import { canvasRead } from './canvas-read.js';

/**
 * Adiciona um grupo ao canvas
 * @param {Object} options - Opções
 * @param {string} options.canvasPath - Caminho do canvas
 * @param {string} options.label - Rótulo do grupo
 * @param {number} options.x - Posição X
 * @param {number} options.y - Posição Y
 * @param {number} options.width - Largura
 * @param {number} options.height - Altura
 * @param {string} [options.color] - Cor de fundo
 * @param {string} [options.labelColor] - Cor do texto
 * @returns {Promise<Object>} Resultado
 */
export async function canvasAddGroup(options) {
  try {
    const {
      canvasPath,
      label,
      x = 0,
      y = 0,
      width = 400,
      height = 300,
      color,
    } = options;

    if (!canvasPath) {
      return errorResponse('Caminho do canvas é obrigatório');
    }

    if (!CONFIG.apiKey) {
      return errorResponse('OBSIDIAN_API_KEY não configurada');
    }

    const normalizedPath = normalizePath(canvasPath).replace(/\.md$/, '.canvas');

    // Lê canvas
    const readResult = await canvasRead({ path: normalizedPath });
    if (!readResult.success) {
      return readResult;
    }

    const canvas = {
      nodes: readResult.data.nodes || [],
      edges: readResult.data.edges || [],
    };

    // Cria grupo
    const id = generateId();
    const node = {
      id,
      type: 'group',
      label: label || 'Grupo',
      x,
      y,
      width,
      height,
    };

    if (color) {
      node.color = color;
    }

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
      `📦 Grupo '${label}' adicionado ao canvas`,
      {
        canvasPath: normalizedPath,
        groupId: id,
        nodeCount: canvas.nodes.length,
      },
      '✅'
    );

  } catch (error) {
    return errorResponse(`Falha ao adicionar grupo: ${error.message}`, error);
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
export default canvasAddGroup;
