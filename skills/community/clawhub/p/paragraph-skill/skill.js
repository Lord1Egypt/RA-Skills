#!/usr/bin/env node

/**
 * Paragraph OpenClaw Skill (REST API implementation)
 * Uses native fetch to interact with Paragraph.com API
 */

// Configuration
const API_BASE = process.env.PARAGRAPH_API_BASE_URL || "https://public.api.paragraph.com/api"
// NOTE: API_KEY is read lazily inside request() to respect per-agent env injection
let DEFAULT_PUBLICATION_ID = process.env.PARAGRAPH_PUBLICATION_ID || null
// Publication slug (for URL building) - can be set manually via env var or auto-discovered
let DEFAULT_PUBLICATION_SLUG = process.env.PARAGRAPH_PUBLICATION_SLUG || null

/**
 * Standardized response format
 * @typedef {Object} ParagraphResult
 * @property {boolean} success
 * @property {any} data
 * @property {string} error
 */

/**
 * Make authenticated request to Paragraph API
 * @param {string} method - HTTP method
 * @param {string} endpoint - API endpoint (without base, e.g., "/v1/posts")
 * @param {Object} body - Request body (will be JSON stringified)
 * @param {Object} params - Query parameters
 * @param {Object} options - Additional options (formData, rawBody, timeout)
 * @param {number} [options.timeout=10000] - Request timeout in milliseconds (default 10s)
 * @returns {Promise<any>}
 */
async function request(method, endpoint, body = null, params = {}, options = {}) {
  // Read API_KEY from env at call time to respect per-skill injection
  const apiKey = process.env.PARAGRAPH_API_KEY
  if (!apiKey) {
    throw new Error("PARAGRAPH_API_KEY environment variable not set")
  }

  const url = new URL(`${API_BASE}${endpoint}`)
  Object.keys(params).forEach(key => {
    if (params[key] !== undefined && params[key] !== null) {
      url.searchParams.append(key, String(params[key]))
    }
  })

  const headers = {
    "Authorization": `Bearer ${apiKey}`
  }

  let fetchBody = null
  if (body) {
    headers["Content-Type"] = "application/json"
    fetchBody = JSON.stringify(body)
  }

  if (options.rawBody) {
    fetchBody = options.rawBody
    Object.assign(headers, options.headers)
  } else if (options.formData) {
    fetchBody = options.formData
    // Don't set Content-Type; fetch will set boundary
  }

  // Set up abort controller for timeout
  const controller = new AbortController()
  const timeoutMs = options.timeout || 30000 // default 30 seconds (POSTs can be slow)
  const timeoutId = setTimeout(() => controller.abort(), timeoutMs)

  try {
    const response = await fetch(url.toString(), {
      method,
      headers,
      body: fetchBody,
      signal: controller.signal
    })

    if (!response.ok) {
      let errorMsg = `HTTP ${response.status} ${response.statusText}`
      try {
        const errorData = await response.json()
        errorMsg = errorData.msg || errorData.message || errorData.error || errorMsg
      } catch (e) {}
      throw new Error(errorMsg)
    }

    if (response.status === 204 || response.headers.get("content-length") === "0") {
      return { success: true }
    }

    const contentType = response.headers.get("content-type") || ""
    if (contentType.includes("application/json")) {
      return await response.json()
    }
    return await response.text()
  } finally {
    clearTimeout(timeoutId)
  }
}

/**
 * Auto-discover publication ID and slug from the API key by fetching the feed
 * Caches the results in DEFAULT_PUBLICATION_ID and DEFAULT_PUBLICATION_SLUG
 * Returns the publication ID
 *
 * Respects pre-configured PARAGRAPH_PUBLICATION_SLUG: if set, uses it to fetch
 * the publication directly instead of auto-discovering from the feed.
 */
