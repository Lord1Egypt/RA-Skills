# Security Policy

## Overview

PlanIt is an OpenClaw skill that helps users plan travel itineraries. This document explains our security practices.

## Architecture

PlanIt is a thin client skill that communicates with a backend service via HTTP API.

## Data Flow

1. User input → Skill → Backend API
2. Backend API processes the request and returns structured itinerary
3. Skill displays results to user

## Authentication

- Uses standard `Authorization: Bearer <token>` header
- Token is configured via environment variable `PLANIT_SECRET`
- No API keys are exposed in client-side code

## Telemetry

The skill collects anonymous usage metrics:

- Event types: `plan_request`, `plan_response`, `action`
- Data collected: user ID (hashed), action type, response type
- No personal information, location data, or conversation content is logged
- Telemetry is sent asynchronously and does not block user requests

Purpose: Improve service quality and detect issues

## No External Data Fetching

The skill client contains **zero** direct external API calls:
- No direct access to external services
- Only HTTP POST to configured backend API endpoint

## Contact

If you have security concerns, please file an issue on GitHub.
