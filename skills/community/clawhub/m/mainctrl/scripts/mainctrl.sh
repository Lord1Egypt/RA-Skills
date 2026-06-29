#!/usr/bin/env bash
set -euo pipefail

# mainctrl.sh — Manage agent tool-blocking state.
#
# Commands:
#   mainctrl status                    Show current state
#   mainctrl on                        Enable blocking (safety on)
#   mainctrl off                       Disable blocking (all tools passthrough)
#   mainctrl agents '<json-array>'     Set controlled agents (JSON array)
#   mainctrl tools [<json-array>]      Show blocked tools, or set (JSON array)
#   mainctrl allow-except '<json>'     Set execAllowExcept (JSON object)
#   mainctrl refresh-memory            Write current status to MEMORY.md

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
STATE_FILE="$SCRIPT_DIR/state.json"
ALL_TOOLS=("write" "edit" "exec" "process" "apply_patch")

# --- helpers ---------------------------------------------------------

die() { echo "mainctrl: $*" >&2; exit 1; }


read_state() {
  if [[ ! -f "$STATE_FILE" ]]; then
    echo '{"enabled":false,"controlledAgents":["main"],"blockedTools":["write","edit","exec","process","apply_patch"],"execAllowExcept":{"find":["-exec","-ok","-delete","-fprint","|","$(",">",">>"],"ls":[">",">>","|"],"pwd":[">",">>","|"],"sed":[">",">>","|",".java",".py",".js",".html",".css"],"cat":[">",">>","|"]}}'
    return
  fi
  cat "$STATE_FILE"
}

write_state() {
  local json="$1"
  echo "$json" | node -e "process.stdout.write(JSON.stringify(JSON.parse(require('fs').readFileSync('/dev/stdin','utf8')))+'\n')" > "$STATE_FILE.tmp" 2>/dev/null || die "invalid JSON"
  mv "$STATE_FILE.tmp" "$STATE_FILE"
}

# --- commands --------------------------------------------------------

cmd_status() {
  local state
  state="$(read_state)"
  local enabled agents blocked
  enabled="$(echo "$state" | node -e "const{stdin,stdout}=process;let d='';stdin.on('data',c=>d+=c);stdin.on('end',()=>{try{stdout.write(JSON.parse(d).enabled?'True':'False')}catch(e){stdout.write('false')}})" 2>/dev/null || echo "false")"
  agents="$(echo "$state" | node -e "const{stdin,stdout}=process;let d='';stdin.on('data',c=>d+=c);stdin.on('end',()=>{try{const a=JSON.parse(d).controlledAgents;stdout.write(Array.isArray(a)?a.join(' '):'main')}catch(e){stdout.write('main')}})" 2>/dev/null || echo "main")"
  blocked="$(echo "$state" | node -e "const{stdin,stdout}=process;let d='';stdin.on('data',c=>d+=c);stdin.on('end',()=>{try{stdout.write(JSON.parse(d).blockedTools.join(' '))}catch(e){}})" 2>/dev/null || echo "")"

  echo "mainctrl status:"
  if [[ "$enabled" == "True" ]]; then
    echo "  safety:            ON  (blocking is active)"
  else
    echo "  safety:            OFF (all tools passthrough)"
  fi
  echo "  controlled agents: $agents"
  echo ""
  echo "  Tool          Status"
  echo "  ------------  --------"
  for tool in "${ALL_TOOLS[@]}"; do
    if [[ "$enabled" != "True" ]]; then
      printf "  %-14s ALLOWED (safety off)\n" "$tool"
    elif echo " $blocked " | grep -q " $tool "; then
      printf "  %-14s BLOCKED\n" "$tool"
    else
      printf "  %-14s ALLOWED\n" "$tool"
    fi
  done

  echo ""

  # Show exec allow-except configuration
  local exec_allow_except
  exec_allow_except="$(echo "$state" | node -e "const{stdin,stdout}=process;let d='';stdin.on('data',c=>d+=c);stdin.on('end',()=>{const a=JSON.parse(d).execAllowExcept;if(a&&Object.keys(a).length)stdout.write(JSON.stringify(a,null,2))})")"
  if [[ -n "$exec_allow_except" ]]; then
    echo "  exec allow-except:"
    echo "$state" | node -e "const{stdin,stdout}=process;let d='';stdin.on('data',c=>d+=c);stdin.on('end',()=>{const a=JSON.parse(d).execAllowExcept||{};Object.keys(a).sort().forEach(k=>stdout.write('    '+k+': '+JSON.stringify(a[k])+'\n'))})"
  fi
}

