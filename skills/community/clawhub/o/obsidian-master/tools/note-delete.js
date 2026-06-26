/**
 * @module tools/note-delete
 * @description Deleta notas com confirmação obrigatória e opção de backup
 */

import { CONFIG, getDefaultHeaders, buildUrl, normalizePath, successResponse, errorResponse, warningResponse } from '../config/defaults.js';

/**
 * Deleta uma nota do vault
 * @param {Object} options - Opções de deleção
 * @param {string} options.path - Caminho da nota
 * @param {boolean} [options.confirm=true] - Exige confirmação
 * @param {boolean} [options.backup=true] - Mover para Arquivo ao invés de deletar
 * @param {string} [options.reason=''] - Motivo da deleção (para log)
 * @returns {Promise<Object>} Resultado da operação
 */
export async function noteDelete(options) {
  try {
    const {
      path,
      confirm = true,
      backup = true,
      reason = '',
    } = options;

    // Validações
    if (!path) {
      return errorResponse('Caminho da nota é obrigatório');
    }

    if (!CONFIG.apiKey) {
      return errorResponse('OBSIDIAN_API_KEY não configurada');
    }

    // Confirmação é obrigatória para deleção
    if (confirm && !options.force) {
      const title = path.split('/').pop().replace('.md', '');
      return warningResponse(
        'Confirmação necessária',
        `A nota '${title}' será ${backup ? 'movida para Arquivo' : 'permanentemente deletada'}. Use confirm=false e force=true para prosseguir.`,
        { path, backup }
      );
    }

    const normalizedPath = normalizePath(path);

    // Verifica se nota existe
    const existsCheck = await checkNoteExists(normalizedPath);
    if (!existsCheck.exists) {
      return errorResponse(`Nota não encontrada: ${normalizedPath}`);
    }

    // Se backup está ativado, move para pasta Arquivo
    if (backup) {
      return await archiveNote(normalizedPath, reason);
    }

    // Deleta permanentemente
    const response = await fetch(buildUrl(`/vault/${normalizedPath}`), {
      method: 'DELETE',
      headers: getDefaultHeaders(),
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Erro ${response.status}: ${errorText}`);
    }

    const title = normalizedPath.split('/').pop().replace('.md', '');

    return successResponse(
      `🗑️ Nota '${title}' deletada permanentemente`,
      {
        path: normalizedPath,
        deleted: true,
        backedUp: false,
        reason,
      },
      '✅'
    );

  } catch (error) {
    return errorResponse(`Falha ao deletar nota: ${error.message}`, error);
  }
}

/**
 * Move nota para pasta de arquivo ao invés de deletar
 * @param {string} path - Caminho atual da nota
 * @param {string} reason - Motivo
 * @returns {Promise<Object>} Resultado
 */
async function archiveNote(path, reason) {
  try {
    const archiveFolder = CONFIG.folders.archive;
    const fileName = path.split('/').pop();
    const archivePath = `${archiveFolder}/${fileName}`;

    // Lê o conteúdo atual
    const readResponse = await fetch(buildUrl(`/vault/${path}`), {
      method: 'GET',
      headers: getDefaultHeaders(),
    });

    if (!readResponse.ok) {
      throw new Error('Não foi possível ler a nota para arquivar');
    }

    let content = await readResponse.text();

    // Adiciona metadata de arquivo
    const today = new Date().toISOString().split('T')[0];
    const archiveInfo = `\n\n---\n\n**🗃️ Arquivado em:** ${today}`;
    if (reason) {
      content += `\n**Motivo:** ${reason}`;
    }
    content += archiveInfo;

    // Atualiza frontmatter
    content = content.replace(
      /type:\s*(\w+)/,
      'type: archive'
    );
    content = content.replace(
      /status:\s*(\w+)/,
      'status: archived'
    );

    // Cria na pasta Arquivo
    const createResponse = await fetch(buildUrl(`/vault/${archivePath}`), {
      method: 'PUT',
      headers: getDefaultHeaders(),
      body: content,
    });

    if (!createResponse.ok) {
      throw new Error('Não foi possível criar nota arquivada');
    }

    // Deleta original
    const deleteResponse = await fetch(buildUrl(`/vault/${path}`), {
      method: 'DELETE',
      headers: getDefaultHeaders(),
    });

    if (!deleteResponse.ok) {
      // Se falhou deletar, tenta deletar o arquivo do arquivo
      await fetch(buildUrl(`/vault/${archivePath}`), {
        method: 'DELETE',
        headers: getDefaultHeaders(),
      });
      throw new Error('Erro ao mover nota para arquivo');
    }

    const title = fileName.replace('.md', '');

    return successResponse(
      `📦 Nota '${title}' movida para ${archiveFolder}`,
      {
        originalPath: path,
        archivePath,
        archived: true,
        archivedAt: today,
        reason,
      },
      '✅'
    );

  } catch (error) {
    return errorResponse(`Falha ao arquivar nota: ${error.message}`, error);
  }
}

/**
 * Verifica se uma nota existe
 * @param {string} path - Caminho da nota
 * @returns {Promise<Object>} { exists: boolean }
 */
async function checkNoteExists(path) {
  try {
    const response = await fetch(buildUrl(`/vault/${path}`), {
      method: 'HEAD',
      headers: getDefaultHeaders(),
    });
    return { exists: response.ok };
  } catch {
    return { exists: false };
  }
}

// Exporta também como default
export default noteDelete;
