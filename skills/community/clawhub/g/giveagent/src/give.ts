import type { SkillContext, GivingPost, InventoryItem, Location, Category, Condition, Size, PickupMethod } from "./types.js";
import { createVisionProvider } from "./vision.js";
import { formatGivingPost, type GivingPostInput } from "./formatter.js";
import { sanitizePostContent, containsAddressLeak } from "./sanitizer.js";
import { createGiveAgentApiClient, type GiveAgentApiClient } from "./giveagent-api-client.js";
import { createStorage, type StorageManager } from "./storage.js";
import { parseCategory } from "./parser.js";
import { randomUUID } from "crypto";

// ============================================
// Configuration
// ============================================

export interface GiveHandlerConfig {
  apiKey: string;
  baseUrl: string;
  defaultLocation: Location;
  defaultPickup: PickupMethod;
}

// ============================================
// Simple message parser
// ============================================

interface ParsedGiveMessage {
  item: string;
  condition: Condition;
  category: Category;
  size: Size;
  notes?: string;
}

/**
 * Extract item details from user message.
 * Supports patterns like:
 * - "give blue couch in good condition"
 * - "giving away my old laptop"
 * - "I want to give a desk"
 */
function parseGiveMessage(message: string): Partial<ParsedGiveMessage> {
  const lowerMsg = message.toLowerCase();

  // Extract item name (everything after trigger words)
  const triggers = ["give", "giving", "giving away", "give away"];
  let item = "";

  for (const trigger of triggers) {
    const idx = lowerMsg.indexOf(trigger);
    if (idx !== -1) {
      const afterTrigger = message.substring(idx + trigger.length).trim();
      // Remove common prefixes like "my", "a", "an", "the"
      item = afterTrigger.replace(/^(my|a|an|the)\s+/i, "").trim();
      break;
    }
  }

  // If no trigger found, use whole message as item name
  if (!item) {
    item = message.trim();
  }

  // Extract condition keywords
  let condition: Condition | undefined;
  if (/\bnew\b/i.test(lowerMsg) && /\blike\s+new\b/i.test(lowerMsg)) {
    condition = "Like New";
  } else if (/\bnew\b/i.test(lowerMsg)) {
    condition = "New";
  } else if (/\bgood\b/i.test(lowerMsg)) {
    condition = "Good";
  } else if (/\bfair\b/i.test(lowerMsg)) {
    condition = "Fair";
  } else if (/\bfor\s+parts\b/i.test(lowerMsg)) {
    condition = "For Parts";
  }

  // Extract category keywords
  const categoryKeywords: Record<string, Category> = {
    furniture: "furniture",
    couch: "furniture",
    sofa: "furniture",
    chair: "furniture",
    table: "furniture",
    desk: "furniture",
    bed: "furniture",
    laptop: "electronics",
    computer: "electronics",
    phone: "electronics",
    tablet: "electronics",
    monitor: "electronics",
    tv: "electronics",
    television: "electronics",
    shirt: "clothing",
    pants: "clothing",
    jacket: "clothing",
    shoes: "clothing",
    dress: "clothing",
    clothing: "clothing",
    clothes: "clothing",
    book: "books",
    novel: "books",
    textbook: "books",
    pot: "kitchen",
    pan: "kitchen",
    plate: "kitchen",
    cup: "kitchen",
    mug: "kitchen",
    blender: "kitchen",
    toy: "kids",
    stroller: "kids",
    crib: "kids",
    bike: "sports",
    bicycle: "sports",
    skateboard: "sports",
    ball: "sports",
    lamp: "home",
    rug: "home",
    curtain: "home",
    plant: "garden",
    tool: "garden",
    shovel: "garden",
    printer: "office",
    keyboard: "office",
    mouse: "office",
    cd: "media",
    dvd: "media",
    vinyl: "media",
  };

  let category: Category | undefined;
  for (const [keyword, cat] of Object.entries(categoryKeywords)) {
    if (new RegExp(`\\b${keyword}\\b`, "i").test(lowerMsg)) {
      category = cat;
      break;
    }
  }

  // Extract size keywords
  let size: Size | undefined;
  if (/\bpocket\b/i.test(lowerMsg)) {
    size = "Pocket";
  } else if (/\bsmall\b/i.test(lowerMsg)) {
    size = "Small";
  } else if (/\bmedium\b/i.test(lowerMsg)) {
    size = "Medium";
  } else if (/\blarge\b/i.test(lowerMsg)) {
    size = "Large";
  } else if (/\bxl\b/i.test(lowerMsg) || /\bextra\s+large\b/i.test(lowerMsg)) {
    size = "XL";
  } else if (/\bfurniture\b/i.test(lowerMsg)) {
    size = "Furniture-sized";
  }

  return { item, condition, category, size };
}

