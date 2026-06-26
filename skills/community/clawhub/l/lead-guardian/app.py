#!/usr/bin/env python3
"""
AI Lead Autoresponder — RAIYA Clone MVP
Instant AI text response to incoming leads with qualification and handoff.

Requirements:
  pip install flask twilio openai python-dotenv

Environment variables needed (.env):
  TWILIO_ACCOUNT_SID=your_account_sid
  TWILIO_AUTH_TOKEN=your_auth_token
  TWILIO_PHONE_NUMBER=+1xxxxxxxxxx
  OPENROUTER_API_KEY=your_openrouter_key
  AGENT_PHONE=+1xxxxxxxxxx  # Jon's phone for hot lead alerts
"""

import os
import json
import sqlite3
from datetime import datetime
from flask import Flask, request, jsonify, render_template_string
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
import requests

load_dotenv()

app = Flask(__name__)
DB_PATH = os.path.join(os.path.dirname(__file__), 'leads.db')

# ============================================
# DATABASE
# ============================================

def init_db():
    """Initialize SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone TEXT NOT NULL,
            name TEXT,
            stage TEXT DEFAULT 'intro',
            direction TEXT,
            timeline TEXT,
            preapproved TEXT,
            price_range TEXT,
            created_at TEXT,
            updated_at TEXT,
            handed_off INTEGER DEFAULT 0
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id INTEGER,
            role TEXT,
            content TEXT,
            timestamp TEXT,
            FOREIGN KEY (conversation_id) REFERENCES conversations(id)
        )
    ''')
    conn.commit()
    conn.close()

def get_conversation(phone):
    """Get or create conversation for a phone number."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM conversations WHERE phone = ?', (phone,))
    row = c.fetchone()
    
    if row:
        conv = {
            'id': row[0], 'phone': row[1], 'name': row[2], 'stage': row[3],
            'direction': row[4], 'timeline': row[5], 'preapproved': row[6],
            'price_range': row[7], 'created_at': row[8], 'updated_at': row[9],
            'handed_off': row[10]
        }
    else:
        now = datetime.now().isoformat()
        c.execute('''
            INSERT INTO conversations (phone, stage, created_at, updated_at)
            VALUES (?, 'intro', ?, ?)
        ''', (phone, now, now))
        conn.commit()
        conv = {
            'id': c.lastrowid, 'phone': phone, 'name': None, 'stage': 'intro',
            'direction': None, 'timeline': None, 'preapproved': None,
            'price_range': None, 'created_at': now, 'updated_at': now,
            'handed_off': 0
        }
    
    conn.close()
    return conv

def update_conversation(conv_id, **kwargs):
    """Update conversation fields."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    kwargs['updated_at'] = datetime.now().isoformat()
    
    updates = ', '.join(f'{k} = ?' for k in kwargs.keys())
    values = list(kwargs.values()) + [conv_id]
    c.execute(f'UPDATE conversations SET {updates} WHERE id = ?', values)
    conn.commit()
    conn.close()

def add_message(conv_id, role, content):
    """Add a message to conversation history."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO messages (conversation_id, role, content, timestamp)
        VALUES (?, ?, ?, ?)
    ''', (conv_id, role, content, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_messages(conv_id, limit=20):
    """Get recent messages for a conversation."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        SELECT role, content FROM messages
        WHERE conversation_id = ?
        ORDER BY id DESC LIMIT ?
    ''', (conv_id, limit))
    rows = c.fetchall()
    conn.close()
    return [{'role': r[0], 'content': r[1]} for r in reversed(rows)]

# ============================================
# AI RESPONSE GENERATION
# ============================================

SYSTEM_PROMPT = """You are Sabine, assistant to Jon Barnato, a real estate agent in Sacramento, California.
You're texting with someone who inquired about real estate. Be friendly, professional, and brief.

Your goals:
1. Qualify them: Are they buying, selling, or both?
2. Timeline: When are they looking to make a move?
3. Pre-approval: Are they pre-approved for a mortgage? (if buying)
4. Price range: What price range works? (if buying)

If they seem ready (timeline < 3 months, pre-approved, or very interested), let them know Jon will reach out directly.

Current conversation state:
- Direction: {direction}
- Timeline: {timeline}
- Pre-approved: {preapproved}
- Price range: {price_range}

Respond naturally with one short text message. No emojis unless the lead uses them first.
Don't repeat questions they've already answered."""

