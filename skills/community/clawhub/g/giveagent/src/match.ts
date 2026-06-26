/**
 * Match coordination state machine.
 *
 * Manages the 4-stage privacy-preserving match flow:
 * 1. MATCH_REQUESTED    — Claimer requests match (waitlist: multiple per listing OK)
 * 2. MATCH_ACCEPTED     — Giver picks one (only 1 active per listing)
 * 3. BOTH_APPROVED      — Both humans approve via /approve (optional pickup_details)
 * 4. COMPLETED          — Human confirms handoff (remaining waitlist auto-cancelled)
 *
 * Agents negotiate via messages after MATCH_ACCEPTED. Each outbound message
 * must be human-reviewed. Addresses shared in negotiation messages only.
 *
 * Handles both giver and claimer roles with state persistence.
 */

import type {
  SkillContext,
  MatchState,
  MatchResult,
  MatchRequest,
  MatchAccepted,
  PickupConfirmed,
  Completed,
  IncomingDM,
} from "./types.js";
import {
  formatMatchRequest,
  formatMatchAccepted,
  formatPickupConfirmed,
  formatCompleted,
  formatClaimedPost,
} from "./formatter.js";
import { createGiveAgentApiClient } from "./giveagent-api-client.js";
import { createStorage, type ActiveMatch } from "./storage.js";

export interface MatchConfig {
  apiKey: string;
  baseUrl: string;
  agentId: string;
}

/**
 * Parse a DM message to extract structured data.
 * Returns null if the message is not a recognized protocol message.
 */
function parseDM(content: string): MatchRequest | MatchAccepted | PickupConfirmed | Completed | null {
  const lines = content.split("\n").map(line => line.trim());

  // Detect message type from first line
  const firstLine = lines[0] || "";

  if (firstLine.includes("[MATCH REQUEST]")) {
    const item = extractDMField(content, "Item");
    const postId = extractDMField(content, "Post");
    const matchId = extractDMField(content, "Match");
    const area = extractDMField(content, "My area");
    const available = extractDMField(content, "Available");
    const message = extractDMField(content, "Message");

    if (!item || !postId || !area || !available) return null;

    return {
      type: "MATCH_REQUEST",
      item,
      postId,
      matchId: matchId || undefined,
      area,
      available,
      message: message || undefined,
    };
  }

  if (firstLine.includes("[MATCH ACCEPTED]")) {
    const item = extractDMField(content, "Item");
    const postId = extractDMField(content, "Post");
    const area = extractDMField(content, "My area");
    const available = extractDMField(content, "Available");

    if (!item || !postId || !area || !available) return null;

    return {
      type: "MATCH_ACCEPTED",
      item,
      postId,
      area,
      available,
    };
  }

  if (firstLine.includes("[PICKUP CONFIRMED]")) {
    const item = extractDMField(content, "Item");
    const pickup = extractDMField(content, "Pickup");
    const date = extractDMField(content, "Date");
    const time = extractDMField(content, "Time");
    const contact = extractDMField(content, "Contact");
    const notes = extractDMField(content, "Notes");

    if (!item || !pickup || !date || !time) return null;

    return {
      type: "PICKUP_CONFIRMED",
      item,
      pickup,
      date,
      time,
      contact: contact || undefined,
      notes: notes || undefined,
    };
  }

  if (firstLine.includes("[COMPLETED]")) {
    const item = extractDMField(content, "Item");
    const dateMatch = content.match(/Exchange completed on (.+)/);
    const date = dateMatch?.[1]?.trim();
    const feedback = extractDMField(content, "Feedback");

    if (!item || !date) return null;

    return {
      type: "COMPLETED",
      item,
      date,
      feedback: feedback || undefined,
    };
  }

  return null;
}

/**
 * Extract a field value from a DM message.
 * Similar to parser.ts extractField but without emoji handling.
 */
function extractDMField(content: string, fieldName: string): string | null {
  const lines = content.split("\n");
  const pattern = new RegExp(`^[\\s🆔📦📍🕐📝⏳📅📱⭐]*${fieldName}\\s*:\\s*(.+)$`, "i");

  for (const line of lines) {
    const trimmed = line.trim();
    const match = trimmed.match(pattern);
    if (match) {
      return match[1]!.trim();
    }
  }
  return null;
}

/**
 * Create a match handler that manages both giver and claimer flows.
 */
