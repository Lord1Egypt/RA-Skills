---
name: highlevel-pit
description: |
  GoHighLevel (Private Integration Token) API integration with managed auth. CRM, sales pipelines, calendars, conversations, payments, and marketing automation.
  Use this skill when users want to manage contacts, opportunities, calendars, conversations, invoices, products, or workflows in GoHighLevel using a Private Integration Token (PIT).
  GoHighLevel has two token types: Agency tokens and Sub-Account tokens. Agency tokens manage locations (sub-accounts), while Sub-Account tokens access CRM, calendars, pipelines, and other location-scoped data.
  For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
  Requires network access and valid Maton API key.
metadata:
  author: maton
  version: "1.0"
  clawdbot:
    emoji: 🧠
    requires:
      env:
        - MATON_API_KEY
---

# GoHighLevel (Private Integration Token)

Access the GoHighLevel API with managed Private Integration Token (PIT) authentication. Manage contacts, sales pipelines, calendars, conversations, invoices, products, businesses, and marketing automation.

## Important: Two Token Types

GoHighLevel uses two types of Private Integration Tokens with different scopes:

| Token Type | Purpose | Key Capabilities |
|---|---|---|
| **Agency** | Manage the agency and its sub-accounts (locations) | Search/create/update/delete locations, manage snapshots |
| **Sub-Account** | Operate within a specific location | Contacts, calendars, pipelines, conversations, payments, custom fields, tags, workflows, campaigns |

**You will typically need both connections** — an agency token for location management and a sub-account token for CRM operations. Use the `Maton-Connection` header to specify which token to use for each request.

## Quick Start

```bash
# List contacts (Sub-Account token)
curl -s -X GET "https://api.maton.ai/highlevel-pit/contacts/?locationId={locationId}&limit=10" \
  -H "Authorization: Bearer $MATON_API_KEY"
```

## Base URL

```
https://api.maton.ai/highlevel-pit/{resource}
```

Maton proxies requests to `services.leadconnectorhq.com` and automatically injects your PIT token.

## Authentication

All requests require the Maton API key in the Authorization header:

```
Authorization: Bearer $MATON_API_KEY
```

**Environment Variable:** Set your API key as `MATON_API_KEY`:

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

### Getting Your API Key

