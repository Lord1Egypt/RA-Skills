#!/usr/bin/env python3
"""
build_occupations.py — rebuild data/career/occupations.json from the O*NET text databases.

The career module scores people against the occupations listed in that file, and its
numbers must be O*NET's, not anyone's transcription. This rebuilds every number for the
SOC codes the file already lists, straight from the database files, and refuses to
overwrite a number the file carries when the databases now say something else, until
you have looked at the change.

A maintainer tool: the skill never runs it. Download and unzip the text databases from
https://www.onetcenter.org/database.html (the release in INTEREST_DB, and WORK_VALUES_DB
for Work Values, which O*NET no longer publishes), then:

    python3 tools/build_occupations.py --interest-db db_31_0_text --work-values-db db_30_2_text --check
    python3 tools/build_occupations.py --interest-db db_31_0_text --work-values-db db_30_2_text

--check rebuilds in memory and exits 1 if the file differs from what the databases say.
A plain run writes the file, unless a number the file already carries would change (a
new O*NET release does that): then it prints each change and exits 3 without writing,
until you pass --allow-changes. A missing table, column or occupation, a rating outside its
scale, or two rows that disagree about one rating exits 2 without writing. For a new release,
update INTEREST_DB, and the file names below if O*NET renamed them.
"""
import argparse
import csv
import datetime
import json
import math
import os
import sys
from collections import Counter, defaultdict

INTEREST_DB = "31.0"
WORK_VALUES_DB = "30.2"

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(SKILL, "data", "career", "occupations.json")
CODE = "O*NET-SOC Code"
LETTERS = "RIASEC"
OI = {"1.B.1.a": "Realistic", "1.B.1.b": "Investigative", "1.B.1.c": "Artistic",
      "1.B.1.d": "Social", "1.B.1.e": "Enterprising", "1.B.1.f": "Conventional"}
IH = {"1.B.1.g": "First Interest High-Point", "1.B.1.h": "Second Interest High-Point",
      "1.B.1.i": "Third Interest High-Point"}
WV = {"1.B.2.a": "Achievement", "1.B.2.b": "Working Conditions", "1.B.2.c": "Recognition",
      "1.B.2.d": "Relationships", "1.B.2.e": "Support", "1.B.2.f": "Independence"}
# Everyday occupations to name as missing when the databases carry them and the file doesn't:
# preschool teachers, patrol officers, couriers, light truck drivers.
COMMON_ELSEWHERE = ("25-2011.00", "33-3051.00", "43-5021.00", "53-3033.00")
FIELD_REMARK = ("still weighted toward the author's own field (data science, ML, research, "
                "computing, medical imaging) with a spread across healthcare, skilled trades, "
                "arts, social services and education, business, sales and law, and "
                "administration and finance")
BROWSE_PAGES = "onetonline.org/explore/interests"


class BuildError(Exception):
    """A table, a column or an occupation the build needs is missing or malformed."""


def _number(row, column, low, high, where, whole=False):
    """A table value that has to be a number on its scale, [low, high], and a whole number
    when `whole`. NaN and 70 used to be written as interest ratings, an IH of 7 crashed, -1 was
    read as the high point E, and a truncated row ended in a traceback."""
    raw = row.get(column)
    try:
        value = float(raw)
    except (TypeError, ValueError):
        raise BuildError(f"{where}: {column} {raw!r} is not a number")
    if not math.isfinite(value) or not low <= value <= high or (whole and not value.is_integer()):
        raise BuildError(f"{where}: {column} {raw!r} is not "
                         + ("a whole number " if whole else "a number ") + f"from {low} to {high}")
    return int(value) if whole else value


def _put(table, code, key, value, where):
    """Record one rating once; True when it is new. A second row that disagreed used to
    replace the first without a word, and an identical one counted its rating twice."""
    if key in table[code]:
        if table[code][key] != value:
            raise BuildError(f"{where}: two rows disagree about {code} {key}: "
                             f"{table[code][key]} and {value}")
        return False
    table[code][key] = value
    return True


def _rows(folder, name):
    path = os.path.join(folder, name)
    if not os.path.exists(path):
        raise BuildError(f"missing {path}")
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t", quoting=csv.QUOTE_NONE))


def _element(row, ids):
    if ids.get(row["Element ID"]) != row["Element Name"]:
        raise BuildError(f"unexpected element {row['Element ID']} {row['Element Name']!r}")
    return row["Element Name"]


