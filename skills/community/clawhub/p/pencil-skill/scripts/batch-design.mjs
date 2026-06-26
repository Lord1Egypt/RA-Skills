#!/usr/bin/env node
import fs from 'node:fs';
import {
  loadPen,
  savePen,
  backupPen,
  parseArgs,
  printHelpAndExit,
  fail,
  parseJsonOrFail,
  findNodeById,
  findNodeContainerById,
  collectIds,
  ensureChildrenArray,
  deepMerge,
  clone,
} from './_utils.mjs';

const HELP = `Usage: node scripts/batch-design.mjs <file.pen> --ops '<JSON operations>'\n   or: node scripts/batch-design.mjs <file.pen> --ops-file <ops.json>`;
const args = parseArgs(process.argv.slice(2));
if (args.help) printHelpAndExit(HELP);
const file = args._[0];
if (!file) printHelpAndExit(HELP, 1);
if (!args.ops && !args['ops-file']) fail('Provide either --ops or --ops-file');

const pen = loadPen(file);
let ops;
if (args.ops) {
  ops = parseJsonOrFail(args.ops, '--ops JSON');
} else {
  let raw;
  try { raw = fs.readFileSync(args['ops-file'], 'utf8'); } catch (error) { fail(`Failed to read ops file: ${error.message}`); }
  ops = parseJsonOrFail(raw, 'ops file JSON');
}
if (!Array.isArray(ops)) fail('Operations must be a JSON array');

backupPen(file);

let changed = 0;
const ids = collectIds(pen);

function normalizeAliasesInNode(value) {
  if (!value || typeof value !== 'object') return value;

  if (!Array.isArray(value)) {
    const aliases = [
      ['fills', 'fill'],
      ['strokes', 'stroke'],
      ['effects', 'effect'],
    ];
    for (const [plural, singular] of aliases) {
      if (plural in value) {
        if (!(singular in value)) value[singular] = value[plural];
        delete value[plural];
      }
    }
  }

  if (Array.isArray(value)) {
    for (const item of value) normalizeAliasesInNode(item);
    return value;
  }

  for (const child of Object.values(value)) {
    normalizeAliasesInNode(child);
  }
  return value;
}

function isDescendantNode(candidate, ancestorId) {
  if (!candidate || !Array.isArray(candidate.children)) return false;
  for (const child of candidate.children) {
    if (child?.id === ancestorId) return true;
    if (isDescendantNode(child, ancestorId)) return true;
  }
  return false;
}

function normalizeIndex(index, arrLen) {
  if (index === undefined || index === null) return arrLen;
  const n = Number(index);
  if (!Number.isInteger(n)) fail(`Invalid index: ${index}`);
  return Math.max(0, Math.min(n, arrLen));
}

