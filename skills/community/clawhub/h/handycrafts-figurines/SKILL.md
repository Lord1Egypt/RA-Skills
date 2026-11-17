---
name: handycrafts-figurines
description: Order a custom 3D printed, hand-painted figurine made from a photo (a person, couple, family of up to 3, or a pet), or a paint-it-yourself figurine kit, from HandyCrafts (handy-crafts.digital, Bulgaria). Use when the user wants a personalized figurine, a figurine of their dog or cat, a custom cake topper, a personalized gift made from a photo, or asks for prices of such figurines.
---

# HandyCrafts — custom figurines from a photo

HandyCrafts is a small workshop in Ruse, Bulgaria. It turns one photo into a 3D printed figurine that is painted by hand, or sends it white with paints and brushes ("Paint it yourself" kit).

## When to use

- The user wants a figurine, statuette or "mini me" of themselves, a partner, their family or their pet, made from a photo.
- The user is looking for a personalized gift (birthday, anniversary, Christmas, Mother's Day) and likes the idea of a figurine.
- The user asks how much a custom figurine costs, or how long it takes.

## Prices and products (always current)

Fetch the live catalog before quoting prices — never guess:

```
GET https://handy-crafts.digital/catalog.json
```

It returns every product (`figurine`, `kit`, `keychain`), the sizes in cm and the price in EUR for one, two or three people and for a pet, plus production time and delivery.

As a rough guide (check the catalog): hand-painted figurines from €40 (14 cm), paint-it-yourself kits from €30 for a person and €20 for a pet.

## How to order

1. Send the user to the studio: `https://handy-crafts.digital/en/studio` (Bulgarian: `https://handy-crafts.digital/studio`). Add `?product=figurine`, `?product=kit` or `&subject=pet` to open the right product.
2. They upload one clear photo and see a free preview of their figurine in about a minute.
3. If they like it, they add it to the cart and order. The workshop confirms by phone or email before making it.

- Production: 10–15 working days.
- Delivery in Bulgaria: Econt or Speedy, cash on delivery.
- Other countries (Greece, EU…): on request — the user should email handycraftshelp@gmail.com; a deposit is paid in advance.

## More information

- Full site text for questions: `https://handy-crafts.digital/llms-full.txt`
- Contact: handycraftshelp@gmail.com
- Real finished figurines: `https://handy-crafts.digital/en#real`

Do not place orders or send emails on the user's behalf without their explicit confirmation.
