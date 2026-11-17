import { writeFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

export function createFaviconIco() {
  const size = 32;
  const pixels = Buffer.alloc(size * size * 4);
  for (let y = 0; y < size; y += 1) for (let x = 0; x < size; x += 1) {
    const index = ((size - 1 - y) * size + x) * 4;
    const green = x >= 7 && x <= 11 || x >= 20 && x <= 24 || y >= 13 && y <= 18;
    pixels[index] = green ? 169 : 20;
    pixels[index + 1] = green ? 217 : 24;
    pixels[index + 2] = green ? 119 : 18;
    pixels[index + 3] = 255;
  }
  const bitmap = Buffer.alloc(40 + pixels.length + size * 4);
  bitmap.writeUInt32LE(40, 0);
  bitmap.writeInt32LE(size, 4);
  bitmap.writeInt32LE(size * 2, 8);
  bitmap.writeUInt16LE(1, 12);
  bitmap.writeUInt16LE(32, 14);
  bitmap.writeUInt32LE(pixels.length, 20);
  pixels.copy(bitmap, 40);
  const icon = Buffer.alloc(22 + bitmap.length);
  icon.writeUInt16LE(0, 0);
  icon.writeUInt16LE(1, 2);
  icon.writeUInt16LE(1, 4);
  icon[6] = size;
  icon[7] = size;
  icon.writeUInt16LE(1, 10);
  icon.writeUInt16LE(32, 12);
  icon.writeUInt32LE(bitmap.length, 14);
  icon.writeUInt32LE(22, 18);
  bitmap.copy(icon, 22);
  return icon;
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  const output = path.join(path.dirname(fileURLToPath(import.meta.url)), 'public', 'favicon.ico');
  await writeFile(output, createFaviconIco());
  console.log(`Wrote ${output}`);
}
