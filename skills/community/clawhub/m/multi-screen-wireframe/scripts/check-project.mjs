#!/usr/bin/env node
import assert from 'node:assert/strict'
import { createHash } from 'node:crypto'
import { readFile, readdir } from 'node:fs/promises'
import { dirname, isAbsolute, join, relative, resolve, sep } from 'node:path'
import { runInNewContext } from 'node:vm'
import { fileURLToPath, pathToFileURL } from 'node:url'

const skillRoot = dirname(dirname(fileURLToPath(import.meta.url)))
const skillVersion = (await readFile(join(skillRoot, 'VERSION'), 'utf8')).trim()
const skillTag = `multi-screen-wireframe@${skillVersion}`

async function listFiles(root) {
  const entries = await readdir(root, { recursive: true, withFileTypes: true })
  return entries
    .filter((entry) => entry.isFile())
    .map((entry) => {
      const parentPath = entry.parentPath || entry.path
      assert.ok(parentPath, `cannot resolve parent directory for ${entry.name}`)
      return normalizePathSeparators(relative(root, join(parentPath, entry.name)))
    })
}

export function normalizePathSeparators(filePath) {
  return filePath.replaceAll('\\', '/')
}

function runClassicScript(source, api) {
  const context = { WireframeVue: api }
  context.window = context
  runInNewContext(source, context)
}

function assertInside(root, source, label) {
  assert.ok(typeof source === 'string' && source.trim(), `${label}.source must be a non-empty string`)
  assert.ok(!isAbsolute(source), `${label}.source must be relative`)
  const target = resolve(root, source)
  assert.ok(target.startsWith(`${root}${sep}`), `${label}.source escapes the project`)
  return target
}

function assertVersionComment(source, label) {
  assert.match(source, new RegExp(`@wireframe-skill\\s+${skillTag.replaceAll('.', '\\.').replaceAll('-', '\\-')}`), `${label} must use ${skillTag}`)
  assert.match(source, /创建基于\s+v\d+\.\d+\.\d+/, `${label} must preserve 创建基于`)
  assert.match(source, new RegExp(`修改基于\\s+v${skillVersion.replaceAll('.', '\\.')}`), `${label} must update 修改基于 to v${skillVersion}`)
}

function componentContract(uiSource) {
  const block = uiSource.match(/const components = Object\.freeze\(\{([\s\S]*?)\n\s*\}\)/)
  assert.ok(block, 'framework/runtime/ui.js public component registry is missing')
  const names = [...block[1].matchAll(/^\s+(Wf[A-Z][A-Za-z0-9]*),\s*$/gm)].map((match) => match[1])
  assert.ok(names.length > 0, 'framework/runtime/ui.js public component registry is empty')
  return {
    fingerprint: createHash('sha256').update(uiSource).digest('hex'),
    names,
  }
}