1. Sign in or create an account at [maton.ai](https://maton.ai)
2. Go to [maton.ai/settings](https://maton.ai/settings)
3. Copy your API key

## Connection Management

Manage your GoHighLevel PIT connections at `https://api.maton.ai`.

### List Connections

```bash
curl -s -X GET "https://api.maton.ai/connections?app=highlevel-pit&status=ACTIVE" \
  -H "Authorization: Bearer $MATON_API_KEY"
```

### Create Connection

```bash
curl -s -X POST "https://api.maton.ai/connections" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -d '{"app": "highlevel-pit"}'
```

Open the returned `url` in a browser to enter your Private Integration Token.

### Get Connection

```bash
curl -s -X GET "https://api.maton.ai/connections/{connection_id}" \
  -H "Authorization: Bearer $MATON_API_KEY"
```

**Response:**
```json
{
  "connection": {
    "connection_id": "{connection_id}",
    "status": "ACTIVE",
    "app": "highlevel-pit",
    "method": "API_KEY"
  }
}
```

### Delete Connection

```bash
curl -s -X DELETE "https://api.maton.ai/connections/{connection_id}" \
  -H "Authorization: Bearer $MATON_API_KEY"
```

### Specifying Connection

Since you will typically have two connections (agency + sub-account), always specify which one to use:

```bash
curl -s -X GET "https://api.maton.ai/highlevel-pit/contacts/?locationId={locationId}" \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Maton-Connection: {connection_id}"
```

If you have multiple connections, always include this header to ensure requests go to the intended account.

## Security & Permissions

- Access is scoped to locations, contacts, opportunities, calendars, conversations, workflows, and CRM data within the connected GoHighLevel account.
- **Two token types with different scopes**: Agency tokens manage locations and snapshots. Sub-Account tokens access contacts, calendars, pipelines, and CRM data. Use the correct connection for the intended scope.
- **All write operations require explicit user approval.** Before executing any create, update, or delete call, confirm the target resource and intended effect with the user.

## API Reference — Agency Token

These endpoints require an **Agency** token.

### Locations (Sub-Accounts)

#### Search Locations

```bash
GET /highlevel-pit/locations/search?companyId={companyId}
```

Query parameters:
- `companyId` (required) - The agency's company ID
- `limit` - Results per page
- `skip` - Number to skip (offset)
- `order` - Sort order
- `email` - Filter by email

**Response:**
```json
{
  "locations": [
    {
      "id": "abc123",
      "companyId": "xyz789",
      "name": "My Sub-Account",
      "address": "123 Main St",
      "city": "San Francisco",
      "state": "CA",
      "country": "US",
      "postalCode": "94105",
      "timezone": "America/Los_Angeles",
      "email": "admin@example.com",
      "phone": "+15551234567"
    }
  ]
}
```

#### Get Location

```bash
GET /highlevel-pit/locations/{locationId}
```

**Response:**
```json
{
  "location": {
    "id": "abc123",
    "name": "My Sub-Account",
    "address": "123 Main St",
    "city": "San Francisco",
    "state": "CA",
    "settings": {
      "allowDuplicateContact": false,
      "allowDuplicateOpportunity": false
    },
    "social": { ... },
    "permissions": { ... }
  }
}
```

#### Create Location

```bash
POST /highlevel-pit/locations/
Content-Type: application/json

{
  "companyId": "{companyId}",
  "name": "New Sub-Account",
  "address": "123 Main St",
  "city": "San Francisco",
  "state": "CA",
  "postalCode": "94105",
  "country": "US",
  "timezone": "America/Los_Angeles",
  "email": "admin@example.com",
  "phone": "+15551234567"
}
```

#### Update Location

```bash
PUT /highlevel-pit/locations/{locationId}
Content-Type: application/json

{
  "name": "Updated Name",
  "city": "Los Angeles"
}
```

#### Delete Location

```bash
DELETE /highlevel-pit/locations/{locationId}
```

### Snapshots

#### List Snapshots

```bash
GET /highlevel-pit/snapshots/?companyId={companyId}
```

## API Reference — Sub-Account Token

These endpoints require a **Sub-Account** token. Most endpoints require a `locationId` query parameter.

### Contacts

#### List Contacts

```bash
GET /highlevel-pit/contacts/?locationId={locationId}
```

Query parameters:
- `locationId` (required)
- `limit` - Results per page (default 20)
- `query` - Search by name, email, or phone
- `startAfter` - Cursor for pagination (contact ID)
- `startAfterId` - Cursor for pagination

**Response:**
```json
{
  "contacts": [
    {
      "id": "abc123",
      "locationId": "loc123",
      "firstName": "John",
      "lastName": "Doe",
      "email": "john@example.com",
      "phone": "+15551234567",
      "companyName": "Acme Inc",
      "tags": ["customer", "vip"],
      "type": "lead",
      "dnd": false,
      "dateAdded": "2026-04-28T07:34:32.829Z",
      "customFields": []
    }
  ],
  "meta": {
    "total": 150,
    "startAfter": "abc123",
    "startAfterId": "abc123"
  }
}
```

#### Get Contact

```bash
GET /highlevel-pit/contacts/{contactId}
```

**Response:**
```json
{
  "contact": {
    "id": "abc123",
    "firstName": "John",
    "lastName": "Doe",
    "email": "john@example.com",
    "phone": "+15551234567",
    "tags": ["customer"],
    "type": "lead",
    "companyName": "Acme Inc",
    "customFields": [],
    "additionalEmails": [],
    "additionalPhones": []
  }
}
```

#### Create Contact

```bash
POST /highlevel-pit/contacts/
Content-Type: application/json

{
  "locationId": "{locationId}",
  "firstName": "John",
  "lastName": "Doe",
  "email": "john@example.com",
  "phone": "+15551234567",
  "companyName": "Acme Inc",
  "tags": ["customer"]
}
```

#### Update Contact

```bash
PUT /highlevel-pit/contacts/{contactId}
Content-Type: application/json

{
  "firstName": "Jane",
  "companyName": "New Company"
}
```

#### Delete Contact

```bash
DELETE /highlevel-pit/contacts/{contactId}
```

#### Search Contacts by Email/Phone

```bash
GET /highlevel-pit/contacts/?locationId={locationId}&query=john@example.com
```

### Contact Tags

#### Add Tags

```bash
POST /highlevel-pit/contacts/{contactId}/tags
Content-Type: application/json

{
  "tags": ["vip", "priority"]
}
```

**Response:**
```json
{
  "tags": ["customer", "vip", "priority"],
  "tagsAdded": ["vip", "priority"]
}
```

#### Remove Tags

```bash
DELETE /highlevel-pit/contacts/{contactId}/tags
Content-Type: application/json

{
  "tags": ["vip"]
}
```

**Response:**
```json
{
  "tags": ["customer", "priority"],
  "tagsRemoved": ["vip"]
}
```

### Contact Notes

#### List Notes

```bash
GET /highlevel-pit/contacts/{contactId}/notes
```

#### Create Note

```bash
POST /highlevel-pit/contacts/{contactId}/notes
Content-Type: application/json

{
  "body": "Spoke with client about renewal"
}
```

**Response:**
```json
{
  "note": {
    "id": "note123",
    "body": "Spoke with client about renewal",
    "dateAdded": "2026-04-30T10:22:47.934Z",
    "contactId": "abc123"
  }
}
```

#### Update Note

```bash
PUT /highlevel-pit/contacts/{contactId}/notes/{noteId}
Content-Type: application/json

{
  "body": "Updated note content"
}
```

#### Delete Note

```bash
DELETE /highlevel-pit/contacts/{contactId}/notes/{noteId}
```

### Contact Tasks

#### List Tasks

```bash
GET /highlevel-pit/contacts/{contactId}/tasks
```

#### Create Task

**IMPORTANT:** The `completed` field is required.

```bash
POST /highlevel-pit/contacts/{contactId}/tasks
Content-Type: application/json

{
  "title": "Follow up call",
  "body": "Discuss contract renewal",
  "dueDate": "2026-06-01T10:00:00Z",
  "completed": false
}
```

**Response:**
```json
{
  "task": {
    "id": "task123",
    "title": "Follow up call",
    "body": "Discuss contract renewal",
    "dueDate": "2026-06-01T10:00:00.000Z",
    "completed": false,
    "contactId": "abc123"
  }
}
```

#### Update Task

```bash
PUT /highlevel-pit/contacts/{contactId}/tasks/{taskId}
Content-Type: application/json

{
  "title": "Updated task",
  "completed": true
}
```

#### Delete Task

```bash
DELETE /highlevel-pit/contacts/{contactId}/tasks/{taskId}
```

### Opportunities (Deals)

#### Search Opportunities

```bash
GET /highlevel-pit/opportunities/search?location_id={locationId}
```

Query parameters:
- `location_id` (required)
- `pipeline_id` - Filter by pipeline
- `pipeline_stage_id` - Filter by stage
- `status` - `open`, `won`, `lost`, `abandoned`, `all`
- `contact_id` - Filter by contact
- `q` - Search query
- `limit` - Results per page
- `page` - Page number

**Response:**
```json
{
  "opportunities": [
    {
      "id": "opp123",
      "name": "Enterprise Deal",
      "monetaryValue": 50000,
      "pipelineId": "pipe123",
      "pipelineStageId": "stage123",
      "status": "open",
      "contactId": "abc123",
      "contact": {
        "id": "abc123",
        "name": "John Doe",
        "email": "john@example.com"
      }
    }
  ],
  "meta": {
    "total": 25,
    "currentPage": 1,
    "nextPage": 2,
    "prevPage": null
  }
}
```

#### Get Opportunity

```bash
GET /highlevel-pit/opportunities/{opportunityId}
```

#### Create Opportunity

```bash
POST /highlevel-pit/opportunities/
Content-Type: application/json

{
  "pipelineId": "{pipelineId}",
  "locationId": "{locationId}",
  "name": "Enterprise Deal",
  "pipelineStageId": "{stageId}",
  "status": "open",
  "contactId": "{contactId}",
  "monetaryValue": 50000
}
```

#### Update Opportunity

**IMPORTANT:** `pipelineId` is required even when not changing it.

```bash
PUT /highlevel-pit/opportunities/{opportunityId}
Content-Type: application/json

{
  "pipelineId": "{pipelineId}",
  "name": "Updated Deal",
  "monetaryValue": 75000,
  "status": "won"
}
```

#### Delete Opportunity

```bash
DELETE /highlevel-pit/opportunities/{opportunityId}
```

### Pipelines

#### List Pipelines

```bash
GET /highlevel-pit/opportunities/pipelines?locationId={locationId}
```

**Response:**
```json
{
  "pipelines": [
    {
      "id": "pipe123",
      "name": "Sales Pipeline",
      "stages": [
        {
          "id": "stage-uuid",
          "name": "New Lead",
          "position": 0,
          "stageWinProbability": 14.29
        },
        {
          "id": "stage-uuid-2",
          "name": "Contacted",
          "position": 1,
          "stageWinProbability": 28.57
        }
      ]
    }
  ]
}
```

### Calendars

#### List Calendars

```bash
GET /highlevel-pit/calendars/?locationId={locationId}
```

**Response:**
```json
{
  "calendars": [
    {
      "id": "cal123",
      "locationId": "loc123",
      "name": "Personal Calendar",
      "calendarType": "personal",
      "eventType": "RoundRobin_OptimizeForAvailability",
      "slotDuration": 30,
      "teamMembers": [
        {
          "userId": "user123",
          "selected": true,
          "priority": 0.5
        }
      ]
    }
  ]
}
```

#### Get Calendar

```bash
GET /highlevel-pit/calendars/{calendarId}
```

#### Create Calendar

```bash
POST /highlevel-pit/calendars/
Content-Type: application/json

{
  "locationId": "{locationId}",
  "name": "Team Calendar",
  "calendarType": "personal",
  "eventType": "RoundRobin_OptimizeForAvailability",
  "teamMembers": [
    {
      "userId": "{userId}",
      "priority": 0.5,
      "selected": true
    }
  ]
}
```

#### Update Calendar

**Note:** Do NOT include `locationId` in the update body.

```bash
PUT /highlevel-pit/calendars/{calendarId}
Content-Type: application/json

{
  "name": "Updated Calendar",
  "calendarType": "personal",
  "eventType": "RoundRobin_OptimizeForAvailability",
  "teamMembers": [
    {
      "userId": "{userId}",
      "priority": 0.5,
      "selected": true
    }
  ]
}
```

#### Delete Calendar

```bash
DELETE /highlevel-pit/calendars/{calendarId}
```

#### Get Calendar Events

Requires at least one of `calendarId`, `userId`, or `groupId`.

```bash
GET /highlevel-pit/calendars/events?locationId={locationId}&calendarId={calendarId}&startTime={epochMs}&endTime={epochMs}
```

Query parameters:
- `locationId` (required)
- `calendarId`, `userId`, or `groupId` (at least one required)
- `startTime` - Start of range (epoch milliseconds)
- `endTime` - End of range (epoch milliseconds)

#### Get Free Slots

```bash
GET /highlevel-pit/calendars/{calendarId}/free-slots?startDate={epochMs}&endDate={epochMs}&timezone={timezone}
```

#### Calendar Groups

```bash
GET /highlevel-pit/calendars/groups?locationId={locationId}
```

### Conversations

#### Search Conversations

```bash
GET /highlevel-pit/conversations/search?locationId={locationId}
```

Query parameters:
- `locationId` (required)
- `limit` - Results per page
- `contactId` - Filter by contact
- `assignedTo` - Filter by assigned user
- `status` - Filter by status

**Response:**
```json
{
  "conversations": [
    {
      "id": "conv123",
      "locationId": "loc123",
      "contactId": "abc123",
      "fullName": "John Doe",
      "type": "TYPE_PHONE",
      "lastMessageDate": 1777361673411,
      "lastMessageType": "TYPE_NO_SHOW",
      "unreadCount": 0
    }
  ],
  "total": 5
}
```

#### Get Conversation

```bash
GET /highlevel-pit/conversations/{conversationId}
```

#### Get Conversation Messages

```bash
GET /highlevel-pit/conversations/{conversationId}/messages
```

#### Create Conversation

```bash
POST /highlevel-pit/conversations/
Content-Type: application/json

{
  "locationId": "{locationId}",
  "contactId": "{contactId}"
}
```

### Users

#### List Users

```bash
GET /highlevel-pit/users/?locationId={locationId}
```

**Response:**
```json
{
  "users": [
    {
      "id": "user123",
      "name": "Admin User",
      "firstName": "Admin",
      "lastName": "User",
      "email": "admin@example.com",
      "phone": "+15551234567",
      "roles": {
        "type": "admin",
        "role": "admin",
        "locationIds": ["loc123"]
      }
    }
  ]
}
```

### Location Tags

#### List Tags

```bash
GET /highlevel-pit/locations/{locationId}/tags
```

**Response:**
```json
{
  "tags": [
    {
      "id": "tag123",
      "name": "VIP Customer",
      "locationId": "loc123"
    }
  ]
}
```

#### Create Tag

```bash
POST /highlevel-pit/locations/{locationId}/tags
Content-Type: application/json

{
  "name": "New Tag"
}
```

#### Get Tag

```bash
GET /highlevel-pit/locations/{locationId}/tags/{tagId}
```

#### Update Tag

```bash
PUT /highlevel-pit/locations/{locationId}/tags/{tagId}
Content-Type: application/json

{
  "name": "Updated Tag"
}
```

#### Delete Tag

```bash
DELETE /highlevel-pit/locations/{locationId}/tags/{tagId}
```

### Custom Fields

#### List Custom Fields

```bash
GET /highlevel-pit/locations/{locationId}/customFields
```

**Response:**
```json
{
  "customFields": [
    {
      "id": "cf123",
      "name": "Customer ID",
      "fieldKey": "contact.customer_id",
      "dataType": "TEXT",
      "model": "contact",
      "position": 50
    }
  ]
}
```

#### Create Custom Field

```bash
POST /highlevel-pit/locations/{locationId}/customFields
Content-Type: application/json

{
  "name": "Customer ID",
  "dataType": "TEXT",
  "model": "contact"
}
```

Valid `dataType` values: `TEXT`, `LARGE_TEXT`, `NUMERICAL`, `PHONE`, `MONETORY`, `CHECKBOX`, `SINGLE_OPTIONS`, `MULTIPLE_OPTIONS`, `FLOAT`, `DATE`, `TEXTBOX_LIST`, `FILE_UPLOAD`, `SIGNATURE`

Valid `model` values: `contact`, `opportunity`

#### Get Custom Field

```bash
GET /highlevel-pit/locations/{locationId}/customFields/{customFieldId}
```

#### Update Custom Field

```bash
PUT /highlevel-pit/locations/{locationId}/customFields/{customFieldId}
Content-Type: application/json

{
  "name": "Updated Field Name"
}
```

#### Delete Custom Field

```bash
DELETE /highlevel-pit/locations/{locationId}/customFields/{customFieldId}
```

### Custom Values

#### List Custom Values

```bash
GET /highlevel-pit/locations/{locationId}/customValues
```

**Response:**
```json
{
  "customValues": [
    {
      "id": "cv123",
      "name": "Company Tagline",
      "fieldKey": "{{ custom_values.company_tagline }}",
      "value": "We build great things",
      "locationId": "loc123"
    }
  ]
}
```

#### Create Custom Value

```bash
POST /highlevel-pit/locations/{locationId}/customValues
Content-Type: application/json

{
  "name": "Company Tagline",
  "value": "We build great things"
}
```

#### Get Custom Value

```bash
GET /highlevel-pit/locations/{locationId}/customValues/{customValueId}
```

#### Update Custom Value

```bash
PUT /highlevel-pit/locations/{locationId}/customValues/{customValueId}
Content-Type: application/json

{
  "name": "Updated Name",
  "value": "Updated value"
}
```

#### Delete Custom Value

```bash
DELETE /highlevel-pit/locations/{locationId}/customValues/{customValueId}
```

### Businesses

#### List Businesses

```bash
GET /highlevel-pit/businesses/?locationId={locationId}
```

**Response:**
```json
{
  "success": true,
  "businesses": [
    {
      "id": "biz123",
      "name": "Acme Inc",
      "locationId": "loc123",
      "city": "Los Angeles",
      "website": "www.acme.com",
      "phone": "+15551234567",
      "email": "info@acme.com"
    }
  ]
}
```

#### Get Business

```bash
GET /highlevel-pit/businesses/{businessId}
```

#### Create Business

```bash
POST /highlevel-pit/businesses/
Content-Type: application/json

{
  "locationId": "{locationId}",
  "name": "New Business",
  "city": "San Francisco",
  "phone": "+15551234567",
  "email": "info@newbiz.com",
  "website": "www.newbiz.com"
}
```

#### Update Business

```bash
PUT /highlevel-pit/businesses/{businessId}
Content-Type: application/json

{
  "name": "Updated Business",
  "city": "Los Angeles"
}
```

#### Delete Business

```bash
DELETE /highlevel-pit/businesses/{businessId}
```

### Products

#### List Products

```bash
GET /highlevel-pit/products/?locationId={locationId}
```

#### Get Product

```bash
GET /highlevel-pit/products/{productId}?locationId={locationId}
```

**Note:** `locationId` query parameter is required even for single product retrieval.

#### Create Product

```bash
POST /highlevel-pit/products/
Content-Type: application/json

{
  "locationId": "{locationId}",
  "name": "Digital Course",
  "description": "Online training program",
  "productType": "DIGITAL"
}
```

#### Delete Product

```bash
DELETE /highlevel-pit/products/{productId}?locationId={locationId}
```

### Invoices

#### List Invoices

**IMPORTANT:** Both `offset` and `altId`/`altType` are required.

```bash
GET /highlevel-pit/invoices/?altId={locationId}&altType=location&limit=20&offset=0
```

#### Get Invoice

```bash
GET /highlevel-pit/invoices/{invoiceId}?altId={locationId}&altType=location
```

### Payments

#### List Orders

```bash
GET /highlevel-pit/payments/orders?altId={locationId}&altType=location&limit=20
```

#### List Transactions

```bash
GET /highlevel-pit/payments/transactions?altId={locationId}&altType=location&limit=20
```

#### List Subscriptions

```bash
GET /highlevel-pit/payments/subscriptions?altId={locationId}&altType=location&limit=20
```

### Trigger Links

#### List Links

```bash
GET /highlevel-pit/links/?locationId={locationId}
```

#### Create Link

```bash
POST /highlevel-pit/links/
Content-Type: application/json

{
  "locationId": "{locationId}",
  "name": "Survey Link",
  "redirectTo": "https://example.com/survey"
}
```

**Response:**
```json
{
  "link": {
    "id": "link123",
    "name": "Survey Link",
    "redirectTo": "https://example.com/survey",
    "fieldKey": "{{trigger_link.link123}}"
  }
}
```

#### Update Link

```bash
PUT /highlevel-pit/links/{linkId}
Content-Type: application/json

{
  "name": "Updated Link",
  "redirectTo": "https://updated.com"
}
```

#### Delete Link

```bash
DELETE /highlevel-pit/links/{linkId}
```

### Workflows

#### List Workflows

```bash
GET /highlevel-pit/workflows/?locationId={locationId}
```

### Campaigns

#### List Campaigns

```bash
GET /highlevel-pit/campaigns/?locationId={locationId}
```

### Forms

#### List Forms

```bash
GET /highlevel-pit/forms/?locationId={locationId}
```

### Surveys

#### List Surveys

```bash
GET /highlevel-pit/surveys/?locationId={locationId}
```

### Funnels

#### List Funnels

```bash
GET /highlevel-pit/funnels/funnel/list?locationId={locationId}
```

**Response:**
```json
{
  "funnels": [...],
  "count": 5
}
```

### Social Media

#### List Accounts

```bash
GET /highlevel-pit/social-media-posting/{locationId}/accounts
```

**Response:**
```json
{
  "success": true,
  "results": {
    "accounts": [...],
    "groups": [...]
  }
}
```

#### List Categories

```bash
GET /highlevel-pit/social-media-posting/{locationId}/categories
```

### Media Files

#### List Files

**IMPORTANT:** The `type` parameter is required.

```bash
GET /highlevel-pit/medias/files?altId={locationId}&altType=location&type=file&limit=20
```

Valid `type` values: `file`, `image`, `video`, `audio`

## Pagination

GoHighLevel uses different pagination styles depending on the endpoint:

### Cursor-Based (Contacts)

```bash
GET /highlevel-pit/contacts/?locationId={locationId}&limit=20&startAfterId={lastContactId}
```

Response includes `meta.startAfterId` for the next page cursor.

### Offset-Based (Opportunities, Invoices)

```bash
GET /highlevel-pit/opportunities/search?location_id={locationId}&limit=20&page=2
GET /highlevel-pit/invoices/?altId={locationId}&altType=location&limit=20&offset=20
```

### Skip-Based (Locations)

```bash
GET /highlevel-pit/locations/search?companyId={companyId}&limit=20&skip=20
```

## Code Examples

### JavaScript

```javascript
const response = await fetch(
  'https://api.maton.ai/highlevel-pit/contacts/?locationId={locationId}&limit=20',
  {
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`,
      'Maton-Connection': '{sub-account-connection-id}'
    }
  }
);
const data = await response.json();
```

### Python

```python
import os
import requests

