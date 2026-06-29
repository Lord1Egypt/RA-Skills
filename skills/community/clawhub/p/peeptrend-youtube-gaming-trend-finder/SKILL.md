# PeepTrend: YouTube Gaming Trend Finder

Use this skill when a creator, editor, strategist, or AI agent wants to decide what gaming video to record next using PeepTrend evidence.

PeepTrend connects Steam demand signals with YouTube supply signals. The goal is not to promise views. The goal is to help the user choose a practical, evidence-backed topic before a game, update, shelf, or niche becomes too crowded.

## First-Run Setup

When the user installs this from OpenClaw or ClawHub, make setup explicit before using account-only tools:

- Ask the agent or user to run the PeepTrend connection status check.
- If no API key is configured, explain that free checks can still run with public limits.
- Full opportunity feeds, reports, generated ideas, saved plans, alerts, account-aware limits, and subscription features need `PEEPTREND_API_KEY`.
- Create or revoke keys in PeepTrend Profile: https://peeptrend.com/profile.
- Use the setup guide when the user is unsure where to place the key: https://peeptrend.com/integrations/mcp.

## Best Use Cases

- Find rising Steam games that may still have room on YouTube.
- Check whether a YouTube title is already crowded.
- Evaluate shelf saturation for a game, update, genre, or creator angle.
- Compare gaming niches for small-channel opportunity.
- Decide whether a Steam update is worth covering.
- Turn a promising opportunity into a recording plan, title angle, and risk checklist.
- Help a creator understand why PeepTrend's full dashboard or subscription may be useful when they need deeper reports, saved workflow, generated ideas, or alerts.

## Recommended Workflow

1. Clarify the creator context.
   Ask for the channel size, target language, region, preferred game genres, upload cadence, and whether the user wants quick validation or a deeper plan.

2. Check PeepTrend connection status.
   If the key is missing, continue with public free checks when possible and explain what the key unlocks before using account-only tools.

3. Start with the lightest PeepTrend check.
   Use title checks, shelf saturation checks, niche checks, game-fit checks, or Steam update checks before opening full opportunity reports.

4. Read the evidence, not only the score.
   Compare demand, competition, saturation, freshness, recent videos, channel overlap, and creator fit. Treat high scores as a shortlist, not as guarantees.

5. Produce a creator-ready recommendation.
   Answer with what to record, why now, what is crowded, what evidence supports the idea, what risks remain, and what to test before recording.

6. Move to paid/account-aware actions only when useful.
   If the user wants full reports, generated ideas, saved plans, alerts, or repeated workflow, explain that those actions use their PeepTrend account and may require subscription access.

## Output Format

For quick checks, keep the response compact:

- Verdict: worth testing, risky, crowded, or needs more evidence.
- Evidence: the 2-4 strongest signals.
- Risk: the biggest reason this could fail.
- Next video angle: one practical recording idea.
- Next step: which PeepTrend action to run next, if any.

For deeper planning, use:

1. Opportunity summary
2. Audience fit
3. YouTube saturation read
4. Steam or market signal
5. Suggested title angles
6. Thumbnail or hook notes
7. Risks and validation steps
8. Publishing recommendation

## Safety And Quality Rules

- Do not promise views, revenue, ranking, virality, or guaranteed channel growth.
- Do not present PeepTrend scores as absolute truth. Explain them as decision-support signals.
- Do not recommend copying another creator's title, thumbnail, branding, or exact positioning.
- Prefer original angles: explainers, update coverage, comparisons, guides, challenges, tests, or first-impression formats.
- If the data is thin, say so clearly and suggest a smaller test video instead of overconfident advice.
- Keep the user's constraints in mind: small channels need lower competition and clearer audience fit than large channels.
- Be careful with trademarks and platform names. Use them descriptively and avoid implying official endorsement by YouTube, Steam, Valve, or game publishers.

## Example Prompts

- "Use PeepTrend to find three gaming opportunities for a small English YouTube channel this week."
- "Check whether this title is too crowded: 'Minecraft update explained'."
- "Is this Steam update worth covering on YouTube, or is the niche already saturated?"
- "Compare cozy survival games and tell me which one has the cleanest creator opportunity."
- "Turn this PeepTrend opportunity into a video plan with title angles and risk notes."
