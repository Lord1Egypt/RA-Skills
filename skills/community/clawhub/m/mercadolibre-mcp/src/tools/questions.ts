import { z } from 'zod'
import type { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js'
import { mlFetch } from '../client.js'
import type { MLQuestion } from '../types.js'

export function registerListQuestions(server: McpServer) {
  server.tool(
    'list_questions',
    'Lista las preguntas recibidas en publicaciones de Mercado Libre. Puede filtrar por item o estado (sin responder, respondidas).',
    {
      seller_id: z.string().describe('ID numérico del vendedor'),
      item_id: z.string().optional().describe('ID de la publicación para filtrar'),
      status: z.enum(['UNANSWERED', 'ANSWERED', 'CLOSED_UNANSWERED']).optional()
        .describe('Filtrar por estado de la pregunta'),
      limit: z.number().min(1).max(50).optional()
        .describe('Cantidad máxima (default 20)'),
      offset: z.number().min(0).optional()
        .describe('Offset para paginación'),
    },
    async ({ seller_id, item_id, status, limit = 20, offset = 0 }) => {
      const params: Record<string, string | number | undefined> = {
        seller_id,
        item: item_id,
        status,
        limit,
        offset,
        sort_fields: 'date_created',
        sort_types: 'DESC',
      }

      const result = await mlFetch<{
        questions: MLQuestion[]
        total: number
      }>('/questions/search', { params })

      if (result.questions.length === 0) {
        return {
          content: [{
            type: 'text' as const,
            text: 'No se encontraron preguntas con los filtros indicados.',
          }],
        }
      }

      const questions = result.questions.map(q => ({
        id: q.id,
        item_id: q.item_id,
        pregunta: q.text,
        de: q.from.nickname,
        fecha: q.date_created,
        estado: q.status,
        respuesta: q.answer ? q.answer.text : null,
        fecha_respuesta: q.answer?.date_created || null,
      }))

      return {
        content: [{
          type: 'text' as const,
          text: `${result.questions.length} preguntas (de ${result.total} total):\n\n` +
            JSON.stringify(questions, null, 2),
        }],
      }
    }
  )
}

export function registerAnswerQuestion(server: McpServer) {
  server.tool(
    'answer_question',
    'Responde una pregunta en Mercado Libre. La respuesta es pública y visible por todos los compradores.',
    {
      question_id: z.number().describe('ID numérico de la pregunta a responder'),
      text: z.string().min(1).max(2000).describe('Texto de la respuesta'),
    },
    async ({ question_id, text }) => {
      await mlFetch<{ id: number; status: string }>(
        `/answers`,
        {
          method: 'POST',
          body: { question_id, text },
        }
      )

      return {
        content: [{
          type: 'text' as const,
          text: `Pregunta #${question_id} respondida exitosamente.\n` +
            `Respuesta: "${text.substring(0, 100)}${text.length > 100 ? '...' : ''}"`,
        }],
      }
    }
  )
}
