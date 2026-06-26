/"
 * @module tools/canvas-connect
 * @description Conecta dois nós do canvas com uma aresta
 */

import { CONFIG, getDefaultHeaders, buildUrl, normalizePath, successResponse, errorResponse } from '../config/defaults.js';
import { canvasRead } from './canvas-read.js';

/**
 * Conecta dois nós no canvas
 * @param {Object} options - Opções
 * @param {string} options.canvasPath - Caminho do canvas
 * @param {string} options.fromNode - ID do nó origem
 * @param {string} options.toNode - ID do nó destino
 * @param {string} [options.label] - Rótulo da conexão
 * @param {string} [options.color] - Cor da aresta
 * @param {string} [options.fromSide='right'] - Lado origem (top/bottom/left/right)
 * @param {string} [options.toSide='left'] - Lado destino
 * @returns {Promise<Object>} Resultado
 */
export async function canvasConnect(options) {
  try {
    const {
      canvasPath,
      fromNode,
      toNode,
      label,
      color,
      fromSide = 'right',
      toSide = 'left',
    } = options;

    if (!canvasPath || !fromNode || !toNode) {
      return errorResponse('Caminho do canvas, nó origem e nó destino são obrigatórios');
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

    // Verifica se nós existem
    const fromExists = canvas.nodes.some(n => n.id === fromNode);
    const toExists = canvas.nodes.some(n => n.id === toNode);

    if (!fromExists) {
      return errorResponse(`Nó origem '${fromNode}' não encontrado`);
    }

    if (!toExists) {
      return errorResponse(`Nó destino '${toNode}' não encontrado`);
    }

    // Cria aresta
    const edge = {
      id: generateId(),
      fromNode,
      toNode,
      fromSide,
      toSide,
    };

    if (label) edge.label = label;
    if (color) edge.color = color;

    canvas.edges.push(edge);

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
      `🔗 Conexão criada entre nós`,
      {
        canvasPath: normalizedPath,
        edgeId: edge.id,
        fromNode,
        toNode,
        edgeCount: canvas.edges.length,
      },
      '✅'
    );

  } catch (error) {
    return errorResponse(`Falha ao conectar nós: ${error.message}`, error);
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
export default canvasConnect;
