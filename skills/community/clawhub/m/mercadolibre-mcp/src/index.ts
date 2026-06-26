#!/usr/bin/env node

// MCP Server Mercado Libre — 11 tools de operaciones de seller
// Primer MCP completo de ML en el mercado

import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js'
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js'

// Tools
import { registerListProducts } from './tools/products.js'
import { registerGetOrders } from './tools/orders.js'
import { registerUpdatePrice } from './tools/pricing.js'
import { registerUpdateStock } from './tools/stock.js'
import { registerListQuestions, registerAnswerQuestion } from './tools/questions.js'
import { registerGetItemMetrics } from './tools/metrics.js'
import { registerManageAds } from './tools/ads.js'
import { registerGetReputation } from './tools/reputation.js'
import { registerSearchCompetitors } from './tools/competitors.js'
import { registerGetCategories } from './tools/categories.js'

const server = new McpServer({
  name: 'mercadolibre',
  version: '1.0.0',
})

// Registrar las 11 tools
registerListProducts(server)
registerGetOrders(server)
registerUpdatePrice(server)
registerUpdateStock(server)
registerListQuestions(server)
registerAnswerQuestion(server)
registerGetItemMetrics(server)
registerManageAds(server)
registerGetReputation(server)
registerSearchCompetitors(server)
registerGetCategories(server)

// Arrancar con transporte stdio
async function main() {
  const transport = new StdioServerTransport()
  await server.connect(transport)
  console.error('[ml-mcp] Server iniciado — 11 tools disponibles')
}

main().catch((error) => {
  console.error('[ml-mcp] Error fatal:', error)
  process.exit(1)
})
