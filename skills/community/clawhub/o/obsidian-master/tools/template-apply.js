/"
 * @module tools/template-apply
 * @description Aplica um template a uma nota existente
 */

import { CONFIG, getDefaultHeaders, buildUrl, normalizePath, successResponse, errorResponse } from '../config/defaults.js';

/**
 * Aplica template a uma nota
 * @param {Object} options - Opções
 * @param {string} options.notePath - Caminho da nota
 * @param {string} options.templatePath - Caminho do template
 * @param {Object} [options.variables] - Variáveis para substituir
 * @param {boolean} [options.preserveContent=true] - Preservar conteúdo existente
 * @returns {Promise<Object>} Resultado
 */
export async function templateApply(options) {
  try {
    const {
      notePath,
      templatePath,
      variables = {},
      preserveContent = true,
    } = options;

    if (!notePath || !templatePath) {
      return errorResponse('Caminho da nota e do template são obrigatórios');
    }

    if (!CONFIG.apiKey) {
      return errorResponse('OBSIDIAN_API_KEY não configurada');
    }

    const normalizedNote = normalizePath(notePath);
    const normalizedTemplate = normalizePath(templatePath);

    // Lê template
    const templateResponse = await fetch(buildUrl(`/vault/${normalizedTemplate}`), {
      method: 'GET',
      headers: getDefaultHeaders(),
    });

    if (!templateResponse.ok) {
      return errorResponse(`Template não encontrado: ${templatePath}`);
    }

    let templateContent = await templateResponse.text();

    // Substitui variáveis
    const now = new Date();
    const defaultVars = {
      date: now.toISOString().split('T')[0],
      time: now.toLocaleTimeString('pt-BR'),
      title: normalizedNote.split('/').pop().replace('.md', ''),
      ...variables,
    };

    for (const [key, value] of Object.entries(defaultVars)) {
      templateContent = templateContent.replace(
        new RegExp(`{{${key}}}`, 'g'),
        value
      );
    }

    // Lê nota atual
    const noteResponse = await fetch(buildUrl(`/vault/${normalizedNote}`), {
      method: 'GET',
      headers: getDefaultHeaders(),
    });

    let finalContent = templateContent;

    if (noteResponse.ok && preserveContent) {
      const currentContent = await noteResponse.text();
      // Adiciona conteúdo atual após o template
      finalContent = templateContent + '\n\n' + currentContent;
    }

    // Salva
    const writeResponse = await fetch(buildUrl(`/vault/${normalizedNote}`), {
      method: 'PUT',
      headers: getDefaultHeaders(),
      body: finalContent,
    });

    if (!writeResponse.ok) {
      throw new Error('Erro ao aplicar template');
    }

    return successResponse(
      `📋 Template aplicado a '${normalizedNote.split('/').pop()}'`,
      {
        notePath: normalizedNote,
        templatePath: normalizedTemplate,
        variables: Object.keys(defaultVars),
      },
      '✅'
    );

  } catch (error) {
    return errorResponse(`Falha ao aplicar template: ${error.message}`, error);
  }
}

// Exporta também como default
export default templateApply;
