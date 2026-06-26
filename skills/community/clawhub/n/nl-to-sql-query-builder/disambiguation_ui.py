#!/usr/bin/env python3
"""
Disambiguation UI - Flask components for user clarification
Part of NL-to-SQL Query Builder skill
"""
from flask import Flask, request, jsonify, render_template_string
from typing import Dict, List, Any, Optional
import json


app = Flask(__name__)

# In-memory session store (use Redis in production)
clarification_sessions = {}


class DisambiguationUI:
    """Handle user clarification for ambiguous queries"""
    
    def __init__(self, session_timeout_minutes: int = 10):
        self.session_timeout = session_timeout_minutes * 60
        
    def create_clarification_request(
        self,
        session_id: str,
        original_query: str,
        ambiguities: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Create a clarification request for user"""
        clarification = {
            'session_id': session_id,
            'original_query': original_query,
            'ambiguities': ambiguities,
            'options': self._generate_options(ambiguities),
            'created_at': None  # Set by caller
        }
        clarification_sessions[session_id] = clarification
        return clarification
    
    def _generate_options(self, ambiguities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate options for each ambiguity"""
        options = []
        for amb in ambiguities:
            options.append({
                'field': amb['field'],
                'question': amb['question'],
                'choices': amb.get('choices', []),
                'allow_custom': amb.get('allow_custom', True)
            })
        return options
    
    def resolve_clarification(
        self,
        session_id: str,
        answers: Dict[str, str]
    ) -> Optional[Dict[str, Any]]:
        """Resolve clarification and return refined query context"""
        session = clarification_sessions.get(session_id)
        if not session:
            return None
        
        # Store answers
        session['answers'] = answers
        session['resolved_at'] = 'now'  # Set by caller
        
        return session


# HTML Template for clarification UI
CLARIFICATION_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Query Clarification</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 600px; margin: 40px auto; padding: 20px; }
        .ambiguity { margin-bottom: 24px; padding: 16px; border: 1px solid #e0e0e0; border-radius: 8px; }
        .ambiguity h3 { margin-top: 0; color: #333; }
        .choices { display: flex; flex-direction: column; gap: 8px; }
        .choice { padding: 10px 14px; border: 1px solid #ccc; border-radius: 6px; cursor: pointer; transition: all 0.2s; }
        .choice:hover { border-color: #666; background: #f9f9f9; }
        .choice.selected { border-color: #0066cc; background: #e6f0ff; }
        input[type="text"] { width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 6px; }
        button { background: #0066cc; color: white; padding: 12px 24px; border: none; border-radius: 6px; cursor: pointer; font-size: 16px; }
        button:hover { background: #0055aa; }
    </style>
</head>
<body>
    <h1>Query Clarification Needed</h1>
    <p><strong>Original query:</strong> {{ original_query }}</p>
    
    <form method="POST" action="/clarify/{{ session_id }}">
        {% for option in options %}
        <div class="ambiguity">
            <h3>{{ option.question }}</h3>
            <input type="hidden" name="field" value="{{ option.field }}">
            {% if option.choices %}
            <div class="choices">
                {% for choice in option.choices %}
                <label class="choice">
                    <input type="radio" name="{{ option.field }}" value="{{ choice }}" required>
                    {{ choice }}
                </label>
                {% endfor %}
            </div>
            {% endif %}
            {% if option.allow_custom %}
            <input type="text" name="{{ option.field }}_custom" placeholder="Or specify your own...">
            {% endif %}
        </div>
        {% endfor %}
        <button type="submit">Submit Clarification</button>
    </form>
</body>
</html>
"""


@app.route('/clarify/<session_id>', methods=['GET', 'POST'])
def clarify(session_id):
    """Render or process clarification UI"""
    session = clarification_sessions.get(session_id)
    if not session:
        return jsonify({'error': 'Session not found'}), 404
    
    if request.method == 'GET':
        return render_template_string(
            CLARIFICATION_HTML,
            original_query=session['original_query'],
            options=session['options'],
            session_id=session_id
        )
    
    # POST - process answers
    answers = {}
    for key, value in request.form.items():
        if key.endswith('_custom') and value:
            field = key[:-7]
            answers[field] = value
        elif not key.endswith('_custom'):
            answers[key] = value
    
    return jsonify({'status': 'clarified', 'answers': answers})


def create_app():
    """Create Flask app for disambiguation"""
    return app


if __name__ == '__main__':
    app.run(debug=True, port=5000)