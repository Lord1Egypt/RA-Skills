import { existsSync, lstatSync, readFileSync, statSync } from 'node:fs'
import { readdir, readFile, realpath, stat, writeFile } from 'node:fs/promises'
import { delimiter, dirname, extname, isAbsolute, relative, resolve, sep } from 'node:path'
import { spawn } from 'node:child_process'
import { fileURLToPath } from 'node:url'

export const ERROR_CODES = Object.freeze({
  CONFIG: 'MEDIA_COMPATIBILITY_INVALID',
  AI_MISSING: 'AI_CLI_NOT_FOUND',
  NODE: 'NODE_VERSION_UNSUPPORTED',
  CREDENTIAL: 'MEDIA_CREDENTIAL_MISSING',
  MODEL: 'MEDIA_MODEL_UNAVAILABLE',
  CATALOG: 'MODEL_CATALOG_UNAVAILABLE'
})

export class MediaError extends Error {
  constructor(code, message, safeRetry = false, details) {
    super(message)
    this.code = code
    this.safeRetry = safeRetry
    this.details = details
  }
}

export function fail(error) {
  return {
    ok: false,
    code: error?.code || 'MEDIA_GENERATION_FAILED',
    message: error?.message || 'Media generation failed.',
    safeRetry: Boolean(error?.safeRetry),
    ...(error?.details ? { details: error.details } : {})
  }
}

export function parseNodeMajor(version = process.version) {
  const match = String(version).match(/v?(\d+)/)
  return match ? Number(match[1]) : Number.NaN
}

export function parseAiCliVersion(output) {
  const match = String(output).match(/\b(\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?)\b/)
  if (!match) throw new MediaError(ERROR_CODES.AI_MISSING, 'Unable to parse ai-cli version.')
  return match[1]
}

export function validateCompatibility(value) {
  const invalid = (message) => { throw new MediaError(ERROR_CODES.CONFIG, message) }
  if (!value || value.schemaVersion !== 1) invalid('Unsupported media compatibility schema.')
  if (!Number.isInteger(value.minimumNodeMajor)) invalid('minimumNodeMajor must be an integer.')
  if (value.credentialEnvironmentVariable !== 'AI_GATEWAY_API_KEY') invalid('Only AI_GATEWAY_API_KEY is supported.')
  if (!value.image || typeof value.image.model !== 'string') invalid('Image model is required.')
  if (!Number.isInteger(value.image.maxReferences) || !Number.isInteger(value.image.maxReferenceBytes) || !Number.isInteger(value.image.timeoutSeconds)) invalid('Image limits are invalid.')
  if (!value.video || typeof value.video.models?.standard !== 'string' || typeof value.video.models?.high !== 'string') invalid('Video models are required.')
  for (const field of ['maxReferences', 'maxReferenceBytes', 'timeoutSeconds', 'defaultDurationSeconds', 'minimumDurationSeconds', 'maximumDurationSeconds']) {
    if (!Number.isInteger(value.video[field])) invalid(`Video ${field} is invalid.`)
  }
  if (typeof value.video.defaultResolution !== 'string') invalid('Video defaultResolution is required.')
  return value
}

export function loadCompatibility(path = resolve(dirname(fileURLToPath(import.meta.url)), '..', 'media-compatibility.json')) {
  try {
    return validateCompatibility(JSON.parse(readFileSync(path, 'utf8')))
  } catch (error) {
    if (error instanceof MediaError) throw error
    throw new MediaError(ERROR_CODES.CONFIG, 'Unable to parse media compatibility configuration.')
  }
}

function executableCandidates(name, platform, env) {
  if (platform !== 'win32') return [name]
  const extensions = (env.PATHEXT || '.EXE;.CMD;.BAT').split(';').filter(Boolean)
  return extname(name) ? [name] : [name, ...extensions.map((item) => `${name}${item.toLowerCase()}`)]
}

export function resolveAiExecutable({ env = process.env, platform = process.platform } = {}) {
  const pathValue = env.PATH || env.Path || env.path || ''
  for (const directory of pathValue.split(delimiter).filter(Boolean)) {
    for (const name of executableCandidates('ai', platform, env)) {
      const candidate = resolve(directory, name)
      try {
        accessSyncExecutable(candidate, platform)
        return candidate
      } catch {}
    }
  }
  throw new MediaError(ERROR_CODES.AI_MISSING, 'ai-cli is not installed or is not available on PATH.')
}

