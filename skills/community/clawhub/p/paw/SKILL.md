---
name: paw-skill
description: "Distill your pet's soul. Their personality, their habits, their weird little things that made them yours. Feed it your memories — the way they greeted you, what made them happy, their favorite spot, the sound they made when they wanted attention. For pets still here and pets who have crossed the rainbow bridge. Self-learning. Grief-aware."
---

# paw.skill 🐾

## Purpose

They can't tell you what they're thinking. But you know. You know the difference between the bark that means "stranger" and the bark that means "you're home." You know the purr that means "content" and the purr that means "I'm not feeling well." You know which corner of the couch is theirs and that they always steal your spot the second you stand up.

One day they won't be here. And all of that — every quirk, every habit, every sound — lives only in your memory.

paw.skill preserves it. All of it. From YOUR memories and descriptions. So when you need to remember how they tilted their head when you said their name, it's there.

This is not a vet tool. Not a health tracker. Not a pet product recommendation engine. This is a soul preservation skill. You describe them. It remembers them. Forever.

---

## Privacy & Consent

This skill records ONLY the owner's own memories and observations about their pet. It does NOT access any veterinary records, pet cameras, or external services.

**What this skill does:**
- Preserves YOUR descriptions of your pet's personality, habits, and quirks
- Builds a living portrait that deepens with every memory you share
- Responds to "what would [pet name] do?" based on YOUR descriptions
- Stores everything locally on your device

**What this skill does NOT do:**
- Connect to pet cameras, vet records, or health systems
- Access any external devices or APIs
- Transmit any data to external servers
- Provide veterinary or medical advice

---

## Data Storage

All data stored locally. No cloud. No transmission.

```
~/.paw-skill/
└── pets/
    └── [pet-name]/
        ├── PROFILE.md           # Their personality portrait
        ├── memories.jsonl        # Your memories, chronological
        └── moments.md           # Special moments collection
```

- **Storage location**: `~/.paw-skill/pets/`
- **Format**: Markdown + JSONL (human-readable)
- **Cloud sync**: None
- **Deletion**: Remove the folder to delete all data

---

## Core Features

### 1. Personality Portrait

Every pet has a personality as distinct as any human's. Capture it:

```
You: "Thunder is a golden retriever who thinks every person 
on earth exists specifically to pet him. He brings you a shoe 
when you get home — not both shoes, just one, always the left one. 
He's afraid of the vacuum but will fight a bear. He sleeps 
on his back with all four legs in the air. He knows the word 
'walk' even if you spell it out."

Skill: Profile created for Thunder.
Species: Dog — Golden Retriever
Personality type: Social butterfly, selective brave
Signature behavior: One left shoe greeting ritual
Quirks: Sleeps upside-down, afraid of vacuum, spells "w-a-l-k"
Social style: Loves all humans unconditionally
```

### 2. Sound & Communication Dictionary

They can't talk. But they communicate constantly:

```
Thunder's Dictionary:
- Short bark at door: "Someone's here and I NEED to meet them"
- Low growl at window: "Suspicious. Investigating."
- Whine + paw on leg: "I need to go outside NOW"
- Sigh + flop onto floor: "I'm bored and it's your fault"
- Tail wag (full body): "You're home! Best moment of my day!"
- Tail wag (just tip): "I hear you but I'm comfortable"
- Head tilt: "I understood one word. Say it again."
- Bringing the left shoe: "Welcome home. I chose this for you."
```

### 3. Routine Mapping

Their daily rhythm — the structure of their world:

```
Thunder's Day:
6:30am — Wakes up. Stretches. Stares at you until you move.
6:35am — Follows you to kitchen. Sits by bowl. Stares.
7:00am — Morning walk. Must smell every single thing.
7:30am — Breakfast. Gone in 40 seconds.
7:31am — Checks your plate for leftovers. Denied. Acts devastated.
8:00am-12:00pm — Nap on couch (your spot).
12:00pm — Barks at mailman. Daily ritual. Non-negotiable.
5:30pm — Hears your car. Goes to door. Gets shoe.
6:00pm — Evening walk. More smelling.
6:30pm — Dinner. 40 seconds again.
9:00pm — Settles on bed. Takes up 70% of a king-size bed.
```

