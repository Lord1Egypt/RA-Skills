// IsoCity CLI - placement rules, ported from src/lib/simulation.ts
// (placeBuilding / bulldozeTile / placeWaterTerraform / placeLandTerraform).
// All functions mutate the grid in place - callers pass a cloned grid.
import {
  createBuilding,
  createTile,
  getBuildingSize,
  WATERFRONT_BUILDINGS,
} from './gamestate.mjs';

const SINGLE_TILE_ALLOWED = ['grass', 'tree', 'road', 'rail'];
const ZONING_ALLOWED = ['grass', 'tree', 'road'];

function tileAt(grid, x, y) {
  return grid[y]?.[x] || null;
}

export function canPlaceMultiTileBuilding(grid, x, y, width, height, gridSize) {
  if (x + width > gridSize || y + height > gridSize) return false;
  for (let dy = 0; dy < height; dy++) {
    for (let dx = 0; dx < width; dx++) {
      const tile = grid[y + dy]?.[x + dx];
      if (!tile) return false;
      if (tile.building.type !== 'grass' && tile.building.type !== 'tree') return false;
    }
  }
  return true;
}

export function getWaterAdjacency(grid, x, y, width, height, gridSize) {
  let waterOnSouthOrEast = false;
  let waterOnNorthOrWest = false;

  for (let dx = 0; dx < width; dx++) {
    if (grid[y + height]?.[x + dx]?.building.type === 'water') { waterOnSouthOrEast = true; break; }
  }
  if (!waterOnSouthOrEast) {
    for (let dy = 0; dy < height; dy++) {
      if (grid[y + dy]?.[x + width]?.building.type === 'water') { waterOnSouthOrEast = true; break; }
    }
  }
  for (let dx = 0; dx < width; dx++) {
    if (grid[y - 1]?.[x + dx]?.building.type === 'water') { waterOnNorthOrWest = true; break; }
  }
  if (!waterOnNorthOrWest) {
    for (let dy = 0; dy < height; dy++) {
      if (grid[y + dy]?.[x - 1]?.building.type === 'water') { waterOnNorthOrWest = true; break; }
    }
  }

  const hasWater = waterOnSouthOrEast || waterOnNorthOrWest;
  const shouldFlip = hasWater && waterOnNorthOrWest && !waterOnSouthOrEast;
  return { hasWater, shouldFlip };
}

export function applyBuildingFootprint(grid, originX, originY, buildingType) {
  const size = getBuildingSize(buildingType);
  for (let dy = 0; dy < size.height; dy++) {
    for (let dx = 0; dx < size.width; dx++) {
      const cell = grid[originY + dy][originX + dx];
      if (dx === 0 && dy === 0) {
        cell.building = createBuilding(buildingType);
      } else {
        cell.building = createBuilding('empty');
        cell.building.level = 0;
      }
      cell.zone = 'none';
    }
  }
}

export function findBuildingOrigin(grid, x, y, gridSize) {
  const tile = grid[y]?.[x];
  if (!tile) return null;

  if (tile.building.type !== 'empty' && tile.building.type !== 'grass' &&
      tile.building.type !== 'water' && tile.building.type !== 'road' &&
      tile.building.type !== 'bridge' && tile.building.type !== 'rail' && tile.building.type !== 'tree') {
    const size = getBuildingSize(tile.building.type);
    if (size.width > 1 || size.height > 1) {
      return { originX: x, originY: y, buildingType: tile.building.type };
    }
    return null;
  }

  if (tile.building.type === 'empty') {
    const maxSize = 4;
    for (let dy = 0; dy < maxSize; dy++) {
      for (let dx = 0; dx < maxSize; dx++) {
        const checkX = x - dx;
        const checkY = y - dy;
        if (checkX >= 0 && checkY >= 0 && checkX < gridSize && checkY < gridSize) {
          const checkTile = grid[checkY][checkX];
          if (checkTile.building.type !== 'empty' &&
              checkTile.building.type !== 'grass' &&
              checkTile.building.type !== 'water' &&
              checkTile.building.type !== 'road' &&
              checkTile.building.type !== 'bridge' &&
              checkTile.building.type !== 'rail' &&
              checkTile.building.type !== 'tree') {
            const size = getBuildingSize(checkTile.building.type);
            if (x >= checkX && x < checkX + size.width &&
                y >= checkY && y < checkY + size.height) {
              return { originX: checkX, originY: checkY, buildingType: checkTile.building.type };
            }
          }
        }
      }
    }
  }

  return null;
}

