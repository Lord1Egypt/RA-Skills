import sys
import argparse
import json
import subprocess
from googlesearch import search

def scan_email(email):
    try:
        result = subprocess.run(['holehe', email, '--only-used'], capture_output=True, text=True)
        raw_lines = result.stdout.split('\n')
        registered = [
            line.replace("[+]", "").strip() 
            for line in raw_lines 
            if "[+]" in line and "Email used" not in line
        ]
        return json.dumps({"target": email, "registered_sites": registered})
    except Exception as e:
        return json.dumps({"error": str(e)})

def scan_username(username):
    try:
        result = subprocess.run(['sherlock', username, '--timeout', '1'], capture_output=True, text=True)
        found = [line.split(': ')[1] for line in result.stdout.split('\n') if 'http' in line]
        return json.dumps({"target": username, "profiles": found})
    except Exception as e:
        return json.dumps({"error": str(e)})

def search_leaks(query):
    dorks = [
        f'site:pastebin.com "{query}"',
        f'site:github.com "{query}" "password"',
        f'"{query}" "database leak"'
    ]
    findings = {}
    try:
        for dork in dorks:
            findings[dork] = [j for j in search(dork, num_results=5)]
        return json.dumps({"query": query, "results": findings})
    except Exception as e:
        return json.dumps({"error": str(e)})

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--tool", required=True)
    parser.add_argument("--target")
    parser.add_argument("--query")
    args = parser.parse_args()

    if args.tool == "scan_email":
        print(scan_email(args.target))
    elif args.tool == "scan_username":
        print(scan_username(args.target))
    elif args.tool == "search_leaks":
        print(search_leaks(args.query))