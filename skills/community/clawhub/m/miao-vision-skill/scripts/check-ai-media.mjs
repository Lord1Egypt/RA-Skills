#!/usr/bin/env node

import { fail, inspectRuntime } from './ai-media-runtime.mjs'

const kind = process.argv[2]
try {
  if (!['image', 'video'].includes(kind)) throw Object.assign(new Error('Usage: check-ai-media.mjs <image|video> [standard|high]'), { code: 'MEDIA_KIND_INVALID' })
  console.log(JSON.stringify(await inspectRuntime(kind, { qualityMode: process.argv[3] || 'standard' })))
} catch (error) {
  console.log(JSON.stringify(fail(error)))
  process.exitCode = 1
}
