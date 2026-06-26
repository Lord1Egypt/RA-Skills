# Platform validation

A 200 HTTP status is not enough.
Validate per platform when possible.

## Strong signals
- final URL still matches the expected profile path
- page title contains the handle or profile marker
- page content clearly indicates a profile exists

## Weak / ambiguous signals
- generic landing page
- consent wall
- login wall with no profile evidence
- redirect to homepage or search page
- page title that is too generic

## Platform notes
- GitHub: strong if final URL matches `/username` and page is not a 404/profile-missing page
- Reddit: strong if final URL matches `/user/username/` and page indicates a user profile
- TikTok: weak if only generic TikTok shell is visible; prefer exact final handle path plus profile cues
- X/Twitter: weak if logged-out shell gives no profile-specific evidence
- Instagram: weak if only generic shell/login page is visible
- YouTube: weak if redirected to consent or generic channel shell without profile-specific evidence
- Hacker News: strong if title or page indicates `Profile: username`
- Keybase/GitLab: often easier to validate from title and final URL

## Rule
If validation is weak, classify as `weak` or `not_verifiable`, not `exact`.
