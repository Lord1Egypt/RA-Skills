/"
 * @module tools/frontmatter-set
 * @description Define ou atualiza propriedades no frontmatter
 */

import { CONFIG, getDefaultHeaders, buildUrl, normalizePath, successResponse, errorResponse } from '../config/defaults.js';

/**
 * Define uma propriedade no frontmatter
 * @param {Object} options - Opções
 * @param {string} options.path - Caminho da nota
 * @param {string} options.field - Nome do campo
 * @param {any} options.value - Valor a definir
 * @param {boolean} [options.createIfMissing=true] - Criar frontmatter se não existir
 * @param {boolean} [options.append=false] - Para arrays, adicionar ao invés de substituir
 * @returns {Promise<Object>} Resultado da operação
 */
export async function frontmatterSet(options) {
  try {
    const {
      path,
      field,
      value,
      createIfMissing = true,
      append = false,
    } = options;

    // Validações
    if (!path) {
      return errorResponse('Caminho da nota é obrigatório');
    }

    if (!field) {
      return errorResponse('Nome do campo é obrigatório');
    }

    if (value === undefined) {
      return errorResponse('Valor é obrigatório');
    }

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

    // Verifica se tem frontmatter
    const hasFrontmatter = content.startsWith('---\n');

    if (!hasFrontmatter) {
      if (!createIfMissing) {
        return errorResponse('Nota não possui frontmatter e createIfMissing=false');
      }

      // Cria frontmatter
      const newFrontmatter = buildFrontmatter({ [field]: value });
      content = newFrontmatter + '\n\n' + content;
    } else {
      // Atualiza frontmatter existente
      const frontmatterMatch = content.match(/^(---\n)([\s\S]*?)(\n---)/);
      if (!frontmatterMatch) {
        return errorResponse('Formato de frontmatter inválido');
      }

      const existingYaml = frontmatterMatch[2];
      const existingData = parseYaml(existingYaml);

      // Para arrays com append=true
      if (append && Array.isArray(existingData[field]) && Array.isArray(value)) {
        existingData[field] = [...existingData[field], ...value];
      } else if (append && Array.isArray(existingData[field])) {
        existingData[field].push(value);
      } else {
        existingData[field] = value;
      }

      // Atualiza modified
      existingData.modified = new Date().toISOString().split('T')[0];

      const newFrontmatter = buildFrontmatter(existingData);
      content = newFrontmatter + content.slice(frontmatterMatch[0].length);
    }

    // Salva
    const writeResponse = await fetch(buildUrl(`/vault/${normalizedPath}`), {
      method: 'PUT',
      headers: getDefaultHeaders(),
      body: content,
    });

    if (!writeResponse.ok) {
      throw new Error('Erro ao salvar nota');
    }

    return successResponse(
      `✏️ Campo '${field}' atualizado`,
      {
        path: normalizedPath,
        field,
        value,
        operation: append ? 'appended' : 'set',
      },
      '✏️'
    );

  } catch (error) {
    return errorResponse(`Falha ao atualizar frontmatter: ${error.message}`, error);
  }
}

/**
 * Constrói frontmatter YAML
 * @param {Object} data - Dados do frontmatter
 * @returns {string} YAML formatado
 */
function buildFrontmatter(data) {
  const lines = ['---'];

  for (const [key, value] of Object.entries(data)) {
    if (Array.isArray(value)) {
      if (value.length === 0) {
        lines.push(`${key}: []`);
      } else {
        lines.push(`${key}:`);
        value.forEach(item => lines.push(`  - ${formatYamlValue(item)}`));
      }
    } else if (typeof value === 'string' && value.includes('\n')) {
      lines.push(`${key}: |`);
      value.split('\n').forEach(line => lines.push(`  ${line}`));
    } else {
      lines.push(`${key}: ${formatYamlValue(value)}`);
    }
  }

  lines.push('---');
  return lines.join('\n');
}

/**
 * Formata valor para YAML
 * @param {any} value - Valor
 * @returns {string} Valor formatado
 */
function formatYamlValue(value) {
  if (value === null) return 'null';
  if (typeof value === 'boolean') return value.toString();
  if (typeof value === 'number') return String(value);
  if (typeof value === 'string') {
    if (value.includes('"') || value.includes('\n') || value.includes(':')) {
      return `"${value.replace(/"/g, '\\"')}"`;
    }
    return value;
  }
  return String(value);
}

/**
 * Parseia YAML simples
 * @param {string} yaml - Conteúdo YAML
 * @returns {Object} Objeto parseado
 */
function parseYaml(yaml) {
  const result = {};
  const lines = yaml.split('\n');
  let currentKey = null;

  for (const line of lines) {
    const trimmed = line.trim();

    if (trimmed.startsWith('- ') && currentKey) {
      const value = trimmed.slice(2).trim();
      if (Array.isArray(result[currentKey])) {
        result[currentKey].push(parseYamlValue(value));
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
      } else {
        result[key] = parseYamlValue(val);
        currentKey = null;
      }
    }
  }

  return result;
}

/**
 * Parseia valor de string YAML
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
export default frontmatterSet;
