/"
 * @module tools/note-move
 * @description Move uma nota entre pastas
 */

import { CONFIG, getDefaultHeaders, buildUrl, normalizePath, successResponse, errorResponse } from '../config/defaults.js';

/**
 * Move uma nota para outra pasta
 * @param {Object} options - Opções
 * @param {string} options.path - Caminho atual
 * @param {string} options.destination - Pasta destino
 * @param {boolean} [options.updateLinks=true] - Atualizar links internos
 * @returns {Promise<Object>} Resultado
 */
export async function noteMove(options) {
  try {
    const {
      path,
      destination,
      updateLinks = true,
    } = options;

    if (!path || !destination) {
      return errorResponse('Caminho atual e destino são obrigatórios');
    }

    if (!CONFIG.apiKey) {
      return errorResponse('OBSIDIAN_API_KEY não configurada');
    }

    const normalizedPath = normalizePath(path);
    const fileName = normalizedPath.split('/').pop();
    const newPath = `${destination}/${fileName}`;

    // Lê conteúdo
    const readResponse = await fetch(buildUrl(`/vault/${normalizedPath}`), {
      method: 'GET',
      headers: getDefaultHeaders(),
    });

    if (!readResponse.ok) {
      return errorResponse(`Nota não encontrada: ${normalizedPath}`);
    }

    let content = await readResponse.text();

    // Cria na nova localização
    const createResponse = await fetch(buildUrl(`/vault/${newPath}`), {
      method: 'PUT',
      headers: getDefaultHeaders(),
      body: content,
    });

    if (!createResponse.ok) {
      throw new Error('Erro ao criar na nova pasta');
    }

    // Deleta original
    const deleteResponse = await fetch(buildUrl(`/vault/${normalizedPath}`), {
      method: 'DELETE',
      headers: getDefaultHeaders(),
    });

    if (!deleteResponse.ok) {
      // Rollback
      await fetch(buildUrl(`/vault/${newPath}`), {
        method: 'DELETE',
        headers: getDefaultHeaders(),
      });
      throw new Error('Erro ao deletar original');
    }

    return successResponse(
      `📁 Nota movida para ${destination}`,
      {
        original: normalizedPath,
        new: newPath,
        updateLinks,
      },
      '✅'
    );

  } catch (error) {
    return errorResponse(`Falha ao mover nota: ${error.message}`, error);
  }
}

// Exporta também como default
export default noteMove;
