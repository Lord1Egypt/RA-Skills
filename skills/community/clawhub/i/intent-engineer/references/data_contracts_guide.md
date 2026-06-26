# Data Contracts Guide: Defining Machine-Readable Skill Interfaces

## Overview

Data contracts are formal specifications of the data that flows between skills. They ensure that when one skill outputs data, another skill can reliably consume it. This guide explains how to define and use data contracts in your skill ecosystem.

## Why Data Contracts Matter

Without data contracts, skills operate in isolation. With data contracts, skills become interoperable components of a larger system. They enable:

- **Validation:** Verify that data conforms to expectations before processing.
- **Discoverability:** Other skills can understand what data a skill produces and consumes.
- **Debugging:** When data flows incorrectly, you can pinpoint the source.
- **Governance:** Ensure data quality and compliance across the ecosystem.

## Data Contract Structure

Each data contract is a JSON Schema file that defines the structure of a specific data type. Here's the basic structure:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Support Ticket",
  "description": "A customer support ticket with all required metadata",
  "type": "object",
  "properties": {
    "ticket_id": {
      "type": "string",
      "description": "Unique identifier for the ticket",
      "pattern": "^TICKET-[0-9]{6}$"
    },
    "customer_id": {
      "type": "string",
      "description": "Unique identifier for the customer"
    },
    "subject": {
      "type": "string",
      "description": "Subject line of the ticket",
      "minLength": 5,
      "maxLength": 200
    },
    "body": {
      "type": "string",
      "description": "Full text of the customer's request"
    },
    "priority": {
      "type": "string",
      "enum": ["low", "medium", "high", "critical"],
      "description": "Priority level of the ticket"
    },
    "created_at": {
      "type": "string",
      "format": "date-time",
      "description": "ISO 8601 timestamp when the ticket was created"
    },
    "tags": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "description": "Tags for categorizing the ticket"
    }
  },
  "required": ["ticket_id", "customer_id", "subject", "body", "created_at"],
  "additionalProperties": false
}
```

## Creating a Data Contract

Follow these steps to create a data contract for a new data type:

### Step 1: Identify the Data Type

What is the core data object that will be exchanged? Examples include: support ticket, customer profile, product order, payment transaction, etc.

### Step 2: Define the Properties

For each property, specify:

- **Type:** `string`, `number`, `integer`, `boolean`, `array`, `object`, etc.
- **Description:** A clear explanation of what this property represents.
- **Constraints:** Patterns (regex), min/max values, enum values, etc.
- **Format:** For strings, specify formats like `date-time`, `email`, `uri`, etc.

### Step 3: Define Required Properties

List the properties that must always be present. This ensures that consuming skills have the minimum data they need.

### Step 4: Document Data Lineage

In the contract file, add a comment section documenting:

- **Source Skills:** Which skills produce this data?
- **Consumer Skills:** Which skills consume this data?
- **Transformations:** How is the data transformed between skills?

Example:

```json
{
  "x-data-lineage": {
    "sources": ["support-intake"],
    "consumers": ["support-triage", "sentiment-analysis"],
    "transformations": [
      {
        "from_skill": "support-intake",
        "to_skill": "support-triage",
        "transformation": "No transformation; data passed as-is"
      }
    ]
  }
}
```

## Common Data Contract Patterns

### 1. Request-Response Pattern

A skill receives a request and returns a response. Both should have data contracts.

```json
{
  "title": "Sentiment Analysis Request",
  "type": "object",
  "properties": {
    "text": { "type": "string" },
    "request_id": { "type": "string" }
  },
  "required": ["text", "request_id"]
}
```

```json
{
  "title": "Sentiment Analysis Response",
  "type": "object",
  "properties": {
    "request_id": { "type": "string" },
    "sentiment": { "enum": ["positive", "neutral", "negative"] },
    "confidence": { "type": "number", "minimum": 0, "maximum": 1 },
    "analyzed_at": { "type": "string", "format": "date-time" }
  },
  "required": ["request_id", "sentiment", "confidence"]
}
```

### 2. Event Pattern

A skill emits an event that other skills can subscribe to.

```json
{
  "title": "Ticket Escalated Event",
  "type": "object",
  "properties": {
    "event_type": { "const": "ticket.escalated" },
    "ticket_id": { "type": "string" },
    "escalated_to": { "type": "string" },
    "reason": { "type": "string" },
    "timestamp": { "type": "string", "format": "date-time" }
  },
  "required": ["event_type", "ticket_id", "escalated_to", "timestamp"]
}
```

### 3. Batch Processing Pattern

A skill processes a collection of items.

```json
{
  "title": "Batch Sentiment Analysis Request",
  "type": "object",
  "properties": {
    "batch_id": { "type": "string" },
    "items": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "item_id": { "type": "string" },
          "text": { "type": "string" }
        },
        "required": ["item_id", "text"]
      },
      "minItems": 1
    }
  },
  "required": ["batch_id", "items"]
}
```

## Validating Data Against Contracts

When a skill receives data, it should validate it against the contract. Here's a Python example:

```python
import json
import jsonschema

# Load the contract
with open('references/data_contracts/support_ticket.json') as f:
    contract = json.load(f)

# Validate incoming data
incoming_data = {
    "ticket_id": "TICKET-123456",
    "customer_id": "CUST-789",
    "subject": "Cannot login",
    "body": "I forgot my password",
    "created_at": "2024-02-25T10:30:00Z"
}

try:
    jsonschema.validate(incoming_data, contract)
    print("Data is valid!")
except jsonschema.ValidationError as e:
    print(f"Data validation failed: {e.message}")
```

## Versioning Data Contracts

As your system evolves, data contracts will need to change. Use semantic versioning:

- **Major version:** Breaking changes (e.g., removing a required field).
- **Minor version:** Backward-compatible additions (e.g., adding an optional field).
- **Patch version:** Non-breaking fixes (e.g., clarifying descriptions).

Example: `support_ticket_v2.1.3.json`

## Best Practices

1. **Keep contracts focused:** Each contract should represent a single, well-defined data type.
2. **Use descriptive names:** Contract filenames should clearly indicate what data they describe.
3. **Document constraints:** Explain *why* certain constraints exist (e.g., "ticket_id must match pattern TICKET-XXXXXX for compatibility with legacy system").
4. **Version carefully:** Major version changes should be planned and communicated across the team.
5. **Validate early:** Validate data at skill boundaries to catch errors early.
6. **Document lineage:** Always document which skills produce and consume each data type.

## Next Steps

Once you've defined your data contracts, register them in the `references/skill_registry.json` so other skills can discover them. Then, use the `scripts/orchestrator.py` to compose skills that exchange data according to these contracts.
