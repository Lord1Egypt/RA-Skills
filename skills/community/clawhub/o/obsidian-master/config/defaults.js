/**
 * Configurações padrão da Obsidian Master Skill
 * Todas as configurações podem ser sobrescritas via variáveis de ambiente
 * @module config/defaults
 */

/**
 * Configurações principais da API REST do Obsidian
 * @typedef {Object} ObsidianConfig
 * @property {string} baseUrl - URL base da API (padrão: https://127.0.0.1:27124)
 * @property {string} apiKey - Chave da API para autenticação Bearer
 * @property {string} vaultPath - Caminho absoluto do vault no sistema de arquivos
 * @property {string} certPath - Caminho do certificado para HTTPS
 */
export const CONFIG = {
  // API REST Local do Obsidian
  baseUrl: process.env.OBSIDIAN_URL || 'https://127.0.0.1:27124',
  apiKey: process.env.OBSIDIAN_API_KEY || '',
  vaultPath: process.env.OBSIDIAN_VAULT || '',
  certPath: process.env.OBSIDIAN_CERT_PATH || '',

  // Pastas padrão do sistema PARA + Zettelkasten
  folders: {
    inbox: process.env.OBSIDIAN_INBOX || '00 - Inbox',
    projects: process.env.OBSIDIAN_PROJECTS || '10 - Projetos',
    areas: process.env.OBSIDIAN_AREAS || '20 - Áreas',
    resources: process.env.OBSIDIAN_RESOURCES || '30 - Recursos',
    archive: process.env.OBSIDIAN_ARCHIVE || '40 - Arquivo',
    daily: process.env.OBSIDIAN_DAILY || '50 - Daily Notes',
    canvas: process.env.OBSIDIAN_CANVAS || '60 - Canvas',
    zettelkasten: process.env.OBSIDIAN_ZETTEL || '70 - Zettelkasten',
    mocs: process.env.OBSIDIAN_MOCS || '80 - MOCs',
    templates: process.env.OBSIDIAN_TEMPLATES || '99 - Templates',
  },

  // Formato de datas
  dateFormat: process.env.OBSIDIAN_DATE_FORMAT || 'YYYY-MM-DD',
  dateTimeFormat: process.env.OBSIDIAN_DATETIME_FORMAT || 'YYYY-MM-DD HH:mm',
  zettelIdFormat: 'YYYYMMDDHHmm',

  // Configurações regionais
  language: process.env.OBSIDIAN_LANGUAGE || 'pt-BR',
  timezone: process.env.OBSIDIAN_TIMEZONE || 'America/Sao_Paulo',

  // Comportamentos
  autoCreateFolders: true,
  backupBeforeDelete: true,
  confirmDestructive: true,
  defaultNoteExtension: '.md',
};

/**
 * Mapeamento de tipos de nota para pastas
 * @type {Object<string, string>}
 */
export const NOTE_TYPE_TO_FOLDER = {
  note: CONFIG.folders.inbox,
  project: CONFIG.folders.projects,
  area: CONFIG.folders.areas,
  resource: CONFIG.folders.resources,
  archive: CONFIG.folders.archive,
  daily: CONFIG.folders.daily,
  canvas: CONFIG.folders.canvas,
  zettel: CONFIG.folders.zettelkasten,
  moc: CONFIG.folders.mocs,
  template: CONFIG.folders.templates,
};

/**
 * Status válidos para notas
 * @type {Array<string>}
 */
export const NOTE_STATUS = ['active', 'archived', 'draft', 'completed'];

/**
 * Tipos válidos de notas
 * @type {Array<string>}
 */
export const NOTE_TYPES = ['note', 'project', 'area', 'resource', 'archive', 'daily', 'canvas', 'zettel', 'moc', 'template'];

/**
 * Headers padrão para requisições à API
 * @returns {Object} Headers HTTP configurados
 */
export function getDefaultHeaders() {
  const headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  };

  if (CONFIG.apiKey) {
    headers['Authorization'] = `Bearer ${CONFIG.apiKey}`;
  }

  return headers;
}

/**
 * Headers para operações específicas
 * @param {string} operation - Tipo de operação (append, prepend, replace)
 * @param {string} targetType - Tipo de alvo (heading, block, frontmatter)
 * @param {string} target - Alvo específico
 * @returns {Object} Headers configurados para PATCH
 */
