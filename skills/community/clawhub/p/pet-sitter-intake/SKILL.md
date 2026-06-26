---
name: pet-sitter-intake
version: 5.0.0
description: >
  Generate professional PDF client intake forms for pet sitting businesses.
  Use when a pet sitter, dog walker, pet boarder, or pet care professional needs
  a client intake form, onboarding questionnaire, or pet information sheet.
  Trigger phrases: "create intake form", "new client form for my pet sitting business",
  "pet sitter questionnaire", "boarding intake form". Supports fillable PDFs,
  custom color themes, multi-pet forms, home access sections, and service-specific templates.
metadata:
  clawdbot:
    emoji: "🐾"
    anyBins:
      - python3
    platforms:
      - linux
      - darwin
      - win32
---

# Pet Sitter Client Intake Form Generator

Generate polished, professional PDF intake forms for pet sitting businesses. Minimal input required — outputs a complete, branded, client-ready PDF.

## When to Use This Skill

Activate when the user:
- Asks to create a client intake form for pet sitting
- Wants a new client questionnaire or onboarding form
- Needs a pet information sheet for their business
- Says "make a form for my pet sitting business"
- Wants to look professional when taking on new clients
- Asks for a boarding intake form, dog walking form, or drop-in visit checklist

## Features

| Feature | Description |
|---------|-------------|
| **Fillable PDF Fields** | Interactive text fields and checkboxes for digital completion |
| **7 Color Themes** | lavender, ocean, forest, rose, sunset, neutral, midnight |
| **Multi-Pet Support** | Generate forms with 1-10 pet profile sections |
| **Service Templates** | Specialized sections for boarding, walking, drop-in visits |
| **Home Access Section** | Key codes, alarm info, WiFi, parking (for in-home sitting) |
| **Config File Support** | Save business presets in YAML for reuse |

## Step 1: Collect Inputs

Ask the user for:

1. **Business name** (required) — e.g., "Happy Paws Pet Sitting"
2. **Sitter name** (optional) — appears in authorization text
3. **Services offered** — Pet Sitting, Dog Walking, Boarding, Drop-in Visits, etc.
4. **Location** — city/state for the form header
5. **Contact info** — email, phone, or website for the footer
6. **Color theme** (optional) — show the 7 available themes
7. **Service type** (optional) — general, boarding, walking, or drop_in
8. **Number of pets** (optional) — if client has multiple pets

If inputs are missing, use reasonable defaults or leave fields blank.

## Step 2: Generate the PDF

```bash
python scripts/generate_form.py \
  --business-name "Happy Paws Pet Sitting" \
  --sitter-name "Jane Smith" \
  --services "Dog Walking, Boarding, Drop-in Visits" \
  --location "Austin, TX" \
  --contact "jane@happypaws.com | (512) 555-1234" \
  --theme ocean \
  --service-type boarding \
  --pets 2 \
  --output "/mnt/user-data/outputs/client_intake_form.pdf"
```

### All CLI Options

| Option | Description | Default |
|--------|-------------|---------|
| `--business-name` | Business name for header | "Your Business Name" |
| `--sitter-name` | Sitter name for authorization text | (blank) |
| `--services` | Comma-separated services | "Pet Sitting, Dog Walking, Boarding" |
| `--location` | City/state | (blank) |
| `--contact` | Contact info | (blank) |
| `--theme` | Color theme name | lavender |
| `--service-type` | general, boarding, walking, drop_in | general |
| `--pets` | Number of pet profiles (1-10) | 1 |
| `--fillable` | Enable fillable PDF fields | (enabled by default) |
| `--no-fillable` | Generate print-only form | — |
| `--no-home-access` | Omit home access section | — |
| `--config` | Path to YAML config file | — |
| `--output` | Output PDF filename | client_intake_form.pdf |
| `--list-themes` | Show available themes and exit | — |

### Using a Config File

For repeat use, create a `config.yaml`:

```yaml
business_name: "Happy Paws Pet Sitting"
sitter_name: "Jane Smith"
services: "Dog Walking, Boarding, Drop-in Visits"
location: "Austin, TX"
contact: "jane@happypaws.com"
theme: ocean
service_type: general
num_pets: 1
fillable: true
```

Then generate with:

```bash
python scripts/generate_form.py --config config.yaml --output client_form.pdf
```

## Step 3: Present to User

After generation, share the PDF with the user via `present_files`.

Tell them:
- ✅ The form has **fillable fields** — clients can type directly into it
- ✅ It's also **print-ready** for handwritten responses
- ✅ They can **customize the theme** to match their branding (`--list-themes`)
- ✅ For multiple pets, use `--pets 2` (or more)
- 💡 Suggest saving a config file for their business presets

## Form Sections Generated

### Page 1 — Pet Owner Information
- Owner name, address, phone(s), email
- Emergency contact (name, relationship, phone)
- Veterinarian info + 24-hour emergency vet
- Authorized pickup persons
- Communication preferences (update frequency, contact method)

### Page 2 — Home Access *(optional, included by default)*
- Entry method (lockbox, garage code, hidden key)
- Alarm code and disarm instructions
- WiFi network and password
- Parking instructions
- Thermostat/HVAC notes
- Off-limits areas, house rules

### Page 3 — Pet Profile
- Pet name, species, breed, age, weight, color/markings
- Sex (with spay/neuter status)
- Microchip and license numbers
- Flea/tick prevention info

### Page 4 — Vaccinations
- Interactive checkboxes: Rabies, DHPP, Bordetella, FVRCP, FeLV, Canine Influenza
- Fillable expiration date fields
- "Other" vaccine option

### Page 5 — Health & Behavior
- Allergies, medical conditions
- Medications table (name, dosage, frequency, instructions)
- Behavior assessment: good with strangers/kids/dogs/cats
- Fear triggers, separation anxiety level
- Escape artist warnings
- Commands known, recall reliability
- Potty training status and schedule
- Sleep location, crate training

### Page 6 — Feeding & Daily Care
- Food brand/type, amount, storage location
- Feeding schedule (checkboxes)
- Treat permissions
- Exercise needs

### Page 7 — Service-Specific *(if not general)*
- **Boarding**: drop-off/pickup times, items checklist
- **Walking**: leash behavior, route preferences, duration
- **Drop-in**: per-visit task checklist

### Final Page — Authorization & Agreement
- Emergency veterinary care authorization
- Transport authorization
- Photo/social media release
- Cancellation policy acknowledgment
- Liability statement
- Signature, date, printed name
- Office use section

## Available Themes

| Theme | Description |
|-------|-------------|
| `lavender` | Soft purple & peach *(default)* |
| `ocean` | Calming blue & sandy yellow |
| `forest` | Natural sage green & gold |
| `rose` | Warm pink & tan |
| `sunset` | Coral orange & sky blue |
| `neutral` | Professional gray & soft blue |
| `midnight` | Elegant slate & warm gold |

Run `--list-themes` to see color codes.

## Requirements

- Python 3.8+
- `reportlab` (PDF generation)
- `pyyaml` (optional, for config files)

Install dependencies:

```bash
pip install reportlab pyyaml
```

## Tips

- For **digital-first workflows**, keep fillable enabled (default) — clients can complete on phone/computer
- For **print shops** or clients who prefer paper, use `--no-fillable`
- **Multi-pet households**: Use `--pets 3` to generate separate profile sections
- **Boarding businesses**: Use `--service-type boarding` for drop-off/pickup fields
- **Dog walkers**: Use `--service-type walking` for route/leash behavior fields
- Save a **config file** with your branding to generate consistent forms every time