response = requests.get(
    'https://api.maton.ai/highlevel-pit/contacts/',
    headers={
        'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}',
        'Maton-Connection': '{sub-account-connection-id}'
    },
    params={'locationId': '{locationId}', 'limit': 20}
)
data = response.json()
```

## Notes

- **Two token types**: Agency tokens manage locations; Sub-Account tokens access CRM data within a location. Use the `Maton-Connection` header to pick the right one.
- Most Sub-Account endpoints require a `locationId` query parameter
- Payment/invoice endpoints use `altId` and `altType=location` instead of `locationId`
- Social media endpoints put `locationId` in the URL path, not as a query param
- Calendar events require `startTime`/`endTime` as **epoch milliseconds**, not ISO-8601
- Calendar event queries require at least one of `calendarId`, `userId`, or `groupId`
- Calendar update does NOT accept `locationId` in the body (returns 422)
- Product GET requires `locationId` as a query parameter
- Contact task creation requires the `completed` field (boolean)
- Opportunity update requires `pipelineId` even when not changing it
- Invoice list requires `offset` parameter (use `0` for first page)
- Media file list requires the `type` parameter
- All delete operations return HTTP 200 (not 204)
- IMPORTANT: When using curl commands, use `curl -g` when URLs contain brackets to disable glob parsing
- IMPORTANT: When piping curl output to `jq` or other commands, environment variables like `$MATON_API_KEY` may not expand correctly in some shell environments

## Error Handling

| Status | Meaning |
|--------|---------|
| 400 | Bad request or invalid parameters |
| 401 | Invalid/missing Maton API key, token not authorized for scope, or user type mismatch |
| 403 | Token does not have access to this location |
| 404 | Resource not found |
| 422 | Validation error — check required fields |
| 429 | Rate limited |
| 4xx/5xx | Passthrough error from GoHighLevel API |

### Common Errors

**"The token does not have access to this location"** (403): You're using an Agency token for an endpoint that requires a Sub-Account token, or vice versa.

**"The token is not authorized for this scope"** (401): The token doesn't have the required scope. Agency tokens can't access CRM data; Sub-Account tokens can't manage locations.

**"Token's user type mismatch"** (401): You're using the wrong token type for this endpoint (e.g., Agency token on a Sub-Account-only endpoint).

**"LocationId can't be undefined"** (422): You forgot the `locationId` query parameter.

## Resources

- [GoHighLevel API Documentation](https://highlevel.stoplight.io/docs/integrations/)
- [GoHighLevel Marketplace](https://marketplace.gohighlevel.com/docs/)
- [Private Integration Token Guide](https://marketplace.gohighlevel.com/docs/integrations/custom-token)
- [Maton Community](https://discord.com/invite/dBfFAcefs2)
- [Maton Support](mailto:support@maton.ai)
