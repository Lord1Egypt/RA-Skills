#!/usr/bin/env node
/**
 * OpenClaw Spirits — Sprite rendering
 * Reads sprites.json and renders with eyes + accessories
 */

const fs = require('fs');
const path = require('path');

const spritesPath = path.join(__dirname, '../assets/sprites.json');
const sprites = JSON.parse(fs.readFileSync(spritesPath, 'utf8'));

// Accessory lines (placed on line 0 if blank)
const ACCESSORY_LINES = {
  none: '',
  bell: '    🔔      ',
  halo: '   (   )    ',
  starmark: '    ✦       ',
  thundermark: '    ⚡      ',
  scroll: '   [===]    ',
  crownfire: '   \\🔥/     '
};

/**
 * Render a spirit sprite
 * @param {object} bones - {species, eye, accessory, ...}
 * @param {number} frame - frame index (0-2)
 * @returns {string[]} - array of lines
 */
function renderSprite(bones, frame = 0) {
  const frames = sprites[bones.species];
  if (!frames) {
    throw new Error(`Unknown species: ${bones.species}`);
  }

  const body = frames[frame % frames.length];
  const lines = body.map(line => line.replace(/{E}/g, bones.eye));

  // Apply accessory if line 0 is blank
  if (bones.accessory && bones.accessory !== 'none' && !lines[0].trim()) {
    lines[0] = ACCESSORY_LINES[bones.accessory] || '';
  }

  // Drop blank line 0 if all frames have it blank (to save vertical space)
  if (!lines[0].trim() && frames.every(f => !f[0].trim())) {
    lines.shift();
  }

  return lines;
}

/**
 * Render a simplified face emoji for the spirit
 * @param {object} bones - {species, eye, ...}
 * @returns {string} - face string
 */
function renderFace(bones) {
  const e = bones.eye;
  const species = bones.species;

  // Custom faces per species
  const faces = {
    mosscat: `(${e}ω${e})`,
    inkoi: `~(${e})~`,
    embermoth: `*(${e}${e})*`,
    frostpaw: `(${e}..${e})`,
    bellhop: `(${e}o${e})`,
    astortoise: `[${e}_${e}]`,
    foldwing: `/${e}v${e}\\`,
    cogmouse: `(${e}·${e})`,
    umbracrow: `:(${e}${e}):`,
    crackviper: `/${e}\\`,
    glowshroom: `|${e}_${e}|`,
    bubbloom: `(${e}~${e})`,
    inkling: `(${e}~${e})`,
    rustbell: `/~${e}~\\`,
    mossrock: `[${e}${e}]`,
    frostfang: `<${e}_${e}>`,
    loopwyrm: `(${e}~${e})`,
    bubbell: `(${e}<>${e})`,
    cogbeast: `[${e}=${e}]`,
    umbra: `:${e}:`,
    stardust: `✦${e}✦`,
    crackle: `/${e}\\`,
    wickling: `|${e}|`,
    echochord: `|${e}_${e}|`
  };

  return faces[species] || `(${e}${e})`;
}

// === CLI ===
if (require.main === module) {
  const args = process.argv.slice(2);
  if (args.length === 0) {
    console.error('Usage: node render.js \'<bones-json>\' [frame]');
    console.error('Example: node render.js \'{"species":"mosscat","eye":"◦","accessory":"halo"}\' 0');
    process.exit(1);
  }

  const bones = JSON.parse(args[0]);
  const frame = args[1] ? parseInt(args[1]) : 0;

  const lines = renderSprite(bones, frame);
  console.log(lines.join('\n'));
}

module.exports = { renderSprite, renderFace };
