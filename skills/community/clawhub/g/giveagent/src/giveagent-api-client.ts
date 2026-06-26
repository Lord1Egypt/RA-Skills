import { sanitizePostContent } from "./sanitizer.js";
import { createRateLimiter } from "./rate-limiter.js";

// ---------------------------------------------------------------------------
// Error Types
// ---------------------------------------------------------------------------

export class GiveAgentApiError extends Error {
  constructor(
    message: string,
    public statusCode: number,
    public endpoint: string,
  ) {
    super(message);
    this.name = "GiveAgentApiError";
  }
}

export class RateLimitExceededError extends Error {
  constructor(action: string) {
    super(`Rate limit exceeded for ${action}`);
    this.name = "RateLimitExceededError";
  }
}

// ---------------------------------------------------------------------------
// API Types
// ---------------------------------------------------------------------------

export interface ListingsParams {
  postType?: "GIVING" | "WANT";
  category?: string;
  city?: string;
  status?: string;
  limit?: number;
  offset?: number;
}

export interface Listing {
  id: string;
  userId: string;
  userName?: string;
  postType: "GIVING" | "WANT";
  status: string;
  item?: string;
  condition?: string;
  category?: string;
  size?: string;
  pickupMethod?: string;
  photoUrl?: string;
  notes?: string;
  availableUntil?: string;
  lookingFor?: string;
  keywords?: string[];
  location?: { city: string; country: string; postalPrefix: string };
  claimedBy?: string;
  createdAt: string;
  updatedAt: string;
}

export interface CreateListingData {
  postType: "GIVING" | "WANT";
  item?: string;
  condition?: string;
  category?: string;
  size?: string;
  pickupMethod?: string;
  photoUrl?: string;
  notes?: string;
  availableUntil?: string;
  lookingFor?: string;
  keywords?: string[];
  location: { city: string; country: string; postalPrefix: string };
}

export interface UpdateListingData {
  status?: string;
  claimedBy?: string;
}

export interface WantItem {
  id: string;
  query: string;
  keywords: string[];
  category?: string;
  status: string;
  priority: string;
  createdAt: string;
}

export interface CreateWantItemData {
  query: string;
  keywords: string[];
  category?: string;
  priority?: string;
}

export interface MatchResult {
  listingId: string;
  wantItemId: string;
  score: number;
  matchedOn: string[];
  listing: Listing;
}

export interface Match {
  id: string;
  giverId: string;
  claimerId: string;
  listingId: string;
  wantItemId?: string;
  state: string;
  pickupDetails?: Record<string, unknown>;
  expiresAt: string;
  createdAt: string;
}

export interface InitiateMatchData {
  listingId: string;
  wantItemId?: string;
}

export interface UpdateMatchData {
  state: string;
  pickupDetails?: Record<string, unknown>;
}

export interface Message {
  id: string;
  matchId: string;
  fromUserId: string;
  toUserId: string;
  messageType: string;
  content: string;
  read: boolean;
  createdAt: string;
}

export interface SendMessageData {
  matchId: string;
  toUserId: string;
  messageType: string;
  content: string;
}

// ---------------------------------------------------------------------------
// Client Interface
// ---------------------------------------------------------------------------

export interface GiveAgentApiClient {
  // Listings
  getListings(params: ListingsParams): Promise<Listing[]>;
  getListing(id: string): Promise<Listing>;
  createListing(data: CreateListingData): Promise<Listing>;
  updateListing(id: string, data: UpdateListingData): Promise<Listing>;

  // Want Items
  getWantItems(): Promise<WantItem[]>;
  createWantItem(data: CreateWantItemData): Promise<WantItem>;
  deleteWantItem(id: string): Promise<void>;

  // Matches
  findMatches(wantItemId: string): Promise<MatchResult[]>;
  initiateMatch(data: InitiateMatchData): Promise<Match>;
  updateMatch(id: string, data: UpdateMatchData): Promise<Match>;
  approveMatch(id: string, pickupDetails?: Record<string, unknown>): Promise<Match>;
  confirmMatchCompletion(id: string): Promise<Match>;

  // Messages
  getMessages(matchId?: string): Promise<Message[]>;
  sendMessage(data: SendMessageData): Promise<Message>;

