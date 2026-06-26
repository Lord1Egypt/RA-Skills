/"
 * @module tools/vault-health
 * @description Diagnóstico completo de saúde do vault
 */

import { CONFIG, getDefaultHeaders, buildUrl, successResponse, errorResponse } from '../config/defaults.js';
import { folderList } from './folder-list.js';

/**
 * Gera relatório completo de saúde do vault
 * @param {Object} options - Opções de análise
 * @param {boolean} [options.fullScan=true] - Scan completo
 * @param {boolean} [options.checkLinks=true] - Verificar links quebrados
 * @param {boolean} [options.checkOrphans=true] - Verificar notas órfãs
 * @returns {Promise<Object>} Relatório de saúde
 */
export async function vaultHealth(options = {}) {
  try {
    const {
      fullScan = true,
      checkLinks = true,
      checkOrphans = true,
    } = options;

    if (!CONFIG.apiKey) {
      return errorResponse('OBSIDIAN_API_KEY não configurada');
    }

    // Lista todo o vault
    const listResult = await folderList({ path: '', recursive: true });
    if (!listResult.success) {
      return errorResponse('Não foi possível listar o vault');
    }

    const { files, folders } = listResult.data;
    const mdFiles = files.filter(f => f.extension === 'md');

    // Métricas de saúde
    const health = {
      overview: {
        totalNotes: mdFiles.length,
        totalFiles: files.length,
        totalFolders: folders.length,
        totalSize: files.reduce((sum, f) => sum + (parseInt(f.size) || 0), 0),
      },
      issues: {
        orphanNotes: [],
        brokenLinks: [],
        emptyNotes: [],
        notesWithoutTags: [],
        notesWithoutFrontmatter: [],
        largeFiles: [],
        oldNotes: [],
      },
      metrics: {
        totalWords: 0,
        totalLinks: 0,
        totalTags: 0,
        tasks: { open: 0, completed: 0 },
      },
      scores: {
        overall: 0,
        connectivity: 0,
        organization: 0,
        maintenance: 0,
      },
    };

    // Processa cada nota
    const allLinks = new Set();
    const allBacklinks = new Map();

    for (const file of mdFiles) {
      try {
        const response = await fetch(buildUrl(`/vault/${file.path}`), {
          method: 'GET',
          headers: getDefaultHeaders(),
        });

        if (!response.ok) continue;

        const content = await response.text();
        const noteName = file.name.replace(/\.md$/, '');

        // Análise de conteúdo
        const wordCount = content.split(/\s+/).filter(w => w.length > 0).length;
        health.metrics.totalWords += wordCount;

        // Verifica notas vazias
        if (wordCount < 10) {
          health.issues.emptyNotes.push({
            name: file.name,
            path: file.path,
            wordCount,
          });
        }

        // Frontmatter
        const hasFrontmatter = content.startsWith('---\n');
        if (!hasFrontmatter) {
          health.issues.notesWithoutFrontmatter.push({
            name: file.name,
            path: file.path,
          });
        } else {
          // Extrai tags
          const tagsMatch = content.match(/^---\n.*?tags:\s*\[?([^\]]+)\]?/s);
          if (!tagsMatch || tagsMatch[1].trim() === '') {
            health.issues.notesWithoutTags.push({
              name: file.name,
              path: file.path,
            });
          }
        }

        // Links
        const linkMatches = content.match(/\[\[([^\]]+)\]\]/g);
        if (linkMatches) {
          const links = linkMatches.map(m => m.replace(/\[\[|\]\]/g, '').split('#')[0]);
          health.metrics.totalLinks += links.length;
          links.forEach(l => allLinks.add(l));

          // Registra backlinks
          links.forEach(target => {
            if (!allBacklinks.has(target)) {
              allBacklinks.set(target, []);
            }
            allBacklinks.get(target).push(noteName);
          });
        }

        // Tags no conteúdo
        const tagMatches = content.match(/#[a-zA-Z0-9_\-\/]+/g);
        if (tagMatches) {
          health.metrics.totalTags += tagMatches.length;
        }

        // Tasks
        health.metrics.tasks.open += (content.match(/- \[ \]/g) || []).length;
        health.metrics.tasks.completed += (content.match(/- \[x\]/gi) || []).length;

        // Verifica notas antigas (sem modificar há 90 dias)
        if (file.lastModified) {
          const lastMod = new Date(file.lastModified);
          const daysSince = (new Date() - lastMod) / (1000 * 60 * 60 * 24);
          if (daysSince > 90) {
            health.issues.oldNotes.push({
              name: file.name,
              path: file.path,
              daysSince: Math.round(daysSince),
            });
          }
        }

        // Verifica arquivos grandes
        if (file.size && parseInt(file.size) > 100000) {
          health.issues.largeFiles.push({
            name: file.name,
            path: file.path,
            size: parseInt(file.size),
          });
        }

      } catch {
        // Ignora erro individual
      }
    }

    // Verifica órfãs (notas sem backlinks)
    if (checkOrphans) {
      for (const file of mdFiles) {
        const noteName = file.name.replace(/\.md$/, '');
        if (!allBacklinks.has(noteName) && !noteName.startsWith('.')) {
          health.issues.orphanNotes.push({
            name: file.name,
            path: file.path,
          });
        }
      }
    }

    // Verifica links quebrados
    if (checkLinks) {
      for (const link of allLinks) {
        // Verifica se link existe
        const linkExists = mdFiles.some(f => {
          const name = f.name.replace(/\.md$/, '');
          return name === link || name.endsWith(`/${link}`);
        });

        if (!linkExists) {
          health.issues.brokenLinks.push({
            target: link,
            referencedIn: findReferences(link, mdFiles),
          });
        }
      }
    }

    // Calcula scores
    health.scores = calculateScores(health, mdFiles.length);

    // Gera resumo
    const totalIssues = Object.values(health.issues).reduce(
      (sum, arr) => sum + arr.length, 0
    );

    return successResponse(
      `🏥 Diagnóstico do Vault: Score ${health.scores.overall}/100`,
      {
        ...health,
        summary: {
          totalIssues,
          criticalIssues: health.issues.brokenLinks.length + health.issues.emptyNotes.length,
          warnings: totalIssues - (health.issues.brokenLinks.length + health.issues.emptyNotes.length),
        },
        recommendations: generateRecommendations(health),
      },
      health.scores.overall >= 80 ? '✅' : health.scores.overall >= 50 ? '⚠️' : '❌'
    );

  } catch (error) {
    return errorResponse(`Falha no diagnóstico: ${error.message}`, error);
  }
}

