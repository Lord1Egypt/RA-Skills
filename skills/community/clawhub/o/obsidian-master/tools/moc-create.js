/"
 * @module tools/moc-create
 * @description Cria um Map of Content automaticamente
 */

import { CONFIG, getDefaultHeaders, buildUrl, successResponse, errorResponse } from '../config/defaults.js';
import { noteCreate } from './note-create.js';
import { searchByTag } from './search-by-tag.js';

/**
 * Cria um MOC (Map of Content)
 * @param {Object} options - Opções
 * @param {string} options.theme - Tema do MOC
 * @param {string} [options.folder] - Pasta (padrão: 80 - MOCs)
 * @param {Array<string>} [options.tags] - Tags para buscar notas
 * @param {boolean} [options.includeBacklinks=true] - Incluir notas que linkam
 * @returns {Promise<Object>} MOC criado
 */
export async function mocCreate(options) {
  try {
    const {
      theme,
      folder = CONFIG.folders.mocs,
      tags = [],
      includeBacklinks = true,
    } = options;

    if (!theme) {
      return errorResponse('Tema é obrigatório');
    }

    if (!CONFIG.apiKey) {
      return errorResponse('OBSIDIAN_API_KEY não configurada');
    }

    // Coleta notas
    const relatedNotes = [];
    const seen = new Set();

    // Por tags
    if (tags.length > 0) {
      const tagResult = await searchByTag({ tags, matchAll: false });
      if (tagResult.success) {
        for (const note of tagResult.data.results) {
          if (!seen.has(note.path)) {
            relatedNotes.push(note);
            seen.add(note.path);
          }
        }
      }
    }

    // Por tema (busca por texto)
    try {
      const searchResponse = await fetch(buildUrl('/search/simple/'), {
        method: 'POST',
        headers: getDefaultHeaders(),
        body: JSON.stringify({ query: theme }),
      });

      if (searchResponse.ok) {
        const results = await searchResponse.json();
        for (const r of results) {
          if (!seen.has(r.path)) {
            relatedNotes.push(r);
            seen.add(r.path);
          }
        }
      }
    } catch {
      // Ignora
    }

    // Gera conteúdo
    const content = generateMocContent(theme, relatedNotes);

    // Cria nota
    return await noteCreate({
      title: `${theme} MOC`,
      content,
      folder,
      type: 'moc',
      tags: ['moc', theme.toLowerCase().replace(/\s+/g, '-')],
    });

  } catch (error) {
    return errorResponse(`Falha ao criar MOC: ${error.message}`, error);
  }
}

/**
 * Gera conteúdo do MOC
 * @param {string} theme - Tema
 * @param {Array} notes - Notas relacionadas
 * @returns {string} Conteúdo
 */
function generateMocContent(theme, notes) {
  const now = new Date().toISOString().split('T')[0];

  let content = `---
title: "${theme} MOC"
created: ${now}
type: moc
tags: [moc, ${theme.toLowerCase().replace(/\s+/g, '-')}]
---

# 🗺️ ${theme}

> Map of Content para o tema: **${theme}**

Criado em: ${now}

## Visão Geral

Este MOC organiza notas relacionadas a ${theme}.

## 📑 Notas Relacionadas (${notes.length})

`;

  // Agrupa por pasta
  const byFolder = {};
  for (const note of notes) {
    const folder = note.path.split('/')[0] || 'Raiz';
    if (!byFolder[folder]) byFolder[folder] = [];
    byFolder[folder].push(note);
  }

  for (const [folder, folderNotes] of Object.entries(byFolder)) {
    content += `### ${folder}\n\n`;
    for (const note of folderNotes) {
      const name = note.name || note.path.split('/').pop().replace('.md', '');
      content += `- [[${name}]]\n`;
    }
    content += '\n';
  }

  content += `## 🔗 Conexões

- [Adicione links para MOCs relacionados]

## 📝 Em Desenvolvimento

- [Ideias a explorar]

---

*MOC gerado automaticamente*`;

  return content;
}

// Exporta também como default
export default mocCreate;