for (let i = 0; i < ops.length; i += 1) {
  const op = ops[i];
  try {
    if (!op || typeof op !== 'object' || typeof op.op !== 'string') throw new Error('Operation must be object with "op"');

    if (op.op === 'insert') {
      const parent = findNodeById(pen, op.parentId);
      if (!parent) throw new Error(`Parent not found: ${op.parentId}`);
      ensureChildrenArray(parent.node, `parent ${op.parentId}`);
      if (!op.node || typeof op.node !== 'object') throw new Error('insert.node is required');
      if (!op.node.id) throw new Error('insert.node.id is required');
      if (ids.has(op.node.id)) throw new Error(`Duplicate id: ${op.node.id}`);

      normalizeAliasesInNode(op.node);
      const idx = normalizeIndex(op.index, parent.node.children.length);
      parent.node.children.splice(idx, 0, op.node);
      ids.add(op.node.id);
      changed += 1;
    } else if (op.op === 'update') {
      const found = findNodeById(pen, op.id);
      if (!found) throw new Error(`Node not found: ${op.id}`);
      if (!op.props || typeof op.props !== 'object') throw new Error('update.props is required');
      if (op.props.id && op.props.id !== op.id && ids.has(op.props.id)) {
        throw new Error(`Cannot change id to duplicate: ${op.props.id}`);
      }
      const oldId = found.node.id;
      const merged = normalizeAliasesInNode(deepMerge(found.node, op.props));
      found.parent.children[found.parent.children.findIndex((c) => c.id === oldId)] = merged;
      if (merged.id !== oldId) {
        ids.delete(oldId);
        ids.add(merged.id);
      }
      changed += 1;
    } else if (op.op === 'delete') {
      const found = findNodeContainerById(pen, op.id);
      if (!found) throw new Error(`Node not found: ${op.id}`);
      found.container.splice(found.index, 1);
      // Remove deleted node and all descendant IDs from tracking
      const deletedIds = collectIds({ children: [found.node] });
      for (const did of deletedIds) ids.delete(did);
      changed += 1;
    } else if (op.op === 'move') {
      const found = findNodeContainerById(pen, op.id);
      if (!found) throw new Error(`Node not found: ${op.id}`);
      const target = findNodeById(pen, op.toParentId);
      if (!target) throw new Error(`Target parent not found: ${op.toParentId}`);
      if (op.id === op.toParentId || isDescendantNode(found.node, op.toParentId)) {
        throw new Error(`Invalid move: cannot move ${op.id} into its own descendant (${op.toParentId})`);
      }
      ensureChildrenArray(target.node, `target parent ${op.toParentId}`);
      found.container.splice(found.index, 1);
      const idx = normalizeIndex(op.index, target.node.children.length);
      target.node.children.splice(idx, 0, found.node);
      changed += 1;
    } else if (op.op === 'copy') {
      const found = findNodeById(pen, op.id);
      if (!found) throw new Error(`Node not found: ${op.id}`);
      if (!op.newId) throw new Error('copy.newId is required');
      if (ids.has(op.newId)) throw new Error(`Duplicate id: ${op.newId}`);
      const targetParentId = op.toParentId ?? 'root';
      const target = targetParentId === 'root' ? { node: pen } : findNodeById(pen, targetParentId);
      if (!target) throw new Error(`Target parent not found: ${targetParentId}`);
      ensureChildrenArray(target.node, `target parent ${targetParentId}`);

      const copied = clone(found.node);
      const oldRootId = copied.id;
      copied.id = op.newId;

      // Collect all original IDs in the source subtree for ref matching
      const originalIds = collectIds({ children: [found.node] });
      originalIds.delete(found.node.id); // exclude root (already renamed)

      function prefixDescendantIds(node, prefix) {
        if (node.children) {
          for (const child of node.children) {
            if (child.id) {
              child.id = `${prefix}-${child.id}`;
            }
            prefixDescendantIds(child, prefix);
          }
        }
        // Rewrite ref if it points to any ID within the original subtree
        if (node.ref && originalIds.has(node.ref)) {
          node.ref = `${prefix}-${node.ref}`;
        }
        // Update descendants overrides keys
        if (node.descendants) {
          const newDescendants = {};
          for (const [key, val] of Object.entries(node.descendants)) {
            const prefixedKey = key.split('/').map(seg => `${prefix}-${seg}`).join('/');
            newDescendants[prefixedKey] = val;
          }
          node.descendants = newDescendants;
        }
      }
      prefixDescendantIds(copied, op.newId);

      // Verify no duplicates
      const copiedIds = collectIds({ children: [copied] });
      for (const cid of copiedIds) {
        if (ids.has(cid)) {
          throw new Error(`Copy would duplicate id: ${cid}`);
        }
      }

      const idx = normalizeIndex(op.index, target.node.children.length);
      target.node.children.splice(idx, 0, copied);
      for (const cid of copiedIds) ids.add(cid);
      changed += 1;
    } else {
      throw new Error(`Unsupported op: ${op.op}`);
    }
  } catch (error) {
    fail(`Operation #${i + 1} failed: ${error.message}`);
  }
}

savePen(file, pen);
process.stdout.write(`OK: ${changed} operation(s) applied\n`);
