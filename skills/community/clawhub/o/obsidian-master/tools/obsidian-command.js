/"
 * @module tools/obsidian-command
 * @description Executa comandos do Obsidian
 */

import { CONFIG, getDefaultHeaders, buildUrl, successResponse, errorResponse } from '../config/defaults.js';

/**
 * Executa um comando do Obsidian
 * @param {Object} options - Opções
 * @param {string} options.command - ID do comando
 * @returns {Promise<Object>} Resultado
 */
export async function obsidianCommand(options) {
  try {
    const { command } = options;

    if (!command) {
      return errorResponse('ID do comando é obrigatório');
    }

    if (!CONFIG.apiKey) {
      return errorResponse('OBSIDIAN_API_KEY não configurada');
    }

    const response = await fetch(buildUrl(`/commands/${command}/`), {
      method: 'POST',
      headers: getDefaultHeaders(),
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Erro ${response.status}: ${errorText}`);
    }

    return successResponse(
      `⚡ Comando '${command}' executado`,
      { command },
      '⚡'
    );

  } catch (error) {
    return errorResponse(`Falha ao executar comando: ${error.message}`, error);
  }
}

/**
 * Lista comandos disponíveis
 * @returns {Promise<Object>} Lista de comandos
 */
export async function listCommands() {
  try {
    const response = await fetch(buildUrl('/commands/'), {
      method: 'GET',
      headers: getDefaultHeaders(),
    });

    if (!response.ok) {
      throw new Error('Erro ao listar comandos');
    }

    const commands = await response.json();

    return successResponse(
      `⚡ ${commands.length} comando(s) disponíveis`,
      { commands },
      '⚡'
    );

  } catch (error) {
    return errorResponse(`Falha ao listar comandos: ${error.message}`, error);
  }
}

// Exporta também como default
export default obsidianCommand;
