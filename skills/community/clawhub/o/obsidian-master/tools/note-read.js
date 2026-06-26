/**
 * @module tools/note-read
 * @description Lê uma nota do vault em diferentes formatos: raw, parsed ou frontmatter
 */

import { CONFIG, getDefaultHeaders, buildUrl, normalizePath, successResponse, errorResponse } from '../config/defaults.js';

/**
 * Lê o conteúdo de uma nota
 * @param {Object} options - Opções de leitura
 * @param {string} options.path - Caminho da nota (ex: "Projetos/Nota.md" ou "Projetos/Nota")
 * @param {string} [options.format='raw'] - Formato: 'raw', 'parsed', ou 'frontmatter'
 * @param {boolean} [options.includeMetadata=true] - Incluir metadados da nota
 * @returns {Promise<Object>} Conteúdo da nota e metadados
 */
export async function noteRead(options) {
  try {
    const {
      path,
      format = 'raw',
      includeMetadata = true,
    } = options;

    // Validações
    if (!path) {
      return errorResponse('Caminho da nota é obrigatório');
    }

    if (!CONFIG.apiKey) {
      return errorResponse('OBSIDIAN_API_KEY não configurada');
    }

    const normalizedPath = normalizePath(path);

    // Faz a requisição
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

    const rawContent = await response.text();

    // Processa conforme formato solicitado
    let result = {
      path: normalizedPath,
      raw: rawContent,
    };

    if (format === 'frontmatter' || format === 'parsed') {
      const parsed = parseNote(rawContent);
      result.frontmatter = parsed.frontmatter;
      result.body = parsed.body;

      // Extrai elementos adicionais se formato for parsed
      if (format === 'parsed') {
        result.links = parsed.links;
        result.tags = parsed.tags;
        result.tasks = parsed.tasks;
        result.headers = parsed.headers;
        result.wordCount = parsed.body.split(/\s+/).filter(w => w.length > 0).length;
      }
    }

    // Busca metadados adicionais se solicitado
    if (includeMetadata) {
      const metadata = await fetchNoteMetadata(normalizedPath);
      result.metadata = metadata;
    }

    const title = normalizedPath.split('/').pop().replace('.md', '');

    return successResponse(
      `📖 Nota '${title}' lida com sucesso`,
      result,
      '📄'
    );

  } catch (error) {
    return errorResponse(`Falha ao ler nota: ${error.message}`, error);
  }
}

/**
 * Parseia o conteúdo de uma nota markdown
 * @param {string} content - Conteúdo raw da nota
 * @returns {Object} { frontmatter, body, links, tags, tasks, headers }
 */
function parseNote(content) {
  const result = {
    frontmatter: {},
    body: content,
    links: [],
    tags: [],
    tasks: { open: [], completed: [] },
    headers: [],
  };

  // Extrai frontmatter
  const frontmatterMatch = content.match(/^---\n([\s\S]*?)\n---/);
  if (frontmatterMatch) {
    result.frontmatter = parseYaml(frontmatterMatch[1]);
    result.body = content.slice(frontmatterMatch[0].length).trim();
  }

  // Extrai wikilinks [[Link]] ou [[Link|Texto]]
  const linkRegex = /\[\[([^\]|]+)(?:\|[^\]]+)?\]\]/g;
  let linkMatch;
  while ((linkMatch = linkRegex.exec(content)) !== null) {
    result.links.push(linkMatch[1]);
  }

  // Extrai tags #tag
  const tagRegex = /#([a-zA-Z0-9_\-\/]+)/g;
  let tagMatch;
  while ((tagMatch = tagRegex.exec(content)) !== null) {
    // Ignora tags dentro de código
    const before = content.slice(0, tagMatch.index);
    const inCodeBlock = (before.match(/```/g)?.length || 0) % 2 === 1;
    if (!inCodeBlock) {
      result.tags.push(tagMatch[1]);
    }
  }

  // Extrai tasks
  const taskOpenRegex = /^- \[ \] (.+)$/gm;
  let taskOpenMatch;
  while ((taskOpenMatch = taskOpenRegex.exec(content)) !== null) {
    result.tasks.open.push(taskOpenMatch[1]);
  }

  const taskDoneRegex = /^- \[x\] (.+)$/gim;
  let taskDoneMatch;
  while ((taskDoneMatch = taskDoneRegex.exec(content)) !== null) {
    result.tasks.completed.push(taskDoneMatch[1]);
  }

  // Extrai headers
  const headerRegex = /^(#{1,6})\s+(.+)$/gm;
  let headerMatch;
  while ((headerMatch = headerRegex.exec(content)) !== null) {
    result.headers.push({
      level: headerMatch[1].length,
      text: headerMatch[2],
    });
  }

  return result;
}

/**
 * Parse simples de YAML (apenas para frontmatter básico)
 * @param {string} yaml - Conteúdo YAML
 * @returns {Object} Objeto parseado
 */
function parseYaml(yaml) {
  const result = {};
  const lines = yaml.split('\n');
  let currentKey = null;
  let currentArray = null;

  for (const line of lines) {
    const trimmed = line.trim();

    // Array item
    if (trimmed.startsWith('- ') && currentKey) {
      const value = trimmed.slice(2).trim();
      result[currentKey].push(parseYamlValue(value));
      continue;
    }

    // Key: value
    const match = trimmed.match(/^([^:]+):\s*(.*)$/);
    if (match) {
      const key = match[1].trim();
      const value = match[2].trim();

      if (value === '') {
        // Pode ser array vazio ou valor nulo
        result[key] = [];
        currentKey = key;
      } else if (value === '[]') {
        result[key] = [];
      } else {
        result[key] = parseYamlValue(value);
      }
    }
  }

  return result;
}

/**
 * Parseia um valor YAML
 * @param {string} value - Valor em string
 * @returns {any} Valor parseado
 */
function parseYamlValue(value) {
  // Boolean
  if (value === 'true') return true;
  if (value === 'false') return false;
  // Null
  if (value === 'null' || value === '~') return null;
  // Number
  if (/^-?\d+$/.test(value)) return parseInt(value, 10);
  if (/^-?\d+\.\d+$/.test(value)) return parseFloat(value);
  // String (remove aspas)
  if (value.startsWith('"') && value.endsWith('"')) {
    return value.slice(1, -1).replace(/\\"/g, '"');
  }
  if (value.startsWith("'") && value.endsWith("'")) {
    return value.slice(1, -1).replace(/\\'/g, "'");
  }
  return value;
}

/**
 * Busca metadados da nota via API
 * @param {string} path - Caminho da nota
 * @returns {Promise<Object>} Metadados
 */
async function fetchNoteMetadata(path) {
  try {
    // Tenta obter informações do arquivo
    const response = await fetch(buildUrl(`/vault/${path}`), {
      method: 'HEAD',
      headers: getDefaultHeaders(),
    });

    return {
      size: response.headers.get('content-length'),
      lastModified: response.headers.get('last-modified'),
      exists: response.ok,
    };
  } catch {
    return { exists: false };
  }
}

// Exporta também como default
export default noteRead;
