import { z } from 'zod'
import type { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js'
import { mlFetch } from '../client.js'
import { getConfig } from '../auth.js'
import type { MLSearchResult } from '../types.js'

export function registerSearchCompetitors(server: McpServer) {
  server.tool(
    'search_competitors',
    'Busca productos de la competencia en Mercado Libre. Retorna top resultados con precio, vendedor, ventas y envío gratis.',
    {
      query: z.string().describe('Término de búsqueda (ej: "repuesto freno toyota")'),
      category_id: z.string().optional()
        .describe('ID de categoría para filtrar (ej: MLA1234)'),
      price_min: z.number().optional().describe('Precio mínimo'),
      price_max: z.number().optional().describe('Precio máximo'),
      limit: z.number().min(1).max(50).optional()
        .describe('Cantidad de resultados (default 10)'),
      sort: z.enum(['relevance', 'price_asc', 'price_desc']).optional()
        .describe('Ordenar por relevancia o precio'),
    },
    async ({ query, category_id, price_min, price_max, limit = 10, sort = 'relevance' }) => {
      const config = getConfig()

      const sortMap: Record<string, string> = {
        relevance: 'relevance',
        price_asc: 'price_asc',
        price_desc: 'price_desc',
      }

      const params: Record<string, string | number | undefined> = {
        q: query,
        category: category_id,
        price: price_min || price_max
          ? `${price_min || '*'}-${price_max || '*'}`
          : undefined,
        limit,
        sort: sortMap[sort],
      }

      const result = await mlFetch<{
        results: MLSearchResult[]
        paging: { total: number }
      }>(`/sites/${config.siteId}/search`, { params })

      if (result.results.length === 0) {
        return {
          content: [{
            type: 'text' as const,
            text: `No se encontraron resultados para "${query}".`,
          }],
        }
      }

      const competitors = result.results.map((r, i) => ({
        posicion: i + 1,
        id: r.id,
        titulo: r.title,
        precio: `${r.currency_id} ${r.price}`,
        vendidos: r.sold_quantity,
        stock: r.available_quantity,
        vendedor: r.seller.nickname,
        mercadolider: r.seller.power_seller_status || 'No',
        envio_gratis: r.shipping.free_shipping,
        condicion: r.condition,
        link: r.permalink,
      }))

      return {
        content: [{
          type: 'text' as const,
          text: `${result.results.length} resultados para "${query}" (${result.paging.total} total):\n\n` +
            JSON.stringify(competitors, null, 2),
        }],
      }
    }
  )
}
