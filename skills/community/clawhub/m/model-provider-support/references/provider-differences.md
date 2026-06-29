# Provider Differences

## Core Principle

Same model name does not imply same product support. Hosted variants can differ in model IDs, release timing, regions, API versions, quotas, safety layers, tooling, and request parameters.

## Claude: Bedrock vs Vertex AI vs Anthropic

- Bedrock answers: AWS docs are authoritative for Bedrock model IDs, regions, inference APIs, parameters, quotas, IAM, guardrails, and provisioned throughput.
- Vertex AI answers: Google Cloud docs are authoritative for Vertex partner model endpoints, regions, IAM, quotas, and request/response behavior.
- Anthropic answers: Anthropic docs are authoritative for first-party Claude API and useful for general Claude behavior, but not sufficient proof of Bedrock or Vertex support.
- Common trap: Anthropic announces a Claude feature, but Bedrock or Vertex may lag, expose it through a different parameter, limit it to selected models/regions, or not support it.
- Conservative answer pattern: “Anthropic first-party docs show X; I need AWS/Google official confirmation before saying the hosted version supports X.”

## GPT/OpenAI: Azure OpenAI vs OpenAI

- Azure answers: Microsoft Learn docs are authoritative for Azure OpenAI model availability, deployment model, API versions, regions, content filters, quotas, and Foundry integration.
- OpenAI answers: OpenAI platform docs are authoritative for first-party OpenAI API models and endpoints.
- Foundry distinction: Azure AI Foundry model catalog is not automatically the same as Azure OpenAI API support; confirm the service, endpoint, and deployment path.
- Common trap: A new OpenAI model, Responses API feature, tool, or parameter may not be available in Azure OpenAI, may require a different API version, or may be limited by region.
- Conservative answer pattern: “OpenAI supports X in first-party API, but Azure support must be checked in Microsoft Learn for the relevant API version and region.”

## Gemini: Vertex AI vs Gemini API

- Vertex answers: Google Cloud Vertex AI docs are authoritative for enterprise Google Cloud Gemini usage, regions, IAM, quotas, grounding, safety, and API reference.
- Gemini API answers: ai.google.dev docs are authoritative for the Gemini Developer API surface.
- Common trap: Gemini API examples often look portable, but Vertex AI can use different endpoints, auth, model naming, SDK setup, quotas, region controls, and feature rollout timing.
- Conservative answer pattern: “Gemini API docs show X; for Vertex AI we need Google Cloud Vertex docs confirming the same feature on the same model/API surface.”

## Answering Checklist

- Ask or infer: model family, exact model/version, provider, service, API version, region, and capability.
- Check source registry for the relevant official URL.
- Use taxonomy status labels internally; expose plain language to the team.
- Quote only short facts or summarize; do not paste long doc text.
- If docs are inaccessible, state the access issue and mark the conclusion as unverified.
- Never turn vendor marketing claims into API support conclusions without documentation.
