---
name: hlp-ghl-api
description: HubLinkPro GoHighLevel API — manage contacts, pipelines, workflows, and messaging for Tri-Cities real estate lead gen
requires:
  env:
    - GHL_API_KEY
    - GHL_LOCATION_ID
  bins:
    - curl
    - jq
---

# HubLinkPro GHL API Skill

Base URL: `https://services.leadconnectorhq.com`
Auth header: `Authorization: Bearer $GHL_API_KEY`
All requests include: `Version: 2021-07-28`

## Get Contact by Phone or Email

curl -s -H "Authorization: Bearer $GHL_API_KEY" -H "Version: 2021-07-28" \
  "https://services.leadconnectorhq.com/contacts/search/duplicate?locationId=$GHL_LOCATION_ID&email=$EMAIL" | jq .

## Create or Update Contact

curl -s -X POST "https://services.leadconnectorhq.com/contacts/" \
  -H "Authorization: Bearer $GHL_API_KEY" -H "Version: 2021-07-28" -H "Content-Type: application/json" \
  -d '{"firstName":"$FIRST","lastName":"$LAST","email":"$EMAIL","phone":"$PHONE","locationId":"'$GHL_LOCATION_ID'","tags":["$TAGS"],"source":"$SOURCE"}' | jq .

## Add Tags to Contact

curl -s -X POST "https://services.leadconnectorhq.com/contacts/$CONTACT_ID/tags" \
  -H "Authorization: Bearer $GHL_API_KEY" -H "Version: 2021-07-28" -H "Content-Type: application/json" \
  -d '{"tags":["$TAG1","$TAG2"]}' | jq .

## Create Opportunity (Pipeline Deal)

curl -s -X POST "https://services.leadconnectorhq.com/opportunities/" \
  -H "Authorization: Bearer $GHL_API_KEY" -H "Version: 2021-07-28" -H "Content-Type: application/json" \
  -d '{"pipelineId":"$PIPELINE_ID","locationId":"'$GHL_LOCATION_ID'","name":"$DEAL_NAME","stageId":"$STAGE_ID","contactId":"$CONTACT_ID","status":"open"}' | jq .

## Move Opportunity Stage

curl -s -X PUT "https://services.leadconnectorhq.com/opportunities/$OPP_ID/status" \
  -H "Authorization: Bearer $GHL_API_KEY" -H "Version: 2021-07-28" -H "Content-Type: application/json" \
  -d '{"stageId":"$NEW_STAGE_ID"}' | jq .

## List Pipelines

curl -s -H "Authorization: Bearer $GHL_API_KEY" -H "Version: 2021-07-28" \
  "https://services.leadconnectorhq.com/opportunities/pipelines?locationId=$GHL_LOCATION_ID" | jq .

## Send SMS via Conversations API

curl -s -X POST "https://services.leadconnectorhq.com/conversations/messages" \
  -H "Authorization: Bearer $GHL_API_KEY" -H "Version: 2021-07-28" -H "Content-Type: application/json" \
  -d '{"type":"SMS","contactId":"$CONTACT_ID","message":"$MESSAGE"}' | jq .

## Search Contacts by Tag

curl -s -H "Authorization: Bearer $GHL_API_KEY" -H "Version: 2021-07-28" \
  "https://services.leadconnectorhq.com/contacts/?locationId=$GHL_LOCATION_ID&query=$SEARCH_TERM&limit=20" | jq .

## Get Contact Activity / Notes

curl -s -H "Authorization: Bearer $GHL_API_KEY" -H "Version: 2021-07-28" \
  "https://services.leadconnectorhq.com/contacts/$CONTACT_ID/notes" | jq .

## Add Note to Contact

curl -s -X POST "https://services.leadconnectorhq.com/contacts/$CONTACT_ID/notes" \
  -H "Authorization: Bearer $GHL_API_KEY" -H "Version: 2021-07-28" -H "Content-Type: application/json" \
  -d '{"body":"$NOTE_TEXT"}' | jq .

## Trigger Workflow for Contact

curl -s -X POST "https://services.leadconnectorhq.com/contacts/$CONTACT_ID/workflow/$WORKFLOW_ID" \
  -H "Authorization: Bearer $GHL_API_KEY" -H "Version: 2021-07-28" -H "Content-Type: application/json" | jq .

## Key HubLinkPro Context

- Location: Tri-Cities TN (Johnson City, Kingsport, Bristol)
- Pipelines: HLP – Sellers, New Construction, Pre-Foreclosure
- Tags: new-lead, fb-seller, new-construction, pre-foreclosure, contacted, qualified, nurture
- Agents: Tasha, Nate, Cory, Laura, Mary Ellen, Josh
- When assigning leads, use tag format: agent-{firstname}