async function discoverPublicationId() {
  // Lazy-load from env if not already set (respects per-agent env injection)
  if (!DEFAULT_PUBLICATION_SLUG && process.env.PARAGRAPH_PUBLICATION_SLUG) {
    DEFAULT_PUBLICATION_SLUG = process.env.PARAGRAPH_PUBLICATION_SLUG
  }

  if (DEFAULT_PUBLICATION_ID) {
    return DEFAULT_PUBLICATION_ID
  }

  // If a slug is configured, use it to fetch the publication and get the ID
  if (DEFAULT_PUBLICATION_SLUG) {
    try {
      const pub = await request("GET", `/v1/publications/slug/${encodeURIComponent(DEFAULT_PUBLICATION_SLUG)}`)
      if (pub && pub.id) {
        DEFAULT_PUBLICATION_ID = String(pub.id)
        // Slug already set from env var, keep it
        return DEFAULT_PUBLICATION_ID
      }
    } catch (e) {
      // If this fails, fall back to feed auto-discovery
      console.warn(`Failed to fetch publication using configured slug "${DEFAULT_PUBLICATION_SLUG}", falling back to feed auto-discovery`)
    }
  }

  // Fallback: auto-discover from feed
  try {
    const result = await request("GET", "/v1/posts/feed", null, { limit: 1 })
    if (result.items && result.items.length > 0) {
      const pub = result.items[0].publication
      if (pub) {
        // Only set slug if not already configured
        if (!DEFAULT_PUBLICATION_SLUG) {
          if (pub.slug) {
            DEFAULT_PUBLICATION_SLUG = pub.slug
          } else if (pub.customDomain) {
            DEFAULT_PUBLICATION_SLUG = pub.customDomain
          }
        }

        // Now fetch the full publication using the slug to get the canonical ID
        if (DEFAULT_PUBLICATION_SLUG) {
          const fullPub = await request("GET", `/v1/publications/slug/${encodeURIComponent(DEFAULT_PUBLICATION_SLUG)}`)
          if (fullPub && fullPub.id) {
            DEFAULT_PUBLICATION_ID = String(fullPub.id)
            // Ensure slug is cached only if not already set
            if (!DEFAULT_PUBLICATION_SLUG && fullPub.slug) {
              DEFAULT_PUBLICATION_SLUG = fullPub.slug
            }
            return DEFAULT_PUBLICATION_ID
          }
        }
      }
    }
  } catch (e) {
    // Silently fall through to error later
  }

  throw new Error("Could not auto-discover publication ID. Either set PARAGRAPH_PUBLICATION_ID or PARAGRAPH_PUBLICATION_SLUG env var, or ensure your publication has at least one post to read from the feed.")
}

/**
 * Get the publication slug (for URL building)
 * Tries to auto-discover if not already cached
 */
async function getPublicationSlug() {
  if (DEFAULT_PUBLICATION_SLUG) {
    return DEFAULT_PUBLICATION_SLUG
  }

  // Ensure we have the ID first
  const id = await discoverPublicationId()

  try {
    // Fetch publication details to get the slug
    const pub = await request("GET", `/v1/publications/${id}`)
    if (pub.slug) {
      DEFAULT_PUBLICATION_SLUG = pub.slug
      return DEFAULT_PUBLICATION_SLUG
    }
    if (pub.customDomain) {
      DEFAULT_PUBLICATION_SLUG = pub.customDomain
      return DEFAULT_PUBLICATION_SLUG
    }
  } catch (e) {
    // Fall through
  }

  throw new Error("Could not determine publication slug. Set PARAGRAPH_PUBLICATION_ID and ensure the publication exists.")
}

/**
 * Wrap tools with standardized error handling
 */
function wrapTool(fn) {
  return async (...args) => {
    try {
      const data = await fn(...args)
      return { success: true, data, error: null }
    } catch (error) {
      return { success: false, data: null, error: error.message || String(error) }
    }
  }
}

/**
 * @type {Object.<string, Function>}
 */
