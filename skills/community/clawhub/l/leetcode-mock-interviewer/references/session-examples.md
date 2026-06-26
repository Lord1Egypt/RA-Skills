# Session Examples

Concrete examples of how each interview mode should flow, including exact interviewer lines.

## Example 1: Full Mock — Sliding Window Medium

**User request:** "Mock interview me on a medium sliding window problem."

### Phase 1: Setup

> Interviewer: "Great, let's do a full mock. Quick setup:
> 1. Target role? (SWE / MLE / AI Engineer)
> 2. Difficulty: medium — confirmed?
> 3. Topic: sliding window — confirmed?
> 4. Do you want hints enabled, or no hints?"

User: "SWE, medium, sliding window, yes to hints."

### Phase 2: Present Problem

> Interviewer: "Here's the problem. Given a string, find the length of the longest substring without repeating characters.
>
> Example 1: Input: 'abcabcbb' → Output: 3 (the substring is 'abc')
> Example 2: Input: 'bbbbb' → Output: 1
> Example 3: Input: 'pwwkew' → Output: 3 (the substring is 'wke')
>
> Constraints: 0 <= s.length <= 50,000. The string consists of English letters, digits, symbols, and spaces.
>
> Take a moment, then walk me through your initial thoughts."

### Phase 3: Interview Loop

**Step A — Clarification + Brute Force:**
> Interviewer: "Before we optimize, what would a brute-force approach look like?"

User: "Check every possible substring and see if it has duplicates."

> Interviewer: "Good. How would you check for duplicates in each substring?"

**Step B — Complexity + Optimization:**
> Interviewer: "What's the time complexity of that brute-force?"

User: "O(n^3) — two loops for substrings, one to check uniqueness."

> Interviewer: "Right. Can we do better? What's the bottleneck — what work are we repeating?"

User: "We're re-scanning characters we've already seen. We could use a sliding window with a set."

> Interviewer: "Walk me through how the window would move."

**Step C — Code:**
> Interviewer: "Sounds solid. Go ahead and implement it."

**Step D — Follow-ups:**
> Interviewer: "Walk me through example 3 step by step with your code."

> Interviewer: "What happens if the input is an empty string?"

> Interviewer: "Could you do this without a hash set? What are the tradeoffs?"

### Phase 4: Feedback

Output the structured feedback template with specific observations from the session.

---

## Example 2: Follow-Up Only

**User request:** "I solved Product of Array Except Self (#238). Interview me on my solution."

**Flow:**
> Interviewer: "Walk me through your approach. How does it work?"

User explains prefix/suffix product arrays.

> Interviewer: "Why don't you use division?"

> Interviewer: "What's the time and space complexity?"

> Interviewer: "Does the output array count as extra space? Why or why not?"

> Interviewer: "What happens if the array contains one or more zeros?"

> Interviewer: "Could you reduce this from O(n) extra space to O(1)?"

End with concise feedback — no need for full setup or problem presentation.

---

## Example 3: Rapid-Fire Warmup

**User request:** "Give me a quick warmup — arrays and hashing, 3 problems."

**Flow:**

> Interviewer: "Let's do 3 quick rounds. Verbal only — explain your approach and complexity, no need to write code.
>
> **Round 1:** Given an array of integers and a target, find two numbers that add up to the target. What's your approach?"

User explains hash map solution.

> Interviewer: "Complexity?"

User: "O(n) time, O(n) space."

> Interviewer: "Good. **Round 2:** Given an integer array, return true if any value appears at least twice. How would you solve it?"

User explains set approach.

> Interviewer: "What if we're not allowed extra space?"

User: "Sort first, then check adjacent elements. O(n log n) time, O(1) space."

> Interviewer: "Nice tradeoff. **Round 3:** Given two strings, determine if they are anagrams. Go."

End with brief feedback on verbal clarity across all 3 rounds.

---

## Example 4: Handling a Freeze

When the candidate stalls for 2+ exchanges:

**Hint level 1 — guiding question:**
> "What information would help you avoid recomputing work?"

**Hint level 2 — directional nudge:**
> "Could a hash map help you remember something as you scan?"

**Hint level 3 — tactical hint (only if hints enabled):**
> "Try tracking character counts. What condition tells you the window is invalid?"

Never jump straight to the answer. Always give the candidate a chance to restart their thinking.

---

## Example 5: Candidate Jumps to Code

If the candidate pastes code without explaining:

> Interviewer: "Hold on — before we look at code, can you walk me through your plan? What's the brute-force idea, and what are you optimizing away?"

If the candidate skips brute force and goes straight to optimal:

> Interviewer: "That's a good direction, but let's back up. What's the most straightforward approach, even if it's slow? I want to understand the baseline first."

These redirects keep the session interview-like instead of turning into silent coding practice.

---

## Example 6: MLE/AI Engineer Variant

**User request:** "Interview me for an MLE role, medium difficulty, random topic."

**Differences from SWE:**
- Can include problems like sparse matrix multiplication, LRU/LFU cache design, or hit counter design
- Follow-ups may include: "How would this scale to a distributed system?" or "What if the data doesn't fit in memory?"
- Complexity analysis should consider amortized costs and practical performance
- May ask about space-time tradeoffs in the context of model serving or data pipelines
