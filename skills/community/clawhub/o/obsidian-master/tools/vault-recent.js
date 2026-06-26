/"
 * @module tools/vault-recent
 * @description Lista notas modificadas recentemente
 */

import { CONFIG, getDefaultHeaders, buildUrl, successResponse, errorResponse } from '../config/defaults.js';
import { searchByDate } from './search-by-date.js';

/**
 * Lista notas recentes
 * @param {Object} options - Opções
 * @param {number} [options.days=7] - Quantos dias atrás
 * @returns {Promise<Object>} Notas recentes
 */
export async function vaultRecent(options = {}) {
  try {
    const { days = 7 } = options;

    const today = new Date();
    const past = new Date(today.getTime() - days * 24 * 60 * 60 * 1000);

    return await searchByDate({
      from: past.toISOString().split('T')[0],
      to: today.toISOString().split('T')[0],
    });

  } catch (error) {
    return errorResponse(`Falha ao buscar notas recentes: ${error.message}`, error);
  }
}

export default vaultRecent;
