# UX Writing Reference

Rules and patterns for writing UI text. Every string a user reads is a design decision.

---

## 1. Button Labels

Never use generic labels. Every button tells the user exactly what will happen.

### Banned Labels

| Never Use | Why |
|-----------|-----|
| OK | Tells user nothing about the action |
| Submit | Vague, form-era holdover |
| Yes / No | Forces user to re-read the question |
| Click here | Accessibility failure, no meaning |
| Cancel (alone) | Ambiguous without paired action context |

### Pattern: Verb + Object

```
Save changes
Create account
Delete 3 items
Export as PDF
Add to cart
Send invitation
Publish post
Archive conversation
```

### Destructive Actions: Name the Destruction + Show Count

```
// BAD
Are you sure?  [Yes] [No]

// GOOD
Delete 14 messages permanently?
This cannot be undone.
[Keep messages]  [Delete 14 messages]
```

```
// BAD
Remove items?  [OK] [Cancel]

// GOOD
Remove 3 items from your cart?
[Keep items]  [Remove 3 items]
```

### Paired Button Rules

| Scenario | Primary | Secondary |
|----------|---------|-----------|
| Save flow | Save changes | Discard |
| Creation | Create project | Cancel |
| Destructive | Keep items | Delete 5 items |
| Confirmation | Send invitation | Go back |
| Upload | Upload file | Choose different file |

The safe/non-destructive action is always visually more prominent (filled button). The destructive action is secondary (outlined or text-only).

---

## 2. Error Messages

### Formula: What Happened + Why + How to Fix

Every error message has three parts. Never skip "how to fix."

### Templates

**Format error:**
```
Title: Invalid email address
Body: Email addresses need an @ symbol and a domain (like name@example.com).
Action: [Fix email address]
```

**Missing required field:**
```
Title: Card number is required
Body: Enter your 16-digit card number to complete checkout.
// Inline: highlight the field, place message directly below it
```

**Permission denied:**
```
Title: You don't have access to this project
Body: Only project admins can change billing settings. Ask [Admin Name] to update your role or make this change for you.
Action: [Request access]  [Go back]
```

**Network error:**
```
Title: Can't connect right now
Body: Check your internet connection and try again. Your draft has been saved locally.
Action: [Try again]
```

**Server error (5xx):**
```
Title: Something went wrong on our end
Body: We're looking into it. Your data is safe. Try again in a few minutes, or contact support if this keeps happening.
Action: [Try again]  [Contact support]
```

**Rate limit:**
```
Title: Too many requests
Body: You've hit the rate limit. Try again in [X] seconds.
Action: [auto-countdown button: "Try again in 28s"]
```

### Rules

