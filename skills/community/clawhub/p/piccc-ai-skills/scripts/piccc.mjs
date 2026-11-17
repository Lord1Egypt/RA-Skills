#!/usr/bin/env node
import { spawn } from 'node:child_process'
import { randomBytes } from 'node:crypto'
import { chmod, mkdir, readFile, rename, rm, writeFile } from 'node:fs/promises'
import { createServer } from 'node:http'
import { homedir } from 'node:os'
import { dirname, extname, join } from 'node:path'

const TERMINAL = new Set(['completed', 'failed', 'cancelled'])
const MODEL_PATHS = {
  image: '/v1/images/models',
  video: '/v1/videos/models',
  audio: '/v1/audio/models',
}
const TASK_PATHS = {
  image: '/v1/images/tasks',
  video: '/v1/videos/tasks',
  audio: '/v1/audio/tasks',
}
const HELP = `Piccc AI (皮可AI) media task CLI

Usage:
  piccc.mjs models image|video|audio [--economy]
  piccc.mjs voices --model ID [--search TEXT]
  piccc.mjs generate image|video|audio --model ID (--prompt TEXT | --prompt-file FILE) [options]
  piccc.mjs task get TASK_ID
  piccc.mjs task wait TASK_ID [--output-dir DIR] [--timeout MS] [--interval MS]
  piccc.mjs tasks [--type TYPE] [--status STATUS] [--page N] [--page-size N]
  piccc.mjs auth login [--client-name NAME] [--timeout MS] [--no-browser]
  piccc.mjs auth status
  piccc.mjs auth logout
  piccc.mjs credits

Generate options:
  --wait                 Wait for a terminal task status
  --output-dir DIR       Download completed outputs (requires --wait)
  --external-id ID       Attach your own task identifier

Run model discovery before generation. See references/api.md for media-specific options.
Authentication: run "piccc.mjs auth login"; use PICCC_API_KEY only when explicitly needed.
`
const { command, positional, options } = parseArgs(process.argv.slice(2))

try {
  if (['', 'help', '--help', '-h'].includes(command) || flag('help')) process.stdout.write(HELP)
  else if (command === 'models') output(await modelsCommand())
  else if (command === 'voices') output(await voices())
  else if (command === 'generate') output(await generateCommand())
  else if (command === 'task') output(await taskCommand())
  else if (command === 'tasks') output(await listTasks())
  else if (command === 'auth') output(await authCommand())
  else if (command === 'credits') output(await creditsCommand())
  else usage()
} catch (error) {
  console.error(error instanceof Error ? error.message : String(error))
  process.exitCode = 1
}

async function models(type) {
  return request(MODEL_PATHS[type])
}

async function authCommand() {
  const action = positional[0]
  if (!['login', 'status', 'logout'].includes(action) || positional.length !== 1) usage()
  validateOptions(action === 'login' ? ['client-name', 'timeout', 'no-browser'] : [])
  if (action === 'login') return login()
  if (action === 'status') return credentialStatus()
  return logout()
}

