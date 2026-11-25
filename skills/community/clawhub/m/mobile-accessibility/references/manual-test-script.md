# Manual screen reader and settings test script

Load this for step 6 of the workflow. Automated checks cannot tell whether a label makes sense, whether focus
lands in the right place after an action, or whether a journey can be finished at all. This script can.
Run it per critical journey, on a real device where possible, once per platform.

## Setup

- Record: device model, OS version, screen reader version, app build, date, tester.
- Use a test account with realistic data (long names, long addresses, many items) and a payment sandbox.
- Learn the gestures before testing; a tester fighting the screen reader produces false findings.
- Android: TalkBack on; in TalkBack's developer settings set "Log output level" to VERBOSE if debugging.
- iOS: VoiceOver on via the Accessibility Shortcut (triple-click the side button) so it can be toggled fast.
- Turn on the screen reader's caption or speech output panel if available, so the spoken text can be copied
  into findings as evidence.

## Pass 1: screen reader, linear navigation

For each screen in the journey:

1. Open the screen. Expected: focus starts at the top (title or first element), or at the most relevant
   element after navigation. The screen title is announced (2.4.2).
2. Swipe right through every element to the end, then left back to the start.
   - Every element is reachable; nothing visible is skipped (1.3.1, 2.1.1).
   - Each element is announced once, in visual reading order (1.3.2, 2.4.3).
   - Each announcement has a name, role and state that match what is on screen: "Wi-Fi, switch, on"
     (4.1.2). No "button", "unlabeled", file names, or icon names like "ic_delete_24".
   - Decorative images are skipped (1.1.1). Related text (title, price, rating) is one stop, not five.
   - Headings are announced as headings (1.3.1).
3. Use heading navigation (TalkBack reading controls set to Headings; VoiceOver rotor set to Headings).
   Expected: the screen's sections can be reached by heading.
4. Activate each control with a double tap. Expected: it does what its label says.
5. Open the actions menu on rows that have swipe, long-press or drag behaviour (TalkBack "Actions",
   VoiceOver rotor "Actions"). Expected: each gesture-only action is available (2.5.1, 2.5.7).

## Pass 2: screen reader, task completion

Complete the journey from start to finish using only the screen reader, for example:

| Step | Check | SC |
|---|---|---|
| Sign in | Fields announce label and type ("Email, edit box"); password manager or autofill offers credentials; paste works | 3.3.2, 1.3.5, 3.3.8 |
| Enter invalid data | Error is announced when it appears, or focus moves to it; the text says how to fix it | 3.3.1, 3.3.3, 4.1.3 |
| Open a dialog or bottom sheet | Focus moves into it; content behind it is not reachable; closing returns focus to the trigger | 2.4.3, 2.1.2 |
| Loading and results | "Loading" and the result ("3 results", "Saved") are announced without moving focus | 4.1.3 |
| Payment or contract | Summary is readable before confirming; there is a review, confirm or undo step | 3.3.4 |
| One-time code | Code field supports autofill or paste; timeout can be extended or is long enough | 3.3.8, 2.2.1 |
| Web view (terms, help, 3-D Secure) | Content is readable and operable with the screen reader; focus does not get stuck | 2.1.2, 4.1.2 |
| Back navigation | Back gesture or button works (TalkBack back; VoiceOver two-finger scrub) | 2.1.1 |

A journey that cannot be finished is a Blocker. Record the exact step and the spoken text.

## Pass 3: text size and display settings

1. Set the largest text size: Android Settings > Display > Font size at maximum (Android 14 and later go to
   200 percent) plus Display size at maximum; iOS Settings > Accessibility > Display and Text Size > Larger
   Text with the largest accessibility size.
2. Walk the journey again. Expected: no truncated or overlapping text, no text cut off inside buttons, all
   content and controls still reachable by scrolling, no horizontal scrolling for reading text (1.4.4, 1.4.10).
3. Turn on Bold Text (iOS) or Bold text / High contrast text (Android, where available). Expected: the app
   follows the setting (EN 301 549 11.7).
4. Turn on Increase Contrast (iOS) or a high-contrast option (Android). Check text and icons against
   backgrounds with a contrast checker on screenshots: 4.5:1 text, 3:1 large text and icons (1.4.3, 1.4.11).
5. Turn on colour filters or grayscale. Expected: errors, states and charts are still understandable (1.4.1).
6. Rotate the device. Expected: the journey works in landscape unless orientation is essential (1.3.4).

## Pass 4: motion

1. iOS: Settings > Accessibility > Motion > Reduce Motion on. Android: Settings > Accessibility > Remove
   animations on (wording varies by device).
2. Expected: parallax, zoom and large transitions are removed or replaced by fades; auto-playing carousels and
   animations longer than five seconds can be paused (2.2.2); nothing flashes more than three times per
   second (2.3.1).

## Pass 5: switch, keyboard and voice

1. Connect a Bluetooth keyboard. Android: Tab and arrow keys; iOS: Settings > Accessibility > Keyboards >
   Full Keyboard Access. Expected: every control can be reached and activated, focus is visible, focus is
   not trapped, and the focused control is not hidden behind the soft keyboard or a sticky bar
   (2.1.1, 2.1.2, 2.4.7, 2.4.11).
2. Android Switch Access or iOS Switch Control: each actionable item is highlighted once; gesture actions are
   available as menu items.
3. iOS Voice Control ("Show names") or Android Voice Access: saying the visible label activates the control
   (2.5.3).

## Recording findings

For each failure write down, at the moment it happens:

- Journey and step, screen name, platform and assistive technology.
- What was expected and what happened, with the spoken text in quotes:
  `TalkBack: "Button" on the pay icon; expected "Pay 24.90 euros, button"`.
- A screenshot or screen recording with the screen reader caption visible.
- The WCAG 2.2 success criterion (number and name) and a first severity guess.

Then map each one to the report table in the skill's output format.
