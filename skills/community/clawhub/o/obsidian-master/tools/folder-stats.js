/**
 * @module tools/folder-stats
 * @description Gera estatísticas de uma pasta específica
 */

import { CONFIG, getDefaultHeaders, buildUrl, successResponse, errorResponse } from '../config/defaults.js';
import { folderList } from './folder-list.js';

/**
 * Gera estatísticas detalhadas de uma pasta
 * @param {Object} options - Opções de análise
 * @param {string} [options.path=''] - Caminho da pasta (vazio = raiz)
 * @param {boolean} [options.recursive=true] - Incluir subpastas
 * @param {boolean} [options.includeContent=true] - Analisar conteúdo das notas
 * @returns {Promise<Object>} Estatísticas da pasta
 */
export async function folderStats(options = {}) {
  try {
    const {
      path = '',
      recursive = true,
      includeContent = true,
    } = options;

    if (!CONFIG.apiKey) {
      return errorResponse('OBSIDIAN_API_KEY não configurada');
    }

    const normalizedPath = path.replace(/^\//, '').replace(/\/$/, '');

    // Lista conteúdo
    const listResult = await folderList({ path: normalizedPath, recursive });
    if (!listResult.success) {
      return errorResponse(`Pasta não encontrada: ${path || 'raiz'}`);
    }

    const { files, folders } = listResult.data;

    // Estatísticas básicas
    const stats = {
      folder: normalizedPath || 'raiz',
      totalFiles: files.length,
      totalFolders: folders.length,
      totalSize: 0,
      byExtension: {},
      byMonth: {},
    };

    // Análise de conteúdo (apenas para .md)
    const contentStats = {
      totalWords: 0,
      totalLines: 0,
      totalLinks: 0,
      totalTags: 0,
      totalTasks: { open: 0, completed: 0 },
      mostUsedTags: {},
      largestFile: null,
      mostRecentFile: null,
      oldestFile: null,
    };

    let largestSize = 0;
    let mostRecent = null;
    let oldest = null;

    for (const file of files) {
      // Tamanho
      if (file.size) {
        const size = parseInt(file.size, 10);
        stats.totalSize += size;

        if (size > largestSize) {
          largestSize = size;
          contentStats.largestFile = {
            name: file.name,
            path: file.path,
            size: size,
          };
        }
      }

      // Extensão
      const ext = file.extension || 'sem-extensao';
      stats.byExtension[ext] = (stats.byExtension[ext] || 0) + 1;

      // Data de modificação
      if (file.lastModified) {
        const date = new Date(file.lastModified);
        const monthKey = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`;
        stats.byMonth[monthKey] = (stats.byMonth[monthKey] || 0) + 1;

        if (!mostRecent || date > mostRecent) {
          mostRecent = date;
          contentStats.mostRecentFile = {
            name: file.name,
            path: file.path,
            date: file.lastModified,
          };
        }

        if (!oldest || date < oldest) {
          oldest = date;
          contentStats.oldestFile = {
            name: file.name,
            path: file.path,
            date: file.lastModified,
          };
        }
      }

      // Analisa conteúdo se for markdown
      if (includeContent && file.extension === 'md') {
        try {
          const contentStats = await analyzeFileContent(file.path);
          if (contentStats) {
            Object.assign(contentStats, {
              totalWords: (contentStats.totalWords || 0) + (contentStats.wordCount || 0),
              totalLines: (contentStats.totalLines || 0) + (contentStats.lineCount || 0),
              totalLinks: (contentStats.totalLinks || 0) + (contentStats.linkCount || 0),
              totalTags: (contentStats.totalTags || 0) + (contentStats.tagCount || 0),
              totalTasks: {
                open: (contentStats.totalTasks?.open || 0) + (contentStats.tasks?.open || 0),
                completed: (contentStats.totalTasks?.completed || 0) + (contentStats.tasks?.completed || 0),
              },
            });
          }
        } catch (error) {
          // Ignora erro de análise individual
        }
      }
    }

    // Calcula médias
    const markdownFiles = files.filter(f => f.extension === 'md').length;
    if (markdownFiles > 0) {
      contentStats.avgWordsPerFile = Math.round(contentStats.totalWords / markdownFiles);
    }

    return successResponse(
      `📊 Estatísticas de ${normalizedPath || 'raiz'}`,
      {
        ...stats,
        contentStats: includeContent ? contentStats : null,
        humanReadable: {
          totalSize: formatBytes(stats.totalSize),
        },
      },
      '📈'
    );

  } catch (error) {
    return errorResponse(`Falha ao gerar estatísticas: ${error.message}`, error);
  }
}

/**
 * Analisa o conteúdo de um arquivo
 * @param {string} path - Caminho do arquivo
 * @returns {Promise<Object|null>} Estatísticas do arquivo
 */
async function analyzeFileContent(path) {
  try {
    const response = await fetch(buildUrl(`/vault/${path}`), {
      method: 'GET',
      headers: getDefaultHeaders(),
    });

    if (!response.ok) return null;

    const content = await response.text();
    const lines = content.split('\n');

    // Contagem básica
    const wordCount = content.split(/\s+/).filter(w => w.length > 0).length;
    const lineCount = lines.length;

    // Links
    const linkMatches = content.match(/\[\[([^\]]+)\]\]/g);
    const linkCount = linkMatches ? linkMatches.length : 0;

    // Tags
    const tagMatches = content.match(/#[a-zA-Z0-9_\-\/]+/g);
    const tagCount = tagMatches ? tagMatches.length : 0;

    // Tasks
    const openTasks = (content.match(/- \[ \]/g) || []).length;
    const completedTasks = (content.match(/- \[x\]/gi) || []).length;

    return {
      wordCount,
      lineCount,
      linkCount,
      tagCount,
      tasks: {
        open: openTasks,
        completed: completedTasks,
      },
    };

  } catch {
    return null;
  }
}

/**
 * Formata bytes para human readable
 * @param {number} bytes - Tamanho em bytes
 * @returns {string} Formato legível
 */
function formatBytes(bytes) {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// Exporta também como default
export default folderStats;