def generate_response(conv, user_message):
    """Generate AI response using OpenRouter."""
    api_key = os.getenv('OPENROUTER_API_KEY')
    if not api_key:
        return "Thanks for reaching out! Jon will get back to you shortly."
    
    messages = get_messages(conv['id'])
    
    system = SYSTEM_PROMPT.format(
        direction=conv['direction'] or 'unknown',
        timeline=conv['timeline'] or 'unknown',
        preapproved=conv['preapproved'] or 'unknown',
        price_range=conv['price_range'] or 'unknown'
    )
    
    api_messages = [{'role': 'system', 'content': system}]
    for m in messages:
        api_messages.append({'role': 'user' if m['role'] == 'lead' else 'assistant', 'content': m['content']})
    api_messages.append({'role': 'user', 'content': user_message})
    
    try:
        response = requests.post(
            'https://openrouter.ai/api/v1/chat/completions',
            headers={
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            },
            json={
                'model': 'anthropic/claude-3-haiku',
                'messages': api_messages,
                'max_tokens': 150
            }
        )
        data = response.json()
        return data['choices'][0]['message']['content']
    except Exception as e:
        print(f"AI error: {e}")
        return "Thanks for your message! Jon will follow up with you shortly."

def extract_qualification(message, conv):
    """Extract qualification info from message."""
    lower = message.lower()
    updates = {}
    
    # Direction
    if any(w in lower for w in ['buy', 'buying', 'purchase', 'looking for a home']):
        updates['direction'] = 'buy'
    elif any(w in lower for w in ['sell', 'selling', 'list my']):
        updates['direction'] = 'sell'
    elif 'both' in lower:
        updates['direction'] = 'both'
    
    # Timeline
    if any(w in lower for w in ['asap', 'right now', 'immediately', 'this week', 'this month']):
        updates['timeline'] = 'immediate'
    elif any(w in lower for w in ['1-3 months', 'couple months', 'few months', 'next month']):
        updates['timeline'] = '1-3 months'
    elif any(w in lower for w in ['6 months', 'next year', 'not sure', 'just looking']):
        updates['timeline'] = '6+ months'
    
    # Pre-approval
    if any(w in lower for w in ['pre-approved', 'preapproved', 'pre approved', 'already approved']):
        updates['preapproved'] = 'yes'
    elif any(w in lower for w in ['not yet', 'no approval', 'haven\'t been approved']):
        updates['preapproved'] = 'no'
    
    # Price range (basic extraction)
    import re
    price_match = re.search(r'\$?(\d{2,3})[,\s]?(\d{3})?k?', lower)
    if price_match:
        updates['price_range'] = message[price_match.start():price_match.end()]
    
    return updates

def is_hot_lead(conv):
    """Determine if lead should be handed off to agent."""
    if conv['timeline'] in ['immediate', '1-3 months']:
        return True
    if conv['preapproved'] == 'yes':
        return True
    return False

# ============================================
# TWILIO INTEGRATION
# ============================================

def send_sms(to, message):
    """Send SMS via Twilio."""
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    from_number = os.getenv('TWILIO_PHONE_NUMBER')
    
    if not all([account_sid, auth_token, from_number]):
        print(f"Would send to {to}: {message}")
        return
    
    client = Client(account_sid, auth_token)
    client.messages.create(to=to, from_=from_number, body=message)

def alert_agent(conv, summary):
    """Alert Jon about a hot lead."""
    agent_phone = os.getenv('AGENT_PHONE')
    if not agent_phone:
        print(f"HOT LEAD: {summary}")
        return
    
    alert = f"🔥 HOT LEAD\nPhone: {conv['phone']}\n{summary}"
    send_sms(agent_phone, alert)

# ============================================
# ROUTES
# ============================================

@app.route('/sms', methods=['POST'])
def sms_webhook():
    """Handle incoming SMS from Twilio."""
    from_number = request.form.get('From')
    body = request.form.get('Body', '').strip()
    
    if not from_number or not body:
        return str(MessagingResponse())
    
    # Get or create conversation
    conv = get_conversation(from_number)
    
    # Log incoming message
    add_message(conv['id'], 'lead', body)
    
    # Check if already handed off
    if conv['handed_off']:
        # Don't auto-respond, Jon is handling it
        return str(MessagingResponse())
    
    # Extract qualification info
    updates = extract_qualification(body, conv)
    if updates:
        update_conversation(conv['id'], **updates)
        conv.update(updates)
    
    # Check if hot lead
    if is_hot_lead(conv) and not conv['handed_off']:
        summary = f"Direction: {conv['direction']}, Timeline: {conv['timeline']}, Pre-approved: {conv['preapproved']}"
        alert_agent(conv, summary)
        update_conversation(conv['id'], handed_off=1, stage='handed_off')
        
        response = "Great! Jon is perfect for this — he'll reach out to you directly very soon."
    else:
        # Generate AI response
        response = generate_response(conv, body)
    
    # Log and send response
    add_message(conv['id'], 'assistant', response)
    
    resp = MessagingResponse()
    resp.message(response)
    return str(resp)

