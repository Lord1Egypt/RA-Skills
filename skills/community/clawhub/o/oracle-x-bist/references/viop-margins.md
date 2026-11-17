# Reading Takasbank's price scan range

The scan range is the one number in a VİOP margin picture that nobody has to
model. Every other input a positioning map needs — how leverage is distributed,
what price a cohort entered at — has to be invented somewhere. Here the
clearing house publishes a figure that binds everyone, per underlying, every
day.

This file is how to get it. It assumes no Oracle-X instance; it is a procedure
against a public host.

## What the number is

The **price scan range** (PSR) is the one-day, 99% confidence price move
Takasbank collateralises against under the BISTECH margin method, expressed as
a percentage of contract value. A position that moves by the PSR has exhausted
the scan risk its **initial** margin was sized for.

### What it is not

It is not a margin-call trigger, and no public source lets you compute one.

The CCP procedure leaves the maintenance level to a General Letter, and states
that maintenance margin is not applied at end of day. The "75% of initial"
figure that circulates in forums and blog posts traces back to a single undated
guide and to nothing authoritative. Presenting a scan range as a call level —
or deriving one with the 75% figure — states as fact something the clearing
house has deliberately not published.

If a chart draws the band, the caption has to say what the band is. "The move
your initial margin was sized for" is true. "Where you get called" is not.

## Where the file is

| Host | Verdict |
|---|---|
| `www.takasbank.com.tr` | Behind bot protection. Will not answer a script, which makes the parameters look unavailable. They are not. |
| `wwwdata.takasbank.com.tr` | A separate host. Open directory listing, no protection. **This is the one.** |
| `wwwdata.takasbank.com.tr/viop/SPAN/` | **Never.** A legacy archive frozen in March 2017 that still serves `200`s — current-looking numbers that are years stale. |

The day's directory:

```
https://wwwdata.takasbank.com.tr/pardosya/Prod/YYMMDD/
```

and inside it the end-of-day SPAN archive:

```
TAKASEOD_…-YYMMDD-001.zip
```

**Run `-001` is end of day.** The intraday runs revise the parameter nine to
sixteen times a session, so no intraday file is a snapshot anything can be
pinned to. Walk back up to about six days when a file is missing — that covers
a long weekend plus a public holiday — and use the file's own `pointInTime`
date rather than the day you fetched it.

## The two filters

The archive holds far more than one portfolio per underlying. It carries a
portfolio per broker under the same element name, and a rights-issue portfolio
beside each main contract. Both are the wrong row and both parse cleanly.

```
setlMeth == "DELIV"          # physically settled single-stock futures,
                             # not the cash-settled broker collateral portfolios
not pfCode.endswith("_C")    # drop the rights-issue portfolio, which shadows
                             # the main contract at a different scan rate
```

Skip either one and **THYAO reads 14.0 where its scan range is 13.4**. Nothing
raises. The number is plausible, wrong, and arrived at silently — which is why
both filters are stated here rather than left to be rediscovered.

## The fields worth reading

Per `futPf` element:

| Path | Meaning |
|---|---|
| `pfCode` | The underlying. Uppercase it; reject anything ending `_C`. |
| `setlMeth` | Must equal `DELIV`. |
| `scanRate/priceScanPct` | The scan range, as a percentage. Divide by 100 for a fraction — `13.4` → `0.134`. |
| `fut/val` | Contract value. |
| `fut/cvf` | Shares per contract, straight from the clearing house — an independent check on any multiplier derived from the bulletin. |

And once per document: `created`, and `pointInTime/date` with `pointInTime/run`.
Report `pointInTime/date`, never the fetch time; a stale file that says so is
usable, one that pretends to be today's is not.

## Parsing it without spending 70 MB

The archive is about two megabytes and expands to roughly seventy, of which
about fifty rows are wanted. Stream it and clear as you go:

```python
import zipfile, xml.etree.ElementTree as ET
from io import BytesIO

archive = zipfile.ZipFile(BytesIO(payload))
name = next(n for n in archive.namelist() if n.lower().endswith(".xml"))

rates: dict[str, float] = {}
with archive.open(name) as handle:
    for _, element in ET.iterparse(handle, events=("end",)):
        if element.tag.split("}")[-1] != "futPf":
            continue
        code = (element.findtext("pfCode") or "").strip().upper()
        settlement = (element.findtext("setlMeth") or "").strip()
        scan = element.findtext(".//scanRate/priceScanPct")
        element.clear()                      # the whole point of iterparse

        if not code or code.endswith("_C") or settlement != "DELIV" or not scan:
            continue
        rate = float(scan) / 100.0
        if rate > 0:
            rates[code] = rate
```

Holding the tree instead costs two orders of magnitude more memory than the
answer. Streamed, this is about a second.

Bound the download and the listing read — a couple of megabytes for the
listing, roughly twelve for the archive. An unbounded read against a directory
index is how a scraper becomes a memory incident.

## Doing it through an instance instead

If Oracle-X is running, `GET /api/bist/viop-map/{ticker}` has already done all
of the above, cached it, and drawn the cohorts against it. Ask
`GET /api/bist/viop-map/underlyings` which tickers are covered before assuming
one is: the map is built only where the data supports it, and coverage is
narrower than the exchange's full list.
