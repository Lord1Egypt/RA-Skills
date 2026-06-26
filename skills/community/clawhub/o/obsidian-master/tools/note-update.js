/**
 * @module tools/note-update
 * @description Atualiza notas existentes com operações: append, prepend, replace ou section
 */

import { CONFIG, getDefaultHeaders, getPatchHeaders, buildUrl, normalizePath, successResponse, errorResponse } from '../config/defaults.js';

/**
 * Atualiza uma nota existente
 * @param {Object} options - Opções de atualização
 * @param {string} options.path - Caminho da nota
 * @param {string} options.content - Novo conteúdo
 * @param {string} [options.operation='append'] - Tipo: 'append', 'prepend', 'replace', 'section'
 * @param {string} [options.target] - Alvo para section (heading, frontmatter field)
 * @param {string} [options.targetType] - Tipo do alvo: 'heading', 'block', 'frontmatter'
 * @param {boolean} [options.addTimestamp=true] - Adicionar timestamp ao conteúdo
 * @returns {Promise<Object>} Resultado da operação
 */
export async function noteUpdate(options) {
  try {
    const {
      path,
      content,
      operation = 'append',
      target,
      targetType,
      addTimestamp = true,
    } = options;

    // Validações
    if (!path) {
      return errorResponse('Caminho da nota é obrigatório');
    }

    if (content === undefined || content === null) {
      return errorResponse('Conteúdo é obrigatório');
    }

    if (!CONFIG.apiKey) {
      return errorResponse('OBSIDIAN_API_KEY não configurada');
    }

    const normalizedPath = normalizePath(path);

    // Verifica se nota existe
    const existsCheck = await checkNoteExists(normalizedPath);
    if (!existsCheck.exists) {
      return errorResponse(`Nota não encontrada: ${normalizedPath}`);
    }

    // Prepara o conteúdo
    let finalContent = content;
    if (addTimestamp && operation === 'append') {
      const now = new Date().toLocaleString('pt-BR');
      finalContent = `\n\n**[${now}]**\n\n${content}`;
    }

    let response;

    // Operações específicas usam PATCH
    if (operation === 'section' && target && targetType) {
      response = await fetch(buildUrl(`/vault/${normalizedPath}`), {
        method: 'PATCH',
        headers: getPatchHeaders(operation, targetType, target),
        body: finalContent,
      });
    } else {
      // Operações append/prepend/replace usam GET + PUT
      const currentResponse = await fetch(buildUrl(`/vault/${normalizedPath}`), {
        method: 'GET',
        headers: getDefaultHeaders(),
      });

      if (!currentResponse.ok) {
        throw new Error('Não foi possível ler a nota atual');
      }

      const currentContent = await currentResponse.text();
      let newContent;

      switch (operation) {
        case 'prepend':
          newContent = finalContent + '\n\n' + currentContent;
          break;
        case 'replace':
          newContent = finalContent;
          break;
        case 'append':
        default:
          newContent = currentContent + '\n' + finalContent;
      }

      // Atualiza o modified no frontmatter
      newContent = updateModifiedDate(newContent);

      response = await fetch(buildUrl(`/vault/${normalizedPath}`), {
        method: 'PUT',
        headers: getDefaultHeaders(),
        body: newContent,
      });
    }

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Erro ${response.status}: ${errorText}`);
    }

    const title = normalizedPath.split('/').pop().replace('.md', '');

    return successResponse(
      `📝 Nota '${title}' atualizada (${operation})`,
      {
        path: normalizedPath,
        operation,
        target: target || 'body',
        contentLength: finalContent.length,
      },
      '✏️'
    );

  } catch (error) {
    return errorResponse(`Falha ao atualizar nota: ${error.message}`, error);
  }
}

/**
 * Atualiza a data de modificação no frontmatter
 * @param {string} content - Conteúdo da nota
 * @returns {string} Conteúdo com data atualizada
 */
function updateModifiedDate(content) {
  const today = new Date().toISOString().split('T')[0];

  // Se tem frontmatter, atualiza o modified
  if (content.startsWith('---')) {
    const frontmatterEnd = content.indexOf('---', 3);
    if (frontmatterEnd !== -1) {
      const frontmatter = content.slice(0, frontmatterEnd + 3);
      const body = content.slice(frontmatterEnd + 3);

      // Atualiza ou adiciona modified
      if (frontmatter.includes('modified:')) {
        const newFrontmatter = frontmatter.replace(
          /modified:\s*[^\n]+/,
          `modified: ${today}`
        );
        return newFrontmatter + body;
      } else {
        // Adiciona modified antes do fechamento ---
        const newFrontmatter = frontmatter.replace(
          '---\n',
          `---\nmodified: ${today}\n`
        );
        return newFrontmatter + body;
      }
    }
  }

  return content;
}

/**
 * Adiciona conteúdo a uma seção específica
 * @param {Object} options - Opções
 * @param {string} options.path - Caminho da nota
 * @param {string} options.heading - Nome do heading
 * @param {string} options.content - Conteúdo a adicionar
 * @param {string} [options.position='end'] - 'start' ou 'end'
 * @returns {Promise<Object>} Resultado
 */
export async function appendToSection(options) {
  const { path, heading, content, position = 'end' } = options;

  return noteUpdate({
    path,
    content,
    operation: 'section',
    targetType: 'heading',
    target: heading,
  });
}

/**
 * Atualiza um campo do frontmatter
 * @param {Object} options - Opções
 * @param {string} options.path - Caminho da nota
 * @param {string} options.field - Nome do campo
 * @param {any} options.value - Novo valor
 * @returns {Promise<Object>} Resultado
 */
export async function updateFrontmatterField(options) {
  const { path, field, value } = options;

  return noteUpdate({
    path,
    content: String(value),
    operation: 'section',
    targetType: 'frontmatter',
    target: field,
  });
}

/**
 * Verifica se uma nota existe
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

// Exporta também como default
export default noteUpdate;
