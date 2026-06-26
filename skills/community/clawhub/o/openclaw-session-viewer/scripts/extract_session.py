#!/usr/bin/env python3
"""Extract OpenClaw session and generate interactive HTML viewer."""

import json
import os
import sys
import argparse
from pathlib import Path
from datetime import datetime

def get_openclaw_dir():
    return Path.home() / ".openclaw"

def list_sessions(agent_id="main"):
    """List available sessions for an agent."""
    sessions_dir = get_openclaw_dir() / "agents" / agent_id / "sessions"
    sessions_file = sessions_dir / "sessions.json"
    
    if not sessions_file.exists():
        print(f"No sessions found for agent: {agent_id}")
        return
    
    with open(sessions_file) as f:
        index = json.load(f)
    
    print(f"Sessions for agent '{agent_id}':\n")
    for key, info in index.items():
        session_id = info.get("sessionId", "unknown")
        updated = info.get("updatedAt", 0)
        channel = info.get("lastChannel", "unknown")
        dt = datetime.fromtimestamp(updated / 1000).strftime("%Y-%m-%d %H:%M") if updated else "unknown"
        print(f"  {key}")
        print(f"    ID: {session_id}")
        print(f"    Updated: {dt}")
        print(f"    Channel: {channel}")
        print()

def get_current_session_file(agent_id="main"):
    """Get the most recently updated session file."""
    sessions_dir = get_openclaw_dir() / "agents" / agent_id / "sessions"
    sessions_file = sessions_dir / "sessions.json"
    
    if not sessions_file.exists():
        raise FileNotFoundError(f"No sessions.json found for agent: {agent_id}")
    
    with open(sessions_file) as f:
        index = json.load(f)
    
    # Find most recently updated session
    latest = None
    latest_time = 0
    for key, info in index.items():
        updated = info.get("updatedAt", 0)
        if updated > latest_time:
            latest_time = updated
            latest = info
    
    if not latest:
        raise FileNotFoundError("No sessions found")
    
    return sessions_dir / f"{latest['sessionId']}.jsonl"

def extract_session(session_file):
    """Extract conversation data from session file."""
    entries = []
    with open(session_file) as f:
        for line in f:
            if line.strip():
                entries.append(json.loads(line))
    
    context_flow = {
        "session_id": None,
        "started_at": None,
        "conversation_turns": [],
        "context_stats": {
            "total_input_tokens": 0,
            "total_output_tokens": 0,
            "total_cache_read": 0,
            "total_cost": 0.0,
            "models_used": set()
        }
    }
    
    current_turn = None
    
    for entry in entries:
        if entry.get("type") == "session":
            context_flow["session_id"] = entry.get("id")
            context_flow["started_at"] = entry.get("timestamp")
            continue
        
        if entry.get("type") != "message":
            continue
        
        msg = entry.get("message", {})
        role = msg.get("role")
        
        if role == "user":
            if current_turn:
                context_flow["conversation_turns"].append(current_turn)
            
            user_text = ""
            for c in msg.get("content", []):
                if c.get("type") == "text":
                    user_text = c.get("text", "")
                    break
            
            current_turn = {
                "turn_id": len(context_flow["conversation_turns"]) + 1,
                "timestamp": entry.get("timestamp"),
                "user_message": user_text,
                "assistant_responses": [],
                "tool_calls": [],
                "tool_results": []
            }
        
        elif role == "assistant" and current_turn:
            usage = msg.get("usage", {})
            model = msg.get("model", "unknown")
            
            context_flow["context_stats"]["total_input_tokens"] += usage.get("input", 0)
            context_flow["context_stats"]["total_output_tokens"] += usage.get("output", 0)
            context_flow["context_stats"]["total_cache_read"] += usage.get("cacheRead", 0)
            context_flow["context_stats"]["total_cost"] += usage.get("cost", {}).get("total", 0)
            context_flow["context_stats"]["models_used"].add(model)
            
            response_text = ""
            thinking_text = ""
            for c in msg.get("content", []):
                if c.get("type") == "text":
                    response_text += c.get("text", "")
                elif c.get("type") == "thinking":
                    thinking_text += c.get("thinking", "") or ""
                elif c.get("type") == "toolCall":
                    current_turn["tool_calls"].append({
                        "id": c.get("id"),
                        "name": c.get("name"),
                        "arguments": c.get("arguments", {})
                    })
            
            current_turn["assistant_responses"].append({
                "timestamp": entry.get("timestamp"),
                "model": model,
                "text": response_text,
                "thinking": thinking_text,
                "token_usage": {
                    "input": usage.get("input", 0),
                    "output": usage.get("output", 0),
                    "cache_read": usage.get("cacheRead", 0),
                    "cost": usage.get("cost", {}).get("total", 0)
                }
            })
        
        elif role == "toolResult" and current_turn:
            tool_call_id = msg.get("toolCallId")
            tool_name = msg.get("toolName", "")
            
            result_text = ""
            for c in msg.get("content", []):
                if c.get("type") == "text":
                    result_text += c.get("text", "")
            
            details = msg.get("details", {})
            
            current_turn["tool_results"].append({
                "tool_call_id": tool_call_id,
                "tool_name": tool_name,
                "result": result_text,
                "details": {
                    "status": details.get("status"),
                    "exit_code": details.get("exitCode"),
                    "duration_ms": details.get("durationMs"),
                    "is_error": msg.get("isError", False)
                }
            })
    
    if current_turn:
        context_flow["conversation_turns"].append(current_turn)
    
    context_flow["context_stats"]["models_used"] = list(context_flow["context_stats"]["models_used"])
    context_flow["context_stats"]["total_turns"] = len(context_flow["conversation_turns"])
    
    return context_flow

