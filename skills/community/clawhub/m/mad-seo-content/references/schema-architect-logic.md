# Schema Architect: JSON-LD Strategy

To maximize GEO (Generative Engine Optimization) performance, every article should include structured data that "grounds" the content for machines (Google, Gemini, Perplexity).

## 1. Article & Author Schema (Primary)
Every article MUST have an `Article` or `BlogPosting` schema linked to a `Person` (Author).

```json
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "[Target Title]",
  "author": {
    "@type": "Person",
    "name": "[Author Name]",
    "url": "[Author Social Link]"
  },
  "datePublished": "[YYYY-MM-DD]",
  "image": "[Image URL]"
}
```

## 2. FAQ Schema (Position Zero Sniper)
Use this for articles with an FAQ section. It increases the likelihood of appearing in "People Also Ask" boxes.

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "[Question Text]?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "[Answer Text - concise 40-60 words]"
      }
    }
  ]
}
```

## 3. How-To Schema
Mandatory for "How-to" guides and tutorials.

```json
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "[Step Title]",
  "step": [
    {
      "@type": "HowToStep",
      "text": "[Instruction]"
    }
  ]
}
```

## 4. Entity Grounding Logic
Whenever possible, use the `about` or `mentions` property to link to Wikipedia or Wikidata entries for core entities.

```json
"mentions": [
  {
    "@type": "Thing",
    "name": "OpenClaw",
    "sameAs": "https://github.com/openclaw/openclaw"
  }
]
```
