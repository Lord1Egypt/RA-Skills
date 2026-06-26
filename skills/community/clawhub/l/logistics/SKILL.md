---
name: logistics
description: Query and explain parcel logistics across courier providers, including tracking, courier identification, multi-package lookup, status interpretation, and delivery-update guidance. Use when the user asks about package tracking, logistics tracking, tracking numbers, identifying courier companies, batch logistics queries, or wants help understanding shipment progress across one or more couriers.
---

# Logistics

## Overview

Use this skill to help the user track parcels, identify couriers, interpret logistics statuses, and understand what a shipment update usually means. It serves as a unified entry point for multi-courier logistics queries, including major Chinese courier networks such as SF Express (顺丰), JD Logistics (京东快递), ZTO (中通), Cainiao (菜鸟), J&T Express (极兔), and others.

## Workflow

1. Identify whether the user has:
   - one tracking number
   - multiple tracking numbers
   - an unknown courier
   - a status they want explained
2. If the courier is unknown, infer cautiously from the number pattern or context.
3. Return the latest useful tracking interpretation first.
4. If a package appears delayed, explain likely reasons and a reasonable next action.
5. Keep summaries concise when handling multiple shipments.