async function login() {
  const loopback = flag('no-browser') ? null : await startLoopbackCallback().catch(() => null)
  try {
    const started = await authRequest('/api/open-api/device/authorization', {
      method: 'POST',
      body: {
        clientName: option('client-name') || defaultClientName(),
        ...(loopback ? { redirect_uri: loopback.redirectUri } : {}),
      },
    })
    let verificationUrl = String(started.verification_uri_complete || started.verification_uri || '')
    if (!started.device_code || !verificationUrl) throw new Error('Piccc AI (皮可AI) returned an invalid authorization response')
    if (loopback) verificationUrl = withRedirectUri(verificationUrl, loopback.redirectUri)

    const opened = loopback && !environmentFlag('PICCC_NO_BROWSER')
      ? await openBrowser(verificationUrl)
      : false
    console.error(opened ? 'Authorization opened in your browser:' : 'Open this link to authorize Piccc AI (皮可AI):')
    console.error(verificationUrl)
    if (started.user_code) console.error(`Verification code: ${started.user_code}`)
    if (opened) console.error('Complete authorization in the browser. This command will continue automatically.')

    const expiresInMs = Math.max(1, Number(started.expires_in || 600)) * 1000
    const timeout = integerOption('timeout') ?? expiresInMs
    if (timeout <= 0) throw new Error('--timeout must be greater than 0')
    const deadline = Date.now() + Math.min(timeout, expiresInMs)
    let interval = Math.max(250, Number(started.interval || 5) * 1000)
    let callbackCompletion = loopback?.completion || null
    while (Date.now() < deadline) {
      const wake = await waitForAuthorization(interval, callbackCompletion)
      if (wake.source === 'callback') callbackCompletion = null
      try {
        const token = await authRequest('/api/open-api/device/token', {
          method: 'POST',
          body: { device_code: started.device_code },
        })
        if (!token.api_key) throw new Error('Piccc AI (皮可AI) did not return an API key')
        if (callbackCompletion) {
          await Promise.race([callbackCompletion, delay(1500)])
        }
        const saved = await writeCredentials({
          apiKey: token.api_key,
          keyId: token.key_id || '',
          keyPrefix: token.key_prefix || String(token.api_key).slice(0, 16),
          createdAt: new Date().toISOString(),
        })
        let availableCredits = null
        let creditsQueryError = ''
        try {
          availableCredits = await queryAvailableCredits()
        } catch (error) {
          creditsQueryError = error instanceof Error ? error.message : String(error)
        }
        return {
          ok: true,
          authenticated: true,
          source: 'credentials_file',
          key_prefix: token.key_prefix,
          credentials_file: saved,
          available_credits: availableCredits,
          ...(creditsQueryError ? { credits_query_error: creditsQueryError } : {}),
        }
      } catch (error) {
        const code = errorCode(error)
        if (code === 'authorization_pending') continue
        if (code === 'slow_down') {
          interval += 5000
          continue
        }
        if (code === 'access_denied') throw new Error('Authorization was denied')
        if (code === 'expired_token') throw new Error('Authorization expired. Run auth login again')
        throw error
      }
    }
    throw new Error('Authorization timed out. Run auth login again')
  } finally {
    await loopback?.close()
  }
}

async function creditsCommand() {
  validateInvocation(0, [])
  return { available_credits: await queryAvailableCredits() }
}

async function queryAvailableCredits() {
  const account = await request('/v1/user')
  const value = Number(account?.credits)
  if (!Number.isFinite(value)) throw new Error('Piccc AI (皮可AI) did not return a valid available credit balance')
  return value
}

async function credentialStatus() {
  const environmentKey = process.env.PICCC_API_KEY?.trim()
  if (environmentKey) {
    return { authenticated: true, source: 'environment', key_prefix: environmentKey.slice(0, 16) }
  }
  const credentials = await readCredentials()
  if (!credentials?.apiKey) return { authenticated: false, source: null }
  return {
    authenticated: true,
    source: 'credentials_file',
    key_prefix: credentials.keyPrefix || credentials.apiKey.slice(0, 16),
    credentials_file: credentialsPath(),
  }
}

async function logout() {
  await rm(credentialsPath(), { force: true })
  return {
    ok: true,
    authenticated: Boolean(process.env.PICCC_API_KEY?.trim()),
    environment_override: Boolean(process.env.PICCC_API_KEY?.trim()),
  }
}

async function modelsCommand() {
  validateInvocation(1, ['economy'])
  const type = requiredMediaType(positional[0])
  const response = await models(type)
  return flag('economy') ? economySelection(type, response) : response
}

async function voices() {
  validateInvocation(0, ['model', 'search'])
  const modelId = required('model')
  const response = await models('audio')
  const model = (response.data || []).find((item) => item.id === modelId)
  if (!model) throw new Error(`Audio model not found: ${modelId}`)
  const search = String(option('search') || '').toLowerCase()
  const items = (model.voice_presets || []).filter((voice) => !search || JSON.stringify(voice).toLowerCase().includes(search))
  return { object: 'list', model: modelId, data: items }
}

