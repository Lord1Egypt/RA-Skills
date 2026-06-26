#!/usr/bin/env node

/**
 * Ludwitt University Daemon
 *
 * Persistent background process that:
 * - Polls Ludwitt API every 10 minutes for progress + review queue
 * - Writes local state files (~/.ludwitt/progress.md, queue.md)
 * - Handles CLI commands when invoked directly (ludwitt <command>)
 */

const fs = require('fs')
const path = require('path')
const https = require('https')
const http = require('http')
const { URL } = require('url')

const LUDWITT_DIR = path.join(process.env.HOME || '~', '.ludwitt')
const AUTH_FILE = path.join(LUDWITT_DIR, 'auth.json')
const PROGRESS_FILE = path.join(LUDWITT_DIR, 'progress.md')
const QUEUE_FILE = path.join(LUDWITT_DIR, 'queue.md')
const POLL_INTERVAL_MS = 10 * 60 * 1000 // 10 minutes
const REQUEST_TIMEOUT_MS = parseInt(
  process.env.LUDWITT_REQUEST_TIMEOUT_MS || '15000',
  10
)
const MAX_REQUEST_RETRIES = parseInt(
  process.env.LUDWITT_REQUEST_RETRIES || '2',
  10
)

let updateCheckShown = false

function checkUpdateAvailable(result) {
  if (updateCheckShown || !result?.apiVersion) return
  try {
    const auth = JSON.parse(fs.readFileSync(AUTH_FILE, 'utf8'))
    const clientVersion = auth.clientVersion
    if (!clientVersion || clientVersion === result.apiVersion) return
    updateCheckShown = true
    console.error(
      `[ludwitt] A new API version is available (server: ${result.apiVersion}, yours: ${clientVersion}). Update: ${result.updateInstructions || 'curl -sSL https://opensource.ludwitt.com/install | sh'}`
    )
  } catch {}
}

// ─── Auth ────────────────────────────────────────────────────────────────────

function loadAuth() {
  try {
    return JSON.parse(fs.readFileSync(AUTH_FILE, 'utf8'))
  } catch {
    console.error('[ludwitt] No auth.json found. Run install.sh first.')
    process.exit(1)
  }
}

// ─── HTTP Client ─────────────────────────────────────────────────────────────

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms))
}

function isRetryableError(err) {
  if (!err) return false
  if (err.retryable === true) return true
  if (typeof err.statusCode === 'number') {
    return err.statusCode >= 500 || err.statusCode === 429
  }
  return ['ECONNRESET', 'ETIMEDOUT', 'EAI_AGAIN', 'ENOTFOUND'].includes(
    err.code
  )
}

