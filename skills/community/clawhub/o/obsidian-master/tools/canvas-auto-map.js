/**
 * @module tools/canvas-auto-map
 * @description Gera um mapa visual automático a partir de um tema ou conjunto de notas
 */

import { CONFIG, getDefaultHeaders, buildUrl, successResponse, errorResponse } from '../config/defaults.js';
import { canvasCreate } from './canvas-create.js';
import { canvasAddNote } from './canvas-add-note.js';
import { canvasAddCard } from './canvas-add-card.js';
import { canvasConnect } from './canvas-connect.js';
import { searchByTag } from './search-by-tag.js';
import { searchBacklinks } from './search-backlinks.js';

/**
 * Gera um canvas automaticamente a partir de um tema
 * @param {Object} options - Opções
 * @param {string} options.theme - Tema central
 * @param {string} [options.centerNote] - Nota central (opcional)
 * @param {Array<string>} [options.tags] - Tags para buscar notas relacionadas
 * @param {number} [options.maxNodes=20] - Máximo de nós
 * @param {boolean} [options.open=true] - Abrir após criar
 * @returns {Promise<Object>} Canvas gerado
 */
export async function canvasAutoMap(options) {
  try {
    const {
      theme,
      centerNote,
      tags = [],
      maxNodes = 20,
      open = true,
    } = options;

    if (!theme) {
      return errorResponse('Tema é obrigatório');
    }

    if (!CONFIG.apiKey) {
      return errorResponse('OBSIDIAN_API_KEY não configurada');
    }

    // Coleta notas relacionadas
    const relatedNotes = await collectRelatedNotes(theme, tags, maxNodes);

    if (relatedNotes.length === 0) {
      return errorResponse(`Nenhuma nota encontrada para o tema: ${theme}`);
    }

    // Cria o canvas
    const canvasName = `${theme} Map`;
    const canvasResult = await canvasCreate({
      name: canvasName,
      open: false,
    });

    if (!canvasResult.success) {
      return canvasResult;
    }

    const canvasPath = canvasResult.data.path;

    // Adiciona nó central (card ou nota)
    let centerNodeId = 'center';
    if (centerNote) {
      await canvasAddNote({
        canvasPath,
        notePath: centerNote,
        x: 0,
        y: 0,
        width: 500,
        height: 500,
        color: '1', // Vermelho
      });
    } else {
      await canvasAddCard({
        canvasPath,
        text: `# ${theme}\n\nMapa de conhecimento gerado automaticamente.`,
        x: 0,
        y: 0,
        width: 400,
        height: 200,
        color: '1',
      });
    }

    // Distribui nós em círculo
    const radius = 600;
    const angleStep = (2 * Math.PI) / relatedNotes.length;

    const nodeIds = [];
    for (let i = 0; i < relatedNotes.length; i++) {
      const note = relatedNotes[i];
      const angle = i * angleStep;
      const x = Math.cos(angle) * radius;
      const y = Math.sin(angle) * radius;

      await canvasAddNote({
        canvasPath,
        notePath: note.path,
        x: x - 200,
        y: y - 200,
        width: 400,
        height: 400,
      });

      // Armazena ID para conexão (simplificado - na prática precisaria do ID real)
      nodeIds.push({ index: i, note: note.path });
    }

    // Abre se solicitado
    if (open) {
      await fetch(buildUrl(`/open/${canvasPath}`), {
        method: 'POST',
        headers: getDefaultHeaders(),
      });
    }

    return successResponse(
      `🗺️ Mapa '${canvasName}' gerado com ${relatedNotes.length} notas`,
      {
        canvasPath,
        theme,
        nodeCount: relatedNotes.length + 1, // + central
        notes: relatedNotes.map(n => n.path),
      },
      '🗺️'
    );

  } catch (error) {
    return errorResponse(`Falha ao gerar mapa: ${error.message}`, error);
  }
}

/**
 * Coleta notas relacionadas ao tema
 * @param {string} theme - Tema
 * @param {Array<string>} tags - Tags adicionais
 * @param {number} maxNodes - Máximo
 * @returns {Promise<Array>} Notas
 */
async function collectRelatedNotes(theme, tags, maxNodes) {
  const notes = [];
  const seen = new Set();

  // Busca por tema
  const searchResult = await searchByTag({
    tags: [theme, ...tags],
    matchAll: false,
  });

  if (searchResult.success) {
    for (const result of searchResult.data.results) {
      if (seen.has(result.path)) continue;
      if (notes.length >= maxNodes) break;

      notes.push(result);
      seen.add(result.path);
    }
  }

  // Busca por texto também
  try {
    const textSearch = await fetch(buildUrl('/search/simple/'), {
      method: 'POST',
      headers: getDefaultHeaders(),
      body: JSON.stringify({ query: theme }),
    });

    if (textSearch.ok) {
      const textResults = await textSearch.json();
      for (const result of textResults) {
        if (seen.has(result.path)) continue;
        if (notes.length >= maxNodes) break;

        notes.push({ path: result.path, file: result.file });
        seen.add(result.path);
      }
    }
  } catch {
    // Ignora erro
  }

  return notes;
}

// Exporta também como default
export default canvasAutoMap;
