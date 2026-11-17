import assert from 'node:assert/strict'
import { spawn } from 'node:child_process'
import { createServer } from 'node:http'
import { mkdtemp, readFile, rm } from 'node:fs/promises'
import { tmpdir } from 'node:os'
import { join, resolve } from 'node:path'
import test from 'node:test'

const root = resolve(import.meta.dirname, '..')
const script = 'scripts/piccc.mjs'
let server
let baseUrl
let deviceTokenRequests = 0
let callbackPageRequest
const requests = []

test.before(async () => {
  server = createServer(async (request, response) => {
    const chunks = []
    for await (const chunk of request) chunks.push(chunk)
    const body = chunks.length ? JSON.parse(Buffer.concat(chunks).toString('utf8')) : null
    requests.push({ method: request.method, url: request.url, body, authorization: request.headers.authorization })
    response.setHeader('Content-Type', 'application/json')

    if (request.url === '/v1/user') return response.end(JSON.stringify({ id: 'user-1', credits: 321.5, membership: { level: 'free', active: true } }))
    if (request.url === '/v1/images/models') return response.end(JSON.stringify({ object: 'list', data: [
      { id: 'image-model', name: 'Image Model', supported_resolutions: ['2K', '0.5K', '1K'], supported_qualities: ['high', 'low', 'medium'] },
      { id: 'special-image', name: '特价图片模型', description: '优惠生成通道', supported_resolutions: ['1K'], supported_qualities: ['standard'] },
    ] }))
    if (request.url === '/v1/videos/models') return response.end(JSON.stringify({ object: 'list', data: [{
      id: 'video-model', name: 'Video Mini', supported_resolutions: ['720p', '480p'], duration: { min: 5, max: 10, step: 1 }, route_modes: ['standard', 'no_real_face'], reference_modes: ['text_to_video'],
    }] }))
    if (request.url === '/v1/audio/models') return response.end(JSON.stringify({ object: 'list', data: [{
      id: 'audio-model', name: 'Audio Model', supported_formats: ['wav', 'mp3'], supported_sample_rates: [48000, 16000, 24000], reference_modes: ['text'], voice_presets: [{ id: 'voice-1', name: '中文女声' }],
    }] }))
    if (request.url === '/v1/images/tasks') return response.end(JSON.stringify({ task_id: 'task-image', status: 'queued' }))
    if (request.url === '/v1/videos/tasks') return response.end(JSON.stringify({ task_id: 'task-video', status: 'queued' }))
    if (request.url === '/v1/audio/tasks') return response.end(JSON.stringify({ task_id: 'task-audio', status: 'queued' }))
    if (request.url === '/v1/tasks/task-image') return response.end(JSON.stringify({ task_id: 'task-image', type: 'image', status: 'completed', progress: 100, outputs: [{ url: `${baseUrl}/files/image.png`, mime_type: 'image/png' }] }))
    if (request.url === '/v1/tasks/task-audio') return response.end(JSON.stringify({ task_id: 'task-audio', type: 'audio', status: 'completed', progress: 100, actual_cost: 7, outputs: [] }))
    if (request.url?.startsWith('/v1/tasks?')) return response.end(JSON.stringify({ items: [{ task_id: 'task-image', type: 'image', status: 'completed' }], page: 1, page_size: 20 }))
    if (request.url === '/api/open-api/device/authorization') {
      const verificationParams = new URLSearchParams({ user_code: 'ABCD-EFGH-JKLM' })
      if (body.redirect_uri) {
        verificationParams.set('redirect_uri', body.redirect_uri)
        const callbackUrl = new URL(body.redirect_uri)
        callbackUrl.searchParams.set('result', 'approved')
        callbackPageRequest = new Promise((resolveCallback) => {
          setTimeout(() => {
            resolveCallback(fetch(callbackUrl, { headers: { 'Accept-Language': 'zh-CN' } }).then((result) => result.text()))
          }, 50)
        })
      }
      return response.end(JSON.stringify({
        device_code: 'device-code',
        user_code: 'ABCD-EFGH-JKLM',
        verification_uri: `${baseUrl}/authorize/device`,
        verification_uri_complete: `${baseUrl}/authorize/device?${verificationParams}`,
        expires_in: 30,
        interval: 0.01,
      }))
    }
    if (request.url === '/api/open-api/device/token') {
      deviceTokenRequests += 1
      if (deviceTokenRequests === 1) {
        response.statusCode = 400
        return response.end(JSON.stringify({ error: 'authorization_pending' }))
      }
      return response.end(JSON.stringify({ token_type: 'Bearer', api_key: 'pcc_live_authorized', key_id: 'ak-authorized', key_prefix: 'pcc_live_authoriz' }))
    }
    if (request.url === '/files/image.png') {
      response.setHeader('Content-Type', 'image/png')
      return response.end(Buffer.from('fake-png'))
    }
    response.statusCode = 404
    response.end(JSON.stringify({ error: { code: 'not_found' } }))
  })
  await new Promise((resolveListen) => server.listen(0, '127.0.0.1', resolveListen))
  const address = server.address()
  baseUrl = `http://127.0.0.1:${address.port}`
})

