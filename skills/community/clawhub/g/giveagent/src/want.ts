import type { SkillContext, WantListItem, Category, Location } from "./types.js";
import { extractKeywords } from "./matcher.js";
import { formatWantPost, type WantPostInput } from "./formatter.js";
import { sanitizePostContent } from "./sanitizer.js";
import { createGiveAgentApiClient } from "./giveagent-api-client.js";
import { createStorage, type StorageManager } from "./storage.js";
import { randomUUID } from "crypto";

// ============================================
// Configuration
// ============================================

export interface WantHandlerConfig {
  apiKey: string;
  baseUrl: string;
  defaultLocation: Location;
}

// ============================================
// Category detection from keywords
// ============================================

/**
 * Detect category from keywords using common item patterns.
 */
function detectCategory(keywords: string[]): Category | undefined {
  const categoryPatterns: Record<Category, string[]> = {
    furniture: ["furniture", "couch", "sofa", "chair", "table", "desk", "bed", "dresser", "cabinet"],
    electronics: ["laptop", "computer", "phone", "tablet", "monitor", "tv", "television", "camera", "speaker"],
    clothing: ["shirt", "pants", "jacket", "shoes", "dress", "clothing", "clothes", "jeans", "sweater"],
    books: ["book", "novel", "textbook", "magazine", "comic", "dictionary"],
    kitchen: ["pot", "pan", "plate", "cup", "mug", "blender", "toaster", "knife", "fork"],
    kids: ["toy", "stroller", "crib", "highchair", "playpen", "doll", "puzzle"],
    sports: ["bike", "bicycle", "skateboard", "ball", "tennis", "golf", "weights", "yoga"],
    home: ["lamp", "rug", "curtain", "pillow", "blanket", "mirror", "frame"],
    garden: ["plant", "tool", "shovel", "rake", "hose", "pot", "seed"],
    office: ["printer", "keyboard", "mouse", "stapler", "folder", "binder", "calculator"],
    media: ["cd", "dvd", "vinyl", "record", "cassette", "vhs"],
    other: [],
  };

  for (const [category, patterns] of Object.entries(categoryPatterns)) {
    for (const pattern of patterns) {
      if (keywords.includes(pattern)) {
        return category as Category;
      }
    }
  }

  return undefined;
}

// ============================================
// Handler factory
// ============================================

export function createWantHandler(config: WantHandlerConfig) {
  /**
   * Handle "want" command - create a new want list item
   */
  async function handleWant(ctx: SkillContext): Promise<void> {
    try {
      const storage = createStorage();

      // Remove trigger words from query
      let query = ctx.userMessage.trim();
      const triggers = ["looking for", "searching for", "want", "need"];
      for (const trigger of triggers) {
        // Match trigger word followed by optional space (so "want" and "want " both match)
        const regex = new RegExp(`^${trigger}\\s*`, "i");
        const before = query;
        query = query.replace(regex, "").trim();
        // If we matched and removed the trigger, break
        if (query !== before) {
          break;
        }
      }

      if (!query || query === "") {
        await ctx.reply("❌ Please specify what you're looking for. Example: 'want a blue couch'");
        return;
      }

      // Extract keywords and filter out trigger words
      const rawKeywords = extractKeywords(query);
      const triggerWords = ["want", "need", "looking", "searching"];
      const keywords = rawKeywords.filter(kw => !triggerWords.includes(kw));

      if (keywords.length === 0) {
        await ctx.reply("❌ Could not extract meaningful keywords from your query. Please try again.");
        return;
      }

      // Detect category
      const category = detectCategory(keywords);

      // Create want list item
      const wantItem: WantListItem = {
        id: randomUUID(),
        query,
        keywords,
        category,
        added: new Date(),
        status: "active",
        priority: "medium",
      };

      // Save to storage
      await storage.addWantItem(wantItem);

      // Check if user wants to post publicly
      const shouldPost = /\b(post|announce|public)\b/i.test(ctx.userMessage);

      if (shouldPost) {
        // Create GiveAgent API client and post [WANT]
        const apiClient = createGiveAgentApiClient({
          baseUrl: config.baseUrl,
          apiKey: config.apiKey,
        });

        const wantPostInput: WantPostInput = {
          lookingFor: query,
          category: category || "other",
          location: config.defaultLocation,
          canPickup: "Flexible",
        };

        const formatted = formatWantPost(wantPostInput);
        const sanitized = sanitizePostContent(formatted);

        await apiClient.createListing({
          postType: "WANT",
          lookingFor: query,
          category: category || "other",
          location: config.defaultLocation,
          keywords,
        });

        await ctx.reply(
          `✅ Added to your want list and posted to GiveAgent!\n\n` +
          `🔎 ${query}\n` +
          `🏷️ Category: ${category || "other"}\n` +
          `🔑 Keywords: ${keywords.join(", ")}\n\n` +
          `Your agent will scan for matches and notify you.`
        );
      } else {
        await ctx.reply(
          `✅ Added to your want list!\n\n` +
          `🔎 ${query}\n` +
          `🏷️ Category: ${category || "other"}\n` +
          `🔑 Keywords: ${keywords.join(", ")}\n\n` +
          `Your agent will scan for matches and notify you. ` +
          `Add "post" to your message if you want to announce this publicly.`
        );
      }
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : String(err);
      await ctx.reply(`❌ Failed to add want item: ${errorMsg}`);
    }
  }

  /**
   * List all active wants
   */
  async function listWants(ctx: SkillContext): Promise<void> {
    try {
      const storage = createStorage();
      const wants = await storage.getWantList();

      const activeWants = wants.filter((w) => w.status === "active");

      if (activeWants.length === 0) {
        await ctx.reply("📋 Your want list is empty. Use 'want [item]' to add something!");
        return;
      }

      const lines = ["📋 Your active want list:\n"];

      for (const want of activeWants) {
        const priority = want.priority === "high" ? "🔴" : want.priority === "medium" ? "🟡" : "🟢";
        const category = want.category ? `#${want.category}` : "";
        lines.push(`${priority} ${want.query} ${category}`);
        lines.push(`   Keywords: ${want.keywords.join(", ")}`);
        lines.push(`   Added: ${want.added.toLocaleDateString()}\n`);
      }

      await ctx.reply(lines.join("\n"));
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : String(err);
      await ctx.reply(`❌ Failed to list wants: ${errorMsg}`);
    }
  }

  /**
   * Remove a want from the list
   */
  async function removeWant(ctx: SkillContext, wantId: string): Promise<void> {
    try {
      const storage = createStorage();
      const wants = await storage.getWantList();

      const want = wants.find((w) => w.id === wantId);

      if (!want) {
        await ctx.reply(`❌ Want not found with ID: ${wantId}`);
        return;
      }

      await storage.removeWantItem(wantId);
      await ctx.reply(`✅ Removed "${want.query}" from your want list.`);
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : String(err);
      await ctx.reply(`❌ Failed to remove want: ${errorMsg}`);
    }
  }

  return {
    handleWant,
    listWants,
    removeWant,
  };
}
