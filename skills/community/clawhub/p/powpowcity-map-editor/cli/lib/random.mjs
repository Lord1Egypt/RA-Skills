// IsoCity CLI - random terrain generator (value-noise lakes/coast + tree clusters)
import { createTile } from './gamestate.mjs';
import { mulberry32 } from './osm.mjs';

function smoothNoiseField(size, rng, cells) {
  const gw = Math.ceil(size / cells) + 2;
  const g = Array.from({ length: gw }, () => Array.from({ length: gw }, () => rng()));
  const field = Array.from({ length: size }, () => new Array(size).fill(0));
  for (let y = 0; y < size; y++) {
    for (let x = 0; x < size; x++) {
      const gx = x / cells, gy = y / cells;
      const x0 = Math.floor(gx), y0 = Math.floor(gy);
      const fx = gx - x0, fy = gy - y0;
      const sx = fx * fx * (3 - 2 * fx), sy = fy * fy * (3 - 2 * fy);
      const v00 = g[y0][x0], v10 = g[y0][x0 + 1], v01 = g[y0 + 1][x0], v11 = g[y0 + 1][x0 + 1];
      field[y][x] = (v00 * (1 - sx) + v10 * sx) * (1 - sy) + (v01 * (1 - sx) + v11 * sx) * sy;
    }
  }
  return field;
}

export function generateRandomTerrain(gridSize, seed = 42) {
  const rng = mulberry32(seed);
  const coarse = smoothNoiseField(gridSize, rng, Math.max(6, Math.floor(gridSize / 6)));
  const fine = smoothNoiseField(gridSize, rng, Math.max(3, Math.floor(gridSize / 14)));
  const treeField = smoothNoiseField(gridSize, rng, Math.max(4, Math.floor(gridSize / 9)));

  const type = Array.from({ length: gridSize }, () => new Array(gridSize).fill('grass'));

  // Ocean on one random edge, fading inward with noise perturbation
  const edge = Math.floor(rng() * 4);
  const coastDepth = gridSize * (0.12 + rng() * 0.15);
  for (let y = 0; y < gridSize; y++) {
    for (let x = 0; x < gridSize; x++) {
      const n = coarse[y][x] * 0.65 + fine[y][x] * 0.35;
      let distFromEdge;
      if (edge === 0) distFromEdge = y;
      else if (edge === 1) distFromEdge = gridSize - 1 - y;
      else if (edge === 2) distFromEdge = x;
      else distFromEdge = gridSize - 1 - x;
      const coastLine = coastDepth * (0.6 + n * 0.8);
      if (distFromEdge < coastLine) type[y][x] = 'water';
    }
  }

  // Interior lakes from noise threshold (only away from the coast)
  for (let y = 0; y < gridSize; y++) {
    for (let x = 0; x < gridSize; x++) {
      if (type[y][x] !== 'grass') continue;
      const n = coarse[y][x] * 0.6 + fine[y][x] * 0.4;
      if (n > 0.74) type[y][x] = 'water';
    }
  }

  // Tree clusters
  for (let y = 0; y < gridSize; y++) {
    for (let x = 0; x < gridSize; x++) {
      if (type[y][x] !== 'grass') continue;
      if (treeField[y][x] > 0.68 && rng() < 0.55) type[y][x] = 'tree';
      else if (rng() < 0.04) type[y][x] = 'tree';
    }
  }

  // Connected-component labeling for waterBodies
  const waterBodies = [];
  const visited = Array.from({ length: gridSize }, () => new Array(gridSize).fill(false));
  for (let y = 0; y < gridSize; y++) {
    for (let x = 0; x < gridSize; x++) {
      if (type[y][x] !== 'water' || visited[y][x]) continue;
      const cells = [];
      const stack = [[x, y]];
      visited[y][x] = true;
      while (stack.length > 0) {
        const [cx, cy] = stack.pop();
        cells.push([cx, cy]);
        for (const [dx, dy] of [[1, 0], [-1, 0], [0, 1], [0, -1]]) {
          const nx = cx + dx, ny = cy + dy;
          if (nx >= 0 && nx < gridSize && ny >= 0 && ny < gridSize &&
              type[ny][nx] === 'water' && !visited[ny][nx]) {
            visited[ny][nx] = true;
            stack.push([nx, ny]);
          }
        }
      }
      if (cells.length >= 2) {
        waterBodies.push({
          id: `lake-${waterBodies.length + 1}`,
          name: `Lake ${waterBodies.length + 1}`,
          type: 'lake',
          tiles: cells.map(([cx, cy]) => ({ x: cx, y: cy })),
          centerX: Math.round(cells.reduce((s, c) => s + c[0], 0) / cells.length),
          centerY: Math.round(cells.reduce((s, c) => s + c[1], 0) / cells.length),
        });
      }
    }
  }

  const grid = [];
  let waterCells = 0, treeCells = 0;
  for (let y = 0; y < gridSize; y++) {
    const row = [];
    for (let x = 0; x < gridSize; x++) {
      const t = type[y][x];
      if (t === 'water') waterCells++;
      if (t === 'tree') treeCells++;
      row.push(createTile(x, y, t, t === 'water' ? 60 : 50));
    }
    grid.push(row);
  }

  return { grid, waterBodies, stats: { waterCells, treeCells, waterBodyCount: waterBodies.length } };
}
