/**
 * @module tools/folder-create
 * @description Cria pastas recursivamente no vault
 */

import { CONFIG, getDefaultHeaders, buildUrl, successResponse, errorResponse } from '../config/defaults.js';

/**
 * Cria uma nova pasta no vault
 * @param {Object} options - Opções de criação
 * @param {string} options.path - Caminho da pasta (ex: "Projetos/Novo Projeto")
 * @param {boolean} [options.recursive=true] - Criar pastas pai se não existirem
 * @param {boolean} [options.createReadme=true] - Criar arquivo README.md na pasta
 * @returns {Promise<Object>} Resultado da operação
 */
export async function folderCreate(options) {
  try {
    const {
      path,
      recursive = true,
      createReadme = true,
    } = options;

    // Validações
    if (!path) {
      return errorResponse('Caminho da pasta é obrigatório');
    }

    if (!CONFIG.apiKey) {
      return errorResponse('OBSIDIAN_API_KEY não configurada');
    }

    // Normaliza o caminho
    const normalizedPath = path.replace(/^\//, '').replace(/\/$/, '');

    // Verifica se já existe
    const existsCheck = await checkFolderExists(normalizedPath);
    if (existsCheck.exists) {
      return errorResponse(`Pasta já existe: ${normalizedPath}`);
    }

    // Cria um arquivo placeholder para garantir que a pasta exista
    // A API REST cria pastas automaticamente ao criar arquivos
    const placeholderPath = `${normalizedPath}/.folder`;

    const response = await fetch(buildUrl(`/vault/${placeholderPath}`), {
      method: 'PUT',
      headers: getDefaultHeaders(),
      body: '# Pasta criada automaticamente\n',
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Erro ${response.status}: ${errorText}`);
    }

    // Cria README.md se solicitado
    if (createReadme) {
      await createReadmeFile(normalizedPath);
    }

    return successResponse(
      `📁 Pasta '${normalizedPath}' criada`,
      {
        path: normalizedPath,
        recursive,
        readmeCreated: createReadme,
      },
      '✅'
    );

  } catch (error) {
    return errorResponse(`Falha ao criar pasta: ${error.message}`, error);
  }
}

/**
 * Cria arquivo README.md em uma pasta
 * @param {string} folderPath - Caminho da pasta
 */
async function createReadmeFile(folderPath) {
  try {
    const folderName = folderPath.split('/').pop();
    const readmeContent = `# ${folderName}

Pasta criada em: ${new Date().toLocaleDateString('pt-BR')}

## Conteúdo

<!-- Lista de notas nesta pasta -->

`;

    await fetch(buildUrl(`/vault/${folderPath}/README.md`), {
      method: 'PUT',
      headers: getDefaultHeaders(),
      body: readmeContent,
    });
  } catch (error) {
    console.warn('Não foi possível criar README:', error.message);
  }
}

/**
 * Verifica se uma pasta existe
 * @param {string} path - Caminho da pasta
 * @returns {Promise<Object>} { exists: boolean }
 */
async function checkFolderExists(path) {
  try {
    // Tenta listar o conteúdo da pasta
    const response = await fetch(buildUrl(`/vault/${path}/`), {
      method: 'GET',
      headers: getDefaultHeaders(),
    });
    return { exists: response.ok };
  } catch {
    return { exists: false };
  }
}

// Exporta também como default
export default folderCreate;