export function findConnectedBridgeTiles(grid, gridSize, x, y) {
  const tile = grid[y]?.[x];
  if (!tile || tile.building.type !== 'bridge') return [];

  const orientation = tile.building.bridgeOrientation || 'ns';
  const bridgeTiles = [{ x, y }];
  const dx = orientation === 'ns' ? 1 : 0;
  const dy = orientation === 'ns' ? 0 : 1;

  let cx = x + dx;
  let cy = y + dy;
  while (cx >= 0 && cx < gridSize && cy >= 0 && cy < gridSize) {
    const t = grid[cy][cx];
    if (t.building.type === 'bridge' && t.building.bridgeOrientation === orientation) {
      bridgeTiles.push({ x: cx, y: cy });
      cx += dx;
      cy += dy;
    } else break;
  }

  cx = x - dx;
  cy = y - dy;
  while (cx >= 0 && cx < gridSize && cy >= 0 && cy < gridSize) {
    const t = grid[cy][cx];
    if (t.building.type === 'bridge' && t.building.bridgeOrientation === orientation) {
      bridgeTiles.push({ x: cx, y: cy });
      cx -= dx;
      cy -= dy;
    } else break;
  }

  return bridgeTiles;
}

export function findAdjacentBridgeTiles(grid, gridSize, x, y) {
  const directions = [{ dx: -1, dy: 0 }, { dx: 1, dy: 0 }, { dx: 0, dy: -1 }, { dx: 0, dy: 1 }];
  for (const { dx, dy } of directions) {
    const nx = x + dx;
    const ny = y + dy;
    if (nx >= 0 && nx < gridSize && ny >= 0 && ny < gridSize) {
      const neighbor = grid[ny][nx];
      if (neighbor.building.type === 'bridge') {
        const position = neighbor.building.bridgePosition;
        if (position === 'start' || position === 'end') {
          return findConnectedBridgeTiles(grid, gridSize, nx, ny);
        }
      }
    }
  }
  return [];
}

// Port of simulation.ts placeBuilding - mutates grid, returns { ok, reason }
export function tryPlace(grid, gridSize, x, y, buildingType, zone) {
  const tile = tileAt(grid, x, y);
  if (!tile) return { ok: false, reason: `(${x},${y}) is out of bounds` };

  if (tile.building.type === 'water') {
    return { ok: false, reason: `(${x},${y}) is water - cannot build (use terraform land first)` };
  }

  if (buildingType === 'road' || buildingType === 'rail') {
    if (!SINGLE_TILE_ALLOWED.includes(tile.building.type)) {
      return { ok: false, reason: `(${x},${y}) has "${tile.building.type}" - road/rail only allowed on grass/tree/road/rail` };
    }
  }

  if (buildingType && buildingType !== 'road' && buildingType !== 'rail' &&
      (tile.building.type === 'road' || tile.building.type === 'bridge' || tile.building.type === 'rail')) {
    return { ok: false, reason: `(${x},${y}) has "${tile.building.type}" - bulldoze it first` };
  }

  if (zone !== null) {
    if (zone === 'none') {
      const origin = findBuildingOrigin(grid, x, y, gridSize);
      if (origin) {
        const size = getBuildingSize(origin.buildingType);
        for (let dy = 0; dy < size.height; dy++) {
          for (let dx = 0; dx < size.width; dx++) {
            const clearX = origin.originX + dx;
            const clearY = origin.originY + dy;
            if (clearX < gridSize && clearY < gridSize) {
              grid[clearY][clearX].building = createBuilding('grass');
              grid[clearY][clearX].zone = 'none';
            }
          }
        }
      } else {
        if (tile.zone === 'none') {
          return { ok: false, reason: `(${x},${y}) has no zone to remove` };
        }
        grid[y][x].zone = 'none';
        grid[y][x].building = createBuilding('grass');
      }
      return { ok: true };
    }
    if (!ZONING_ALLOWED.includes(tile.building.type)) {
      return { ok: false, reason: `(${x},${y}) has "${tile.building.type}" - zoning only allowed on grass/tree/road` };
    }
    grid[y][x].zone = zone;
    return { ok: true };
  }

  if (!buildingType) return { ok: false, reason: 'no building type given' };

  const size = getBuildingSize(buildingType);
  let shouldFlip = false;
  if (WATERFRONT_BUILDINGS.includes(buildingType)) {
    const waterCheck = getWaterAdjacency(grid, x, y, size.width, size.height, gridSize);
    if (!waterCheck.hasWater) {
      return { ok: false, reason: `${buildingType} at (${x},${y}) must be adjacent to water` };
    }
    shouldFlip = waterCheck.shouldFlip;
  }

  if (size.width > 1 || size.height > 1) {
    if (!canPlaceMultiTileBuilding(grid, x, y, size.width, size.height, gridSize)) {
      return { ok: false, reason: `${buildingType} (${size.width}x${size.height}) does not fit at (${x},${y}) - needs clear grass/tree tiles` };
    }
    applyBuildingFootprint(grid, x, y, buildingType);
    if (shouldFlip) grid[y][x].building.flipped = true;
    return { ok: true };
  }

  if (!SINGLE_TILE_ALLOWED.includes(tile.building.type)) {
    return { ok: false, reason: `(${x},${y}) has "${tile.building.type}" - cannot place here` };
  }

  if (buildingType === 'rail' && tile.building.type === 'road') {
    grid[y][x].hasRailOverlay = true;
  } else if (buildingType === 'road' && tile.building.type === 'rail') {
    grid[y][x].building = createBuilding('road');
    grid[y][x].hasRailOverlay = true;
    grid[y][x].zone = 'none';
  } else if (buildingType === 'rail' && tile.hasRailOverlay) {
    // already has rail overlay
  } else if (buildingType === 'road' && tile.hasRailOverlay) {
    // already road with rail overlay
  } else {
    grid[y][x].building = createBuilding(buildingType);
    grid[y][x].zone = 'none';
    if (buildingType !== 'road') grid[y][x].hasRailOverlay = false;
  }
  if (shouldFlip) grid[y][x].building.flipped = true;
  return { ok: true };
}

