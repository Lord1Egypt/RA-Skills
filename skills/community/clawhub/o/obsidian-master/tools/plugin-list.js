/**
 * @module tools/plugin-list
 * @description Lista plugins instalados (requere permissões especiais)
 */

import { CONFIG, getDefaultHeaders, buildUrl, successResponse, errorResponse } from '../config/defaults.js';

/**
 * Lista plugins do Obsidian
 * @returns {Promise<Object>} Lista de plugins
 */
export async function pluginList() {
  return errorResponse('Plugin list requer integração direta com Obsidian. Use a API REST para operações em notas.');
}

export default pluginList;