async function generateCommand() {
  if (positional.length !== 1) usage()
  const type = requiredMediaType(positional[0])
  const shared = ['model', 'prompt', 'prompt-file', 'wait', 'output-dir', 'timeout', 'interval', 'external-id']
  const media = {
    image: ['aspect-ratio', 'resolution', 'quality', 'n', 'web-search'],
    video: ['route-mode', 'reference-mode', 'resolution', 'aspect-ratio', 'duration', 'audio', 'web-search'],
    audio: ['format', 'sample-rate', 'speech-rate', 'loudness-rate', 'pitch-rate', 'reference-mode', 'voice-id', 'audio-reference', 'image-reference'],
  }
  validateOptions([...shared, ...media[type]])
  if (option('prompt') && option('prompt-file')) throw new Error('Use either --prompt or --prompt-file, not both')
  if (option('output-dir') && !flag('wait')) throw new Error('--output-dir requires --wait')
  if ((option('timeout') || option('interval')) && !flag('wait')) throw new Error('--timeout and --interval require --wait')
  return generate(type)
}

async function generate(type) {
  const response = await models(type)
  const modelId = required('model')
  const model = (response.data || []).find((item) => item.id === modelId)
  if (!model) throw new Error(`${type} model not found: ${modelId}`)
  const warning = specialOfferWarning(model)
  if (warning) console.error(`[piccc-ai] ${warning}`)
  const body = type === 'image'
    ? await imageBody(model)
    : type === 'video'
      ? await videoBody(model)
      : await audioBody(model)
  const created = await request(TASK_PATHS[type], { method: 'POST', body })
  if (!flag('wait')) {
    return type === 'audio'
      ? { ...created, billing: { precharge_credits: 10, final_cost_available_after_completion: true } }
      : created
  }
  const task = await waitForTask(created.task_id, type === 'video' ? 1200000 : 600000)
  if (task.status !== 'completed') throw new Error(JSON.stringify(task, null, 2))
  const downloads = option('output-dir') ? await downloadOutputs(task, option('output-dir')) : []
  return { ...task, downloads }
}

async function imageBody(model) {
  return compact({
    model: required('model'),
    prompt: await promptValue(),
    aspect_ratio: option('aspect-ratio'),
    resolution: option('resolution') || lowestResolution(model.supported_resolutions),
    quality: option('quality') || lowestQuality(model.supported_qualities),
    n: integerOption('n') ?? 1,
    web_search: booleanOption('web-search') ?? false,
    external_id: option('external-id'),
  })
}

async function videoBody(model) {
  return compact({
    model: required('model'),
    prompt: await promptValue(),
    route_mode: option('route-mode') || preferredChoice(model.route_modes, ['no_real_face', 'standard']),
    reference_mode: option('reference-mode') || preferredChoice(model.reference_modes, ['text_to_video', 'text']),
    resolution: option('resolution') || lowestResolution(model.supported_resolutions),
    aspect_ratio: option('aspect-ratio'),
    duration_seconds: integerOption('duration') ?? positiveInteger(model.duration?.min),
    audio: booleanOption('audio') ?? false,
    web_search: booleanOption('web-search') ?? false,
    external_id: option('external-id'),
  })
}

async function audioBody(model) {
  const audioReference = option('audio-reference')
  const imageReference = option('image-reference')
  return compact({
    model: required('model'),
    prompt: await promptValue(),
    output_format: option('format') || preferredChoice(model.supported_formats, ['mp3', 'ogg_opus', 'aac', 'wav']),
    sample_rate: integerOption('sample-rate') ?? lowestPositiveNumber(model.supported_sample_rates),
    speech_rate: numberOption('speech-rate'),
    loudness_rate: numberOption('loudness-rate'),
    pitch_rate: numberOption('pitch-rate'),
    reference_mode: option('reference-mode') || 'text',
    voice_id: option('voice-id'),
    audio_references: audioReference ? [audioReference] : undefined,
    image_references: imageReference ? [imageReference] : undefined,
    external_id: option('external-id'),
  })
}