// Port of simulation.ts bulldozeTile - mutates grid, returns { ok, reason }
export function tryBulldoze(grid, gridSize, x, y) {
  const tile = tileAt(grid, x, y);
  if (!tile) return { ok: false, reason: `(${x},${y}) is out of bounds` };
  if (tile.building.type === 'water') return { ok: false, reason: `(${x},${y}) is water - nothing to bulldoze` };

  if (tile.building.type === 'bridge') {
    const bridgeTiles = findConnectedBridgeTiles(grid, gridSize, x, y);
    for (const bt of bridgeTiles) {
      grid[bt.y][bt.x].building = createBuilding('water');
      grid[bt.y][bt.x].zone = 'none';
      grid[bt.y][bt.x].hasRailOverlay = false;
    }
    return { ok: true };
  }

  if (tile.building.type === 'road') {
    const adjacentBridgeTiles = findAdjacentBridgeTiles(grid, gridSize, x, y);
    if (adjacentBridgeTiles.length > 0) {
      grid[y][x].building = createBuilding('grass');
      grid[y][x].zone = 'none';
      grid[y][x].hasRailOverlay = false;
      for (const bt of adjacentBridgeTiles) {
        grid[bt.y][bt.x].building = createBuilding('water');
        grid[bt.y][bt.x].zone = 'none';
        grid[bt.y][bt.x].hasRailOverlay = false;
      }
      return { ok: true };
    }
  }

  const origin = findBuildingOrigin(grid, x, y, gridSize);
  if (origin) {
    const size = getBuildingSize(origin.buildingType);
    for (let dy = 0; dy < size.height; dy++) {
      for (let dx = 0; dx < size.width; dx++) {
        const clearX = origin.originX + dx;
        const clearY = origin.originY + dy;
        if (clearX < gridSize && clearY < gridSize) {
          grid[clearY][clearX].building = createBuilding('grass');
          grid[clearY][clearX].zone = 'none';
          grid[clearY][clearX].hasRailOverlay = false;
        }
      }
    }
    return { ok: true };
  }

  if (tile.building.type === 'grass' && tile.zone === 'none' && !tile.hasSubway) {
    return { ok: false, reason: `(${x},${y}) is already empty grass` };
  }

  grid[y][x].building = createBuilding('grass');
  grid[y][x].zone = 'none';
  grid[y][x].hasRailOverlay = false;
  return { ok: true };
}

// Port of simulation.ts placeWaterTerraform - mutates grid
export function tryTerraformWater(grid, gridSize, x, y) {
  const tile = tileAt(grid, x, y);
  if (!tile) return { ok: false, reason: `(${x},${y}) is out of bounds` };
  if (tile.building.type === 'water') return { ok: false, reason: `(${x},${y}) is already water` };
  if (tile.building.type === 'bridge') return { ok: false, reason: `(${x},${y}) is a bridge - terraforming would break it` };

  const origin = findBuildingOrigin(grid, x, y, gridSize);
  if (origin) {
    const size = getBuildingSize(origin.buildingType);
    for (let dy = 0; dy < size.height; dy++) {
      for (let dx = 0; dx < size.width; dx++) {
        const clearX = origin.originX + dx;
        const clearY = origin.originY + dy;
        if (clearX < gridSize && clearY < gridSize) {
          grid[clearY][clearX].building = createBuilding('grass');
          grid[clearY][clearX].zone = 'none';
        }
      }
    }
  }

  grid[y][x].building = createBuilding('water');
  grid[y][x].zone = 'none';
  grid[y][x].hasSubway = false;
  return { ok: true };
}

// Port of simulation.ts placeLandTerraform - mutates grid
export function tryTerraformLand(grid, gridSize, x, y) {
  const tile = tileAt(grid, x, y);
  if (!tile) return { ok: false, reason: `(${x},${y}) is out of bounds` };
  if (tile.building.type !== 'water') return { ok: false, reason: `(${x},${y}) is not water` };

  grid[y][x].building = createBuilding('grass');
  grid[y][x].zone = 'none';
  return { ok: true };
}
