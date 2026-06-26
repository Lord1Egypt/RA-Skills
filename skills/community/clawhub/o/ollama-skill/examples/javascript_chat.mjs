import 'dotenv/config'
import { Ollama } from 'ollama'

const ollama = new Ollama({ host: process.env.OLLAMA_HOST || 'http://localhost:11434' })

const response = await ollama.chat({
  model: process.env.OLLAMA_MODEL || 'qwen3-coder',
  messages: [{ role: 'user', content: 'Refactor a Python function for readability.' }],
})

console.log(response.message.content)
