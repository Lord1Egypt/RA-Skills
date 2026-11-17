# Recipes

Every recipe assumes the setup from `SKILL.md`:

```sh
export JOBBER_HUB='https://clienthub.getjobber.com/client_hubs/<hub-uuid>'
PARSE=references/parse-clienthub.mjs        # adjust to where the skill lives
hub() { fpx get -p jobber "$JOBBER_HUB/$1" | node "$PARSE" "$1"; }
```

`hub` takes the page name, which is also the parser kind — they are the same
word on purpose, so the two can never drift apart.

## Appointments

Record shape:

```jsonc
{
  "group": "Today" | "Upcoming" | "Past",
  "id": "2236612358",
  "date": "Jun 28, 2026",
  "weekday": "Sunday",
  "time": "9:00am",        // null when the vendor hides times (canViewTime:false)
  "arrivalWindow": null,   // e.g. "8:00am - 10:00am" when the vendor sets one
  "duration": null,
  "location": "123 Elm St, ...",
  "confirmed": true,
  "url": "appointments/2236612358"  // hub-relative: the hub id never appears
}
```

Everything upcoming:

```sh
hub appointments | jq '[.[] | select(.group != "Past")]'
```

The next visit, as one line:

```sh
hub appointments \
  | jq -r 'map(select(.group != "Past")) | first
           | if . == null then "no upcoming visits"
             else "\(.weekday) \(.date)\(if .time then " at \(.time)" else "" end) — \(.location)"
             end'
```

Visit history, most recent first (the hub already returns `Past` newest-first):

```sh
hub appointments | jq -r '.[] | select(.group=="Past") | "\(.date)\t\(.location)"'
```

Absolute URL for one visit:

```sh
hub appointments | jq -r --arg base "$JOBBER_HUB/" 'first | $base + .url'
```

## Invoices

Record shape:

```jsonc
{
  "section": "Paid",                 // the list heading this card sat under
  "id": "150208512",
  "title": "For Services Rendered",
  "number": "#15313",
  "details": ["Sent Mar 23, 2026 | Due Apr 07, 2026", "$135.00 & paid in full"],
  "url": "invoices/150208512"       // hub-relative, like appointments
}
```

`details` is an ordered list of the card's metadata rows, kept raw rather than
parsed into fields. The rows the vendor shows vary by invoice state — an unpaid
invoice carries a balance row a paid one does not — so a fixed schema would
invent fields for some invoices and drop rows for others.

Everything not yet paid:

```sh
hub invoices | jq '[.[] | select(.section != "Paid")]'
```

One line per invoice:

```sh
hub invoices | jq -r '.[] | "\(.number)\t\(.section)\t\(.details[0] // "")"'
```

Pull the amounts out of the detail rows:

```sh
hub invoices | jq -r '.[] | . as $i
  | ($i.details[] | select(test("\\$")) ) // "no amount"
  | "\($i.number)\t\(.)"'
```

Sum what is outstanding — note this parses money out of display strings, so
sanity-check it before trusting it for anything that matters:

```sh
hub invoices \
  | jq '[.[] | select(.section != "Paid") | .details[] | select(test("\\$"))
         | capture("\\$(?<amt>[0-9,]+(\\.[0-9]{2})?)").amt | gsub(",";"") | tonumber]
        | add // 0'
```

## Quotes and work requests

Same card shape as invoices — `section`, `title`, `number`, `details`, `url`:

```sh
hub quotes         | jq -r '.[] | "\(.number)\t\(.section)\t\(.title)"'
hub work_requests  | jq -r '.[] | "\(.section)\t\(.title)"'
```

Quotes awaiting your response:

```sh
hub quotes | jq '[.[] | select(.section | test("await|pending|review"; "i"))]'
```

## A single record

Detail pages are HTML too, and their layout differs from the list cards. The
parser targets lists; for one record, take the URL from the list and open it:

```sh
hub invoices | jq -r --arg base "$JOBBER_HUB/" \
  '.[] | select(.number=="#15313") | $base + .url'
```

To read a detail page's raw HTML yourself:

```sh
fpx get -p jobber "$JOBBER_HUB/invoices/150208512" > invoice.html
```

## Several vendors

One hub per business; there is no combined view. Loop over the hubs you hold:

```sh
for hub_url in "$QUEENBEE_HUB" "$GREENWORX_HUB"; do
  JOBBER_HUB="$hub_url"
  echo "== $(fpx get -p jobber "$JOBBER_HUB/appointments" \
          | grep -oiE '<title>[^<]*' | head -1 | cut -c8-)"
  hub appointments | jq -r '.[] | select(.group!="Past") | "  \(.date) \(.location)"'
done
```

## Health check

```sh
fpx health -p jobber   # is the bridge up at all?
fpx get -p jobber "$JOBBER_HUB/appointments" | head -c 200
```

A `<title>Just a moment` in that output means the request did not go through the
tab — the parser exits `3` on it rather than returning an empty list.