def read_tables(interest_db, work_values_db):
    if os.path.exists(os.path.join(interest_db, "Work Values.txt")):
        raise BuildError(f"{interest_db} has its own Work Values.txt: point --work-values-db at "
                         "it and update WORK_VALUES_DB")
    t = {"titles": {}, "oi": defaultdict(dict), "ih": defaultdict(dict),
         "source": defaultdict(Counter), "zones": {}, "ex": defaultdict(dict)}
    titles, zones = defaultdict(dict), defaultdict(dict)
    for r in _rows(interest_db, "Occupation Data.txt"):
        _put(titles, r[CODE], "Title", r["Title"], "Occupation Data.txt")
    for r in _rows(interest_db, "Career Interest Types.txt"):
        where = f"Career Interest Types.txt, {r[CODE]}"
        if r["Scale ID"] == "OI":        # Occupational Interests, 1-7
            if _put(t["oi"], r[CODE], _element(r, OI), _number(r, "Data Value", 1, 7, where), where):
                t["source"][r[CODE]][r["Domain Source"]] += 1
        elif r["Scale ID"] == "IH":      # Interest High-Points, 0 (none) or 1-6 for R..C
            _put(t["ih"], r[CODE], _element(r, IH),
                 _number(r, "Data Value", 0, 6, where, whole=True), where)
    for r in _rows(interest_db, "Job Zones.txt"):
        where = f"Job Zones.txt, {r[CODE]}"
        _put(zones, r[CODE], "Job Zone", _number(r, "Job Zone", 1, 5, where, whole=True), where)
    for r in _rows(work_values_db, "Work Values.txt"):
        if r["Scale ID"] == "EX":        # Work Values Extent, 1-7
            where = f"Work Values.txt, {r[CODE]}"
            _put(t["ex"], r[CODE], _element(r, WV), _number(r, "Data Value", 1, 7, where), where)
    t["titles"] = {c: v["Title"] for c, v in titles.items()}
    t["zones"] = {c: v["Job Zone"] for c, v in zones.items()}
    return t


def rank_work_values(extent):
    """Highest Extent first. Values with the same Extent share the average of the places they
    span, so two tied for second both rank 2.5. Ties used to be broken by value name, which let
    the alphabet move occupations between values bands."""
    order = sorted(extent, key=lambda n: (-extent[n], n))
    ranks = {}
    for n in order:
        places = [i + 1 for i, m in enumerate(order) if extent[m] == extent[n]]
        rank = sum(places) / len(places)
        ranks[n] = int(rank) if rank.is_integer() else rank
    return ranks


def _joined(items):
    return items[0] if len(items) == 1 else "; ".join(items[:-1]) + "; and " + items[-1]


