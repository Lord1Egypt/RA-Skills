/**
 * @module tools/daily-open
 * @description Abre ou cria a daily note de hoje
 */

import { CONFIG, getDefaultHeaders, buildUrl, normalizePath, successResponse, errorResponse, formatDailyDate } from '../config/defaults.js';

/**
 * Abre ou cria a daily note de hoje
 * @param {Object} options - Opções
 * @param {boolean} [options.create=true] - Criar se não existir
 * @param {boolean} [options.open=true] - Abrir no Obsidian
 * @param {string} [options.date] - Data específica (YYYY-MM-DD), padrão: hoje
 * @returns {Promise<Object>} Daily note
 */
export async function dailyOpen(options = {}) {
  try {
    const {
      create = true,
      open = true,
      date = formatDailyDate(new Date()),
    } = options;

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

    let wasCreated = false;

    if (!checkResponse.ok && create) {
      // Cria daily note
      wasCreated = true;

      const content = generateDailyTemplate(date);

      await fetch(buildUrl(`/vault/${filePath}`), {
        method: 'PUT',
        headers: getDefaultHeaders(),
        body: content,
      });
    } else if (!checkResponse.ok && !create) {
      return errorResponse(`Daily note não existe: ${fileName}`);
    }

    // Abre se solicitado
    if (open) {
      await fetch(buildUrl(`/open/${filePath}`), {
        method: 'POST',
        headers: getDefaultHeaders(),
      });
    }

    return successResponse(
      wasCreated ? `📅 Daily de ${date} criada` : `📅 Daily de ${date} aberta`,
      {
        path: filePath,
        date,
        wasCreated,
        opened: open,
      },
      '📅'
    );

  } catch (error) {
    return errorResponse(`Falha ao abrir daily: ${error.message}`, error);
  }
}

/**
 * Gera template para daily note
 * @param {string} date - Data
 * @returns {string} Conteúdo
 */
function generateDailyTemplate(date) {
  const now = new Date();
  const formattedDate = now.toLocaleDateString('pt-BR', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });

  return `---
title: "${date}"
created: ${date}
type: daily
tags: [daily]
---

# ${formattedDate}

## 🌅 Intenção do Dia

## ✅ Tasks

## 📝 Notas Rápidas

## 🌙 Review
- O que foi feito:
- Aprendizados:
- Amanhã:
`;
}

// Exporta também como default
export default dailyOpen;
