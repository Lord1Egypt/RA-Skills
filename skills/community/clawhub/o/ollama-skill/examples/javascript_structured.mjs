import 'dotenv/config'
import ollama from 'ollama'
import { z } from 'zod'
import { zodToJsonSchema } from 'zod-to-json-schema'

const TaskPlan = z.object({
  summary: z.string(),
  risk: z.string(),
  next_action: z.string(),
})

const response = await ollama.chat({
  model: process.env.OLLAMA_MODEL || 'gpt-oss',
  messages: [{ role: 'user', content: 'Return JSON with summary, risk, next_action.' }],
  format: zodToJsonSchema(TaskPlan),
})

console.log(response.message.content)
