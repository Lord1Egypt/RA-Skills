/"
 * @module tools/daily-append
 * @description Adiciona entrada na daily note
 */

import { CONFIG, getDefaultHeaders, buildUrl, successResponse, errorResponse, formatDailyDate } from '../config/defaults.js';

/**
 * Adiciona conteúdo à daily note
 * @param {Object} options - Opções
 * @param {string} options.content - Conteúdo a adicionar
 * @param {string} [options.section] - Seção específica (ex: 'Notas Rápidas')
 * @param {string} [options.date] - Data (padrão: hoje)
 * @param {boolean} [options.createIfMissing=true] - Criar daily se não existir
 * @param {boolean} [options.addTimestamp=true] - Adicionar timestamp
 * @returns {Promise<Object>} Resultado
 */
export async function dailyAppend(options) {
  try {
    const {
      content,
      section,
      date = formatDailyDate(new Date()),
      createIfMissing = true,
      addTimestamp = true,
    } = options;

    if (!content) {
      return errorResponse('Conteúdo é obrigatório');
    }

    if (!CONFIG.apiKey) {
      return errorResponse('OBSIDIAN_API_KEY não configurada');
    }

    const dailyFolder = CONFIG.folders.daily;
    const fileName = `${date}.md`;
    const filePath = `${dailyFolder}/${fileName}`;

    // Verifica se existe
    const checkResponse = await fetch(buildUrl(`/vault/${filePath}`), {
      method: 'HEAD',
      headers: getDefaultHeaders(),
    });

    let currentContent = '';

    if (!checkResponse.ok) {
      if (!createIfMissing) {
        return errorResponse(`Daily note não existe: ${fileName}`);
      }
      // Cria básica
      currentContent = `---\ntitle: "${date}"\ncreated: ${date}\ntype: daily\ntags: [daily]\n---\n\n# ${date}\n`;
    } else {
      // Lê conteúdo
      const readResponse = await fetch(buildUrl(`/vault/${filePath}`), {
        method: 'GET',
        headers: getDefaultHeaders(),
      });
      currentContent = await readResponse.text();
    }

    // Prepara novo conteúdo
    const now = new Date().toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' });
    const timestamp = addTimestamp ? `**${now}** ` : '';
    const newEntry = `\n${timestamp}${content}`;

    let updatedContent;

    if (section) {
      // Procura a seção
      const sectionRegex = new RegExp(`^(## ${section}.*)$`, 'm');
      if (sectionRegex.test(currentContent)) {
        // Adiciona após a seção
        updatedContent = currentContent.replace(
          sectionRegex,
          `$1\n${newEntry}`
        );
      } else {
        // Seção não existe, adiciona no final
        updatedContent = currentContent + `\n## ${section}\n${newEntry}`;
      }
    } else {
      // Adiciona no final
      updatedContent = currentContent + newEntry;
    }

    // Salva
    const writeResponse = await fetch(buildUrl(`/vault/${filePath}`), {
      method: 'PUT',
      headers: getDefaultHeaders(),
      body: updatedContent,
    });

    if (!writeResponse.ok) {
      throw new Error('Erro ao salvar');
    }

    return successResponse(
      `📝 Adicionado à daily de ${date}`,
      {
        path: filePath,
        date,
        section,
        contentLength: content.length,
      },
      '✅'
    );

  } catch (error) {
    return errorResponse(`Falha ao adicionar à daily: ${error.message}`, error);
  }
}

// Exporta também como default
export default dailyAppend;
