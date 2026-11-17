# 📱 PAPI — WhatsApp Cloud API & Voice AI Engine
### *Automação de WhatsApp e Mensagens de Voz para Agentes de IA*

<p align="center">
  <img src="assets/logo.png" alt="PAPI Logo" width="120" height="120" />
</p>

<p align="center">
  <a href="https://clawhub.ai"><img src="https://img.shields.io/badge/ClawHub-Skill-blue.svg" alt="ClawHub Skill" /></a>
  <a href="https://papi.api.br"><img src="https://img.shields.io/badge/PAPI-Cloud%20Portal-emerald.svg" alt="PAPI Cloud Portal" /></a>
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License MIT" />
</p>

---

## 🇺🇸 English

### Overview
**PAPI** is a high-performance WhatsApp Cloud API and conversational messaging engine for AI Agents. It allows Hermes, OpenClaw, and autonomous agents to send realistic Push-to-Talk (PTT) voice notes, interactive quick-reply buttons, rich media, polls, documents, and contacts with real-time webhooks.

### 🚀 Quick Onboarding & First-Time Setup
1. **Get your PAPI API Key & Instance**:
   - Access the developer portal at [https://papi.api.br](https://papi.api.br) to create your instance and obtain your API key.
2. **Configure Environment Variables**:
   ```bash
   export PAPI_API_KEY="your_papi_api_key"
   export PAPI_INSTANCE_ID="your_instance_id"
   export PAPI_BASE_URL="https://api.papi.api.br"
   ```
3. **Configure Hermes / OpenClaw (`config.yaml`)**:
   ```yaml
   env:
     PAPI_API_KEY: "your_papi_api_key"
     PAPI_INSTANCE_ID: "your_instance_id"
     PAPI_BASE_URL: "https://api.papi.api.br"
   ```
4. **Run Connection Doctor Diagnostic**:
   ```bash
   curl -s "https://api.papi.api.br/api/instances/${PAPI_INSTANCE_ID}/status" \
     -H "x-api-key: ${PAPI_API_KEY}"
   ```

### Key Features
- 🎙️ **Native PTT Voice Memos**: Send realistic human-sounding voice notes directly in WhatsApp chat bubbles.
- 🔘 **Interactive Buttons & Lists**: Send quick replies, CTA URL buttons, and interactive choice lists.
- 📊 **Polls & Surveys**: Real-time polling with instant vote tracking.
- 🚀 **High Throughput & Webhooks**: Fast delivery with HMAC-SHA256 signature security.

---

## 🇧🇷 Português

### Visão Geral
O **PAPI** é uma plataforma de alta performance de WhatsApp Cloud API e mensageria conversacional para agentes de IA. Permite que o Hermes, OpenClaw e agentes autônomos disparem áudios de voz no formato PTT (gravado na hora), botões interativos, mídias em alta resolução, enquetes, documentos e fluxos de atendimento com webhooks em tempo real.

### 🚀 Onboarding Rápido & Primeiro Uso
1. **Obtenha sua Chave e Instância PAPI**:
   - Acesse o portal oficial em [https://papi.api.br](https://papi.api.br) para registrar sua instância e copiar sua chave de API.
2. **Configure as Variáveis de Ambiente**:
   ```bash
   export PAPI_API_KEY="sua_chave_papi"
   export PAPI_INSTANCE_ID="sua_instancia"
   export PAPI_BASE_URL="https://api.papi.api.br"
   ```
3. **Configure no Hermes / OpenClaw (`config.yaml`)**:
   ```yaml
   env:
     PAPI_API_KEY: "sua_chave_papi"
     PAPI_INSTANCE_ID: "sua_instancia"
     PAPI_BASE_URL: "https://api.papi.api.br"
   ```
4. **Execute o Teste de Conexão**:
   ```bash
   curl -s "https://api.papi.api.br/api/instances/${PAPI_INSTANCE_ID}/status" \
     -H "x-api-key: ${PAPI_API_KEY}"
   ```

### Principais Recursos
- 🎙️ **Áudios de Voz PTT Nativos**: Envio de notas de voz autênticas no formato de microfone gravado.
- 🔘 **Botões Interativos & Listas**: Respostas rápidas e botões de chamada para ação (CTA).
- 📊 **Enquetes Interativas**: Votações com retorno instantâneo via webhook.
- 🚀 **Alta Performance & Segurança**: Infraestrutura estável com verificação de assinatura HMAC-SHA256.

---

## 📦 Installation / Instalação

```bash
hermes skills install papi
# or via clawhub
clawhub install papi
```
