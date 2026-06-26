import { fileURLToPath } from 'node:url';
import { dirname } from 'node:path';
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
import fs from 'node:fs';
import path from 'node:path';
import ts from 'typescript';

const ROOT = path.join(__dirname, '..');
const SUPPORTED_EXTENSIONS = ['.ts', '.tsx', '.mts', '.cts', '.js', '.jsx', '.mjs', '.cjs'] as const;

export function collectLintTargets(baseDir: string): string[] {
  return collectFiles(baseDir).filter((file) => {
    const ext = path.extname(file);
    if (!SUPPORTED_EXTENSIONS.includes(ext as (typeof SUPPORTED_EXTENSIONS)[number])) return false;
    if (file.endsWith('.d.ts') || file.endsWith('.d.mts') || file.endsWith('.d.cts')) return false;
    return true;
  });
}

export function lintFiles(files: string[]): void {
  const failures: string[] = [];

  for (const file of files) {
    const sourceText = fs.readFileSync(file, 'utf8');
    const sourceFile = ts.createSourceFile(
      file,
      sourceText,
      ts.ScriptTarget.Latest,
      true,
      scriptKindFromFile(file),
    );

    if (sourceFile.parseDiagnostics.length === 0) continue;

    for (const diagnostic of sourceFile.parseDiagnostics) {
      const rendered = ts.flattenDiagnosticMessageText(diagnostic.messageText, '\n');
      const pos = diagnostic.start != null ? sourceFile.getLineAndCharacterOfPosition(diagnostic.start) : null;
      failures.push(
        `${file}${pos ? `:${pos.line + 1}:${pos.character + 1}` : ''} ${rendered}`,
      );
    }
  }

  if (failures.length > 0) {
    throw new Error(`Syntax lint failed:\n${failures.join('\n')}`);
  }
}

function scriptKindFromFile(filePath: string): ts.ScriptKind {
  const ext = path.extname(filePath);
  switch (ext) {
    case '.js':
      return ts.ScriptKind.JS;
    case '.jsx':
      return ts.ScriptKind.JSX;
    case '.ts':
      return ts.ScriptKind.TS;
    case '.tsx':
      return ts.ScriptKind.TSX;
    case '.mjs':
      return ts.ScriptKind.JS;
    case '.cjs':
      return ts.ScriptKind.JS;
    case '.mts':
      return ts.ScriptKind.TS;
    case '.cts':
      return ts.ScriptKind.TS;
    default:
      return ts.ScriptKind.Unknown;
  }
}

function collectFiles(dir: string): string[] {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  const files: string[] = [];

  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      files.push(...collectFiles(fullPath));
      continue;
    }
    files.push(fullPath);
  }

  return files;
}

function runCli(): void {
  const targets = ['src', 'scripts', 'tests']
    .map((dir) => path.join(ROOT, dir))
    .flatMap((dir) => collectLintTargets(dir));

  lintFiles(targets);
  console.log(`✅ Syntax lint passed (${targets.length} TS/JS files)`);
}

if (process.argv[1] && path.resolve(process.argv[1]) === path.resolve(__filename)) {
  runCli();
}