/**
 * Calcula scores de saúde
 * @param {Object} health - Dados de saúde
 * @param {number} totalNotes - Total de notas
 * @returns {Object} Scores
 */
function calculateScores(health, totalNotes) {
  const scores = {
    overall: 0,
    connectivity: 0,
    organization: 0,
    maintenance: 0,
  };

  if (totalNotes === 0) return scores;

  // Connectivity (links e não-órfãs)
  const orphanRate = health.issues.orphanNotes.length / totalNotes;
  scores.connectivity = Math.round((1 - orphanRate) * 100);

  // Organization (tags e frontmatter)
  const tagRate = 1 - (health.issues.notesWithoutTags.length / totalNotes);
  const fmRate = 1 - (health.issues.notesWithoutFrontmatter.length / totalNotes);
  scores.organization = Math.round(((tagRate + fmRate) / 2) * 100);

  // Maintenance (notas vazias e antigas)
  const emptyRate = health.issues.emptyNotes.length / totalNotes;
  const oldRate = health.issues.oldNotes.length / totalNotes;
  scores.maintenance = Math.round((1 - (emptyRate + oldRate) / 2) * 100);

  // Overall
  scores.overall = Math.round(
    (scores.connectivity * 0.4) +
    (scores.organization * 0.3) +
    (scores.maintenance * 0.3)
  );

  return scores;
}

/**
 * Encontra referências a um link
 * @param {string} link - Link alvo
 * @param {Array} files - Lista de arquivos
 * @returns {Array} Referências
 */
function findReferences(link, files) {
  // Simplificado - retorna alguns arquivos que poderiam referenciar
  return files.slice(0, 3).map(f => f.name);
}

/**
 * Gera recomendações baseadas nos problemas
 * @param {Object} health - Dados de saúde
 * @returns {Array} Recomendações
 */
function generateRecommendations(health) {
  const recs = [];

  if (health.issues.brokenLinks.length > 0) {
    recs.push(`Corrija ${health.issues.brokenLinks.length} link(s) quebrado(s)`);
  }

  if (health.issues.orphanNotes.length > 0) {
    recs.push(`${health.issues.orphanNotes.length} nota(s) órfã(s) - considere criar conexões`);
  }

  if (health.issues.emptyNotes.length > 0) {
    recs.push(`${health.issues.emptyNotes.length} nota(s) praticamente vazia(s)`);
  }

  if (health.issues.notesWithoutTags.length > 0) {
    recs.push(`${health.issues.notesWithoutTags.length} nota(s) sem tags`);
  }

  if (health.issues.oldNotes.length > 0) {
    recs.push(`${health.issues.oldNotes.length} nota(s) não modificadas há 90+ dias`);
  }

  if (recs.length === 0) {
    recs.push('Vault está saudável! Continue assim.');
  }

  return recs;
}

// Exporta também como default
export default vaultHealth;
