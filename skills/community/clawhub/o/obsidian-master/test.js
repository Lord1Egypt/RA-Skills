/**
 * Test Suite - Obsidian Master Skill
 * Roda testes básicos em todas as tools
 *
 * Uso: node test.js
 */

import { noteCreate } from './tools/note-create.js';
import { noteRead } from './tools/note-read.js';
import { noteUpdate } from './tools/note-update.js';
import { noteDelete } from './tools/note-delete.js';
import { folderCreate } from './tools/folder-create.js';
import { folderList } from './tools/folder-list.js';
import { vaultStats } from './tools/vault-stats.js';
import { vaultHealth } from './tools/vault-health.js';

// Configuração de teste
const TEST_VAULT = process.env.OBSIDIAN_VAULT || '';
const TEST_TIMEOUT = 30000;

// Cores para output
const colors = {
  reset: '\x1b[0m',
  green: '\x1b[32m',
  red: '\x1b[31m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
};

// Logger
function log(message, color = 'reset') {
  console.log(`${colors[color]}${message}${colors.reset}`);
}

// Resultados
const results = {
  passed: 0,
  failed: 0,
  errors: [],
};

/**
 * Executa um teste
 * @param {string} name - Nome do teste
 * @param {Function} fn - Função de teste
 */
async function test(name, fn) {
  try {
    log(`\n🧪 Testando: ${name}`, 'blue');
    await fn();
    log(`✅ PASSOU: ${name}`, 'green');
    results.passed++;
  } catch (error) {
    log(`❌ FALHOU: ${name}`, 'red');
    log(`   Erro: ${error.message}`, 'red');
    results.failed++;
    results.errors.push({ name, error: error.message });
  }
}

/**
 * Verifica se API está configurada
 */
async function checkApiConfig() {
  if (!process.env.OBSIDIAN_API_KEY) {
    throw new Error('OBSIDIAN_API_KEY não configurada. Configure as variáveis de ambiente antes de executar os testes.');
  }
}

/**
 * Testes principais
 */
async function runTests() {
  log('\n═══════════════════════════════════════════', 'blue');
  log('   OBSIDIAN MASTER - TEST SUITE v1.0', 'blue');
  log('═══════════════════════════════════════════\n', 'blue');

  // Verifica configuração
  await test('Configuração da API', async () => {
    await checkApiConfig();
    log('   API Key configurada', 'green');
  });

  // Testes de Vault Intelligence
  await test('vault-stats', async () => {
    const result = await vaultStats({ includeContent: false });
    if (!result.success) throw new Error(result.message);
    log(`   Total de notas: ${result.data?.overview?.totalNotes || 'N/A'}`, 'yellow');
  });

  await test('vault-health', async () => {
    const result = await vaultHealth({ fullScan: false });
    if (!result.success) throw new Error(result.message);
    log(`   Score de saúde: ${result.data?.scores?.overall || 'N/A'}/100`, 'yellow');
  });

  // Testes de Pasta
  await test('folder-create', async () => {
    const result = await folderCreate({
      path: '99 - Templates/__test_folder',
      createReadme: false,
    });
    // Pode já existir
    log(`   ${result.message}`, 'yellow');
  });

  await test('folder-list', async () => {
    const result = await folderList({ path: '', recursive: false });
    if (!result.success) throw new Error(result.message);
    log(`   Pastas encontradas: ${result.data?.folders?.length || 0}`, 'yellow');
  });

  // Testes de Nota
  const testNotePath = '99 - Templates/__test_note.md';

  await test('note-create', async () => {
    const result = await noteCreate({
      title: '__test_note',
      content: 'Esta é uma nota de teste gerada automaticamente.',
      folder: '99 - Templates',
      type: 'note',
      tags: ['test'],
    });
    if (!result.success) throw new Error(result.message);
    log(`   Criada: ${result.data?.path}`, 'yellow');
  });

  await test('note-read', async () => {
    const result = await noteRead({ path: testNotePath, format: 'parsed' });
    if (!result.success) throw new Error(result.message);
    log(`   Lida: ${result.data?.wordCount || 0} palavras`, 'yellow');
  });

  await test('note-update', async () => {
    const result = await noteUpdate({
      path: testNotePath,
      content: '\nTexto adicionado em teste.',
      operation: 'append',
    });
    if (!result.success) throw new Error(result.message);
    log(`   Atualizada: ${result.data?.operation}`, 'yellow');
  });

  await test('note-delete (backup)', async () => {
    const result = await noteDelete({
      path: testNotePath,
      confirm: false,
      backup: true,
    });
    // Note: This will actually move to archive, not delete
    log(`   ${result.message}`, 'yellow');
  });

  // Resumo
  log('\n═══════════════════════════════════════════', 'blue');
  log('   RESULTADOS DOS TESTES', 'blue');
  log('═══════════════════════════════════════════\n', 'blue');

  log(`✅ Passaram: ${results.passed}`, 'green');
  log(`❌ Falharam: ${results.failed}`, results.failed > 0 ? 'red' : 'green');

  if (results.errors.length > 0) {
    log('\nDetalhes dos erros:', 'red');
    results.errors.forEach((e, i) => {
      log(`  ${i + 1}. ${e.name}: ${e.error}`, 'red');
    });
  }

  log('\n═══════════════════════════════════════════\n', 'blue');

  // Exit code
  process.exit(results.failed > 0 ? 1 : 0);
}

// Executa testes
runTests().catch((error) => {
  log(`\n❌ Erro fatal: ${error.message}`, 'red');
  process.exit(1);
});