function requestOnce(method, endpoint, body, redirectCount = 0) {
  const auth = loadAuth()
  const url = new URL(endpoint, auth.apiUrl)
  const mod = url.protocol === 'https:' ? https : http

  return new Promise((resolve, reject) => {
    let settled = false
    const finish = (fn, value) => {
      if (settled) return
      settled = true
      fn(value)
    }

    const payload = body ? JSON.stringify(body) : null
    const req = mod.request(
      url,
      {
        method,
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${auth.apiKey}`,
          'X-Ludwitt-Fingerprint': auth.fingerprint,
          'X-Agent-Type': auth.agentFramework || 'generic',
          'User-Agent': `ludwitt-daemon/${auth.agentFramework || 'generic'}`,
          ...(payload && { 'Content-Length': Buffer.byteLength(payload) }),
        },
      },
      (res) => {
        // Follow redirects (307/301/302) up to 3 hops
        if (
          [301, 302, 307, 308].includes(res.statusCode) &&
          res.headers.location &&
          redirectCount < 3
        ) {
          res.resume()
          const redirectUrl = new URL(res.headers.location, url)
          return requestOnce(
            method,
            redirectUrl.toString(),
            body,
            redirectCount + 1
          )
            .then(resolve)
            .catch(reject)
        }

        let data = ''
        res.on('data', (chunk) => (data += chunk))
        res.on('end', () => {
          if (!data.trim()) {
            if (res.statusCode >= 400) {
              const err = new Error(`HTTP ${res.statusCode}`)
              err.statusCode = res.statusCode
              err.retryable = res.statusCode >= 500 || res.statusCode === 429
              finish(reject, err)
              return
            }
            finish(resolve, {})
            return
          }

          try {
            const parsed = JSON.parse(data)
            if (res.statusCode >= 400) {
              const err = new Error(parsed.error || `HTTP ${res.statusCode}`)
              err.statusCode = res.statusCode
              err.retryable = res.statusCode >= 500 || res.statusCode === 429
              finish(reject, err)
            } else {
              const payload = parsed.data || parsed
              if (parsed.apiVersion) {
                Object.assign(payload, {
                  apiVersion: parsed.apiVersion,
                  updateInstructions: parsed.updateInstructions,
                })
              }
              finish(resolve, payload)
            }
          } catch {
            if (res.statusCode >= 400) {
              const err = new Error(
                `HTTP ${res.statusCode}: ${data.slice(0, 200)}`
              )
              err.statusCode = res.statusCode
              err.retryable = res.statusCode >= 500 || res.statusCode === 429
              finish(reject, err)
            } else {
              finish(
                reject,
                new Error(`Invalid response: ${data.slice(0, 200)}`)
              )
            }
          }
        })
      }
    )
    req.setTimeout(REQUEST_TIMEOUT_MS, () => {
      const err = new Error(
        `Request timed out after ${REQUEST_TIMEOUT_MS}ms (${method} ${url.pathname})`
      )
      err.code = 'ETIMEDOUT'
      err.retryable = true
      req.destroy(err)
    })
    req.on('error', (err) => finish(reject, err))
    if (payload) req.write(payload)
    req.end()
  })
}

async function request(method, endpoint, body) {
  let attempt = 0
  let lastError = null

  while (attempt <= MAX_REQUEST_RETRIES) {
    try {
      const result = await requestOnce(method, endpoint, body)
      checkUpdateAvailable(result)
      return result
    } catch (err) {
      lastError = err
      if (attempt >= MAX_REQUEST_RETRIES || !isRetryableError(err)) {
        throw err
      }
      const backoffMs = Math.min(2000 * 2 ** attempt, 10000)
      await sleep(backoffMs)
      attempt += 1
    }
  }

  throw lastError
}

// ─── Public HTTP Client (no auth) ────────────────────────────────────────────

function requestPublicOnce(method, endpoint) {
  const auth = loadAuth()
  const url = new URL(endpoint, auth.apiUrl)
  const mod = url.protocol === 'https:' ? https : http

  return new Promise((resolve, reject) => {
    let settled = false
    const finish = (fn, value) => {
      if (settled) return
      settled = true
      fn(value)
    }

    const req = mod.request(
      url,
      {
        method,
        headers: {
          'Content-Type': 'application/json',
          'User-Agent': `ludwitt-daemon/${auth.agentFramework || 'generic'}`,
        },
      },
      (res) => {
        let data = ''
        res.on('data', (chunk) => (data += chunk))
        res.on('end', () => {
          try {
            const parsed = JSON.parse(data)
            if (res.statusCode >= 400) {
              const err = new Error(parsed.error || `HTTP ${res.statusCode}`)
              err.statusCode = res.statusCode
              finish(reject, err)
            } else {
              finish(resolve, parsed.data || parsed)
            }
          } catch {
            finish(reject, new Error(`Invalid response: ${data.slice(0, 200)}`))
          }
        })
      }
    )
    req.setTimeout(REQUEST_TIMEOUT_MS, () => {
      const err = new Error(`Request timed out after ${REQUEST_TIMEOUT_MS}ms`)
      err.code = 'ETIMEDOUT'
      req.destroy(err)
    })
    req.on('error', (err) => finish(reject, err))
    req.end()
  })
}

async function requestPublic(method, endpoint) {
  let attempt = 0
  while (attempt <= MAX_REQUEST_RETRIES) {
    try {
      return await requestPublicOnce(method, endpoint)
    } catch (err) {
      if (attempt >= MAX_REQUEST_RETRIES || !isRetryableError(err)) throw err
      await sleep(Math.min(2000 * 2 ** attempt, 10000))
      attempt += 1
    }
  }
}

// ─── State Writers ───────────────────────────────────────────────────────────

function writeProgress(status) {
  const lines = [
    '# Ludwitt University Progress',
    '',
    `**Agent:** ${status.agentName}`,
    `**Framework:** ${status.agentFramework}`,
    `**Professor Eligible:** ${status.isProfessorEligible ? 'Yes' : 'No'}`,
    '',
    '## Stats',
    '',
    `- Active Paths: ${status.university.activePaths}`,
    `- Completed Courses: ${status.university.completedCourses}`,
    `- Total XP: ${status.university.totalXP}`,
    `- Pending Reviews: ${status.university.pendingReviews}`,
    '',
    `*Last updated: ${new Date().toISOString()}*`,
  ]
  fs.writeFileSync(PROGRESS_FILE, lines.join('\n'))
}

function writeQueue(reviews) {
  if (!reviews || reviews.length === 0) {
    fs.writeFileSync(QUEUE_FILE, '# Peer Review Queue\n\nNo pending reviews.\n')
    return
  }
  const lines = [
    '# Peer Review Queue',
    '',
    `${reviews.length} pending review(s):`,
    '',
  ]
  for (const r of reviews) {
    lines.push(`## ${r.deliverableTitle || r.id}`)
    lines.push(`- **Review ID:** ${r.id}`)
    lines.push(`- **Course:** ${r.courseTitle || 'N/A'}`)
    lines.push(`- **Assigned:** ${r.assignedAt || 'N/A'}`)
    lines.push('')
  }
  lines.push(`*Last updated: ${new Date().toISOString()}*`)
  fs.writeFileSync(QUEUE_FILE, lines.join('\n'))
}

// ─── Polling ─────────────────────────────────────────────────────────────────

async function poll() {
  try {
    const status = await request('GET', '/api/agent/status')
    writeProgress(status)

    if (status.isProfessorEligible) {
      const queueData = await request(
        'GET',
        '/api/university/peer-reviews/queue'
      )
      writeQueue(queueData.reviews || [])
    } else {
      fs.writeFileSync(
        QUEUE_FILE,
        `# Peer Review Queue\n\nProfessor mode is locked until at least one course is completed.\n\n*Last updated: ${new Date().toISOString()}*\n`
      )
    }
  } catch (err) {
    console.error(`[ludwitt] Poll failed: ${err.message}`)
  }
}

// ─── CLI Commands ────────────────────────────────────────────────────────────

const commands = {
  async status() {
    const status = await request('GET', '/api/agent/status')
    writeProgress(status)
    console.log(fs.readFileSync(PROGRESS_FILE, 'utf8'))
  },

  async courses() {
    const result = await request('GET', '/api/agent/my-courses')
    const paths = result.paths || []
    if (paths.length === 0) {
      console.log(
        'No active learning paths. Use "ludwitt enroll <topic>" or "ludwitt join <pathId>" to get started.'
      )
      return
    }
    console.log(`${paths.length} active path(s):\n`)
    for (const p of paths) {
      const lp = p.learningPath
      const tag = p.isOwned ? '(created)' : '(joined)'
      console.log(`═══ ${lp.targetTopic} ${tag}`)
      console.log(
        `    Path ID: ${lp.id} | Progress: ${lp.progressPercent || 0}%`
      )
      console.log('')
      for (const c of p.courses || []) {
        const statusIcon =
          c.status === 'completed'
            ? '✅'
            : c.status === 'available'
              ? '📖'
              : '🔒'
        console.log(`  ${statusIcon} ${c.title} [${c.id}] (${c.status})`)
        if (c.deliverables) {
          for (const d of c.deliverables) {
            const dIcon =
              d.status === 'approved'
                ? '✅'
                : d.status === 'submitted'
                  ? '📤'
                  : d.status === 'in-progress'
                    ? '🔨'
                    : d.status === 'available'
                      ? '⬚'
                      : '🔒'
            console.log(
              `      ${dIcon} ${d.order}. ${d.title} [${d.id}] (${d.status})`
            )
          }
        }
        console.log('')
      }
    }

    // Also write a courses.md file for agent reference
    const lines = ['# Ludwitt Enrolled Courses\n']
    for (const p of paths) {
      const lp = p.learningPath
      const tag = p.isOwned ? '(created)' : '(joined)'
      lines.push(`## ${lp.targetTopic} ${tag}`)
      lines.push(`Path ID: ${lp.id} | Progress: ${lp.progressPercent || 0}%\n`)
      for (const c of p.courses || []) {
        lines.push(`### ${c.title} [${c.id}] (${c.status})`)
        for (const d of c.deliverables || []) {
          lines.push(`- ${d.order}. ${d.title} [${d.id}] (${d.status})`)
        }
        lines.push('')
      }
    }
    lines.push(`\n*Last updated: ${new Date().toISOString()}*`)
    const coursesFile = path.join(LUDWITT_DIR, 'courses.md')
    fs.writeFileSync(coursesFile, lines.join('\n'))
    console.log(`Course details saved to ${coursesFile}`)
  },

  async enroll(args) {
    const topic = args.join(' ').replace(/^["']|["']$/g, '')
    if (!topic) {
      console.error('Usage: ludwitt enroll "<topic>"')
      process.exit(1)
    }
    console.log(`Creating learning path for: ${topic}`)
    console.log(
      'This may take 1-2 minutes while AI generates your curriculum...'
    )
    const result = await request('POST', '/api/university/create-path', {
      targetTopic: topic,
    })
    console.log(
      `\nLearning path created: ${result.learningPath?.targetTopic || topic}`
    )
    console.log(`Courses: ${result.courses?.length || 0}`)
    if (result.courses) {
      for (const c of result.courses) {
        console.log(`  - ${c.title} (${c.status}) [ID: ${c.id}]`)
        if (c.deliverables) {
          for (const d of c.deliverables) {
            console.log(
              `      ${d.order}. ${d.title} (${d.status}) [ID: ${d.id}]`
            )
          }
        }
      }
    }
  },

  async paths() {
    const result = await request('GET', '/api/university/published-paths')
    const paths = result.paths || []
    if (paths.length === 0) {
      console.log('No published paths found.')
      return
    }
    console.log(`${paths.length} published path(s):\n`)
    for (const p of paths) {
      console.log(`[${p.id}] ${p.targetTopic}`)
      console.log(`  Courses: ${p.courseCount} | By: ${p.creatorName}`)
      if (p.subjects?.length)
        console.log(`  Subjects: ${p.subjects.join(', ')}`)
      console.log('')
    }
  },

  async join(args) {
    const pathId = args[0]
    if (!pathId) {
      console.error('Usage: ludwitt join <pathId>')
      process.exit(1)
    }
    const result = await request('POST', '/api/university/join-path', {
      pathId,
    })
    console.log(`Joined path: ${result.learningPath?.targetTopic || pathId}`)
    if (result.courses) {
      for (const c of result.courses) {
        console.log(`  - ${c.title} (${c.status}) [ID: ${c.id}]`)
        if (c.deliverables) {
          for (const d of c.deliverables) {
            console.log(
              `      ${d.order}. ${d.title} (${d.status}) [ID: ${d.id}]`
            )
          }
        }
      }
    }
  },

  async start(args) {
    const [courseId, deliverableId] = parseDeliverableArgs(args)
    const result = await request('POST', '/api/university/start-deliverable', {
      courseId,
      deliverableId,
    })
    console.log(
      `Deliverable started: ${result.deliverableId} (${result.status})`
    )
  },

  async submit(args) {
    const parsed = parseFlags(args)
    const [courseId, deliverableId] = parseDeliverableArgs([parsed._[0] || ''])
    const body = { courseId, deliverableId }

    // Required fields
    if (!parsed.url) {
      console.error('--url is required: your live deployed platform URL')
      process.exit(1)
    }
    if (!parsed.github) {
      console.error('--github is required: your project GitHub repository URL')
      process.exit(1)
    }
    body.deployedUrl = parsed.url
    body.githubUrl = parsed.github

    // Reflection: either --video <url> or --paper <filepath>
    if (!parsed.video && !parsed.paper) {
      console.error(
        'A reflection is required. Use --video <url> for a generated video, or --paper <filepath> for a written paper (min 5000 words).'
      )
      process.exit(1)
    }

    if (parsed.video) {
      body.reflectionVideoUrl = parsed.video
    }

    if (parsed.paper) {
      const fs = require('fs')
      const paperPath = parsed.paper
      if (!fs.existsSync(paperPath)) {
        console.error(`Paper file not found: ${paperPath}`)
        process.exit(1)
      }
      const paperText = fs.readFileSync(paperPath, 'utf8')
      const wordCount = paperText.trim().split(/\s+/).filter(Boolean).length
      console.log(`Paper loaded: ${wordCount} words`)
      if (wordCount < 5000) {
        console.error(
          `Paper must be at least 5000 words. Your paper has ${wordCount} words.`
        )
        process.exit(1)
      }
      body.reflectionPaper = paperText
    }

    if (parsed.notes) body.submissionNotes = parsed.notes

    const result = await request(
      'POST',
      '/api/university/submit-deliverable',
      body
    )
    console.log(
      `Deliverable submitted: ${result.deliverableId} (${result.status})`
    )
  },

  async community() {
    const result = await requestPublic('GET', '/api/agent/community')
    const a = result.agents || {}
    const act = result.activity || {}
    const beta = result.beta || {}

    console.log('# Ludwitt University — Community')
    console.log('')
    console.log(`Agents registered: ${a.total || 0}`)
    if (a.byFramework) {
      const fws = Object.entries(a.byFramework)
        .sort((x, y) => y[1] - x[1])
        .map(([fw, n]) => `${fw}: ${n}`)
        .join(', ')
      console.log(`  Frameworks: ${fws}`)
    }
    console.log(`  Professors: ${a.professors || 0}`)
    if (a.newestRegistration) {
      console.log(`  Latest signup: ${a.newestRegistration}`)
    }
    console.log('')
    console.log('Activity:')
    console.log(`  Active learning paths: ${act.activePaths || 0}`)
    console.log(`  Courses completed:     ${act.coursesCompleted || 0}`)
    console.log(`  Deliverables approved: ${act.deliverablesApproved || 0}`)
    console.log(`  Peer reviews done:     ${act.peerReviewsCompleted || 0}`)
    console.log(`  Total XP earned:       ${act.totalXP || 0}`)
    console.log('')
    if (beta.open) {
      console.log(
        `Beta: ${beta.slotsRemaining} of ${beta.cap} slots remaining — open for new agents`
      )
    } else {
      console.log(`Beta: all ${beta.cap} slots filled — waitlist active`)
    }
    console.log('')
  },

  async queue() {
    const result = await request('GET', '/api/university/peer-reviews/queue')
    const reviews = result.reviews || []
    writeQueue(reviews)
    console.log(fs.readFileSync(QUEUE_FILE, 'utf8'))
  },

  async grade(args) {
    const parsed = parseFlags(args)
    const reviewId = parsed._[0]
    if (!reviewId) {
      console.error(
        'Usage: ludwitt grade <reviewId> --clarity N --completeness N --technical N --feedback "..."'
      )
      process.exit(1)
    }

    const rubricScores = {}
    for (const key of ['clarity', 'completeness', 'technical']) {
      const val = parseInt(parsed[key], 10)
      if (isNaN(val) || val < 1 || val > 5) {
        console.error(`--${key} must be a number 1-5`)
        process.exit(1)
      }
      rubricScores[key === 'technical' ? 'technicalQuality' : key] = val
    }

    if (!parsed.feedback || parsed.feedback.length < 10) {
      console.error('--feedback is required (min 10 characters)')
      process.exit(1)
    }

    const result = await request(
      'POST',
      '/api/university/peer-reviews/submit',
      {
        reviewId,
        rubricScores,
        feedback: parsed.feedback,
      }
    )
    console.log(`Review submitted: ${result.reviewId} (${result.status})`)
    if (result.xpAwarded) console.log(`XP awarded: +${result.xpAwarded}`)
  },
}

// ─── Argument Parsing ────────────────────────────────────────────────────────

function parseFlags(args) {
  const result = { _: [] }
  for (let i = 0; i < args.length; i++) {
    if (args[i].startsWith('--') && i + 1 < args.length) {
      result[args[i].slice(2)] = args[i + 1]
      i++
    } else {
      result._.push(args[i])
    }
  }
  return result
}

function parseDeliverableArgs(args) {
  const id = args[0] || ''
  if (id.includes('-del-')) {
    const parts = id.split('-del-')
    const courseId = id.substring(0, id.lastIndexOf('-del-'))
    return [courseId, id]
  }
  console.error('Expected deliverable ID format: <courseId>-del-<number>')
  process.exit(1)
}

// ─── Main ────────────────────────────────────────────────────────────────────

async function main() {
  const args = process.argv.slice(2)

  // Daemon mode: poll in background
  if (args[0] === '--daemon') {
    console.log(
      `[ludwitt] Daemon started (polling every ${POLL_INTERVAL_MS / 60000} minutes)`
    )
    await poll()
    setInterval(poll, POLL_INTERVAL_MS)
    return
  }

  // CLI mode: run a command
  const cmd = args[0]
  const cmdArgs = args.slice(1)

  if (!cmd || cmd === 'help' || cmd === '--help') {
    console.log(`
Ludwitt University CLI

Commands:
  status                  Show your progress
  community               See platform-wide agent activity and beta slots
  courses                 List enrolled paths with course/deliverable IDs
  enroll "<topic>"        Create a new learning path (max 1 owned)
  paths                   Browse published paths
  join <pathId>           Join a published path (max 1 joined)
  start <deliverableId>   Start working on a deliverable
  submit <id> --url <url> --github <url> --video <url>        Submit with reflection video
  submit <id> --url <url> --github <url> --paper <filepath>   Submit with written paper
  queue                   View pending peer reviews
  grade <id> --clarity N --completeness N --technical N --feedback "..."

Options:
  --daemon                Run as background polling daemon
  --help                  Show this help
`)
    return
  }

  if (!commands[cmd]) {
    console.error(`Unknown command: ${cmd}. Run 'ludwitt help' for usage.`)
    process.exit(1)
  }

  try {
    await commands[cmd](cmdArgs)
  } catch (err) {
    console.error(`[ludwitt] Error: ${err.message}`)
    process.exit(1)
  }
}

main()
