/"
 * @module tools/search-by-frontmatter
 * @description Busca notas por valores específicos no frontmatter
 */

import { CONFIG, getDefaultHeaders, buildUrl, successResponse, errorResponse } from '../config/defaults.js';
import { folderList } from './folder-list.js';

/**
 * Busca notas por propriedade do frontmatter
 * @param {Object} options - Opções de busca
 * @param {string} options.field - Nome do campo (ex: 'status', 'type')
 * @param {any} options.value - Valor a buscar
 * @param {string} [options.operator='equals'] - Operador: 'equals', 'contains', 'exists', 'in'
 * @param {string} [options.folder] - Limitar a uma pasta
 * @param {boolean} [options.multiple=false] - Permitir múltiplos valores (array)
 * @returns {Promise<Object>} Notas encontradas
 */
export async function searchByFrontmatter(options) {
  try {
    const {
      field,
      value,
      operator = 'equals',
      folder,
      multiple = false,
    } = options;

    if (!field) {
      return errorResponse('Campo do frontmatter é obrigatório');
    }

    if (!CONFIG.apiKey) {
      return errorResponse('OBSIDIAN_API_KEY não configurada');
    }

    // Lista arquivos
    const listResult = await folderList({ path: folder || '', recursive: true });
    if (!listResult.success) {
      return errorResponse('Não foi possível listar arquivos');
    }

    const files = listResult.data.files.filter(f => f.extension === 'md');
    const results = [];

    for (const file of files) {
      try {
        const response = await fetch(buildUrl(`/vault/${file.path}`), {
          method: 'GET',
          headers: getDefaultHeaders(),
        });

        if (!response.ok) continue;

        const content = await response.text();

        // Extrai frontmatter
        const frontmatter = extractFrontmatter(content);

        if (!frontmatter) continue;

        // Verifica se campo existe e valor corresponde
        const fieldValue = frontmatter[field];

        if (fieldValue === undefined && operator !== 'exists') continue;

        const matches = matchValue(fieldValue, value, operator, multiple);

        if (matches) {
          results.push({
            name: file.name,
            path: file.path,
            frontmatter,
            [field]: fieldValue,
          });
        }

      } catch {
        // Ignora erro individual
      }
    }

    // Ordena por nome
    results.sort((a, b) => a.name.localeCompare(b.name));

    const valueStr = multiple && Array.isArray(value)
      ? value.join(', ')
      : String(value);

    return successResponse(
      `📋 ${results.length} nota(s) com ${field} ${operator} "${valueStr}"`,
      {
        field,
        value,
        operator,
        totalResults: results.length,
        results,
      },
      '📋'
    );

  } catch (error) {
    return errorResponse(`Falha na busca por frontmatter: ${error.message}`, error);
  }
}

/**
 * Extrai frontmatter de conteúdo
 * @param {string} content - Conteúdo da nota
 * @returns {Object|null} Frontmatter parseado
 */
function extractFrontmatter(content) {
  const match = content.match(/^---\n([\s\S]*?)\n---/);
  if (!match) return null;

  const yaml = match[1];
  const result = {};

  const lines = yaml.split('\n');
  let currentKey = null;
  let currentArray = null;

  for (const line of lines) {
    const trimmed = line.trim();

    if (trimmed.startsWith('- ') && currentKey) {
      const value = trimmed.slice(2).trim();
      if (Array.isArray(result[currentKey])) {
        result[currentKey].push(parseValue(value));
      }
      continue;
    }

    const keyMatch = trimmed.match(/^([^:]+):\s*(.*)$/);
    if (keyMatch) {
      const key = keyMatch[1].trim();
      const val = keyMatch[2].trim();

      if (val === '' || val === '[]') {
        result[key] = [];
        currentKey = key;
      } else {
        result[key] = parseValue(val);
        currentKey = null;
      }
    }
  }

  return result;
}

/**
 * Parseia um valor YAML simples
 * @param {string} value - Valor em string
 * @returns {any} Valor parseado
 */
function parseValue(value) {
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

/**
 * Compara valores segundo operador
 * @param {any} fieldValue - Valor do campo
 * @param {any} searchValue - Valor buscado
 * @param {string} operator - Operador
 * @param {boolean} multiple - Múltiplos valores
 * @returns {boolean} Match
 */
function matchValue(fieldValue, searchValue, operator, multiple) {
  switch (operator) {
    case 'exists':
      return fieldValue !== undefined;

    case 'equals':
      if (multiple && Array.isArray(searchValue)) {
        return searchValue.some(v => String(fieldValue).toLowerCase() === String(v).toLowerCase());
      }
      return String(fieldValue).toLowerCase() === String(searchValue).toLowerCase();

    case 'contains':
      if (Array.isArray(fieldValue)) {
        return fieldValue.some(v => String(v).toLowerCase().includes(String(searchValue).toLowerCase()));
      }
      return String(fieldValue).toLowerCase().includes(String(searchValue).toLowerCase());

    case 'in':
      if (Array.isArray(searchValue)) {
        return searchValue.includes(fieldValue);
      }
      return false;

    default:
      return false;
  }
}

// Exporta também como default
export default searchByFrontmatter;
