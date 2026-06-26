import { z } from 'zod'
import type { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js'
import { mlFetch } from '../client.js'
import type { MLProduct } from '../types.js'

export function registerListProducts(server: McpServer) {
  server.tool(
    'list_products',
    'Lista los productos/publicaciones de un vendedor en Mercado Libre. Retorna título, precio, stock, estado, link y thumbnail.',
    {
      seller_id: z.string().describe('ID numérico del vendedor en ML'),
      status: z.enum(['active', 'paused', 'closed', 'under_review']).optional()
        .describe('Filtrar por estado de la publicación'),
      limit: z.number().min(1).max(100).optional()
        .describe('Cantidad máxima de productos (default 50)'),
      offset: z.number().min(0).optional()
        .describe('Offset para paginación'),
    },
    async ({ seller_id, status, limit = 50, offset = 0 }) => {
      // Paso 1: buscar IDs del vendedor
      const searchResult = await mlFetch<{
        results: string[]
        paging: { total: number; offset: number; limit: number }
      }>(`/users/${seller_id}/items/search`, {
        params: {
          status: status,
          limit: Math.min(limit, 50),
          offset,
        },
      })

      if (searchResult.results.length === 0) {
        return {
          content: [{
            type: 'text' as const,
            text: `No se encontraron productos para el vendedor ${seller_id}` +
              (status ? ` con estado "${status}"` : '') + '.',
          }],
        }
      }

      // Paso 2: obtener detalle de cada item (multi-get de a 20)
      const itemIds = searchResult.results
      const products: MLProduct[] = []

      for (let i = 0; i < itemIds.length; i += 20) {
        const batch = itemIds.slice(i, i + 20)
        const items = await mlFetch<Array<{ code: number; body: MLProduct }>>(
          '/items',
          { params: { ids: batch.join(',') } }
        )
        for (const item of items) {
          if (item.code === 200) products.push(item.body)
        }
      }

      const summary = products.map(p => ({
        id: p.id,
        titulo: p.title,
        precio: `${p.currency_id} ${p.price}`,
        stock: p.available_quantity,
        vendidos: p.sold_quantity,
        estado: p.status,
        link: p.permalink,
        thumbnail: p.thumbnail,
        tipo: p.listing_type_id,
        catalogo: p.catalog_listing ?? false,
      }))

      return {
        content: [{
          type: 'text' as const,
          text: `${products.length} productos encontrados (de ${searchResult.paging.total} total):\n\n` +
            JSON.stringify(summary, null, 2),
        }],
      }
    }
  )
}