def build(previous, tables, compiled):
    """The rebuilt document for the SOC codes `previous` lists, in its order."""
    occupations, not_rated, source = [], [], Counter()
    for o in previous["occupations"]:
        c = o["soc_code"]
        oi, ih = tables["oi"].get(c, {}), tables["ih"].get(c, {})
        if c not in tables["titles"] or sorted(oi) != sorted(OI.values()) or c not in tables["zones"]:
            raise BuildError(f"{c} ({o.get('title')}) is not fully in the O*NET {INTEREST_DB} tables")
        high_point = "".join(LETTERS[ih[k] - 1] for k in IH.values() if ih.get(k, 0))
        if not high_point:
            raise BuildError(f"{c} has no interest high point")
        ex = tables["ex"].get(c)
        if ex is not None and sorted(ex) != sorted(WV.values()):
            raise BuildError(f"{c} has an incomplete set of Work Values: {sorted(ex)}")
        if ex is None:
            not_rated.append(f"{tables['titles'][c]} {c}")
        source.update(tables["source"][c])
        occupations.append({
            "soc_code": c, "title": tables["titles"][c],
            "riasec": [oi[n] for n in OI.values()], "high_point_code": high_point,
            "job_zone": tables["zones"][c], "source_url": o.get("source_url"),
            "work_values": rank_work_values(ex) if ex else None,
            "work_values_extent_1_7": dict(sorted(ex.items())) if ex else None,
            "work_values_db": WORK_VALUES_DB if ex else None,
        })

    n = len(occupations)
    listed = {o["soc_code"] for o in occupations}
    leads = sum(o["riasec"][LETTERS.index(o["high_point_code"][0])] == max(o["riasec"])
                for o in occupations)
    areas = len({o["high_point_code"][0] for o in occupations})
    elsewhere = [tables["titles"][c] for c in COMMON_ELSEWHERE
                 if c not in listed and sorted(tables["oi"].get(c, {})) == sorted(OI.values())]
    counts = [f"{k} for {v}" for k, v in source.most_common()]
    interest_source = (
        "O*NET marks the Domain Source of these interest ratings as "
        + (" and ".join([", ".join(counts[:-1]), counts[-1]]) if len(counts) > 1 else counts[0])
        + f" of the {sum(source.values())} ratings here"
        + (": they are O*NET's model estimates, and should be described that way."
           if all("Machine Learning" in k for k in source) else
           ". Describe each rating by its source."))
    return {
        "dataset": "onet_occupations_career_fit",
        "version": str(previous.get("version", "1.0.0")).split("+")[0] + f"+onet{INTEREST_DB}",
        "compiled": compiled,
        "license": "CC BY 4.0",
        "attribution": (
            f"This page includes information from the O*NET {INTEREST_DB} Database and the O*NET "
            f"{WORK_VALUES_DB} Database by the U.S. Department of Labor, Employment and Training "
            "Administration (USDOL/ETA). Used under the CC BY 4.0 license. O*NET® is a trademark "
            "of USDOL/ETA. The developer of the life-companion skill has modified all or some of "
            "this information. USDOL/ETA has not approved, endorsed, or tested these "
            "modifications."),
        "fetched_from": [
            f"https://www.onetcenter.org/dl_files/database/db_{INTEREST_DB.replace('.', '_')}_text.zip",
            f"https://www.onetcenter.org/dl_files/database/db_{WORK_VALUES_DB.replace('.', '_')}_text.zip",
            "https://www.onetcenter.org/license_db.html",
        ] + [u for u in previous.get("fetched_from", []) if BROWSE_PAGES in u],
        "schema": {
            "soc_code": "O*NET-SOC 8-digit occupation code (string)",
            "title": f"O*NET occupation title (O*NET {INTEREST_DB} Occupation Data)",
            "riasec": (f"[R,I,A,S,E,C] O*NET Occupational Interest ratings, 1-7 (O*NET {INTEREST_DB} "
                       "Career Interest Types, scale OI). Every occupation here carries them; "
                       "career_match.py still accepts null for a code-only occupation"),
            "high_point_code": ("O*NET's own First/Second/Third Interest High-Point as 1-3 Holland "
                                f"letters (O*NET {INTEREST_DB}, scale IH)"),
            "job_zone": f"O*NET Job Zone, integer 1-5 (O*NET {INTEREST_DB} Job Zones)",
            "source_url": ("O*NET OnLine page where the occupation was first observed (a "
                           "Browse-by-Interests list or the occupation's summary page); the numbers "
                           "come from the database files in fetched_from"),
            "work_values": ("{value_name: rank 1-6} ipsative ranking (1=most important) over the six "
                            "O*NET Work Values, where values with equal Extent share the average "
                            f"rank (2.5), or null when O*NET {WORK_VALUES_DB} does not rate the "
                            "occupation"),
            "work_values_extent_1_7": ("the six 1-7 Extent scores the ranking was derived from "
                                       f"(O*NET {WORK_VALUES_DB} Work Values, scale EX), or null"),
            "work_values_db": ("O*NET Database release the Work Values came from "
                               f"(\"{WORK_VALUES_DB}\"), or null"),
        },
        "notes": {
            "build": (
                f"Built by tools/build_occupations.py from the O*NET {INTEREST_DB} text database "
                "(Occupation Data.txt, Career Interest Types.txt, Job Zones.txt) and, for Work "
                f"Values, the O*NET {WORK_VALUES_DB} text database (Work Values.txt), for the SOC "
                "codes this file already listed. A value O*NET does not publish is null; nothing "
                "is estimated."),
            "interest_source": interest_source,
            "work_values_ranks": (
                "work_values ranks the six Extent scores from highest to lowest. Values with equal "
                "Extent share the average of the places they span, so two tied for second both "
                "rank 2.5: no tie is broken by value name."),
            **({"mapped_terms": previous["notes"]["mapped_terms"]}
               if previous.get("notes", {}).get("mapped_terms") else {}),
            "not_rated_for_work_values": (
                f"{len(not_rated)} occupations have no Work Values in O*NET {WORK_VALUES_DB} and "
                "carry work_values: null: " + "; ".join(not_rated) + "."
                if not_rated else "Every occupation here has Work Values."),
        },
        "count": n,
        "occupations": occupations,
        "scale_note": (
            "riasec holds O*NET Occupational Interests (elements 1.B.1.a-f, scale OI), 1-7, higher "
            f"= stronger interest, from the O*NET {INTEREST_DB} Database (Career Interest Types.txt). "
            "high_point_code is O*NET's First/Second/Third Interest High-Point (elements "
            "1.B.1.g/h/i, scale IH), mapped 1=R, 2=I, 3=A, 4=S, 5=E, 6=C, with 0 meaning no "
            "further high point. "
            + ("In every occupation here the first high point is one of the highest of the six "
               "ratings. " if leads == n else
               f"For {leads} of these {n} occupations the first high point is one of the highest "
               "of the six ratings. ")
            + "work_values_extent_1_7 holds the six O*NET Work Values (elements 1.B.2.a-f, scale "
            f"EX, Extent), 1-7, from the O*NET {WORK_VALUES_DB} Database."),
        "coverage_note": (
            f"{n} occupations across "
            + ("all six RIASEC areas" if areas == 6 else f"{areas} of the six RIASEC areas")
            + f", {FIELD_REMARK}. All {n} carry numeric interest ratings; "
            + f"{n - len(not_rated)} also carry Work Values."
            + (f" Common occupations such as {_joined(elsewhere)} are in O*NET {INTEREST_DB} but "
               "not in this file." if elsewhere else "")),
        "work_values_discontinuation_note": (
            f"O*NET no longer publishes Work Values: the O*NET {INTEREST_DB} text database has no "
            f"Work Values.txt, so Work Values here come from {WORK_VALUES_DB}, an older release "
            f"than the interest data. Occupations {WORK_VALUES_DB} does not rate carry "
            "work_values: null, not an estimate."),
    }


