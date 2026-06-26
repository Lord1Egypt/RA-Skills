import { renderToString } from '@antv/infographic/ssr';
import fs from 'fs';

const filePath = process.argv[2] || 'input.ifgc';
const outputPath = process.argv[3] || filePath.replace('.ifgc', '.svg');

const content = fs.readFileSync(filePath, 'utf-8');
const svg = await renderToString(content);

fs.writeFileSync(outputPath, svg);
console.log(`Saved to ${outputPath}`);