function economySelection(type, response) {
  const items = Array.isArray(response?.data) ? response.data : []
  if (!items.length) throw new Error(`No ${type} models are currently available`)
  const model = [...items].sort((left, right) => compareEconomyModels(type, left, right))[0]
  return {
    object: 'economy_selection',
    type,
    model,
    defaults: economyDefaults(type, model),
    special_offer: isSpecialOfferModel(model),
    warning: specialOfferWarning(model),
  }
}

function economyDefaults(type, model) {
  if (type === 'image') {
    return compact({
      resolution: lowestResolution(model.supported_resolutions),
      quality: lowestQuality(model.supported_qualities),
      n: 1,
      web_search: false,
    })
  }
  if (type === 'video') {
    return compact({
      route_mode: preferredChoice(model.route_modes, ['no_real_face', 'standard']),
      reference_mode: preferredChoice(model.reference_modes, ['text_to_video', 'text']),
      resolution: lowestResolution(model.supported_resolutions),
      duration_seconds: positiveInteger(model.duration?.min),
      audio: false,
      web_search: false,
    })
  }
  return compact({
    output_format: preferredChoice(model.supported_formats, ['mp3', 'ogg_opus', 'aac', 'wav']),
    sample_rate: lowestPositiveNumber(model.supported_sample_rates),
    reference_mode: preferredChoice(model.reference_modes, ['text']),
  })
}

function compareEconomyModels(type, left, right) {
  const leftPrice = minimumAdvertisedPrice(left)
  const rightPrice = minimumAdvertisedPrice(right)
  if (leftPrice !== rightPrice) return leftPrice - rightPrice
  const leftTextScore = economyTextScore(left)
  const rightTextScore = economyTextScore(right)
  if (leftTextScore !== rightTextScore) return leftTextScore - rightTextScore
  if (type !== 'audio') {
    const leftResolution = resolutionWeight(lowestResolution(left.supported_resolutions))
    const rightResolution = resolutionWeight(lowestResolution(right.supported_resolutions))
    if (leftResolution !== rightResolution) return leftResolution - rightResolution
  }
  return 0
}

function minimumAdvertisedPrice(model) {
  const direct = [model.minimum_credits, model.estimated_min_credits, model.base_cost]
    .map(Number)
    .filter((value) => Number.isFinite(value) && value >= 0)
  const pricing = model.pricing && typeof model.pricing === 'object' ? model.pricing : {}
  const resolutionPrices = (model.supported_resolutions || [])
    .map((resolution) => Number(pricing[resolution]))
    .filter((value) => Number.isFinite(value) && value >= 0)
  const recurring = [pricing.creditsPerSecond, pricing.baseCreditsPerSecond, pricing.minimumCredits, pricing.taskCredits]
    .map(Number)
    .filter((value) => Number.isFinite(value) && value >= 0)
  const values = [...direct, ...resolutionPrices, ...recurring]
  return values.length ? Math.min(...values) : Number.POSITIVE_INFINITY
}

function economyTextScore(model) {
  const text = `${model.id || ''} ${model.name || ''} ${model.description || ''}`.toLowerCase()
  if (isSpecialOfferModel(model)) return -200
  if (/\b(mini|lite|economy|budget|low[ -]?cost|flash|fast)\b|优惠|经济/.test(text)) return -100
  if (/\b(pro|ultra|premium|quality)\b|旗舰|高质量/.test(text)) return 100
  return 0
}

function isSpecialOfferModel(model) {
  const text = `${model.id || ''} ${model.name || ''} ${model.description || ''}`.toLowerCase()
  return /特价|折扣|限时优惠|special[ -]?(offer|price)?|discount|promo/.test(text)
}

