import { z } from 'zod'
import type { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js'
import { mlFetch } from '../client.js'
import type { MLProduct } from '../types.js'

export function registerUpdateStock(server: McpServer) {
  server.tool(
    'update_stock',
    'Actualiza el stock/cantidad disponible de una publicación en Mercado Libre. Retorna stock anterior y nuevo.',
    {
      item_id: z.string().describe('ID de la publicación (ej: MLA1234567890)'),
      quantity: z.number().int().min(0).describe('Nueva cantidad disponible'),
    },
    async ({ item_id, quantity }) => {
      // Obtener stock actual
      const current = await mlFetch<MLProduct>(`/items/${item_id}`, {
        params: { attributes: 'id,title,available_quantity' },
      })

      const previousStock = current.available_quantity

      // Actualizar stock
      await mlFetch<MLProduct>(`/items/${item_id}`, {
        method: 'PUT',
        body: { available_quantity: quantity },
      })

      return {
        content: [{
          type: 'text' as const,
          text: `Stock actualizado para ${item_id} ("${current.title}"):\n` +
            `  Anterior: ${previousStock} unidades\n` +
            `  Nuevo:    ${quantity} unidades\n` +
            `  Diferencia: ${quantity >= previousStock ? '+' : ''}${quantity - previousStock}`,
        }],
      }
    }
  )
}
