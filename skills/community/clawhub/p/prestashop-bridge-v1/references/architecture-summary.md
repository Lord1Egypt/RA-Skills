# Architecture Summary

PrestaShop Bridge V1 is a stable boundary between AI-driven automation and a PrestaShop 9 runtime.

## Core components
- Symfony 6.4
- API Platform 3
- Redis Messenger transport
- MySQL job persistence
- Python/OpenClaw handler clients

## Stability goals
- isolate agent integrations from native API volatility
- protect writes with signatures and async workflows
- retain durable job truth in MySQL
