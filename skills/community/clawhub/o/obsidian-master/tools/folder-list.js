/**
 * @module tools/folder-list
 * @description Lista o conteúdo de uma pasta (notas e subpastas)
 */

import { CONFIG, getDefaultHeaders, buildUrl, successResponse, errorResponse } from '../config/defaults.js';

/**
 * Lista o conteúdo de uma pasta
 * @param {Object} options - Opções de listagem
 * @param {string} [options.path=''] - Caminho da pasta (vazio = raiz do vault)
 * @param {boolean} [options.recursive=false] - Listar recursivamente
 * @param {string} [options.filter] - Filtrar por extensão (ex: '.md')
 * @param {boolean} [options.includeMetadata=true] - Incluir metadados dos arquivos
 * @returns {Promise<Object>} Lista de arquivos e pastas
 */
export async function folderList(options = {}) {
  try {
    const {
      path = '',
      recursive = false,
      filter,
      includeMetadata = true,
    } = options;

    if (!CONFIG.apiKey) {
      return errorResponse('OBSIDIAN_API_KEY não configurada');
    }

    // Normaliza o caminho
    const normalizedPath = path.replace(/^\//, '').replace(/\/$/, '');
    const apiPath = normalizedPath ? `/vault/${normalizedPath}/` : '/vault/';

    const response = await fetch(buildUrl(apiPath), {
      method: 'GET',
      headers: getDefaultHeaders(),
    });

    if (!response.ok) {
      if (response.status === 404) {
        return errorResponse(`Pasta não encontrada: ${path || 'raiz'}`);
      }
      const errorText = await response.text();
      throw new Error(`Erro ${response.status}: ${errorText}`);
    }

    const items = await response.json();

    // Processa os itens
    const files = [];
    const folders = [];

    for (const item of items) {
      if (item.endsWith('/')) {
        // É uma pasta
        const folderName = item.slice(0, -1);
        folders.push({
          name: folderName,
          path: normalizedPath ? `${normalizedPath}/${folderName}` : folderName,
          type: 'folder',
        });
      } else {
        // É um arquivo
        if (!filter || item.endsWith(filter)) {
          const fileInfo = {
            name: item,
            path: normalizedPath ? `${normalizedPath}/${item}` : item,
            type: 'file',
            extension: item.split('.').pop() || '',
          };

          if (includeMetadata) {
            // Busca metadados se possível
            try {
              const metaResponse = await fetch(
                buildUrl(`/vault/${normalizedPath ? normalizedPath + '/' : ''}${item}`),
                { method: 'HEAD', headers: getDefaultHeaders() }
              );
              if (metaResponse.ok) {
                fileInfo.size = metaResponse.headers.get('content-length');
                fileInfo.lastModified = metaResponse.headers.get('last-modified');
              }
            } catch {
              // Ignora erro de metadados
            }
          }

          files.push(fileInfo);
        }
      }
    }

    // Se recursivo, processa subpastas
    if (recursive) {
      for (const folder of folders) {
        const subResult = await folderList({
          path: folder.path,
          recursive: true,
          filter,
          includeMetadata,
        });
        if (subResult.success) {
          files.push(...subResult.data.files);
          folders.push(...subResult.data.folders.filter(f => f.path !== folder.path));
        }
      }
    }

    return successResponse(
      `📂 ${files.length} arquivo(s) e ${folders.length} pasta(s) em ${path || 'raiz'}`,
      {
        path: normalizedPath || 'raiz',
        files,
        folders: folders.filter((f, i, arr) => arr.findIndex(t => t.path === f.path) === i), // Remove duplicados
        totalFiles: files.length,
        totalFolders: folders.length,
      },
      '📁'
    );

  } catch (error) {
    return errorResponse(`Falha ao listar pasta: ${error.message}`, error);
  }
}

// Exporta também como default
export default folderList;
