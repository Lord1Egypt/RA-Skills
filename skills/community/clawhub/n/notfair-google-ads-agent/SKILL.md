---
name: notfair-google-ads-agent
description: "NotFair Google Ads agent for OpenClaw. Diagnose live Google Ads accounts, audit wasted spend, review search terms, draft negative keywords, inspect policy errors, and propose approval-gated campaign changes through NotFair's hosted MCP server."
homepage: https://notfair.co
author: NotFair
license: MIT-0
category: advertising
subcategory: google-ads
keywords:
  - google-ads
  - ppc
  - sem
  - advertising
  - mcp
  - openclaw
  - notfair
  - campaign-management
  - wasted-spend
  - search-terms
  - negative-keywords
  - policy-errors
tags:
  - google-ads
  - advertising
  - mcp
  - openclaw
metadata:
  openclaw:
    emoji: "NF"
    install:
      - id: openclaw-notfair
        kind: node
        label: "NotFair Google Ads Plugin"
---

# NotFair Google Ads Agent

Use this skill when the user asks to manage, audit, diagnose, or optimize Google Ads through NotFair.

## Setup

    openclaw plugins install openclaw-notfair
    openclaw notfair login
    openclaw notfair connect
    openclaw notfair status

If the plugin is not authenticated, ask the user to run openclaw notfair login.

## Available OpenClaw Tools

- notfair_list_connected_accounts - list connected Google Ads accounts.
- notfair_run_script - run read-only JavaScript analysis against Google Ads data.
- notfair_google_ads_tool - call a specific NotFair MCP tool by exact name and JSON arguments.

## Safety Model

- Read-only analysis can run without extra approval.
- Any Google Ads write must be explicitly approved by the user before execution.
- Treat budget increases, campaign creation, campaign enabling, bid changes, and keyword/ad mutations as external money-affecting side effects.
- Prefer creating paused/draft changes when a tool supports it.
- Never delete or remove entities unless the user explicitly requests the destructive action and confirms scope.

## Default Workflow

1. Call notfair_list_connected_accounts when account context is unclear.
2. Use notfair_run_script for broad diagnosis and reporting.
3. Use notfair_google_ads_tool for specific NotFair tools such as keyword ideas, search term analysis, negative keywords, campaign updates, or policy-error fixes.
4. Present findings and proposed actions before writes.
5. After an approved write, verify the resulting Google Ads state.

## Example Read-Only Script

    const campaigns = await ads.gaql("SELECT campaign.id, campaign.name, campaign.status, metrics.cost_micros, metrics.clicks, metrics.conversions FROM campaign WHERE segments.date DURING LAST_30_DAYS ORDER BY metrics.cost_micros DESC LIMIT 20");
    return campaigns.rows.map((row) => ({
      id: row.campaign.id,
      name: row.campaign.name,
      status: row.campaign.status,
      spend: row.metrics.cost_micros / 1000000,
      clicks: row.metrics.clicks,
      conversions: row.metrics.conversions
    }));
