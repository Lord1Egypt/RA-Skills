/**
 * Asset Loader — Loads PNG sprite sheets from the source repo and converts
 * to pixel array format (string[][]) for the game engine.
 *
 * Ported from the original VS Code extension's assetLoader.ts, adapted for
 * standalone operation with pngjs.
 */

import * as fs from 'fs';
import * as path from 'path';
import { fileURLToPath } from 'url';
import { PNG } from 'pngjs';

// Constants matching the original extension
const PNG_ALPHA_THRESHOLD = 128;
const CHAR_COUNT = 6;
const CHAR_FRAME_W = 16;
const CHAR_FRAME_H = 32;
const CHAR_FRAMES_PER_ROW = 7;
const CHARACTER_DIRECTIONS = ['down', 'up', 'right'] as const;
const WALL_PIECE_WIDTH = 16;
const WALL_PIECE_HEIGHT = 32;
const WALL_GRID_COLS = 4;
const WALL_BITMASK_COUNT = 16;
const FLOOR_PATTERN_COUNT = 7;
const FLOOR_TILE_SIZE = 16;

/**
 * Path to bundled sprite assets.
 * Assets ship with the project in public/assets/ — no external dependencies.
 * PIXEL_AGENTS_ROOT env var is set by the CLI entry point; falls back to
 * __dirname (server/) going up one level.
 */
const __dirname = path.dirname(fileURLToPath(import.meta.url));
const PROJECT_ROOT = process.env.PIXEL_AGENTS_ROOT || path.resolve(__dirname, '..');
const ASSETS_DIR = path.resolve(PROJECT_ROOT, 'public', 'assets');

export interface CharacterDirectionSprites {
  down: string[][][];
  up: string[][][];
  right: string[][][];
}

/** Convert a pixel's RGBA to hex string, or '' for transparent */
function pixelToHex(data: Uint8Array, idx: number): string {
  const r = data[idx];
  const g = data[idx + 1];
  const b = data[idx + 2];
  const a = data[idx + 3];
  if (a < PNG_ALPHA_THRESHOLD) return '';
  return `#${r.toString(16).padStart(2, '0')}${g.toString(16).padStart(2, '0')}${b.toString(16).padStart(2, '0')}`.toUpperCase();
}

/**
 * Load all 6 character sprite sheets.
 * Each PNG is 112×96 (7 frames × 3 direction rows, 16×32 per frame).
 */
export function loadCharacterSprites(): CharacterDirectionSprites[] | null {
  try {
    const charDir = path.join(ASSETS_DIR, 'characters');
    const characters: CharacterDirectionSprites[] = [];

    for (let ci = 0; ci < CHAR_COUNT; ci++) {
      const filePath = path.join(charDir, `char_${ci}.png`);
      if (!fs.existsSync(filePath)) {
        console.log(`[AssetLoader] Character sprite not found: ${filePath}`);
        return null;
      }

      const png = PNG.sync.read(fs.readFileSync(filePath));
      const charData: CharacterDirectionSprites = { down: [], up: [], right: [] };

      for (let dirIdx = 0; dirIdx < CHARACTER_DIRECTIONS.length; dirIdx++) {
        const dir = CHARACTER_DIRECTIONS[dirIdx];
        const rowOffsetY = dirIdx * CHAR_FRAME_H;
        const frames: string[][][] = [];

        for (let f = 0; f < CHAR_FRAMES_PER_ROW; f++) {
          const sprite: string[][] = [];
          const frameOffsetX = f * CHAR_FRAME_W;
          for (let y = 0; y < CHAR_FRAME_H; y++) {
            const row: string[] = [];
            for (let x = 0; x < CHAR_FRAME_W; x++) {
              const idx = ((rowOffsetY + y) * png.width + (frameOffsetX + x)) * 4;
              row.push(pixelToHex(png.data as unknown as Uint8Array, idx));
            }
            sprite.push(row);
          }
          frames.push(sprite);
        }
        charData[dir] = frames;
      }
      characters.push(charData);
    }

    console.log(`[AssetLoader] ✅ Loaded ${characters.length} character sprites`);
    return characters;
  } catch (err) {
    console.error(`[AssetLoader] ❌ Error loading characters: ${err}`);
    return null;
  }
}

/**
 * Load wall tiles from walls.png (64×128, 4×4 grid of 16×32 pieces).
 * Returns 16 sprites indexed by bitmask.
 */
export function loadWallSprites(): string[][][] | null {
  try {
    const wallPath = path.join(ASSETS_DIR, 'walls.png');
    if (!fs.existsSync(wallPath)) {
      console.log(`[AssetLoader] walls.png not found at: ${wallPath}`);
      return null;
    }

    const png = PNG.sync.read(fs.readFileSync(wallPath));
    const sprites: string[][][] = [];

    for (let mask = 0; mask < WALL_BITMASK_COUNT; mask++) {
      const ox = (mask % WALL_GRID_COLS) * WALL_PIECE_WIDTH;
      const oy = Math.floor(mask / WALL_GRID_COLS) * WALL_PIECE_HEIGHT;
      const sprite: string[][] = [];
      for (let r = 0; r < WALL_PIECE_HEIGHT; r++) {
        const row: string[] = [];
        for (let c = 0; c < WALL_PIECE_WIDTH; c++) {
          const idx = ((oy + r) * png.width + (ox + c)) * 4;
          row.push(pixelToHex(png.data as unknown as Uint8Array, idx));
        }
        sprite.push(row);
      }
      sprites.push(sprite);
    }

    console.log(`[AssetLoader] ✅ Loaded ${sprites.length} wall tile pieces`);
    return sprites;
  } catch (err) {
    console.error(`[AssetLoader] ❌ Error loading wall tiles: ${err}`);
    return null;
  }
}

/**
 * Load floor tiles from floors.png (horizontal strip of 7 tiles, 16px each).
 * Returns 7 sprites, each 16×16.
 */
export function loadFloorSprites(): string[][][] | null {
  try {
    const floorPath = path.join(ASSETS_DIR, 'floors.png');
    if (!fs.existsSync(floorPath)) {
      console.log(`[AssetLoader] floors.png not found — using fallback`);
      return null;
    }

    const png = PNG.sync.read(fs.readFileSync(floorPath));
    const sprites: string[][][] = [];

    for (let t = 0; t < FLOOR_PATTERN_COUNT; t++) {
      const sprite: string[][] = [];
      for (let y = 0; y < FLOOR_TILE_SIZE; y++) {
        const row: string[] = [];
        for (let x = 0; x < FLOOR_TILE_SIZE; x++) {
          const px = t * FLOOR_TILE_SIZE + x;
          const idx = (y * png.width + px) * 4;
          row.push(pixelToHex(png.data as unknown as Uint8Array, idx));
        }
        sprite.push(row);
      }
      sprites.push(sprite);
    }

    console.log(`[AssetLoader] ✅ Loaded ${sprites.length} floor tile patterns`);
    return sprites;
  } catch (err) {
    console.error(`[AssetLoader] ❌ Error loading floor tiles: ${err}`);
    return null;
  }
}

/** Load all sprites and return a combined payload for the WebSocket init message */
export function loadAllSprites(): {
  characters: CharacterDirectionSprites[] | null;
  wallSprites: string[][][] | null;
  floorSprites: string[][][] | null;
} {
  console.log('[AssetLoader] Loading sprites from:', ASSETS_DIR);
  return {
    characters: loadCharacterSprites(),
    wallSprites: loadWallSprites(),
    floorSprites: loadFloorSprites(),
  };
}
