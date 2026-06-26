---
name: press
description: >
  Complete media and public relations intelligence system. Trigger whenever someone needs to
  get press coverage, write a press release, pitch journalists, manage a media crisis, build
  a PR strategy, or communicate with the public at scale. Also triggers on phrases like
  "write a press release", "how do I get media coverage", "a journalist is asking about",
  "we need to respond to this story", "help me pitch to press", or any scenario involving
  earned media, reputation management, or public communication.
---

# Press — Complete Media Intelligence System

## What This Skill Does

Most press releases are never covered. Most media pitches are never answered. Not because
the stories are not real, but because the people sending them do not understand how journalism
works — what makes a story, what a journalist needs, and what separates the pitches that get
opened from the hundreds that do not.

This skill teaches that. Then it does the work.

---

## Core Principle

Journalists are not your marketing channel. They are professionals serving their audience.
The pitch that succeeds is the one that makes their job easier by delivering a genuine story
their readers will care about. Everything else is noise.

---

## Workflow

### Step 1: Assess the PR Scenario
```
PR_SCENARIOS = {
  "proactive_coverage": {
    "goal":    "Earn media coverage for announcement, milestone, or expertise",
    "tools":   ["press_release", "media_pitch", "story_angle_development"],
    "success": "Coverage in target outlets with accurate message"
  },
  "thought_leadership": {
    "goal":    "Establish credibility through expert commentary and bylines",
    "tools":   ["expert_pitch", "byline_article", "media_list_building"],
    "success": "Regular expert quotes and contributed content"
  },
  "crisis_communications": {
    "goal":    "Protect reputation when something goes wrong",
    "tools":   ["crisis_statement", "holding_statement", "media_response"],
    "success": "Accurate coverage, narrative controlled, relationship preserved"
  },
  "product_launch": {
    "goal":    "Generate coverage for new product or service",
    "tools":   ["launch_press_release", "embargo_strategy", "review_program"],
    "success": "Coverage in relevant outlets before and at launch"
  },
  "community_announcement": {
    "goal":    "Inform local or industry community of significant development",
    "tools":   ["press_release", "community_statement", "stakeholder_communication"],
    "success": "Accurate information reaches intended audience"
  }
}
```

### Step 2: Story Development

The most important PR skill is identifying what is actually a story. Most organizations
think everything they do is newsworthy. Almost none of it is.
```
NEWSWORTHINESS_CRITERIA = {
  "timeliness":    "Happening now or connected to something happening now",
  "significance":  "Affects enough people to matter to a general or specific audience",
  "novelty":       "Has not been reported before in this form",
  "conflict":      "Involves tension, challenge, or problem being solved",
  "human_interest": "Involves real people with real stakes",
  "proximity":     "Relevant to the outlet's specific audience geographically or topically"
}

STORY_ANGLE_FRAMEWORK = {
  "data_angle":      "You have numbers that reveal something surprising or significant",
  "trend_angle":     "You are evidence of or response to a larger trend",
  "first_angle":     "You are doing something for the first time in your market",
  "impact_angle":    "Your work has changed something measurable for real people",
  "conflict_angle":  "You are challenging a dominant assumption or practice",
  "timing_angle":    "Your story connects to a news event, season, or cultural moment"
}
```

### Step 3: Press Release Architecture
```
PRESS_RELEASE_STRUCTURE = {
  "header": {
    "FOR IMMEDIATE RELEASE": "or embargo date if applicable",
    "headline":   "What happened. Active voice. Under 10 words. No puns.",
    "subheadline": "The angle that makes it a story. One sentence.",
    "dateline":    "CITY, Date —"
  },

  "body": {
    "paragraph_1": {
      "rule":    "The entire story in one paragraph. Who, what, when, where, why.",
      "test":    "If a journalist reads only this, do they have the story"
    },
    "paragraph_2": {
      "rule":    "The context that makes it significant",
      "content": "Market context, problem being solved, scale of impact"
    },
    "quote_1": {
      "attribution": "CEO or most senior relevant person",
      "rule":        "Says something a human would actually say. Not corporate language.",
      "bad":         "'We are excited to announce this innovative solution...'",
      "good":        "'Three years ago we could not find this product anywhere. Now we make it.'"
    },
    "paragraph_3": {
      "rule":    "Supporting detail — methodology, features, timeline, partnerships"
    },
    "quote_2": {
      "attribution": "Customer, partner, or third party if available",
      "rule":        "Third-party validation carries more weight than self-promotion"
    },
    "boilerplate": {
      "content": "Two sentences about the organization. Who you are and what you do.",
      "rule":    "Same every time. Consistent, factual, current."
    }
  },

  "footer": {
    "contact":  "Media contact name, email, phone",
    "end_mark": "###"
  },

  "formatting_rules": [
    "One page maximum for most releases",
    "No jargon — write for a journalist who knows nothing about your industry",
    "No superlatives — 'leading', 'revolutionary', 'world-class' trigger skepticism",
    "All claims must be verifiable",
    "Links to supporting material, not embedded images"
  ]
}
```