def changes(previous, doc):
    """Values the file already carries that the databases now say differently."""
    rebuilt = {o["soc_code"]: o for o in doc["occupations"]}
    out = []
    for o in previous["occupations"]:
        for field in ("title", "riasec", "high_point_code", "job_zone", "work_values",
                      "work_values_extent_1_7"):
            old, new = o.get(field), rebuilt[o["soc_code"]][field]
            if old is not None and old != new:
                out.append((o["soc_code"], field, old, new))
    return out


def serialize(doc):
    return json.dumps(doc, ensure_ascii=False, indent=1) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description="Rebuild occupations.json from the O*NET text databases.")
    ap.add_argument("--interest-db", required=True,
                    help=f"unzipped O*NET {INTEREST_DB} text database folder")
    ap.add_argument("--work-values-db", required=True,
                    help=f"unzipped O*NET {WORK_VALUES_DB} text database folder")
    ap.add_argument("--data", default=DATA, help="the occupations.json to rebuild (default: the skill's)")
    ap.add_argument("--compiled", help="date to write in `compiled` (default today; --check keeps the file's)")
    ap.add_argument("--check", action="store_true",
                    help="rebuild in memory and exit 1 if the file differs")
    ap.add_argument("--allow-changes", action="store_true",
                    help="write even when a value the file carries would change")
    a = ap.parse_args(argv)
    try:
        with open(a.data, encoding="utf-8") as f:
            text = f.read()
        previous = json.loads(text)
        if (not isinstance(previous, dict) or not isinstance(previous.get("occupations"), list)
                or not all(isinstance(o, dict) and o.get("soc_code") for o in previous["occupations"])):
            raise BuildError(f"{a.data} is not an occupations file: it needs an object whose "
                             "\"occupations\" list gives every entry a soc_code")
        compiled = (previous.get("compiled") if a.check
                    else a.compiled or datetime.date.today().isoformat())
        doc = build(previous, read_tables(a.interest_db, a.work_values_db), compiled)
    except (BuildError, KeyError, OSError, ValueError) as e:
        print(f"build_occupations: {e!r}", file=sys.stderr)
        return 2
    out = serialize(doc)
    if a.check:
        if out == text:
            print(f"{a.data} matches the O*NET {INTEREST_DB} and {WORK_VALUES_DB} databases")
            return 0
        old_lines, new_lines = text.splitlines(), out.splitlines()
        diff = [(i, x, y) for i, (x, y) in enumerate(zip(old_lines, new_lines), 1) if x != y]
        print(f"{a.data} differs from what the databases say: {len(diff)} differing lines, "
              f"{len(old_lines)} lines in the file against {len(new_lines)} rebuilt")
        for i, x, y in diff[:10]:
            print(f"  line {i}\n    file:    {x.strip()[:160]}\n    rebuilt: {y.strip()[:160]}")
        return 1
    changed = changes(previous, doc)
    if changed and not a.allow_changes:
        print(f"refusing to write: {len(changed)} values the file carries would change",
              file=sys.stderr)
        for c, field, old, new in changed[:40]:
            print(f"  {c} {field}: {old!r} -> {new!r}", file=sys.stderr)
        if len(changed) > 40:
            print(f"  ... and {len(changed) - 40} more", file=sys.stderr)
        print("look at them, then pass --allow-changes", file=sys.stderr)
        return 3
    with open(a.data, "w", encoding="utf-8") as f:
        f.write(out)
    print(f"wrote {a.data}: {doc['count']} occupations, "
          f"{sum(bool(o['work_values']) for o in doc['occupations'])} with Work Values, "
          f"{len(changed)} changed values")
    return 0


if __name__ == "__main__":
    sys.exit(main())