export const tools = {
  /**
   * Test connection and authentication
   */
  paragraph_testConnection: wrapTool(async () => {
    // Call a lightweight authenticated endpoint to verify API key
    const result = await request("GET", "/v1/subscribers", null, { limit: 1 })
    // If we get here, auth worked
    return {
      message: "Connected to Paragraph API",
      hasSubscribers: (result.items?.length || 0) > 0,
      totalSubscribers: result.pagination?.total || 0
    }
  }),

  /**
   * Create a new blog post
   *
   * Posts are published immediately onchain, but the slug and URL require a few seconds
   * of processing to become available. By default, this tool returns immediately without waiting.
   * Set waitForProcessing to true to poll for up to ~25 seconds until slug/url are ready.
   *
   * @param {boolean} waitForProcessing - If false (default), returns immediately with post ID. Set true to poll for full post data including slug and URL.
   */
  paragraph_createPost: wrapTool(async ({
    title,
    markdown,
    subtitle,
    imageUrl,
    sendNewsletter = false,
    slug,
    postPreview,
    categories,
    waitForProcessing = false // DEFAULT TO FALSE – fast response by default
  }) => {
    if (!title || !markdown) {
      throw new Error("Missing required parameters: title, markdown")
    }

    // Build request body directly (no wrapper)
    const body = {
      title,
      markdown,
      sendNewsletter
    }

    if (subtitle) body.subtitle = subtitle
    if (imageUrl) body.imageUrl = imageUrl
    if (slug) body.slug = slug
    if (postPreview) body.postPreview = postPreview
    if (categories) body.categories = categories // array or comma-separated string

    const createResult = await request("POST", "/v1/posts", body)
    const postId = createResult.id

    // If waitForProcessing is true (default) and the immediate response lacks slug/url, poll for the full post data
    if (waitForProcessing) {
      // Quick check: maybe creation response already has slug/url (sometimes it does)
      if (createResult.slug && createResult.url) {
        return createResult
      }

      const maxAttempts = 12 // ~25 seconds total with backoff
      for (let i = 0; i < maxAttempts; i++) {
        try {
          // Use request with built-in timeout (3s per attempt)
          const full = await request("GET", `/v1/posts/${postId}`, null, {}, { timeout: 3000 })
          if (full.slug && full.url) {
            return full // Return complete post object
          }
        } catch (e) {
          // Ignore errors (network, timeout, rate limit) and continue polling
        }
        // Gentle backoff: 1s then 2s intervals to be rate-limit friendly
        const delay = i === 0 ? 1000 : 2000
        await new Promise(r => setTimeout(r, delay))
      }
      // Timeout – return the initial result with a note
      return {
        ...createResult,
        slug: createResult.slug || null,
        url: createResult.url || null,
        publishedAt: createResult.publishedAt || null,
        _warning: "Onchain processing not complete within ~25s. Call paragraph_getPost later to retrieve full data."
      }
    }

    // waitForProcessing = false: return immediate result (slug/url may be undefined)
    return {
      id: createResult.id,
      slug: createResult.slug,
      url: createResult.url,
      publishedAt: createResult.publishedAt
    }
  }),

  /**
   * Get a post by ID
   */
  paragraph_getPost: wrapTool(async ({ postId }) => {
    if (!postId) throw new Error("postId is required")
    const result = await request("GET", `/v1/posts/${postId}`)
    return result
  }),

  /**
   * Get a post by publication slug and post slug
   */
  paragraph_getPostBySlug: wrapTool(async ({ publicationSlug, postSlug }) => {
    if (!publicationSlug || !postSlug) {
      throw new Error("publicationSlug and postSlug are required")
    }
    // Encode slugs to handle special characters
    const encSlug = encodeURIComponent(publicationSlug)
    const encPostSlug = encodeURIComponent(postSlug)
    const result = await request("GET", `/publications/slug/${encSlug}/posts/slug/${encPostSlug}`)
    return result
  }),

  /**
   * List posts in a publication
   */
  paragraph_listPosts: wrapTool(async ({
    publicationId,
    limit = 10,
    cursor,
    includeContent = false
  }) => {
    const pubId = publicationId || await discoverPublicationId()
    if (!pubId) throw new Error("publicationId required or PARAGRAPH_PUBLICATION_ID must be set, or feed must have posts to auto-discover")

    console.log("DEBUG: listPosts using publicationId:", pubId) // temporary debug

    const params = { limit }
    if (cursor) params.cursor = cursor
    if (includeContent) params.includeContent = "true"

    const result = await request("GET", `/v1/publications/${pubId}/posts`, null, params)
    return {
      posts: result.items || [],
      pagination: result.pagination || {}
    }
  }),

  /**
   * Get publication by slug
   */
  paragraph_getPublication: wrapTool(async ({ slug }) => {
    if (!slug) throw new Error("slug is required")
    const result = await request("GET", `/publications/slug/${encodeURIComponent(slug)}`)
    return result
  }),

  /**
   * Get publication by custom domain
   */
  paragraph_getPublicationByDomain: wrapTool(async ({ domain }) => {
    if (!domain) throw new Error("domain is required")
    const result = await request("GET", `/publications/domain/${encodeURIComponent(domain)}`)
    return result
  }),

  /**
   * Get the current publication associated with the API key
   * This auto-discovers the publication (via feed -> slug -> ID) and returns full details.
   * Does not override a pre-configured PARAGRAPH_PUBLICATION_SLUG.
   */
  paragraph_getMyPublication: wrapTool(async () => {
    // This will populate DEFAULT_PUBLICATION_ID (and may set slug if not configured)
    const id = await discoverPublicationId()
    // Now fetch full publication details by the canonical ID
    const result = await request("GET", `/v1/publications/${id}`)
    // Cache slug for URL building ONLY if not already configured (respects env var)
    if (!DEFAULT_PUBLICATION_SLUG) {
      if (result.slug) {
        DEFAULT_PUBLICATION_SLUG = result.slug
      } else if (result.customDomain) {
        DEFAULT_PUBLICATION_SLUG = result.customDomain
      }
    }
    return result
  }),

  /**
   * Add a new subscriber
   */
  paragraph_addSubscriber: wrapTool(async ({
    email,
    wallet,
    sendWelcomeEmail = true
  }) => {
    if (!email && !wallet) throw new Error("At least one of email or wallet is required")

    const result = await request("POST", "/v1/subscribers", {
      email,
      wallet,
      sendWelcomeEmail
    })
    // Response may be { success: true } or include id, etc.
    return result
  }),

  /**
   * List subscribers (cursor-based pagination)
   */
  paragraph_listSubscribers: wrapTool(async ({
    limit = 10,
    cursor
  }) => {
    const params = { limit }
    if (cursor) params.cursor = cursor

    // Note: Endpoint does not require publicationId - API key scopes to a publication
    const result = await request("GET", "/v1/subscribers", null, params)
    return {
      subscribers: result.items || [],
      pagination: result.pagination || {}
    }
  }),

  /**
   * Import subscribers from CSV
   */
  paragraph_importSubscribers: wrapTool(async ({ csvPath, sendWelcomeEmail = true }) => {
    if (!csvPath) throw new Error("csvPath is required")

    const fs = await import('fs')
    const csvBuffer = fs.readFileSync(csvPath)

    // Build URL with query param
    const url = new URL(`${API_BASE}/v1/subscribers/import`)
    url.searchParams.append('sendWelcomeEmail', sendWelcomeEmail)

    const formData = new FormData()
    formData.append('file', csvBuffer, 'subscribers.csv')

    const response = await fetch(url.toString(), {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${process.env.PARAGRAPH_API_KEY}`
        // Content-type (with boundary) set automatically by fetch when using FormData
      },
      body: formData
    })

    if (!response.ok) {
      let errorMsg = `HTTP ${response.status} ${response.statusText}`
      try {
        const errorData = await response.json()
        errorMsg = errorData.msg || errorData.message || errorData.error || errorMsg
      } catch (e) {}
      throw new Error(errorMsg)
    }

    if (response.status === 204) {
      return { imported: 0, skipped: 0, total: 0 }
    }

    const result = await response.json()
    return {
      imported: result.imported || 0,
      skipped: result.skipped || 0,
      total: result.total || 0
    }
  }),

  /**
   * Get coin (tokenized post) by ID
   */
  paragraph_getCoin: wrapTool(async ({ coinId }) => {
    if (!coinId) throw new Error("coinId is required")
    const result = await request("GET", `/v1/coins/${coinId}`)
    return result
  }),

  /**
   * Get coin by contract address
   */
  paragraph_getCoinByContract: wrapTool(async ({ contractAddress }) => {
    if (!contractAddress) throw new Error("contractAddress is required")
    const result = await request("GET", `/v1/coins/contract/${contractAddress}`)
    return result
  }),

  /**
   * Get popular coins
   */
  paragraph_getPopularCoins: wrapTool(async () => {
    const result = await request("GET", "/v1/coins/list/popular")
    return result.coins || result.items || result
  }),

  /**
   * List coin holders
   */
  paragraph_listCoinHolders: wrapTool(async ({
    coinId,
    limit = 50,
    cursor
  }) => {
    if (!coinId) throw new Error("coinId is required")
    const params = { limit }
    if (cursor) params.cursor = cursor

    const result = await request("GET", `/v1/coins/${coinId}/holders`, null, params)
    return {
      holders: result.holders || [],
      pagination: result.pagination || {}
    }
  }),

  /**
   * Get user by ID
   */
  paragraph_getUser: wrapTool(async ({ userId }) => {
    if (!userId) throw new Error("userId is required")
    const result = await request("GET", `/v1/users/${userId}`)
    return result
  }),

  /**
   * Get user by wallet address
   */
  paragraph_getUserByWallet: wrapTool(async ({ walletAddress }) => {
    if (!walletAddress) throw new Error("walletAddress is required")
    const result = await request("GET", `/v1/users/wallet/${walletAddress}`)
    return result
  }),

  /**
   * Get subscriber count for a publication (by ID)
   */
  paragraph_getSubscriberCount: wrapTool(async ({ publicationId }) => {
    if (!publicationId) throw new Error("publicationId is required")
    const result = await request("GET", `/v1/publications/${publicationId}/subscribers/count`)
    return { count: result.count }
  }),

  /**
   * Get feed (curated posts) - public, no auth required
   */
  paragraph_getFeed: wrapTool(async ({ limit = 20, cursor }) => {
    const params = { limit }
    if (cursor) params.cursor = cursor
    const result = await request("GET", "/v1/posts/feed", null, params)
    return {
      posts: result.items || [],
      pagination: result.pagination || {}
    }
  }),

  /**
   * Get posts by tag
   */
  paragraph_getPostsByTag: wrapTool(async ({ tag, limit = 20, cursor }) => {
    if (!tag) throw new Error("tag is required")
    const params = { limit }
    if (cursor) params.cursor = cursor
    const result = await request("GET", `/v1/posts/tag/${encodeURIComponent(tag)}`, null, params)
    return {
      posts: result.items || [],
      pagination: result.pagination || {}
    }
  })
}

export default tools