test.after(async () => {
  await new Promise((resolveClose) => server.close(resolveClose))
})

test('one skill lists image, video, and audio models', async () => {
  const image = await run(['models', 'image'])
  const video = await run(['models', 'video'])
  const audio = await run(['models', 'audio'])
  assert.equal(image.data[0].id, 'image-model')
  assert.equal(video.data[0].id, 'video-model')
  assert.equal(audio.data[0].id, 'audio-model')
  assert.ok(requests.slice(-3).every((item) => item.authorization === 'Bearer test-key'))
})

test('economy model selection includes low-cost defaults and special-offer warning', async () => {
  const result = await run(['models', 'image', '--economy'])
  assert.equal(result.object, 'economy_selection')
  assert.equal(result.model.id, 'special-image')
  assert.equal(result.defaults.resolution, '1K')
  assert.equal(result.defaults.quality, 'standard')
  assert.equal(result.defaults.n, 1)
  assert.equal(result.special_offer, true)
  assert.match(result.warning, /特价模型可能生成较慢、稳定性较差/)
})

test('voice search returns live voice IDs', async () => {
  const result = await run(['voices', '--model', 'audio-model', '--search', '中文'])
  assert.equal(result.data[0].id, 'voice-1')
})

test('image generation waits and downloads output', async () => {
  const directory = await mkdtemp(join(tmpdir(), 'piccc-skills-'))
  try {
    const result = await run(['generate', 'image', '--model', 'image-model', '--prompt', 'a red kite', '--wait', '--output-dir', directory, '--interval', '10'])
    assert.equal(result.status, 'completed')
    assert.equal((await readFile(result.downloads[0], 'utf8')), 'fake-png')
    const submitted = requests.findLast((item) => item.url === '/v1/images/tasks')
    assert.equal(submitted.body.prompt, 'a red kite')
    assert.equal(submitted.body.model, 'image-model')
    assert.equal(submitted.body.resolution, '0.5K')
    assert.equal(submitted.body.quality, 'low')
    assert.equal(submitted.body.n, 1)
    assert.equal(submitted.body.web_search, false)
  } finally {
    await rm(directory, { recursive: true, force: true })
  }
})

test('video generation maps shared CLI options', async () => {
  const result = await run(['generate', 'video', '--model', 'video-model', '--prompt', 'ocean sunset', '--duration', '5', '--aspect-ratio', '16:9'])
  assert.equal(result.task_id, 'task-video')
  const submitted = requests.findLast((item) => item.url === '/v1/videos/tasks')
  assert.equal(submitted.body.duration_seconds, 5)
  assert.equal(submitted.body.aspect_ratio, '16:9')
  assert.equal(submitted.body.resolution, '480p')
  assert.equal(submitted.body.route_mode, 'no_real_face')
  assert.equal(submitted.body.reference_mode, 'text_to_video')
  assert.equal(submitted.body.audio, false)
  assert.equal(submitted.body.web_search, false)
})

