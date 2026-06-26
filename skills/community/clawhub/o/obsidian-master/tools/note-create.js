/**
 * @module tools/note-create
 * @description Cria uma nova nota com frontmatter completo e opcionalmente aplica um template
 */

import { CONFIG, getDefaultHeaders, buildUrl, normalizePath, successResponse, errorResponse, warningResponse, formatDailyDate, formatZettelId } from '../config/defaults.js';
import { TEMPLATES, processTemplate, getTypeEmoji } from '../config/vault-structure.js';

/**
 * Cria uma nova nota no vault
 * @param {Object} options - Opções de criação
 * @param {string} options.title - Título da nota
 * @param {string} [options.content=''] - Conteúdo da nota (se vazio, usa template)
 * @param {string} [options.folder] - Pasta destino (padrão: inbox)
 * @param {string} [options.type='note'] - Tipo: note, project, area, daily, zettel, moc, etc
 * @param {Array<string>} [options.tags=[]] - Tags para o frontmatter
 * @param {Object} [options.frontmatter={}] - Propriedades adicionais do frontmatter
 * @param {string} [options.template] - Nome do template a usar
 * @param {boolean} [options.open=false] - Abrir a nota no Obsidian após criar
 * @returns {Promise<Object>} Resultado da operação
 */
export async function noteCreate(options) {
  try {
    const {
      title,
      content = '',
      folder = CONFIG.folders.inbox,
      type = 'note',
      tags = [],
      frontmatter = {},
      template,
      open = false,
    } = options;

    // Validações
    if (!title) {
      return errorResponse('Título da nota é obrigatório');
    }

    if (!CONFIG.apiKey) {
      return errorResponse('OBSIDIAN_API_KEY não configurada');
    }

    // Gera nome do arquivo
    const fileName = `${title}.md`;
    const filePath = folder ? `${folder}/${fileName}` : fileName;
    const normalizedPath = normalizePath(filePath);

    // Verifica se nota já existe
    const existsCheck = await checkNoteExists(normalizedPath);
    if (existsCheck.exists) {
      return errorResponse(`Nota já existe: ${normalizedPath}. Use note-update para modificar.`);
    }

    // Prepara conteúdo
    let finalContent = content;
    const now = new Date();
    const dateStr = formatDailyDate(now);

    if (!finalContent) {
      // Usa template baseado no tipo ou especificado
      const templateName = template || type;
      const templateContent = TEMPLATES[templateName] || TEMPLATES.note;

      const variables = {
        title,
        date: dateStr,
        datetime: now.toISOString(),
        zettelId: formatZettelId(now),
        tags: tags.length > 0 ? `[${tags.join(', ')}]` : '[]',
        ...frontmatter,
      };

      finalContent = processTemplate(templateContent, variables);
    } else if (type !== 'raw') {
      // Adiciona frontmatter se não for conteúdo raw
      const typeEmoji = getTypeEmoji(type);
      const frontmatterYaml = buildFrontmatter({
        title,
        created: dateStr,
        modified: dateStr,
        tags,
        type,
        status: 'active',
        ...frontmatter,
      });

      finalContent = frontmatterYaml + '\n' + finalContent;
    }

    // Cria a nota via API
    const response = await fetch(buildUrl(`/vault/${normalizedPath}`), {
      method: 'PUT',
      headers: getDefaultHeaders(),
      body: finalContent,
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Erro ${response.status}: ${errorText}`);
    }

    // Abre a nota se solicitado
    if (open) {
      await fetch(buildUrl(`/open/${normalizedPath}`), {
        method: 'POST',
        headers: getDefaultHeaders(),
      });
    }

    return successResponse(
      `${typeEmoji} Nota '${title}' criada em ${folder || 'raiz'}`,
      {
        path: normalizedPath,
        title,
        type,
        tags,
        folder: folder || 'raiz',
        created: dateStr,
        opened: open,
      },
      '✅'
    );

  } catch (error) {
    return errorResponse(`Falha ao criar nota: ${error.message}`, error);
  }
}

/**
 * Verifica se uma nota já existe
 * @param {string} path - Caminho da nota
 * @returns {Promise<Object>} { exists: boolean }
 */
async function checkNoteExists(path) {
  try {
    const response = await fetch(buildUrl(`/vault/${path}`), {
      method: 'HEAD',
      headers: getDefaultHeaders(),
    });
    return { exists: response.ok };
  } catch {
    return { exists: false };
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
        value.forEach(item => lines.push(`  - ${item}`));
      }
    } else if (typeof value === 'string' && value.includes('\n')) {
      lines.push(`${key}: |`);
      value.split('\n').forEach(line => lines.push(`  ${line}`));
    } else {
      lines.push(`${key}: ${JSON.stringify(value)}`);
    }
  }

  lines.push('---');
  return lines.join('\n');
}

// Exporta também como default
export default noteCreate;
