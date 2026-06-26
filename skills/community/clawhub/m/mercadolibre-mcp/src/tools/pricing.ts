import { z } from 'zod'
import type { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js'
import { mlFetch } from '../client.js'
import type { MLProduct } from '../types.js'

export function registerUpdatePrice(server: McpServer) {
  server.tool(
    'update_price',
    'Actualiza el precio de una publicación en Mercado Libre. Retorna precio anterior y nuevo para confirmación.',
    {
      item_id: z.string().describe('ID de la publicación (ej: MLA1234567890)'),
      price: z.number().positive().describe('Nuevo precio en la moneda de la publicación'),
    },
    async ({ item_id, price }) => {
      // Obtener precio actual antes de cambiar
      const current = await mlFetch<MLProduct>(`/items/${item_id}`, {
        params: { attributes: 'id,title,price,currency_id' },
      })

      const previousPrice = current.price

      // Actualizar precio
      await mlFetch<MLProduct>(`/items/${item_id}`, {
        method: 'PUT',
        body: { price },
      })

      return {
        content: [{
          type: 'text' as const,
          text: `Precio actualizado para ${item_id} ("${current.title}"):\n` +
            `  Anterior: ${current.currency_id} ${previousPrice}\n` +
            `  Nuevo:    ${current.currency_id} ${price}\n` +
            `  Cambio:   ${price > previousPrice ? '+' : ''}${((price - previousPrice) / previousPrice * 100).toFixed(1)}%`,
        }],
      }
    }
  )
}
