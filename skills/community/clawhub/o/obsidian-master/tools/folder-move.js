/"
 * @module tools/folder-move
 * @description Move pastas inteiras mantendo estrutura
 */

import { CONFIG, getDefaultHeaders, buildUrl, successResponse, errorResponse } from '../config/defaults.js';
import { folderList } from './folder-list.js';

/**
 * Move uma pasta para outra localização
 * @param {Object} options - Opções de movimentação
 * @param {string} options.from - Caminho de origem
 * @param {string} options.to - Caminho de destino
 * @param {boolean} [options.merge=false] - Mesclar se pasta destino existir
 * @param {boolean} [options.updateLinks=true] - Atualizar wikilinks internos
 * @returns {Promise<Object>} Resultado da operação
 */
export async function folderMove(options) {
  try {
    const {
      from,
      to,
      merge = false,
      updateLinks = true,
    } = options;

    // Validações
    if (!from || !to) {
      return errorResponse('Caminhos de origem e destino são obrigatórios');
    }

    if (!CONFIG.apiKey) {
      return errorResponse('OBSIDIAN_API_KEY não configurada');
    }

    const fromPath = from.replace(/^\//, '').replace(/\/$/, '');
    const toPath = to.replace(/^\//, '').replace(/\/$/, '');

    if (fromPath === toPath) {
      return errorResponse('Origem e destino são iguais');
    }

    // Lista conteúdo da pasta origem
    const listResult = await folderList({ path: fromPath, recursive: true });
    if (!listResult.success) {
      return errorResponse(`Pasta de origem não encontrada: ${fromPath}`);
    }

    const { files, folders } = listResult.data;

    // Verifica se destino existe
    const destExists = await checkFolderExists(toPath);
    if (destExists && !merge) {
      return errorResponse(`Pasta de destino já existe: ${toPath}. Use merge=true para mesclar.`);
    }

    // Move cada arquivo
    const movedFiles = [];
    const failedFiles = [];

    for (const file of files) {
      try {
        // Lê conteúdo
        const readResponse = await fetch(buildUrl(`/vault/${file.path}`), {
          method: 'GET',
          headers: getDefaultHeaders(),
        });

        if (!readResponse.ok) {
          failedFiles.push({ file: file.name, error: 'Erro ao ler' });
          continue;
        }

        let content = await readResponse.text();

        // Atualiza links se necessário
        if (updateLinks) {
          content = updateInternalLinks(content, fromPath, toPath);
        }

        // Calcula novo caminho
        const relativePath = file.path.replace(fromPath, '').replace(/^\//, '');
        const newPath = `${toPath}/${relativePath}`;

        // Cria no destino
        const writeResponse = await fetch(buildUrl(`/vault/${newPath}`), {
          method: 'PUT',
          headers: getDefaultHeaders(),
          body: content,
        });

        if (!writeResponse.ok) {
          failedFiles.push({ file: file.name, error: 'Erro ao escrever' });
          continue;
        }

        // Deleta original
        const deleteResponse = await fetch(buildUrl(`/vault/${file.path}`), {
          method: 'DELETE',
          headers: getDefaultHeaders(),
        });

        if (!deleteResponse.ok) {
          // Se falhou deletar, tenta deletar o novo
          await fetch(buildUrl(`/vault/${newPath}`), {
            method: 'DELETE',
            headers: getDefaultHeaders(),
          });
          failedFiles.push({ file: file.name, error: 'Erro ao deletar original' });
          continue;
        }

        movedFiles.push({
          original: file.path,
          new: newPath,
        });

      } catch (error) {
        failedFiles.push({ file: file.name, error: error.message });
      }
    }

    return successResponse(
      `📁 Pasta '${fromPath}' movida para '${toPath}'`,
      {
        from: fromPath,
        to: toPath,
        filesMoved: movedFiles.length,
        filesFailed: failedFiles.length,
        movedFiles,
        failedFiles,
        updateLinks,
      },
      '✅'
    );

  } catch (error) {
    return errorResponse(`Falha ao mover pasta: ${error.message}`, error);
  }
}

/**
 * Atualiza links internos no conteúdo
 * @param {string} content - Conteúdo original
 * @param {string} oldPath - Caminho antigo
 * @param {string} newPath - Caminho novo
 * @returns {string} Conteúdo atualizado
 */
function updateInternalLinks(content, oldPath, newPath) {
  // Atualiza wikilinks que referenciam a pasta antiga
  const oldFolderName = oldPath.split('/').pop();
  const newFolderName = newPath.split('/').pop();

  // Regex simples para links diretos à pasta
  const linkPattern = new RegExp(`\\[\\[${oldFolderName}/([^\\]]+)\\]\\]`, 'g');
  return content.replace(linkPattern, `[[${newFolderName}/$1]]`);
}

/**
 * Verifica se uma pasta existe
 * @param {string} path - Caminho da pasta
 * @returns {Promise<boolean>}
 */
async function checkFolderExists(path) {
  try {
    const response = await fetch(buildUrl(`/vault/${path}/`), {
      method: 'HEAD',
      headers: getDefaultHeaders(),
    });
    return response.ok;
  } catch {
    return false;
  }
}

// Exporta também como default
export default folderMove;
