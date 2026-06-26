/**
 * @module tools/vault-stats
 * @description Gera estatísticas completas do vault inteiro
 */

import { CONFIG, getDefaultHeaders, buildUrl, successResponse, errorResponse } from '../config/defaults.js';
import { folderList } from './folder-list.js';

/**
 * Gera estatísticas completas do vault
 * @param {Object} options - Opções de análise
 * @param {boolean} [options.includeContent=true] - Analisar conteúdo das notas
 * @param {boolean} [options.includeStructure=true] - Analisar estrutura de pastas
 * @returns {Promise<Object>} Estatísticas completas do vault
 */
export async function vaultStats(options = {}) {
  try {
    const {
      includeContent = true,
      includeStructure = true,
    } = options;

    if (!CONFIG.apiKey) {
      return errorResponse('OBSIDIAN_API_KEY não configurada');
    }

    // Lista todo o vault
    const listResult = await folderList({ path: '', recursive: true });
    if (!listResult.success) {
      return errorResponse('Não foi possível listar o vault');
    }

    const { files, folders } = listResult.data;

    // Filtra apenas arquivos markdown
    const mdFiles = files.filter(f => f.extension === 'md');

    // Estatísticas gerais
    const stats = {
      overview: {
        totalFiles: files.length,
        totalFolders: folders.length,
        totalNotes: mdFiles.length,
        otherFiles: files.length - mdFiles.length,
      },
      size: {
        total: 0,
        markdown: 0,
        other: 0,
        averageNoteSize: 0,
      },
      activity: {
        byMonth: {},
        lastModified: null,
        firstCreated: null,
      },
    };

    // Análise de conteúdo
    const contentStats = {
      totalWords: 0,
      totalCharacters: 0,
      averageWordsPerNote: 0,
      totalLinks: 0,
      totalUniqueLinks: new Set(),
      totalTags: 0,
      uniqueTags: new Set(),
      tasks: {
        open: 0,
        completed: 0,
      },
      largestNote: null,
      smallestNote: null,
      mostRecent: null,
      oldest: null,
    };

    let largestSize = 0;
    let smallestSize = Infinity;
    let mostRecent = null;
    let oldest = null;

    for (const file of files) {
      // Tamanho
      if (file.size) {
        const size = parseInt(file.size, 10);
        stats.size.total += size;

        if (file.extension === 'md') {
          stats.size.markdown += size;

          if (size > largestSize) {
            largestSize = size;
            contentStats.largestNote = {
              name: file.name,
              path: file.path,
              size: formatBytes(size),
              sizeBytes: size,
            };
          }

          if (size < smallestSize) {
            smallestSize = size;
            contentStats.smallestNote = {
              name: file.name,
              path: file.path,
              size: formatBytes(size),
              sizeBytes: size,
            };
          }
        } else {
          stats.size.other += size;
        }
      }

      // Data
      if (file.lastModified) {
        const date = new Date(file.lastModified);
        const monthKey = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`;
        stats.activity.byMonth[monthKey] = (stats.activity.byMonth[monthKey] || 0) + 1;

        if (!mostRecent || date > mostRecent) {
          mostRecent = date;
          contentStats.mostRecent = {
            name: file.name,
            path: file.path,
            date: file.lastModified,
          };
          stats.activity.lastModified = file.lastModified;
        }

        if (!oldest || date < oldest) {
          oldest = date;
          contentStats.oldest = {
            name: file.name,
            path: file.path,
            date: file.lastModified,
          };
          stats.activity.firstCreated = file.lastModified;
        }
      }

      // Análise de conteúdo
      if (includeContent && file.extension === 'md') {
        try {
          const fileStats = await analyzeNoteContent(file.path);
          if (fileStats) {
            contentStats.totalWords += fileStats.wordCount || 0;
            contentStats.totalCharacters += fileStats.charCount || 0;
            contentStats.totalLinks += fileStats.linkCount || 0;
            contentStats.totalTags += fileStats.tagCount || 0;
            contentStats.tasks.open += fileStats.tasks?.open || 0;
            contentStats.tasks.completed += fileStats.tasks?.completed || 0;

            fileStats.links?.forEach(link => contentStats.totalUniqueLinks.add(link));
            fileStats.tags?.forEach(tag => contentStats.uniqueTags.add(tag));
          }
        } catch {
          // Ignora erros individuais
        }
      }
    }

    // Calcula médias
    if (mdFiles.length > 0) {
      stats.size.averageNoteSize = Math.round(stats.size.markdown / mdFiles.length);
      contentStats.averageWordsPerNote = Math.round(contentStats.totalWords / mdFiles.length);
    }

    // Estrutura de pastas
    let structure = null;
    if (includeStructure) {
      structure = analyzeFolderStructure(folders, mdFiles);
    }

    // Converte Sets para Arrays
    const result = {
      ...stats,
      content: {
        ...contentStats,
        uniqueLinks: Array.from(contentStats.totalUniqueLinks),
        uniqueTags: Array.from(contentStats.uniqueTags),
        totalUniqueLinks: contentStats.totalUniqueLinks.size,
        totalUniqueTags: contentStats.uniqueTags.size,
      },
      structure,
      humanReadable: {
        totalSize: formatBytes(stats.size.total),
        markdownSize: formatBytes(stats.size.markdown),
        averageNoteSize: formatBytes(stats.size.averageNoteSize),
      },
    };

    return successResponse(
      `📊 Estatísticas do Vault`,
      result,
      '📈'
    );

  } catch (error) {
    return errorResponse(`Falha ao gerar estatísticas: ${error.message}`, error);
  }
}

/**
 * Analisa conteúdo de uma nota
 * @param {string} path - Caminho da nota
 * @returns {Promise<Object>} Estatísticas da nota
 */
async function analyzeNoteContent(path) {
  try {
    const response = await fetch(buildUrl(`/vault/${path}`), {
      method: 'GET',
      headers: getDefaultHeaders(),
    });

    if (!response.ok) return null;

    const content = await response.text();

    // Estatísticas básicas
    const wordCount = content.split(/\s+/).filter(w => w.length > 0).length;
    const charCount = content.length;

    // Links
    const linkMatches = content.match(/\[\[([^\]|]+)(?:\|[^\]]+)?\]\]/g);
    const links = linkMatches ? linkMatches.map(m => m.match(/\[\[([^\]|]+)/)[1]) : [];

    // Tags
    const tagMatches = content.match(/#[a-zA-Z0-9_\-\/]+/g);
    const tags = tagMatches ? tagMatches.map(t => t.slice(1)) : [];

    // Tasks
    const openTasks = (content.match(/- \[ \]/g) || []).length;
    const completedTasks = (content.match(/- \[x\]/gi) || []).length;

    return {
      wordCount,
      charCount,
      linkCount: links.length,
      links,
      tagCount: tags.length,
      tags,
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
 * Analisa estrutura de pastas
 * @param {Array} folders - Lista de pastas
 * @param {Array} files - Lista de arquivos
 * @returns {Object} Estrutura analisada
 */
function analyzeFolderStructure(folders, files) {
  const folderStats = {};

  // Conta arquivos por pasta
  for (const file of files) {
    const folderPath = file.path.split('/').slice(0, -1).join('/') || 'raiz';
    if (!folderStats[folderPath]) {
      folderStats[folderPath] = { count: 0, files: [] };
    }
    folderStats[folderPath].count++;
    folderStats[folderPath].files.push(file.name);
  }

  // Identifica pastas mais populares
  const sortedFolders = Object.entries(folderStats)
    .sort((a, b) => b[1].count - a[1].count)
    .slice(0, 10);

  return {
    totalFolders: folders.length,
    distribution: folderStats,
    mostPopulated: sortedFolders.map(([name, stats]) => ({
      folder: name,
      fileCount: stats.count,
    })),
  };
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
export default vaultStats;
