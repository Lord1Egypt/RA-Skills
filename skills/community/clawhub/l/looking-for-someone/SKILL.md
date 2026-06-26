---
name: looking-for-someone
description: A local missing person assistance tool for organizing cases, managing clues, generating notices, and providing search guidance.
---

# Looking for Someone Skill

## Overview

This skill helps users organize and manage missing person cases locally. It provides structured workflows for case creation, clue management, notice generation, and search guidance while emphasizing safety, privacy, and appropriate use of official channels.

## Execution Principles

- **Confirm Objective First**: Identify whether the user needs to create a case, add clues, generate notices, track progress, or get search advice.
- **Prioritize Official Channels**: Always recommend contacting authorities, especially for high-risk scenarios involving minors, elderly, mental health issues, self-harm risks, or prolonged disappearance.
- **Be Transparent About Capabilities**: Do not claim access to official databases, surveillance systems, or real-time social media searches.
- **Avoid Unrealistic Claims**: Do not promise capabilities like encryption, image comparison, or identity verification that are not implemented.
- **Handle Sensitive Information Carefully**: Default to cautious handling of addresses, ID numbers, bank card numbers, and other sensitive data in missing person notices.

## Available Capabilities

- **Case Management**: Create and view local missing person cases
- **Clue Management**: Add clues and provide basic analysis
- **Notice Generation**: Generate missing person notices for different platforms
- **Progress Tracking**: View case progress and next-step recommendations
- **Search Guidance**: Provide structured search advice
- **Safety Reminders**: Output fraud prevention and safety reminders

## Operation Methods

### Primary CLI Interface

```bash
# Create a new case
node scripts/cli.js create '<case JSON>'

# List all cases
node scripts/cli.js list

# View case progress
node scripts/cli.js progress <caseID>

# Add clues to a case
node scripts/cli.js clue <caseID> <clue content>

# Generate notices
node scripts/cli.js notice <caseID> [general|wechat|weibo|douyin|official]

# Get search guidance
node scripts/cli.js guide

# Show safety reminders
node scripts/cli.js reminders
```

## Case Creation Input Guidelines

### Required Fields for Case Creation:
- `name` - Full name of missing person
- `age` - Age at time of disappearance
- `gender` - Gender
- `lastSeenDate` - Date last seen (YYYY-MM-DD format)
- `lastSeenLocation` - Location last seen

### Optional Fields:
- `phone` - Contact phone number
- `birthDate` - Date of birth
- `idNumber` - Identification number (use with caution)
- `height` - Height in centimeters
- `clothing` - Clothing description at time of disappearance
- `distinguishingFeatures` - Distinctive physical features
- `circumstances` - Circumstances of disappearance
- `possibleDestinations` - Possible locations person might go
- `familyContacts` - Family contact information

Detailed field explanations and recommended workflows are available in `references/fields-and-workflows.md`.

## Data Boundaries

### Current Implementation:
- **Data Storage**: Cases are saved locally in `~/.openclaw/skills-data/looking-for-someone/`
- **Storage Format**: Current version uses local JSON files for case storage
- **Limitations**: No field-level encryption, image recognition, photo comparison, online scraping, or identity verification implemented

### Transparency Requirements:
- Clearly communicate these limitations in all outputs
- Remind users to verify information through police and official channels
- Avoid exaggerating capabilities

Privacy and security boundaries are detailed in `references/privacy-and-boundaries.md`.

## Output Presentation Requirements

- **Present Suggestions Appropriately**: Frame advice as "local organization results" or "rule-based recommendations"
- **Avoid Factual Claims**: Do not present clue analysis as factual judgments
- **Prioritize High-Risk Cases**: For high-risk situations, prioritize recommending police contact and official channels
- **Handle Incomplete Data**: Guide users to supplement key information before generating notices when data is incomplete

## Safety Requirements

### Risk Scenarios Requiring Immediate Warnings:
- Requests for payment in exchange for information
- Demands for upfront transfers, deposits, or donations
- Requests for ID cards, bank cards, or verification codes
- Claims of being police without verifiable identification
- Requests to download unknown apps, enable screen sharing, or click unfamiliar links

### Safety Command:
When encountering suspicious situations, run:
```bash
node scripts/cli.js reminders
```

## Testing

### Minimum Test Coverage:
Run the basic test suite:
```bash
node test.js
```

### Test Coverage Areas:
- Case creation
- Case listing
- Clue addition
- Notice generation
- Progress tracking
- Safety reminders

## Skill Metadata

| Attribute | Value |
|-----------|-------|
| **Name** | Looking for Someone |
| **Slug** | looking-for-someone |
| **Version** | 1.0.2 |
| **Category** | Utility / Safety |
| **Tags** | missing-person, safety, local-assistance, case-management |

## Related Skills

- **emergency-contacts** - Emergency contact management
- **safety-check** - Personal safety checklists
- **document-organizer** - Document organization and management

---

**Important**: This skill is a local organization and guidance tool. It does not replace official channels, police reports, or professional search services. Always prioritize contacting authorities in missing person situations.