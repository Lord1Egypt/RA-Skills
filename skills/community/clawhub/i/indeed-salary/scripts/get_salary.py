#!/usr/bin/env python3
"""Look up the salary for an Indeed job posting by job key or pasted URL. 1 credit.

Returns min, max, currency, period, and whether the figure came from
the employer or an estimate.

Usage:
  python3 get_salary.py a1b2c3d4e5f60718
  python3 get_salary.py a1b2c3d4e5f60718 --country gb
  python3 get_salary.py "https://www.indeed.com/viewjob?jk=a1b2c3d4e5f60718"
"""

import argparse

import _client


def main():
    parser = argparse.ArgumentParser(
        description="Salary lookup via RolesAPI (GET /v1/roles/{job_key}/salary, or /v1/roles/by-url for URLs)."
    )
    parser.add_argument("job", help="16-character job key, or an Indeed viewjob URL")
    parser.add_argument("--country", default=None, help="Two-letter Indeed country edition code (default us)")
    args = parser.parse_args()

    if args.job.startswith("http://") or args.job.startswith("https://"):
        envelope = _client.request(
            "GET",
            "/v1/roles/by-url",
            params={"url": args.job, "fields": "job_key,title,salary"},
        )
    else:
        envelope = _client.request(
            "GET",
            "/v1/roles/" + args.job + "/salary",
            params={"country": args.country},
        )
    _client.output(envelope)


if __name__ == "__main__":
    main()
