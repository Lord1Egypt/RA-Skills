import { z } from 'zod'
import type { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js'
import { mlFetch } from '../client.js'
import type { MLOrder } from '../types.js'

export function registerGetOrders(server: McpServer) {
  server.tool(
    'get_orders',
    'Obtiene las órdenes/ventas de un vendedor. Incluye comprador, items, envío y pagos.',
    {
      seller_id: z.string().describe('ID numérico del vendedor en ML'),
      status: z.enum(['paid', 'shipped', 'delivered', 'cancelled']).optional()
        .describe('Filtrar por estado de la orden'),
      date_from: z.string().optional()
        .describe('Fecha desde (ISO 8601, ej: 2026-03-01T00:00:00.000-03:00)'),
      date_to: z.string().optional()
        .describe('Fecha hasta (ISO 8601)'),
      limit: z.number().min(1).max(50).optional()
        .describe('Cantidad máxima de órdenes (default 20)'),
      offset: z.number().min(0).optional()
        .describe('Offset para paginación'),
    },
    async ({ seller_id, status, date_from, date_to, limit = 20, offset = 0 }) => {
      const params: Record<string, string | number | undefined> = {
        seller: seller_id,
        'order.status': status,
        'order.date_created.from': date_from,
        'order.date_created.to': date_to,
        limit,
        offset,
        sort: 'date_desc',
      }

      const result = await mlFetch<{
        results: MLOrder[]
        paging: { total: number; offset: number; limit: number }
      }>('/orders/search', { params })

      if (result.results.length === 0) {
        return {
          content: [{
            type: 'text' as const,
            text: 'No se encontraron órdenes con los filtros indicados.',
          }],
        }
      }

      const orders = result.results.map(o => ({
        id: o.id,
        estado: o.status,
        fecha: o.date_created,
        total: `${o.currency_id} ${o.total_amount}`,
        comprador: o.buyer.nickname,
        items: o.order_items.map(oi => ({
          id: oi.item.id,
          titulo: oi.item.title,
          cantidad: oi.quantity,
          precio_unitario: oi.unit_price,
        })),
        envio_estado: o.shipping?.status || 'sin envío',
        pago_estado: o.payments?.[0]?.status || 'sin pago',
      }))

      return {
        content: [{
          type: 'text' as const,
          text: `${result.results.length} órdenes (de ${result.paging.total} total):\n\n` +
            JSON.stringify(orders, null, 2),
        }],
      }
    }
  )
}
