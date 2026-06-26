/"
 * @module tools/note-duplicate
 * @description Duplica uma nota
 */

import { CONFIG, getDefaultHeaders, buildUrl, normalizePath, successResponse, errorResponse, formatDailyDate } from '../config/defaults.js';

/**
 * Duplica uma nota
 * @param {Object} options - Opções
 * @param {string} options.path - Caminho da nota original
 * @param {string} [options.newName] - Nome da cópia (padrão: "Nome (Cópia)")
 * @param {string} [options.folder] - Pasta da cópia (padrão: mesma da original)
 * @param {boolean} [options.includeTimestamp=true] - Adicionar timestamp
 * @returns {Promise<Object>} Cópia criada
 */
export async function noteDuplicate(options) {
  try {
    const {
      path,
      newName,
      folder,
      includeTimestamp = true,
    } = options;

    if (!path) {
      return errorResponse('Caminho da nota é obrigatório');
    }

    if (!CONFIG.apiKey) {
      return errorResponse('OBSIDIAN_API_KEY não configurada');
    }

    const normalizedPath = normalizePath(path);
    const originalFolder = normalizedPath.split('/').slice(0, -1).join('/');
    const originalName = normalizedPath.split('/').pop().replace('.md', '');

    // Define novo nome
    let copyName = newName || `${originalName} (Cópia)`;
    if (includeTimestamp) {
      const timestamp = formatDailyDate(new Date());
      copyName = `${copyName} ${timestamp}`;
    }

    const targetFolder = folder || originalFolder;
    const newPath = targetFolder
      ? `${targetFolder}/${copyName}.md`
      : `${copyName}.md`;

    // Lê original
    const readResponse = await fetch(buildUrl(`/vault/${normalizedPath}`), {
      method: 'GET',
      headers: getDefaultHeaders(),
    });

    if (!readResponse.ok) {
      return errorResponse(`Nota não encontrada: ${normalizedPath}`);
    }

    let content = await readResponse.text();

    // Adiciona nota de cópia no frontmatter
    const today = formatDailyDate(new Date());
    content = content.replace(
      /^---/m,
      `---\nduplicated_from: ${originalName}\nduplicated_at: ${today}`
    );

    // Cria cópia
    const writeResponse = await fetch(buildUrl(`/vault/${newPath}`), {
      method: 'PUT',
      headers: getDefaultHeaders(),
      body: content,
    });

    if (!writeResponse.ok) {
      throw new Error('Erro ao criar cópia');
    }

    return successResponse(
      `📄 Nota duplicada: '${copyName}'`,
      {
        original: normalizedPath,
        copy: newPath,
        originalName,
        copyName,
      },
      '✅'
    );

  } catch (error) {
    return errorResponse(`Falha ao duplicar nota: ${error.message}`, error);
  }
}

// Exporta também como default
export default noteDuplicate;