- Never blame the user. "Invalid input" becomes "This field needs a number between 1 and 100."
- Never use error codes alone. "Error 403" means nothing. Always pair with human language.
- Never use "Oops!" or humor in error states. The user is blocked; respect that.
- Place errors inline next to the field, not in a modal or toast that disappears.
- Use red (#DC2626 or equivalent) for error borders/icons, not for the entire message text.

---

## 3. Empty States

### Formula: Acknowledge + Explain Value + Action CTA + Optional Help

```
// Project list empty state

[illustration or icon]

No projects yet
Projects help you organize work, track progress, and collaborate with your team.

[Create your first project]

Need help getting started? Read the quick-start guide.
```

```
// Search with no results

No results for "exmple"
Did you mean "example"?

Try different keywords, remove filters, or [browse all items].
```

```
// Filtered view empty

No completed tasks this week
Completed tasks will appear here as your team finishes work.

[View all tasks]
```

### Rules

- Keep the acknowledgment to one short line. Don't over-explain emptiness.
- The value proposition should answer "why would I want things here?"
- The CTA button uses the same verb+object pattern as all buttons.
- Help links open in context (panel, tooltip, or new tab), never navigate away from the empty state.
- Never show a completely blank screen. Even loading-to-empty transitions need a state.

---

## 4. Voice vs Tone

**Voice** is the personality. It never changes. Define it once.

| Voice Attribute | Means | Does Not Mean |
|----------------|-------|---------------|
| Clear | Short sentences, common words | Dumbed down or robotic |
| Confident | Direct statements, no hedging | Arrogant or dismissive |
| Helpful | Guides next step, anticipates needs | Condescending or hand-holding |
| Human | Natural phrasing, contractions OK | Slang, jokes, or emoji in UI text |

**Tone** adapts to the moment.

| Moment | Tone | Example |
|--------|------|---------|
| Success | Warm, encouraging | "Your account is ready. Let's set up your first project." |
| Error | Calm, direct | "That file is too large. The maximum size is 25 MB." |
| Destructive confirmation | Serious, precise | "This will permanently delete 14 messages. This cannot be undone." |
| Onboarding | Friendly, guiding | "Welcome. We'll walk you through the basics in about 2 minutes." |
| Empty state | Neutral, inviting | "No notifications yet. You'll see updates from your team here." |

### Hard Rule

Never use humor in error states, destructive actions, or security messages. A user who just lost data does not want a witty quip.

---

## 5. Accessibility Writing

### Link Text

Links must make sense when read alone (screen readers navigate by link list).

```
// BAD
To learn more about pricing, click here.

// GOOD
View our pricing plans.

// BAD
Read more

// GOOD
Read the full accessibility guidelines
```

### Alt Text

Describe the information the image conveys, not the image itself.

```
// BAD
alt="photo"
alt="image of a chart"
alt=""  (unless purely decorative)

// GOOD
alt="Revenue grew 34% from Q1 to Q4 2025"
alt="Team photo: 12 people standing in front of the office"
alt=""  (decorative divider, background pattern)
```

Rule: If the image were deleted, what information would be lost? That is your alt text.

### Icon Buttons

Every icon-only button needs an `aria-label`.

```html
<!-- BAD -->
<button><TrashIcon /></button>

<!-- GOOD -->
<button aria-label="Delete message"><TrashIcon /></button>

<!-- With tooltip for sighted users too -->
<button aria-label="Delete message" title="Delete message">
  <TrashIcon />
</button>
```

### Form Labels

Every input has a visible `<label>`. Placeholder text is not a label.

```html
<!-- BAD -->
<input placeholder="Enter your email" />

<!-- GOOD -->
<label for="email">Email address</label>
<input id="email" placeholder="name@example.com" />
```

---

## 6. Translation Planning

English is compact. Other languages expand. Design with this in mind.

### Expansion Percentages

| Language | Expansion | 10-char English becomes |
|----------|-----------|------------------------|
| German | +30% | ~13 characters |
| French | +20% | ~12 characters |
| Finnish | +30-40% | ~13-14 characters |
| Italian | +15% | ~11-12 characters |
| Spanish | +15-20% | ~12 characters |
| Portuguese | +20-25% | ~12-13 characters |
| Chinese | -30% | ~7 characters |
| Japanese | -20-30% | ~7-8 characters |
| Korean | -10-20% | ~8-9 characters |
| Arabic | +25% (RTL) | ~12-13 characters |

### Design Rules

- Buttons: Allow at least 30% extra width. Never set fixed-width buttons for text.
- Navigation: Horizontal nav bars that barely fit in English will break in German. Test with pseudolocalization.
- Truncation: If you must truncate, truncate with `...` and provide the full text on hover/focus via `title` attribute.
- Icons + text: Always pair icons with text labels for translatability. Icon-only works only for universally understood symbols (close X, hamburger menu).
- Strings: Never concatenate strings. Use full-sentence templates with placeholders: `"Showing {count} of {total} results"` not `"Showing " + count + " of " + total + " results"`.
- Pluralization: Use ICU MessageFormat or equivalent. Never assume `count === 1` is the only singular rule (Arabic has 6 plural forms).

---

## 7. Terminology Consistency

Pick one term. Use it everywhere. Document it here.

| Use This | Not This |
|----------|----------|
| Delete | Remove, Trash, Erase, Destroy |
| Settings | Preferences, Options, Configuration |
| Sign in | Log in, Login, Sign on |
| Sign out | Log out, Logout, Sign off |
| Sign up | Register, Create account, Join |
| Search | Find, Look up, Query |
| Edit | Modify, Change, Update (in UI labels) |
| Save | Apply (for saving data, not filter application) |
| Profile | Account (for user identity page) |
| Workspace | Organization, Team, Company |
| Member | User (in team context) |
| Notification | Alert (reserve "alert" for system-level) |

### Enforcement

- Create a glossary file in the project. Lint against it.
- When a new term is introduced, add it to the glossary before shipping.
- Search the entire codebase when renaming. Partial renames are worse than inconsistency.

---

## 8. Loading State Copy

Never show "Loading..." for more than 2 seconds without context.

### Progressive Messages

```
// Immediate (0-2s)
[spinner]

// Short wait (2-5s)
Loading your dashboard...

// Medium wait (5-15s)
Crunching the numbers. This usually takes a few seconds.

// Long wait (15s+)
Still working on it. Large datasets take a bit longer.

// Very long (30s+)
This is taking longer than usual. You can wait or [try again].
```

### Skeleton Screens Over Spinners

Use skeleton screens (gray placeholder shapes) for known layouts. Use spinners only for unknown or variable layouts.

```
// Known layout: use skeleton
[====== skeleton heading ======]
[== skeleton line 1 ===========]
[== skeleton line 2 =======]
[== skeleton line 3 ==============]

// Unknown layout: use spinner with context
[spinner] Searching 12,000 records...
```

### Progress Indicators

For operations with known progress, show a percentage or step count.

```
Uploading 3 of 7 files (42%)
[=========>                    ]

Importing contacts... Step 2 of 4: Validating email addresses
```

---

## 9. Confirmation Dialogs

### Structure

```
Title: State what will happen (verb + object)
Body: Consequences in plain language. Irreversibility if applicable.
Actions: [Safe option]  [Destructive option]
```

### Non-Destructive Confirmation

```
Title: Publish this article?
Body: It will be visible to everyone in your workspace immediately.
Actions: [Go back]  [Publish article]
```

### Destructive Confirmation

```
Title: Delete "Q4 Report" and 3 attachments?
Body: This will permanently delete the document and its attachments.
      This cannot be undone.
Actions: [Keep document]  [Delete document and attachments]
```

### High-Stakes Destructive (Type-to-Confirm)

```
Title: Delete workspace "Acme Corp"?
Body: This will permanently delete the workspace, all 47 projects,
      and all member data. This cannot be undone.

      Type "Acme Corp" to confirm:
      [                           ]

Actions: [Cancel]  [Delete workspace] (disabled until typed)
```

### Rules

- The safe action (cancel/keep/go back) is the visually prominent button (filled, primary color).
- The destructive action is secondary (outlined, red text or red outline).
- Never pre-select the destructive option.
- For keyboard users, focus lands on the safe action by default.
- Escape key always triggers the safe action.

---

## 10. Microcopy

### Placeholder vs Label

Placeholders vanish on input. Labels stay visible. Use both.

```html
<!-- BAD: placeholder as only label -->
<input placeholder="Email" />

<!-- GOOD: visible label + helpful placeholder -->
<label for="email">Email address</label>
<input id="email" placeholder="name@example.com" />
```

### Helper Text

Place below the input. Use for format hints, constraints, or context.

```
Password
[                    ]
Must be at least 8 characters with one number and one symbol.

Phone number
[                    ]
We'll only use this for two-factor authentication.
```

### Success Messages with Next Steps

Never dead-end a user after success. Always tell them what comes next.

```
// BAD
Success!

// GOOD
Account created. Check your email for a verification link.

// BAD
Payment received.

// GOOD
Payment received. Your order #4821 will ship within 2 business days.
You'll get a tracking email when it does. [View order details]

// BAD
File uploaded.

// GOOD
"Q4-Report.pdf" uploaded. [Share with team]  [Upload another]
```

### Character Counts

Show remaining characters, not total limit, and only when the user is close to the limit.

```
// Show nothing until 80% of limit reached
// At 80%+:
23 characters remaining

// At limit:
0 characters remaining (input blocked or visual warning)

// Over limit (if allowed):
12 characters over limit (red, with explanation of what happens)
```

### Toggle Labels

Label the current state, not the action. Or label both sides.

```
// BAD (ambiguous: is it on or will clicking turn it on?)
[toggle] Notifications

// GOOD: label both states
Notifications: Off [toggle] On

// GOOD: describe what toggle does
[toggle] Receive email notifications
         Currently: Off
```
