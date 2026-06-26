# Active Standards & Protocols Reference

*Last updated: 2026-04-02*

## Agent Communication Protocols

### A2A (Agent-to-Agent) — Google DeepMind
- **Status:** Published specification, active development
- **Version:** 0.2.x
- **Core concept:** HTTP-based protocol for agents to discover, communicate, and collaborate
- **Key primitives:** Agent Cards (.well-known/agent.json), Tasks, Messages, Parts
- **Adoption:** Growing — major LLM providers offering A2A endpoints
- **Spec:** https://google.github.io/A2A/

### MCP (Model Context Protocol) — Anthropic
- **Status:** Published specification, widely adopted
- **Version:** 2025-03-26 (current)
- **Core concept:** Standardized way for LLMs to access tools, resources, and prompts
- **Key primitives:** Tools, Resources, Prompts, Sampling
- **Adoption:** High — Claude Code, many third-party integrations
- **Spec:** https://spec.modelcontextprotocol.io/

### ACP (Agent Communication Protocol) — IBM
- **Status:** Draft specification
- **Core concept:** REST-based asynchronous agent communication for enterprise integration
- **Key difference from A2A:** Designed for async workflows vs. real-time task execution
- **Target audience:** Enterprise IT, integration teams
- **Status note:** Less adoption than A2A or MCP as of Q1 2026

### ANP (Agent Network Protocol) — Community/OpenAI-adjacent
- **Status:** Early proposal
- **Core concept:** Decentralized agent discovery and coordination
- **Status note:** Far less mature than A2A/MCP; watch for adoption signals

## Governance Standards

### NIST AI RMF (AI Risk Management Framework)
- **Status:** NIST AI RMF 1.0 published January 2023
- **Generative AI Profile:** NIST AI 600-1 draft — initial public draft released July 2024
- **Core structure:** Map, Measure, Manage, Govern (4 functions)
- **AI RMF Playbook:** Companion document with suggested actions
- **Agentic systems:** Not yet fully addressed in published version; active working group
- **Relevance:** De facto US standard for AI risk management

### EU AI Act
- **Status:** Fully in force August 2024
- **Risk tiers:** Unacceptable (banned) → High → Limited → Minimal
- **High-risk AI:** Credit, employment, biometrics, critical infrastructure, law enforcement
- **General Purpose AI Models (GPAI):** New requirements for foundation model providers
- **Key deadline:** High-risk system requirements apply from August 2026
- **Enforcement:** EU AI Office + national market surveillance authorities
- **Fines:** Up to €35M or 7% global revenue for most serious violations

### OWASP LLM Top 10
- **Status:** Published, version 1.1 (2025 update)
- **Top threats:**
  1. Prompt Injection
  2. Sensitive Information Disclosure
  3. Supply Chain Vulnerabilities
  4. Data and Model Poisoning
  5. Improper Output Handling
  6. Excessive Agency
  7. System Prompt Leakage
  8. Vector and Embedding Weaknesses
  9. Misinformation
  10. Unbounded Consumption
- **Agentic risk note:** "Excessive Agency" (#6) is the most relevant for multi-agent systems

### ISO/IEC 42001 (AI Management Systems)
- **Status:** Published December 2023
- **Core concept:** ISO 9001-style management system standard for AI
- **Certification:** Available from accredited bodies
- **Adoption:** Enterprise and regulated industries pursuing AI governance certification

## Micropayment Standards

### x402 Payment Protocol
- **Status:** Early adoption, Coinbase-driven
- **Core concept:** HTTP 402 "Payment Required" status code repurposed for machine-to-machine payments
- **How it works:** Agent makes request → receives 402 + payment details → pays → retries with proof
- **Use case:** Agent APIs charging per-call without subscriptions or API keys
- **Adoption:** Small but growing — toku.agency, some AI agent marketplaces
- **Technical note:** Requires crypto infrastructure (EVM or Solana-compatible)

## On-Chain Agent Infrastructure

### Vector Protocol
- **Status:** Live on Aptos blockchain
- **Core concept:** On-chain agent registration, discovery, and payment rails
- **Key features:** Agent profiles, APEX token payments, spend limits, multi-agent messaging
- **Adoption:** Early — hundreds of registered agents

### Theoriq
- **Status:** Live
- **Core concept:** Composable AI agent protocol with on-chain attribution
- **Key features:** Agent marketplace, dynamic swarms, on-chain reputation

### NEAR AI
- **Status:** Production
- **Core concept:** Decentralized AI infrastructure on NEAR blockchain
- **Key features:** Agent hosting, model registry, compute marketplace
