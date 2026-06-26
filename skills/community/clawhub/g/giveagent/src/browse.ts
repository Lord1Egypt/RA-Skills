/**
 * Browse handler — periodic scanner for matching [GIVING] and [WANT] posts.
 *
 * Runs as a heartbeat every 4 hours (configurable), fetching recent posts
 * from m/giveagent and notifying the user of matches against their want list
 * and inventory.
 */

import type { SkillContext, GivingPost, WantPost, MatchResult } from "./types.js";
import { sanitizePostContent } from "./sanitizer.js";
import { parsePost, isExpired } from "./parser.js";
import { findMatches, findReverseMatches } from "./matcher.js";
import { createGiveAgentApiClient } from "./giveagent-api-client.js";
import { createStorage } from "./storage.js";

export interface BrowseConfig {
  apiKey: string;
  baseUrl: string;
}

/**
 * Create a heartbeat handler that periodically scans for matches.
 * Intended for registration via SkillRegistrar.registerHeartbeat().
 */
export function createBrowseHandler(config: BrowseConfig) {
  const apiClient = createGiveAgentApiClient({
    baseUrl: config.baseUrl,
    apiKey: config.apiKey,
  });
  const storage = createStorage();

  return async function browse(): Promise<void> {
    try {
      // Load seen posts to avoid duplicates
      const seenPostIds = await storage.getSeenPostIds();

      // Load user's want list and inventory
      const wantList = await storage.getWantList();
      const inventory = await storage.getInventory();

      // Fetch recent [GIVING] listings from GiveAgent API
      const rawListings = await apiClient.getListings({
        postType: "GIVING",
        limit: 100,
      });

      // Convert API listings to GivingPost format
      const givingPosts: GivingPost[] = [];
      for (const listing of rawListings) {
        // Skip already-seen posts
        if (seenPostIds.has(listing.id)) {
          continue;
        }

        // Convert listing to GivingPost
        const givingPost: GivingPost = {
          postType: "GIVING",
          item: listing.item || "Unknown",
          condition: (listing.condition as any) || "Good",
          category: (listing.category as any) || "other",
          location: listing.location || { city: "Unknown", country: "Unknown", postalPrefix: "" },
          size: (listing.size as any) || "Medium",
          pickup: (listing.pickupMethod as any) || "Flexible",
          photoUrl: listing.photoUrl,
          notes: listing.notes,
          availableUntil: listing.availableUntil ? new Date(listing.availableUntil) : new Date(),
          postId: listing.id,
          author: listing.userId,
          createdAt: new Date(listing.createdAt),
        };

        if (!isExpired(givingPost)) {
          givingPosts.push(givingPost);
        }

        // Mark as seen regardless of parse success
        await storage.markPostSeen(listing.id);
      }

      // Find matches against want list
      const matches = findMatches(wantList, givingPosts);

      // Log match results (in production, this would notify user via ctx.reply)
      if (matches.length > 0) {
        console.log(`[browse] Found ${matches.length} new matches:`);
        for (const match of matches) {
          console.log(
            `  - ${match.givingPost.item} (score: ${match.score}, matched on: ${match.matchedOn.join(", ")})`
          );
        }
      } else {
        console.log(`[browse] No new matches found in this scan.`);
      }

      // Fetch recent [WANT] listings for reverse matching
      const rawWantListings = await apiClient.getListings({
        postType: "WANT",
        limit: 100,
      });

      const wantPosts: WantPost[] = [];
      for (const listing of rawWantListings) {
        // Skip already-seen posts
        if (seenPostIds.has(listing.id)) {
          continue;
        }

        // Convert listing to WantPost
        const wantPost: WantPost = {
          postType: "WANT",
          lookingFor: listing.lookingFor || "Unknown",
          category: (listing.category as any) || "other",
          location: listing.location || { city: "Unknown", country: "Unknown", postalPrefix: "" },
          canPickup: (listing.pickupMethod as any) || "Flexible",
          notes: listing.notes,
          postId: listing.id,
          author: listing.userId,
          createdAt: new Date(listing.createdAt),
        };

        wantPosts.push(wantPost);
        await storage.markPostSeen(listing.id);
      }

      // Find reverse matches (inventory items that match want posts)
      const reverseMatches = findReverseMatches(inventory, wantPosts);

      if (reverseMatches.length > 0) {
        console.log(`[browse] Found ${reverseMatches.length} reverse matches:`);
        for (const match of reverseMatches) {
          console.log(
            `  - ${match.wantItem.query} wants your ${match.givingPost.item} (score: ${match.score})`
          );
        }
      }
    } catch (err) {
      console.error(`[browse] Scan failed:`, err);
      // Don't throw — heartbeat should continue on errors
    }
  };
}

