import type {ExplainerPlan} from "./scene-types";

export const samplePlan: ExplainerPlan = {
  title: "How SmartSync Works",
  subtitle: "Real-time collaboration made simple",
  ctaText: "Try SmartSync Free",
  ctaUrl: "https://example.com/signup",
  scenes: [
    {
      id: "context-01",
      stage: "context",
      durationInFrames: 90,
      headline: "Teams Are More Distributed Than Ever",
      subheadline: "67% of knowledge workers collaborate across time zones daily",
      voiceover:
        "Remote and hybrid teams are the new normal, but staying in sync across tools and time zones is harder than ever.",
      assetHint: "globe with connected nodes, soft blue gradient",
    },
    {
      id: "problem-01",
      stage: "problem",
      durationInFrames: 105,
      headline: "Updates Get Lost Between Apps",
      subheadline: "Average worker switches context 400 times per day",
      voiceover:
        "Critical updates get buried in email threads, scattered across Slack channels, and lost between project boards. The result? Duplicated work and missed deadlines.",
      assetHint: "chaotic grid of app icons with red notification badges",
    },
    {
      id: "mechanism-01",
      stage: "mechanism",
      durationInFrames: 120,
      headline: "One Feed, Every Update, Zero Noise",
      subheadline: "SmartSync connects your tools and filters what matters",
      voiceover:
        "SmartSync connects to your existing tools — Slack, Jira, Notion, GitHub — and surfaces only the updates relevant to you, in one unified feed.",
      assetHint: "clean dashboard UI showing unified feed from multiple sources",
    },
    {
      id: "benefits-01",
      stage: "benefits",
      durationInFrames: 120,
      headline: "Ship Faster, Stay Aligned",
      subheadline: "Teams using SmartSync report 40% fewer status meetings",
      voiceover:
        "Your team spends less time chasing updates and more time building. Fewer meetings, fewer misses, faster shipping.",
      assetHint: "team members collaborating with green checkmarks, upward chart",
    },
    {
      id: "next-step-01",
      stage: "next-step",
      durationInFrames: 90,
      headline: "Try SmartSync Free",
      subheadline: "No credit card required — 14-day full-access trial",
      voiceover:
        "Start your free trial today. No credit card required. See why thousands of teams trust SmartSync to stay in sync.",
      assetHint: "CTA button with subtle glow animation",
    },
  ],
};