function specialOfferWarning(model) {
  return isSpecialOfferModel(model) ? '特价模型可能生成较慢、稳定性较差。' : ''
}

function lowestResolution(values) {
  const items = Array.isArray(values) ? values.filter(Boolean).map(String) : []
  return [...items].sort((left, right) => resolutionWeight(left) - resolutionWeight(right))[0]
}

function resolutionWeight(value) {
  const text = String(value || '').toLowerCase()
  const k = text.match(/([0-9.]+)\s*k/)
  if (k) return Number(k[1]) * 1000
  const p = text.match(/([0-9.]+)\s*p/)
  if (p) return Number(p[1])
  const dimensions = text.match(/([0-9]+)\s*[x×]\s*([0-9]+)/)
  if (dimensions) return Math.sqrt(Number(dimensions[1]) * Number(dimensions[2]))
  return Number.POSITIVE_INFINITY
}

function lowestQuality(values) {
  return preferredChoice(values, ['draft', 'economy', 'low', 'standard', 'auto', 'medium', 'high', 'hd', 'ultra'])
}

function preferredChoice(values, preferences) {
  const items = Array.isArray(values) ? values.filter(Boolean).map(String) : []
  for (const preference of preferences) {
    const match = items.find((item) => item.toLowerCase() === preference)
    if (match) return match
  }
  return items[0]
}

function lowestPositiveNumber(values) {
  const items = Array.isArray(values) ? values.map(Number).filter((value) => Number.isFinite(value) && value > 0) : []
  return items.length ? Math.min(...items) : undefined
}

function positiveInteger(value) {
  const number = Number(value)
  return Number.isFinite(number) && number > 0 ? Math.trunc(number) : undefined
}

async function taskCommand() {
  const action = positional[0]
  const taskId = positional[1]
  if (!['get', 'wait'].includes(action) || !taskId || positional.length !== 2) usage()
  validateOptions(action === 'wait' ? ['output-dir', 'timeout', 'interval'] : [])
  if (action === 'get') return getTask(taskId)
  const task = await waitForTask(taskId, 1200000)
  const downloads = task.status === 'completed' && option('output-dir') ? await downloadOutputs(task, option('output-dir')) : []
  return { ...task, downloads }
}

async function getTask(taskId) {
  return request(`/v1/tasks/${encodeURIComponent(taskId)}`)
}

async function waitForTask(taskId, defaultTimeout) {
  const timeout = integerOption('timeout') ?? defaultTimeout
  const interval = integerOption('interval') ?? 3000
  if (timeout <= 0) throw new Error('--timeout must be greater than 0')
  if (interval <= 0) throw new Error('--interval must be greater than 0')
  const deadline = Date.now() + timeout
  while (true) {
    const task = await getTask(taskId)
    console.error(`[piccc-ai] ${task.status} ${task.progress ?? 0}%`)
    if (TERMINAL.has(task.status)) return task
    if (Date.now() >= deadline) return { ...task, timed_out: true }
    await new Promise((resolve) => setTimeout(resolve, Math.max(500, interval)))
  }
}

async function listTasks() {
  validateInvocation(0, ['type', 'status', 'page', 'page-size'])
  const query = new URLSearchParams()
  for (const [optionName, queryName] of [['type', 'type'], ['status', 'status'], ['page', 'page'], ['page-size', 'page_size']]) {
    if (option(optionName)) query.set(queryName, option(optionName))
  }
  return request(`/v1/tasks${query.size ? `?${query}` : ''}`)
}

async function downloadOutputs(task, directory) {
  await mkdir(directory, { recursive: true })
  const files = []
  for (const [index, item] of (task.outputs || []).entries()) {
    if (!item?.url) continue
    const response = await fetch(item.url)
    if (!response.ok) throw new Error(`Download failed: HTTP ${response.status}`)
    const extension = extensionFor(item, response.headers.get('content-type'))
    const path = join(directory, `${safeName(task.task_id)}-${index + 1}${extension}`)
    await writeFile(path, Buffer.from(await response.arrayBuffer()))
    files.push(path)
  }
  return files
}

