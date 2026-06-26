import { z } from 'zod'
import type { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js'
import { mlFetch } from '../client.js'

export function registerManageAds(server: McpServer) {
  server.tool(
    'manage_ads',
    'Gestiona Product Ads de Mercado Libre: activar, pausar o consultar estado de publicidad de un item.',
    {
      seller_id: z.string().describe('ID numérico del vendedor'),
      item_id: z.string().describe('ID de la publicación (ej: MLA1234567890)'),
      action: z.enum(['status', 'activate', 'pause']).describe(
        'Acción: "status" consulta el estado actual, "activate" activa publicidad, "pause" la pausa'
      ),
      daily_budget: z.number().positive().optional()
        .describe('Presupuesto diario en moneda local (solo para activate)'),
    },
    async ({ seller_id, item_id, action, daily_budget }) => {
      if (action === 'status') {
        // Consultar estado actual del ad
        try {
          const adData = await mlFetch<{
            id: string
            status: string
            daily_budget: number
            campaign_id: string
          }>(`/advertising/product_ads/${item_id}`)

          return {
            content: [{
              type: 'text' as const,
              text: `Publicidad de ${item_id}:\n` +
                `  Estado: ${adData.status}\n` +
                `  Presupuesto diario: ${adData.daily_budget}\n` +
                `  Campaña: ${adData.campaign_id}`,
            }],
          }
        } catch {
          return {
            content: [{
              type: 'text' as const,
              text: `El item ${item_id} no tiene publicidad activa o no es elegible para Product Ads.`,
            }],
          }
        }
      }

      if (action === 'activate') {
        const body: Record<string, unknown> = {
          item_id,
          status: 'active',
        }
        if (daily_budget) body.daily_budget = daily_budget

        const result = await mlFetch<{ id: string; status: string; daily_budget: number }>(
          `/advertising/product_ads`,
          { method: 'POST', body }
        )

        return {
          content: [{
            type: 'text' as const,
            text: `Publicidad activada para ${item_id}:\n` +
              `  Estado: ${result.status}\n` +
              `  Presupuesto diario: ${result.daily_budget}`,
          }],
        }
      }

      // pause
      await mlFetch(`/advertising/product_ads/${item_id}`, {
        method: 'PUT',
        body: { status: 'paused' },
      })

      return {
        content: [{
          type: 'text' as const,
          text: `Publicidad pausada para ${item_id}.`,
        }],
      }
    }
  )
}
