import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

export const SKILL_ID = 'insentek-openapi';
export const PACKAGE_NAME = '@insentek/openapi-skill';
export const CLI_NAME = 'insentek-api-skill';

export const PACKAGE_ROOT = path.resolve(__dirname, '..');
export const ASSETS_DIR = path.join(PACKAGE_ROOT, 'assets');

export const ASSET_ENTRIES = [
  'skill.json',
  'SKILL.md',
  'docs',
  'reference',
  'examples',
  'scripts',
];
