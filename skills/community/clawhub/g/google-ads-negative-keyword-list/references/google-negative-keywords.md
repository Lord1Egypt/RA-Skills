# Negative keyword rules and account limits in Google Ads

Reference for the Google Ads Negative Keyword List skill. Every limit and rule below is a US-facing constraint the workflow has to respect.

## Limits that shape the list

- 5,000 keywords per negative keyword list, 20 lists per account.
- 10,000 negative keywords per campaign, 1,000 account-level negative keywords.
- Display and Video campaigns consider at most 1,000 negatives, and all of them act as broad match there.
- Performance Max campaign-level negatives went from a 100 cap to 10,000 in March 2025.

## Exact versus phrase

- Negative exact blocks one query, so it is the safer choice for a single irrelevant term.
- Negative phrase blocks every query containing the words, so it can kill revenue when the words are ambiguous.
- Write the phrase in the order a searcher would type it, without quotes and without match type punctuation.

## Where the term goes

- Account level applies the term to all search and shopping inventory in the account.
- Campaign level keeps it inside one product line; ad group level stays inside one intent cluster.
- Shared lists let a term serve several campaigns at once without duplicating the row.
