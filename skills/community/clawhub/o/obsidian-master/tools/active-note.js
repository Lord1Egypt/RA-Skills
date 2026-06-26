/**
 * @module tools/active-note
 * @description Obtém informações sobre a nota atualmente aberta
 */

import { CONFIG, getDefaultHeaders, buildUrl, successResponse, errorResponse } from '../config/defaults.js';

/**
 * Obtém informações da nota ativa
 * @returns {Promise<Object>} Informações da nota
 */
export async function activeNote() {
  try {
    if (!CONFIG.apiKey) {
      return errorResponse('OBSIDIAN_API_KEY não configurada');
    }

    const response = await fetch(buildUrl('/active/'), {
      method: 'GET',
      headers: getDefaultHeaders(),
    });

    if (!response.ok) {
      throw new Error('Não foi possível obter a nota ativa');
    }

    const data = await response.json();

    return successResponse(
      '📄 Nota ativa obtida',
      data,
      '📄'
    );

  } catch (error) {
    return errorResponse(`Falha ao obter nota ativa: ${error.message}`, error);
  }
}

export default activeNote;
