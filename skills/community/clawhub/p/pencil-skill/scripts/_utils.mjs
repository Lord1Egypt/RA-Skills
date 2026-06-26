import fs from 'node:fs';
import path from 'node:path';

export function printHelpAndExit(helpText, code = 0) {
  const out = code === 0 ? process.stdout : process.stderr;
  out.write(`${helpText.trim()}\n`);
  process.exit(code);
}

export function fail(message) {
  process.stderr.write(`${message}\n`);
  process.exit(1);
}

export function parseJsonOrFail(text, label = 'JSON') {
  try {
    return JSON.parse(text);
  } catch (error) {
    fail(`Invalid ${label}: ${error.message}`);
  }
}

export function loadPen(filePath) {
  let raw;
  try {
    raw = fs.readFileSync(filePath, 'utf8');
  } catch (error) {
    fail(`Failed to read file: ${filePath} (${error.message})`);
  }

  const data = parseJsonOrFail(raw, '.pen JSON');
  if (!data || typeof data !== 'object' || !Array.isArray(data.children)) {
    fail('Invalid .pen file: missing top-level "children" array');
  }
  return data;
}

export function savePen(filePath, data) {
  try {
    fs.writeFileSync(filePath, `${JSON.stringify(data, null, 2)}\n`, 'utf8');
  } catch (error) {
    fail(`Failed to save file: ${filePath} (${error.message})`);
  }
}

export function backupPen(filePath) {
  const backupPath = `${filePath}.bak`;
  try {
    fs.copyFileSync(filePath, backupPath);
  } catch (error) {
    fail(`Failed to create backup: ${backupPath} (${error.message})`);
  }
  return backupPath;
}

export function walkNodes(tree, callback, options = {}) {
  const maxDepth = Number.isInteger(options.maxDepth) ? options.maxDepth : Infinity;

  function walk(node, parent, depth, pathIds) {
    callback(node, { parent, depth, pathIds: [...pathIds] });
    if (depth >= maxDepth) return;
    if (!Array.isArray(node?.children)) return;
    for (const child of node.children) {
      const nextPath = child?.id ? [...pathIds, child.id] : [...pathIds, '(no-id)'];
      walk(child, node, depth + 1, nextPath);
    }
  }

  if (Array.isArray(tree?.children)) {
    for (const child of tree.children) {
      walk(child, tree, 0, [child?.id || '(no-id)']);
    }
  }
}

export function findNodeById(tree, id) {
  if (!id) return null;
  let result = null;

  function walk(node, parent, parentPath) {
    if (result) return;
    const currentPath = [...parentPath, node.id || '(no-id)'];
    if (node.id === id) {
      result = { node, parent, path: currentPath };
      return;
    }
    if (!Array.isArray(node.children)) return;
    for (const child of node.children) {
      walk(child, node, currentPath);
      if (result) return;
    }
  }

  for (const child of tree.children || []) {
    walk(child, tree, []);
    if (result) break;
  }

  return result;
}

export function findNodeContainerById(tree, id) {
  function walkInArray(arr, parentNode) {
    for (let i = 0; i < arr.length; i += 1) {
      const node = arr[i];
      if (node?.id === id) {
        return { node, parent: parentNode, container: arr, index: i };
      }
      if (Array.isArray(node?.children)) {
        const found = walkInArray(node.children, node);
        if (found) return found;
      }
    }
    return null;
  }
  return walkInArray(tree.children || [], tree);
}

export function collectIds(tree) {
  const ids = new Set();
  walkNodes(tree, (node) => {
    if (node?.id) ids.add(node.id);
  });
  return ids;
}

export function deepMerge(target, source) {
  if (!source || typeof source !== 'object' || Array.isArray(source)) {
    return source;
  }
  const out = (target && typeof target === 'object' && !Array.isArray(target)) ? { ...target } : {};
  for (const [key, value] of Object.entries(source)) {
    if (value && typeof value === 'object' && !Array.isArray(value)) {
      out[key] = deepMerge(out[key], value);
    } else {
      out[key] = value;
    }
  }
  return out;
}

export function ensureChildrenArray(node, label = 'node') {
  if (!Array.isArray(node.children)) node.children = [];
  if (!Array.isArray(node.children)) {
    fail(`${label} does not support children array`);
  }
}

export function parseArgs(argv) {
  const args = { _: [] };
  for (let i = 0; i < argv.length; i += 1) {
    const token = argv[i];
    if (!token.startsWith('--')) {
      args._.push(token);
      continue;
    }
    const key = token.slice(2);
    const next = argv[i + 1];
    if (!next || next.startsWith('--')) {
      args[key] = true;
    } else {
      if (args[key] === undefined) {
        args[key] = next;
      } else if (Array.isArray(args[key])) {
        args[key].push(next);
      } else {
        args[key] = [args[key], next];
      }
      i += 1;
    }
  }
  return args;
}

export function toNumberOrFail(value, label) {
  const n = Number(value);
  if (!Number.isFinite(n)) fail(`Invalid number for ${label}: ${value}`);
  return n;
}

export function clone(value) {
  return JSON.parse(JSON.stringify(value));
}

export function basenameSafe(p) {
  return path.basename(p);
}