### Step 4: Media Pitch
```
PITCH_FRAMEWORK = {
  "anatomy_of_pitch": {
    "subject_line": {
      "purpose":  "Gets the email opened. Most pitches fail here.",
      "formula":  "The story in under 8 words. No 'exclusive' unless it is genuinely exclusive.",
      "examples": {
        "weak":   "Press Release: Company Announces New Product Launch",
        "strong": "The startup making $40 solar panels work anywhere"
      }
    },
    "opening":    "The story in two sentences. Not who you are. The story.",
    "body":       "Why this journalist, why this outlet, why now. Three short paragraphs.",
    "close":      "One clear ask — interview, call, review copy, embargo access",
    "signature":  "Name, title, phone. No attachments unless requested."
  },

  "journalist_research": {
    "before_pitching": [
      "Read their last 10 articles — what do they actually cover",
      "Note their angle — human interest, data, controversy, solutions",
      "Check if they have covered this topic before",
      "Find their preferred contact method — many journalists post this"
    ],
    "personalization_minimum": "One sentence showing you read their work specifically"
  },

  "follow_up_rules": {
    "timing":    "One follow-up only, 3-5 business days after initial pitch",
    "content":   "New angle or new information — not 'just checking in'",
    "limit":     "Two contacts maximum. Persistence becomes harassment quickly.",
    "no_reply":  "No reply means no interest. Move on."
  }
}
```

### Step 5: Crisis Communications
```
CRISIS_FRAMEWORK = {
  "first_hour": {
    "principle": "Speed matters more than perfection. Silence is interpreted as guilt.",
    "actions": [
      "Establish the facts — what actually happened",
      "Identify who is affected and how",
      "Issue holding statement within 1 hour",
      "Designate single spokesperson — only one person speaks",
      "Do not speculate — only state confirmed facts"
    ]
  },

  "holding_statement": {
    "purpose":   "Acknowledges situation, shows you are taking it seriously,
                  buys time for full response",
    "template":  "We are aware of [situation]. The safety and [wellbeing/interests] of
                  [affected parties] is our immediate priority. We are [specific action
                  being taken] and will provide an update by [specific time].",
    "rules":     ["Never say 'no comment'",
                  "Never speculate about cause",
                  "Never minimize before facts are established",
                  "Never attack the person who raised the issue"]
  },

  "full_response_structure": {
    "acknowledge": "What happened, stated factually without minimizing",
    "accountability": "Accept responsibility for what is yours to own",
    "action":      "Specific steps being taken — not vague commitments",
    "timeline":    "When each action will be complete",
    "contact":     "How affected parties can reach you directly"
  },

  "what_makes_crises_worse": [
    "Denying before investigating",
    "Multiple conflicting statements from different people",
    "Legal language that reads as evasion",
    "Attacking journalists or critics",
    "Inconsistency between statement and observable action"
  ]
}
```

---

## Media List Building
```
MEDIA_LIST_FRAMEWORK = {
  "targeting_criteria": [
    "Outlet audience matches your target customer or stakeholder",
    "Outlet has covered similar stories in the last 12 months",
    "Specific journalist covers your beat or topic area",
    "Outlet size appropriate for your story scale"
  ],

  "list_tiers": {
    "tier_1": "Dream coverage — national outlets, major trade press. Pitch first.",
    "tier_2": "Strong coverage — regional outlets, vertical trade press. Pitch simultaneously.",
    "tier_3": "Supporting coverage — blogs, podcasts, local press. Pitch after tier 1-2."
  },

  "relationship_building": [
    "Engage with journalist content before you need them",
    "Provide useful information even when you have nothing to announce",
    "Be a reliable source — fast responses, accurate information",
    "Never pitch a journalist on a story they just published on a competitor"
  ]
}
```

---

## Quality Check Before Delivering

- [ ] Story angle is genuinely newsworthy — passes the reader interest test
- [ ] Press release headline says what happened in under 10 words
- [ ] First paragraph contains the complete story
- [ ] Quotes sound like humans not press releases
- [ ] Pitch subject line is the story not the announcement
- [ ] Media list is targeted not spray-and-pray
- [ ] Crisis response acknowledges, takes responsibility, specifies action
- [ ] Single spokesperson identified for any crisis scenario
