---
name: OMNI Research Verifier
id: omni-research-verifier
version: 1.0.0
category: Research & Analysis
author: OmniArchitect
tags: [research, verification, fact-checking, evidence, citations]
description: Autonomous verification engine that deconstructs claims, evaluates source credibility, and identifies contradictions.
dependencies:
  - requests>=2.31.0
  - beautifulsoup4>=4.12.0
  - duckduckgo_search>=4.2.0
usage: |
  Pass a single claim or a complex paragraph. The skill will return a structured JSON report
  detailing the veracity, evidence, and any conflicting information found.
example_input: "The global market for solid-state batteries will exceed $10B by 2030."
example_output:
  status: "success"
  confidence_score: 85
  executive_summary: "Consensus supports significant growth, though $10B is the high-end estimate."
  contradictions: ["Source B suggests supply chain issues may delay this to 2032."]
---

# OMNI Research Verifier

## Overview
This skill provides a high-assurance verification layer for agentic workflows. It is designed to be the "Truth Node" in a multi-agent system. Unlike standard search skills, OMNI Research Verifier doesn't just find sources — it evaluates them, scores them, and identifies contradictions.

## Problem It Solves
Large language models are prone to hallucinations and fabricated citations. This skill forces the agent to step outside its internal weights and verify every claim against a live, multi-source ground truth.

## How It Works

### 1. Claim Extraction
The skill deconstructs user input into individual claims that need verification.

### 2. Multi-Source Search
It queries across web and news sources simultaneously using the `duckduckgo_search` library.

### 3. Credibility Scoring
Each source is evaluated based on domain authority (.edu, .gov, .org get higher scores) and content quality.

### 4. Contradiction Detection
The skill scans for conflicting information across sources and flags them for user review.

### 5. Structured Report
Outputs a JSON report with:
- Executive Summary
- Evidence Table (source, credibility score, excerpt)
- Contradictions (if any)
- Formatted Citations
- Confidence Score (0-100)

## Installation

```bash
claw install omni-research-verifier

Usage

from omni_research_verifier import process

result = process("The Earth's core has stopped rotating.")
print(result)

Example Output

{
  "status": "success",
  "confidence_score": 85,
  "executive_summary": "Claim is Mixed based on 5 sources.",
  "contradictions": [
    "Potential conflict identified in https://example.com"
  ],
  "evidence_table": [
    {
      "source": "https://example.com",
      "title": "Earth's core rotation study",
      "snippet": "The Earth's core has slowed...",
      "score": 0.7,
      "timestamp": "2026-08-18"
    }
  ],
  "citations": [
    "Earth's core rotation study. (2026-08-18). Retrieved from https://example.com"
  ]
}

Technical Requirements

· Python 3.10+
· Internet connection for web search
· OpenClaw agent environment

Security Notes

· No API keys required (uses duckduckgo_search which is free and anonymous)
· No persistent storage of search results
· All searches are performed anonymously via DuckDuckGo

License

MIT-0 — Free to use, modify, and redistribute. No attribution required.

Support

For issues or suggestions, please open an issue on GitHub or contact the maintainer.

Changelog

Version 1.0.0 (2026-08-18)

· Initial release
· Multi-source search capability
· Credibility scoring engine
· Contradiction detection
· Structured JSON output