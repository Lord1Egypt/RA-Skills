---
name: nexus-edge-deployer
description: Deploy 1-bit quantized AI models on VPS for Agent-as-a-Service with 98%
  margins.
version: '2.1.0'
metadata:
  openclaw:
    emoji: 🖥️
    homepage: https://github.com/Shuwanito/SkillsMP/tree/main/.claude/skills/nexus-edge-deployer
    os:
    - macos
    - linux
    - windows
---

# Edge AI Deployer

Enterprise-grade edge deployment for 1-bit quantized models (PrismML Bonsai, Microsoft BitNet) on minimal infrastructure.

## Capabilities
- Deploy Bonsai 8B (1.15GB), 4B (0.57GB), and 1.7B (0.24GB) models on VPS
- Calculate AaaS unit economics: cost per agent, margin per VPS, break-even analysis
- Configure Ollama or llama.cpp for multi-tenant inference serving
- Auto-provision Hetzner CX22 (EUR 3.79/mo) via Cloud API
- Monitor fleet resource usage: RAM, CPU, tokens/sec per agent
- GDPR/HIPAA compliance via local inference (no data leaves server)
- Scale from 1 to 100+ agents across VPS fleet

## Workflow
1. Assess client requirements: model quality, latency, privacy, platform
2. Select optimal model tier (8B for quality, 4B for balance, 1.7B for mobile)
3. Provision VPS via Hetzner API with cloud-init (Ollama + model pre-loaded)
4. Deploy agent with client-specific persona and capabilities
5. Benchmark inference quality against full-precision baseline
6. Configure monitoring, alerting, and auto-scaling rules
7. Generate unit economics report: revenue, cost, margin, projections

## Guidelines
- Always benchmark 1-bit model quality before deploying to production
- Maximum 3 Bonsai 8B agents per 4GB VPS (reserve 0.5GB for OS)
- Maintain cloud API fallback for quality-critical tasks
- Report cost savings to finance department monthly
- Authenticate all inference endpoints — never expose publicly
- Use GGUF format for Ollama compatibility