#!/usr/bin/env node
import { cp, lstat } from 'node:fs/promises'
import { dirname, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const skillRoot = dirname(dirname(fileURLToPath(import.meta.url)))
const starter = resolve(skillRoot, 'starter')
const requested = process.argv[2]

if (!requested) {
  throw new Error('Usage: node scripts/create-project.mjs <new-target-directory>')
}

const target = resolve(requested)
if (target === skillRoot || target === starter || target === dirname(target)) {
  throw new Error(`Refusing unsafe target: ${target}`)
}

try {
  await lstat(target)
  throw new Error(`Target already exists: ${target}`)
} catch (error) {
  if (error.code !== 'ENOENT') throw error
}

await cp(starter, target, { recursive: true, errorOnExist: true })
console.log(`Created Vue Global wireframe project: ${target}`)