function extensionFor(item, contentType = '') {
  try {
    const value = extname(new URL(item.url).pathname)
    if (/^\.[a-z0-9]{1,8}$/i.test(value)) return value
  } catch {}
  const mime = String(item.mime_type || contentType).toLowerCase()
  if (mime.includes('jpeg')) return '.jpg'
  if (mime.includes('png')) return '.png'
  if (mime.includes('webp')) return '.webp'
  if (mime.includes('webm')) return '.webm'
  if (mime.includes('video')) return '.mp4'
  if (mime.includes('mpeg')) return mime.startsWith('audio') ? '.mp3' : '.mp4'
  if (mime.includes('ogg')) return '.ogg'
  if (mime.includes('flac')) return '.flac'
  if (mime.includes('audio')) return '.wav'
  return '.bin'
}

async function promptValue() {
  if (option('prompt-file')) return (await readFile(option('prompt-file'), 'utf8')).trim()
  return required('prompt')
}

async function request(path, init = {}) {
  const key = await resolveApiKey()
  if (!key) throw new Error('Piccc AI (皮可AI) is not authorized. Run: node scripts/piccc.mjs auth login')
  const base = (process.env.PICCC_API_BASE_URL || 'https://api.picccai.cn').replace(/\/+$/, '')
  return fetchJson(`${base}${path}`, {
    method: init.method || 'GET',
    headers: { Authorization: `Bearer ${key}`, Accept: 'application/json', ...(init.body ? { 'Content-Type': 'application/json' } : {}) },
    body: init.body ? JSON.stringify(init.body) : undefined,
  })
}

async function authRequest(path, init = {}) {
  const base = (process.env.PICCC_AUTH_BASE_URL || 'https://picccai.cn').replace(/\/+$/, '')
  return fetchJson(`${base}${path}`, {
    method: init.method || 'GET',
    headers: { Accept: 'application/json', ...(init.body ? { 'Content-Type': 'application/json' } : {}) },
    body: init.body ? JSON.stringify(init.body) : undefined,
  })
}

async function startLoopbackCallback() {
  const state = randomBytes(24).toString('base64url')
  let resolveCompletion
  let completed = false
  const completion = new Promise((resolve) => { resolveCompletion = resolve })
  const server = createServer((request, response) => {
    let url
    try {
      url = new URL(request.url || '/', 'http://127.0.0.1')
    } catch {
      response.writeHead(400).end()
      return
    }
    if (url.pathname !== '/piccc-ai/authorized' || url.searchParams.get('state') !== state) {
      response.writeHead(404).end()
      return
    }
    const result = url.searchParams.get('result') || ''
    if (!['approved', 'denied', 'expired'].includes(result)) {
      response.writeHead(400).end()
      return
    }
    response.writeHead(200, {
      'Cache-Control': 'no-store',
      'Content-Type': 'text/html; charset=utf-8',
      'Content-Security-Policy': "default-src 'none'; style-src 'unsafe-inline'",
      'X-Content-Type-Options': 'nosniff',
    })
    response.end(loopbackResultHtml(result, request.headers['accept-language']))
    if (!completed) {
      completed = true
      resolveCompletion(result)
    }
  })

  await new Promise((resolve, reject) => {
    const handleError = (error) => reject(error)
    server.once('error', handleError)
    server.listen(0, '127.0.0.1', () => {
      server.off('error', handleError)
      resolve()
    })
  })
  server.on('error', () => undefined)
  const address = server.address()
  if (!address || typeof address === 'string') {
    await new Promise((resolve) => server.close(resolve))
    throw new Error('Could not start the local authorization callback')
  }

  return {
    redirectUri: `http://127.0.0.1:${address.port}/piccc-ai/authorized?state=${encodeURIComponent(state)}`,
    completion,
    close: () => new Promise((resolve) => {
      if (!server.listening) return resolve()
      server.close(() => resolve())
    }),
  }
}