def generate_html(data):
    """Generate interactive HTML viewer."""
    json_str = json.dumps(data, ensure_ascii=True)
    json_str = json_str.replace('</script>', '<\\/script>')
    
    html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OpenClaw Session Viewer</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, monospace; background: #0d1117; color: #c9d1d9; line-height: 1.6; }
        .container { display: flex; height: 100vh; }
        .sidebar { width: 320px; background: #161b22; border-right: 1px solid #30363d; display: flex; flex-direction: column; flex-shrink: 0; }
        .sidebar-header { padding: 20px; border-bottom: 1px solid #30363d; background: #0d1117; }
        .sidebar-header h1 { font-size: 1.2rem; color: #58a6ff; margin-bottom: 10px; }
        .stats { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; font-size: 0.75rem; }
        .stat { background: #21262d; padding: 8px; border-radius: 6px; }
        .stat-value { font-weight: bold; color: #7ee787; }
        .turn-list { flex: 1; overflow-y: auto; padding: 10px; }
        .turn-item { padding: 12px; margin-bottom: 8px; background: #21262d; border-radius: 8px; cursor: pointer; border: 2px solid transparent; }
        .turn-item:hover { background: #30363d; }
        .turn-item.active { border-color: #58a6ff; background: #1f6feb22; }
        .turn-number { font-weight: bold; color: #58a6ff; font-size: 0.85rem; }
        .turn-preview { font-size: 0.8rem; color: #8b949e; margin-top: 4px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
        .turn-meta { font-size: 0.7rem; color: #6e7681; margin-top: 6px; display: flex; gap: 10px; }
        .main-content { flex: 1; overflow-y: auto; padding: 30px; }
        .turn-detail { max-width: 1000px; margin: 0 auto; }
        .section { margin-bottom: 30px; background: #161b22; border-radius: 12px; border: 1px solid #30363d; overflow: hidden; }
        .section-header { padding: 15px 20px; background: #21262d; border-bottom: 1px solid #30363d; display: flex; justify-content: space-between; align-items: center; }
        .section-title { font-weight: 600; display: flex; align-items: center; gap: 10px; }
        .section-body { padding: 20px; }
        .message-content { white-space: pre-wrap; word-break: break-word; font-family: monospace; font-size: 0.9rem; line-height: 1.7; background: #0d1117; padding: 15px; border-radius: 8px; max-height: 500px; overflow-y: auto; }
        .user-message { border-left: 4px solid #3fb950; }
        .assistant-message { border-left: 4px solid #58a6ff; }
        .thinking-message { border-left: 4px solid #a371f7; }
        .tool-call { border-left: 4px solid #f0883e; }
        .tool-result { border-left: 4px solid #3fb950; }
        .tool-item { margin-bottom: 20px; background: #0d1117; border-radius: 8px; overflow: hidden; }
        .tool-header { padding: 10px 15px; background: #21262d; font-weight: 600; font-size: 0.85rem; display: flex; justify-content: space-between; }
        .tool-name { color: #f0883e; }
        .tool-body { padding: 15px; font-family: monospace; font-size: 0.85rem; white-space: pre-wrap; word-break: break-word; max-height: 400px; overflow-y: auto; }
        .badge { display: inline-block; padding: 2px 8px; border-radius: 12px; font-size: 0.7rem; font-weight: 600; }
        .badge-model { background: #388bfd33; color: #58a6ff; }
        .badge-tokens { background: #3fb95033; color: #7ee787; }
        .badge-success { background: #3fb95033; color: #3fb950; }
        .badge-error { background: #f8514933; color: #f85149; }
        .empty-state { text-align: center; padding: 60px 20px; color: #6e7681; }
        .nav-buttons { display: flex; gap: 10px; margin-top: 20px; justify-content: center; }
        .nav-btn { padding: 10px 20px; background: #21262d; border: 1px solid #30363d; color: #c9d1d9; border-radius: 6px; cursor: pointer; }
        .nav-btn:hover { background: #30363d; }
        .nav-btn:disabled { opacity: 0.5; cursor: not-allowed; }
        .timestamp { color: #6e7681; font-size: 0.8rem; }
        .collapsible-header { cursor: pointer; }
        .collapsible-header::after { content: ' ▼'; font-size: 0.7rem; }
        .collapsible-header.collapsed::after { content: ' ▶'; }
        .collapsible-body.collapsed { display: none; }
        .search-box { padding: 10px 20px; border-bottom: 1px solid #30363d; }
        .search-input { width: 100%; padding: 8px 12px; background: #0d1117; border: 1px solid #30363d; border-radius: 6px; color: #c9d1d9; }
        .search-input:focus { outline: none; border-color: #58a6ff; }
    </style>
</head>
<body>
    <div class="container">
        <div class="sidebar">
            <div class="sidebar-header">
                <h1>🦞 Session Viewer</h1>
                <div class="stats" id="stats"></div>
            </div>
            <div class="search-box">
                <input type="text" class="search-input" placeholder="Search..." id="searchInput">
            </div>
            <div class="turn-list" id="turnList"></div>
        </div>
        <div class="main-content" id="mainContent">
            <div class="empty-state"><h2>Select a turn</h2></div>
        </div>
    </div>
    <script>
        var data = ''' + json_str + ''';
        var currentTurn = 0;
        var filteredTurns = data.conversation_turns;

        function esc(t) { var d = document.createElement('div'); d.textContent = t || ''; return d.innerHTML; }
        function fmtTime(ts) { return new Date(ts).toLocaleString('zh-CN', {month:'short',day:'numeric',hour:'2-digit',minute:'2-digit'}); }
        
        function renderStats() {
            var s = data.context_stats;
            document.getElementById('stats').innerHTML =
                '<div class="stat"><div class="stat-value">'+s.total_turns+'</div><div>Turns</div></div>'+
                '<div class="stat"><div class="stat-value">'+(s.total_input_tokens/1000).toFixed(1)+'K</div><div>In Tokens</div></div>'+
                '<div class="stat"><div class="stat-value">'+(s.total_output_tokens/1000).toFixed(1)+'K</div><div>Out Tokens</div></div>'+
                '<div class="stat"><div class="stat-value">$'+s.total_cost.toFixed(2)+'</div><div>Cost</div></div>';
        }
        
        function renderList() {
            var h = '';
            for (var i = 0; i < filteredTurns.length; i++) {
                var t = filteredTurns[i];
                var preview = (t.user_message || '').replace(/^Sender.*?\\n\\n/s,'').substring(0,80);
                h += '<div class="turn-item'+(i===currentTurn?' active':'')+'" onclick="sel('+i+')">'+
                    '<div class="turn-number">Turn #'+t.turn_id+'</div>'+
                    '<div class="turn-preview">'+esc(preview)+'...</div>'+
                    '<div class="turn-meta"><span>🕐 '+fmtTime(t.timestamp)+'</span>'+
                    (t.tool_calls.length?'<span>🔧'+t.tool_calls.length+'</span>':'')+
                    (t.tool_results.length?'<span>📤'+t.tool_results.length+'</span>':'')+'</div></div>';
            }
            document.getElementById('turnList').innerHTML = h;
        }
        
        function sel(i) { currentTurn = i; renderList(); renderDetail(filteredTurns[i]); }
        
        function renderDetail(t) {
            var h = '<div class="turn-detail">';
            h += '<div class="section"><div class="section-header"><div class="section-title">👤 User</div><span class="timestamp">'+fmtTime(t.timestamp)+'</span></div>';
            h += '<div class="section-body"><div class="message-content user-message">'+esc(t.user_message)+'</div></div></div>';
            
            for (var i = 0; i < t.assistant_responses.length; i++) {
                var r = t.assistant_responses[i];
                h += '<div class="section"><div class="section-header"><div class="section-title">🤖 Assistant</div>';
                h += '<div><span class="badge badge-model">'+r.model+'</span> <span class="badge badge-tokens">'+(r.token_usage.input+r.token_usage.output)+' tok</span></div></div>';
                h += '<div class="section-body">';
                if (r.thinking) {
                    h += '<div style="margin-bottom:15px"><div class="collapsible-header" onclick="tog(this)"><strong>💭 Thinking</strong></div>';
                    h += '<div class="collapsible-body"><div class="message-content thinking-message" style="margin-top:10px">'+esc(r.thinking)+'</div></div></div>';
                }
                h += '<div class="message-content assistant-message">'+esc(r.text)+'</div></div></div>';
            }
            
            if (t.tool_calls.length) {
                h += '<div class="section"><div class="section-header"><div class="section-title">🔧 Tool Calls ('+t.tool_calls.length+')</div></div><div class="section-body">';
                for (var i = 0; i < t.tool_calls.length; i++) {
                    var tc = t.tool_calls[i];
                    h += '<div class="tool-item"><div class="tool-header"><span class="tool-name">'+tc.name+'</span><span style="color:#6e7681;font-size:0.75rem">'+tc.id+'</span></div>';
                    h += '<div class="tool-body tool-call">'+esc(JSON.stringify(tc.arguments,null,2))+'</div></div>';
                }
                h += '</div></div>';
            }
            
            if (t.tool_results.length) {
                h += '<div class="section"><div class="section-header"><div class="section-title">📤 Tool Results ('+t.tool_results.length+')</div></div><div class="section-body">';
                for (var i = 0; i < t.tool_results.length; i++) {
                    var tr = t.tool_results[i];
                    var badge = tr.details.is_error ? '<span class="badge badge-error">Error</span>' : '<span class="badge badge-success">OK</span>';
                    h += '<div class="tool-item"><div class="tool-header"><span class="tool-name">'+(tr.tool_name||'exec')+'</span>'+badge+'</div>';
                    h += '<div class="tool-body tool-result">'+esc(tr.result)+'</div></div>';
                }
                h += '</div></div>';
            }
            
            h += '<div class="nav-buttons">';
            h += '<button class="nav-btn" onclick="sel('+(currentTurn-1)+')"'+(currentTurn===0?' disabled':'')+'>← Prev</button>';
            h += '<button class="nav-btn" onclick="sel('+(currentTurn+1)+')"'+(currentTurn>=filteredTurns.length-1?' disabled':'')+'>Next →</button>';
            h += '</div></div>';
            document.getElementById('mainContent').innerHTML = h;
        }
        
        function tog(el) { el.classList.toggle('collapsed'); el.nextElementSibling.classList.toggle('collapsed'); }
        
        document.getElementById('searchInput').addEventListener('input', function(e) {
            var q = e.target.value.toLowerCase();
            if (!q) { filteredTurns = data.conversation_turns; }
            else {
                filteredTurns = data.conversation_turns.filter(function(t) {
                    return t.user_message.toLowerCase().indexOf(q) >= 0 ||
                        t.assistant_responses.some(function(r) { return r.text.toLowerCase().indexOf(q) >= 0; }) ||
                        t.tool_calls.some(function(tc) { return JSON.stringify(tc.arguments).toLowerCase().indexOf(q) >= 0; }) ||
                        t.tool_results.some(function(r) { return r.result.toLowerCase().indexOf(q) >= 0; });
                });
            }
            currentTurn = 0; renderList();
            if (filteredTurns.length) renderDetail(filteredTurns[0]);
            else document.getElementById('mainContent').innerHTML = '<div class="empty-state"><h2>No results</h2></div>';
        });
        
        document.addEventListener('keydown', function(e) {
            if (e.target.tagName === 'INPUT') return;
            if (e.key === 'ArrowDown' || e.key === 'j') { if (currentTurn < filteredTurns.length-1) sel(currentTurn+1); }
            if (e.key === 'ArrowUp' || e.key === 'k') { if (currentTurn > 0) sel(currentTurn-1); }
        });
        
        renderStats(); renderList(); if (filteredTurns.length) sel(0);
    </script>
</body>
</html>'''
    return html

def main():
    parser = argparse.ArgumentParser(description='Extract OpenClaw session and generate viewer')
    parser.add_argument('--agent', default='main', help='Agent ID (default: main)')
    parser.add_argument('--session-id', help='Specific session ID')
    parser.add_argument('--output', '-o', default='/tmp/session_viewer.html', help='Output HTML file')
    parser.add_argument('--list', '-l', action='store_true', help='List available sessions')
    parser.add_argument('--json', action='store_true', help='Output JSON instead of HTML')
    
    args = parser.parse_args()
    
    if args.list:
        list_sessions(args.agent)
        return
    
    try:
        if args.session_id:
            session_file = get_openclaw_dir() / "agents" / args.agent / "sessions" / f"{args.session_id}.jsonl"
        else:
            session_file = get_current_session_file(args.agent)
        
        print(f"Extracting: {session_file}")
        data = extract_session(session_file)
        
        if args.json:
            output_file = args.output.replace('.html', '.json')
            with open(output_file, 'w') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"✅ Saved JSON: {output_file}")
        else:
            html = generate_html(data)
            with open(args.output, 'w') as f:
                f.write(html)
            print(f"✅ Saved HTML: {args.output}")
            print(f"   Turns: {data['context_stats']['total_turns']}")
            print(f"   Tokens: {data['context_stats']['total_input_tokens'] + data['context_stats']['total_output_tokens']}")
        
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
