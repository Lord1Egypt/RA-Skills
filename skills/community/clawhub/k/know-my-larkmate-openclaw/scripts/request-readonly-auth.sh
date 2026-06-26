#!/usr/bin/env bash
set -euo pipefail

SCOPES="auth:user.id:read calendar:calendar.event:read docs:document.content:read docx:document:readonly drive:drive.metadata:readonly im:chat:read im:message.group_msg:get_as_user im:message.p2p_msg:get_as_user minutes:minutes.search:read minutes:minutes:readonly search:docs:read search:message vc:meeting.search:read wiki:node:read wiki:node:retrieve wiki:space:read wiki:space:retrieve offline_access"

exec lark-cli auth login --scope "$SCOPES"
