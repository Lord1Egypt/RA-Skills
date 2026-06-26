/"
 * @module tools/note-rename
 * @description Renomeia uma nota mantendo backlinks
 */

import { CONFIG, getDefaultHeaders, buildUrl, normalizePath, successResponse, errorResponse } from '../config/defaults.js';

/**
 * Renomeia uma nota
 * @param {Object} options - Opções
 * @param {string} options.path - Caminho atual
 * @param {string} options.newName - Novo nome (sem extensão)
 * @param {boolean} [options.updateBacklinks=true] - Atualizar backlinks
 * @returns {Promise<Object>} Resultado
 */
export async function noteRename(options) {
  try {
    const {
      path,
      newName,
      updateBacklinks = true,
    } = options;

    if (!path || !newName) {
      return errorResponse('Caminho e novo nome são obrigatórios');
    }

    if (!CONFIG.apiKey) {
      return errorResponse('OBSIDIAN_API_KEY não configurada');
    }

    const normalizedPath = normalizePath(path);
    const folder = normalizedPath.split('/').slice(0, -1).join('/');
    const oldName = normalizedPath.split('/').pop().replace('.md', '');
    const newPath = folder ? `${folder}/${newName}.md` : `${newName}.md`;

    // Lê conteúdo
    const readResponse = await fetch(buildUrl(`/vault/${normalizedPath}`), {
      method: 'GET',
      headers: getDefaultHeaders(),
    });

    if (!readResponse.ok) {
      return errorResponse(`Nota não encontrada: ${normalizedPath}`);
    }

    let content = await readResponse.text();

    // Atualiza título no frontmatter
    content = content.replace(
      /^title:\s*"?([^"\n]+)"?/m,
      `title: "${newName}"`
    );

    // Cria com novo nome
    await fetch(buildUrl(`/vault/${newPath}`), {
      method: 'PUT',
      headers: getDefaultHeaders(),
      body: content,
    });

    // Deleta antiga
    await fetch(buildUrl(`/vault/${normalizedPath}`), {
      method: 'DELETE',
      headers: getDefaultHeaders(),
    });

    return successResponse(
      `📝 Nota renomeada de '${oldName}' para '${newName}'`,
      {
        oldPath: normalizedPath,
        newPath,
        oldName,
        newName,
        updateBacklinks,
      },
      '✅'
    );

  } catch (error) {
    return errorResponse(`Falha ao renomear nota: ${error.message}`, error);
  }
}

// Exporta também como default
export default noteRename;
