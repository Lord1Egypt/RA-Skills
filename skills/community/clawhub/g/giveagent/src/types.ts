// ============================================
// Post Types
// ============================================

export type PostType = "GIVING" | "WANT" | "CLAIMED" | "EXPIRED";

export type Category =
  | "furniture" | "electronics" | "clothing" | "books"
  | "kitchen" | "kids" | "sports" | "home"
  | "garden" | "office" | "media" | "other";

export type Condition = "New" | "Like New" | "Good" | "Fair" | "For Parts";

export type Size = "Pocket" | "Small" | "Medium" | "Large" | "XL" | "Furniture-sized";

export type PickupMethod = "Pickup Only" | "Can Ship Locally" | "Flexible";

export interface Location {
  city: string;
  country: string;
  postalPrefix: string;
}

export interface GivingPost {
  postType: "GIVING";
  item: string;
  condition: Condition;
  category: Category;
  location: Location;
  size: Size;
  pickup: PickupMethod;
  photoUrl?: string;
  notes?: string;
  availableUntil: Date;
  postId?: string;
  author?: string;
  createdAt?: Date;
}

export interface WantPost {
  postType: "WANT";
  lookingFor: string;
  category: Category;
  location: Location;
  sizeRange?: string;
  minCondition?: Condition;
  canPickup: PickupMethod;
  notes?: string;
  postId?: string;
  author?: string;
  createdAt?: Date;
}

export interface ClaimedPost {
  postType: "CLAIMED";
  item: string;
  matchedWith: string;
  pickupArranged: boolean;
  originalPostId: string;
}

export interface ExpiredPost {
  postType: "EXPIRED";
  item: string;
  reason: "withdrawn by owner" | "deadline passed" | "item discarded";
  originalPostId: string;
}

export type ParsedPost = GivingPost | WantPost | ClaimedPost | ExpiredPost;

// ============================================
// Want List & Inventory
// ============================================

export interface WantListItem {
  id: string;
  query: string;
  keywords: string[];
  category?: Category;
  location?: Location;
  maxDistance?: number;
  added: Date;
  status: "active" | "matched" | "fulfilled" | "cancelled";
  priority: "low" | "medium" | "high";
}

export interface InventoryItem {
  id: string;
  postId: string;
  item: string;
  category: Category;
  status: "active" | "claimed" | "expired" | "completed";
  postedAt: Date;
  claimedBy?: string;
  completedAt?: Date;
}

// ============================================
// Matching
// ============================================

export interface MatchResult {
  wantItem: WantListItem;
  givingPost: GivingPost;
  score: number;
  matchedOn: string[];
}

// ============================================
// DM Message Types (per protocol)
// ============================================

export interface MatchRequest {
  type: "MATCH_REQUEST";
  item: string;
  postId: string;
  matchId?: string;
  area: string;
  available: string;
  message?: string;
}

export interface MatchAccepted {
  type: "MATCH_ACCEPTED";
  item: string;
  postId: string;
  area: string;
  available: string;
}

export interface PickupConfirmed {
  type: "PICKUP_CONFIRMED";
  item: string;
  pickup: string;
  date: string;
  time: string;
  contact?: string;
  notes?: string;
}

export interface Completed {
  type: "COMPLETED";
  item: string;
  date: string;
  feedback?: string;
}

export type DMMessage = MatchRequest | MatchAccepted | PickupConfirmed | Completed;

// ============================================
// Match State Machine
// ============================================

export type MatchState =
  | "MATCH_REQUESTED"
  | "MATCH_ACCEPTED"
  | "BOTH_APPROVED"
  | "COMPLETED"
  | "EXPIRED"
  | "CANCELLED";

// ============================================
// Privacy
// ============================================

export type PrivacyStage = 1 | 2 | 3 | 4;

// ============================================
// User Config
// ============================================

export interface UserConfig {
  giveagentApiUrl: string;
  giveagentApiKey: string;
  agentId: string;
  defaultLocation: Location;
  defaultPickup: PickupMethod;
  autoScan: boolean;
  scanIntervalMs: number;
  maxActiveWants: number;
  maxActiveGivings: number;
  autoClaimEnabled: boolean;
}

// ============================================
// GiveAgent API Types
// ============================================

/**
 * GiveAgent REST API response types.
 * API hosted at api.giveagent.ai
 */
export interface MoltbookPost {
  id: string;
  submolt: string;
  title: string;
  content: string;
  author: string;
  created_at: string;
  updated_at: string;
  url?: string;
  media?: { url: string; type: string }[];
}

/**
 * ASSUMPTION: Moltbook DM API shape.
 * Conventional REST DM endpoint. Needs validation.
 */
export interface MoltbookDM {
  id: string;
  from: string;
  to: string;
  content: string;
  created_at: string;
  read: boolean;
}

export interface MoltbookComment {
  id: string;
  postId: string;
  author: string;
  content: string;
  created_at: string;
}

export interface MoltbookSubmolt {
  name: string;
  display_name: string;
  description: string;
  subscriber_count: number;
  created_at: string;
}

// ============================================
// API Parameters
// ============================================

export interface GetPostsParams {
  submolt: string;
  sort?: "new" | "hot" | "top";
  limit?: number;
  offset?: number;
  after?: string;
}

export interface GetDMsParams {
  unread?: boolean;
  limit?: number;
  after?: string;
}

// ============================================
// Rate Limiting
// ============================================

export interface RateLimitStatus {
  requestsRemaining: number;
  postsRemaining: number;
  resetAt: Date;
}

// ============================================
// OpenClaw Skill SDK Interface (STUBBED)
// ============================================

/**
 * Stubbed OpenClaw Skill SDK interface.
 * The real SDK is provided by the OpenClaw runtime at install time.
 */
export interface SkillContext {
  userMessage: string;
  media?: { url: string; mimeType: string; data?: Buffer }[];
  agentId: string;
  userId: string;
  reply: (message: string) => Promise<void>;
  describeImage?: (imageUrl: string) => Promise<string>;
  sendDM?: (recipientAgentId: string, message: string) => Promise<void>;
  onDMReceived?: (handler: (dm: IncomingDM) => Promise<void>) => void;
}

export interface IncomingDM {
  from: string;
  content: string;
  timestamp: string;
}

export interface SkillHandler {
  name: string;
  triggers: string[];
  handler: (ctx: SkillContext) => Promise<void>;
}

export interface SkillRegistrar {
  register: (handler: SkillHandler) => void;
  registerHeartbeat: (intervalMs: number, handler: () => Promise<void>) => void;
  registerDMHandler?: (handler: (ctx: SkillContext, dm: IncomingDM) => Promise<void>) => void;
}
