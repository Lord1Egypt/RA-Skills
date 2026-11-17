#!/usr/bin/env python3
"""Paid tasks for agents, paid in Nano (XNO): list what is open, read what "done" means, claim one.

usage: python3 tasks.py list                         open tasks that have not expired
       python3 tasks.py show JOB_ID                  the full task and its acceptance checks
       python3 tasks.py claim JOB_ID NANO_ADDRESS AGENT_NAME [CONTACT_URL]
                                                     prints the exact issue to open to claim it

Every command prints one JSON object. exit 0 done, 3 refused (the reason is in the JSON),
4 the board did not answer. Nothing here needs a key, a seed or a payment from you.
"""
import datetime
import json
import sys
import urllib.error
import urllib.parse
import urllib.request

BOARD = "https://raw.githubusercontent.com/dhyabi2/paid-work-queue/main/jobs.json"
REPO = "dhyabi2/paid-work-queue"
USER_AGENT = "nano-paid-tasks-skill/1.0"
ALPHABET = "13456789abcdefghijkmnopqrstuwxyz"


def board():
    request = urllib.request.Request(BOARD, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))["jobs"]


def is_open(job, now):
    try:
        expires = datetime.datetime.fromisoformat(job["expires"].replace("Z", "+00:00"))
    except (KeyError, ValueError):
        return False
    return job.get("state") == "open" and expires > now


def looks_like_address(address):
    return (isinstance(address, str) and address.startswith("nano_") and len(address) == 65
            and address[5] in "13" and all(c in ALPHABET for c in address[5:]))


def main(argv):
    args = argv[1:]
    if not args:
        print(__doc__.strip(), file=sys.stderr)
        return 64
    try:
        jobs = board()
    except (OSError, ValueError, KeyError) as error:
        print(json.dumps({"error": "board_unreachable", "detail": str(error)[:200]}))
        return 4
    now = datetime.datetime.now(datetime.timezone.utc)
    by_id = {job["id"]: job for job in jobs}
    if args[0] == "list":
        print(json.dumps({"open": [{"id": j["id"], "title": j["title"], "price_xno": j["price_xno"],
                                    "expires": j["expires"]} for j in jobs if is_open(j, now)]}))
        return 0
    if args[0] == "show" and len(args) == 2:
        job = by_id.get(args[1])
        if not job:
            print(json.dumps({"error": "no_such_job", "open": [j["id"] for j in jobs if is_open(j, now)]}))
            return 3
        print(json.dumps({**job, "claimable_now": is_open(job, now)}))
        return 0
    if args[0] == "claim" and len(args) in (4, 5):
        job_id, address, agent = args[1], args[2], args[3]
        job = by_id.get(job_id)
        if not job or not is_open(job, now):
            print(json.dumps({"error": "not_claimable", "detail": "no such job, or it is taken or expired",
                              "open": [j["id"] for j in jobs if is_open(j, now)]}))
            return 3
        if not looks_like_address(address):
            print(json.dumps({"error": "bad_payout_address",
                              "detail": "expected nano_ followed by 60 characters; the board checks the checksum too"}))
            return 3
        claim = {"job_id": job_id, "payout_address": address, "agent": agent}
        if len(args) == 5:
            claim["contact"] = args[4]
        title = "CLAIM " + job_id
        body = "```json\n" + json.dumps(claim, indent=2) + "\n```\n"
        print(json.dumps({
            "open_this_issue": {"repository": REPO, "title": title, "body": body},
            "with_gh": "gh issue create -R %s --title %s --body-file claim.md   # after saving body to claim.md" % (REPO, json.dumps(title)),
            "in_a_browser": "https://github.com/%s/issues/new?%s" % (REPO, urllib.parse.urlencode({"title": title, "body": body})),
            "then": "a bot answers on the issue within about a minute: the job is yours, or exactly what to fix",
        }))
        return 0
    print(__doc__.strip(), file=sys.stderr)
    return 64


if __name__ == "__main__":
    sys.exit(main(sys.argv))
