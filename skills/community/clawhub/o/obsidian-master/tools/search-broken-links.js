/**
 * @module tools/search-broken-links
 * @description Encontra links quebrados no vault (apontando para notas inexistentes)
 */

import { CONFIG, getDefaultHeaders, buildUrl, successResponse, errorResponse } from '../config/defaults.js';

/**
 * Busca links quebrados no vault
 * @param {Object} options - Opções de busca
 * @param {string} [options.folder] - Limitar a uma pasta específica
 * @param {boolean} [options.checkEmbedded=true] - Verificar embeds ![[...]]
 * @param {boolean} [options.checkExternal=false] - Verificar links externos [text](url)
 * @returns {Promise<Object>} Links quebrados encontrados
 */
export async function searchBrokenLinks(options = {}) {
  try {
    const {
      folder,
      checkEmbedded = true,
      checkExternal = false,
    } = options;

    if (!CONFIG.apiKey) {
      return errorResponse('OBSIDIAN_API_KEY não configurada');
    }

    // Lista todos os arquivos
    const listPath = folder || '';
    const response = await fetch(buildUrl(`/vault/${listPath}`), {
      method: 'GET',
      headers: getDefaultHeaders(),
    });

    if (!response.ok) {
      throw new Error('Não foi possível listar o vault');
    }

    const items = await response.json();
    const mdFiles = items.filter(i => i.endsWith('.md'));

    // Coleta todas as notas existentes
    const existingNotes = new Set(mdFiles.map(f => f.replace(/\.md$/, '')));

    // Adiciona notas em subpastas
    const allNotes = await collectAllNotes(listPath);
    allNotes.forEach(n => existingNotes.add(n.replace(/\.md$/, '')));

    const brokenLinks = [];

    for (const file of mdFiles) {
      try {
        const fileResponse = await fetch(
          buildUrl(`/vault/${listPath ? listPath + '/' : ''}${file}`),
          { method: 'GET', headers: getDefaultHeaders() }
        );

        if (!fileResponse.ok) continue;

        const content = await fileResponse.text();
        const fileBrokenLinks = [];

        // Links wikilink [[Nota]]
        const wikilinkMatches = content.match(/\[\[([^\]|#]+)(?:#[^\]]*)?(?:\|[^\]]*)?\]\]/g);
        if (wikilinkMatches) {
          for (const match of wikilinkMatches) {
            const target = match.replace(/\[\[|\]\]/g, '').split('#')[0].split('|')[0].trim();

            // Verifica se existe
            if (!noteExists(target, existingNotes, listPath)) {
              fileBrokenLinks.push({
                type: 'wikilink',
                target,
                context: findContext(content, match),
              });
            }
          }
        }

        // Embeds ![[Nota]]
        if (checkEmbedded) {
          const embedMatches = content.match(/!\[\[([^\]]+)\]\]/g);
          if (embedMatches) {
            for (const match of embedMatches) {
              const target = match.replace(/!?\[\[|\]\]/g, '');

              if (!noteExists(target, existingNotes, listPath)) {
                fileBrokenLinks.push({
                  type: 'embed',
                  target,
                  context: findContext(content, match),
                });
              }
            }
          }
        }

        // Links externos [text](url)
        if (checkExternal) {
          const externalMatches = content.match(/\[([^\]]+)\]\((https?:\/\/[^\)]+)\)/g);
          if (externalMatches) {
            for (const match of externalMatches) {
              const url = match.match(/\((https?:\/\/[^\)]+)\)/)?.[1];
              if (url) {
                // Verificação de URL seria async, pulamos por enquanto
                // Poderia fazer HEAD request para verificar
              }
            }
          }
        }

        if (fileBrokenLinks.length > 0) {
          brokenLinks.push({
            file,
            path: `${listPath ? listPath + '/' : ''}${file}`,
            brokenCount: fileBrokenLinks.length,
            links: fileBrokenLinks,
          });
        }

      } catch {
        // Ignora erro individual
      }
    }

    // Calcula estatísticas
    const totalBroken = brokenLinks.reduce((sum, b) => sum + b.brokenCount, 0);

    return successResponse(
      `💔 ${brokenLinks.length} arquivo(s) com ${totalBroken} link(s) quebrado(s)`,
      {
        totalFiles: mdFiles.length,
        filesWithBrokenLinks: brokenLinks.length,
        totalBrokenLinks: totalBroken,
        brokenLinks,
        suggestions: [
          'Crie as notas ausentes ou remova os links',
          'Use aliases se o nome mudou',
          'Verifique se há erros de digitação nos nomes',
        ],
      },
      '💔'
    );

  } catch (error) {
    return errorResponse(`Falha ao buscar links quebrados: ${error.message}`, error);
  }
}

/**
 * Coleta todas as notas recursivamente
 * @param {string} basePath - Caminho base
 * @returns {Promise<Set>} Set de notas
 */
async function collectAllNotes(basePath) {
  const notes = new Set();

  try {
    const response = await fetch(buildUrl(`/vault/${basePath}`), {
      method: 'GET',
      headers: getDefaultHeaders(),
    });

    if (!response.ok) return notes;

    const items = await response.json();

    for (const item of items) {
      if (item.endsWith('.md')) {
        notes.add(item.replace(/\.md$/, ''));
      } else if (item.endsWith('/')) {
        // Pasta - recursivo
        const subNotes = await collectAllNotes(`${basePath}/${item.slice(0, -1)}`);
        subNotes.forEach(n => notes.add(n));
      }
    }
  } catch {
    // Ignora erro
  }

  return notes;
}

/**
 * Verifica se uma nota existe
 * @param {string} target - Nome alvo
 * @param {Set} existingNotes - Notas existentes
 * @param {string} currentFolder - Pasta atual
 * @returns {boolean}
 */
function noteExists(target, existingNotes, currentFolder) {
  // Verifica exato
  if (existingNotes.has(target)) return true;

  // Verifica com caminho relativo
  if (existingNotes.has(`${currentFolder}/${target}`)) return true;

  // Verifica case insensitive
  for (const note of existingNotes) {
    if (note.toLowerCase() === target.toLowerCase()) return true;
    if (note.endsWith(`/${target.toLowerCase()}`)) return true;
  }

  return false;
}

/**
 * Encontra contexto ao redor de um link
 * @param {string} content - Conteúdo completo
 * @param {string} match - Link encontrado
 * @returns {string} Contexto
 */
function findContext(content, match) {
  const index = content.indexOf(match);
  if (index === -1) return '';

  const start = Math.max(0, index - 50);
  const end = Math.min(content.length, index + match.length + 50);

  return content.slice(start, end).replace(/\n/g, ' ').trim();
}

// Exporta também como default
export default searchBrokenLinks;
