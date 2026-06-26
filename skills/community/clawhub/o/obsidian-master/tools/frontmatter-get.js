/"
 * @module tools/frontmatter-get
 * @description Lê e extrai propriedades do frontmatter de uma nota
 */

import { CONFIG, getDefaultHeaders, buildUrl, normalizePath, successResponse, errorResponse } from '../config/defaults.js';

/**
 * Lê propriedades do frontmatter de uma nota
 * @param {Object} options - Opções de leitura
 * @param {string} options.path - Caminho da nota
 * @param {string} [options.field] - Campo específico (se vazio, retorna todos)
 * @param {boolean} [options.includeComputed=false] - Incluir campos computados
 * @returns {Promise<Object>} Propriedades do frontmatter
 */
export async function frontmatterGet(options) {
  try {
    const {
      path,
      field,
      includeComputed = false,
    } = options;

    // Validações
    if (!path) {
      return errorResponse('Caminho da nota é obrigatório');
    }

    if (!CONFIG.apiKey) {
      return errorResponse('OBSIDIAN_API_KEY não configurada');
    }

    const normalizedPath = normalizePath(path);

    // Lê a nota
    const response = await fetch(buildUrl(`/vault/${normalizedPath}`), {
      method: 'GET',
      headers: getDefaultHeaders(),
    });

    if (!response.ok) {
      if (response.status === 404) {
        return errorResponse(`Nota não encontrada: ${normalizedPath}`);
      }
      const errorText = await response.text();
      throw new Error(`Erro ${response.status}: ${errorText}`);
    }

    const content = await response.text();

    // Extrai frontmatter
    const frontmatter = extractFrontmatter(content);

    if (!frontmatter) {
      return errorResponse(`Nota não possui frontmatter: ${normalizedPath}`);
    }

    // Se solicitou campo específico
    if (field) {
      if (frontmatter[field] === undefined) {
        return errorResponse(`Campo '${field}' não encontrado no frontmatter`);
      }

      return successResponse(
        `📋 Campo '${field}' obtido`,
        {
          path: normalizedPath,
          field,
          value: frontmatter[field],
          exists: true,
        },
        '📋'
      );
    }

    // Adiciona campos computados se solicitado
    if (includeComputed) {
      frontmatter._computed = {
        wordCount: content.split(/\s+/).filter(w => w.length > 0).length,
        hasBacklinks: false, // Seria necessário buscar
        fileSize: content.length,
      };
    }

    return successResponse(
      `📋 Frontmatter completo de '${normalizedPath.split('/').pop()}'`,
      {
        path: normalizedPath,
        frontmatter,
        fieldCount: Object.keys(frontmatter).length,
      },
      '📋'
    );

  } catch (error) {
    return errorResponse(`Falha ao ler frontmatter: ${error.message}`, error);
  }
}

/**
 * Extrai frontmatter de conteúdo
 * @param {string} content - Conteúdo da nota
 * @returns {Object|null} Frontmatter parseado ou null
 */
function extractFrontmatter(content) {
  const match = content.match(/^---\n([\s\S]*?)\n---/);
  if (!match) return null;

  const yaml = match[1];
  const result = {};

  const lines = yaml.split('\n');
  let currentKey = null;

  for (const line of lines) {
    const trimmed = line.trim();

    // Array item
    if (trimmed.startsWith('- ') && currentKey) {
      const value = trimmed.slice(2).trim();
      if (Array.isArray(result[currentKey])) {
        result[currentKey].push(parseYamlValue(value));
      }
      continue;
    }

    // Key: value
    const keyMatch = trimmed.match(/^([^:]+):\s*(.*)$/);
    if (keyMatch) {
      const key = keyMatch[1].trim();
      const val = keyMatch[2].trim();

      if (val === '' || val === '[]') {
        result[key] = [];
        currentKey = key;
      } else {
        result[key] = parseYamlValue(val);
        currentKey = null;
      }
    }
  }

  return result;
}

/**
 * Parseia valor YAML
 * @param {string} value - Valor em string
 * @returns {any} Valor parseado
 */
function parseYamlValue(value) {
  if (value === 'true') return true;
  if (value === 'false') return false;
  if (value === 'null' || value === '~') return null;
  if (/^-?\d+$/.test(value)) return parseInt(value, 10);
  if (/^-?\d+\.\d+$/.test(value)) return parseFloat(value);
  if (value.startsWith('"') && value.endsWith('"')) {
    return value.slice(1, -1).replace(/\\"/g, '"');
  }
  if (value.startsWith("'") && value.endsWith("'")) {
    return value.slice(1, -1).replace(/\\'/g, "'");
  }
  return value;
}

// Exporta também como default
export default frontmatterGet;
