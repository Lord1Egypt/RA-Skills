---
name: papi
version: 1.1.0
description: "PAPI WhatsApp Cloud API - Envio e automação de mensagens WhatsApp (texto, PTT áudio de voz, mídias, botões interativos, enquetes, listas e webhooks)."
metadata: {"openclaw":{"emoji":"📱","homepage":"https://papi.api.br","tags":["papi","whatsapp","messaging","audio-ptt","ai-agents"]}}
---

# 📱 PAPI — WhatsApp Cloud API & Voice AI Engine

> 🌐 **Plataforma Oficial:** [https://papi.api.br](https://papi.api.br)
> 🚀 **Capacidades:** Disparo de mensagens de texto, notas de voz realistas (PTT), botões de resposta rápida, enquetes interativas, mídia HD, envio de contatos/localização e webhooks em tempo real.

---

## 🚀 Onboarding & Setup Rápido (Primeiro Uso)

Ao utilizar a skill pela primeira vez ou quando as credenciais não estiverem configuradas:

### 📋 Checklist de Credenciais
- [ ] **1. Chave de API (`PAPI_API_KEY`)**:
  - Obtenha seu token de acesso no painel de desenvolvedor em [https://papi.api.br](https://papi.api.br).
- [ ] **2. Identificador da Instância (`PAPI_INSTANCE_ID`)**:
  - Obtenha o identificador da sua instância pareada no painel PAPI (ex: `instancia_prod`).
- [ ] **3. URL Base da API (`PAPI_BASE_URL`)**:
  - Padrão oficial: `https://api.papi.api.br`

### 🔧 Configuração de Ambiente
Defina no seu `.env` ou exporte no terminal:
```bash
export PAPI_API_KEY="sua_chave_papi_aqui"
export PAPI_INSTANCE_ID="sua_instancia_aqui"
export PAPI_BASE_URL="https://api.papi.api.br"
```

No Hermes / OpenClaw (`config.yaml`):
```yaml
env:
  PAPI_API_KEY: "sua_chave_papi_aqui"
  PAPI_INSTANCE_ID: "sua_instancia_aqui"
  PAPI_BASE_URL: "https://api.papi.api.br"
```

### 🩺 Autodiagnóstico de Conectividade (Doctor)
```bash
curl -s "${PAPI_BASE_URL}/api/instances/${PAPI_INSTANCE_ID}/status" \
  -H "x-api-key: ${PAPI_API_KEY}"
```

---

## 📱 Formato de Destinatário (JID)

- **Número Individual (Brasil - E.164):** `55DDNNNNNNNNN@s.whatsapp.net`
  - Exemplo: `5527999999999@s.whatsapp.net`
- **Grupos:** `ID_DO_GRUPO@g.us`

---

## 🛠️ Métodos de Envio

### 1. Mensagem de Texto
```bash
curl -X POST "${PAPI_BASE_URL}/api/instances/${PAPI_INSTANCE_ID}/send-text" \
  -H "x-api-key: ${PAPI_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "jid": "5527999999999@s.whatsapp.net",
    "text": "Olá! Sua solicitação foi confirmada com sucesso. 🚀"
  }'
```

### 2. Áudio / Nota de Voz PTT (Push-to-Talk)
```bash
curl -X POST "${PAPI_BASE_URL}/api/instances/${PAPI_INSTANCE_ID}/send-audio" \
  -H "x-api-key: ${PAPI_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "jid": "5527999999999@s.whatsapp.net",
    "url": "https://seu-dominio.com/audio.mp3",
    "ptt": true
  }'
```

### 3. Imagem com Legenda
```bash
curl -X POST "${PAPI_BASE_URL}/api/instances/${PAPI_INSTANCE_ID}/send-image" \
  -H "x-api-key: ${PAPI_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "jid": "5527999999999@s.whatsapp.net",
    "url": "https://seu-dominio.com/imagem.jpg",
    "caption": "Segue o relatório atualizado 📊"
  }'
```

### 4. Botões Interativos
```bash
curl -X POST "${PAPI_BASE_URL}/api/instances/${PAPI_INSTANCE_ID}/send-buttons" \
  -H "x-api-key: ${PAPI_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "jid": "5527999999999@s.whatsapp.net",
    "text": "Como deseja prosseguir com o seu atendimento?",
    "footer": "PAPI Cloud",
    "buttons": [
      {"type": "quick_reply", "displayText": "Falar com Consultor", "id": "btn_atendimento"},
      {"type": "quick_reply", "displayText": "Ver Documentação", "id": "btn_docs"},
      {"type": "cta_url", "displayText": "Acessar Portal", "url": "https://papi.api.br"}
    ]
  }'
```

### 5. Enquete Interativa
```bash
curl -X POST "${PAPI_BASE_URL}/api/instances/${PAPI_INSTANCE_ID}/send-poll" \
  -H "x-api-key: ${PAPI_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "jid": "5527999999999@s.whatsapp.net",
    "name": "Qual horário prefere para nossa call técnica?",
    "options": ["10:00 BRT", "14:30 BRT", "17:00 BRT"],
    "selectableCount": 1
  }'
```

---

## 🔒 Segurança e Privacidade
* **Stateless Zero-Storage:** As mensagens trafegam diretamente entre a API PAPI e o WhatsApp.
* **Segurança de Ponta a Ponta:** Suporte a verificação de assinatura HMAC-SHA256 em webhooks.
