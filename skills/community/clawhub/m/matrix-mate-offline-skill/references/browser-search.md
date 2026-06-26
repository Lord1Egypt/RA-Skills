# Browser-Assisted ITA Matrix Search

Use browser automation only for the search and link-capture step.

## V1 flow

1. Confirm the user's route intent, dates, cabin, and passenger mix.
2. Open ITA Matrix in the agent browser.
3. Fill the search form and submit it.
4. Wait for an itinerary or result page that exposes a usable itinerary/share link.
5. Capture that link.
6. Call `parse_matrix_link` with the captured URL.
7. If Matrix Mate cannot verify the result, ask the user for manual JSON plus fare rules text.

## Important limits

- No login handling
- No payment or checkout actions
- No CAPTCHA bypassing
- No unsupported scraping promises beyond normal page interaction needed to capture the itinerary URL

## Preferred outcome

The best outcome is a Matrix itinerary URL that already contains the `search=` payload and still yields verifiable booking details plus fare rules when Matrix Mate parses it.