function accessSyncExecutable(path, platform) {
  if (!existsSync(path) || !statSync(path).isFile()) throw new Error('not executable')
  if (platform !== 'win32') {
    const mode = lstatSync(path).mode
    if ((mode & 0o111) === 0) throw new Error('not executable')
  }
}

export function runProcess(executable, args, { env = process.env, timeoutMs = 30000 } = {}) {
  return new Promise((resolvePromise, rejectPromise) => {
    const child = spawn(executable, args, { env, shell: false, stdio: ['ignore', 'pipe', 'pipe'] })
    const stdout = []
    const stderr = []
    let timedOut = false
    const timer = setTimeout(() => {
      timedOut = true
      child.kill('SIGKILL')
    }, timeoutMs)
    child.stdout.on('data', (chunk) => stdout.push(chunk))
    child.stderr.on('data', (chunk) => stderr.push(chunk))
    child.once('error', (error) => {
      clearTimeout(timer)
      rejectPromise(error)
    })
    child.once('close', (code, signal) => {
      clearTimeout(timer)
      resolvePromise({ code: code ?? 1, signal, timedOut, stdout: Buffer.concat(stdout).toString('utf8'), stderr: Buffer.concat(stderr).toString('utf8') })
    })
  })
}

function parseJsonOutput(stdout, code, message) {
  try {
    return JSON.parse(stdout)
  } catch {
    throw new MediaError(code, message)
  }
}

function findPricing(value) {
  if (!value || typeof value !== 'object') return null
  for (const key of ['pricing', 'price', 'cost']) {
    if (value[key] !== undefined) return value[key]
  }
  for (const child of Object.values(value)) {
    const found = findPricing(child)
    if (found !== null) return found
  }
  return null
}

export function selectModel(config, kind, qualityMode = 'standard') {
  if (kind === 'image') return config.image.model
  if (kind === 'video') return config.video.models[qualityMode]
  throw new MediaError('MEDIA_KIND_INVALID', 'kind must be image or video.')
}

export async function inspectRuntime(kind, options = {}) {
  const config = options.config || loadCompatibility()
  const nodeVersion = options.nodeVersion || process.version
  if (parseNodeMajor(nodeVersion) < config.minimumNodeMajor) {
    throw new MediaError(ERROR_CODES.NODE, `AI media requires Node.js ${config.minimumNodeMajor} or newer.`)
  }
  const env = options.env || process.env
  if (!env[config.credentialEnvironmentVariable]) {
    throw new MediaError(ERROR_CODES.CREDENTIAL, 'AI_GATEWAY_API_KEY is not configured.')
  }
  const executable = options.executable || resolveAiExecutable({ env, platform: options.platform })
  const runner = options.runner || runProcess
  let versionResult
  try {
    versionResult = await runner(executable, ['--version'], { env, timeoutMs: 15000 })
  } catch {
    throw new MediaError(ERROR_CODES.AI_MISSING, 'Unable to start ai-cli.')
  }
  if (versionResult.code !== 0) throw new MediaError(ERROR_CODES.AI_MISSING, 'Unable to resolve ai-cli version.')
  const model = selectModel(config, kind, options.qualityMode || 'standard')
  let catalogResult
  try {
    catalogResult = await runner(executable, ['models', model, '--json'], { env, timeoutMs: 30000 })
  } catch {
    throw new MediaError(ERROR_CODES.CATALOG, 'The ai-cli model catalog is unavailable.', true)
  }
  if (catalogResult.code !== 0) {
    throw new MediaError(ERROR_CODES.MODEL, `The configured ${kind} model is unavailable.`, true)
  }
  const catalog = parseJsonOutput(catalogResult.stdout, ERROR_CODES.CATALOG, 'The ai-cli model catalog returned invalid JSON.')
  const serialized = JSON.stringify(catalog)
  if (!serialized.includes(model)) throw new MediaError(ERROR_CODES.MODEL, `The configured ${kind} model is unavailable.`, true)
  const pricing = findPricing(catalog)
  return {
    ok: true,
    value: {
      available: true,
      kind,
      executable,
      aiCliVersion: parseAiCliVersion(versionResult.stdout),
      nodeVersion,
      credentialConfigured: true,
      model,
      modelAvailable: true,
      pricingSummary: pricing === null ? 'See the live Vercel AI Gateway model catalog.' : JSON.stringify(pricing)
    }
  }
}

