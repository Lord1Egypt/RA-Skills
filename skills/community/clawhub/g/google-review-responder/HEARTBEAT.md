# Heartbeat: Review Responder

## On Every Heartbeat

1. Check for new unanswered Google Business reviews for each active client.
   Run for each client configured in `~/review-responder/clients/`:
   ```
   python3 ~/review-responder/gbp_reviews.py check --client <client_id>
   ```

2. If the script finds new reviews, read the output carefully. For each new review:
   - Draft a response following the guidelines in the Review Responder skill (SKILL.md)
   - Send the draft to the operator via Telegram for approval
   - Use the message format specified in SKILL.md

3. If no new reviews are found for any client, reply HEARTBEAT_OK.

## Important
- Do NOT auto-post replies. Every response requires operator approval via Telegram.
- If the script errors (missing config, API failure), report the error via Telegram so the operator can investigate.
- Check `python3 ~/review-responder/gbp_reviews.py pending` to see if there are stale pending reviews that haven't been addressed. If any are older than 48 hours, send a reminder.
