# Project Bootstrap Checklist

## Before coding
- Define product goal
- Define target user
- Define MVP boundary
- Decide if FastAPI is truly needed
- Decide billing model
- Decide upload/storage needs
- Decide key analytics events
- Decide key email flows

## Before data modeling
- Define core domain entities
- Separate auth data from app data
- Separate billing truth from UI redirects
- Separate file storage from DB metadata

## Before deployment
- Prepare env var inventory
- Confirm Clerk setup
- Confirm Stripe webhook plan
- Confirm Resend sender strategy
- Confirm PostHog and Sentry setup
- Confirm Vercel deployment shape

## Before adding FastAPI
- Prove Python is necessary
- Define exact boundary
- Define auth and transport between frontend and FastAPI
- Define deployment plan
