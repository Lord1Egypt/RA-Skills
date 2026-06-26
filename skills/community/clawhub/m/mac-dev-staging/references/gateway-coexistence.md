# Gateway Coexistence

Use this file when the Mac needs a local development gateway/controller while a separate shared gateway already exists on Linux.

## Recommended Topology

- Ryzen gateway: shared, LAN-visible, production-like orchestration
- Mac local gateway/controller: loopback-only, development/testing only

Recommended ports:

- Ryzen gateway: `192.168.88.11:18789`
- Mac local controller/gateway: `127.0.0.1:28789`
- Mac managed browser CDP: `127.0.0.1:18800`
- optional nginx reverse proxy: `127.0.0.1:8080`

## Why Split Them

This keeps local experiments from colliding with the shared orchestration surface.

Good examples:

- testing controller hooks on the Mac without touching the real gateway
- replaying CRM fixtures locally
- simulating a handshake or browser workflow before wiring it to production automation

## Rules

- never bind the Mac local controller to `0.0.0.0` by default
- do not reuse the shared gateway port
- keep a separate token or trust path for the Mac-local controller
- if the Mac-local controller dies, the shared Ryzen gateway must keep working

## Validation

Before enabling the Mac-local controller:

- run `scripts/detect-ports.sh`
- verify `28789` is free
- verify the real gateway is still reachable on `192.168.88.11:18789`
- write a receipt for the action
