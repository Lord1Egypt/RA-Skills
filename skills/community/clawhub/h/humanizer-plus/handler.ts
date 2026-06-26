import { VercelRequest, VercelResponse } from '@vercel/node'

/**
 * AI Text Humanizer — Self-contained handler for ClawHub.
 * Two-layer architecture: LLM rewriting (primary) + regex fallback (deterministic).
 * Targets 24 known AI writing patterns from Wikipedia's WikiProject AI Cleanup.
 */

// ─── Environment helper ──────────────────────────────────────────────────────

function env(key: string): string {
  if (typeof process !== 'undefined' && process.env) {
    return process.env[key] || ''
  }
  return ''
}

// ─── Auth ────────────────────────────────────────────────────────────────────

function authenticate(req: VercelRequest): boolean {
  const authHeader = req.headers['authorization'] || ''
  const token = authHeader.replace(/^Bearer\s+/i, '')
  const expected = env('CLAW0X_API_KEY')
  if (!expected || !token) return false
  return token === expected
}

// ─── Response helpers ────────────────────────────────────────────────────────

function successResponse(res: VercelResponse, data: Record<string, unknown>) {
  return res.status(200).json(data)
}

function errorResponse(res: VercelResponse, message: string, status = 500, details?: unknown) {
  const body: Record<string, unknown> = { error: message }
  if (details) body.details = details
  return res.status(status).json(body)
}

// ─── System prompt (from blader/humanizer, Wikipedia WikiProject AI Cleanup) ─

const HUMANIZER_SYSTEM_PROMPT = `You are a writing editor that identifies and removes signs of AI-generated text. Based on Wikipedia's "Signs of AI writing" guide (WikiProject AI Cleanup).

When given text, rewrite it to remove these 24 AI patterns:

CONTENT: 1) Significance inflation ("pivotal moment", "testament to") 2) Notability name-dropping 3) Superficial -ing analyses ("highlighting...", "showcasing...") 4) Promotional language ("nestled", "vibrant", "groundbreaking") 5) Vague attributions ("Experts believe") 6) Formulaic "Despite challenges... continues to thrive"

LANGUAGE: 7) AI vocabulary (Additionally, delve, landscape, tapestry, underscore, foster, garner, showcase, testament, pivotal, crucial, enhance, interplay, intricate) 8) Copula avoidance ("serves as" instead of "is") 9) Negative parallelisms ("It's not just X, it's Y") 10) Rule of three overuse 11) Synonym cycling 12) False ranges ("from X to Y, from A to B")

STYLE: 13) Em dash overuse 14) Boldface overuse 15) Inline-header lists 16) Title Case Headings 17) Emojis 18) Curly quotes

COMMUNICATION: 19) Chatbot artifacts ("I hope this helps!") 20) Knowledge-cutoff disclaimers 21) Sycophantic tone ("Great question!")

FILLER: 22) Filler phrases ("In order to" -> "To") 23) Excessive hedging ("could potentially possibly" -> "may") 24) Generic conclusions ("The future looks bright")

PERSONALITY RULES:
- Have opinions. React to facts, don't just report them.
- Vary rhythm. Short sentences. Then longer ones.
- Acknowledge complexity. Real humans have mixed feelings.
- Use "I" when it fits.
- Let some mess in. Perfect structure feels algorithmic.
- Be specific about feelings.

PROCESS:
1. Identify all AI patterns in the input
2. Rewrite removing those patterns
3. Do a final "obviously AI generated" audit pass
4. Revise again to catch lingering AI-isms

OUTPUT: Return ONLY the final humanized text. No explanations, no pattern lists, no meta-commentary.`

// ─── Layer 1: LLM-powered humanization (Gemini) ─────────────────────────────

async function humanizeWithLLM(text: string): Promise<{ humanized: string; method: 'llm' }> {
  const apiKey = env('GEMINI_API_KEY')
  if (!apiKey) throw new Error('NO_API_KEY')

  const model = 'gemini-3.1-flash-lite-preview'
  const url = `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${apiKey}`

  const res = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      system_instruction: { parts: [{ text: HUMANIZER_SYSTEM_PROMPT }] },
      contents: [{ parts: [{ text }] }],
      generationConfig: { maxOutputTokens: 4096, temperature: 0.7 },
    }),
  })

  if (!res.ok) {
    const err = await res.text()
    throw new Error(`Gemini API ${res.status}: ${err}`)
  }

  const data = await res.json()
  const humanized = data.candidates?.[0]?.content?.parts?.[0]?.text || ''
  if (!humanized) throw new Error('Empty response from LLM')

  return { humanized, method: 'llm' }
}

// ─── Layer 2: Regex-based fallback (deterministic) ───────────────────────────

const AI_VOCAB: Record<string, string> = {
  'additionally': 'also', 'furthermore': 'also', 'moreover': 'also',
  'testament': 'example', 'landscape': 'field', 'showcasing': 'showing',
  'underscoring': 'showing', 'highlighting': 'showing',
  'delve': 'look into', 'delving': 'looking into',
  'pivotal': 'important', 'transformative': 'major',
  'groundbreaking': 'new', 'cutting-edge': 'modern',
  'leveraging': 'using', 'utilize': 'use', 'utilizing': 'using',
  'facilitate': 'help', 'facilitating': 'helping',
  'endeavor': 'effort', 'subsequently': 'then',
  'nevertheless': 'still', 'aforementioned': 'this',
  'thereby': 'so', 'wherein': 'where', 'whilst': 'while',
  'seamless': 'smooth', 'seamlessly': 'smoothly',
  'robust': 'strong', 'holistic': 'complete',
  'synergy': 'cooperation', 'paradigm': 'model',
  'ecosystem': 'system', 'empower': 'help', 'empowering': 'helping',
}

