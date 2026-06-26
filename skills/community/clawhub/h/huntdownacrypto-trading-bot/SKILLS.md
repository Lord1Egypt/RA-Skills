## **1\. Healthcheck — Security audits & hardening**

Assess and secure your OpenClaw host. Check firewall, SSH, backups, updates, and align to your risk tolerance.

**Use when:** You want to audit your machine's security, harden against threats, or check if updates are available.

**Key commands:**

* openclaw security audit \--deep  
* openclaw update status  
* Schedule periodic checks

---

## **2\. Skill Creator — Build custom skills**

Create, improve, or audit AgentSkills. Use when you want to author new skills from scratch or enhance existing ones.

**Use when:** You want to extend OpenClaw with custom skills, organize scripts/references, or review skill structure.

**Key workflow:**

* Understand concrete examples  
* Plan reusable contents (scripts, references, assets)  
* Initialize with templates  
* Edit SKILL.md and resources  
* Package for distribution

---

## **3\. Node Connect — Diagnose connection failures**

Fix pairing and connectivity issues for Android/iOS/macOS apps (QR, setup code, Wi-Fi, Tailscale, VPS).

**Use when:** Your app won't connect, QR scans fail, or you see "pairing required" / "bootstrap token invalid" errors.

**Key checks:**

* openclaw qr \--json  
* openclaw devices list  
* openclaw devices approve \--latest

—-------------

name: crypto\_trading\_bot  
description: Analyze BTC and ETH setups, turn trading ideas into deterministic bot rules, and produce code-friendly entry, exit, and risk logic.  
user-invocable: true  
\---

\# Crypto Trading Bot

Use this skill when the user wants to:  
\- Analyze BTC or ETH setups  
\- Convert a trading idea into exact bot rules  
\- Create structured entry, exit, and risk logic