/**
 * Create a handler for manual "browse" command.
 * Runs a single scan immediately when invoked by the user.
 */
export function createScanOnceHandler(config: BrowseConfig) {
  const apiClient = createGiveAgentApiClient({
    baseUrl: config.baseUrl,
    apiKey: config.apiKey,
  });
  const storage = createStorage();

  return async function scanOnce(ctx: SkillContext): Promise<void> {
    try {
      await ctx.reply("🔍 Scanning GiveAgent for matches...");

      // Load seen posts to avoid duplicates
      const seenPostIds = await storage.getSeenPostIds();

      // Load user's want list and inventory
      const wantList = await storage.getWantList();
      const inventory = await storage.getInventory();

      // Fetch recent [GIVING] listings
      const rawListings = await apiClient.getListings({
        postType: "GIVING",
        limit: 100,
      });

      const givingPosts: GivingPost[] = [];
      let newPostCount = 0;

      for (const listing of rawListings) {
        const isNew = !seenPostIds.has(listing.id);
        if (isNew) newPostCount++;

        // Convert listing to GivingPost
        const givingPost: GivingPost = {
          postType: "GIVING",
          item: listing.item || "Unknown",
          condition: (listing.condition as any) || "Good",
          category: (listing.category as any) || "other",
          location: listing.location || { city: "Unknown", country: "Unknown", postalPrefix: "" },
          size: (listing.size as any) || "Medium",
          pickup: (listing.pickupMethod as any) || "Flexible",
          photoUrl: listing.photoUrl,
          notes: listing.notes,
          availableUntil: listing.availableUntil ? new Date(listing.availableUntil) : new Date(),
          postId: listing.id,
          author: listing.userId,
          createdAt: new Date(listing.createdAt),
        };

        if (!isExpired(givingPost)) {
          givingPosts.push(givingPost);
        }

        if (isNew) {
          await storage.markPostSeen(listing.id);
        }
      }

      // Find matches against want list
      const matches = findMatches(wantList, givingPosts);

      if (matches.length === 0) {
        await ctx.reply(
          `✅ Scan complete. Checked ${newPostCount} new posts, no matches found.`
        );
      } else {
        let message = `🎉 Found ${matches.length} ${matches.length === 1 ? "match" : "matches"}!\n\n`;

        for (const match of matches.slice(0, 5)) {
          // Show top 5 matches
          const { givingPost, score, matchedOn } = match;
          message += `📦 **${givingPost.item}**\n`;
          message += `   Condition: ${givingPost.condition}\n`;
          message += `   Location: ${givingPost.location.city}, ${givingPost.location.country}\n`;
          message += `   Score: ${score} (matched on: ${matchedOn.join(", ")})\n`;
          message += `   Post: ${givingPost.postId}\n\n`;
        }

        if (matches.length > 5) {
          message += `... and ${matches.length - 5} more matches.\n`;
        }

        await ctx.reply(message);
      }

      // Fetch recent [WANT] listings for reverse matching
      const rawWantListings = await apiClient.getListings({
        postType: "WANT",
        limit: 100,
      });

      const wantPosts: WantPost[] = [];
      for (const listing of rawWantListings) {
        const isNew = !seenPostIds.has(listing.id);

        // Convert listing to WantPost
        const wantPost: WantPost = {
          postType: "WANT",
          lookingFor: listing.lookingFor || "Unknown",
          category: (listing.category as any) || "other",
          location: listing.location || { city: "Unknown", country: "Unknown", postalPrefix: "" },
          canPickup: (listing.pickupMethod as any) || "Flexible",
          notes: listing.notes,
          postId: listing.id,
          author: listing.userId,
          createdAt: new Date(listing.createdAt),
        };

        wantPosts.push(wantPost);

        if (isNew) {
          await storage.markPostSeen(listing.id);
        }
      }

      // Find reverse matches
      const reverseMatches = findReverseMatches(inventory, wantPosts);

      if (reverseMatches.length > 0) {
        let message = `\n🔄 Also found ${reverseMatches.length} people looking for your items:\n\n`;

        for (const match of reverseMatches.slice(0, 3)) {
          message += `🔎 Someone wants: **${match.wantItem.query}**\n`;
          message += `   Your item: ${match.givingPost.item}\n`;
          message += `   Score: ${match.score}\n\n`;
        }

        if (reverseMatches.length > 3) {
          message += `... and ${reverseMatches.length - 3} more.\n`;
        }

        await ctx.reply(message);
      }
    } catch (err) {
      const errorMessage =
        err instanceof Error ? err.message : String(err);
      await ctx.reply(`❌ Scan failed: ${errorMessage}`);
    }
  };
}
