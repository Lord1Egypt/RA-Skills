#!/usr/bin/env node

import { mkdir, readFile } from 'node:fs/promises'
import { isAbsolute, resolve } from 'node:path'
import { pathToFileURL } from 'node:url'
import {
  MediaError, buildAiArguments, ensureNewOutputDirectory, fail, inspectRuntime,
  loadCompatibility, runProcess, validateGeneratedFiles, validateReferences,
  validateRequest, writeManifest
} from './ai-media-runtime.mjs'

export function parseArguments(argv) {
  const options = { confirmRemote: false }
  for (let index = 0; index < argv.length; index += 1) {
    const value = argv[index]
    if (value === '--confirm-remote') options.confirmRemote = true
    else if (value === '--request') options.requestPath = argv[++index]
    else if (value === '--output-dir') options.outputDir = argv[++index]
    else throw new MediaError('ARGUMENT_INVALID', `Unknown argument: ${value}`)
  }
  if (!options.requestPath || !options.outputDir) throw new MediaError('ARGUMENT_MISSING', '--request and --output-dir are required.')
  if (!isAbsolute(options.requestPath) || !isAbsolute(options.outputDir)) throw new MediaError('ARGUMENT_PATH_INVALID', '--request and --output-dir must be absolute paths.')
  return options
}

export async function runMediaGeneration(options, dependencies = {}) {
  if (!options.confirmRemote) throw new MediaError('REMOTE_GENERATION_CONFIRMATION_REQUIRED', 'Remote generation requires explicit confirmation.')
  const cwd = dependencies.cwd || process.cwd()
  const config = dependencies.config || loadCompatibility()
  const request = validateRequest(JSON.parse(await readFile(options.requestPath, 'utf8')), config)
  await ensureNewOutputDirectory(options.outputDir, cwd)
  const references = await validateReferences(request, config)
  const runtime = await (dependencies.inspectRuntime || inspectRuntime)(request.kind, {
    config,
    env: dependencies.env || process.env,
    nodeVersion: dependencies.nodeVersion,
    executable: dependencies.executable,
    runner: dependencies.runner
  })
  await mkdir(options.outputDir, { recursive: true })
  const { model, args } = buildAiArguments(request, config, options.outputDir, references.map((item) => item.path))
  const runner = dependencies.runner || runProcess
  const execution = await runner(runtime.value.executable, args, {
    env: dependencies.env || process.env,
    timeoutMs: config[request.kind].timeoutSeconds * 1000
  })
  if (execution.timedOut) throw new MediaError('AI_CLI_TIMEOUT', 'ai-cli exceeded the configured media timeout.', true)
  let payload
  try { payload = JSON.parse(execution.stdout) } catch { throw new MediaError('AI_CLI_JSON_INVALID', 'ai-cli returned invalid JSON.', true) }
  if (![0, 1, 2].includes(execution.code)) throw new MediaError('AI_CLI_FAILED', 'ai-cli failed before producing a valid result.', true)
  if (execution.code === 1) throw new MediaError('MEDIA_GENERATION_FAILED', 'ai-cli reported that all media jobs failed.', true)
  const artifacts = await validateGeneratedFiles(payload, options.outputDir, request.kind)
  const manifest = await writeManifest(options.outputDir, request, runtime, payload, artifacts)
  return {
    ok: true,
    value: {
      delivery: {
        status: execution.code === 2 ? 'partial' : 'succeeded',
        kind: request.kind,
        model,
        artifacts: artifacts.map((item) => ({ ...item, path: resolve(options.outputDir, item.path) }))
      },
      manifest: manifest.path
    }
  }
}

async function main() {
  try {
    const options = parseArguments(process.argv.slice(2))
    console.log(JSON.stringify(await runMediaGeneration(options)))
  } catch (error) {
    console.log(JSON.stringify(fail(error)))
    process.exitCode = 1
  }
}

if (import.meta.url === pathToFileURL(process.argv[1] || '').href) await main()
