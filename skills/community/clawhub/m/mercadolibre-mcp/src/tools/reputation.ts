import { z } from 'zod'
import type { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js'
import { mlFetch } from '../client.js'

export function registerGetReputation(server: McpServer) {
  server.tool(
    'get_reputation',
    'Obtiene la reputación de un vendedor: nivel, ventas completadas, reclamos, cancelaciones y tiempo de despacho.',
    {
      seller_id: z.string().describe('ID numérico del vendedor en ML'),
    },
    async ({ seller_id }) => {
      const user = await mlFetch<{
        id: number
        nickname: string
        seller_reputation: {
          level_id: string
          power_seller_status: string | null
          transactions: {
            completed: number
            canceled: number
            total: number
            ratings: {
              positive: number
              neutral: number
              negative: number
            }
            period: string
          }
          metrics: {
            claims: { rate: number; value: number }
            delayed_handling_time: { rate: number; value: number }
            cancellations: { rate: number; value: number }
            sales: { completed: number; period: string }
          }
        }
        status: { site_status: string }
        points: number
        registration_date: string
      }>(`/users/${seller_id}`)

      const rep = user.seller_reputation
      const metrics = rep.metrics
      const tx = rep.transactions

      return {
        content: [{
          type: 'text' as const,
          text: `Reputación de ${user.nickname} (ID: ${user.id}):\n\n` +
            `  Nivel: ${rep.level_id}\n` +
            `  MercadoLíder: ${rep.power_seller_status || 'No'}\n` +
            `  Estado: ${user.status.site_status}\n` +
            `  Registrado: ${user.registration_date}\n` +
            `\nTransacciones (${tx.period}):\n` +
            `  Completadas: ${tx.completed}\n` +
            `  Canceladas: ${tx.canceled}\n` +
            `  Total: ${tx.total}\n` +
            `  Calificación positiva: ${(tx.ratings.positive * 100).toFixed(1)}%\n` +
            `  Calificación neutral: ${(tx.ratings.neutral * 100).toFixed(1)}%\n` +
            `  Calificación negativa: ${(tx.ratings.negative * 100).toFixed(1)}%\n` +
            `\nMétricas:\n` +
            `  Reclamos: ${(metrics.claims.rate * 100).toFixed(2)}% (${metrics.claims.value} casos)\n` +
            `  Despacho demorado: ${(metrics.delayed_handling_time.rate * 100).toFixed(2)}% (${metrics.delayed_handling_time.value} casos)\n` +
            `  Cancelaciones: ${(metrics.cancellations.rate * 100).toFixed(2)}% (${metrics.cancellations.value} casos)\n` +
            `  Ventas completadas: ${metrics.sales.completed} (${metrics.sales.period})`,
        }],
      }
    }
  )
}
