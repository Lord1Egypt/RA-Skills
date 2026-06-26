# Hitem3D Live Validation Plan

## Goal

Turn the skill from a design-complete implementation into a real-world validated production skill.

## Required live checks

1. Auth works with real AK/SK
2. Balance endpoint returns the expected structure
3. Single-image default pipeline works end to end
4. Portrait pipeline works end to end
5. Multi-view pipeline works end to end
6. Batch pipeline works on at least 3 images
7. Downloaded filenames and extensions match actual output
8. Query response fields match script assumptions
9. One failure case is observed and messaged correctly

## What to verify in each run

- HTTP response shape
- success/failure code conventions
- task_id location
- query state values
- final download URL field
- whether format is echoed back by query-task
- whether cover_url is returned consistently
- whether multi_images_bit + repeated multi_images works exactly as expected

## Current blocker

No recoverable AK/SK were found from shell env, launchctl env, common config files, or obvious plaintext config locations.
There is browser session evidence that Hitem3D was used before, but browser cookies alone are not a safe or sufficient substitute for Open API credentials.

## Realistic next step

As soon as valid AK/SK are available in environment, run:
- auth
- balance
- single-image run
- portrait run
- multi-view run
- batch run

Then patch response parsing and error handling based on actual results.