function loopbackResultHtml(result, acceptLanguage = '') {
  const approved = result === 'approved'
  const chinese = /^zh(?:-|,|;|$)/i.test(String(acceptLanguage))
  const title = chinese
    ? approved ? '授权已完成' : '授权未完成'
    : approved ? 'Authorization complete' : 'Authorization not completed'
  const description = chinese
    ? approved ? '可以关闭此页面并返回智能体。' : '可以关闭此页面并返回智能体重试。'
    : approved ? 'You can close this page and return to the agent.' : 'You can close this page and try again from the agent.'
  const color = approved ? '#16a34a' : '#d97706'
  return `<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>${title}</title>
  <style>
    :root{color-scheme:light dark;font-family:Inter,ui-sans-serif,system-ui,sans-serif}
    body{min-height:100vh;margin:0;display:grid;place-items:center;background:#fafafa;color:#18181b}
    main{width:min(28rem,calc(100% - 2rem));box-sizing:border-box;padding:2rem;border:1px solid #e4e4e7;border-radius:.75rem;background:#fff;text-align:center;box-shadow:0 8px 24px rgba(15,23,42,.08)}
    span{display:grid;place-items:center;width:3rem;height:3rem;margin:0 auto 1rem;border-radius:999px;background:color-mix(in srgb,${color} 12%,transparent);color:${color};font-size:1.5rem}
    h1{margin:0;font-size:1.125rem}p{margin:.75rem 0 0;color:#64748b;line-height:1.65;font-size:.875rem}
    @media(prefers-color-scheme:dark){body{background:#09090b;color:#fafafa}main{background:#0f0f12;border-color:#27272a}p{color:#a1a1aa}}
  </style>
</head>
<body><main><span aria-hidden="true">${approved ? '✓' : '!'}</span><h1>${title}</h1><p>${description}</p></main></body>
</html>`
}

function withRedirectUri(verificationUrl, redirectUri) {
  try {
    const url = new URL(verificationUrl)
    if (!url.searchParams.has('redirect_uri')) url.searchParams.set('redirect_uri', redirectUri)
    return url.toString()
  } catch {
    return verificationUrl
  }
}

async function waitForAuthorization(milliseconds, callbackCompletion) {
  if (!callbackCompletion) {
    await delay(milliseconds)
    return { source: 'timer' }
  }
  return Promise.race([
    delay(milliseconds).then(() => ({ source: 'timer' })),
    callbackCompletion.then((result) => ({ source: 'callback', result })),
  ])
}

function environmentFlag(name) {
  return ['1', 'true', 'yes', 'on'].includes(String(process.env[name] || '').trim().toLowerCase())
}

async function openBrowser(url) {
  try {
    const parsed = new URL(url)
    if (!['http:', 'https:'].includes(parsed.protocol)) return false
    const command = process.platform === 'win32'
      ? 'rundll32.exe'
      : process.platform === 'darwin'
        ? 'open'
        : 'xdg-open'
    const args = process.platform === 'win32' ? ['url.dll,FileProtocolHandler', parsed.toString()] : [parsed.toString()]
    const child = spawn(command, args, { detached: true, stdio: 'ignore', windowsHide: true })
    return await new Promise((resolve) => {
      let settled = false
      const finish = (opened) => {
        if (settled) return
        settled = true
        if (opened) child.unref()
        resolve(opened)
      }
      child.once('spawn', () => finish(true))
      child.once('error', () => finish(false))
    })
  } catch {
    return false
  }
}

