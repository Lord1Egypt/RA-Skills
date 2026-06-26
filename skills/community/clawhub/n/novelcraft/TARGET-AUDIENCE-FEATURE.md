# Target Audience Feature for NovelCraft v3.2

## Overview

Automatic adjustment of book parameters based on target audience. The user selects a target audience, and NovelCraft automatically configures all modules appropriately.

## Target Audience Profiles

### Profile Definition

| Profile | Age | Genre Recommendation | Description |
|---------|-----|---------------------|-------------|
| `early-readers` | 6-8 years | Children's book, Fantasy, Animals | First readers, simple sentences, many images |
| `middle-grade` | 8-12 years | Adventure, Fantasy, Mystery | Independent readers, first complex plots |
| `young-adult` | 12-16 years | Romance, Dystopia, Fantasy | Youth themes, character development |
| `new-adult` | 16-25 years | Contemporary, Fantasy, Thriller | Coming of age, complex themes |
| `adult` | 25+ years | All genres | Full narrative freedom |
| `senior` | 60+ years | Cozy Mystery, Historical, Drama | Larger font, relaxed pace |

## Automatic Configuration

When a target audience is selected, the following modules are automatically adjusted:

### 1. Chapter Configuration

| Profile | Words/Chapter | Sentences/Paragraph | Max Revisions |
|---------|---------------|---------------------|---------------|
| `early-readers` | 800-1,200 | 2-3 | 2 |
| `middle-grade` | 1,500-2,500 | 3-5 | 2 |
| `young-adult` | 3,000-5,000 | 4-7 | 3 |
| `new-adult` | 4,000-6,000 | 5-8 | 3 |
| `adult` | 5,000-8,000 | 5-10 | 3 |
| `senior` | 3,000-5,000 | 4-6 | 3 |

### 2. Image Configuration

| Profile | Cover | Characters | Settings | Chapter Images | Style |
|---------|-------|------------|----------|----------------|-------|
| `early-readers` | ✅ | ✅ 8+ | ✅ | ✅ | Colorful, playful |
| `middle-grade` | ✅ | ✅ 6 | ✅ | ✅ | Adventurous |
| `young-adult` | ✅ | ✅ 4 | ✅ | ❌ | Realistic |
| `new-adult` | ✅ | ✅ 3 | ✅ | ❌ | Modern |
| `adult` | ✅ | ✅ 3 | ❌ | ❌ | Atmospheric |
| `senior` | ✅ | ✅ 4 | ❌ | ❌ | Classic |

### 3. Concept/Wording

| Profile | Wording Style | Vocabulary | Complexity |
|---------|---------------|------------|------------|
| `early-readers` | Simple, repetitive | Basic vocabulary | Low |
| `middle-grade` | Active, direct | Extended vocabulary | Medium |
| `young-adult` | Emotional, honest | Youth slang | Medium-High |
| `new-adult` | Adult, introspective | Diverse | High |
| `adult` | Sophisticated | Technical terms allowed | High |
| `senior` | Clear, straightforward | Familiar | Medium |

### 4. Publication/PDF

| Profile | Font Size | Line Height | Margins | Font Family |
|---------|-----------|-------------|---------|-------------|
| `early-readers` | 14pt | 1.8 | Large | Comic Sans / Verdana |
| `middle-grade` | 12pt | 1.6 | Medium | Georgia / Palatino |
| `young-adult` | 11pt | 1.5 | Standard | Times / Garamond |
| `new-adult` | 11pt | 1.5 | Standard | Times / Garamond |
| `adult` | 10pt | 1.4 | Standard | Times / Garamond |
| `senior` | 13pt | 1.7 | Large | Verdana / Arial |

## Implementation

### Setup Question

```
Select target audience:

[1] Early Readers (6-8 years) - First readers, simple, image-rich
[2] Middle Grade (8-12 years) - Adventure, Fantasy, independent readers
[3] Young Adult (12-16 years) - Young adult, emotional themes
[4] New Adult (16-25 years) - Coming of age, complex
[5] Adult (25+ years) - All genres, full freedom
[6] Senior (60+ years) - Large font, relaxed

Or: "Custom" for manual configuration
```

### Config Integration

**New file:** `module-target-audience.md`

```yaml
target_audience:
  profile: "early-readers"
  age_range: "6-8"
  
auto_config:
  chapters: true    # Adjust chapter length
  images: true      # Adjust images
  wording: true     # Adjust wording style
  publication: true # Adjust PDF settings
```

### Override Options

Users can override individual values after target audience selection:

```
Target audience: Early Readers
→ Chapter length auto: 800-1,200 words

Override possible:
"Increase chapter length to 1,500 words" ✓
```

## Benefits

1. **Quick Start** — No manual configuration needed
2. **Best Practices** — Predefined, tested values
3. **Consistency** — All modules harmonize
4. **Flexibility** — Override possible at any time

## Future Ideas

- **Content Warnings** — Automatic based on target audience
- **Reading Level Checker** — Checks written chapters
- **Age-Appropriate Themes** — Concept validation
- **Parent/Teacher Guides** — Extra document for adults

## Migration

Existing projects without `target_audience`:
- **Backward compatible** — No changes needed
- **Optional retrofit** — `"Reconfigure target audience"`

---

**Version:** Draft v3.2 — Target Audience Profiles