test('audio generation marks the initial charge as a precharge', async () => {
  const result = await run(['generate', 'audio', '--model', 'audio-model', '--prompt', 'hello'])
  assert.equal(result.billing.precharge_credits, 10)
  assert.equal(result.billing.final_cost_available_after_completion, true)
  const submitted = requests.findLast((item) => item.url === '/v1/audio/tasks')
  assert.equal(submitted.body.output_format, 'mp3')
  assert.equal(submitted.body.sample_rate, 16000)
  assert.equal(submitted.body.reference_mode, 'text')
})

test('special-offer generation prints a reliability warning', async () => {
  const result = await runRaw(['generate', 'image', '--model', 'special-image', '--prompt', 'draft'])
  assert.equal(result.code, 0)
  assert.match(result.stderr, /特价模型可能生成较慢、稳定性较差/)
})

test('task commands query and filter existing tasks', async () => {
  const task = await run(['task', 'get', 'task-audio'])
  const list = await run(['tasks', '--type', 'image', '--status', 'completed'])
  assert.equal(task.actual_cost, 7)
  assert.equal(list.items[0].task_id, 'task-image')
  const request = requests.findLast((item) => item.url?.startsWith('/v1/tasks?'))
  assert.match(request.url, /type=image/)
  assert.match(request.url, /status=completed/)
})

test('missing credentials point to device authorization', async () => {
  const directory = await mkdtemp(join(tmpdir(), 'piccc-skills-auth-missing-'))
  try {
    const result = await runRaw(['models', 'image'], {
      PICCC_API_KEY: '',
      PICCC_API_BASE_URL: baseUrl,
      PICCC_CREDENTIALS_FILE: join(directory, 'missing.json'),
    })
    assert.notEqual(result.code, 0)
    assert.match(result.stderr, /auth login/)
  } finally {
    await rm(directory, { recursive: true, force: true })
  }
})

test('help works without an API key', async () => {
  const result = await runRaw(['--help'], { PICCC_API_KEY: '', PICCC_API_BASE_URL: '' })
  assert.equal(result.code, 0)
  assert.match(result.stdout, /Piccc AI \(皮可AI\) media task CLI/)
  assert.match(result.stdout, /PICCC_API_KEY/)
})

test('unknown generation options fail before creating a paid task', async () => {
  const requestCount = requests.length
  const result = await runRaw(['generate', 'image', '--model', 'image-model', '--prompt', 'test', '--resoluton', '1K'])
  assert.notEqual(result.code, 0)
  assert.match(result.stderr, /Unknown option: --resoluton/)
  assert.equal(requests.length, requestCount)
})

test('output directory requires waiting for the task', async () => {
  const result = await runRaw(['generate', 'image', '--model', 'image-model', '--prompt', 'test', '--output-dir', 'output'])
  assert.notEqual(result.code, 0)
  assert.match(result.stderr, /--output-dir requires --wait/)
})

test('credits returns the current available balance', async () => {
  const result = await run(['credits'])
  assert.equal(result.available_credits, 321.5)
  const request = requests.findLast((item) => item.url === '/v1/user')
  assert.equal(request.authorization, 'Bearer test-key')
})

