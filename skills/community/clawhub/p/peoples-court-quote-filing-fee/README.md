# ClawHub skill: peoples-court-quote-filing-fee

This skill quotes the People's Court filing fee for a claim amount. It uses the live `quote_filing_fee` MCP tool at `https://mcp.peoplescourt.ai/mcp` and falls back to the published schedule.

## Publish

Run these from `/workspace/aeo-audit/`:

1. `npm i -g clawhub`
2. `clawhub login` (signs in with GitHub)
3. Preview the publish:
   `clawhub skill publish ./peoples-court-quote-filing-fee --slug peoples-court-quote-filing-fee --name "People's Court: Quote Filing Fee" --dry-run`
4. Publish:
   `clawhub skill publish ./peoples-court-quote-filing-fee --slug peoples-court-quote-filing-fee --name "People's Court: Quote Filing Fee" --changelog "Initial release"`

Add `--owner <org>` to publish under an org instead of your personal handle. New skills start at 1.0.0. The release stays pending until ClawHub's security checks pass.

Note: the portable Agent Skills spec prefers `name` to match the folder name. If validation complains, rename the folder to `peoples-court-quote-filing-fee` before you publish.

Expected live URL: `clawhub.ai/<user>/skills/peoples-court-quote-filing-fee`

## After it goes live

- Open the listing and confirm that the Website/homepage link points to https://peoplescourt.ai.
- Force-index the listing URL in Google Search Console with URL Inspection, then Request indexing.