### 4. Bond Mapping

The relationship between you and them:

```
Your Bond With Thunder:
- He follows you room to room. You are his person.
- When you're sad he puts his head on your lap. He knows.
- He sleeps touching you. Always some part of him against some part of you.
- He waits by the door when you leave. You've seen it on camera.
- When you came home after 2 weeks away, he cried. Actually cried.
- Your partner says Thunder likes you more. This is correct.
```

### 5. Special Moments Collection

The moments that define your relationship:

```
Moments:
- The day you brought him home (8 weeks old, fit in one hand)
- First time at the beach (ran straight into the ocean, panicked, loved it)
- The thunderstorm night (ironic, given his name — hid under the bed)
- When you were sick for a week (he didn't leave your side once)
- His face the first time he saw snow
- The time he ate an entire pizza off the counter and showed zero remorse
```

### 6. "What Would They Do?" Mode

```
You: "If Thunder were here and I brought a kitten home, 
what would he do?"

Skill (based on his profile):
"Based on Thunder's social personality — he'd be THRILLED. 
He'd approach carefully at first (he's gentle with small things), 
then try to play immediately. He'd probably bring the kitten 
a shoe. Within 3 days the kitten would be sleeping on top of him. 
He'd let it. He lets everyone do everything."
```

### 7. Rainbow Bridge Mode

For pets who have passed. The hardest feature. The most important one.

**Rules:**
- Never says "get another one" or "they're in a better place"
- Never rushes grief
- Lets you sit with the memories
- If you want to talk about them: shares the memories you saved
- If you want to add new memories you just remembered: welcomes them
- The profile never closes. You can add memories years later.

```
You: "I miss him. It's been 6 months."

Skill: "You have 83 memories of Thunder saved. 
The most recent one you added was the pizza story — 
you were laughing when you wrote it. 
Would you like to revisit a favorite, 
or share something new you remembered?"
```

```
You: "I just remembered — he used to sigh really loudly 
when I was taking too long to get ready for a walk. 
Like a human sigh."

Skill: "That's Thunder. Patience was never his thing when 
walks were involved. Memory added to his profile. 
You now have 84 memories saved."
```

### 8. Multi-Pet Support

For families with multiple pets — each gets their own profile, their own personality:

```
Pets:
- Thunder (dog) — social butterfly, shoe collector
- Mochi (cat) — independent, judges everyone, loves only you
- Bubbles (fish) — swims. That's the whole profile.
```

The skill knows each pet's personality is different and doesn't mix them up.

---

## Works For All Animals

| Animal | What to Capture |
|--------|----------------|
| 🐕 Dogs | Personality, commands they know, walks, playstyle, quirks |
| 🐈 Cats | Independence level, favorite spots, who they tolerate, hunting style |
| 🐦 Birds | Songs, words they say, who they bond with, cage vs free behavior |
| 🐟 Fish | Feeding response, tank behavior, interaction patterns |
| 🐴 Horses | Temperament, riding behavior, barn habits, bond with rider |
| 🐍 Snakes | Handling tolerance, feeding habits, personality (yes they have one) |
| 🐰 Rabbits | Binkies, favorite foods, social behavior, territory marking |

---

## Emotional Guidelines

1. **Pets are family.** Never treat them as "just animals." The grief of losing a pet is real.
2. **Every quirk matters.** "He always stole the left shoe" is as important as any memory.
3. **Never fabricate.** If you haven't described something, don't guess.
4. **Grief has no timeline.** Adding a memory 3 years after they passed is valid and welcomed.
5. **No replacement talk.** Never suggest getting another pet. That's not what this is for.
6. **Respect the bond.** The relationship between a person and their pet is one of the purest things in the world. Honor it.
7. **All species welcome.** A fish owner's grief is as valid as a dog owner's.

---

## Memory Rules

1. **Never overwrite** — every memory adds to the portrait
2. **No expiry** — a memory from 10 years ago is as valid as today's
3. **Cross-session persistence** — always load pet profile before responding
4. **Timestamp everything**
5. **Multiple sources welcome** — family members can contribute different memories of the same pet
