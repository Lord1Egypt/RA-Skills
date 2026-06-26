# Troubleshooting — PowerPoint

## `PowerPoint not running` or no active object

Cause:
- PowerPoint is closed
- no live instance exists to attach to

Fix:
- launch PowerPoint intentionally or attach only after confirming an open deck exists

## Slide action hit the wrong slide

Cause:
- wrong active slide
- selection changed
- slide identity was not re-verified before write

Fix:
- re-read active presentation and slide index
- prefer explicit slide references when possible

## Slideshow commands do nothing

Cause:
- command ran in edit view
- slideshow window is not active
- deck is not in the expected state

Fix:
- confirm current view and slideshow state first
- rerun only after PowerPoint reports the expected deck and slide

## PDF export looks stale

Cause:
- notes, numbering, or active content was not in the expected final state

Fix:
- verify the active deck and slide order first
- export only after the app reflects the final presentation state

## macOS script errors against PowerPoint

Cause:
- wrong terminology for the PowerPoint dictionary
- app not fully ready

Fix:
- keep scripts short
- validate presentation identity first
- retry only after confirming PowerPoint is frontmost and has an open deck

## `osascript` can see PowerPoint but actions still fail

Cause:
- modal dialog open
- wrong deck is frontmost
- PowerPoint dictionary term does not match the intended object

Fix:
- re-read active presentation identity
- close or acknowledge the modal dialog
- reduce the script to the smallest reproducible action