test('device authorization saves credentials and uses them automatically', async () => {
  const directory = await mkdtemp(join(tmpdir(), 'piccc-skills-auth-'))
  const credentialsFile = join(directory, 'credentials.json')
  const env = {
    PICCC_API_KEY: '',
    PICCC_API_BASE_URL: baseUrl,
    PICCC_AUTH_BASE_URL: baseUrl,
    PICCC_CREDENTIALS_FILE: credentialsFile,
    PICCC_NO_BROWSER: '1',
  }
  try {
    const login = await runRaw(['auth', 'login', '--client-name', 'Codex test', '--timeout', '5000'], env)
    assert.equal(login.code, 0)
    assert.equal(deviceTokenRequests, 2)
    assert.match(await callbackPageRequest, /授权已完成/)
    assert.doesNotMatch(await callbackPageRequest, /Authorization complete/)
    assert.match(login.stderr, /authorize\/device\?user_code=ABCD-EFGH-JKLM/)
    const authorizationRequest = requests.findLast((item) => item.url === '/api/open-api/device/authorization')
    assert.match(authorizationRequest.body.redirect_uri, /^http:\/\/127\.0\.0\.1:\d+\/piccc-ai\/authorized\?state=/)
    assert.doesNotMatch(`${login.stdout}${login.stderr}`, /pcc_live_authorized/)
    const loginResult = JSON.parse(login.stdout)
    assert.equal(loginResult.authenticated, true)
    assert.equal(loginResult.source, 'credentials_file')
    assert.equal(loginResult.available_credits, 321.5)

    const credentials = JSON.parse(await readFile(credentialsFile, 'utf8'))
    assert.equal(credentials.apiKey, 'pcc_live_authorized')
    const balanceRequest = requests.findLast((item) => item.url === '/v1/user')
    assert.equal(balanceRequest.authorization, 'Bearer pcc_live_authorized')
    const modelsResult = await runRaw(['models', 'image'], env)
    assert.equal(modelsResult.code, 0)
    assert.equal(JSON.parse(modelsResult.stdout).data[0].id, 'image-model')
    const modelRequest = requests.findLast((item) => item.url === '/v1/images/models')
    assert.equal(modelRequest.authorization, 'Bearer pcc_live_authorized')

    const status = await runRaw(['auth', 'status'], env)
    assert.equal(JSON.parse(status.stdout).source, 'credentials_file')
    const logout = await runRaw(['auth', 'logout'], env)
    assert.equal(JSON.parse(logout.stdout).authenticated, false)
    await assert.rejects(readFile(credentialsFile, 'utf8'), { code: 'ENOENT' })
  } finally {
    await rm(directory, { recursive: true, force: true })
  }
})

test('manual authorization remains available without a browser callback', async () => {
  const directory = await mkdtemp(join(tmpdir(), 'piccc-skills-auth-manual-'))
  try {
    const result = await runRaw(['auth', 'login', '--no-browser', '--timeout', '5000'], {
      PICCC_API_KEY: '',
      PICCC_AUTH_BASE_URL: baseUrl,
      PICCC_CREDENTIALS_FILE: join(directory, 'credentials.json'),
    })
    assert.equal(result.code, 0)
    const authorizationRequest = requests.findLast((item) => item.url === '/api/open-api/device/authorization')
    assert.equal(authorizationRequest.body.redirect_uri, undefined)
    assert.doesNotMatch(result.stderr, /redirect_uri=/)
  } finally {
    await rm(directory, { recursive: true, force: true })
  }
})

function run(args) {
  return runRaw(args).then((result) => {
    if (result.code !== 0) throw new Error(`${script} exited ${result.code}: ${result.stderr}`)
    try { return JSON.parse(result.stdout) } catch (error) { throw new Error(`Invalid JSON from ${script}: ${result.stdout}\n${result.stderr}`, { cause: error }) }
  })
}

function runRaw(args, env = {}) {
  return new Promise((resolveRun, rejectRun) => {
    const child = spawn(process.execPath, [resolve(root, script), ...args], {
      env: { ...process.env, PICCC_API_KEY: 'test-key', PICCC_API_BASE_URL: baseUrl, ...env },
      stdio: ['ignore', 'pipe', 'pipe'],
    })
    let stdout = ''
    let stderr = ''
    child.stdout.on('data', (chunk) => { stdout += chunk })
    child.stderr.on('data', (chunk) => { stderr += chunk })
    child.on('error', rejectRun)
    child.on('close', (code) => resolveRun({ code, stdout, stderr }))
  })
}