export function createMatchHandler(config: MatchConfig) {
  const apiClient = createGiveAgentApiClient({
    baseUrl: config.baseUrl,
    apiKey: config.apiKey,
  });
  const storage = createStorage();

  /**
   * Initiate a match as the claimer (WANT side).
   * Sends a [MATCH REQUEST] DM to the giving agent.
   */
  async function initiateMatch(
    ctx: SkillContext,
    matchResult: MatchResult
  ): Promise<void> {
    const { givingPost, wantItem } = matchResult;

    if (!givingPost.author) {
      throw new Error("Cannot initiate match: giving post has no author");
    }

    if (!givingPost.postId) {
      throw new Error("Cannot initiate match: giving post has no postId");
    }

    // Create active match record
    const matchId = `match-${Date.now()}-${Math.random().toString(36).slice(2, 9)}`;
    const now = new Date();
    const expiresAt = new Date(now.getTime() + 48 * 60 * 60 * 1000); // 48 hours

    const match: ActiveMatch = {
      id: matchId,
      wantItemId: wantItem.id,
      givingPostId: givingPost.postId,
      counterpartAgentId: givingPost.author,
      state: "MATCH_REQUESTED",
      role: "claimer",
      item: givingPost.item,
      postId: givingPost.postId,
      area: givingPost.location.city,
      createdAt: now,
      updatedAt: now,
      expiresAt,
    };

    // Create match via API first to get the API match ID
    const apiMatch = await apiClient.initiateMatch({
      listingId: givingPost.postId,
      wantItemId: wantItem.id,
    });

    // Store local match with API match ID
    match.apiMatchId = apiMatch.id;
    await storage.addMatch(match);

    // Format message including the API match ID so the giver can accept it
    const messageContent = formatMatchRequest({
      item: givingPost.item,
      postId: givingPost.postId,
      matchId: apiMatch.id,
      area: givingPost.location.city,
      available: "flexible", // TODO: Get from user config
      message: `I'm interested in your ${givingPost.item}. My agent will coordinate pickup if you accept.`,
    });

    // Send message
    await apiClient.sendMessage({
      matchId: apiMatch.id,
      toUserId: givingPost.author,
      messageType: "MATCH_REQUEST",
      content: messageContent,
    });

    await ctx.reply(
      `✅ Match request sent to @${givingPost.author} for ${givingPost.item}. Waiting for their response.`
    );
  }

  /**
   * Accept a match as the giver (GIVING side).
   * Finds the existing API match and transitions it to MATCH_ACCEPTED.
   * Sends a [MATCH ACCEPTED] DM to the claimer.
   */
  async function acceptMatch(
    ctx: SkillContext,
    request: MatchRequest,
    fromAgentId: string
  ): Promise<void> {
    // Find the existing local match (created by handleIncomingDM)
    const matches = await storage.getMatches();
    const existingMatch = matches.find(
      m => m.postId === request.postId &&
           m.counterpartAgentId === fromAgentId &&
           m.state === "MATCH_REQUESTED" &&
           m.role === "giver"
    );

    const apiMatchId = existingMatch?.apiMatchId || request.matchId;
    if (!apiMatchId) {
      await ctx.reply(
        `❌ Cannot accept: no API match ID found for this request. ` +
        `The claimer's agent may need to re-send the match request.`
      );
      return;
    }

    // Accept the existing match via API (MATCH_REQUESTED → MATCH_ACCEPTED)
    await apiClient.updateMatch(apiMatchId, { state: "MATCH_ACCEPTED" });

    // Update local match state
    if (existingMatch) {
      await storage.updateMatchState(existingMatch.id, "MATCH_ACCEPTED");
    } else {
      // No local record yet — create one
      const now = new Date();
      const match: ActiveMatch = {
        id: `match-${Date.now()}-${Math.random().toString(36).slice(2, 9)}`,
        apiMatchId,
        wantItemId: "",
        givingPostId: request.postId,
        counterpartAgentId: fromAgentId,
        state: "MATCH_ACCEPTED",
        role: "giver",
        item: request.item,
        postId: request.postId,
        area: request.area,
        available: request.available,
        createdAt: now,
        updatedAt: now,
        expiresAt: new Date(now.getTime() + 48 * 60 * 60 * 1000),
      };
      await storage.addMatch(match);
    }

    // Send [MATCH ACCEPTED] message via API
    const messageContent = formatMatchAccepted({
      item: request.item,
      postId: request.postId,
      area: request.area || "unknown",
      available: request.available || "flexible",
    });

    await apiClient.sendMessage({
      matchId: apiMatchId,
      toUserId: fromAgentId,
      messageType: "MATCH_ACCEPTED",
      content: messageContent,
    });

    await ctx.reply(
      `✅ Match accepted for ${request.item}. Waiting for human approval on both sides.`
    );
  }

  /**
   * Request human approval for a match (Stage 3).
   * Called after both agents have agreed to coordinate.
   */
  async function requestHumanApproval(
    ctx: SkillContext,
    match: ActiveMatch
  ): Promise<void> {
    const roleText = match.role === "giver" ? "give away" : "receive";
    const message = `🤝 Match pending approval:\n\n` +
      `Item: ${match.item}\n` +
      `You will ${roleText} this item.\n` +
      `Area: ${match.area || "unknown"}\n` +
      `Available: ${match.available || "flexible"}\n\n` +
      `Reply "approve ${match.id}" to proceed, or "reject ${match.id}" to cancel.`;

    await ctx.reply(message);
  }

  /**
   * Approve a match after human consent.
   * Calls POST /approve with optional pickup_details.
   * When both parties approve → BOTH_APPROVED.
   */
  async function approveMatch(
    ctx: SkillContext,
    matchId: string,
    pickupDetails?: {
      address: string;
      date: string;
      time: string;
      contact?: string;
      notes?: string;
    }
  ): Promise<void> {
    const matches = await storage.getMatches();
    const match = matches.find(m => m.id === matchId);

    if (!match) {
      throw new Error(`Match ${matchId} not found`);
    }

    if (match.state === "EXPIRED" || match.expiresAt.getTime() < Date.now()) {
      throw new Error("Match has expired");
    }

    // Call /approve with optional pickup_details
    const result = await apiClient.approveMatch(
      match.id,
      pickupDetails as unknown as Record<string, unknown> | undefined,
    );

    if (pickupDetails) {
      await storage.updateMatch(matchId, { pickupDetails });

      // Send PICKUP_CONFIRMED message to counterpart
      const messageContent = formatPickupConfirmed({
        item: match.item,
        pickup: pickupDetails.address,
        date: pickupDetails.date,
        time: pickupDetails.time,
        contact: pickupDetails.contact,
        notes: pickupDetails.notes,
      });

      await apiClient.sendMessage({
        matchId: match.id,
        toUserId: match.counterpartAgentId,
        messageType: "PICKUP_CONFIRMED",
        content: messageContent,
      });
    }

    if (result.state === "BOTH_APPROVED") {
      await storage.updateMatchState(matchId, "BOTH_APPROVED");
      await ctx.reply(
        `✅ Both parties approved pickup for ${match.item}. ` +
        `Reply "completed ${match.id}" after the exchange.`
      );
    } else {
      await storage.updateMatchState(matchId, "MATCH_ACCEPTED");
      await ctx.reply(
        `✅ You approved pickup for ${match.item}. Waiting for the other party to approve.`
      );
    }
  }

  /**
   * Mark a match as completed (Stage 5).
   * Sends [COMPLETED] DM and updates the giving post to [CLAIMED].
   */
  async function confirmCompletion(
    ctx: SkillContext,
    matchId: string,
    feedback?: string
  ): Promise<void> {
    const matches = await storage.getMatches();
    const match = matches.find(m => m.id === matchId);

    if (!match) {
      throw new Error(`Match ${matchId} not found`);
    }

    // Confirm completion via API (BOTH_APPROVED -> COMPLETED)
    await apiClient.confirmMatchCompletion(match.id);

    // Update local match state
    await storage.updateMatchState(matchId, "COMPLETED");

    // Send [COMPLETED] message via API
    const messageContent = formatCompleted({
      item: match.item,
      date: new Date().toISOString().slice(0, 10),
      feedback,
    });

    await apiClient.sendMessage({
      matchId: match.id,
      toUserId: match.counterpartAgentId,
      messageType: "COMPLETED",
      content: messageContent,
    });

    // Update listing to claimed status
    if (match.role === "giver") {
      try {
        await apiClient.updateListing(match.postId, {
          status: "claimed",
          claimedBy: match.counterpartAgentId,
        });
      } catch (err) {
        console.error(`Failed to update listing ${match.postId}:`, err);
      }
    }

    await ctx.reply(
      `🎉 Match completed! Thank you for using GiveAgent. The post has been marked as [CLAIMED].`
    );

    // Update stats
    if (match.role === "giver") {
      await storage.incrementStat("totalGiven");
    } else {
      await storage.incrementStat("totalReceived");
    }
    await storage.incrementStat("totalMatches");
  }

  /**
   * Handle incoming DM from another agent.
   * Routes to appropriate handler based on message type.
   */
  async function handleIncomingDM(ctx: SkillContext, dm: IncomingDM): Promise<void> {
    const parsed = parseDM(dm.content);

    if (!parsed) {
      // Not a protocol message, ignore
      return;
    }

    try {
      switch (parsed.type) {
        case "MATCH_REQUEST": {
          // Store a local match record so the "accept" command can find it
          const now = new Date();
          const localMatchId = `match-${Date.now()}-${Math.random().toString(36).slice(2, 9)}`;
          const localMatch: ActiveMatch = {
            id: localMatchId,
            apiMatchId: parsed.matchId,
            wantItemId: "",
            givingPostId: parsed.postId,
            counterpartAgentId: dm.from,
            state: "MATCH_REQUESTED",
            role: "giver",
            item: parsed.item,
            postId: parsed.postId,
            area: parsed.area,
            available: parsed.available,
            createdAt: now,
            updatedAt: now,
            expiresAt: new Date(now.getTime() + 48 * 60 * 60 * 1000),
          };
          await storage.addMatch(localMatch);

          await ctx.reply(
            `📨 New match request from @${dm.from}:\n\n` +
            `Item: ${parsed.item}\n` +
            `Their area: ${parsed.area}\n` +
            `Available: ${parsed.available}\n` +
            (parsed.message ? `Message: ${parsed.message}\n` : "") +
            `\nReply "accept ${parsed.postId}" to accept this match.`
          );
          break;
        }

        case "MATCH_ACCEPTED": {
          const matches = await storage.getMatches();
          const match = matches.find(
            m => m.postId === parsed.postId && m.counterpartAgentId === dm.from
          );

          if (match) {
            await storage.updateMatchState(match.id, "MATCH_ACCEPTED");
            await requestHumanApproval(ctx, match);
          }
          break;
        }

        case "PICKUP_CONFIRMED": {
          const matches = await storage.getMatches();
          const match = matches.find(
            m => m.item === parsed.item && m.counterpartAgentId === dm.from
          );

          if (match) {
            await ctx.reply(
              `📅 Pickup proposed:\n\n` +
              `Item: ${parsed.item}\n` +
              `Location: ${parsed.pickup}\n` +
              `Date: ${parsed.date}\n` +
              `Time: ${parsed.time}\n` +
              (parsed.contact ? `Contact: ${parsed.contact}\n` : "") +
              (parsed.notes ? `Notes: ${parsed.notes}\n` : "") +
              `\nReply "approve ${match.id}" to approve, or "completed ${match.id}" after the exchange.`
            );
          }
          break;
        }

        case "COMPLETED": {
          const matches = await storage.getMatches();
          const match = matches.find(
            m => m.item === parsed.item && m.counterpartAgentId === dm.from
          );

          if (match) {
            await storage.updateMatchState(match.id, "COMPLETED");
            await ctx.reply(
              `✅ Exchange completed for ${parsed.item}. Thank you!` +
              (parsed.feedback ? `\n\nFeedback: ${parsed.feedback}` : "")
            );
          }
          break;
        }
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : String(err);
      console.error(`[match] Error handling DM from ${dm.from}:`, errorMessage);
    }
  }

  /**
   * Cleanup expired matches (called periodically).
   */
  async function cleanupExpiredMatches(): Promise<void> {
    const matches = await storage.getMatches();
    const now = Date.now();

    for (const match of matches) {
      if (
        match.state !== "COMPLETED" &&
        match.state !== "CANCELLED" &&
        match.expiresAt.getTime() < now
      ) {
        await storage.updateMatchState(match.id, "EXPIRED");
        await storage.incrementStat("totalExpired");
        console.log(`[match] Expired match ${match.id} for item: ${match.item}`);
      }
    }
  }

  return {
    initiateMatch,
    acceptMatch,
    requestHumanApproval,
    approveMatch,
    confirmCompletion,
    handleIncomingDM,
    cleanupExpiredMatches,
  };
}
