/"
 * @module tools/link-create
 * @description Cria link entre duas notas
 */

import { CONFIG, getDefaultHeaders, buildUrl, normalizePath, successResponse, errorResponse } from '../config/defaults.js';

/**
 * Cria link entre notas
 * @param {Object} options - Opções
 * @param {string} options.fromPath - Nota origem
 * @param {string} options.toPath - Nota destino
 * @param {boolean} [options.bidirectional=true] - Link bidirecional
 * @param {string} [options.section] - Seção para adicionar
 * @param {string} [options.context] - Texto de contexto
 * @returns {Promise<Object>} Resultado
 */
export async function linkCreate(options) {
  try {
    const {
      fromPath,
      toPath,
      bidirectional = true,
      section,
      context,
    } = options;

    if (!fromPath || !toPath) {
      return errorResponse('Ambas as notas são obrigatórias');
    }

    if (!CONFIG.apiKey) {
      return errorResponse('OBSIDIAN_API_KEY não configurada');
    }

    const normalizedFrom = normalizePath(fromPath);
    const normalizedTo = normalizePath(toPath);

    const toName = normalizedTo.split('/').pop().replace('.md', '');
    const fromName = normalizedFrom.split('/').pop().replace('.md', '');

    // Adiciona link na origem
    await addLinkToNote(normalizedFrom, toName, section, context);

    // Adiciona link no destino (bidirecional)
    if (bidirectional) {
      await addLinkToNote(normalizedTo, fromName, null, `Referenciado por: ${fromName}`);
    }

    return successResponse(
      bidirectional
        ? `🔗 Link bidirecional criado entre '${fromName}' e '${toName}'`
        : `🔗 Link criado de '${fromName}' para '${toName}'`,
      {
        from: normalizedFrom,
        to: normalizedTo,
        bidirectional,
      },
      '🔗'
    );

  } catch (error) {
    return errorResponse(`Falha ao criar link: ${error.message}`, error);
  }
}

/**
 * Adiciona link em uma nota
 * @param {string} path - Caminho
 * @param {string} target - Nome da nota alvo
 * @param {string} section - Seção
 * @param {string} context - Contexto
 */
async function addLinkToNote(path, target, section, context) {
  const response = await fetch(buildUrl(`/vault/${path}`), {
    method: 'GET',
    headers: getDefaultHeaders(),
  });

  if (!response.ok) throw new Error(`Nota não encontrada: ${path}`);

  let content = await response.text();

  const linkText = context
    ? `[[${target}|${context}]]`
    : `[[${target}]]`;

  if (section) {
    const sectionRegex = new RegExp(`^(## ${section}.*)$`, 'm');
    if (sectionRegex.test(content)) {
      content = content.replace(sectionRegex, `$1\n${linkText}`);
    } else {
      content += `\n## ${section}\n${linkText}`;
    }
  } else {
    // Adiciona ao final
    content += `\n\n${linkText}`;
  }

  const writeResponse = await fetch(buildUrl(`/vault/${path}`), {
    method: 'PUT',
    headers: getDefaultHeaders(),
    body: content,
  });

  if (!writeResponse.ok) throw new Error('Erro ao salvar');
}

// Exporta também como default
export default linkCreate;