export function validateRequest(request, config) {
  if (!request || request.schemaVersion !== 1) throw new MediaError('MEDIA_REQUEST_INVALID', 'Unsupported request schema.')
  if (!['image', 'video'].includes(request.kind)) throw new MediaError('MEDIA_KIND_INVALID', 'kind must be image or video.')
  if (!['passthrough', 'append_defaults'].includes(request.promptMode)) throw new MediaError('PROMPT_MODE_INVALID', 'promptMode must be passthrough or append_defaults.')
  if (!['standard', 'high'].includes(request.qualityMode)) throw new MediaError('QUALITY_MODE_INVALID', 'qualityMode must be standard or high.')
  if (typeof request.prompt !== 'string' || [...request.prompt].length < 1 || [...request.prompt].length > 4096) throw new MediaError('PROMPT_INVALID', 'prompt must contain 1–4096 Unicode characters.')
  if (typeof request.aspectRatio !== 'string' || request.aspectRatio.trim() === '') throw new MediaError('ASPECT_RATIO_INVALID', 'aspectRatio must be resolved before generation.')
  if (request.model !== undefined) throw new MediaError('MODEL_OVERRIDE_FORBIDDEN', 'Request files cannot select a model.')
  if (!Array.isArray(request.references)) throw new MediaError('REFERENCES_INVALID', 'references must be an array.')
  if (!request.source || !['verified_artifact', 'verified_evidence', 'analyzed_data', 'user_prompt'].includes(request.source.kind)) throw new MediaError('SOURCE_INVALID', 'A supported source kind is required.')
  if (request.source.path !== undefined && !isAbsolute(request.source.path)) throw new MediaError('SOURCE_INVALID', 'source.path must be absolute.')
  if (request.source.kind !== 'user_prompt' && (typeof request.source.path !== 'string' || !existsSync(request.source.path))) throw new MediaError('SOURCE_INVALID', 'A readable local source path is required for data-derived media.')
  if (request.kind === 'video' && request.duration !== null && request.duration !== undefined) {
    if (!Number.isInteger(request.duration) || request.duration < config.video.minimumDurationSeconds || request.duration > config.video.maximumDurationSeconds) throw new MediaError('DURATION_INVALID', `Video duration must be ${config.video.minimumDurationSeconds}–${config.video.maximumDurationSeconds} seconds.`)
  }
  return request
}

export function sniffImage(buffer) {
  if (buffer.length >= 8 && buffer.subarray(0, 8).equals(Buffer.from([137, 80, 78, 71, 13, 10, 26, 10]))) return 'image/png'
  if (buffer.length >= 3 && buffer[0] === 0xff && buffer[1] === 0xd8 && buffer[2] === 0xff) return 'image/jpeg'
  if (buffer.length >= 12 && buffer.toString('ascii', 0, 4) === 'RIFF' && buffer.toString('ascii', 8, 12) === 'WEBP') return 'image/webp'
  return null
}

export function sniffMedia(buffer, kind) {
  if (kind === 'image') return sniffImage(buffer)
  if (buffer.length >= 12 && buffer.toString('ascii', 4, 8) === 'ftyp') return 'video/mp4'
  return null
}

export async function validateReferences(request, config) {
  const limits = config[request.kind]
  if (request.references.length > limits.maxReferences) throw new MediaError('REFERENCE_LIMIT_EXCEEDED', `At most ${limits.maxReferences} reference image(s) are allowed.`)
  const checked = []
  for (const item of request.references) {
    if (typeof item !== 'string' || !isAbsolute(item) || /^(https?:|data:)/i.test(item)) throw new MediaError('REFERENCE_PATH_INVALID', 'Reference images must use local absolute paths.')
    let resolvedPath
    try {
      resolvedPath = await realpath(item)
      const info = await stat(resolvedPath)
      if (!info.isFile()) throw new Error('not a file')
      if (info.size > limits.maxReferenceBytes) throw new MediaError('REFERENCE_TOO_LARGE', 'A reference image exceeds the configured size limit.')
      const mimeType = sniffImage((await readFile(resolvedPath)).subarray(0, 16))
      if (!mimeType) throw new MediaError('REFERENCE_MIME_INVALID', 'Reference images must be PNG, JPEG, or WebP files.')
      checked.push({ path: resolvedPath, mimeType, size: info.size })
    } catch (error) {
      if (error instanceof MediaError) throw error
      throw new MediaError('REFERENCE_UNREADABLE', 'A reference image cannot be read.')
    }
  }
  return checked
}

