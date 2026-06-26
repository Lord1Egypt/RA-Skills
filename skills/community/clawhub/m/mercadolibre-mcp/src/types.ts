// Tipos compartidos del MCP server Mercado Libre

export interface MLConfig {
  clientId: string
  clientSecret: string
  refreshToken: string
  siteId: string // MLA, MLU, MLB, etc.
}

export interface TokenData {
  accessToken: string
  expiresAt: number // Unix timestamp en ms
}

export interface MLProduct {
  id: string
  title: string
  price: number
  currency_id: string
  available_quantity: number
  sold_quantity: number
  status: string
  permalink: string
  thumbnail: string
  category_id: string
  condition: string
  listing_type_id: string
  date_created: string
  last_updated: string
  health?: number
  catalog_listing?: boolean
}

export interface MLOrder {
  id: number
  status: string
  date_created: string
  date_closed: string
  total_amount: number
  currency_id: string
  buyer: {
    id: number
    nickname: string
    first_name: string
    last_name: string
  }
  order_items: Array<{
    item: { id: string; title: string }
    quantity: number
    unit_price: number
  }>
  shipping: {
    id: number
    status: string
  }
  payments: Array<{
    id: number
    status: string
    total_paid_amount: number
  }>
}

export interface MLQuestion {
  id: number
  item_id: string
  seller_id: number
  status: string
  text: string
  date_created: string
  from: { id: number; nickname: string }
  answer?: {
    text: string
    date_created: string
    status: string
  }
}

export interface MLReputation {
  seller_id: number
  nickname: string
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

export interface MLVisits {
  item_id: string
  total_visits: number
  date_from: string
  date_to: string
}

export interface MLAdCampaign {
  item_id: string
  status: string
  daily_budget: number
  ads_cost: number
}

export interface MLCategory {
  id: string
  name: string
  path_from_root: Array<{ id: string; name: string }>
  children_categories: Array<{ id: string; name: string }>
  attributes?: Array<{
    id: string
    name: string
    value_type: string
    tags: Record<string, unknown>
  }>
}

export interface MLSearchResult {
  id: string
  title: string
  price: number
  currency_id: string
  sold_quantity: number
  available_quantity: number
  permalink: string
  thumbnail: string
  seller: {
    id: number
    nickname: string
    power_seller_status: string | null
  }
  shipping: { free_shipping: boolean }
  condition: string
}

export interface MLError {
  message: string
  error: string
  status: number
  cause: string[]
}
