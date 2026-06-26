import { z } from 'zod'
import type { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js'
import { mlFetch } from '../client.js'

export function registerGetItemMetrics(server: McpServer) {
  server.tool(
    'get_item_metrics',
    'Obtiene métricas de una publicación: visitas, salud de publicación y datos de catálogo.',
    {
      item_id: z.string().describe('ID de la publicación (ej: MLA1234567890)'),
      date_from: z.string().optional()
        .describe('Fecha desde para visitas (YYYY-MM-DD, default: últimos 30 días)'),
      date_to: z.string().optional()
        .describe('Fecha hasta para visitas (YYYY-MM-DD, default: hoy)'),
    },
    async ({ item_id, date_from, date_to }) => {
      // Calcular fechas por defecto (últimos 30 días)
      const now = new Date()
      const thirtyDaysAgo = new Date(now.getTime() - 30 * 24 * 60 * 60 * 1000)
      const from = date_from || thirtyDaysAgo.toISOString().split('T')[0]
      const to = date_to || now.toISOString().split('T')[0]

      // Obtener datos del item y visitas en paralelo
      const [itemData, visitsData] = await Promise.all([
        mlFetch<{
          id: string
          title: string
          price: number
          currency_id: string
          available_quantity: number
          sold_quantity: number
          status: string
          health: number
          listing_type_id: string
          catalog_listing: boolean
          category_id: string
          permalink: string
        }>(`/items/${item_id}`, {
          params: {
            attributes: 'id,title,price,currency_id,available_quantity,sold_quantity,status,health,listing_type_id,catalog_listing,category_id,permalink',
          },
        }),
        mlFetch<Array<{ date: string; total: number }>>(
          `/items/${item_id}/visits/time_window`,
          { params: { last: 30, unit: 'day' } }
        ).catch(() => [] as Array<{ date: string; total: number }>),
      ])

      const totalVisits = visitsData.reduce((sum, v) => sum + v.total, 0)
      const avgDailyVisits = totalVisits > 0 ? Math.round(totalVisits / visitsData.length) : 0
      const conversionRate = totalVisits > 0
        ? ((itemData.sold_quantity / totalVisits) * 100).toFixed(2)
        : '0.00'

      return {
        content: [{
          type: 'text' as const,
          text: `Métricas de ${item_id} ("${itemData.title}"):\n\n` +
            `  Estado: ${itemData.status}\n` +
            `  Precio: ${itemData.currency_id} ${itemData.price}\n` +
            `  Stock: ${itemData.available_quantity}\n` +
            `  Vendidos: ${itemData.sold_quantity}\n` +
            `  Tipo listado: ${itemData.listing_type_id}\n` +
            `  En catálogo: ${itemData.catalog_listing ? 'Sí' : 'No'}\n` +
            `  Salud: ${itemData.health != null ? `${(itemData.health * 100).toFixed(0)}%` : 'N/D'}\n` +
            `\nVisitas (últimos 30 días):\n` +
            `  Total: ${totalVisits}\n` +
            `  Promedio diario: ${avgDailyVisits}\n` +
            `  Tasa de conversión estimada: ${conversionRate}%\n` +
            `\n  Categoría: ${itemData.category_id}\n` +
            `  Link: ${itemData.permalink}`,
        }],
      }
    }
  )
}
