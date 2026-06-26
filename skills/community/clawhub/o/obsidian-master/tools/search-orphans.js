/**
 * @module tools/search-orphans
 * @description Encontra notas sem nenhum link para elas (órfãs)
 */

import { CONFIG, getDefaultHeaders, buildUrl, successResponse, errorResponse } from '../config/defaults.js';

/**
 * Busca notas órfãs (sem backlinks)
 * @param {Object} options - Opções de busca
 * @param {string} [options.excludeFolders] - Pastas a excluir (ex: "99 - Templates,00 - Inbox")
 * @param {number} [options.minWords=10] - Mínimo de palavras para considerar
 * @param {boolean} [options.includeSuggestions=true] - Sugerir links para cada órfã
 * @returns {Promise<Object>} Notas órfãs encontradas
 */
export async function searchOrphans(options = {}) {
  try {
    const {
      excludeFolders = [CONFIG.folders.archive, CONFIG.folders.templates],
      minWords = 10,
      includeSuggestions = true,
    } = options;

    if (!CONFIG.apiKey) {
      return errorResponse('OBSIDIAN_API_KEY não configurada');
    }

    // Lista todos os arquivos
    const response = await fetch(buildUrl('/vault/'), {
      method: 'GET',
      headers: getDefaultHeaders(),
    });

    if (!response.ok) {
      throw new Error('Não foi possível listar o vault');
    }

    const items = await response.json();
    const mdFiles = items.filter(i => i.endsWith('.md'));

    const excludeList = Array.isArray(excludeFolders) ? excludeFolders : excludeFolders.split(',');

    const orphans = [];
    const allNotes = [];
    const allLinks = new Set();

    // Primeira passada: coleta todas as notas e links
    for (const file of mdFiles) {
      // Pula pastas excluídas
      if (excludeList.some(ex => file.startsWith(ex))) continue;

      const noteName = file.replace(/\.md$/, '');
      allNotes.push({
        name: noteName,
        path: file,
      });

      try {
        const fileResponse = await fetch(buildUrl(`/vault/${file}`), {
          method: 'GET',
          headers: getDefaultHeaders(),
        });

        if (!fileResponse.ok) continue;

        const content = await fileResponse.text();

        // Extrai links
        const linkMatches = content.match(/\[\[([^\]|]+)/g);
        if (linkMatches) {
          linkMatches.forEach(match => {
            const target = match.replace('[[', '').trim();
            allLinks.add(target);
          });
        }

      } catch {
        // Ignora erro
      }
    }

    // Segunda passada: identifica órfãs
    for (const note of allNotes) {
      // Verifica se alguém linka para esta nota
      const hasBacklinks = allLinks.has(note.name);

      if (!hasBacklinks) {
        // Verifica tamanho mínimo
        try {
          const contentResponse = await fetch(buildUrl(`/vault/${note.path}`), {
            method: 'GET',
            headers: getDefaultHeaders(),
          });

          if (contentResponse.ok) {
            const content = await contentResponse.text();
            const wordCount = content.split(/\s+/).filter(w => w.length > 0).length;

            if (wordCount >= minWords) {
              const orphanInfo = {
                name: note.name,
                path: note.path,
                wordCount,
              };

              if (includeSuggestions) {
                orphanInfo.suggestions = generateLinkSuggestions(note, allNotes, allLinks);
              }

              orphans.push(orphanInfo);
            }
          }
        } catch {
          // Ignora erro
        }
      }
    }

    return successResponse(
      `🐣 ${orphans.length} nota(s) órfã(s) encontrada(s)`,
      {
        totalNotes: allNotes.length,
        orphanCount: orphans.length,
        orphanRate: `${((orphans.length / allNotes.length) * 100).toFixed(1)}%`,
        orphans,
        recommendations: [
          'Considere criar um MOC para agrupar notas órfãs relacionadas',
          'Verifique se há sinônimos que poderiam ser usados como aliases',
          'Notas de template ou daily podem ser excluídas desta análise',
        ],
      },
      '🐣'
    );

  } catch (error) {
    return errorResponse(`Falha ao buscar órfãs: ${error.message}`, error);
  }
}

/**
 * Gera sugestões de links para uma nota órfã
 * @param {Object} orphan - Nota órfã
 * @param {Array} allNotes - Todas as notas
 * @param {Set} allLinks - Todos os links existentes
 * @returns {Array} Sugestões
 */
function generateLinkSuggestions(orphan, allNotes, allLinks) {
  const suggestions = [];

  // Notas com nomes similares
  for (const note of allNotes) {
    if (note.name === orphan.name) continue;

    // Calcula similaridade simples (palavras em comum)
    const orphanWords = orphan.name.toLowerCase().split(/\s+/);
    const noteWords = note.name.toLowerCase().split(/\s+/);
    const commonWords = orphanWords.filter(w => noteWords.includes(w));

    if (commonWords.length > 0) {
      suggestions.push({
        type: 'similar_name',
        note: note.name,
        reason: `Palavras em comum: ${commonWords.join(', ')}`,
      });
    }
  }

  return suggestions.slice(0, 5);
}

// Exporta também como default
export default searchOrphans;
