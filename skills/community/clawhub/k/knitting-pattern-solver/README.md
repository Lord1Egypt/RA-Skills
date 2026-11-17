# Knitting Pattern Solver

## The Problem

Knitting patterns use a dense shorthand notation (`k2, p1, *yo, k2tog, rep from * 3 times`) that is:
- **Impenetrable to beginners** — you need to memorize dozens of abbreviations before you can start
- **Error-prone for experts** — miscounting a repeat or miscalculating yarn means ripping out hours of work
- **Opaque for planning** — there's no easy way to know "how much yarn will this actually use?" before you commit

Every knitter has experienced the frustration of running out of yarn on the last 10 rows, or discovering a stitch-count error 50 rows after it happened.

## Who Needs This

- **53 million knitters in the US alone** (Craft Yarn Council), 28+ million in the UK/EU
- Beginners who can't yet read pattern notation fluently
- Experienced knitters managing complex lace/cable patterns with many repeats
- Yarn shop owners helping customers plan projects and buy the right amount
- Pattern designers verifying their repeat math before publishing

## How It Works

The skill provides two core tools:

### Pattern Parser (`scripts/pattern_parser.py`)
Parses standard knitting notation into structured data. It:
- Splits a row instruction into segments (plain stitches, repeats, special instructions)
- Expands `* ... rep from * N times` into explicit stitch sequences
- Computes net stitch count change per row
- Tracks running stitch count from cast-on through every row
- Flags mismatches when the repeat doesn't divide evenly into available stitches

### Yarn Calculator (`scripts/yarn_calculator.py`)
Projects total yarn needed from a gauge swatch. It:
- Takes swatch dimensions (stitches/4", rows/4", yards used in swatch)
- Takes project dimensions (total stitches wide, total rows)
- Calculates the area ratio and projects total yardage
- Adds a configurable safety buffer (default 15%)
- Converts to skein count for common skein sizes

## Real-World Example

Sarah is knitting her first lace shawl. The pattern reads:
```
CO 120 sts
Row 1: *k2tog, yo, k1, yo, ssk, rep from * to end
Row 2: purl
```

She runs the parser:
```bash
$ python scripts/pattern_parser.py --verify "CO 120, Row 1: *k2tog, yo, k1, yo, ssk, rep from * to end, Row 2: p"
```

Output:
```
Cast on: 120 stitches

Row 1: *k2tog, yo, k1, yo, ssk, rep from * to end
  Repeat unit: [k2tog(-1), yo(+1), k1(0), yo(+1), ssk(-1)] = 5 sts, net +0
  120 / 5 = 24 repeats (divides evenly ✓)
  Row 1 stitch count: 120 (no change)

Row 2: purl
  Stitch count: 120 (no change)

All rows verified. Pattern is balanced.
```

She then calculates yarn:
```bash
$ python scripts/yarn_calculator.py --gauge-stitches 24 --gauge-rows 28 --swatch-yards 12 --project-stitches 120 --project-rows 180
```

Output:
```
Gauge: 24 sts × 28 rows per 4" square
Swatch area: 672 stitch-units, consumed 12 yards
Project area: 120 × 180 = 21,600 stitch-units
Area ratio: 21,600 / 672 = 32.14
Estimated yarn: 12 × 32.14 = 385.7 yards
With 15% buffer: 443.6 yards
Recommended: Buy 3 skeins of 165yd each (495 yd total)
```

## License

MIT — see [LICENSE](LICENSE)