@app.route('/api/leads', methods=['GET'])
def list_leads():
    """List all leads for admin dashboard."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        SELECT id, phone, name, stage, direction, timeline, preapproved, 
               price_range, created_at, updated_at, handed_off
        FROM conversations ORDER BY updated_at DESC
    ''')
    rows = c.fetchall()
    conn.close()
    
    leads = []
    for r in rows:
        leads.append({
            'id': r[0], 'phone': r[1], 'name': r[2], 'stage': r[3],
            'direction': r[4], 'timeline': r[5], 'preapproved': r[6],
            'price_range': r[7], 'created_at': r[8], 'updated_at': r[9],
            'handed_off': bool(r[10])
        })
    
    return jsonify({'leads': leads})

@app.route('/api/leads/<int:lead_id>/messages', methods=['GET'])
def get_lead_messages(lead_id):
    """Get messages for a specific lead."""
    messages = get_messages(lead_id, limit=50)
    return jsonify({'messages': messages})

@app.route('/api/leads/<int:lead_id>/handoff', methods=['POST'])
def mark_handoff(lead_id):
    """Manually mark a lead as handed off."""
    update_conversation(lead_id, handed_off=1, stage='handed_off')
    return jsonify({'status': 'ok'})

@app.route('/')
def dashboard():
    """Admin dashboard HTML."""
    return render_template_string(DASHBOARD_HTML)

# ============================================
# DASHBOARD HTML
# ============================================

DASHBOARD_HTML = '''
<!DOCTYPE html>
<html>
<head>
<title>Lead Autoresponder Dashboard</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: -apple-system, sans-serif; background: #0D0D0F; color: #F0F0F5; }
.container { max-width: 1200px; margin: 0 auto; padding: 24px; }
h1 { margin-bottom: 24px; }
.lead-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }
@media (max-width: 800px) { .lead-grid { grid-template-columns: 1fr; } }
.lead-list { background: #16161A; border-radius: 10px; padding: 16px; max-height: 600px; overflow-y: auto; }
.lead-item { padding: 12px; border-bottom: 1px solid #2A2A33; cursor: pointer; }
.lead-item:hover { background: #1E1E24; }
.lead-item.hot { border-left: 3px solid #EF4444; }
.lead-item.active { background: #2A2A33; }
.lead-phone { font-weight: 600; }
.lead-meta { font-size: 12px; color: #888; margin-top: 4px; }
.chat-panel { background: #16161A; border-radius: 10px; padding: 16px; }
.chat-messages { max-height: 400px; overflow-y: auto; margin-bottom: 16px; }
.msg { padding: 8px 12px; margin: 4px 0; border-radius: 8px; max-width: 80%; }
.msg.lead { background: #2A2A33; margin-right: auto; }
.msg.assistant { background: #C8102E; margin-left: auto; }
.badge { display: inline-block; padding: 2px 8px; border-radius: 10px; font-size: 11px; }
.badge.hot { background: rgba(239,68,68,0.2); color: #EF4444; }
.badge.qualified { background: rgba(234,179,8,0.2); color: #EAB308; }
.badge.new { background: rgba(34,197,94,0.2); color: #22C55E; }
</style>
</head>
<body>
<div class="container">
    <h1>🤖 Lead Autoresponder</h1>
    <div class="lead-grid">
        <div class="lead-list" id="leads"></div>
        <div class="chat-panel">
            <h3 id="chat-title">Select a lead</h3>
            <div class="chat-messages" id="messages"></div>
        </div>
    </div>
</div>
<script>
let selectedLead = null;

async function loadLeads() {
    const res = await fetch('/api/leads');
    const data = await res.json();
    const container = document.getElementById('leads');
    
    container.innerHTML = data.leads.map(l => {
        const isHot = l.timeline === 'immediate' || l.timeline === '1-3 months' || l.preapproved === 'yes';
        let badge = '<span class="badge new">New</span>';
        if (l.handed_off) badge = '<span class="badge hot">Handed Off</span>';
        else if (isHot) badge = '<span class="badge hot">Hot</span>';
        else if (l.direction) badge = '<span class="badge qualified">Qualifying</span>';
        
        return `
            <div class="lead-item ${isHot ? 'hot' : ''}" onclick="selectLead(${l.id})">
                <div class="lead-phone">${l.phone} ${badge}</div>
                <div class="lead-meta">
                    ${l.direction || 'Unknown'} | ${l.timeline || 'No timeline'} | 
                    ${new Date(l.updated_at).toLocaleString()}
                </div>
            </div>`;
    }).join('');
}

async function selectLead(id) {
    selectedLead = id;
    document.querySelectorAll('.lead-item').forEach(el => el.classList.remove('active'));
    event.currentTarget.classList.add('active');
    
    const res = await fetch(`/api/leads/${id}/messages`);
    const data = await res.json();
    
    document.getElementById('chat-title').textContent = `Conversation #${id}`;
    document.getElementById('messages').innerHTML = data.messages.map(m => 
        `<div class="msg ${m.role}">${m.content}</div>`
    ).join('');
}

loadLeads();
setInterval(loadLeads, 30000);
</script>
</body>
</html>
'''

if __name__ == '__main__':
    init_db()
    print("Lead Autoresponder running on http://localhost:5001")
    app.run(host='0.0.0.0', port=5001, debug=True)
