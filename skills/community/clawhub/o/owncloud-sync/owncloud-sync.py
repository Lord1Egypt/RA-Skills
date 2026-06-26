#!/usr/bin/env python3

import subprocess
import json
import re
from datetime import datetime, timedelta
import os
import sys

CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'owncloud.json')

# Load config
with open(CONFIG_FILE) as f:
    config = json.load(f)

OWNCLOUD_URL = config.get('OWNCLOUD_URL')
OWNCLOUD_USER = config.get('OWNCLOUD_USER')
OWNCLOUD_PASS = config.get('OWNCLOUD_PASSWD')

GOG_ACCOUNT = 'denis.etienne@gmail.com'
EMAIL_RECIPIENT = 'denis.etienne@gmail.com'
PERIOD_DAYS = 30
START_DATE = (datetime.now() - timedelta(days=PERIOD_DAYS)).strftime('%Y-%m-%d')

GOOGLE_DRIVE_QUERY = f'after:{START_DATE}'


# Function to run shell command and return output

def run_cmd(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f'Error running command: {cmd}', file=sys.stderr)
        print(e, file=sys.stderr)
        print(result.stdout, file=sys.stderr)
        sys.exit(1)


GOG_BIN = '/opt/homebrew/bin/gog'

def gog_drive_search(query):
    cmd = f'{GOG_BIN} --verbose drive search "{query}"'
    return run_cmd(cmd).splitlines()


def owncloud_search_file(filename):
    # Prepare XML body for SEARCH
    xml_body = f'''<?xml version="1.0" encoding="UTF-8"?>
<ns0:searchrequest xmlns:ns0="urn:ietf:params:xml:ns:caldav">
  <ns0:basicsearch>
    <ns0:select>
      <ns0:prop>
        <d:getlastmodified xmlns:d="DAV:"/>
        <d:displayname xmlns:d="DAV:"/>
        <d:href xmlns:d="DAV:"/>
      </ns0:prop>
    </ns0:select>
    <ns0:from>
      <ns0:scope>
        <ns0:depth>infinity</ns0:depth>
      </ns0:scope>
    </ns0:from>
    <ns0:where>
      <ns0:like>
        <ns0:prop>
          <d:displayname xmlns:d="DAV:"/>
        </ns0:prop>
        <ns0:literal>*{filename}*</ns0:literal>
      </ns0:like>
    </ns0:where>
  </ns0:basicsearch>
</ns0:searchrequest>'''

    # Run curl command
    curl_cmd = [
        'curl', '-s', '-u', f'{OWNCLOUD_USER}:{OWNCLOUD_PASS}',
        '-X', 'SEARCH',
        '-H', 'Content-Type: text/xml',
        '-d', xml_body,
        OWNCLOUD_URL
    ]

    try:
        result = subprocess.run(curl_cmd, capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        print('Failed to query OwnCloud', file=sys.stderr)
        print(e, file=sys.stderr)
        sys.exit(1)

    response = result.stdout

    # Save xml_body to report file for logging
    with open(os.path.join(os.path.dirname(__file__), 'owncloud-sync-report.rqt'), 'a') as f:
        f.write(xml_body + '\n')

    # Parse response using regex
    hrefs = re.findall(r'<d:href>(.*?)</d:href>', response)
    displaynames = re.findall(r'<d:displayname>(.*?)</d:displayname>', response)
    lastmodifieds = re.findall(r'<d:getlastmodified>(.*?)</d:getlastmodified>', response)

    for dn, href, lm in zip(displaynames, hrefs, lastmodifieds):
        if dn == filename:
            return href + '||' + lm
    return ''


def parse_gdrive_line(line):
    # Expected format:
    # ID <file_name> file <size_unit> YYYY-MM-DD HH:MM

    # Split line into id and rest
    parts = line.split(None, 1)
    if len(parts) < 2:
        return None
    _id, rest = parts

    # Use regex to extract filename and metadata
    # Metadata pattern
    meta_pattern = re.compile(r' file +[\d\.]+ (B|KB|MB|GB) +\d{4}-\d{2}-\d{2} \d{2}:\d{2}$')

    m = meta_pattern.search(rest)
    if not m:
        print(f"Failed to parse metadata in line: {line}", file=sys.stderr)
        return None

    filename = rest[:m.start()].rstrip()
    metadata = rest[m.start():].strip()

    # Extract modification date
    mod_date = metadata.split()[-2] + ' ' + metadata.split()[-1]

    return {
        'id': _id,
        'filename': filename,
        'mod_date': mod_date
    }


def main():
    gd_lines = gog_drive_search(GOOGLE_DRIVE_QUERY)

    files = []

    for line in gd_lines:
        if line.strip() == '' or line.startswith('NAME '):
            continue
        parsed = parse_gdrive_line(line)
        if parsed:
            files.append(parsed)

    report = []
    report.append(f'OwnCloud Sync Report - Last {PERIOD_DAYS} days')
    report.append(f'Report generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    report.append(f'Total new files in Google Drive: {len(files)}')
    report.append('Files missing or older on OwnCloud:')

    for f in files:
        oc_result = owncloud_search_file(f['filename'])
        if not oc_result:
            report.append(f"{f['filename']} - MISSING")
        else:
            path, lm_str = oc_result.split('||')
            try:
                gd_dt = datetime.strptime(f['mod_date'], '%Y-%m-%d %H:%M')
                oc_dt = datetime.strptime(lm_str, '%a, %d %b %Y %H:%M:%S %Z')
            except Exception as e:
                print(f"Failed to parse dates for file {f['filename']}: {e}", file=sys.stderr)
                continue

            if gd_dt > oc_dt:
                report.append(f"{f['filename']} - OLDER ON OWNCLOUD (path: {path})")

    report.append('')
    report.append(f'Report generation time: (approx)')

    report_file = os.path.join(os.path.dirname(__file__), 'owncloud-sync-report.txt')

    with open(report_file, 'w') as rf:
        rf.write('\n'.join(report) + '\n')

    # Send the report by email using gog mail
    mail_cmd = [
        GOG_BIN, 'mail', 'send',
        '--to', EMAIL_RECIPIENT,
        '--subject', 'OwnCloud Sync Report',
        '--body-file', report_file
    ]

    try:
        subprocess.run(mail_cmd, check=True)
    except subprocess.CalledProcessError as e:
        print('Failed to send email report', file=sys.stderr)
        print(e, file=sys.stderr)


if __name__ == '__main__':
    main()