  // Images
  uploadImage(file: Blob, filename: string): Promise<{ url: string }>;
}

// ---------------------------------------------------------------------------
// Factory
// ---------------------------------------------------------------------------

/**
 * Create an authenticated GiveAgent API client.
 *
 * The client applies:
 * - Sliding-window rate limiting (100 req/min)
 * - Content sanitization on all API responses
 * - 15-second request timeout via AbortSignal.timeout
 * - Authorization: Bearer header on every request
 */
export function createGiveAgentApiClient(config: {
  baseUrl: string;
  apiKey: string;
}): GiveAgentApiClient {
  const { baseUrl, apiKey } = config;
  const rateLimiter = createRateLimiter();

  const defaultHeaders: Record<string, string> = {
    Authorization: `Bearer ${apiKey}`,
    "Content-Type": "application/json",
    Accept: "application/json",
  };

  /**
   * Core fetch wrapper — adds auth headers, timeout, rate-limit recording,
   * and translates HTTP error statuses into GiveAgentApiError.
   */
  async function request<T>(
    method: string,
    path: string,
    body?: unknown,
    headers?: Record<string, string>,
  ): Promise<T> {
    if (!rateLimiter.canMakeRequest()) {
      throw new RateLimitExceededError("request");
    }
    rateLimiter.recordRequest();

    const url = `${baseUrl}${path}`;
    const init: RequestInit = {
      method,
      headers: { ...defaultHeaders, ...headers },
      signal: AbortSignal.timeout(15000),
    };

    if (body !== undefined) {
      // Don't stringify if body is FormData
      if (body instanceof FormData) {
        init.body = body;
        // Remove Content-Type to let browser set multipart boundary
        const headersObj = init.headers as Record<string, string>;
        delete headersObj["Content-Type"];
      } else {
        init.body = JSON.stringify(body);
      }
    }

    let response: Response;
    try {
      response = await fetch(url, init);
    } catch (err) {
      const message = err instanceof Error ? err.message : String(err);
      throw new Error(`Network error calling ${method} ${path}: ${message}`);
    }

    if (!response.ok) {
      let errorMessage: string;
      try {
        const errorBody = (await response.json()) as { message?: string; error?: string };
        errorMessage = errorBody.message ?? errorBody.error ?? response.statusText;
      } catch {
        errorMessage = response.statusText;
      }
      throw new GiveAgentApiError(
        `${method} ${path} failed: ${errorMessage}`,
        response.status,
        path,
      );
    }

    // Handle void responses (DELETE)
    if (response.status === 204 || response.headers.get("content-length") === "0") {
      return undefined as T;
    }

    return response.json() as Promise<T>;
  }

  // ---------------------------------------------------------------------------
  // Sanitization helpers
  // ---------------------------------------------------------------------------

  function sanitizeListing(listing: Listing): Listing {
    return {
      ...listing,
      item: listing.item ? sanitizePostContent(listing.item) : listing.item,
      notes: listing.notes ? sanitizePostContent(listing.notes) : listing.notes,
      lookingFor: listing.lookingFor
        ? sanitizePostContent(listing.lookingFor)
        : listing.lookingFor,
    };
  }

  function sanitizeWantItem(wantItem: WantItem): WantItem {
    return {
      ...wantItem,
      query: sanitizePostContent(wantItem.query),
    };
  }

  function sanitizeMessage(message: Message): Message {
    return {
      ...message,
      content: sanitizePostContent(message.content),
    };
  }

  function sanitizeMatchResult(result: MatchResult): MatchResult {
    return {
      ...result,
      listing: sanitizeListing(result.listing),
    };
  }

  // ---------------------------------------------------------------------------
  // Client Methods: Listings
  // ---------------------------------------------------------------------------

  async function getListings(params: ListingsParams): Promise<Listing[]> {
    const query = new URLSearchParams();
    if (params.postType) query.set("post_type", params.postType);
    if (params.category) query.set("category", params.category);
    if (params.city) query.set("city", params.city);
    if (params.status) query.set("status", params.status);
    if (params.limit !== undefined) query.set("limit", String(params.limit));
    if (params.offset !== undefined) query.set("offset", String(params.offset));

    const qs = query.toString();
    const path = qs ? `/api/v1/listings?${qs}` : "/api/v1/listings";
    const listings = await request<Listing[]>("GET", path);
    return listings.map(sanitizeListing);
  }

  async function getListing(id: string): Promise<Listing> {
    const listing = await request<Listing>("GET", `/api/v1/listings/${encodeURIComponent(id)}`);
    return sanitizeListing(listing);
  }

  async function createListing(data: CreateListingData): Promise<Listing> {
    const listing = await request<Listing>("POST", "/api/v1/listings", data);
    return sanitizeListing(listing);
  }

  async function updateListing(id: string, data: UpdateListingData): Promise<Listing> {
    const listing = await request<Listing>(
      "PATCH",
      `/api/v1/listings/${encodeURIComponent(id)}`,
      data,
    );
    return sanitizeListing(listing);
  }

  // ---------------------------------------------------------------------------
  // Client Methods: Want Items
  // ---------------------------------------------------------------------------

  async function getWantItems(): Promise<WantItem[]> {
    const wantItems = await request<WantItem[]>("GET", "/api/v1/want-items");
    return wantItems.map(sanitizeWantItem);
  }

  async function createWantItem(data: CreateWantItemData): Promise<WantItem> {
    const wantItem = await request<WantItem>("POST", "/api/v1/want-items", data);
    return sanitizeWantItem(wantItem);
  }

  async function deleteWantItem(id: string): Promise<void> {
    await request<void>("DELETE", `/api/v1/want-items/${encodeURIComponent(id)}`);
  }

  // ---------------------------------------------------------------------------
  // Client Methods: Matches
  // ---------------------------------------------------------------------------

  async function findMatches(wantItemId: string): Promise<MatchResult[]> {
    const results = await request<MatchResult[]>(
      "POST",
      "/api/v1/matches/find",
      { want_item_id: wantItemId },
    );
    return results.map(sanitizeMatchResult);
  }

  async function initiateMatch(data: InitiateMatchData): Promise<Match> {
    return request<Match>("POST", "/api/v1/matches", data);
  }

  async function updateMatch(id: string, data: UpdateMatchData): Promise<Match> {
    return request<Match>("PATCH", `/api/v1/matches/${encodeURIComponent(id)}`, data);
  }

  async function approveMatch(id: string, pickupDetails?: Record<string, unknown>): Promise<Match> {
    const body = pickupDetails ? { pickup_details: pickupDetails } : undefined;
    return request<Match>("POST", `/api/v1/matches/${encodeURIComponent(id)}/approve`, body);
  }

  async function confirmMatchCompletion(id: string): Promise<Match> {
    return request<Match>("POST", `/api/v1/matches/${encodeURIComponent(id)}/confirm-completion`);
  }

  // ---------------------------------------------------------------------------
  // Client Methods: Messages
  // ---------------------------------------------------------------------------

  async function getMessages(matchId?: string): Promise<Message[]> {
    const query = matchId ? `?match_id=${encodeURIComponent(matchId)}` : "";
    const messages = await request<Message[]>("GET", `/api/v1/messages${query}`);
    return messages.map(sanitizeMessage);
  }

  async function sendMessage(data: SendMessageData): Promise<Message> {
    const message = await request<Message>("POST", "/api/v1/messages", data);
    return sanitizeMessage(message);
  }

  // ---------------------------------------------------------------------------
  // Client Methods: Images
  // ---------------------------------------------------------------------------

  async function uploadImage(file: Blob, filename: string): Promise<{ url: string }> {
    const formData = new FormData();
    formData.append("file", file, filename);

    return request<{ url: string }>("POST", "/api/v1/images/upload", formData);
  }

  // ---------------------------------------------------------------------------
  // Return Client
  // ---------------------------------------------------------------------------

  return {
    getListings,
    getListing,
    createListing,
    updateListing,
    getWantItems,
    createWantItem,
    deleteWantItem,
    findMatches,
    initiateMatch,
    updateMatch,
    approveMatch,
    confirmMatchCompletion,
    getMessages,
    sendMessage,
    uploadImage,
  };
}
