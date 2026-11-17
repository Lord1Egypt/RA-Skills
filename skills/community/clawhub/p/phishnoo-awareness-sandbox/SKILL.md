---
name: phishnoo-awareness-sandbox
description: Explore synthetic Phishnoo security-awareness metrics and submit example threat reports through the Phishnoo sandbox.
version: 1.0.0
homepage: https://phishnoo.com
metadata:
  openclaw:
    primaryEnv: PHISHNOO_SANDBOX_KEY
    requires:
      env:
        - PHISHNOO_SANDBOX_KEY
    envVars:
      - name: PHISHNOO_SANDBOX_KEY
        required: true
        description: Operator-issued Phishnoo sandbox key for synthetic data.
---

## About Phishnoo

[Phishnoo](https://phishnoo.com) is a cybersecurity awareness and social engineering defense platform for organizations. It combines realistic phishing simulations, short security training modules, and employee threat reporting. Employees practice spotting and reporting suspicious messages, while security teams track progress and see where more training is needed.

Phishnoo Academy helps employees build practical cybersecurity skills they can use at work. Phishnoo Radar turns user reports into a resource on emerging threats, and the P-Shield™ CyberSafe Index helps organizations measure workforce security awareness over time. Phishnoo also offers AI Exposure Testing to help teams understand how AI-enabled workplace systems respond to untrusted communications.

## Phishnoo Sandbox

The sandbox lets developers explore example awareness metrics and threat reporting workflows with synthetic data.

Use this skill when the user asks to inspect the Phishnoo sandbox or file a synthetic example report. Configure `PHISHNOO_SANDBOX_KEY` through the client's secret settings and send it only as `Authorization: Bearer <key>` to `https://api.phishnoo.nl`. Never include it in URLs, command arguments, reports, or output.

Connect over Streamable HTTP at `https://api.phishnoo.nl/mcp`. Use `get_me`, `get_scores`, `get_campaigns`, `get_progress`, and `get_threats` to read sandbox data. Use `report_threat` only when the user requests a write. Send a synthetic title and optional example URL without credentials, query, or fragment. Never send employee records, actual messages, or live customer data.

REST fallback: GET /v1/me, /v1/scores, /v1/campaigns, /v1/progress, /v1/threats; POST /v1/threats with JSON. See https://api.phishnoo.nl/docs.
