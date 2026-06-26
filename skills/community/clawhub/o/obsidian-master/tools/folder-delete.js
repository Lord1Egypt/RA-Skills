/**
 * @module tools/folder-delete
 * @description Deleta pastas com confirmação obrigatória
 */

import { CONFIG, getDefaultHeaders, buildUrl, successResponse, errorResponse, warningResponse } from '../config/defaults.js';
import { folderList } from './folder-list.js';

/**
 * Deleta uma pasta e todo seu conteúdo
 * @param {Object} options - Opções de deleção
 * @param {string} options.path - Caminho da pasta
 * @param {boolean} [options.confirm=true] - Exige confirmação
 * @param {boolean} [options.backup=true] - Mover para Arquivo ao invés de deletar
 * @param {boolean} [options.keepStructure=true] - Manter estrutura vazia
 * @returns {Promise<Object>} Resultado da operação
 */
export async function folderDelete(options) {
  try {
    const {
      path,
      confirm = true,
      backup = true,
      keepStructure = false,
    } = options;

    // Validações
    if (!path) {
      return errorResponse('Caminho da pasta é obrigatório');
    }

    if (!CONFIG.apiKey) {
      return errorResponse('OBSIDIAN_API_KEY não configurada');
    }

    const normalizedPath = path.replace(/^\//, '').replace(/\/$/, '');

    // Lista conteúdo
    const listResult = await folderList({ path: normalizedPath, recursive: true });

    const totalFiles = listResult.success ? listResult.data.files.length : 0;
    const totalFolders = listResult.success ? listResult.data.folders.length + 1 : 0;

    // Confirmação obrigatória
    if (confirm && !options.force) {
      const action = backup ? 'arquivar' : 'deletar permanentemente';
      return warningResponse(
        'Confirmação necessária',
        `A pasta '${normalizedPath}' contém ${totalFiles} arquivo(s) e ${totalFolders} subpasta(s). Ela será ${action}. Use confirm=false e force=true para prosseguir.`,
        { path: normalizedPath, files: totalFiles, folders: totalFolders, backup }
      );
    }

    // Se backup, move para pasta Arquivo
    if (backup) {
      return await archiveFolder(normalizedPath, listResult.data?.files || []);
    }

    // Deleta cada arquivo
    const deletedFiles = [];
    const failedFiles = [];

    if (listResult.success) {
      for (const file of listResult.data.files) {
        try {
          const response = await fetch(buildUrl(`/vault/${file.path}`), {
            method: 'DELETE',
            headers: getDefaultHeaders(),
          });

          if (response.ok) {
            deletedFiles.push(file.path);
          } else {
            failedFiles.push({ file: file.path, error: 'Erro ao deletar' });
          }
        } catch (error) {
          failedFiles.push({ file: file.path, error: error.message });
        }
      }
    }

    // Deleta pasta placeholder
    try {
      await fetch(buildUrl(`/vault/${normalizedPath}/.folder`), {
        method: 'DELETE',
        headers: getDefaultHeaders(),
      });
    } catch {
      // Ignora erro ao deletar placeholder
    }

    return successResponse(
      `🗑️ Pasta '${normalizedPath}' deletada`,
      {
        path: normalizedPath,
        deletedFiles: deletedFiles.length,
        failedFiles: failedFiles.length,
        deletedFiles,
        failedFiles,
      },
      '✅'
    );

  } catch (error) {
    return errorResponse(`Falha ao deletar pasta: ${error.message}`, error);
  }
}

/**
 * Arquiva uma pasta movendo para a pasta Arquivo
 * @param {string} path - Caminho da pasta
 * @param {Array} files - Lista de arquivos
 * @returns {Promise<Object>} Resultado
 */
async function archiveFolder(path, files) {
  try {
    const archiveFolder = CONFIG.folders.archive;
    const folderName = path.split('/').pop();
    const archivePath = `${archiveFolder}/${folderName}_arquivado_${formatDate()}`;

    // Cria pasta de arquivo
    await fetch(buildUrl(`/vault/${archivePath}/.folder`), {
      method: 'PUT',
      headers: getDefaultHeaders(),
      body: '# Arquivado\n',
    });

    // Move cada arquivo
    const archivedFiles = [];
    for (const file of files) {
      try {
        const readResponse = await fetch(buildUrl(`/vault/${file.path}`), {
          method: 'GET',
          headers: getDefaultHeaders(),
        });

        if (readResponse.ok) {
          const content = await readResponse.text();
          const fileName = file.path.split('/').pop();

          await fetch(buildUrl(`/vault/${archivePath}/${fileName}`), {
            method: 'PUT',
            headers: getDefaultHeaders(),
            body: content,
          });

          // Deleta original
          await fetch(buildUrl(`/vault/${file.path}`), {
            method: 'DELETE',
            headers: getDefaultHeaders(),
          });

          archivedFiles.push(fileName);
        }
      } catch (error) {
        console.warn(`Erro ao arquivar ${file.path}:`, error.message);
      }
    }

    return successResponse(
      `📦 Pasta '${path}' arquivada em ${archivePath}`,
      {
        originalPath: path,
        archivePath,
        archivedFiles: archivedFiles.length,
        archivedFiles,
      },
      '✅'
    );

  } catch (error) {
    return errorResponse(`Falha ao arquivar pasta: ${error.message}`, error);
  }
}

/**
 * Formata data para sufixo
 * @returns {string} Data formatada
 */
function formatDate() {
  const now = new Date();
  return `${now.getFullYear()}${String(now.getMonth() + 1).padStart(2, '0')}${String(now.getDate()).padStart(2, '0')}`;
}

// Exporta também como default
export default folderDelete;