async function assertComponentDocs(root, frameworkRoot) {
  const docs = await readFile(join(root, 'COMPONENTS.md'), 'utf8')
  const uiSource = await readFile(join(frameworkRoot, 'runtime/ui.js'), 'utf8')
  const contract = componentContract(uiSource)
  const marker = docs.match(/<!-- ui-contract-sha256: ([a-f0-9]{64}) -->/)
  assert.ok(marker, 'COMPONENTS.md ui-contract-sha256 marker is missing')
  assert.equal(marker[1], contract.fingerprint, 'COMPONENTS.md is stale: review the API text and update ui-contract-sha256')
  const documentedNames = [...docs.matchAll(/^### (Wf[A-Z][A-Za-z0-9]*)\s*$/gm)].map((match) => match[1])
  assert.deepEqual(documentedNames.sort(), [...contract.names].sort(), 'COMPONENTS.md must contain exactly one heading for every public Wf component')
}

export async function checkProject(projectDirectory, options = {}) {
  const root = resolve(projectDirectory)
  const frameworkRoot = resolve(options.frameworkDirectory || join(root, 'framework'))
  const frameworkFormat = (await readFile(join(frameworkRoot, 'FORMAT_VERSION'), 'utf8')).trim()
  assert.equal(frameworkFormat, 'vue-global@2', 'framework/FORMAT_VERSION must be vue-global@2')
  const projectSource = await readFile(join(root, 'src/project.js'), 'utf8')
  let project = null
  runClassicScript(projectSource, { defineProject(value) { project = value } })
  assert.ok(project && typeof project === 'object', 'src/project.js must call WireframeVue.defineProject()')
  assert.equal(project.format, 'vue-global', 'project.format must be "vue-global"')
  assert.equal(project.formatVersion, 2, 'project.formatVersion must be 2')
  assert.ok(project.viewports && typeof project.viewports === 'object', 'project.viewports must be an object')
  const viewports = Object.entries(project.viewports)
  assert.ok(viewports.length > 0, 'project.viewports must not be empty')
  for (const [key, viewport] of viewports) {
    assert.ok(Number.isFinite(viewport?.width) && viewport.width > 0, `viewport ${key}.width must be positive`)
    assert.ok(Number.isFinite(viewport?.height) && viewport.height > 0, `viewport ${key}.height must be positive`)
  }
  assert.ok(Object.hasOwn(project.viewports, project.defaultViewport), 'project.defaultViewport is missing')

  assert.ok(Array.isArray(project.screens) && project.screens.length > 0, 'project.screens must not be empty')
  const screens = Array.from(project.screens)
  const ids = screens.map((screen) => screen.id)
  assert.equal(new Set(ids).size, ids.length, 'screen ids must be unique')
  assert.ok(screens.some((screen) => screen.entry === true), 'at least one screen must set entry: true')

  const screenDirectory = join(root, 'src/screens')
  const screenFiles = (await readdir(screenDirectory))
    .filter((name) => name.endsWith('.js') && name !== '_template.js')
    .sort()
  assert.deepEqual(screenFiles, ids.map((id) => `${id}.js`).sort(), 'project screens and src/screens files must match exactly')

  for (const screen of screens) {
    assert.match(screen.id, /^[a-z0-9-]+$/, `invalid screen id: ${screen.id}`)
    assert.ok(typeof screen.title === 'string' && screen.title.trim(), `${screen.id}.title must be non-empty`)
    assert.ok(Array.isArray(screen.links), `${screen.id}.links must be an array`)
    assert.ok(Array.isArray(screen.edgeCases), `${screen.id}.edgeCases must be an array`)
    for (const target of screen.links) assert.ok(ids.includes(target), `${screen.id} links to missing screen ${target}`)

    const source = await readFile(join(screenDirectory, `${screen.id}.js`), 'utf8')
    assert.doesNotMatch(source, /^\s*(?:import|export)\s/m, `${screen.id}.js must not use ESM`)
    assert.match(source, new RegExp(`WireframeVue\\.defineScreen\\(['"]${screen.id}['"]`), `${screen.id}.js must register its id`)
    assertVersionComment(source, `src/screens/${screen.id}.js`)
    new Function(source)
  }

  const componentNames = new Set()
  for (const [index, entry] of (project.components || []).entries()) {
    const label = `project.components[${index}]`
    assert.match(entry.name, /^Wf[A-Z][A-Za-z0-9]*$/, `${label}.name must use Wf PascalCase`)
    assert.ok(!componentNames.has(entry.name), `duplicate business component ${entry.name}`)
    componentNames.add(entry.name)
    const sourcePath = assertInside(root, entry.source, label)
    const source = await readFile(sourcePath, 'utf8')
    assert.doesNotMatch(source, /^\s*(?:import|export)\s/m, `${entry.source} must not use ESM`)
    assert.match(source, new RegExp(`defineComponent\\(['"]${entry.name}['"]`), `${entry.source} must register ${entry.name}`)
    if (entry.source.includes('/layouts/')) assertVersionComment(source, entry.source)
    new Function(source)
  }

  const annotationsSource = await readFile(join(root, 'src/annotations.js'), 'utf8')
  let annotationState = null
  runClassicScript(annotationsSource, { defineAnnotations(value) { annotationState = value } })
  assert.ok(annotationState && typeof annotationState === 'object', 'src/annotations.js must call defineAnnotations()')
  assert.ok(typeof annotationState.annotationsRevision === 'string' && annotationState.annotationsRevision, 'annotationsRevision must be non-empty')
  assert.ok(Array.isArray(annotationState.annotations), 'annotations must be an array')
  const annotationIds = new Set()
  for (const annotation of annotationState.annotations) {
    assert.ok(annotation.id && !annotationIds.has(annotation.id), `duplicate or missing annotation id ${annotation.id}`)
    annotationIds.add(annotation.id)
    assert.ok(ids.includes(annotation.screenId), `annotation ${annotation.id} references missing screen`)
    assert.ok(annotation.anchor?.kind === 'screen' || annotation.anchor?.kind === 'node', `annotation ${annotation.id} has invalid anchor`)
    if (annotation.anchor.kind === 'node') assert.ok(annotation.anchor.selector, `annotation ${annotation.id} node anchor needs selector`)
    assert.ok(typeof annotation.content === 'string' && annotation.content.trim(), `annotation ${annotation.id} content is empty`)
  }

  const indexSource = await readFile(join(root, 'index.html'), 'utf8')
  const orderedScripts = [
    'vue.global.js',
    'registry.js',
    'ui.js',
    'react.production.min.js',
    'react-dom.production.min.js',
    'board.js',
    'src/project.js',
    'src/annotations.js',
    'loader.js',
  ]
  let lastIndex = -1
  for (const script of orderedScripts) {
    const nextIndex = indexSource.indexOf(script)
    assert.ok(nextIndex > lastIndex, `index.html must load ${script} in framework order`)
    lastIndex = nextIndex
  }

  const sourceFiles = await listFiles(join(root, 'src'))
  assert.ok(!sourceFiles.some((file) => file.endsWith('.jsx') || file.endsWith('.vue') || file.endsWith('.ts')), 'src must only use classic JavaScript, CSS, and data assets')
  const frameworkFiles = await listFiles(frameworkRoot)
  assert.ok(!frameworkFiles.some((file) => /esbuild|\.wasm$/i.test(file)), 'framework must not contain esbuild or WASM')
  if (options.allowMaintenanceSource !== true) {
    assert.ok(!frameworkFiles.some((file) => /\.(?:jsx|tsx|ts)$/i.test(file)), 'delivery framework must not contain maintenance source')
  }
  assert.ok(frameworkFiles.some((file) => file.endsWith('runtime/board.js')), 'framework/runtime/board.js is missing')
  assert.ok(frameworkFiles.some((file) => file.endsWith('vendor/LICENSE-vue.txt')), 'Vue license is missing')
  assert.ok(frameworkFiles.some((file) => file.endsWith('vendor/VERSIONS.txt')), 'vendor version record is missing')

  if (options.delivery !== false) {
    const rootNames = await readdir(root)
    assert.ok(!rootNames.includes('dist'), 'delivery must not contain dist/')
    assert.ok(!rootNames.includes('build.command') && !rootNames.includes('build.cmd'), 'delivery must not contain build scripts')
    assert.doesNotMatch(indexSource, /(?:src|href)=["'][^"']*\.\.\/[^"']*framework\//, 'delivery index.html must use its local framework/ and must not copy demo paths')
    if (options.allowMaintenanceSource !== true) await assertComponentDocs(root, frameworkRoot)
  }

  return { root, projectName: project.name, screenCount: ids.length, componentCount: componentNames.size }
}

const invokedPath = process.argv[1] ? pathToFileURL(resolve(process.argv[1])).href : ''
if (invokedPath === import.meta.url) {
  const target = process.argv[2] || join(skillRoot, 'starter')
  const result = await checkProject(target)
  console.log(`vue-global project: pass (${result.screenCount} screens, ${result.componentCount} shared components)\n${result.root}`)
}