const FILLER: [RegExp, string][] = [
  [/\bin order to\b/gi, 'to'],
  [/\bdue to the fact that\b/gi, 'because'],
  [/\bit is worth noting that\b/gi, ''],
  [/\bit is important to note that\b/gi, ''],
  [/\bit should be noted that\b/gi, ''],
  [/\bat the end of the day\b/gi, ''],
  [/\bin today's rapidly evolving\b/gi, "in today's"],
  [/\bat the forefront of\b/gi, 'leading'],
  [/\bat the intersection of\b/gi, 'combining'],
  [/\bin the realm of\b/gi, 'in'],
  [/\bwhen it comes to\b/gi, 'for'],
  [/\bthe fact that\b/gi, 'that'],
  [/\ba wide range of\b/gi, 'many'],
  [/\ba plethora of\b/gi, 'many'],
]

const CHATBOT: RegExp[] = [
  /\bi hope this helps[.!]?\s*/gi,
  /\blet me know if you[^.!?]*[.!?]\s*/gi,
  /\bfeel free to[^.!?]*[.!?]\s*/gi,
  /\bgreat question[.!]?\s*/gi,
  /\byou're absolutely right[.!]?\s*/gi,
  /\bin conclusion,?\s*/gi,
  /\bto summarize,?\s*/gi,
]

const INFLATION: [RegExp, string][] = [
  [/\bmarking a pivotal moment in the evolution of\b/gi, ''],
  [/\bserves as an? (?:enduring )?testament to\b/gi, 'shows'],
  [/\bnestled (?:within|in|at)\b/gi, 'in'],
  [/\bthe transformative (?:potential|power) of\b/gi, ''],
  [/\bthe future looks bright\b/gi, ''],
  [/\bexciting times lie ahead\b/gi, ''],
  [/\bunlock(?:ing)? (?:the )?(?:full )?potential\b/gi, 'improving'],
]

const COPULA: [RegExp, string][] = [
  [/\bserves as\b/gi, 'is'], [/\bfunctions as\b/gi, 'is'],
  [/\bstands as\b/gi, 'is'], [/\bacts as\b/gi, 'is'],
]

function humanizeWithRegex(text: string): { humanized: string; method: 'regex' } {
  let r = text
  for (const p of CHATBOT) r = r.replace(p, '')
  for (const [p, s] of FILLER) r = r.replace(p, s)
  for (const [p, s] of INFLATION) r = r.replace(p, s)
  for (const [p, s] of COPULA) r = r.replace(p, s)
  for (const [w, s] of Object.entries(AI_VOCAB)) {
    r = r.replace(new RegExp(`\\b${w}\\b`, 'gi'), s)
  }
  // Remove emojis
  r = r.replace(/[\u{1F600}-\u{1F64F}\u{1F300}-\u{1F5FF}\u{1F680}-\u{1F6FF}\u{1F1E0}-\u{1F1FF}\u{2600}-\u{26FF}\u{2700}-\u{27BF}]\s*/gu, '')
  // Em dash overuse
  if ((r.match(/\u2014/g) || []).length > 2) r = r.replace(/\u2014/g, ',')
  // Hedging
  r = r.replace(/\bcould potentially possibly\b/gi, 'may')
  r = r.replace(/\bcould potentially\b/gi, 'may')
  // Cleanup whitespace
  r = r.replace(/ {2,}/g, ' ').replace(/^ +/gm, '').replace(/\n{3,}/g, '\n\n')
  return { humanized: r.trim(), method: 'regex' }
}

// ─── Main handler ────────────────────────────────────────────────────────────

async function handler(req: VercelRequest, res: VercelResponse) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' })
  }

  if (!authenticate(req)) {
    return res.status(401).json({ error: 'Unauthorized' })
  }

  const input = req.body?.input || {}
  const text: string = input.text || input.content || input.body || ''

  if (!text || typeof text !== 'string' || text.trim().length === 0) {
    return errorResponse(res, 'Input must contain a "text", "content", or "body" string field', 400)
  }

  const startTime = Date.now()

  try {
    let result: { humanized: string; method: string }
    try {
      result = await humanizeWithLLM(text)
    } catch (llmErr: any) {
      console.warn('[humanizer] LLM unavailable, using regex fallback:', llmErr.message)
      result = humanizeWithRegex(text)
    }

    const latencyMs = Date.now() - startTime

    return successResponse(res, {
      humanized_text: result.humanized,
      original_length: text.length,
      humanized_length: result.humanized.length,
      method: result.method,
      _meta: { skill: 'humanizer', latency_ms: latencyMs, version: '2.2.0' },
    })
  } catch (error: any) {
    console.error('[humanizer] Processing error:', error.message)
    return errorResponse(res, 'Processing failed', 500, error.message)
  }
}

export default handler
