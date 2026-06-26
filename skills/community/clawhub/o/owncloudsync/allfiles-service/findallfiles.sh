#!/usr/bin/bash
# Date 26/02/2026
# This script is part of the allfiles service
# The allfiles service is used by the openclaw skill Owncloud-sync
#
# Narrower scope version : exclude images (if used, adapt google query)
#  -type f ! -name "*.png" ! -name "*.jpg" -printf '%f|%TY-%Tm-%Td %TH:%TM\n' > /tmp/allfiles.txt

# ---------------------------------------------------------------------------
# Guard against symlink attacks: reject any attempt to serve /tmp/allfiles.txt
# if it has been replaced by a symbolic link. A local attacker could otherwise
# point it to an arbitrary file (e.g. /etc/passwd) and leak its contents
# through the /allfiles endpoint.
# ---------------------------------------------------------------------------
if [[ -L "/tmp/allfiles.txt" ]]; then
    echo "FATAL: /tmp/allfiles.txt is a symbolic link — possible symlink attack detected." >&2
    exit 1
fi

# WARNING: ADAPT NEXT 2 LINES !!
OWNCLOUD_USERNAME=ChangeUserNameHere
OWNCLOUD_ROOT_INSTALL_DIR=/var/www/html/data

# ---------------------------------------------------------------------------
# Validate configuration variables against an explicit allowlist of safe
# characters before interpolating them into the find command. Although these
# values are set statically by an administrator, rejecting unexpected characters
# (spaces, shell metacharacters, path traversal sequences) prevents accidental
# or malicious misconfiguration from causing unintended command behavior.
# ---------------------------------------------------------------------------
if [[ ! "$OWNCLOUD_USERNAME" =~ ^[a-zA-Z0-9._-]+$ ]]; then
    echo "FATAL: OWNCLOUD_USERNAME contains invalid characters: '$OWNCLOUD_USERNAME'" >&2
    exit 1
fi

if [[ ! "$OWNCLOUD_ROOT_INSTALL_DIR" =~ ^/[a-zA-Z0-9/_-]+$ ]]; then
    echo "FATAL: OWNCLOUD_ROOT_INSTALL_DIR contains invalid characters: '$OWNCLOUD_ROOT_INSTALL_DIR'" >&2
    exit 1
fi

/usr/bin/find "$OWNCLOUD_ROOT_INSTALL_DIR"/"$OWNCLOUD_USERNAME"/ -type f -printf '%f|%TY-%Tm-%Td %TH:%TM\n' > /tmp/allfiles.txt