export function getPatchHeaders(operation, targetType, target) {
  return {
    ...getDefaultHeaders(),
    'Operation': operation,
    'Target-Type': targetType,
    'Target': target,
  };
}

/**
 * Headers para queries Dataview
 * @returns {Object} Headers para DQL
 */
export function getDataviewHeaders() {
  return {
    ...getDefaultHeaders(),
    'Content-Type': 'application/vnd.olrapi.dataview.dql+txt',
  };
}

/**
 * Valida se a configuração essencial está presente
 * @throws {Error} Se configurações obrigatórias estiverem faltando
 */
export function validateConfig() {
  const required = ['baseUrl'];
  const missing = required.filter(key => !CONFIG[key]);

  if (missing.length > 0) {
    throw new Error(`Configurações obrigatórias faltando: ${missing.join(', ')}`);
  }

  if (!CONFIG.apiKey) {
    console.warn('⚠️ OBSIDIAN_API_KEY não configurada. Algumas operações podem falhar.');
  }
}

/**
 * Constrói URL completa para um endpoint
 * @param {string} path - Caminho do endpoint
 * @returns {string} URL completa
 */
export function buildUrl(path) {
  const base = CONFIG.baseUrl.replace(/\/$/, '');
  const cleanPath = path.startsWith('/') ? path : `/${path}`;
  return `${base}${cleanPath}`;
}

/**
 * Formata data para ID Zettelkasten
 * @param {Date} [date] - Data a formatar (padrão: agora)
 * @returns {string} ID no formato YYYYMMDDHHmm
 */
export function formatZettelId(date = new Date()) {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  const hours = String(date.getHours()).padStart(2, '0');
  const minutes = String(date.getMinutes()).padStart(2, '0');
  return `${year}${month}${day}${hours}${minutes}`;
}

/**
 * Formata data para nome de daily note
 * @param {Date} [date] - Data a formatar (padrão: agora)
 * @returns {string} Data no formato YYYY-MM-DD
 */
export function formatDailyDate(date = new Date()) {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}

/**
 * Extrai nome do arquivo de um caminho
 * @param {string} path - Caminho completo
 * @returns {string} Nome do arquivo sem extensão
 */
export function getNoteName(path) {
  return path.split('/').pop().replace(/\.md$/, '');
}

/**
 * Normaliza caminho de nota
 * @param {string} path - Caminho original
 * @returns {string} Caminho normalizado
 */
export function normalizePath(path) {
  // Remove leading slash
  let normalized = path.replace(/^\//, '');
  // Remove trailing slash
  normalized = normalized.replace(/\/$/, '');
  // Garante extensão .md
  if (!normalized.endsWith('.md')) {
    normalized += '.md';
  }
  return normalized;
}

/**
 * Gera resposta padronizada de sucesso
 * @param {string} message - Mensagem de sucesso
 * @param {Object} data - Dados adicionais
 * @param {string} emoji - Emoji da operação
 * @returns {Object} Resposta formatada
 */
export function successResponse(message, data = {}, emoji = '✅') {
  return {
    success: true,
    message,
    data,
    emoji,
    timestamp: new Date().toISOString(),
  };
}

/**
 * Gera resposta padronizada de erro
 * @param {string} message - Mensagem de erro
 * @param {Error|Object} error - Objeto de erro
 * @param {string} emoji - Emoji do erro
 * @returns {Object} Resposta formatada
 */
export function errorResponse(message, error = null, emoji = '❌') {
  const response = {
    success: false,
    message,
    emoji,
    timestamp: new Date().toISOString(),
  };

  if (error) {
    response.error = {
      code: error.code || 'UNKNOWN',
      details: error.message || error.toString(),
      stack: error.stack,
    };
  }

  return response;
}

/**
 * Gera resposta padronizada com aviso
 * @param {string} message - Mensagem principal
 * @param {string} warning - Mensagem de aviso
 * @param {Object} data - Dados adicionais
 * @param {string} emoji - Emoji
 * @returns {Object} Resposta formatada
 */
export function warningResponse(message, warning, data = {}, emoji = '⚠️') {
  return {
    success: true,
    message,
    warning,
    data,
    emoji,
    timestamp: new Date().toISOString(),
  };
}