cmd_on() {
  local state
  state="$(read_state)"
  state="$(echo "$state" | node -e "const{stdin,stdout}=process;let d='';stdin.on('data',c=>d+=c);stdin.on('end',()=>{try{const s=JSON.parse(d);s.enabled=true;stdout.write(JSON.stringify(s))}catch(e){process.exit(1)}})" 2>/dev/null || die "failed to update state")"
  write_state "$state"
  echo "mainctrl: safety ON — destructive tools blocked for controlled agents"
}

cmd_off() {
  local state
  state="$(read_state)"
  state="$(echo "$state" | node -e "const{stdin,stdout}=process;let d='';stdin.on('data',c=>d+=c);stdin.on('end',()=>{try{const s=JSON.parse(d);s.enabled=false;stdout.write(JSON.stringify(s))}catch(e){process.exit(1)}})" 2>/dev/null || die "failed to update state")"
  write_state "$state"
  echo "mainctrl: safety OFF — all tools allowed for all agents"
}

cmd_agents() {
  shift
  local agents_json="${1:-}"
  if [[ -z "$agents_json" ]]; then
    echo "Usage: mainctrl agents '<json-array>'" >&2
    echo "Example: mainctrl agents '[\"main\",\"coder\"]'" >&2
    exit 1
  fi

  # Validate JSON
  echo "$agents_json" | node -e "const{stdin}=process;let d='';stdin.on('data',c=>d+=c);stdin.on('end',()=>{try{JSON.parse(d)}catch(e){process.exit(1)}})" 2>/dev/null || die "invalid JSON array"

  local state
  state="$(read_state)"
  state="$(echo "$state" | node -e "const{stdin,stdout}=process;let d='';stdin.on('data',c=>d+=c);stdin.on('end',()=>{try{const s=JSON.parse(d);s.controlledAgents=JSON.parse(process.argv[1]);stdout.write(JSON.stringify(s))}catch(e){process.exit(1)}})" "$agents_json")" 2>/dev/null || die "failed to update agents"
  write_state "$state"
  echo "mainctrl: controlled agents updated"
}

