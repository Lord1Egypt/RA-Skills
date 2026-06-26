/**
 * @module tools/frontmatter-add-tag
 * @description Adiciona uma tag ao frontmatter de uma nota
 */

import { CONFIG, getDefaultHeaders, buildUrl, normalizePath, successResponse, errorResponse } from '../config/defaults.js';

/**
 * Adiciona uma tag ao frontmatter
 * @param {Object} options - Opções
 * @param {string} options.path - Caminho da nota
 * @param {string} options.tag - Tag a adicionar (sem #)
 * @param {boolean} [options.avoidDuplicates=true] - Evitar duplicatas
 * @returns {Promise<Object>} Resultado da operação
 */
export async function frontmatterAddTag(options) {
  try {
    const {
      path,
      tag,
      avoidDuplicates = true,
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

    // Extrai frontmatter existente ou cria novo
    let frontmatter = {};
    let bodyStart = 0;

    const frontmatterMatch = content.match(/^---\n([\s\S]*?)\n---/);
    if (frontmatterMatch) {
      frontmatter = parseFrontmatter(frontmatterMatch[1]);
      bodyStart = frontmatterMatch[0].length;
    }

    // Garante que tags é array
    if (!frontmatter.tags) {
      frontmatter.tags = [];
    } else if (!Array.isArray(frontmatter.tags)) {
      frontmatter.tags = [frontmatter.tags];
    }

    // Verifica duplicata
    if (avoidDuplicates && frontmatter.tags.includes(normalizedTag)) {
      return successResponse(
        `⏩ Tag '#${normalizedTag}' já existe na nota`,
        {
          path: normalizedPath,
          tag: normalizedTag,
          skipped: true,
          existingTags: frontmatter.tags,
        },
        '⏩'
      );
    }

    // Adiciona tag
    frontmatter.tags.push(normalizedTag);
    frontmatter.modified = new Date().toISOString().split('T')[0];

    // Reconstrói frontmatter
    const newFrontmatter = buildFrontmatter(frontmatter);
    const newContent = newFrontmatter + content.slice(bodyStart);

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
      `🏷️ Tag '#${normalizedTag}' adicionada`,
      {
        path: normalizedPath,
        tag: normalizedTag,
        totalTags: frontmatter.tags.length,
        allTags: frontmatter.tags,
      },
      '🏷️'
    );

  } catch (error) {
    return errorResponse(`Falha ao adicionar tag: ${error.message}`, error);
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
        // Array inline: [a, b, c]
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
export default frontmatterAddTag;