// ============================================
// Handler factory
// ============================================

export function createGiveHandler(config: GiveHandlerConfig) {
  return async (ctx: SkillContext): Promise<void> => {
    try {
      const apiClient = createGiveAgentApiClient({
        baseUrl: config.baseUrl,
        apiKey: config.apiKey,
      });

      const storage = createStorage();

      // Parse message for item details
      const parsed = parseGiveMessage(ctx.userMessage);

      // Set defaults
      const item = parsed.item || "Unknown item";
      const condition = parsed.condition || "Good";
      const category = parsed.category || "other";
      const size = parsed.size || "Medium";
      let notes = parsed.notes;
      let photoUrl: string | undefined;

      // If photo available, use vision to describe it
      if (ctx.media && ctx.media.length > 0 && ctx.describeImage) {
        const visionProvider = createVisionProvider(ctx);
        try {
          const description = await visionProvider.describeItem(ctx.media[0]!.url);

          // Override with vision-detected values if available
          const visionItem = description.nameEn || description.name;
          const finalItem = visionItem && visionItem !== "Unknown item" ? visionItem : item;

          // Use vision notes if we didn't get item name from message
          if (!parsed.item || parsed.item === ctx.userMessage.trim()) {
            notes = description.notes || notes;
          }

          photoUrl = ctx.media[0]!.url;

          // Build the giving post with vision-enhanced data
          const givingPostInput: GivingPostInput = {
            item: finalItem,
            condition: description.condition || condition,
            category: description.category || category,
            location: config.defaultLocation,
            size: description.estimatedSize || size,
            pickup: config.defaultPickup,
            photoUrl,
            notes,
          };

          await processGivingPost(ctx, apiClient, storage, givingPostInput);
        } catch (err) {
          // Vision failed, continue with parsed values
          const givingPostInput: GivingPostInput = {
            item,
            condition,
            category,
            location: config.defaultLocation,
            size,
            pickup: config.defaultPickup,
            photoUrl,
            notes,
          };

          await processGivingPost(ctx, apiClient, storage, givingPostInput);
        }
      } else {
        // No photo, use parsed values
        const givingPostInput: GivingPostInput = {
          item,
          condition,
          category,
          location: config.defaultLocation,
          size,
          pickup: config.defaultPickup,
          notes,
        };

        await processGivingPost(ctx, apiClient, storage, givingPostInput);
      }
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : String(err);
      await ctx.reply(`❌ Failed to post your giving item: ${errorMsg}`);
    }
  };
}

/**
 * Process the giving post: format, sanitize, check for leaks, post to GiveAgent API, save to storage.
 */
async function processGivingPost(
  ctx: SkillContext,
  client: GiveAgentApiClient,
  storage: StorageManager,
  input: GivingPostInput
): Promise<void> {
  // Format the post
  const formatted = formatGivingPost(input);

  // Sanitize
  const sanitized = sanitizePostContent(formatted);

  // Check for address leaks
  if (containsAddressLeak(sanitized)) {
    await ctx.reply(
      "⚠️ Warning: Your post contains what looks like a street address or phone number. " +
      "For your privacy, please only share general area information (city/postal prefix) " +
      "until both parties have agreed to the exchange.\n\n" +
      "Please revise and try again."
    );
    return;
  }

  // Post to GiveAgent API
  const post = await client.createListing({
    postType: "GIVING",
    item: input.item,
    condition: input.condition,
    category: input.category,
    size: input.size,
    pickupMethod: input.pickup,
    photoUrl: input.photoUrl,
    notes: sanitized,
    availableUntil: new Date(Date.now() + 14 * 24 * 60 * 60 * 1000).toISOString(),
    location: input.location,
  });

  // Save to local inventory
  const inventoryItem: InventoryItem = {
    id: randomUUID(),
    postId: post.id,
    item: input.item,
    category: input.category,
    status: "active",
    postedAt: new Date(),
  };

  await storage.addInventoryItem(inventoryItem);

  // Increment stats
  await storage.incrementStat("totalGiven");

  // Reply with confirmation
  await ctx.reply(
    `✅ Posted your giving item to m/giveagent!\n\n` +
    `📦 ${input.item}\n` +
    `📋 ${input.condition}\n` +
    `🏷️ #${input.category}\n` +
    `📍 ${input.location.city}, ${input.location.country}\n\n` +
    `Your agent will monitor for matches and notify you when someone wants it.`
  );
}