cmd_tools() {
  shift  # discard "tools" itself
  local args=("$@")

  if [[ ${#args[@]} -eq 0 ]]; then
    # Show current blocked tools
    local state blocked
    state="$(read_state)"
    blocked="$(echo "$state" | node -e "const{stdin,stdout}=process;let d='';stdin.on('data',c=>d+=c);stdin.on('end',()=>{try{stdout.write(JSON.parse(d).blockedTools.join(' '))}catch(e){}})" 2>/dev/null || echo "")"
    local enabled
    enabled="$(echo "$state" | node -e "const{stdin,stdout}=process;let d='';stdin.on('data',c=>d+=c);stdin.on('end',()=>{try{stdout.write(JSON.parse(d).enabled?'True':'False')}catch(e){stdout.write('false')}})" 2>/dev/null || echo "false")"

    echo "mainctrl blocked tools:"
    if [[ "$enabled" != "True" ]]; then
      echo "  safety is OFF — all tools passthrough"
    fi
    echo ""
    echo "  Tool          Status"
    echo "  ------------  --------"
    for tool in "${ALL_TOOLS[@]}"; do
      if [[ "$enabled" != "True" ]]; then
        printf "  %-14s ALLOWED (safety off)\n" "$tool"
      elif echo " $blocked " | grep -q " $tool "; then
        printf "  %-14s BLOCKED\n" "$tool"
      else
        printf "  %-14s ALLOWED\n" "$tool"
      fi
    done

    echo ""

    # Show exec allow-except configuration
    local exec_allow_except
    exec_allow_except="$(echo "$state" | node -e "const{stdin,stdout}=process;let d='';stdin.on('data',c=>d+=c);stdin.on('end',()=>{const a=JSON.parse(d).execAllowExcept;if(a&&Object.keys(a).length)stdout.write(JSON.stringify(a,null,2))})")"
    if [[ -n "$exec_allow_except" ]]; then
      echo "  exec allow-except:"
      echo "$state" | node -e "const{stdin,stdout}=process;let d='';stdin.on('data',c=>d+=c);stdin.on('end',()=>{const a=JSON.parse(d).execAllowExcept||{};Object.keys(a).sort().forEach(k=>stdout.write('    '+k+': '+JSON.stringify(a[k])+'\n'))})"
    fi
    return
  fi

  # Set mode — accept JSON array
  local tools_json="${args[0]}"
  echo "$tools_json" | node -e "const{stdin}=process;let d='';stdin.on('data',c=>d+=c);stdin.on('end',()=>{try{JSON.parse(d)}catch(e){process.exit(1)}})" 2>/dev/null || die "invalid JSON array"

  local state
  state="$(read_state)"
  state="$(echo "$state" | node -e "const{stdin,stdout}=process;let d='';stdin.on('data',c=>d+=c);stdin.on('end',()=>{try{const s=JSON.parse(d);s.blockedTools=JSON.parse(process.argv[1]);stdout.write(JSON.stringify(s))}catch(e){process.exit(1)}})" "$tools_json")" 2>/dev/null || die "failed to update tools"
  write_state "$state"
  echo "mainctrl: blocked tools updated"
}

cmd_allow_except() {
  shift
  local veto_json="${1:-}"
  if [[ -z "$veto_json" ]]; then
    echo "Usage: mainctrl allow-except '<json>'" >&2
    echo "Example: mainctrl allow-except '{\"ls\":[\">\",\">>\",\"|\"],\"pwd\":[\">\",\">>\",\"|\"],\"find\":[\"-exec\",\"-ok\",\"-delete\",\"-fprint\",\"|\",\"\$(\",\">\",\">>\"]}'" >&2
    exit 1
  fi

  # Validate JSON
  echo "$veto_json" | node -e "const{stdin}=process;let d='';stdin.on('data',c=>d+=c);stdin.on('end',()=>{try{JSON.parse(d)}catch(e){process.exit(1)}})" 2>/dev/null || die "invalid JSON for execAllowExcept"

  local state
  state="$(read_state)"
  state="$(echo "$state" | node -e "const{stdin,stdout}=process;let d='';stdin.on('data',c=>d+=c);stdin.on('end',()=>{try{const s=JSON.parse(d);s.execAllowExcept=JSON.parse(process.argv[1]);stdout.write(JSON.stringify(s))}catch(e){process.exit(1)}})" "$veto_json")" 2>/dev/null || die "failed to update exec allow-except"
  write_state "$state"
  echo "mainctrl: exec allow-except updated"
}

# --- refresh-memory -------------------------------------------------

cmd_refresh_memory() {
  local status_output memory_file tmpfile
  status_output="$(cmd_status)"
  memory_file="$HOME/.openclaw/workspace/MEMORY.md"

  tmpfile="$(mktemp)"

  # Build the new block content
  {
    echo "### mainctrl 运行状态"
    echo ""
    echo '```'
    echo "$status_output"
    echo '```'
  } > "$tmpfile"

  node -e "const fs=require('fs');const newBlock=fs.readFileSync(process.argv[1],'utf8');const memFile=process.argv[2];let content='';try{content=fs.readFileSync(memFile,'utf8')}catch(e){}const m=content.match(/^### mainctrl 运行状态\\n+\x60{3}\\n[\\s\\S]*?\\n\x60{3}/m);if(m){content=content.slice(0,m.index)+newBlock+content.slice(m.index+m[0].length)}else{if(content){if(!content.endsWith('\\n'))content+='\\n';content+='\\n'+newBlock}else{content=newBlock}}fs.writeFileSync(memFile,content)" "$tmpfile" "$memory_file"

  rm -f "$tmpfile"
  echo "mainctrl: memory refreshed → $memory_file"
}

# --- plugin commands -------------------------------------------------

cmd_plugin_install() {
  # Install the companion plugin from projects source
  local src="$SCRIPT_DIR/../plugin"
  if [[ ! -f "$src/package.json" ]]; then
    die "plugin source not found at $src"
  fi
  openclaw plugins install "$src" --force
  openclaw plugins enable mainctrl
  echo "mainctrl: plugin installed. Restart gateway to activate."
}

cmd_plugin_remove() {
  openclaw plugins disable mainctrl
  openclaw plugins uninstall mainctrl
  echo "mainctrl: plugin removed. Restart gateway to activate."
}

# --- dispatch --------------------------------------------------------

case "${1:-}" in
  status)       cmd_status ;;
  on)           cmd_on ;;
  off)          cmd_off ;;
  agents)       cmd_agents "$@" ;;
  tools)        cmd_tools "$@" ;;
  allow-except)    cmd_allow_except "$@" ;;
  refresh-memory)  cmd_refresh_memory ;;
  plugin)          [[ -z "${2:-}" ]] && die "usage: mainctrl plugin {install|remove}"
                case "$2" in
                  install) cmd_plugin_install ;;
                  remove)  cmd_plugin_remove ;;
                  *)       die "unknown subcommand: $2" ;;
                esac ;;
  *)            echo "Usage: mainctrl {status|on|off|agents '<json-array>'|tools [<json-array>]|allow-except '<json>'|refresh-memory|plugin {install|remove}}" >&2; exit 1 ;;
esac
