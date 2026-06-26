# Pill Reminder — Configuration

Edit this file to manage your pills. Follow the format exactly.

---

## Profiles

### Profile: [YOUR NAME]

**channel:** groupme  
**reminder-window:** 30min

**Pills:**

- pill: [PILL NAME]
  count: [NUMBER]
  refill-threshold: [NUMBER]  # alerts when count drops to this
  times:
    - "8:00 AM"
    - "8:00 PM"  # add more doses as needed
  last-logged: [AUTO]  # DO NOT EDIT
  refill-log: [AUTO]    # DO NOT EDIT

---

## Example (copy this pattern for each pill):

### Profile: Brian

**channel:** groupme  
**reminder-window:** 30min

**Pills:**

- pill: Vitamin D
  count: 60
  refill-threshold: 7
  times:
    - "8:00 AM"
  last-logged: 0
  refill-log: 0

- pill: Lisinopril
  count: 30
  refill-threshold: 5
  times:
    - "9:00 AM"
  last-logged: 0
  refill-log: 0

---

### Profile: [CHILD NAME]

**channel:** groupme  
**reminder-window:** 30min

**Pills:**

- pill:
  count:
  refill-threshold:
  times:
    -
  last-logged: 0
  refill-log: 0