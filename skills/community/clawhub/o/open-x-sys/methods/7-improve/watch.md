# Watch

> `watch(x, signal)` · Stage 7 · Improve
> **Prompt**: "Keep an eye on ___ and tell me when ___."
> **Also heard as**: "Let me know if this changes." · "What should I be tracking?" · "How will I know it is going wrong?"
> **Produces**: signals and thresholds recorded in the system, checked whenever it comes back.

## What it is for

An understanding is true as of a date, and a decision rests on conditions that can change. Watch records the few signals that would show a change that matters: the early sign that one future is arriving, that a practice has stopped working, that an assumption no longer holds. It lets the system notice, on the person's behalf, the moment at which something should be looked at again.

## What it produces

For each watch, recorded in the person's system:

- **The signal**: something specific that can be observed.
- **The threshold**: the value or event at which it counts.
- **What it would mean**: which understanding, decision or practice it bears on.
- **What to do then**: the response, decided in advance.
- **Where to look, and how often it is worth looking.**

## What a good use looks like

- Each signal is observable by a definite act: reading a figure in a named source, opening a file, rerunning a script. "Market sentiment" is not a signal.
- It has a threshold. Without one, every movement is noise or alarm depending on mood.
- It is tied to something that would change: "if hours per episode rise above six for two weeks, the editing practice needs review".
- It prefers leading signals, which move before the outcome, to lagging ones, which confirm it afterwards.
- The response is decided now, while calm, and recorded with the signal.
- There are few. Three watches that matter are checked; thirty are ignored.
- It comes from the earlier stages: the early signals of **What-if** futures, the failure signs from **Invert**, the switching conditions of a practice, the "as of" date of an understanding.
- **It is honest about how watching works.** OpenXSys has no background process. A watch is checked when the system comes back in a new session, by actually looking, and the person is told which watches were checked and which could not be. If the person wants a signal checked without a session, that means code running on a schedule, which they must approve.
- Stale watches are retired.

## Where it goes wrong

- **Watching everything.**
- **No threshold, no meaning, no response.**
- **A promise of alerts** the system cannot deliver.
- **Lagging signals only**, which report the damage.
- **Watches that outlive their reason.**
- **Reporting "nothing changed"** without having looked.

## It works with

Watch closes routes that end in a decision or a build, and is the last step of Shell's scenarios and the first of **Boyd's loop**. It receives signals from **What-if**, **Invert**, **Best Practice** and **Review**. When a watched signal is found to have fired, the system says so on return with the **Watch** signal (see `system/return.md`), and the usual next method is **Review** or **What-if**.

## Teach-back

"This was Watch: choose the two or three things that would tell you early that something important has changed. For each, decide the level that counts and what you will do when it is reached. Write it down now, so that later you only have to look."

## The thinking behind it

- **John Boyd**, in briefings from the 1970s to the 1990s, described the loop of observing, orienting, deciding and acting, in which observation continually feeds an updated picture of the situation.
- **Pierre Wack**, *Harvard Business Review* (1985): scenarios come with early signals, events that indicate which future is unfolding.

OpenXSys simplifies: Boyd's loop concerns tempo in conflict and Wack's signals belong to scenario planning; Watch takes from both the practice of deciding in advance what to look for and what it will mean.
