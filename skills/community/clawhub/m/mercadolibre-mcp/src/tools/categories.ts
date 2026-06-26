import { z } from 'zod'
import type { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js'
import { mlFetch } from '../client.js'
import { getConfig } from '../auth.js'
import type { MLCategory } from '../types.js'

export function registerGetCategories(server: McpServer) {
  server.tool(
    'get_categories',
    'Obtiene categorías de Mercado Libre y sus atributos. Útil para saber qué categoría usar al publicar y qué atributos son requeridos.',
    {
      category_id: z.string().optional()
        .describe('ID de categoría específica (ej: MLA1234). Si se omite, lista las categorías raíz del sitio.'),
      query: z.string().optional()
        .describe('Buscar categoría por nombre (ej: "repuestos autos"). Usa el category predictor de ML.'),
    },
    async ({ category_id, query }) => {
      const config = getConfig()

      // Si se pasa un category_id, obtener detalle + atributos
      if (category_id) {
        const [category, attributes] = await Promise.all([
          mlFetch<MLCategory>(`/categories/${category_id}`),
          mlFetch<Array<{
            id: string
            name: string
            value_type: string
            tags: { required?: boolean }
            values?: Array<{ id: string; name: string }>
          }>>(`/categories/${category_id}/attributes`).catch(() => []),
        ])

        const path = category.path_from_root.map(p => p.name).join(' > ')
        const requiredAttrs = attributes.filter(a => a.tags?.required)
        const optionalAttrs = attributes.filter(a => !a.tags?.required)

        return {
          content: [{
            type: 'text' as const,
            text: `Categoría: ${category.name} (${category_id})\n` +
              `Ruta: ${path}\n\n` +
              `Subcategorías: ${category.children_categories.length > 0
                ? category.children_categories.map(c => `${c.name} (${c.id})`).join(', ')
                : 'Ninguna (categoría hoja)'}\n\n` +
              `Atributos requeridos (${requiredAttrs.length}):\n` +
              requiredAttrs.map(a => `  - ${a.name} (${a.id}) [${a.value_type}]` +
                (a.values?.length ? ` — opciones: ${a.values.slice(0, 5).map(v => v.name).join(', ')}${a.values.length > 5 ? '...' : ''}` : '')
              ).join('\n') +
              `\n\nAtributos opcionales (${optionalAttrs.length}):\n` +
              optionalAttrs.slice(0, 10).map(a => `  - ${a.name} (${a.id}) [${a.value_type}]`).join('\n') +
              (optionalAttrs.length > 10 ? `\n  ... y ${optionalAttrs.length - 10} más` : ''),
          }],
        }
      }

      // Si se pasa query, usar el predictor de categorías
      if (query) {
        const predictions = await mlFetch<Array<{
          id: string
          name: string
          path_from_root: Array<{ id: string; name: string }>
        }>>(`/sites/${config.siteId}/domain_discovery/search`, {
          params: { q: query },
        }).catch(() =>
          // Fallback al category predictor clásico
          mlFetch<Array<{
            id: string
            name: string
            path_from_root: Array<{ id: string; name: string }>
          }>>(`/sites/${config.siteId}/category_predictor/predict`, {
            params: { title: query },
          }).catch(() => [])
        )

        if (!predictions || predictions.length === 0) {
          return {
            content: [{
              type: 'text' as const,
              text: `No se encontraron categorías para "${query}". Probá con otros términos.`,
            }],
          }
        }

        const cats = (Array.isArray(predictions) ? predictions : [predictions]).map(p => ({
          id: p.id,
          nombre: p.name,
          ruta: p.path_from_root?.map(r => r.name).join(' > ') || '',
        }))

        return {
          content: [{
            type: 'text' as const,
            text: `Categorías sugeridas para "${query}":\n\n` +
              JSON.stringify(cats, null, 2),
          }],
        }
      }

      // Sin parámetros: categorías raíz del sitio
      const rootCategories = await mlFetch<Array<{ id: string; name: string }>>(
        `/sites/${config.siteId}/categories`
      )

      return {
        content: [{
          type: 'text' as const,
          text: `Categorías raíz de ${config.siteId} (${rootCategories.length}):\n\n` +
            rootCategories.map(c => `  ${c.id}: ${c.name}`).join('\n'),
        }],
      }
    }
  )
}