export function ensureWithin(parent, child) {
  const relation = relative(resolve(parent), resolve(child))
  return relation !== '' && !relation.startsWith(`..${sep}`) && relation !== '..' && !isAbsolute(relation)
}

export async function ensureNewOutputDirectory(outputDir, cwd = process.cwd()) {
  if (!isAbsolute(outputDir)) throw new MediaError('OUTPUT_DIRECTORY_INVALID', 'output-dir must be absolute.')
  const artifactRoot = resolve(cwd, 'miao-vision', 'artifacts')
  if (!ensureWithin(artifactRoot, outputDir)) throw new MediaError('OUTPUT_DIRECTORY_INVALID', 'output-dir must be a new directory inside ./miao-vision/artifacts/.')
  try {
    const entries = await readdir(outputDir)
    if (entries.length > 0) throw new MediaError('OUTPUT_DIRECTORY_NOT_EMPTY', 'output-dir must not exist or must be empty.')
  } catch (error) {
    if (error?.code !== 'ENOENT') throw error
  }
  return artifactRoot
}

export async function validateGeneratedFiles(payload, outputDir, kind) {
  if (!payload || !Array.isArray(payload.results)) throw new MediaError('AI_CLI_JSON_INVALID', 'ai-cli returned an invalid result object.')
  const artifacts = []
  for (const result of payload.results) {
    if (!result?.success || typeof result.file !== 'string') continue
    const candidate = isAbsolute(result.file) ? resolve(result.file) : resolve(outputDir, result.file)
    if (!ensureWithin(outputDir, candidate)) throw new MediaError('OUTPUT_PATH_ESCAPE', 'ai-cli returned a file outside the output directory.')
    let info
    try { info = await stat(candidate) } catch { throw new MediaError('OUTPUT_FILE_MISSING', 'ai-cli reported a missing output file.') }
    if (!info.isFile() || info.size === 0) throw new MediaError('OUTPUT_FILE_EMPTY', 'ai-cli returned an empty output file.')
    const realCandidate = await realpath(candidate)
    const realOutput = await realpath(outputDir)
    if (!ensureWithin(realOutput, realCandidate)) throw new MediaError('OUTPUT_PATH_ESCAPE', 'ai-cli returned a symlink outside the output directory.')
    const mimeType = sniffMedia((await readFile(realCandidate)).subarray(0, 16), kind)
    if (!mimeType) throw new MediaError('OUTPUT_MIME_INVALID', `ai-cli returned an invalid ${kind} file.`)
    artifacts.push({ path: relative(realOutput, realCandidate), mimeType, size: info.size })
  }
  if (artifacts.length === 0) throw new MediaError('MEDIA_GENERATION_FAILED', 'No valid media files were generated.', true)
  return artifacts
}

export function buildAiArguments(request, config, outputDir, referencePaths = []) {
  const model = selectModel(config, request.kind, request.qualityMode)
  const args = [request.kind, request.prompt, '--json', '--no-preview', '-n', '1', '-m', model, '-o', outputDir]
  if (request.aspectRatio) args.push('--aspect-ratio', request.aspectRatio)
  for (const path of referencePaths) args.push('-i', path)
  if (request.kind === 'video') {
    args.push('--duration', String(request.duration ?? config.video.defaultDurationSeconds), '--resolution', config.video.defaultResolution)
  } else if (request.qualityMode === 'high') {
    args.push('--quality', 'high')
  }
  return { model, args }
}

export async function writeManifest(outputDir, request, runtime, payload, artifacts) {
  const manifest = {
    schemaVersion: 1,
    kind: request.kind,
    status: payload.results.some((result) => !result.success) ? 'partial' : 'succeeded',
    generator: 'ai-cli',
    model: runtime.value.model,
    prompt: request.prompt,
    promptMode: request.promptMode,
    qualityMode: request.qualityMode,
    elapsedMs: payload.elapsed_ms,
    source: request.source,
    createdAt: new Date().toISOString(),
    artifacts,
    warnings: []
  }
  const manifestPath = resolve(outputDir, 'media-generation.json')
  await writeFile(manifestPath, `${JSON.stringify(manifest, null, 2)}\n`, { flag: 'wx' })
  return { path: manifestPath, value: manifest }
}
