/"
 * @module tools/note-merge
 * @description Mescla duas notas em uma
 */

import { CONFIG, getDefaultHeaders, buildUrl, normalizePath, successResponse, errorResponse } from '../config/defaults.js';

/**
 * Mescla duas notas
 * @param {Object} options - Opções
 * @param {string} options.primary - Nota primária (mantida)
 * @param {string} options.secondary - Nota secundária (mesclada e deletada)
 * @param {string} [options.separator='\n\n---\n\n'] - Separador entre conteúdos
 * @param {boolean} [options.deleteSecondary=true] - Deletar nota secundária
 * @returns {Promise<Object>} Resultado
 */
export async function noteMerge(options) {
  try {
    const {
      primary,
      secondary,
      separator = '\n\n---\n\n',
      deleteSecondary = true,
    } = options;

    if (!primary || !secondary) {
      return errorResponse('Ambas as notas são obrigatórias');
    }

    if (!CONFIG.apiKey) {
      return errorResponse('OBSIDIAN_API_KEY não configurada');
    }

    const primaryPath = normalizePath(primary);
    const secondaryPath = normalizePath(secondary);

    if (primaryPath === secondaryPath) {
      return errorResponse('As notas são iguais');
    }

    // Lê ambas
    const [primaryResponse, secondaryResponse] = await Promise.all([
      fetch(buildUrl(`/vault/${primaryPath}`), { method: 'GET', headers: getDefaultHeaders() }),
      fetch(buildUrl(`/vault/${secondaryPath}`), { method: 'GET', headers: getDefaultHeaders() }),
    ]);

    if (!primaryResponse.ok) {
      return errorResponse(`Nota primária não encontrada: ${primaryPath}`);
    }

    if (!secondaryResponse.ok) {
      return errorResponse(`Nota secundária não encontrada: ${secondaryPath}`);
    }

    const primaryContent = await primaryResponse.text();
    const secondaryContent = await secondaryResponse.text();

    // Extrai body do secondary (sem frontmatter)
    const secondaryBody = secondaryContent.replace(/^---\n[\s\S]*?\n---\n?/, '').trim();

    // Mescla
    const mergedContent = primaryContent + separator +
      `**Mesclado de:** [[${secondaryPath.split('/').pop().replace('.md', '')}]]\n\n` +
      secondaryBody;

    // Salva primária
    await fetch(buildUrl(`/vault/${primaryPath}`), {
      method: 'PUT',
      headers: getDefaultHeaders(),
      body: mergedContent,
    });

    // Deleta secundária se solicitado
    if (deleteSecondary) {
      await fetch(buildUrl(`/vault/${secondaryPath}`), {
        method: 'DELETE',
        headers: getDefaultHeaders(),
      });
    }

    return successResponse(
      `🔀 Notas mescladas em '${primaryPath.split('/').pop()}'`,
      {
        primary: primaryPath,
        secondary: secondaryPath,
        deleted: deleteSecondary,
      },
      '✅'
    );

  } catch (error) {
    return errorResponse(`Falha ao mesclar notas: ${error.message}`, error);
  }
}

// Exporta também como default
export default noteMerge;
