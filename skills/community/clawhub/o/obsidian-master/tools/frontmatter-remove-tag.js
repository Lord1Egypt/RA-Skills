/"
 * @module tools/frontmatter-remove-tag
 * @description Remove uma tag do frontmatter de uma nota
 */

import { CONFIG, getDefaultHeaders, buildUrl, normalizePath, successResponse, errorResponse } from '../config/defaults.js';

/**
 * Remove uma tag do frontmatter
 * @param {Object} options - Opções
 * @param {string} options.path - Caminho da nota
 * @param {string} options.tag - Tag a remover (sem #)
 * @param {boolean} [options.silentIfMissing=true] - Não retornar erro se tag não existe
 * @returns {Promise<Object>} Resultado da operação
 */
export async function frontmatterRemoveTag(options) {
  try {
    const {
      path,
      tag,
      silentIfMissing = true,
    } = options;

    // Validações
    if (!path) {
      return errorResponse('Caminho da nota é obrigatório');
    }

    if (!tag) {
      return errorResponse('Tag é obrigatória');
    }

    // Normaliza tag
    const normalizedTag = tag.replace(/^#/, '').trim().toLowerCase();

    if (!CONFIG.apiKey) {
      return errorResponse('OBSIDIAN_API_KEY não configurada');
    }

    const normalizedPath = normalizePath(path);

    // Lê conteúdo atual
    const readResponse = await fetch(buildUrl(`/vault/${normalizedPath}`), {
      method: 'GET',
      headers: getDefaultHeaders(),
    });

    if (!readResponse.ok) {
      return errorResponse(`Nota não encontrada: ${normalizedPath}`);
    }

    let content = await readResponse.text();

    // Extrai frontmatter
    const frontmatterMatch = content.match(/^---\n([\s\S]*?)\n---/);
    if (!frontmatterMatch) {
      if (silentIfMissing) {
        return successResponse(
          `⏩ Nota sem frontmatter`,
          { path: normalizedPath, skipped: true },
          '⏩'
        );
      }
      return errorResponse('Nota não possui frontmatter');
    }

    const frontmatter = parseFrontmatter(frontmatterMatch[1]);

    // Verifica se tem tags
    if (!frontmatter.tags || !Array.isArray(frontmatter.tags) || frontmatter.tags.length === 0) {
      if (silentIfMissing) {
        return successResponse(
          `⏩ Nota sem tags`,
          { path: normalizedPath, skipped: true },
          '⏩'
        );
      }
      return errorResponse('Nota não possui tags no frontmatter');
    }

    // Verifica se tag existe
    const tagIndex = frontmatter.tags.findIndex(
      t => t.toLowerCase() === normalizedTag.toLowerCase()
    );

    if (tagIndex === -1) {
      if (silentIfMissing) {
        return successResponse(
          `⏩ Tag '#${normalizedTag}' não existe na nota`,
          {
            path: normalizedPath,
            tag: normalizedTag,
            skipped: true,
            existingTags: frontmatter.tags,
          },
          '⏩'
        );
      }
      return errorResponse(`Tag '#${normalizedTag}' não encontrada na nota`);
    }

    // Remove a tag
    const removedTag = frontmatter.tags[tagIndex];
    frontmatter.tags.splice(tagIndex, 1);
    frontmatter.modified = new Date().toISOString().split('T')[0];

    // Reconstrói frontmatter
    const newFrontmatter = buildFrontmatter(frontmatter);
    const newContent = newFrontmatter + content.slice(frontmatterMatch[0].length);

    // Salva
    const writeResponse = await fetch(buildUrl(`/vault/${normalizedPath}`), {
      method: 'PUT',
      headers: getDefaultHeaders(),
      body: newContent,
    });

    if (!writeResponse.ok) {
      throw new Error('Erro ao salvar nota');
    }

    return successResponse(
      `🗑️ Tag '#${removedTag}' removida`,
      {
        path: normalizedPath,
        tag: removedTag,
        remainingTags: frontmatter.tags.length,
        allTags: frontmatter.tags,
      },
      '🗑️'
    );

  } catch (error) {
    return errorResponse(`Falha ao remover tag: ${error.message}`, error);
  }
}

/**
 * Parseia frontmatter
 * @param {string} yaml - Conteúdo YAML
 * @returns {Object} Frontmatter
 */
function parseFrontmatter(yaml) {
  const result = {};
  const lines = yaml.split('\n');
  let currentKey = null;

  for (const line of lines) {
    const trimmed = line.trim();

    if (trimmed.startsWith('- ') && currentKey) {
      const value = trimmed.slice(2).trim().replace(/^["']|["']$/g, '');
      if (Array.isArray(result[currentKey])) {
        result[currentKey].push(value);
      }
      continue;
    }

    const match = trimmed.match(/^([^:]+):\s*(.*)$/);
    if (match) {
      const key = match[1].trim();
      const val = match[2].trim();

      if (val === '' || val === '[]') {
        result[key] = [];
        currentKey = key;
      } else if (val.startsWith('[') && val.endsWith(']')) {
        result[key] = val.slice(1, -1).split(',').map(s => s.trim().replace(/^["']|["']$/g, ''));
        currentKey = null;
      } else {
        result[key] = val.replace(/^["']|["']$/g, '');
        currentKey = null;
      }
    }
  }

  return result;
}

/**
 * Constrói frontmatter YAML
 * @param {Object} data - Dados
 * @returns {string} YAML
 */
function buildFrontmatter(data) {
  const lines = ['---'];

  for (const [key, value] of Object.entries(data)) {
    if (Array.isArray(value)) {
      if (value.length === 0) {
        lines.push(`${key}: []`);
      } else {
        lines.push(`${key}:`);
        value.forEach(item => lines.push(`  - ${item}`));
      }
    } else {
      lines.push(`${key}: ${value}`);
    }
  }

  lines.push('---');
  return lines.join('\n') + '\n';
}

// Exporta também como default
export default frontmatterRemoveTag;
