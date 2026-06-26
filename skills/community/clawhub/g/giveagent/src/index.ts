/**
 * GiveAgent Skill Entry Point
 *
 * Registers all handlers with the OpenClaw runtime:
 * - give: Create giving posts
 * - want: Manage want list
 * - browse: Search for matches
 * - match: Coordinate pickups
 *
 * Sets up heartbeat for auto-scanning and DM routing for match coordination.
 */

import { createStorage } from "./storage.js";
import { createGiveAgentApiClient } from "./giveagent-api-client.js";
import { createRateLimiter } from "./rate-limiter.js";
import { createGiveHandler } from "./give.js";
import { createWantHandler } from "./want.js";
import { createBrowseHandler, createScanOnceHandler } from "./browse.js";
import { createMatchHandler } from "./match.js";
import { parseGivingPost } from "./parser.js";
import type { SkillRegistrar, SkillContext, UserConfig, MatchRequest } from "./types.js";

/**
 * Register GiveAgent skill with the OpenClaw runtime.
 *
 * Config resolution: passed-in config overrides stored config.
 * Required fields: giveagentApiKey, agentId, defaultLocation.
 */
export async function registerSkill(
  registrar: SkillRegistrar,
  config?: Partial<UserConfig>,
): Promise<void> {
  // ---- Load and merge config ----

  const storage = createStorage();
  const storedConfig = await storage.getConfig();
  const merged: UserConfig = { ...storedConfig, ...config };

  // Validate required fields
  const errors: string[] = [];

  // API key and agent ID must be non-empty after trim
  if (!merged.giveagentApiKey || merged.giveagentApiKey.trim() === "") {
    errors.push("giveagentApiKey must be a non-empty string");
  }
  if (!merged.agentId || merged.agentId.trim() === "") {
    errors.push("agentId must be a non-empty string");
  }

  // Validate API URL
  if (!merged.giveagentApiUrl || merged.giveagentApiUrl.trim() === "") {
    errors.push("giveagentApiUrl must be a non-empty string");
  } else {
    try {
      new URL(merged.giveagentApiUrl);
    } catch {
      errors.push(`giveagentApiUrl must be a valid URL (got: ${merged.giveagentApiUrl})`);
    }
  }

  // Validate scan interval
  if (typeof merged.scanIntervalMs !== "number" || merged.scanIntervalMs <= 0) {
    errors.push(`scanIntervalMs must be a positive number (got: ${merged.scanIntervalMs})`);
  }

  // Validate max active wants and givings
  if (typeof merged.maxActiveWants !== "number" || merged.maxActiveWants < 1) {
    errors.push(`maxActiveWants must be >= 1 (got: ${merged.maxActiveWants})`);
  }
  if (typeof merged.maxActiveGivings !== "number" || merged.maxActiveGivings < 1) {
    errors.push(`maxActiveGivings must be >= 1 (got: ${merged.maxActiveGivings})`);
  }

  // Validate default location
  if (!merged.defaultLocation) {
    errors.push("defaultLocation is required");
  } else {
    if (!merged.defaultLocation.city || merged.defaultLocation.city.trim() === "") {
      errors.push("defaultLocation.city must be a non-empty string");
    }
    if (!merged.defaultLocation.country || merged.defaultLocation.country.trim() === "") {
      errors.push("defaultLocation.country must be a non-empty string");
    }
    if (!merged.defaultLocation.postalPrefix || merged.defaultLocation.postalPrefix.trim() === "") {
      errors.push("defaultLocation.postalPrefix must be a non-empty string");
    }
  }

  // Throw all validation errors at once
  if (errors.length > 0) {
    throw new Error("GiveAgent config validation failed:\n  - " + errors.join("\n  - "));
  }

  // ---- Create shared infrastructure ----

  const apiClient = createGiveAgentApiClient({
    baseUrl: merged.giveagentApiUrl,
    apiKey: merged.giveagentApiKey,
  });
  const rateLimiter = createRateLimiter();

  // ---- Create handlers ----

  const giveHandler = createGiveHandler({
    apiKey: merged.giveagentApiKey,
    baseUrl: merged.giveagentApiUrl,
    defaultLocation: merged.defaultLocation,
    defaultPickup: merged.defaultPickup,
  });

  const wantHandler = createWantHandler({
    apiKey: merged.giveagentApiKey,
    baseUrl: merged.giveagentApiUrl,
    defaultLocation: merged.defaultLocation,
  });

  const browseHandler = createBrowseHandler({
    apiKey: merged.giveagentApiKey,
    baseUrl: merged.giveagentApiUrl,
  });

  const scanOnceHandler = createScanOnceHandler({
    apiKey: merged.giveagentApiKey,
    baseUrl: merged.giveagentApiUrl,
  });

  const matchHandler = createMatchHandler({
    apiKey: merged.giveagentApiKey,
    baseUrl: merged.giveagentApiUrl,
    agentId: merged.agentId,
  });

  // ---- Register "give" command ----

  registrar.register({
    name: "give",
    triggers: ["give away", "giving", "giveaway", "donate"],
    handler: async (ctx: SkillContext) => {
      await giveHandler(ctx);
    },
  });

  // ---- Register "want" command ----

  registrar.register({
    name: "want",
    triggers: ["want", "looking for", "need", "searching for"],
    handler: async (ctx: SkillContext) => {
      const message = ctx.userMessage.toLowerCase();

      if (message.includes("list") || message.includes("my wants")) {
        await wantHandler.listWants(ctx);
      } else if (message.includes("remove") || message.includes("cancel")) {
        const idMatch = message.match(/(?:remove|cancel)\s+(\S+)/);
        const wantId = idMatch?.[1];

        if (!wantId) {
          await ctx.reply("❌ Please specify the want ID to remove. Example: 'remove abc123'");
          return;
        }

        await wantHandler.removeWant(ctx, wantId);
      } else {
        await wantHandler.handleWant(ctx);
      }
    },
  });

  // ---- Register "browse" command ----

  registrar.register({
    name: "browse",
    triggers: ["browse", "scan", "search", "check posts"],
    handler: async (ctx: SkillContext) => {
      await scanOnceHandler(ctx);
    },
  });

  // ---- Register "match" command ----

  registrar.register({
    name: "match",
    triggers: ["match", "claim", "accept", "approve", "confirm pickup", "complete"],
    handler: async (ctx: SkillContext) => {
      const message = ctx.userMessage.toLowerCase();

      if (message.includes("claim") || message.includes("initiate")) {
        const postIdMatch = message.match(/(?:claim|initiate)\s+(\S+)/);
        const postId = postIdMatch?.[1];

        if (!postId) {
          await ctx.reply("❌ Please specify the post ID to claim. Example: 'claim post123'");
          return;
        }

        // Fetch the listing from GiveAgent API, parse it, and initiate match
        try {
          const listing = await apiClient.getListing(postId);

          if (!listing) {
            await ctx.reply(`❌ Post ${postId} not found. It may have been removed or expired.`);
            return;
          }

          // Convert API listing to GivingPost format
          const parsedPost = parseGivingPost(listing.notes || listing.item || "");

          // If parser failed, construct from listing data
          const givingPost = parsedPost || {
            postType: "GIVING" as const,
            item: listing.item || "Unknown item",
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

          // Attach metadata from the API listing (in case we used parsed post)
          givingPost.postId = listing.id;
          givingPost.author = listing.userId;

          // Find a matching want item, or create a transient one
          const wantList = await storage.getWantList();
          let wantItem = wantList.find(
            (w) =>
              w.status === "active" &&
              w.keywords.some((kw) =>
                givingPost.item.toLowerCase().includes(kw.toLowerCase()),
              ),
          );

          if (!wantItem) {
            // Create a transient want item for this claim
            wantItem = {
              id: `transient-${Date.now()}`,
              query: givingPost.item,
              keywords: givingPost.item.toLowerCase().split(/\s+/),
              added: new Date(),
              status: "active",
              priority: "medium",
            };
          }

          await matchHandler.initiateMatch(ctx, {
            wantItem,
            givingPost,
            score: 1.0,
            matchedOn: ["manual-claim"],
          });
        } catch (err) {
          const msg = err instanceof Error ? err.message : String(err);
          await ctx.reply(`❌ Failed to claim post ${postId}: ${msg}`);
        }
        return;
      }

      if (message.includes("accept")) {
        const postIdMatch = message.match(/accept\s+(\S+)/);
        const postId = postIdMatch?.[1];

        if (!postId) {
          await ctx.reply("❌ Please specify the post ID to accept. Example: 'accept post123'");
          return;
        }

        // Look up an existing match for this post ID
        const matches = await storage.getMatches();
        const match = matches.find(
          (m) => (m.postId === postId || m.id === postId) && m.state === "MATCH_REQUESTED",
        );

        if (!match) {
          await ctx.reply(
            `❌ No pending match request found for ${postId}. ` +
            `Use 'claim <postId>' to initiate a new match.`,
          );
          return;
        }

        // Construct a MatchRequest from the stored match
        const request: MatchRequest = {
          type: "MATCH_REQUEST",
          item: match.item,
          postId: match.postId,
          area: match.area || "unknown",
          available: match.available || "flexible",
        };

        await matchHandler.acceptMatch(ctx, request, match.counterpartAgentId);
        return;
      }

      if (message.includes("approve")) {
        const matchIdMatch = message.match(/approve\s+(\S+)/);
        const matchId = matchIdMatch?.[1];

        if (!matchId) {
          await ctx.reply("❌ Please specify the match ID to approve. Example: 'approve match123'");
          return;
        }

        await matchHandler.approveMatch(ctx, matchId);
        return;
      }

      if (message.includes("confirm pickup") || message.includes("pickup")) {
        const matchIdMatch = message.match(/(?:confirm pickup|pickup)\s+(\S+)/);
        const matchId = matchIdMatch?.[1];

        if (!matchId) {
          await ctx.reply("❌ Please specify the match ID. Example: 'confirm pickup match123'");
          return;
        }

        // Parse optional pickup details from the message
        // Expected format: "confirm pickup <matchId> at <address> on <date> at <time>"
        const addressMatch = message.match(/at\s+(.+?)(?:\s+on\s+|\s*$)/);
        const dateMatch = message.match(/on\s+(\S+)/);
        const timeMatch = message.match(/at\s+(\d{1,2}:\d{2}(?:\s*[ap]m)?)\s*$/i);

        const pickupDetails = {
          address: addressMatch?.[1] || "TBD",
          date: dateMatch?.[1] || "TBD",
          time: timeMatch?.[1] || "TBD",
        };

        await matchHandler.approveMatch(ctx, matchId, pickupDetails);
        return;
      }

      if (message.includes("complete") || message.includes("done")) {
        const matchIdMatch = message.match(/(?:complete|done)\s+(\S+)/);
        const matchId = matchIdMatch?.[1];

        if (!matchId) {
          await ctx.reply("❌ Please specify the match ID. Example: 'complete match123'");
          return;
        }

        const feedbackMatch = message.match(/feedback:\s*(.+)$/i);
        const feedback = feedbackMatch?.[1];

        await matchHandler.confirmCompletion(ctx, matchId, feedback);
        return;
      }

      // Default: show match help
      await ctx.reply(
        "🤝 Match coordination commands:\n\n" +
        "• claim <postId> — Initiate a match for a giving post\n" +
        "• accept <postId> — Accept an incoming match request\n" +
        "• approve <matchId> — Approve a match (human consent)\n" +
        "• confirm pickup <matchId> — Confirm pickup details\n" +
        "• complete <matchId> — Mark exchange as completed",
      );
    },
  });

  // ---- Register heartbeat for auto-scanning ----

  if (merged.autoScan) {
    let consecutiveErrors = 0;

    registrar.registerHeartbeat(merged.scanIntervalMs, async () => {
      try {
        await browseHandler();
        await matchHandler.cleanupExpiredMatches();
        // Reset error counter on success
        consecutiveErrors = 0;
      } catch (err) {
        consecutiveErrors++;
        console.error("[giveagent] Heartbeat error:", err);

        // Warn after 2+ consecutive failures
        if (consecutiveErrors >= 2) {
          console.warn(
            `[giveagent] WARNING: Auto-scan has failed ${consecutiveErrors} times in a row. ` +
            "This may require attention."
          );
        }
      }
    });
  }

  // ---- Register DM routing for match coordination ----

  if (registrar.registerDMHandler) {
    registrar.registerDMHandler(async (ctx, dm) => {
      await matchHandler.handleIncomingDM(ctx, dm);
    });
  }
}