async function fetchJson(url, init) {
  const response = await fetch(url, init)
  const text = await response.text()
  let data
  try { data = text ? JSON.parse(text) : null } catch { data = text }
  if (!response.ok) {
    const code = typeof data === 'object' && data ? String(data.statusMessage || data.error || data.message || '') : ''
    const error = new Error(`Piccc AI (皮可AI) API ${response.status}: ${typeof data === 'string' ? data : JSON.stringify(data)}`)
    error.code = code
    error.status = response.status
    throw error
  }
  return data
}

function credentialsPath() {
  return process.env.PICCC_CREDENTIALS_FILE || join(homedir(), '.piccc-ai', 'credentials.json')
}

async function readCredentials() {
  try {
    const parsed = JSON.parse(await readFile(credentialsPath(), 'utf8'))
    return parsed && typeof parsed === 'object' ? parsed : null
  } catch (error) {
    if (error?.code === 'ENOENT' || error instanceof SyntaxError) return null
    throw error
  }
}

async function writeCredentials(credentials) {
  const path = credentialsPath()
  const directory = dirname(path)
  const temporary = `${path}.${process.pid}.tmp`
  await mkdir(directory, { recursive: true, mode: 0o700 })
  await writeFile(temporary, `${JSON.stringify(credentials, null, 2)}\n`, { encoding: 'utf8', mode: 0o600 })
  await rename(temporary, path)
  await chmod(path, 0o600).catch(() => undefined)
  return path
}

async function resolveApiKey() {
  const environmentKey = process.env.PICCC_API_KEY?.trim()
  if (environmentKey) return environmentKey
  const credentials = await readCredentials()
  return String(credentials?.apiKey || '').trim()
}

function defaultClientName() {
  return `Piccc AI (皮可AI) Skill (${process.platform})`
}

function errorCode(error) {
  return error && typeof error === 'object' ? String(error.code || '') : ''
}

function delay(milliseconds) {
  return new Promise((resolve) => setTimeout(resolve, milliseconds))
}

function parseArgs(args) {
  const command = args.shift() || ''
  const positional = []
  const options = {}
  for (let index = 0; index < args.length; index++) {
    const token = args[index]
    if (!token.startsWith('--')) { positional.push(token); continue }
    const key = token.slice(2)
    const next = args[index + 1]
    options[key] = next && !next.startsWith('--') ? args[++index] : true
  }
  return { command, positional, options }
}

function validateInvocation(positionalCount, allowedOptions) {
  if (positional.length !== positionalCount) usage()
  validateOptions(allowedOptions)
}

function validateOptions(allowed) {
  const accepted = new Set(allowed)
  for (const name of Object.keys(options)) {
    if (!accepted.has(name)) throw new Error(`Unknown option: --${name}`)
  }
}

function requiredMediaType(value) {
  if (!MODEL_PATHS[value]) throw new Error('Media type must be image, video, or audio')
  return value
}
function option(name) { return options[name] === true ? undefined : options[name] }
function required(name) { const value = option(name); if (!value) throw new Error(`--${name} is required`); return value }
function flag(name) { return options[name] === true || options[name] === 'true' }
function integerOption(name) { const value = option(name); if (value == null) return undefined; const number = Number(value); if (!Number.isInteger(number)) throw new Error(`--${name} must be an integer`); return number }
function numberOption(name) { const value = option(name); if (value == null) return undefined; const number = Number(value); if (!Number.isFinite(number)) throw new Error(`--${name} must be a number`); return number }
function booleanOption(name) { return options[name] == null ? undefined : flag(name) }
function compact(value) { return Object.fromEntries(Object.entries(value).filter(([, item]) => item !== undefined && item !== '')) }
function safeName(value) { return String(value || 'piccc-output').replace(/[^a-z0-9_.-]+/gi, '_') }
function output(value) { process.stdout.write(`${JSON.stringify(value, null, 2)}\n`) }
function usage() { throw new Error('Usage: piccc.mjs models TYPE | voices --model ID | generate TYPE --model ID (--prompt TEXT | --prompt-file FILE) | task get|wait TASK_ID | tasks [filters] | auth login|status|logout | credits') }
