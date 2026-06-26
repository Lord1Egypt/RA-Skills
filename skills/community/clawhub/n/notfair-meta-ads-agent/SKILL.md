---
name: notfair-meta-ads-agent
description: "NotFair Meta Ads agent for OpenClaw. Diagnose live Meta Ads accounts across Facebook and Instagram, audit spend and delivery, inspect campaigns/ad sets/ads/creatives, draft budget/status/creative fixes, and propose approval-gated changes through NotFair's hosted MCP server: https://notfair.co/meta-ads-mcp"
homepage: https://notfair.co/meta-ads-mcp
author: NotFair
license: MIT
category: advertising
subcategory: meta-ads
keywords:
  - meta-ads
  - facebook-ads
  - instagram-ads
  - paid-social
  - social-ads
  - advertising
  - mcp
  - openclaw
  - notfair
  - campaign-management
  - ad-sets
  - creatives
  - wasted-spend
tags:
  - meta-ads
  - facebook-ads
  - instagram-ads
  - advertising
  - mcp
  - openclaw
metadata:
  openclaw:
    emoji: "NF"
    install:
      - id: openclaw-notfair
        kind: node
        label: "NotFair Meta Ads Plugin"
---

# NotFair Meta Ads Agent

Use this skill when the user asks to manage, audit, diagnose, or optimize Meta Ads / Facebook Ads / Instagram Ads through NotFair.

Powered by [NotFair's hosted Meta Ads MCP server](https://notfair.co/meta-ads-mcp).

## Setup

    openclaw plugins install clawhub:openclaw-notfair
    openclaw plugins enable openclaw-notfair
    openclaw config set 'plugins.entries.openclaw-notfair.config.mcpUrl' '"https://notfair.co/api/mcp/meta_ads"' --strict-json
    openclaw notfair login
    openclaw notfair status

If the plugin is not authenticated, ask the user to run `openclaw notfair login`. If Meta Ads is not connected, send them to [NotFair Meta Ads setup](https://notfair.co/connect/meta-ads).

## Available OpenClaw Tools

- listAdAccounts - list Meta ad accounts connected to this session.
- runScript - run sandboxed JavaScript against the Meta Marketing API for broad audits and cross-surface analysis.
- getAdAccount - inspect account currency, timezone, spend cap, status, balance, and Business Manager context.
- getInsights - pull performance insights at account, campaign, ad set, or ad level.
- listCampaigns - list campaigns with status, objective, budget, bid strategy, schedule, and timestamps.
- listAdSets - list ad sets with targeting, optimization goal, budget, schedule, and promoted object.
- listAds - list ads with parent campaign/ad set ids and creative envelopes.
- listPages - list manageable Facebook Pages for ad creative `object_story_spec.page_id`.
- getPagePostInsights - compare boosted-post ad performance with aggregate Page post engagement.
- Write tools: pauseCampaign, enableCampaign, pauseAdSet, enableAdSet, pauseAd, enableAd, updateCampaignBudget, updateAdSetBudget, renameCampaign, renameAd, createCampaign, createAdSet, createAdCreative, createAd, updateCampaign, updateAdSet, updateAdCreative.

## Safety Model

- Read-only analysis can run without extra approval.
- Any Meta Ads write must be explicitly approved by the user before execution.
- Treat budget increases, campaign/ad set/ad creation, enabling delivery, bid changes, targeting changes, and creative swaps as external money-affecting side effects.
- Prefer creating paused/draft entities when a tool supports it.
- Never delete or remove entities unless the user explicitly requests the destructive action and confirms scope.
- For boosted Page-post ads, `pauseAd` may fail because Meta blocks status changes on the boosted post ad object. Pause the parent ad set instead and explain the limitation.
- Budget values from Meta are commonly in the account's minor currency units (for example cents for USD); convert before showing the user.

## Default Workflow

1. Call listAdAccounts when account context is unclear.
2. Use runScript for broad account audits, waste analysis, creative inspection, or campaign × ad set × ad × insight correlation.
3. Use typed point tools for narrow queries: getInsights, listCampaigns, listAdSets, listAds, getAdAccount, listPages, and getPagePostInsights.
4. Present findings and proposed actions before any write.
5. After an approved write, verify the resulting Meta Ads state with the relevant read tool.

## Example Read-Only Script

    const campaigns = await ads.graphParallel([
      {
        path: `/${ads.accountId}/campaigns`,
        params: {
          fields: "id,name,status,effective_status,objective,daily_budget,lifetime_budget,bid_strategy,updated_time",
          limit: 100
        }
      },
      {
        path: `/${ads.accountId}/insights`,
        params: {
          level: "campaign",
          date_preset: "last_30d",
          fields: "campaign_id,campaign_name,spend,impressions,clicks,ctr,cpc,cpm,actions",
          limit: 100
        }
      }
    ]);

    return campaigns;
